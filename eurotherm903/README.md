# eurotherm903

Runtime StreamDevice pattern imported from the DLS support module `eurotherm903`,
release `1-9-2` (`/dls_sw/prod/R3.14.12.7/support/eurotherm903/1-9-2`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`eurotherm903.ibek.support.yaml`](eurotherm903.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `eurotherm903.Eurotherm903` | Eurotherm 903 temperature controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `eurotherm903.ibek.support.yaml`
- `eurotherm903.proto`
- `eurotherm903.template`
- `eurotherm903_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
