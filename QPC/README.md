# QPC

Runtime StreamDevice pattern imported from the DLS support module `QPC`, release `2-3`
(`/dls_sw/prod/R3.14.12.7/support/QPC/2-3`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`QPC.ibek.support.yaml`](QPC.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `QPC.digitelQpc` | Digitel QPC ion pump controller (single QPC controller) |
| `QPC.digitelQpcIonp` | Template database for digitel QPC - Ion Pump |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `QPC.ibek.support.yaml`
- `digitelQPCController.template`
- `digitelQpc.proto`
- `digitelQpcIonp.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (1 file)
