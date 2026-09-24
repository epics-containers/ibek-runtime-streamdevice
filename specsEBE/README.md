# specsEBE

Runtime StreamDevice pattern imported from the DLS support module `specsEBE`, release
`0-7` (`/dls_sw/prod/R3.14.12.7/support/specsEBE/0-7`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`specsEBE.ibek.support.yaml`](specsEBE.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `specsEBE.EBE4` | Specs EBE-4 template file. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ebe4.db`
- `ebe4.proto`
- `ebe4_settings.req`
- `specsEBE.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (7 files)
