# caenN1470

Runtime StreamDevice pattern imported from the DLS support module `caenN1470`, release
`1-4` (`/dls_sw/prod/R3.14.12.7/support/caenN1470/1-4`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`caenN1470.ibek.support.yaml`](caenN1470.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

Its entity models mirror the DLS `etc/builder.py`: builder class names, parameters named
as the builder XML attributes, `Ident` arguments as `object` references, and the
arguments builder.py derives done in Jinja. So builder2ibek converts a builder XML to
this pattern without redoing builder.py's work.

## Entity models

| Entity model | Loads | Description |
|---|---|---|
| `caenN1470.caenN1470` | `caenN1470.template`, and `caenN1470chan.template` once for each channel 0 to `NCHANS`-1 | A CAEN N1470 HV power supply, as builder.py's `caenN1470` makes it. `label0`-`label3` labelled the DLS EDM screen; no record uses them. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `caenN1470.ibek.support.yaml`
- `caenN1470.proto`
- `caenN1470.pvi.device.yaml`
- `caenN1470.template`
- `caenN1470_settings.req`
- `caenN1470chan.template`
- `caenN1470chan_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
