"""Flag hostnames, IP addresses, internal URLs and credentials in library files.

Scans every text file git tracks or would track (untracked files that are not
ignored are included, so a pattern can be checked before it is committed).
Accepted findings are listed, with the reason, in ci/content-allow.yaml as a
file path plus the exact matched text; an entry that no longer matches anything
fails the check.

usage: uv run --with-requirements ci/requirements.txt ci/check_content.py [PATH...]
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import subprocess
import sys
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent
ALLOW_FILE = Path(__file__).with_name("content-allow.yaml")

# Domains whose hosts are internal to a facility; their public web sites are
# listed in PUBLIC_HOSTS.
INTERNAL_DOMAINS = r"(?:diamond\.ac\.uk|dls\.ac\.uk|rl\.ac\.uk|stfc\.ac\.uk)"
PUBLIC_HOSTS = {"www.diamond.ac.uk", "diamond.ac.uk", "www.stfc.ac.uk", "stfc.ac.uk"}
# DLS network host names: terminal servers, industrial PCs and workstations
# (bl04i-ea-serv-01, i15-ts-01). IOC names (BL04I-MO-IOC-01) are PV
# prefixes and instance names, not hosts, and are not flagged.
DLS_HOST = (
    r"(?:(?:bl\d\d[a-z]|sr\d\d[a-z]|fe\d\d[a-z])-[a-z]{2}-(?:serv|ts|ipc|pc|ws)-\d\d"
    r"|[a-z]\d\d-(?:serv|ts|ipc)-\d\d)"
)

CHECKS: list[tuple[str, re.Pattern]] = [
    ("internal hostname", re.compile(rf"\b(?:[\w-]+\.)*{INTERNAL_DOMAINS}\b", re.I)),
    ("internal hostname", re.compile(rf"\b{DLS_HOST}\b", re.I)),
    ("credential", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("credential", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    (
        "credential",
        re.compile(r"\b(?:ghp|gho|ghs|ghu|github_pat|glpat)[-_][A-Za-z0-9_]{16,}"),
    ),
    ("credential", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    (
        "credential",
        re.compile(
            r"""(?i)\b(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token"""
            r"""|auth[_-]?token)\b\s*[:=]\s*["']?[^\s"'$(){}]{4,}"""
        ),
    ),
    ("credential", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@")),
]
URL_RE = re.compile(r"\b(?:https?|ftp)://([^/\s\"'<>)\]]+)", re.I)
IPV4_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d{1,3}){3})(?::\d+)?(?![\w.])")


def ip_finding(text: str) -> bool:
    """True for an IPv4 address that could name a real host."""
    try:
        address = ipaddress.IPv4Address(text)
    except ValueError:
        return False
    return not (
        address.is_loopback
        or address.is_unspecified
        or text.startswith("255.")  # netmasks
        or address in ipaddress.IPv4Network("192.0.2.0/24")  # TEST-NET-1
        or address in ipaddress.IPv4Network("198.51.100.0/24")  # TEST-NET-2
        or address in ipaddress.IPv4Network("203.0.113.0/24")  # TEST-NET-3
    )


def url_finding(host: str) -> bool:
    """True for a URL host on a private network: a bare intranet name or an IP.

    Hosts in the internal domains are caught by the hostname check.
    """
    host = host.rsplit("@", 1)[-1].split(":")[0].lower().rstrip(".")
    if host == "localhost" or "$" in host or "{" in host:  # macros, placeholders
        return False
    if IPV4_RE.fullmatch(host):
        return ip_finding(host)
    return "." not in host


def scan(path: Path, rel: str) -> list[tuple[int, str, str]]:
    try:
        text = path.read_text()
    except (UnicodeDecodeError, OSError):
        return []
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        for kind, regex in CHECKS:
            findings += [
                (number, kind, m.group(0))
                for m in regex.finditer(line)
                if m.group(0).lower() not in PUBLIC_HOSTS
            ]
        findings += [
            (number, "IP address", m.group(0))
            for m in IPV4_RE.finditer(line)
            if ip_finding(m.group(1))
        ]
        findings += [
            (number, "internal URL", m.group(0))
            for m in URL_RE.finditer(line)
            if url_finding(m.group(1))
        ]
    return sorted(set(findings))


def tracked_files(paths: list[str]) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            *paths,
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [f for f in result.stdout.split("\0") if f]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="paths to scan (default: every file)")
    args = parser.parse_args()
    allow = YAML(typ="safe").load(ALLOW_FILE) or []
    allowed = {(entry["file"], entry["match"]) for entry in allow}
    seen: set[tuple[str, str]] = set()
    failures = 0
    files = tracked_files(args.paths)
    for rel in files:
        if rel.startswith("ci/"):
            continue  # the checks themselves hold the patterns they look for
        for number, kind, match in scan(ROOT / rel, rel):
            if (rel, match) in allowed:
                seen.add((rel, match))
                continue
            print(f"FAIL {rel}:{number}: {kind}: {match}")
            failures += 1
    stale = [
        key
        for key in sorted(allowed - seen)
        if not args.paths or any(key[0].startswith(p.rstrip("/")) for p in args.paths)
    ]
    for rel, match in stale:
        print(f"FAIL stale entry in {ALLOW_FILE.name}: {rel}: {match}")
    print(f"content: {len(files)} files scanned, {failures} finding(s)")
    return 1 if failures or stale else 0


if __name__ == "__main__":
    sys.exit(main())
