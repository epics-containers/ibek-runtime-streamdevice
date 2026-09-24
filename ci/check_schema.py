"""Validate every pattern's ibek.support.yaml and ibek.manifest.yaml.

- each ``*.ibek.support.yaml`` against ``ibek.support.schema.json`` from the
  pinned ibek release, then through ibek's own loader, which builds the entity
  models the schema cannot check (parameter types, defaults, Jinja);
- each ``ibek.manifest.yaml`` through ibek's manifest loader and vendoring plan,
  the same validation `ibek pattern add` runs before it writes a file;
- each ``databases:`` file an entity model names is vendored into ``config/``,
  where ``ibek runtime generate2`` looks for it.

usage: uv run --with-requirements ci/requirements.txt ci/check_schema.py [PATTERN...]
"""

from __future__ import annotations

import json
import sys
import urllib.request
from importlib.metadata import version
from pathlib import Path

import jsonschema
from ibek.entity_factory import EntityFactory
from ibek.pattern_cmds.sources import PatternError
from patterns import SUPPORT_SUFFIX, pattern_arg_parser, select_patterns, vendored_files
from ruamel.yaml import YAML

SCHEMA_URL = (
    "https://github.com/epics-containers/ibek/releases/download/"
    "{tag}/ibek.support.schema.json"
)


def release_tag(pkg_version: str) -> str:
    """The GitHub release tag of an ibek PyPI version (4.8.0b1 -> 4.8.0-beta.1)."""
    for pep440, semver in (("a", "-alpha."), ("b", "-beta."), ("rc", "-rc.")):
        head, sep, tail = pkg_version.partition(pep440)
        if sep and tail.isdigit():
            return f"{head}{semver}{tail}"
    return pkg_version


def load_schema() -> dict:
    url = SCHEMA_URL.format(tag=release_tag(version("ibek")))
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def check_support_yaml(path: Path, validator: jsonschema.Validator) -> list[str]:
    errors = []
    data = YAML(typ="safe").load(path)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.absolute_path) or "<root>"
        errors.append(f"schema: {where}: {error.message}")
    if errors:
        return errors
    try:
        EntityFactory().make_entity_models([path])
    except Exception as exc:  # ibek raises pydantic and Jinja errors alike
        errors.append(f"ibek: {type(exc).__name__}: {exc}")
    return errors


def check_databases(path: Path, vendored: set[str]) -> list[str]:
    errors = []
    data = YAML(typ="safe").load(path)
    for model in data.get("entity_models", []):
        for db in model.get("databases", []) or []:
            if f"config/{db['file']}" not in vendored:
                errors.append(
                    f"entity model {model['name']}: database {db['file']} "
                    "is not vendored into config/"
                )
    return errors


def main() -> int:
    args = pattern_arg_parser(__doc__.splitlines()[0]).parse_args()
    validator = jsonschema.Draft202012Validator(load_schema())
    failures = 0
    patterns = select_patterns(args.patterns)
    for pattern in patterns:
        problems: list[str] = []
        try:
            vendored = {key for _, key in vendored_files(pattern)}
        except PatternError as exc:
            problems.append(f"ibek.manifest.yaml: {exc}")
            vendored = set()
        for support in sorted(pattern.glob(f"*{SUPPORT_SUFFIX}")):
            problems += [
                f"{support.name}: {e}" for e in check_support_yaml(support, validator)
            ]
            if vendored:
                problems += [
                    f"{support.name}: {e}" for e in check_databases(support, vendored)
                ]
        for problem in problems:
            print(f"FAIL {pattern.name}: {problem}")
        failures += bool(problems)
    print(f"schema: {len(patterns) - failures} of {len(patterns)} patterns valid")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
