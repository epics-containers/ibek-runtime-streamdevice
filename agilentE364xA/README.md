# agilentE364xA

Runtime StreamDevice pattern imported from the DLS support module `agilentE364xA`,
release `1-2-1` (`/dls_sw/prod/R3.14.12.7/support/agilentE364xA/1-2-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`agilentE364xA.ibek.support.yaml`](agilentE364xA.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `agilentE364xA.E364xA` | Agilent E364xA programmable DC power supply |
| `agilentE364xA.caputcallback` | Imported from DLS module agilentE364xA (caputcallback.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `E364xA.proto`
- `E364xA.template`
- `agilentE364xA.ibek.support.yaml`
- `caputcallback.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
