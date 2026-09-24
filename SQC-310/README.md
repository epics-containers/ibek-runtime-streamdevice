# SQC-310

Runtime StreamDevice pattern imported from the DLS support module `SQC-310`, release
`0-2` (`/dls_sw/prod/R3.14.12.7/support/SQC-310/0-2`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`SQC-310.ibek.support.yaml`](SQC-310.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `SQC-310.SQC310` | SQC-310 Quartz Crystal Microbalance |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `SQC-310.ibek.support.yaml`
- `SQC-310.proto`
- `SQC-310.template`
- `SQC-310_material.template`
- `SQC-310_sensor.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
