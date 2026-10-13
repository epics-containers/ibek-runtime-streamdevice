"""Render every pattern's PVI screens with `ibek runtime generate2` and check their PVs.

All patterns' vendored files are flattened into the ``config`` folder of one
scratch IOC (as an instance's ``config/`` holds them), with one entity of every
entity model in its ``ioc.yaml``. ``ibek runtime generate2`` then runs with PVI
enabled, as it does when an IOC starts. This checks that:

- every ``<model>.pvi.device.yaml`` loads in pvi and renders a ``.bob``, and
  generate2 succeeds for the IOC as a whole;
- every entity model with databases has a ``pvi:`` block, and its screen has a
  button on the index (models whose name starts with ``_`` are templates for
  others and have no screen);
- every PV on each screen, subscreens included, resolves, with the macros the
  index button passes, to a record (or a field of one) that the model's own
  templates create. The records are the ones in ``ioc.subst``'s rows for the
  model, with the macros of the row, so the check follows what the IOC loads.

usage: uv run --with-requirements ci/requirements.txt ci/check_pvi.py
           [--keep DIR] [PATTERN...]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from patterns import ROOT, SUPPORT_SUFFIX, select_patterns, vendored_files
from ruamel.yaml import YAML
from template_load import CONFIG_FILE, parse_subst, placeholder

MACRO = re.compile(r"\$[({]([A-Za-z_][A-Za-z0-9_]*)(?:=([^)}]*))?[)}]")
# The parser the PVI generator reads templates with.
GENERATOR = ROOT / "generate-pvi.py"
# Values the screens pass for a PV that carries no record: a command button.
NO_PV = {"SignalX"}


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_pvi", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def expand(text: str, macros: dict[str, str]) -> str:
    """Macro expansion, with ``$(NAME=default)``; unknown macros are left as they are."""

    def sub(m: re.Match) -> str:
        if m[1] in macros:
            return macros[m[1]]
        return m[2] if m[2] is not None else m[0]

    for _ in range(10):
        new = MACRO.sub(sub, text)
        if new == text:
            break
        text = new
    return text


def flatten(patterns: list[Path], config: Path) -> list[tuple[Path, Path]]:
    """Copy every pattern's vendored files into ``config``.

    Returns (pattern, support yaml in config) for each support yaml.
    """
    placed: dict[str, Path] = {}
    supports = []
    for pattern in patterns:
        for src, key in vendored_files(pattern):
            name = Path(key).name
            if name in placed and placed[name].read_bytes() != src.read_bytes():
                sys.exit(f"FAIL {pattern.name}/{name}: differs from {placed[name]}")
            placed[name] = src
            shutil.copy2(src, config / name)
            if name.endswith(SUPPORT_SUFFIX):
                supports.append((pattern, config / name))
    return sorted(supports, key=lambda item: item[1].name)


def entity_for(module: str, model: dict, given: dict) -> dict:
    entity = {"type": f"{module}.{model['name']}"}
    for name, spec in (model.get("parameters") or {}).items():
        if name in given:
            entity[name] = given[name]
        elif "default" not in spec:
            entity[name] = placeholder(name, spec)
        if spec.get("type") == "id":
            entity[name] = f"ci_{model['name']}_{name}"
    return entity


def screen_pvs(opi: Path, bob: str, seen: set[str] | None = None) -> list[str]:
    """Every PV name on a screen and, recursively, on the screens it opens."""
    seen = set() if seen is None else seen
    if bob in seen:
        return []
    seen.add(bob)
    root = ET.parse(opi / bob).getroot()
    pvs = [e.text for e in root.iter("pv_name") if e.text and e.text not in NO_PV]
    for element in root.iter("file"):
        if element.text and element.text.endswith(".bob"):
            pvs += screen_pvs(opi, element.text, seen)
    return pvs


def model_records(generator, patterns: dict[str, Path], subst: str) -> dict[str, set]:
    """{entity type: {record name}} from the rows of ioc.subst."""
    records: dict[str, set[str]] = {}
    for template, columns, row in parse_subst(subst):
        macros = dict(zip(columns, row, strict=False))
        etype = macros.get("type", "")
        folder = patterns.get(template)
        if not etype or folder is None:
            continue
        parser = generator.Parser(folder, {})
        parser.parse(template, macros)
        names = records.setdefault(etype, set())
        names |= {expand(record.name, macros) for record in parser.records}
    return records


def run(work: Path, patterns: list[Path]) -> int:
    yaml = YAML(typ="safe")
    values = (yaml.load(CONFIG_FILE) or {}).get("values") or {}
    generator = load_generator()
    epics = work / "epics"
    config = epics / "ioc" / "config"
    config.mkdir(parents=True)
    supports = flatten(patterns, config)

    folders: dict[str, Path] = {}
    for pattern in patterns:
        for src, key in vendored_files(pattern):
            if key.endswith((".template", ".db")):
                folders[Path(key).name] = pattern

    failures: list[str] = []
    entities = []
    expected: dict[str, str] = {}  # entity type -> screen stem
    for pattern, support in supports:
        data = yaml.load(support)
        for model in data["entity_models"]:
            if not model.get("databases"):
                continue
            etype = f"{data['module']}.{model['name']}"
            if model.get("pvi"):
                expected[etype] = Path(model["pvi"]["yaml_path"]).name.split(".")[0]
            elif not model["name"].startswith("_"):
                failures.append(f"{etype}: has databases but no pvi: block")
            given = values.get(pattern.name, {}).get(model["name"], {})
            entities.append(entity_for(data["module"], model, given))
    (config / "ioc.yaml").write_text(
        json.dumps(
            {"ioc_name": "ci", "description": "pvi screens", "entities": entities}
        )
    )

    env = {**os.environ, "EPICS_ROOT": str(epics)}
    done = subprocess.run(
        [sys.executable, "-m", "ibek", "runtime", "generate2", str(config)],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if done.returncode:
        print(done.stdout + done.stderr)
        print("FAIL ibek runtime generate2 with pvi")
        return 1

    opi = epics / "opi"
    index = ET.parse(opi / "index.bob").getroot()
    buttons = {}
    for action in index.iter("action"):
        macros = action.find("macros")
        buttons[action.findtext("file")] = {
            c.tag: c.text or "" for c in (macros if macros is not None else [])
        }
    subst = (epics / "runtime" / "ioc.subst").read_text()
    records = model_records(generator, folders, subst)

    checked = 0
    for etype, stem in sorted(expected.items()):
        bob = f"{stem}.pvi.bob"
        if not (opi / bob).is_file() or bob not in buttons:
            failures.append(f"{etype}: no {bob} on the screen index")
            continue
        names = records.get(etype, set())
        for pv in sorted(set(screen_pvs(opi, bob))):
            checked += 1
            resolved = expand(pv, buttons[bob])
            base = resolved.rsplit(".", 1)[0] if resolved not in names else resolved
            if "$" in resolved or base not in names:
                failures.append(f"{etype}: PV {pv} -> {resolved} is not a record")

    for failure in failures:
        print(f"FAIL {failure}")
    print(
        f"check_pvi: {len(expected)} screens, {checked} PVs, "
        f"{len(entities)} entities, {len(failures)} failures"
    )
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "patterns", nargs="*", help="pattern folder names (default: every pattern)"
    )
    parser.add_argument("--keep", type=Path, help="generate here and keep the output")
    args = parser.parse_args()
    patterns = select_patterns(args.patterns)
    if args.keep:
        shutil.rmtree(args.keep, ignore_errors=True)
        args.keep.mkdir(parents=True)
        return run(args.keep.resolve(), patterns)
    with tempfile.TemporaryDirectory() as tmp:
        return run(Path(tmp), patterns)


if __name__ == "__main__":
    sys.exit(main())
