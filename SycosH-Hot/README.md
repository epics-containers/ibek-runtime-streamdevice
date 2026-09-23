# SycosH-Hot

Runtime StreamDevice pattern imported from the DLS support module `SycosH-Hot`, release
`1-8` (`/dls_sw/prod/R3.14.12.7/support/SycosH-Hot/1-8`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`SycosH-Hot.ibek.support.yaml`](SycosH-Hot.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `SycosH-Hot.SycosH_Hot` | SycosH-Hot humidity generator controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `SycosH-Hot.ibek.support.yaml`
- `SycosH-Hot.proto`
- `SycosH-Hot.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
