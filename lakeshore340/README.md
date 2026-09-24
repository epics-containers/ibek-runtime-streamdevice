# lakeshore340

Runtime StreamDevice pattern imported from the DLS support module `lakeshore340`,
release `2-6` (`/dls_sw/prod/R3.14.12.7/support/lakeshore340/2-6`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`lakeshore340.ibek.support.yaml`](lakeshore340.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `lakeshore340.lakeshore340` | Lakeshore 340 Temperature Controller Notes: The temperatures in Kelvin are archived once every 10 secs. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `lakeshore340.ibek.support.yaml`
- `lakeshore340.proto`
- `lakeshore340.template`
- `lakeshore340_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (2 files)
