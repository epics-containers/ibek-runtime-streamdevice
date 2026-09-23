# tdklambda

Runtime StreamDevice pattern imported from the DLS support module `tdklambda`, release
`1-5` (`/dls_sw/prod/R3.14.12.7/support/tdklambda/1-5`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`tdklambda.ibek.support.yaml`](tdklambda.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `tdklambda.Gen3300w` | TDK Lambda 3300W power supply |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `gen3300w.proto`
- `gen3300w.template`
- `tdklambda.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
