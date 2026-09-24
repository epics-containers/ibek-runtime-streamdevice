# keithley6514

Runtime StreamDevice pattern imported from the DLS support module `keithley6514`,
release `0-4` (`/dls_sw/prod/R3.14.12.7/support/keithley6514/0-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`keithley6514.ibek.support.yaml`](keithley6514.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `keithley6514.keithley6514` | Keithley 6514 System Electrometer |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `keithley6514.ibek.support.yaml`
- `keithley6514.proto`
- `keithley6514.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
