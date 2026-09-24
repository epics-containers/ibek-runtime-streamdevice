# enzLoCuM4

Runtime StreamDevice pattern imported from the DLS support module `enzLoCuM4`, release
`2-42` (`/dls_sw/prod/R3.14.12.7/support/enzLoCuM4/2-42`). Its files are pristine copies
of that release, apart from the scripted changes its support yaml header lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`enzLoCuM4.ibek.support.yaml`](enzLoCuM4.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `enzLoCuM4.enzLoCuM4` | Template database for an ENZ LoCuM-4 Low Current Monitor |
| `enzLoCuM4.enzLoCuM4Readback` | Imported from DLS module enzLoCuM4 (enzLoCuM4Readback.template) NOTE: needs a generic IOC built with enzLoCuM4 (not the plain generic image). |
| `enzLoCuM4.enzLoCuM4Readback_generic_diagonal` | Imported from DLS module enzLoCuM4 (enzLoCuM4Readback_generic_diagonal.template) |
| `enzLoCuM4.enzLoCuM4Readback_generic_vertical` | Imported from DLS module enzLoCuM4 (enzLoCuM4Readback_generic_vertical.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `enzLoCuM4.ibek.support.yaml`
- `enzLoCuM4.protocol`
- `enzLoCuM4.template`
- `enzLoCuM4Readback.template`
- `enzLoCuM4Readback_generic_common.template`
- `enzLoCuM4Readback_generic_diagonal.template`
- `enzLoCuM4Readback_generic_vertical.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (2 files)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `enzLoCuM4Readback.template` | `DTYP "Hy8401ip"` (Hytec IP ADC) |
