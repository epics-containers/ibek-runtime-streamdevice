# ETLdetector

Runtime StreamDevice pattern imported from the DLS support module `ETLdetector`, release
`1-21` (`/dls_sw/prod/R3.14.12.7/support/ETLdetector/1-21`). Its files are pristine
copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ETLdetector.ibek.support.yaml`](ETLdetector.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `ETLdetector.ETLdetector` | Comms for ETL (SENS-tech) scintillator detector |
| `ETLdetector.ETLdetectorDebug` | Imported from DLS module ETLdetector (ETLdetectorDebug.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ETLdetector.ibek.support.yaml`
- `ETLdetector.protocol`
- `ETLdetector.template`
- `ETLdetectorDebug.template`
- `ETLdetector_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (3 files)
