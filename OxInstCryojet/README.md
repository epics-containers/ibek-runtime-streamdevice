# OxInstCryojet

Runtime StreamDevice pattern imported from the DLS support module `OxInstCryojet`,
release `2-28` (`/dls_sw/prod/R3.14.12.7/support/OxInstCryojet/2-28`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`OxInstCryojet.ibek.support.yaml`](OxInstCryojet.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `OxInstCryojet.cryojetITC503S` | Oxford Instruments Cryojet ITC503S temperature controller |
| `OxInstCryojet.cryojet` | Oxford Instruments Cryojet temperature controller |
| `OxInstCryojet.MercuryiTC_SCPI_heater` | Oxford Instruments MercuryiTC SCPI heater commands |
| `OxInstCryojet.MercuryiTC_SCPI_loop` | Oxford Instruments MercuryiTC SCPI loop commands |
| `OxInstCryojet.MercuryiTC_SCPI_system` | Oxford Instruments MercuryiTC SCPI system commands |
| `OxInstCryojet.MercuryiTC_SCPI_tempSensor` | Oxford Instruments MercuryiTC SCPI temperature sensor commands |
| `OxInstCryojet.ILM201` | Imported from DLS module OxInstCryojet (ILM201.template) |
| `OxInstCryojet.ITC4` | Imported from DLS module OxInstCryojet (ITC4.template) |
| `OxInstCryojet.MercuryiTC_SCPI` | Oxford Instruments Mercury iTC: system, one temperature sensor, one heater and one loop (the motherboard configuration) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ILM201.template`
- `ILM201_settings.req`
- `ITC4.template`
- `ITC4_settings.req`
- `MercuryiTC-SCPI.proto`
- `MercuryiTC-SCPI.template`
- `MercuryiTC-SCPI_heater.template`
- `MercuryiTC-SCPI_loop.template`
- `MercuryiTC-SCPI_system.template`
- `MercuryiTC-SCPI_tempSensor.template`
- `OxInstCryojet.ibek.support.yaml`
- `cjet.proto`
- `cryojet.template`
- `cryojetITC503S.template`
- `cryojetITC503S_settings.req`
- `cryojet_settings.req`
- `itc4.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (2 files)
- `test/` - device tests from the DLS source release (1 file)
