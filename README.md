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
| `ibek.manifest.yaml` | declares which files are vendored, and where | **yes** in this repo |
| `README.md` | the pattern's documentation: source, entity models, files, caveats | **yes** in this repo |
| `docs/`, `sim/`, `test/` | documentation, device simulator and tests from the DLS source release | optional |

There is **no hard-coded proto/template/support shape**. The vendoring lock simply
hashes a **file list**, so it already generalises to any combination of the above (or
files not yet invented). Add the files your support yaml needs and they are vendored
together as a unit.

### Runtime files and pattern docs: `ibek.manifest.yaml`

A pattern folder holds two kinds of file: **runtime files**, which `ibek pattern`
copies into an IOC instance, and **pattern docs**, which stay in this library. The
pattern's `ibek.manifest.yaml` is what tells them apart. It is an ordered,
first-match-wins **allow-list**: each `src` regex is matched (`re.fullmatch`) against a
file's path relative to the pattern folder, and a file matched by no entry is never
vendored. Every pattern here carries the same manifest:

```yaml
version: 1
vendor:
  - src: '[^/]+\.(template|proto|protocol|db|req|ibek\.support\.yaml|pvi\.device\.yaml)$'
    dest: config
```

It vendors the runtime file types at the top of the folder into the instance's
`config/`, and nothing else: `README.md`, the manifest itself and everything under
`docs/`, `sim/` and `test/` stay here. A file that should reach the IOC must therefore
sit at the top of the folder with one of those suffixes; a new runtime file type needs
the regex extending in every manifest that ships one.

Each pattern's `README.md` says which DLS module and release the pattern came from,
lists its entity models and which files are vendored, and records what a user needs to
know before loading it: templates that need more than the generic image, and upstream
defects carried as-is. How each file was obtained, and any change made to it, stays in
the header of the pattern's `*.ibek.support.yaml`: that file is vendored, so the notes
travel into every IOC instance that uses the pattern.

The manifest format is documented in ibek's
[`ibek.manifest.yaml` reference](https://github.com/epics-containers/ibek/blob/main/docs/reference/pattern-manifest.md).
It needs ibek 4.8 or later; an older ibek ignores the manifest and vendors every file in
the folder.

This repo provides StreamDevice patterns for many devices, each a top-level folder
auto-generated from the device's DLS XMLbuilder support module (`etc/builder.py` +
its StreamDevice protocol and EPICS template). The `lakeshore340` pattern is the
worked example of the file-set:

```
lakeshore340/
  lakeshore340.ibek.support.yaml   # entity_model "lakeshore340", parameters, databases:
  lakeshore340.proto               # StreamDevice protocol
  lakeshore340.template            # EPICS records
  lakeshore340_settings.req        # autosave request file
  ibek.manifest.yaml               # vendors the four files above - not vendored itself
  README.md                        # pattern docs - not vendored
  sim/                             # device simulator - not vendored
  test/                            # device tests - not vendored
```

## Faithful storage

**Extracted device files stay as close to their DLS source as possible.** Copy
byte-for-byte wherever the file works unmodified; where it cannot, apply only
**mechanical, scripted, re-runnable** transformations and record that you did. Never
hand-edit an extracted file. They carry **no provenance header**.

The point of the old byte-for-byte rule was to keep patterns diffable against future
DLS releases. Reproducible derivation preserves that — you re-run the conversion on the
new release and compare, instead of diffing text.

### Pristine — always

`.proto`/`.protocol` files. StreamDevice protocol syntax is the same at DLS and in
epics-containers, so these are always exact copies.

### Derived — VDCT-authored databases

Many DLS modules author their databases in **VisualDCT**, which does not exist in the
vanilla EPICS 7 base the generic IOC images build against. A verbatim VDCT template
cannot load at runtime, so `.template`/`.db` from those modules are **derived**:
`expand()` blocks become native msi `substitute`/`include` directives, `#!` layout
lines and `template() { }` blocks are dropped, and macros passed into an included
template gain a `_` prefix. Done by
[vdct2template](https://github.com/epics-containers/vdct2template).

A derived pattern **must** say so in its `*.ibek.support.yaml` header, naming the source
module, version and `/dls_sw/prod/...` path, and which files are derived versus
pristine. See `currAmp/` for the worked example.

The procedure and its helper scripts live in the `vdct-conversion` skill in
[builder2ibek](https://github.com/epics-containers/builder2ibek).

### Derived — DLS annotation comments stripped

DLS databases carry comment lines for DLS screen and GDA tooling:

```
# % gui, $(name=), edm, device.edl, P=$(P)
#% gdatag,pv,ro,$(gda_name=),RANGE,Range Selection
# %gda,subsystem,ODCurrAmp,monitor,channel1,Channel 1 value
```

epics-containers has no consumer for them (screens come from PVI), yet msi and
`dbLoadRecords` expand macros on every line, comments included, so each macro they name
would need a value or the IOC logs `macLib: macro ... is undefined` at boot. They are
removed from every `.template`/`.db` by
[`strip-dls-annotations.py`](strip-dls-annotations.py), which also drops the
`# % macro` documentation lines and empty `databases` args left pointing at macros
nothing references any more. Record content is untouched. `# % macro` lines for live
macros, and `# % autosave`, `# % archiver`, `# % alh` and `# % controldesk` lines, stay.

Run it after importing templates from a DLS release; `--check` exits non-zero if any
file still needs it.

### Checking a pattern against a newer DLS release

- **Pristine files** — diff directly against `/dls_sw/prod/*/support/<module>/`.
- **Derived files** — re-run the conversion on the new release and diff the outputs.
- **Databases** — every `.template`/`.db` has had its annotation comments stripped, so
  run `strip-dls-annotations.py` over the imported release too before diffing.

For a stronger check than text diffing, expand both the pattern's template and the DLS
module's built `db/` copy with `msi` using the same macros, then compare canonical
record/field sets. That is invariant to comment, ordering and whitespace changes, and it
is what proves a conversion preserved behaviour. `currAmp` passes this on all six
templates.

### The support yaml

The repo-authored **`*.ibek.support.yaml`** is generated here rather than extracted, so
it begins with the DLS-source provenance comment described above. That comment is
static and deterministic, and is vendored along with the rest of the file.

### Vendored files are byte-identical

`ibek pattern` copies each runtime file into an IOC instance **verbatim**: it adds no
header and rewrites nothing, and the per-file `sha256` in the instance's
`runtime-lock.yaml` is taken over the library's bytes. So `diff -r` between an instance's
`config/` and the pattern folder at the pinned tag shows only the files the manifest
leaves out. The instance's provenance is the adjacent `runtime-lock.yaml`, which records
the library, the pinned tag and every vendored file's hash.

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
2. writes each runtime file the pattern's `ibek.manifest.yaml` selects into
   `services/bl01t-ea-lake-01/config/`, byte-for-byte,
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
version: 1
patterns:
  lakeshore340:
    version: v0.1.0
    source: github.com/epics-containers/ibek-runtime-streamdevice
    files:
      config/lakeshore340.ibek.support.yaml: sha256:…
      config/lakeshore340.proto: sha256:…
      config/lakeshore340.template: sha256:…
      config/lakeshore340_settings.req: sha256:…
```

Only the files the manifest selects appear: `README.md`, `sim/` and `test/` are not
vendored.

(a hash value may be `"DIRTY # <reason>"` for a deliberately locally-modified file).

### Update a pin

```bash
ibek pattern update services/bl01t-ea-lake-01 --name lakeshore340 --version v0.2.0
# or re-vendor every pinned pattern at its recorded version:
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
ibek pattern restore services/bl01t-ea-lake-01 --name lakeshore340   # one pattern
ibek pattern restore services/bl01t-ea-lake-01                       # all patterns
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

Not every DLS StreamDevice module can take the runtime path: some need a module-specific
**compiled** library, `.dbd`, or SNL sequencer program that the generic
`ioc-streamdevice` image does not ship, so they are build-time-only. Those modules — and
the test used to tell them apart — are listed in [BUILD-TIME-ONLY.md](BUILD-TIME-ONLY.md).

## Adding a new pattern

1. Create a top-level folder named after the pattern, e.g. `mydevice/`.
2. Drop in the file-set:
   - `mydevice.ibek.support.yaml` — the `ibek` support module (module name, one or more
     `entity_models` with their parameters, and a `databases:` list referencing the
     template/DB files),
   - the `*.proto`, `*.template`/`*.db`, and any other files that support yaml
     references,
   - `ibek.manifest.yaml` — copy it from any other pattern; extend its `src` regex only
     for a runtime file type it does not list,
   - `README.md` — the pattern docs, following any other pattern's `README.md`,
   - any publishable documentation, simulator or tests from the DLS source release, in
     `docs/`, `sim/` and `test/`.
3. Copy each file unmodified where it works as-is. If the module is VDCT-authored,
   convert it as described in [Faithful storage](#faithful-storage)
   — scripted, never hand-edited — and record the derivation in the support yaml header.
   Add nothing to the files for the vendoring step: `ibek pattern` copies them verbatim.
4. Validate locally by vendoring into a scratch IOC instance:
   `ibek pattern add mydevice@work <instance> --source <this repo's checkout>`, run
   `ibek pattern check <instance>`, and confirm `<instance>/config/` holds the runtime
   files and nothing from `README.md`, `docs/`, `sim/` or `test/`.
   For a derived pattern also check `msi` expands it with no undefined macros, and that
   its canonical record/field set matches the DLS module's built `db/` copy.
5. Open a PR. Once merged, **cut a new semver tag** (`vX.Y.Z`) so consumers can pin the
   new pattern; Renovate will then offer the bump downstream.

## CI checks

Every pull request runs the checks in `ci/`, which also run locally from the
repo root with [uv](https://docs.astral.sh/uv/):

| Check | Command |
|---|---|
| Schema: each `*.ibek.support.yaml` against the pinned ibek release's `ibek.support.schema.json` and ibek's loader; each `ibek.manifest.yaml` through ibek's vendoring plan | `uv run --with-requirements ci/requirements.txt ci/check_schema.py` |
| Autosave: each `.req` file holds exactly the PVs its template's `# % autosave` tags give | `uv run --with-requirements ci/requirements.txt ci/check_autosave.py` |
| Content: no hostnames, IP addresses, internal URLs or credentials | `uv run --with-requirements ci/requirements.txt ci/check_content.py` |
| Pattern add: a real `ibek pattern add` of every pattern, and of a sample together, into a scratch services repo; checks the lock, the vendored files, the instance schema and `ibek pattern check` | `uv run --with-requirements ci/requirements.txt ci/check_pattern_add.py` |
| Template load: every vendored template loaded through `iocInit` in the generic `ioc-streamdevice` IOC, with the macros its entity model passes | see below |

Each takes pattern names to check only those patterns. The template load test
runs inside the published generic IOC image named in `.github/workflows/ci.yml`:

```bash
uv run --with-requirements ci/requirements.txt ci/template_load.py prepare build/load
docker run --rm -v "$PWD:$PWD" -w "$PWD" \
    ghcr.io/epics-containers/ioc-streamdevice-runtime:2.8.26ec4 \
    python ci/template_load.py run build/load
```

The ibek version the checks use is pinned in `ci/requirements.txt`; move it
deliberately when the library adopts a new ibek. Known faults in the library
content are listed, each with its reason, in `ci/template-load.yaml`,
`ci/autosave-allow.yaml` and `ci/content-allow.yaml`; an entry that no longer
applies fails its check, so remove it when the fault is fixed.

## License

[Apache License 2.0](LICENSE).
