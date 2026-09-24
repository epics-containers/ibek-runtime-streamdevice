# specsVCU1000

Runtime StreamDevice pattern imported from the DLS support module `specsVCU1000`,
release `1-9-2` (`/dls_sw/prod/R3.14.12.7/support/specsVCU1000/1-9-2`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`specsVCU1000.ibek.support.yaml`](specsVCU1000.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `specsVCU1000.specsVCU1000` | SPECS VCU1000 controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `specsVCU1000.ibek.support.yaml`
- `specsVCU1000.proto`
- `specsVCU1000.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (12 files)
- `sim/` - device simulator from the DLS source release (1 file)
