# alicatGasFlow

Runtime StreamDevice pattern imported from the DLS support module `alicatGasFlow`,
release `2-15` (`/dls_sw/prod/R3.14.12.7/support/alicatGasFlow/2-15`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`alicatGasFlow.ibek.support.yaml`](alicatGasFlow.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `alicatGasFlow.alicatGasFlow` | Alicat gas flow meter |
| `alicatGasFlow.alicatPressureCtrl` | Alicat pressure controller |
| `alicatGasFlow.alicatMassCtrl` | Alicat mass flow controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `alicatGasFlow.ibek.support.yaml`
- `alicatGasFlow.proto`
- `alicatGasFlow.template`
- `alicatGasFlow_settings.req`
- `alicatMC.proto`
- `alicatMassCtrl.template`
- `alicatMassCtrl_detail.template`
- `alicatMassCtrl_settings.req`
- `alicatPC.proto`
- `alicatPressureCtrl.template`
- `alicatPressureCtrl_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (3 files)
- `test/` - device tests from the DLS source release (1 file)
