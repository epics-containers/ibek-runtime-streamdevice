# specsXRC1000

Runtime StreamDevice pattern imported from the DLS support module `specsXRC1000`,
release `0-1` (`/dls_sw/prod/R3.14.12.7/support/specsXRC1000/0-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`specsXRC1000.ibek.support.yaml`](specsXRC1000.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `specsXRC1000.specsXRC1000` | SPECS XRC1000 X-ray source controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `specsXRC1000.ibek.support.yaml`
- `specsXRC1000.proto`
- `specsXRC1000.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
