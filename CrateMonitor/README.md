# CrateMonitor

Runtime StreamDevice pattern imported from the DLS support module `CrateMonitor`,
release `2-4` (`/dls_sw/prod/R3.14.12.7/support/CrateMonitor/2-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`CrateMonitor.ibek.support.yaml`](CrateMonitor.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `CrateMonitor.CrateMonitor` | VME Crate Monitor (fan speeds, supply voltages, temperatures and status). |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `CrateMon.proto`
- `CrateMonitor.ibek.support.yaml`
- `CrateMonitor.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
