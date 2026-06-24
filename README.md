# ibek-runtime-streamdevice

A central **library of runtime StreamDevice support patterns**. Each pattern is a
self-contained set of StreamDevice files (protocol, EPICS DB/template and the `ibek`
support definition that wires them up) that an IOC instance can **vendor at a pinned
version** using `ibek pattern`.

Vendoring copies a pattern's files into an IOC instance's `config/` directory and
records exactly which version was taken, with per-file integrity hashes. The IOC then
loads that device support **at runtime**, with no image rebuild — the generic
`ioc-streamdevice` image already ships StreamDevice; this repo only supplies the
per-device protocol/DB/support files.

This repo is consumed by the `ibek pattern` subsystem in
[epics-containers/ibek](https://github.com/epics-containers/ibek). It is one of two
central pattern libraries; its sibling
[`ibek-runtime-support`](https://github.com/epics-containers/ibek-runtime-support)
holds non-StreamDevice runtime patterns (extra entities/DB for otherwise-generic IOCs).

## What a "pattern" is — the file-set contract

A pattern is **a top-level folder named after the pattern**. The folder name is the
pattern name used on the command line.

A pattern holds an **arbitrary file-set**, not a fixed triplet. The only required
member is the `ibek` support definition; everything else is whatever that definition
references:

| File | Role | Required |
|---|---|---|
| `*.ibek.support.yaml` | `ibek` support module: declares the `entity_models`, their parameters, and which DB/template files to instantiate | **yes** |
| `*.proto` | StreamDevice protocol file(s) | typical |
| `*.template` / `*.db` | EPICS database/template instantiated by the entity | typical |
| `*.req` | autosave request file(s) | optional |
| `*.pvi.device.yaml` | PVI device descriptor (UI/PV generation) | optional |
| anything else the support yaml references | … | optional |

There is **no hard-coded proto/template/support shape**. The vendoring lock simply
hashes a **file list**, so it already generalises to any combination of the above (or
files not yet invented). Add the files your support yaml needs and they are vendored
together as a unit.

This repo currently provides one pattern:

```
lakeshore340/
  lakeshore340.ibek.support.yaml   # entity_model "lakeshore340", parameters, databases:
  lakeshore340.proto               # StreamDevice protocol
  lakeshore340.template            # EPICS records
```

## Pristine storage and the vendored header

**Files in this repo are stored PRISTINE.** They contain exactly the StreamDevice /
EPICS / ibek content, with **no provenance header**.

When `ibek pattern` vendors a file into an IOC instance, it injects a deterministic
provenance header as the first line **before hashing**:

```
# Vendored from github.com/epics-containers/ibek-runtime-streamdevice@v0.1.0 — DO NOT EDIT
```

(note: em dash `—`). Because the header is added at vendor time and is part of the
content that is hashed into the instance's lock file, integrity checking on the
consumer side is a trivial `sha256(file_as_written) == lock`. The header is
deterministic (no timestamps or absolute paths) so it is reproducible.

**Do not commit this header here.** It is a consumer-side artifact. Patterns in this
repo must stay header-free and pristine; the header you see in a vendored copy belongs
to the IOC instance, not to this library.

## Versioning

Releases are cut as **repo-wide semantic-version git tags** (`v0.1.0`, `v0.2.0`, …). A
tag is an **immutable point** covering every pattern in the repo at that revision, so
`name@<tag>` always resolves to the same bytes.

There is intentionally **no per-pattern version**: a single tag versions the whole
library. Bump the tag when any pattern changes; consumers opt in to the new content by
moving their pin.

On the consumer side, [Renovate](https://docs.renovatebot.com/) tracks the pin using
the **`github-releases`** datasource and raises a PR to bump the pinned version when a
new tag is published, keeping IOC instances current without manual edits.

## Consumer pin / update workflow

All consumer commands run against an **IOC instance directory** (`services/<instance>/`
in a services repo). `ibek pattern` writes the vendored files into the instance's
`config/`, and writes `runtime-lock.yaml` + `ioc.schema.json` at the **instance root**
(not in `config/`, which is the ≤ 1 MiB K8s ConfigMap and holds runtime inputs only).

### Add a pattern (pin a version)

Qualified name `<library>:<pattern>@<tag>` selects the library, pattern and version:

```bash
ibek pattern add ibek-runtime-streamdevice:lakeshore340@v0.1.0 services/bl01t-ea-lake-01
```

This:

1. fetches the pattern's file-set at tag `v0.1.0`,
2. writes each file into `services/bl01t-ea-lake-01/config/` with the vendored header,
3. records `version`, `source` and a per-file `sha256` in
   `services/bl01t-ea-lake-01/runtime-lock.yaml`,
4. merges the pattern's entity models into the instance's
   `services/bl01t-ea-lake-01/ioc.schema.json` and points
   `config/ioc.yaml`'s first line at it
   (`# yaml-language-server: $schema=../ioc.schema.json`).

You then reference the entity in `config/ioc.yaml` (the entity type is
`<module>.<entity_model>`, here both are `lakeshore340`):

```yaml
entities:
  - type: lakeshore340.lakeshore340
    P: BL01T-EA-TEST-01
    PORT: p1
    ADDR: 12
    LOOP: 2
    SCAN: 5
    TEMPSCAN: 2
    name: lakeshore
```

The resulting `runtime-lock.yaml` looks like:

```yaml
version: v0.1.0
source: github.com/epics-containers/ibek-runtime-streamdevice
files:
  config/lakeshore340.ibek.support.yaml: "sha256:…"
  config/lakeshore340.proto: "sha256:…"
  config/lakeshore340.template: "sha256:…"
```

(a hash value may be `"DIRTY # <reason>"` for a deliberately locally-modified file).

### Update a pin

```bash
ibek pattern update lakeshore340 services/bl01t-ea-lake-01 -v v0.2.0
# or update every pinned pattern to its latest resolvable version:
ibek pattern update services/bl01t-ea-lake-01
```

### Check integrity (CI / pre-commit)

```bash
ibek pattern check services/bl01t-ea-lake-01
```

Re-hashes each vendored file and fails if it drifts from `runtime-lock.yaml`. Allow
intentional local edits with `--allow-dirty` (or `IBEK_ALLOW_DIRTY=1`); such files must
be marked `DIRTY` in the lock.

### Restore vendored files

```bash
ibek pattern restore lakeshore340 services/bl01t-ea-lake-01   # one pattern
ibek pattern restore services/bl01t-ea-lake-01                # all patterns
```

Rewrites the vendored files from the locked version, discarding local edits.

### Inspect the merged schema

```bash
ibek pattern schema services/bl01t-ea-lake-01
```

> The vendored files are generated into their runtime locations (proto/DB placement)
> by `ibek runtime generate2 <config-dir>` when the IOC starts, so the pattern's
> StreamDevice protocol and DB end up where the IOC loads them from.

## Relationship to `ibek-support` (build-time path)

`lakeshore340` also exists in
[epics-containers/ibek-support](https://github.com/epics-containers/ibek-support). The
two are **different delivery paths for the same device**, and must not silently
diverge:

- **This repo (runtime path) is canonical for runtime vendoring.** Patterns are
  vendored into an instance at a pinned version and loaded by a *generic*
  `ioc-streamdevice` image **with no image rebuild**. There is no `install.yml` and no
  compilation step — just protocol/DB/support files.
- **`ibek-support`'s `lakeshore340` is the build-time / compiled path.** It carries an
  `install.yml` and is baked into a purpose-built container image at build time.

When you change `lakeshore340` device support (protocol, records, or parameters), apply
the equivalent change to **both** repos, or explicitly document why they differ.
Treat them as two views of one device and keep them in step.

## Adding a new pattern

1. Create a top-level folder named after the pattern, e.g. `mydevice/`.
2. Drop in the file-set:
   - `mydevice.ibek.support.yaml` — the `ibek` support module (module name, one or more
     `entity_models` with their parameters, and a `databases:` list referencing the
     template/DB files),
   - the `*.proto`, `*.template`/`*.db`, and any other files that support yaml
     references.
3. Keep every file **pristine** — no vendored header (that is added by `ibek pattern`
   at vendor time).
4. Validate locally by vendoring into a scratch IOC instance:
   `ibek pattern add ibek-runtime-streamdevice:mydevice@HEAD <instance>` (or test
   against a branch) and run `ibek pattern check`.
5. Open a PR. Once merged, **cut a new semver tag** (`vX.Y.Z`) so consumers can pin the
   new pattern; Renovate will then offer the bump downstream.

## License

[Apache License 2.0](LICENSE).
