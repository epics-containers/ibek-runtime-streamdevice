# kriIonBeam

Runtime StreamDevice pattern imported from the DLS support module `kriIonBeam`, release
`3-1` (`/dls_sw/prod/R3.14.12.7/support/kriIonBeam/3-1`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`kriIonBeam.ibek.support.yaml`](kriIonBeam.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `kriIonBeam.Autocontroller` | Top-level template for the Kaufman & Robinson ion beam auto controller. Assumed to be using streamDevice. |
| `kriIonBeam.KaufmanSourceController` | Top-level template for the Kaufman & Robinson ion beam KSC. Assumed to be using streamDevice. |
| `kriIonBeam.ProgramParameters` | Program template for the Kaufman & Robinson ion beam auto controller. Assumed to be using streamDevice. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `autocontroller.template`
- `kaufmanSourceController.template`
- `kriIonBeam.ibek.support.yaml`
- `kriIonBeam.proto`
- `programParameters.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
