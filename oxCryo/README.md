# oxCryo

Runtime StreamDevice pattern imported from the DLS support module `OXCryo`, release
`1-4` (`/dls_sw/prod/R3.14.12.7/support/OXCryo/1-4`). Its protocol files are pristine
copies of that release; its templates are **derived** from the release's VDCT sources.

How each file was obtained, and any change made to it, is recorded in the header of
[`oxCryo.ibek.support.yaml`](oxCryo.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `oxCryo.OXPH700` | Control for Oxford cryostream 700 series (Phenix) |
| `oxCryo.OXCS700` | Control for Oxford cryostream 700 series |
| `oxCryo.OXCB700` | Control for Oxford Cryostream 700 series (Cobra) |
| `oxCryo.OXNH700` | Control for Oxford N-Helix 700 series |
| `oxCryo.OXCB800` | Control for Oxford Cryostream 800 series (Cobra) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `OXCB700.proto`
- `OXCB700.template`
- `OXCB700_settings.req`
- `OXCB800.proto`
- `OXCB800.template`
- `OXCB800_settings.req`
- `OXCS700.proto`
- `OXCS700.template`
- `OXCS700_settings.req`
- `OXNH700.proto`
- `OXNH700.template`
- `OXNH700_settings.req`
- `OXPH700.template`
- `OXcommon.proto`
- `OXcommon.template`
- `OXcommonCB.template`
- `oxCryo.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file

## Upstream defects carried as-is

- `OXPH700`/`OXCB700` protocols redirect into records their templates lack
