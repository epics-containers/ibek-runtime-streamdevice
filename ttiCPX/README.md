# ttiCPX

Runtime StreamDevice pattern imported from the DLS support module `ttiCPX`, release
`3-0` (`/dls_sw/prod/R3.14.12.7/support/ttiCPX/3-0`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ttiCPX.ibek.support.yaml`](ttiCPX.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `ttiCPX.ttiCPX` | TTi CPX Power Supply |
| `ttiCPX.ttiCPXChannel` | TTi CPX Power Supply channel |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ttiCPX.ibek.support.yaml`
- `ttiCPX.proto`
- `ttiCPX_channel.template`
- `ttiCPX_channel_settings.req`
- `ttiCPX_general.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
