# GR150

Runtime StreamDevice pattern imported from the DLS support module `GR150`, release
`2-5-5` (`/dls_sw/prod/R3.14.12.7/support/GR150/2-5-5`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`GR150.ibek.support.yaml`](GR150.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `GR150.gr150` | Support for Grant GR150 chiller. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `GR150.ibek.support.yaml`
- `gr150.protocol`
- `gr150.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (2 files)
