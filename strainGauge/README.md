# strainGauge

Runtime StreamDevice pattern imported from the DLS support module `strainGauge`, release
`2-9` (`/dls_sw/prod/R3.14.12.7/support/strainGauge/2-9`). Its files are pristine copies
of that release, apart from the scripted changes its support yaml header lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`strainGauge.ibek.support.yaml`](strainGauge.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `strainGauge.strainGaugeOmegaPt` | Controls Omega Pt series controllers |
| `strainGauge.strainGauge` | Support for the Newport strain gauge NOTE: needs a generic IOC built with strainGauge (not the plain generic image). |
| `strainGauge.motorInit` | Sets a motor record's position at init |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `motorInit.template`
- `omegaPt.protocol`
- `strainGauge.ibek.support.yaml`
- `strainGauge.protocol`
- `strainGauge.template`
- `strainGaugeOmegaPt.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `strainGauge.template` | compiled aSub routine `parseSetpointValue` |
