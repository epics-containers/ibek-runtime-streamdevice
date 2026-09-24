# motomanNX100

Runtime StreamDevice pattern imported from the DLS support module `motomanNX100`,
release `1-17-1` (`/dls_sw/prod/R3.14.12.7/support/motomanNX100/1-17-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`motomanNX100.ibek.support.yaml`](motomanNX100.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `motomanNX100.nx100` | Imported from DLS module motomanNX100 (nx100.template) |
| `motomanNX100.nx100dvar` | Imported from DLS module motomanNX100 (nx100dvar.template) |
| `motomanNX100.nx100io` | Imported from DLS module motomanNX100 (nx100io.template) |
| `motomanNX100.nx100pvar` | Imported from DLS module motomanNX100 (nx100pvar.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `motomanNX100.ibek.support.yaml`
- `nx100.proto`
- `nx100.template`
- `nx100dvar.template`
- `nx100io.template`
- `nx100pvar.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
