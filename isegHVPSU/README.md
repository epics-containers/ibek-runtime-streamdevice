# isegHVPSU

Runtime StreamDevice pattern imported from the DLS support module `isegHVPSU`, release
`2-1` (`/dls_sw/prod/R3.14.12.7/support/isegHVPSU/2-1`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`isegHVPSU.ibek.support.yaml`](isegHVPSU.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `isegHVPSU.isegNHQ223M` | ISEG HV PSU template file. Notes: The voltages and currents are archived every 10s All other parameters (including status) are read on demand |
| `isegHVPSU.isegHVPSU` | ISEG HV PSU template file. Notes: The voltages and currents are archived every 10s All other parameters (including status) are read on demand |
| `isegHVPSU.trigger_process` | Imported from DLS module isegHVPSU (trigger_process.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `isegHVPSU.ibek.support.yaml`
- `isegHVPSU.proto`
- `isegHVPSU.template`
- `isegHVPSU_settings.req`
- `isegNHQ223M.template`
- `isegNHQ223M_settings.req`
- `trigger_process.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
