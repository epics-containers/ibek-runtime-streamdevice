# CanberraG64

Runtime StreamDevice pattern imported from the DLS support module `CanberraG64`, release
`1-7` (`/dls_sw/prod/R3.14.12.7/support/CanberraG64/1-7`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`CanberraG64.ibek.support.yaml`](CanberraG64.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `CanberraG64.CanberraG64` | Imported from DLS module CanberraG64 (CanberraG64.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `CanberraG64.ibek.support.yaml`
- `CanberraG64.protocol`
- `CanberraG64.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
