# chemyxFusion

Runtime StreamDevice pattern imported from the DLS support module `chemyxFusion`,
release `1-0` (`/dls_sw/prod/R3.14.12.7/support/chemyxFusion/1-0`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`chemyxFusion.ibek.support.yaml`](chemyxFusion.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `chemyxFusion.Fusion4000` | Chemyx Fusion 4000 syringe pump controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `chemyxFusion.ibek.support.yaml`
- `fusion4000.proto`
- `fusion4000.template`
- `fusion4000_parameter.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
