# Keithley6487

Runtime StreamDevice pattern imported from the DLS support module `Keithley6487`,
release `1-1dls8` (`/dls_sw/prod/R3.14.12.7/support/Keithley6487/1-1dls8`). Its files
are pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`Keithley6487.ibek.support.yaml`](Keithley6487.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `Keithley6487.Keithley6487` | Controls a Keithley 6487 picoammeter |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `Keithley6487.ibek.support.yaml`
- `devKeithley6487.db`
- `devKeithley6487.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (4 files)
