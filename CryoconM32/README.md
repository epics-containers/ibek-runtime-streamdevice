# CryoconM32

Runtime StreamDevice pattern imported from the DLS support module `CryoconM32`, release
`1-7` (`/dls_sw/prod/R3.14.12.7/support/CryoconM32/1-7`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`CryoconM32.ibek.support.yaml`](CryoconM32.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

Its entity models mirror the DLS `etc/builder.py`: builder class names, parameters named
as the builder XML attributes, `Ident` arguments as `object` references, and the
arguments builder.py derives done in Jinja. So builder2ibek converts a builder XML to
this pattern without redoing builder.py's work.

## Entity models

| Entity model | Loads | Description |
|---|---|---|
| `CryoconM32.CryoconM32` | `M32_system.template` | CryoconM32 temperature controller device class (includes sensors and control loops configured with other classes). `name` is the id its sensors' and loops' `tctrlr` names. |
| `CryoconM32.CryoconM32_sensor` | `M32_sensor.template` | A sensor channel of the CryoconM32 `tctrlr`, whose PV prefix and port it takes. |
| `CryoconM32.CryoconM32_control` | `M32_control.template` | A control loop of the CryoconM32 `tctrlr`, whose PV prefix and port it takes. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `CryoconM32.ibek.support.yaml`
- `CryoconM32.protocol`
- `CryoconM32.pvi.device.yaml`
- `CryoconM32_control.pvi.device.yaml`
- `CryoconM32_sensor.pvi.device.yaml`
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
