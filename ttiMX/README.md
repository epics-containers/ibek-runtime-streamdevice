# ttiMX

Runtime StreamDevice pattern imported from the DLS support module `ttiMX`, release `1-4`
(`/dls_sw/prod/R3.14.12.7/support/ttiMX/1-4`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ttiMX.ibek.support.yaml`](ttiMX.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `ttiMX.ttiMX_channel` | Imported from DLS module ttiMX (ttiMX_channel.template) |
| `ttiMX.ttiMX_general` | Imported from DLS module ttiMX (ttiMX_general.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ttiMX.ibek.support.yaml`
- `ttiMX.proto`
- `ttiMX_channel.template`
- `ttiMX_channel_settings.req`
- `ttiMX_general.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
