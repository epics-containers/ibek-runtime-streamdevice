#!/usr/bin/env python3
"""Strip DLS EDM/GDA annotation comments from the pattern databases.

DLS support modules annotate their databases with comment lines read by DLS
screen and GDA tooling:

    # % gui, $(name=), edm, device.edl, P=$(P)
    #% gdatag,pv,ro,$(gda_name=),RANGE,Range Selection
    # %gda,subsystem,ODCurrAmp,monitor,channel1,Channel 1 value

epics-containers has no consumer for them: screens come from PVI. Their macro
references are still expanded line by line by msi and by dbLoadRecords, so any
macro they name must be defined or the IOC logs `macro ... is undefined`.

This script, run over every pattern folder:

1. deletes every `gui`, `gdatag` and `gda` annotation line from the
   `.template` / `.db` files (any `#`/`%` spacing variant);
2. deletes the `# % macro, X, ...` documentation line (and its indented
   continuation lines) of each macro that step 1 leaves unreferenced in the
   folder, and of every unreferenced `gda_*` macro;
3. deletes each `X: ""` databases arg in `*.ibek.support.yaml` whose macro
   step 1 leaves unreferenced by that database and the files it includes.

`# % autosave`, `# % archiver`, `# % alh`, `# % controldesk` and all other
`# % macro` lines are kept. Record content is never touched.

Run it after importing templates from a DLS release. Idempotent.

    python3 strip-dls-annotations.py           # apply
    python3 strip-dls-annotations.py --check   # exit 1 if anything would change
"""

import argparse
import re
import sys
from pathlib import Path

ANNOTATION = re.compile(r"^\s*#[\s#%]*(gui|gdatag|gda)\s*,")
MACRO_DOC = re.compile(r"^\s*#\s*%\s*macro\s*,\s*([A-Za-z_]\w*)")
GDA_PROSE_DOC = re.compile(r"^\s*#\s+(gda_\w*)\s+-\s")
CONTINUATION = re.compile(r"^#\s{3,}\S")
MACRO_REF = re.compile(r"\$[({]([A-Za-z_]\w*)")
INCLUDE = re.compile(r'^\s*include\s+"([^"]+)"')
DB_FILE = re.compile(r"^\s*-\s*file:\s*(\S+)")
ARGS = re.compile(r"^(\s*)args:\s*$")
EMPTY_ARG = re.compile(r'^(\s*)([A-Za-z_]\w*):\s*""\s*$')


def read(path: Path) -> list[str]:
    with path.open(newline="") as f:
        return f.read().splitlines(keepends=True)


def refs(lines) -> set[str]:
    return {m.group(1) for line in lines for m in MACRO_REF.finditer(line)}


def live_refs(files: dict[Path, list[str]]) -> set[str]:
    """Macros referenced anywhere except `# % macro` documentation lines."""
    return refs(
        line for lines in files.values() for line in lines if not MACRO_DOC.match(line)
    )


def closure(name: str, files: dict[Path, list[str]]) -> list[str]:
    """Lines of a database file plus everything it msi-includes."""
    by_name = {f.name: lines for f, lines in files.items()}
    seen: set[str] = set()
    todo, out = [name], []
    while todo:
        n = todo.pop()
        if n in seen or n not in by_name:
            continue
        seen.add(n)
        out += by_name[n]
        todo += [m.group(1) for line in by_name[n] if (m := INCLUDE.match(line))]
    return out


def strip_databases(before: dict[Path, list[str]]) -> dict[Path, list[str]]:
    mid = {
        f: [ln for ln in lines if not ANNOTATION.match(ln)]
        for f, lines in before.items()
    }
    still_live = live_refs(mid)
    orphaned = live_refs(before) - still_live
    for lines in before.values():
        for line in lines:
            m = MACRO_DOC.match(line) or GDA_PROSE_DOC.match(line)
            if m and m.group(1).startswith("gda_") and m.group(1) not in still_live:
                orphaned.add(m.group(1))

    after = {}
    for f, lines in mid.items():
        out, dropping = [], False
        for line in lines:
            m = MACRO_DOC.match(line) or GDA_PROSE_DOC.match(line)
            if m:
                dropping = m.group(1) in orphaned
            elif not (dropping and CONTINUATION.match(line)):
                dropping = False
            if not dropping:
                out.append(line)
        after[f] = out
    return after


def strip_args(
    text: list[str], before: dict[Path, list[str]], after: dict[Path, list[str]]
) -> list[str]:
    out, db_file, args_indent = [], None, None
    for line in text:
        if m := DB_FILE.match(line):
            db_file, args_indent = m.group(1), None
        elif m := ARGS.match(line):
            args_indent = len(m.group(1))
        elif line.strip() and args_indent is not None:
            indent = len(line) - len(line.lstrip())
            if indent <= args_indent:
                args_indent = None
            elif (m := EMPTY_ARG.match(line)) and db_file:
                macro = m.group(2)
                if macro in refs(closure(db_file, before)) and macro not in refs(
                    closure(db_file, after)
                ):
                    continue
        out.append(line)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).parent)
    parser.add_argument("--check", action="store_true", help="report only")
    args = parser.parse_args()

    changed: dict[Path, list[str]] = {}
    for pattern in sorted(p for p in args.root.iterdir() if p.is_dir()):
        if pattern.name.startswith("."):
            continue
        dbs = sorted(
            f
            for f in pattern.rglob("*")
            if f.is_file() and f.suffix in (".template", ".db")
        )
        before = {f: read(f) for f in dbs}
        after = strip_databases(before)
        changed |= {f: after[f] for f in dbs if after[f] != before[f]}
        for support in pattern.glob("*.ibek.support.yaml"):
            text = read(support)
            new = strip_args(text, before, after)
            if new != text:
                changed[support] = new

    for f in sorted(changed):
        print(f.relative_to(args.root))
    if args.check:
        return 1 if changed else 0
    for f, lines in changed.items():
        with f.open("w", newline="") as out:
            out.write("".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
