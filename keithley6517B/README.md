# keithley6517B

Runtime StreamDevice pattern imported from the DLS support module `keithley6517B`,
release `1-2` (`/dls_sw/prod/R3.14.12.7/support/keithley6517B/1-2`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`keithley6517B.ibek.support.yaml`](keithley6517B.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `keithley6517B.keithley6517B` | Keithley 6517B Electrometer |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `keithley6517B.ibek.support.yaml`
- `keithley6517B.proto`
- `keithley6517B.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
