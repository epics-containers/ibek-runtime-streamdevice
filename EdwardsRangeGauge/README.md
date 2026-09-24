# EdwardsRangeGauge

Runtime StreamDevice pattern imported from the DLS support module `EdwardsRangeGauge`,
release `23-4` (`/dls_sw/prod/R3.14.12.7/support/EdwardsRangeGauge/23-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`EdwardsRangeGauge.ibek.support.yaml`](EdwardsRangeGauge.ibek.support.yaml). That
header is vendored with the pattern, so the provenance travels into every IOC instance
that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `EdwardsRangeGauge.EdwardsRangeGauge` | Template for Serial control and monitoring of Edwards Pressure pumps via serial. Usually in collaboration with a PLC which has On/Off control. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `EdGauge.proto`
- `EdwardsGauge.template`
- `EdwardsRangeGauge.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
