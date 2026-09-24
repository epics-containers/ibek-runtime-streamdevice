"""Shared helpers for the CI checks: find patterns and their vendored files."""

from __future__ import annotations

import argparse
from pathlib import Path

from ibek.pattern_cmds.manifest import plan_vendor

ROOT = Path(__file__).resolve().parent.parent
SUPPORT_SUFFIX = ".ibek.support.yaml"
MANIFEST_NAME = "ibek.manifest.yaml"


def all_patterns(root: Path = ROOT) -> list[Path]:
    """Every top-level folder holding a *.ibek.support.yaml, sorted by name."""
    return sorted(
        d
        for d in root.iterdir()
        if d.is_dir()
        and not d.name.startswith(".")
        and any(d.glob(f"*{SUPPORT_SUFFIX}"))
    )


def select_patterns(names: list[str], root: Path = ROOT) -> list[Path]:
    """The named patterns, or all of them when no name is given."""
    if not names:
        return all_patterns(root)
    return [root / name for name in names]


def vendored_files(pattern: Path) -> list[tuple[Path, str]]:
    """(source path, destination key) for each file `ibek pattern add` vendors."""
    return plan_vendor(pattern)


def pattern_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "patterns", nargs="*", help="pattern folder names (default: every pattern)"
    )
    return parser
