# agilent4UHV

Runtime StreamDevice pattern imported from the DLS support module `agilent4UHV`, release
`0-1` (`/dls_sw/prod/R3.14.12.7/support/agilent4UHV/0-1`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`agilent4UHV.ibek.support.yaml`](agilent4UHV.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `agilent4UHV._agilent4UHVTemplate` | Agilent 4UHV Ion Pump Controller (controller-level template) |
| `agilent4UHV._agilent4UHVIonpTemplate` | Agilent 4UHV Ion Pump Controller (per-pump template) |
| `agilent4UHV.agilent4UHV` | Agilent 4UHV Ion Pump Controller |
| `agilent4UHV.agilent4UHVIonp` | Agilent 4UHV Ion Pump Controller (per-pump device) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `agilent4UHV.ibek.support.yaml`
- `agilent4UHV.proto`
- `agilent4UHV.template`
- `agilent4UHVIonp.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
