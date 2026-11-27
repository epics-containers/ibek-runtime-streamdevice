# agilent4UHV

Runtime StreamDevice pattern imported from the DLS support module `agilent4UHV`, release
`0-1` (`/dls_sw/prod/R3.14.12.7/support/agilent4UHV/0-1`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`agilent4UHV.ibek.support.yaml`](agilent4UHV.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

Its entity models mirror the DLS `etc/builder.py`: builder class names, parameters named
as the builder XML attributes, `Ident` arguments as `object` references, and the
arguments builder.py derives done in Jinja. So builder2ibek converts a builder XML to
this pattern without redoing builder.py's work.

## Entity models

| Entity model | Loads | Description |
|---|---|---|
| `agilent4UHV.agilent4UHV` | `agilent4UHV.template` | An Agilent 4UHV Ion Pump Controller. `name` is the id its pumps' `CTLR` names. |
| `agilent4UHV.agilent4UHVIonp` | `agilent4UHVIonp.template` | A pump of the controller `CTLR`, whose port it takes. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `agilent4UHV.ibek.support.yaml`
- `agilent4UHV.proto`
- `agilent4UHV.pvi.device.yaml`
- `agilent4UHV.template`
- `agilent4UHVIonp.pvi.device.yaml`
- `agilent4UHVIonp.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
