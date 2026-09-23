# axisCameraControl

Runtime StreamDevice pattern imported from the DLS support module `axisCameraControl`,
release `2-4` (`/dls_sw/prod/R3.14.12.7/support/axisCameraControl/2-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`axisCameraControl.ibek.support.yaml`](axisCameraControl.ibek.support.yaml). That
header is vendored with the pattern, so the provenance travels into every IOC instance
that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `axisCameraControl.axisCameraControl` | Control template for an Axis web camera (Pan/Tilt/Zoom control) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `axisCameraControl.ibek.support.yaml`
- `axisCameraControl.template`
- `ptz.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
