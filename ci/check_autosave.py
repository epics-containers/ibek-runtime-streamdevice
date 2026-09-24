"""Check each pattern's autosave .req files against its templates' autosave tags.

A template marks a record for autosave with a DLS tag comment,
``# % autosave <level> <FIELD> [<FIELD>...]``, which applies to the record it
sits in or, outside a record, to the next record. Level 0 is restored before
``iocInit`` and goes to ``<template>_positions.req``; levels 1 and 2 go to
``<template>_settings.req``. A ``.req`` names one PV per line, ``VAL`` as the
bare record name (autosave reads only the first token of a line).

For every vendored template and ``.req`` this checks that:

- each template with tags ships the matching ``.req`` files;
- each ``.req`` holds exactly the PVs its template's tags give;
- each ``.req`` belongs to a vendored template and names only its records.

Known differences are listed, with the reason, in ci/autosave-allow.yaml.

usage: uv run --with-requirements ci/requirements.txt ci/check_autosave.py [PATTERN...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from patterns import pattern_arg_parser, select_patterns, vendored_files
from ruamel.yaml import YAML

ALLOW_FILE = Path(__file__).with_name("autosave-allow.yaml")

TAG_RE = re.compile(r"^\s*#+\s*%\s*autosave\s+(\d)\s*(.*?)\s*$")
RECORD_RE = re.compile(r'^\s*g?record\s*\(\s*[^,]+,\s*(?:"([^"]*)"|([^\s")]+))\s*\)')
TEMPLATE_SUFFIXES = (".template", ".db")
REQ_KINDS = {0: "positions", 1: "settings", 2: "settings"}


def strip_comment(line: str) -> str:
    """The line with any trailing ``#`` comment removed, ignoring ``#`` in strings."""
    in_string = False
    for i, char in enumerate(line):
        if char == '"' and (i == 0 or line[i - 1] != "\\"):
            in_string = not in_string
        elif char == "#" and not in_string:
            return line[:i]
    return line


def tagged_pvs(template: Path) -> dict[str, set[str]]:
    """{"positions"|"settings": {PV, ...}} from a template's autosave tags."""
    result: dict[str, set[str]] = {"positions": set(), "settings": set()}
    pending: list[tuple[int, list[str]]] = []
    current: str | None = None
    depth = 0

    def add(record: str, level: int, fields: list[str]) -> None:
        for field in fields or ["VAL"]:
            pv = record if field == "VAL" else f"{record}.{field}"
            result[REQ_KINDS[level]].add(pv)

    for line in template.read_text(errors="replace").splitlines():
        tag = TAG_RE.match(line)
        if tag:
            level, fields = int(tag[1]), tag[2].split()
            if current is not None and depth > 0:
                add(current, level, fields)
            else:
                pending.append((level, fields))
            continue
        code = strip_comment(line)
        record = RECORD_RE.match(code)
        if record:
            current = record[1] or record[2]
            for level, fields in pending:
                add(current, level, fields)
            pending = []
        depth += code.count("{") - code.count("}")
        if depth <= 0:
            depth = 0
    return result


def record_names(template: Path) -> set[str]:
    names = set()
    for line in template.read_text(errors="replace").splitlines():
        record = RECORD_RE.match(strip_comment(line))
        if record:
            names.add(record[1] or record[2])
    return names


def req_pvs(req: Path) -> set[str]:
    pvs = set()
    for line in req.read_text(errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("file "):
            pvs.add(line.split()[0])
    return pvs


def check_pattern(pattern: Path) -> list[str]:
    files = {
        src.relative_to(pattern).as_posix(): src for src, _ in vendored_files(pattern)
    }
    templates = {
        Path(rel).stem: src
        for rel, src in files.items()
        if rel.endswith(TEMPLATE_SUFFIXES)
    }
    reqs = {Path(rel).name: src for rel, src in files.items() if rel.endswith(".req")}
    problems = []
    expected_reqs = set()
    for stem, template in sorted(templates.items()):
        for kind, pvs in tagged_pvs(template).items():
            if not pvs:
                continue
            name = f"{stem}_{kind}.req"
            expected_reqs.add(name)
            if name not in reqs:
                problems.append(
                    f"{name}: missing; {template.name} tags {len(pvs)} PV(s)"
                )
                continue
            shipped = req_pvs(reqs[name])
            for pv in sorted(pvs - shipped):
                problems.append(f"{name}: missing {pv} (tagged in {template.name})")
            for pv in sorted(shipped - pvs):
                problems.append(f"{name}: {pv} is not tagged in {template.name}")
    for name, req in sorted(reqs.items()):
        if name in expected_reqs:
            continue
        stem, _, kind = Path(name).stem.rpartition("_")
        if stem not in templates or kind not in ("positions", "settings"):
            problems.append(f"{name}: no vendored template {stem}.template/.db")
            continue
        records = record_names(templates[stem])
        for pv in sorted(req_pvs(req)):
            if pv.split(".")[0] not in records:
                problems.append(
                    f"{name}: {pv} is not a record of {templates[stem].name}"
                )
            else:
                problems.append(f"{name}: {pv} is not tagged in {templates[stem].name}")
    return problems


def main() -> int:
    args = pattern_arg_parser(__doc__.splitlines()[0]).parse_args()
    allow = YAML(typ="safe").load(ALLOW_FILE) or {}
    failures = 0
    allowed_seen: set[tuple[str, str]] = set()
    patterns = select_patterns(args.patterns)
    for pattern in patterns:
        allowed = {entry["problem"] for entry in allow.get(pattern.name, [])}
        problems = []
        for problem in check_pattern(pattern):
            if problem in allowed:
                allowed_seen.add((pattern.name, problem))
                print(f"allowed {pattern.name}: {problem}")
            else:
                problems.append(problem)
        for problem in problems:
            print(f"FAIL {pattern.name}: {problem}")
        failures += bool(problems)
    stale = [
        (name, entry["problem"])
        for name, entries in allow.items()
        if not args.patterns or name in args.patterns
        for entry in entries
        if (name, entry["problem"]) not in allowed_seen
    ]
    for name, problem in stale:
        print(f"FAIL stale entry in {ALLOW_FILE.name}: {name}: {problem}")
    print(f"autosave: {len(patterns) - failures} of {len(patterns)} patterns match")
    return 1 if failures or stale else 0


if __name__ == "__main__":
    sys.exit(main())
