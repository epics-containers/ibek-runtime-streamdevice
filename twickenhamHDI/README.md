# twickenhamHDI

Runtime StreamDevice pattern imported from the DLS support module `twickenhamHDI`,
release `2-3` (`/dls_sw/prod/R3.14.12.7/support/twickenhamHDI/2-3`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`twickenhamHDI.ibek.support.yaml`](twickenhamHDI.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `twickenhamHDI.twickenhamHDI` | Imported from DLS module twickenhamHDI (twickenhamHDI.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `hdi.protocol`
- `twickenhamHDI.ibek.support.yaml`
- `twickenhamHDI.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
