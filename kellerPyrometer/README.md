# kellerPyrometer

Runtime StreamDevice pattern imported from the DLS support module `kellerPyrometer`,
release `0-1` (`/dls_sw/prod/R3.14.12.7/support/kellerPyrometer/0-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`kellerPyrometer.ibek.support.yaml`](kellerPyrometer.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `kellerPyrometer.kellerPyrometer` | Keller Pyrometer |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `kellerPyrometer.ibek.support.yaml`
- `kellerPyrometer.proto`
- `kellerPyrometer.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
