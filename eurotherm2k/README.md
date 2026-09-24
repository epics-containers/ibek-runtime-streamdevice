# eurotherm2k

Runtime StreamDevice pattern imported from the DLS support module `eurotherm2k`, release
`2-10` (`/dls_sw/prod/R3.14.12.7/support/eurotherm2k/2-10`). Its templates and protocol
file are pristine copies of that release. The `eurotherm2k.eurotherm2k` entity model is
hand-written
([ibek-runtime-streamdevice#22](https://github.com/epics-containers/ibek-runtime-streamdevice/issues/22))
and sets its own defaults for `SPMAX` (`100`) and `EGU` (`C/min`), which differ from
`eurotherm2k.template`'s defaults of `1000` and `C/s`.

How each file was obtained, and any change made to it, is recorded in the header of
[`eurotherm2k.ibek.support.yaml`](eurotherm2k.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `eurotherm2k.eurotherm2k` | Eurotherm 2k temperature controller |
| `eurotherm2k.eurothermParam` | Set and read back a parameter on a eurotherm 2k series controller |
| `eurotherm2k.eurothermConfParam` | Generic database for setting a parameter on a eurotherm 2k series controller, works when it is in configure mode. |
| `eurotherm2k.eurothermPV` | Read back a process value from a eurotherm 2k series controller |
| `eurotherm2k.eurothermModbus` | Controls the eurotherm 2000 series temp controller via modbus interface NOTE: needs a generic IOC built with eurotherm2k (not the plain generic image). |
| `eurotherm2k.eurothermModbusLoop` | Controls an individual channel of eurotherm, requires a eurothermModbus entry NOTE: needs a generic IOC built with eurotherm2k (not the plain generic image). |
| `eurotherm2k.eurothermModbusPV` | Controls an individual channel of eurotherm, requires a eurothermModbus entry NOTE: needs a generic IOC built with eurotherm2k (not the plain generic image). |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `eurotherm2k.ibek.support.yaml`
- `eurotherm2k.proto`
- `eurotherm2k.template`
- `eurotherm2k_settings.req`
- `eurothermConfParam.template`
- `eurothermModbus.template`
- `eurothermModbusLoop.template`
- `eurothermModbusLoop_settings.req`
- `eurothermModbusPV.template`
- `eurothermPV.template`
- `eurothermParam.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (3 files)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `eurothermModbus.template`, `eurothermModbusLoop.template`, `eurothermModbusPV.template` | compiled Modbus asyn driver (`drvModbusAsynConfigure`, `eurothermModbusCtrlConfigure`) |
