# smc

Runtime StreamDevice pattern imported from the DLS support module `smc`, release `1-8`
(`/dls_sw/prod/R3.14.12.7/support/smc/1-8`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`smc.ibek.support.yaml`](smc.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `smc.magnet` | Imported from DLS module smc (magnet.template) |
| `smc.smc` | Imported from DLS module smc (smc.template) |
| `smc.smcTripleAxis` | Imported from DLS module smc (smcTripleAxis.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `magnet.template`
- `magnet_settings.req`
- `smc.ibek.support.yaml`
- `smc.protocol`
- `smc.template`
- `smcTripleAxis.template`
- `smc_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (1 file)
