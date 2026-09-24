# fw102

Runtime StreamDevice pattern imported from the DLS support module `fw102`, release `2-1`
(`/dls_sw/prod/R3.14.12.7/support/fw102/2-1`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`fw102.ibek.support.yaml`](fw102.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `fw102._fw102Template` | Thorlabs FW102 motorised filter wheel |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `fw102.ibek.support.yaml`
- `fw102.proto`
- `fw102.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
