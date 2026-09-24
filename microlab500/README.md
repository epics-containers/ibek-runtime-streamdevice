# microlab500

Runtime StreamDevice pattern imported from the DLS support module `microlab500`, release
`1-5` (`/dls_sw/prod/R3.14.12.7/support/microlab500/1-5`). Its protocol files are
pristine copies of that release; its templates are **derived** from the release's VDCT
sources.

How each file was obtained, and any change made to it, is recorded in the header of
[`microlab500.ibek.support.yaml`](microlab500.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `microlab500.microlab500` | Controls a Hamilton Microlab 500 series syringe pump NOTE: needs a generic IOC built with motor (not the plain generic image). |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `microlab500.ibek.support.yaml`
- `microlab500.proto`
- `microlab500half.template`
- `microlab500whole.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (1 file)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[BUILD-TIME-ONLY.md](../BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `microlab500whole.template` | the motor record |
