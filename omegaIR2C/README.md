# omegaIR2C

Runtime StreamDevice pattern imported from the DLS support module `omegaIR2C`, release
`1-5` (`/dls_sw/prod/R3.14.12.7/support/omegaIR2C/1-5`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`omegaIR2C.ibek.support.yaml`](omegaIR2C.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `omegaIR2C.omegaIR2C` | Controls an Omega iR2C Pyrometer |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `iR2C.proto`
- `omegaIR2C.ibek.support.yaml`
- `omegaIR2C.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
