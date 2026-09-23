# OxInstIPS

Runtime StreamDevice pattern imported from the DLS support module `OxInstIPS`, release
`2-0` (`/dls_sw/prod/R3.14.12.7/support/OxInstIPS/2-0`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`OxInstIPS.ibek.support.yaml`](OxInstIPS.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `OxInstIPS.OxInstIPS` | OxInstIPS Oxford Instruments superconducting magnet power supply controller device class. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `OxInstIPS.ibek.support.yaml`
- `OxInstIPS.protocol`
- `OxInstIPS.template`
- `OxInstIPS_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (3 files)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
