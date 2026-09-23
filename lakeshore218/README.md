# lakeshore218

Runtime StreamDevice pattern imported from the DLS support module `lakeshore218`,
release `2-9` (`/dls_sw/prod/R3.14.12.7/support/lakeshore218/2-9`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`lakeshore218.ibek.support.yaml`](lakeshore218.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `lakeshore218.lakeshore218` | Lakeshore 218 Temperature Monitor Notes: The temperatures in Kelvin are archived once every 10 secs. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `lakeshore218.ibek.support.yaml`
- `lakeshore218.proto`
- `lakeshore218.template`
- `lakeshore218_settings.req`
- `lakeshore218channel.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
