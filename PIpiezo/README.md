# PIpiezo

Runtime StreamDevice pattern imported from the DLS support module `PIpiezo`, release
`1-23` (`/dls_sw/prod/R3.14.12.7/support/PIpiezo/1-23`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`PIpiezo.ibek.support.yaml`](PIpiezo.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `PIpiezo.E725` | Controls a PI E725 piezo controller |
| `PIpiezo.E871` | Controls a PI E871 piezo controller |
| `PIpiezo.E816` | Controls a PI E816 piezo controller |
| `PIpiezo.C877` | Controls a PI C877 piezo controller |
| `PIpiezo.E871-absGrp` | Imported from DLS module PIpiezo (E871-absGrp.template) NOTE: needs a generic IOC built with PIpiezo (not the plain generic image). |
| `PIpiezo.E871-relGrp` | Imported from DLS module PIpiezo (E871-relGrp.template) |
| `PIpiezo.PI-E516` | Imported from DLS module PIpiezo (PI-E516.template) NOTE: needs a generic IOC built with PIpiezo (not the plain generic image). |
| `PIpiezo.actuatorcallback` | Imported from DLS module PIpiezo (actuatorcallback.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `C877.proto`
- `C877.template`
- `E725.proto`
- `E725.template`
- `E725_positions.req`
- `E725_settings.req`
- `E816.proto`
- `E816.template`
- `E816_positions.req`
- `E871-absGrp.template`
- `E871-absGrp_positions.req`
- `E871-absGrp_settings.req`
- `E871-relGrp.template`
- `E871.proto`
- `E871.template`
- `PI-E516.template`
- `PIpiezo.ibek.support.yaml`
- `actuatorcallback.template`
- `e725Z_detail.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (3 files)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `E871-absGrp.template`, `PI-E516.template` | the motor record |

## Upstream defects carried as-is

- `C877` `REF:MODE` has a stream INP but no DTYP
