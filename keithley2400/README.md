# keithley2400

Runtime StreamDevice pattern imported from the DLS support module `keithley2400`,
release `1-23` (`/dls_sw/prod/R3.14.12.7/support/keithley2400/1-23`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`keithley2400.ibek.support.yaml`](keithley2400.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `keithley2400.Keithley2400` | Keithley 2400 SourceMeter |
| `keithley2400.Keithley2461` | Keithley 2461 SourceMeter |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `k2400.proto`
- `k2400.template`
- `k2400_detail.template`
- `k2400_settings.req`
- `k2461.proto`
- `k2461.template`
- `k2461_settings.req`
- `keithley2400.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
