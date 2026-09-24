"""Vendor patterns with a real `ibek pattern add` and check the result.

Each pattern is added from this working copy into its own instance of a scratch
services repo, then:

- ``runtime-lock.yaml`` lists exactly the files the pattern's manifest vendors,
  each with the sha256 of the file written;
- each vendored file is byte-identical to the library file it came from, and
  nothing else (``docs/``, ``sim/``, ``test/``) reaches the instance;
- ``ioc.schema.json`` defines every entity model of the pattern;
- ``ibek pattern check`` passes, and fails once a vendored file is edited.

A sample of patterns is also added together into one instance, as an IOC
using several devices would, and checked the same way.

usage: uv run --with-requirements ci/requirements.txt ci/check_pattern_add.py
           [--keep DIR] [PATTERN...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from patterns import ROOT, SUPPORT_SUFFIX, select_patterns, vendored_files
from ruamel.yaml import YAML

LIBRARY = "ibek-runtime-streamdevice"
# The image the instances pin; ibek fetches its published ioc.schema.json as
# the base of each instance schema. Keep in step with IMAGE in ci.yml.
IMAGE = "ghcr.io/epics-containers/ioc-streamdevice-runtime:2.8.26ec4"
# Patterns added together into one instance.
SAMPLE = ["eurotherm2k", "lakeshore340", "oxCryo", "gardasoftLED"]


def ibek(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "ibek", *args], capture_output=True, text=True
    )


def make_instance(services: Path, name: str) -> Path:
    instance = services / name
    (instance / "config").mkdir(parents=True)
    (instance / "values.yaml").write_text(f"ioc-instance:\n  image: {IMAGE}\n")
    (instance / "config" / "ioc.yaml").write_text(
        f"ioc_name: {name}\ndescription: scratch instance for {name}\nentities: []\n"
    )
    return instance


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def entity_types(pattern: Path) -> set[str]:
    types = set()
    for support in pattern.glob(f"*{SUPPORT_SUFFIX}"):
        data = YAML(typ="safe").load(support)
        types |= {f"{data['module']}.{m['name']}" for m in data["entity_models"]}
    return types


def schema_types(schema: Path) -> set[str]:
    found: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            const = node.get("properties", {}).get("type", {}).get("const")
            if isinstance(const, str):
                found.add(const)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(json.loads(schema.read_text()))
    return found


def check_instance(instance: Path, patterns: list[Path]) -> list[str]:
    problems = []
    lock = YAML(typ="safe").load(instance / "runtime-lock.yaml") or {}
    locked = lock.get("patterns", {})
    expected_files = {
        "values.yaml",
        "config/ioc.yaml",
        "runtime-lock.yaml",
        "ioc.schema.json",
    }
    for pattern in patterns:
        entry = locked.get(pattern.name)
        if entry is None:
            problems.append(f"{pattern.name}: not in runtime-lock.yaml")
            continue
        if entry.get("source") != str(ROOT):
            problems.append(f"{pattern.name}: lock source is {entry.get('source')!r}")
        plan = dict((key, src) for src, key in vendored_files(pattern))
        files = entry.get("files", {})
        for key in sorted(set(plan) ^ set(files)):
            where = "the lock" if key in files else "the manifest plan"
            problems.append(f"{pattern.name}: {key} is only in {where}")
        for key in sorted(set(plan) & set(files)):
            written = instance / key
            if not written.is_file():
                problems.append(f"{pattern.name}: {key} was not written")
            elif written.read_bytes() != plan[key].read_bytes():
                problems.append(f"{pattern.name}: {key} differs from the library file")
            elif files[key] != sha256(written):
                problems.append(f"{pattern.name}: {key} hash in lock does not match")
        expected_files |= set(plan)
    written = {
        p.relative_to(instance).as_posix() for p in instance.rglob("*") if p.is_file()
    }
    for extra in sorted(written - expected_files):
        problems.append(f"{extra} is in the instance but not in the lock")

    schema = instance / "ioc.schema.json"
    if not schema.is_file():
        problems.append("ioc.schema.json was not written")
    else:
        defined = schema_types(schema)
        for pattern in patterns:
            for missing in sorted(entity_types(pattern) - defined):
                problems.append(f"{pattern.name}: ioc.schema.json lacks {missing}")

    result = ibek("pattern", "check", str(instance))
    if result.returncode != 0:
        problems.append(f"ibek pattern check failed: {result.stderr.strip()}")
    return problems


def check_tamper(instance: Path) -> list[str]:
    """`ibek pattern check` must fail once a vendored file is edited."""
    target = next(
        p
        for p in sorted((instance / "config").iterdir())
        if p.suffix == ".proto" or p.suffix == ".template"
    )
    target.write_bytes(target.read_bytes() + b"\n# edited\n")
    result = ibek("pattern", "check", str(instance))
    if result.returncode == 0:
        return [f"ibek pattern check passed with {target.name} edited"]
    return []


def add(instance: Path, pattern: Path) -> list[str]:
    result = ibek(
        "pattern",
        "add",
        f"{LIBRARY}:{pattern.name}",
        str(instance),
        "--source",
        str(ROOT),
    )
    if result.returncode != 0:
        output = (result.stderr or result.stdout).strip()
        return [f"{pattern.name}: ibek pattern add failed: {output}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "patterns", nargs="*", help="pattern folder names (default: every pattern)"
    )
    parser.add_argument(
        "--keep", type=Path, help="build the scratch services repo here and keep it"
    )
    args = parser.parse_args()

    services_root = args.keep or Path(tempfile.mkdtemp(prefix="pattern-add-"))
    services = services_root / "services"
    if services.exists():
        shutil.rmtree(services)
    patterns = select_patterns(args.patterns)
    failures = 0

    for pattern in patterns:
        instance = make_instance(services, pattern.name)
        problems = add(instance, pattern) or check_instance(instance, [pattern])
        for problem in problems:
            print(f"FAIL {pattern.name}: {problem}")
        failures += bool(problems)

    sample = [ROOT / name for name in SAMPLE]
    instance = make_instance(services, "sample")
    problems = []
    for pattern in sample:
        problems += add(instance, pattern)
    if not problems:
        problems = check_instance(instance, sample) or check_tamper(instance)
    for problem in problems:
        print(f"FAIL sample instance ({', '.join(SAMPLE)}): {problem}")
    failures += bool(problems)

    if not args.keep:
        shutil.rmtree(services_root)
    print(
        f"pattern add: {len(patterns) + 1 - failures} of {len(patterns) + 1} "
        "instances vendored and checked"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
