"""Load every vendored template into the generic ioc-streamdevice IOC.

Two steps, so that only the second needs the IOC image:

``prepare OUT [PATTERN...]`` (pinned ibek, outside the image)
    For each entity model of each pattern, write an ``ioc.yaml`` holding one
    entity of that model and run ``ibek runtime generate2`` on it, as an IOC
    instance does at start-up. Required parameters get a placeholder by type,
    or the value given in ci/template-load.yaml. Each row of the generated
    ``ioc.subst`` is one test case: one template, with the macros its entity
    model passes. One ``ioc.yaml`` holding an entity of every model of the
    pattern must generate too.

``run OUT`` (inside the image; standard library only)
    Expand each case with ``msi -V`` (an undefined macro is an error). Then
    start the image's IOC binary with its own ``ioc.dbd``, an asyn IP port
    (never connected) for each port the records name, ``STREAM_PROTOCOL_PATH``
    at the pattern, and a field-less stub of each record the pattern's other
    cases create, which protocols may redirect to. Load the database, run
    ``iocInit``, and ``dbgf`` each PV of the template's autosave ``.req``
    files. Any load, record-initialisation, protocol or missing-PV error fails
    the case.

ci/template-load.yaml lists the templates that need more than the generic
image, which must fail, and the known error lines of templates that load.
An entry that no longer applies fails the check, so the lists stay accurate.

usage (with the image pulled):
    uv run --with-requirements ci/requirements.txt \\
        ci/template_load.py prepare build/load
    docker run --rm -v "$PWD:$PWD" -w "$PWD" IMAGE \\
        python ci/template_load.py run build/load
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = Path(__file__).with_name("template-load.yaml")

# ---------------------------------------------------------------------------
# prepare
# ---------------------------------------------------------------------------

PLACEHOLDER = {"int": 1, "float": 1.0, "bool": False}


def placeholder(name: str, spec: dict) -> object:
    kind = spec.get("type")
    if kind == "enum":
        return next(iter(spec["values"]))
    if kind in PLACEHOLDER:
        return PLACEHOLDER[kind]
    # str parameters are as often numbers (addresses, limits, delays) as names,
    # and "1" is valid as both
    return "1"


def parse_subst(text: str) -> list[tuple[str, list[str], list[str]]]:
    """(file, column names, row) for each row of each ``file "x" {...}`` block."""
    blocks = []
    for match in re.finditer(r'file\s+"([^"]+)"\s*\{(.*?)\n\}', text, re.S):
        rows = [
            re.findall(r'"((?:[^"\\]|\\.)*)"', row)
            for row in re.findall(r"\{([^{}]*)\}", match.group(2))
        ]
        blocks += [(match.group(1), rows[0], row) for row in rows[1:]]
    return blocks


def generate(
    cfg: Path, runtime: Path, supports: list[Path], entities: list[dict]
) -> None:
    """``ibek runtime generate2`` of an ioc.yaml holding ``entities``."""
    from ibek.runtime_cmds.commands import do_generate

    ioc_yaml = cfg / "ioc.yaml"
    ioc_yaml.write_text(
        json.dumps(
            {"ioc_name": "ci", "description": "template load", "entities": entities}
        )
    )
    runtime.mkdir(parents=True, exist_ok=True)
    do_generate([ioc_yaml], supports, runtime, False)


def expand(text: str, macros: dict[str, str]) -> str:
    """msi-style macro expansion, enough for .req lines."""

    def sub(m: re.Match) -> str:
        name, _, default = (m.group(1) or m.group(2)).partition("=")
        return macros.get(
            name, default if "=" in (m.group(1) or m.group(2)) else m.group(0)
        )

    for _ in range(5):
        text = re.sub(r"\$\(([^()]*)\)|\$\{([^{}]*)\}", sub, text)
    return text


def write_case(
    case: Path,
    pattern: Path,
    entity: str,
    template: str,
    block: str,
    pvs: list[str],
    xfail: str | None,
    known_errors: list[str],
) -> None:
    case.mkdir()
    (case / "ioc.subst").write_text(block)
    (case / "case.json").write_text(
        json.dumps(
            {
                "pattern": pattern.name,
                "pattern_dir": str(pattern),
                "entity": entity,
                "template": template,
                "req_pvs": sorted(set(pvs)),
                "xfail": xfail,
                "known_errors": known_errors,
            },
            indent=2,
        )
    )


def prepare(out: Path, names: list[str]) -> int:
    from patterns import select_patterns, vendored_files
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    config = yaml.load(CONFIG_FILE) or {}
    values = config.get("values") or {}
    xfail = {
        f"{entry['pattern']}/{entry['template']}": entry["reason"]
        for entry in config.get("xfail") or []
    }
    known: dict[str, list[str]] = {}
    for entry in config.get("known_errors") or []:
        known.setdefault(f"{entry['pattern']}/{entry['template']}", []).append(
            entry["error"]
        )
    together_xfail = {
        entry["pattern"]: entry["reason"]
        for entry in config.get("generate_together_xfail") or []
    }
    if out.exists():
        shutil.rmtree(out)
    cases_dir = out / "cases"
    cases_dir.mkdir(parents=True)
    failures = 0
    reached: set[str] = set()
    all_templates: set[str] = set()

    for pattern in select_patterns(names):
        work = out / "generate" / pattern.name
        cfg = work / "config"
        cfg.mkdir(parents=True)
        files = {Path(key).name: src for src, key in vendored_files(pattern)}
        all_templates |= {
            f"{pattern.name}/{n}" for n in files if n.endswith((".template", ".db"))
        }
        supports = sorted(
            src for n, src in files.items() if n.endswith(".ibek.support.yaml")
        )
        entities = []
        for support in supports:
            data = yaml.load(support)
            for model in data["entity_models"]:
                if not model.get("databases"):
                    continue
                given = values.get(pattern.name, {}).get(model["name"], {})
                entity = {"type": f"{data['module']}.{model['name']}"}
                for pname, spec in (model.get("parameters") or {}).items():
                    if pname in given:
                        entity[pname] = given[pname]
                    elif "default" not in spec:
                        entity[pname] = placeholder(pname, spec)
                    if spec.get("type") == "id":
                        entity[pname] = f"ci_{model['name']}_{pname}"
                entities.append(entity)
        for number, entity in enumerate(entities):
            runtime = work / f"runtime-{number:02d}"
            try:
                generate(cfg, runtime, supports, [entity])
            except Exception as exc:  # ibek raises pydantic and Jinja errors alike
                print(
                    f"FAIL {pattern.name}: {entity['type']}: ibek runtime generate2: "
                    f"{type(exc).__name__}: {exc}"
                )
                failures += 1
                continue
            subst = (runtime / "ioc.subst").read_text()
            for index, (template, columns, row) in enumerate(parse_subst(subst)):
                macros = dict(zip(columns, row, strict=False))
                key = f"{pattern.name}/{template}"
                reached.add(key)
                header = "{ " + ", ".join(f'"{c}"' for c in columns) + " }"
                values_row = "{ " + ", ".join(json.dumps(v) for v in row) + " }"
                block = f'file "{template}" {{\npattern\n{header}\n{values_row}\n}}\n'
                pvs = []
                for kind in ("positions", "settings"):
                    req = files.get(f"{Path(template).stem}_{kind}.req")
                    if req:
                        pvs += [
                            expand(line.split()[0], macros)
                            for line in req.read_text().splitlines()
                            if line.strip() and not line.lstrip().startswith("#")
                        ]
                write_case(
                    cases_dir / f"{pattern.name}--{number:02d}{index:02d}",
                    pattern,
                    entity["type"],
                    template,
                    block,
                    pvs,
                    xfail.get(key),
                    known.get(key, []),
                )
        # An IOC instance may use every entity model of a pattern at once.
        try:
            generate(cfg, work / "runtime-all", supports, entities)
            if pattern.name in together_xfail:
                print(
                    f"FAIL {pattern.name}: listed under generate_together_xfail in "
                    f"{CONFIG_FILE.name}, but generates"
                )
                failures += 1
        except Exception as exc:
            if pattern.name in together_xfail:
                print(
                    f"xfail {pattern.name}: generate2 with one entity of each model: "
                    f"{together_xfail[pattern.name]}"
                )
            else:
                print(
                    f"FAIL {pattern.name}: ibek runtime generate2 with one entity of "
                    f"each model: {type(exc).__name__}: {exc}"
                )
                failures += 1

    # templates no entity model loads directly are msi include/substitute targets
    included = set()
    for key in all_templates:
        text = (ROOT / key).read_text(errors="replace")
        pattern_name = key.split("/")[0]
        for target in re.findall(
            r'^\s*(?:include|substitute\s+"[^"]*"\s*;?\s*include)\s+"([^"]+)"',
            text,
            re.M,
        ):
            included.add(f"{pattern_name}/{target}")
    for key in sorted(all_templates - reached - included):
        print(
            f"FAIL {key}: vendored, but no entity model loads it "
            "and no template includes it"
        )
        failures += 1
    selected = {p.name for p in select_patterns(names)}
    stale = {key for key in xfail if key.split("/")[0] in selected} - reached
    for key in sorted(stale):
        print(
            f"FAIL stale xfail entry in {CONFIG_FILE.name}: "
            f"{key} is not loaded by any case"
        )
    cases = len(list(cases_dir.iterdir()))
    print(
        f"prepare: {cases} cases from {len(reached)} templates "
        f"({len(included & all_templates - reached)} more reached through msi include)"
    )
    return 1 if failures or stale else 0


# ---------------------------------------------------------------------------
# run (inside the IOC image: standard library only)
# ---------------------------------------------------------------------------

# Output lines that mean the database did not load or a record did not initialise.
ERROR_RE = re.compile(
    r"(?i)(error|illegal|not found|can't|cannot|unknown|undefined|invalid|bad |"
    r"no such|failed|does not exist|syntax|abort|findInterface)"
)
# Messages caused by the asyn ports being deliberately unconnected. A StreamDevice
# record whose @init handler cannot run reports "Can't start @init handler" and
# "Record initialization failed"; its protocol was parsed by then, so protocol
# errors are still reported. Records processed at iocInit (PINI, CA links) then
# report the port as not connected.
BENIGN_RE = re.compile(
    r"(Can't start @init handler|Record initialization failed|queueRequest failed"
    r"|@init handler failed|init_record Error \(514,11\)"
    r"|lockRequest: port \S+ not connected"
    r"|connectToAsynPort: Can't connect to 127\.0\.0\.1:9"
    r"|: Connect failed|: Protocol aborted"
    r"|ca_array_put Channel write request failed)"
)
# dbgf prints a field's type and value; the value may be any string.
DBGF_VALUE_RE = re.compile(r"^DBF_[A-Z0-9_]+:\s")
RECORD_RE = re.compile(r'^\s*g?record\s*\(\s*([^,\s]+)\s*,\s*"([^"]*)"', re.M)
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
COMMAND_ECHO_RE = re.compile(r"^\x1b\[1m.*\x1b\[0m$")
LINK_RE = re.compile(r'field\s*\(\s*(?:INP|OUT)\s*,\s*"@([^"]*)"\s*\)')
DTYP_STREAM_RE = re.compile(r'field\s*\(\s*DTYP\s*,\s*"stream"\s*\)', re.I)
ASYN_PORT_RE = re.compile(
    r'field\s*\(\s*(?:PORT\s*,\s*"([^"]+)"|(?:INP|OUT)\s*,\s*"@asyn(?:Mask)?\(\s*([^,)\s]+))'
)


def asyn_ports(db: str) -> set[str]:
    """The asyn port names the records in ``db`` use."""
    buses = {a or b for a, b in ASYN_PORT_RE.findall(db)}
    for record in re.split(r"\n\s*(?=g?record\s*\()", db):
        if not DTYP_STREAM_RE.search(record):
            continue
        for link in LINK_RE.findall(record):
            tokens = link.split()
            if len(tokens) < 3:
                continue
            # "@file protocol(arg, arg) bus [addr]": skip past the protocol call
            rest = link.split(None, 1)[1]
            depth, i = 0, 0
            while i < len(rest):
                if rest[i] == "(":
                    depth += 1
                elif rest[i] == ")":
                    depth -= 1
                elif rest[i].isspace() and depth == 0:
                    break
                i += 1
            bus = rest[i:].split()
            if bus:
                buses.add(bus[0])
    return buses


def expand_case(case: Path, args: argparse.Namespace) -> list[str]:
    """msi-expand a case's substitution into ioc.db; return any msi errors."""
    meta = json.loads((case / "case.json").read_text())
    msi = subprocess.run(
        [*args.msi, "-V", f"-I{meta['pattern_dir']}", "-S", str(case / "ioc.subst")],
        capture_output=True,
        text=True,
    )
    (case / "msi.log").write_text(msi.stderr)
    if msi.returncode != 0 or msi.stderr.strip():
        return [f"msi: {line}" for line in msi.stderr.strip().splitlines()]
    (case / "ioc.db").write_text(msi.stdout)
    return []


def records(db: str) -> dict[str, str]:
    """{record name: record type} of an expanded database."""
    return {m[2]: m[1] for m in RECORD_RE.finditer(db)}


def load_case(
    case: Path, args: argparse.Namespace, slot: int, context: dict[str, str]
) -> tuple[str, list[str]]:
    """Load a case's ioc.db, plus a stub of each record in ``context`` it lacks.

    A protocol may redirect to a record another entity model of the pattern
    creates (``%($1:ERR)``); StreamDevice checks at init that it exists. The
    stubs, of the right type and with no fields, stand in for those records.
    """
    meta = json.loads((case / "case.json").read_text())
    db = (case / "ioc.db").read_text()
    own = records(db)
    stubs = "".join(
        f'record({rtype}, "{name}") {{}}\n'
        for name, rtype in sorted(context.items())
        if name not in own
    )
    (case / "context.db").write_text(stubs)
    lines = [
        f'epicsEnvSet("STREAM_PROTOCOL_PATH", "{meta["pattern_dir"]}")',
        f'dbLoadDatabase("{args.dbd}")',
        "ioc_registerRecordDeviceDriver(pdbbase)",
    ]
    lines += [
        f'drvAsynIPPortConfigure("{bus}", "127.0.0.1:9", 0, 1, 0)'
        for bus in sorted(asyn_ports(db))
    ]
    lines += [
        f'dbLoadRecords("{case / "ioc.db"}")',
        f'dbLoadRecords("{case / "context.db"}")',
        "iocInit",
        'echo "CI: iocInit done"',
    ]
    lines += [f'dbgf "{pv}"' for pv in meta["req_pvs"]]
    lines += ['echo "CI: done"', "exit"]
    (case / "st.cmd").write_text("\n".join(lines) + "\n")
    env = dict(os.environ)
    env.update(
        {
            "EPICS_CAS_INTF_ADDR_LIST": "127.0.0.1",
            "EPICS_CAS_BEACON_ADDR_LIST": "127.0.0.1",
            "EPICS_CAS_AUTO_BEACON_ADDR_LIST": "NO",
            "EPICS_CAS_SERVER_PORT": str(20000 + 2 * slot),
            "EPICS_PVAS_INTF_ADDR_LIST": "127.0.0.1",
            "EPICS_PVAS_BROADCAST_PORT": str(40000 + 2 * slot),
            "EPICS_PVAS_SERVER_PORT": str(40001 + 2 * slot),
            "EPICS_PVA_AUTO_ADDR_LIST": "NO",
        }
    )
    try:
        ioc = subprocess.run(
            [*args.ioc, str(case / "st.cmd")],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            env=env,
            timeout=args.timeout,
            cwd=case,
        )
        output = ioc.stdout + ioc.stderr
    except subprocess.TimeoutExpired as exc:
        output = (
            (exc.stdout or b"").decode(errors="replace")
            if isinstance(exc.stdout, bytes)
            else (exc.stdout or "")
        )
        output += "\nCI: IOC timed out"
    (case / "ioc.log").write_text(output)
    problems = []
    matched: set[str] = set()
    if "CI: iocInit done" not in output:
        problems.append("the IOC did not reach the end of iocInit")
    if "CI: done" not in output:
        problems.append("the IOC did not finish the startup script")
    for line in output.splitlines():
        if COMMAND_ECHO_RE.match(line):
            continue  # iocsh echoes each startup-script command in bold
        line = ANSI_RE.sub("", line).strip()
        if line.startswith(("CI:", "epics>", "#")) or DBGF_VALUE_RE.match(line):
            continue
        known = [k for k in meta["known_errors"] if k in line]
        if known:
            matched.update(known)
            continue
        if ERROR_RE.search(line) and not BENIGN_RE.search(line):
            problems.append(line)
    if not meta["xfail"]:
        problems += [
            f"known error listed in {CONFIG_FILE.name} did not occur: {k}"
            for k in meta["known_errors"]
            if k not in matched
        ]
    return ("fail" if problems else "pass"), problems


def run(out: Path, args: argparse.Namespace) -> int:
    cases = sorted(p for p in (out / "cases").iterdir() if (p / "case.json").is_file())
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        msi_errors = list(pool.map(lambda case: expand_case(case, args), cases))
    # every record each pattern's loadable cases create, for load_case's stubs
    context: dict[str, dict[str, str]] = {}
    for case, errors in zip(cases, msi_errors, strict=True):
        meta = json.loads((case / "case.json").read_text())
        if not errors and not meta["xfail"]:
            pattern_records = context.setdefault(meta["pattern"], {})
            for name, rtype in records((case / "ioc.db").read_text()).items():
                pattern_records.setdefault(name, rtype)

    def load(item: tuple[int, tuple[Path, list[str]]]) -> tuple[str, list[str]]:
        slot, (case, errors) = item
        if errors:
            return "fail", errors
        meta = json.loads((case / "case.json").read_text())
        return load_case(case, args, slot % args.jobs, context.get(meta["pattern"], {}))

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(load, enumerate(zip(cases, msi_errors, strict=True))))
    failures = 0
    passed = 0
    xfailed = 0
    for case, (status, problems) in zip(cases, results, strict=True):
        meta = json.loads((case / "case.json").read_text())
        label = f"{meta['pattern']}/{meta['template']} ({meta['entity']})"
        if meta["xfail"]:
            if status == "pass":
                print(
                    f"FAIL {label}: listed in {CONFIG_FILE.name} as needing "
                    f"{meta['xfail']}, but it loads"
                )
                failures += 1
            else:
                print(f"xfail {label}: needs {meta['xfail']}")
                xfailed += 1
            continue
        if status == "pass":
            passed += 1
            continue
        failures += 1
        print(f"FAIL {label}   [{case}]")
        for problem in problems[: args.max_lines]:
            print(f"    {problem}")
        if len(problems) > args.max_lines:
            print(
                f"    ... {len(problems) - args.max_lines} more lines "
                f"in {case / 'ioc.log'}"
            )
    print(
        f"template load: {passed} passed, {xfailed} expected failures, "
        f"{failures} failed, of {len(cases)} cases"
    )
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="step", required=True)
    p = sub.add_parser("prepare", help="generate the test cases (needs pinned ibek)")
    p.add_argument("out", type=Path)
    p.add_argument(
        "patterns", nargs="*", help="pattern folder names (default: every pattern)"
    )
    r = sub.add_parser("run", help="load the test cases (inside the IOC image)")
    r.add_argument("out", type=Path)
    r.add_argument(
        "--ioc",
        default="/epics/ioc/bin/linux-x86_64/ioc",
        help="command that runs the IOC binary (split on spaces)",
    )
    r.add_argument("--dbd", default="/epics/ioc/dbd/ioc.dbd")
    r.add_argument(
        "--msi", default="msi", help="command that runs msi (split on spaces)"
    )
    r.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    r.add_argument("--timeout", type=float, default=30)
    r.add_argument("--max-lines", type=int, default=10)
    args = parser.parse_args()
    if args.step == "prepare":
        sys.path.insert(0, str(Path(__file__).parent))
        return prepare(args.out.resolve(), args.patterns)
    args.ioc = args.ioc.split()
    args.msi = args.msi.split()
    return run(args.out.resolve(), args)


if __name__ == "__main__":
    sys.exit(main())
