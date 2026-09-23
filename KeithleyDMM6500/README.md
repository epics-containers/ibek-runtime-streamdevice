# KeithleyDMM6500

Runtime StreamDevice pattern imported from the DLS support module `KeithleyDMM6500`,
release `1-1` (`/dls_sw/prod/R3.14.12.7/support/KeithleyDMM6500/1-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`KeithleyDMM6500.ibek.support.yaml`](KeithleyDMM6500.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `KeithleyDMM6500.dmm6500` | Device to control Keithley DMM6500 Multimeter |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `KeithleyDMM6500.ibek.support.yaml`
- `dmm6500.proto`
- `dmm6500.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
