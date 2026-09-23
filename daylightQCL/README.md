# daylightQCL

Runtime StreamDevice pattern imported from the DLS support module `daylightQCL`, release
`0-3` (`/dls_sw/prod/R3.14.12.7/support/daylightQCL/0-3`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`daylightQCL.ibek.support.yaml`](daylightQCL.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `daylightQCL.daylightQCL` | Daylight Solutions quantum cascade laser (QCL) controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `daylightQCL.ibek.support.yaml`
- `daylightQCL.proto`
- `daylightQCL.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
