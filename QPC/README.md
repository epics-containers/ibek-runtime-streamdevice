# QPC

Runtime StreamDevice pattern imported from the DLS support module `QPC`, release `2-3`
(`/dls_sw/prod/R3.14.12.7/support/QPC/2-3`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`QPC.ibek.support.yaml`](QPC.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

Its entity models mirror the DLS `etc/builder.py`: builder class names, parameters named
as the builder XML attributes, `Ident` arguments as `object` references, and the
arguments builder.py derives done in Jinja. So builder2ibek converts a builder XML to
this pattern without redoing builder.py's work.

## Entity models

| Entity model | Loads | Description |
|---|---|---|
| `QPC.digitelQpc` | `digitelQPCController.template` | A Digitel QPC ion pump controller. `name` is the id its ion pumps' `QPC` names; `unit` is rendered as 2 upper-case hex digits, as builder.py does. |
| `QPC.digitelQpcIonp` | `digitelQpcIonp.template` | An ion pump on the controller `QPC`, whose port and unit it takes. `SPLY`/`SPT` are rendered `%02d` and `spon`/`spoff` `%1.2G`, as builder.py does. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `QPC.ibek.support.yaml`
- `digitelQPCController.template`
- `digitelQpc.proto`
- `digitelQpc.pvi.device.yaml`
- `digitelQpcIonp.pvi.device.yaml`
- `digitelQpcIonp.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (1 file)
