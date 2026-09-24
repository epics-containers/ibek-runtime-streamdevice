# caenN1470

Runtime StreamDevice pattern imported from the DLS support module `caenN1470`, release
`1-4` (`/dls_sw/prod/R3.14.12.7/support/caenN1470/1-4`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`caenN1470.ibek.support.yaml`](caenN1470.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `caenN1470._caenN1470chan` | CAEN N1470 HV power supply (per-channel template) |
| `caenN1470._caenN1470` | CAEN N1470 HV power supply (board-level template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `caenN1470.ibek.support.yaml`
- `caenN1470.proto`
- `caenN1470.template`
- `caenN1470_settings.req`
- `caenN1470chan.template`
- `caenN1470chan_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
