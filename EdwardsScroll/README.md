# EdwardsScroll

Runtime StreamDevice pattern imported from the DLS support module `EdwardsScroll`,
release `1-15` (`/dls_sw/prod/R3.14.12.7/support/EdwardsScroll/1-15`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`EdwardsScroll.ibek.support.yaml`](EdwardsScroll.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `EdwardsScroll.EdwardsScroll` | Template for Serial control and monitoring of Edwards Scroll pumps via serial. Usually in collaboration with a PLC which has On/Off control. |
| `EdwardsScroll.EdwardsScroll_SerialOnOffExtra` | Imported from DLS module EdwardsScroll (EdwardsScroll_SerialOnOffExtra.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `EdScroll.proto`
- `EdwardsScroll.ibek.support.yaml`
- `EdwardsScroll.template`
- `EdwardsScroll_SerialOnOffExtra.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
