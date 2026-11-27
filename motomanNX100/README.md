# motomanNX100

Runtime StreamDevice pattern imported from the DLS support module `motomanNX100`,
release `1-17-1` (`/dls_sw/prod/R3.14.12.7/support/motomanNX100/1-17-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`motomanNX100.ibek.support.yaml`](motomanNX100.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

The models are ibek-support-dls's `motomanNX100` models, but for its two BL11I ones
(see below), with `PORT` a string as in `builder.py`.

| Entity model | Description |
|---|---|
| `motomanNX100.nx100` | Setup a motoman NX100 motor controller for use with EPICS |
| `motomanNX100.nx100dvar` | Set and Read a D (decimal) variable on the robot |
| `motomanNX100.nx100pvar` | Set and Read a P (position) variable on the robot |
| `motomanNX100.auto_nx100io` | Reads digital I/O variables from the robot (`nx100io.template`, under the name XMLbuilder gives it) |
| `motomanNX100.nx100io` | The same as `auto_nx100io` |

The release's `BL11I-barcode.db` and `BL11I-robot-interlocks.db` (builder's
`auto_BL11I_barcode` and `auto_BL11I_robot_interlocks`) serve one beamline. They belong
in a BL11I pattern of ibek-runtime-support, not here.

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `auto_nx100io.pvi.device.yaml`
- `motomanNX100.ibek.support.yaml`
- `nx100.proto`
- `nx100.pvi.device.yaml`
- `nx100.template`
- `nx100dvar.pvi.device.yaml`
- `nx100dvar.template`
- `nx100io.pvi.device.yaml`
- `nx100io.template`
- `nx100pvar.pvi.device.yaml`
- `nx100pvar.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
