# CryoconM32

Runtime StreamDevice pattern imported from the DLS support module `CryoconM32`, release
`1-7` (`/dls_sw/prod/R3.14.12.7/support/CryoconM32/1-7`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`CryoconM32.ibek.support.yaml`](CryoconM32.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `CryoconM32.CryoconM32` | CryoconM32 temperature controller device class (includes sensors and control loops configured with other classes). |
| `CryoconM32.CryoconM32_control` | A control loop for the CryoconM32 |
| `CryoconM32.CryoconM32_sensor` | A sensor channel for the CryoconM32 |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `CryoconM32.ibek.support.yaml`
- `CryoconM32.protocol`
- `M32_control.template`
- `M32_sensor.template`
- `M32_system.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)

## Upstream defects carried as-is

- `STS:SINKTEMP` has a stream INP but no DTYP
