# linkam

Runtime StreamDevice pattern imported from the DLS support module `linkam`, release
`2-15` (`/dls_sw/prod/R3.14.12.7/support/linkam/2-15`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`linkam.ibek.support.yaml`](linkam.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `linkam.linkam` | Linkam temperature stage controller. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `linkam.ibek.support.yaml`
- `linkam.proto`
- `linkam.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
