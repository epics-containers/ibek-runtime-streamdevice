# lakeshore331

Runtime StreamDevice pattern imported from the DLS support module `lakeshore331`,
release `1-13` (`/dls_sw/prod/R3.14.12.7/support/lakeshore331/1-13`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`lakeshore331.ibek.support.yaml`](lakeshore331.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `lakeshore331.lakeshore331` | Lakeshore 331 Temperature Controller Notes: The temperatures in Kelvin are archived once every 10 secs. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `lakeshore331.ibek.support.yaml`
- `lakeshore331.protocol`
- `lakeshore331.template`
- `lakeshore331_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
