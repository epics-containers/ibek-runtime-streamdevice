# macroSensors

Runtime StreamDevice pattern imported from the DLS support module `macroSensors`,
release `2-0` (`/dls_sw/prod/R3.14.12.7/support/macroSensors/2-0`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`macroSensors.ibek.support.yaml`](macroSensors.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `macroSensors.dmc_a2` | Support for the macro sensors dual channel LVDT reader. The raw readings are available in the ':LVDT' PVs. A linear translation function is also applied with the result available in the ':VAL' PVs. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `dmc-a2.proto`
- `dmc-a2.template`
- `dmc-a2_settings.req`
- `macroSensors.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
