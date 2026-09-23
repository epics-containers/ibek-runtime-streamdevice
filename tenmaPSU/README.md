# tenmaPSU

Runtime StreamDevice pattern imported from the DLS support module `tenmaPSU`, release
`0-4-3` (`/dls_sw/prod/R3.14.12.7/support/tenmaPSU/0-4-3`). Its files are pristine
copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`tenmaPSU.ibek.support.yaml`](tenmaPSU.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `tenmaPSU.tenma` | Tenma PSU |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `tenma.proto`
- `tenma.template`
- `tenmaPSU.ibek.support.yaml`
- `tenma_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
