# keithley2600

Runtime StreamDevice pattern imported from the DLS support module `keithley2600`,
release `2-3` (`/dls_sw/prod/R3.14.12.7/support/keithley2600/2-3`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`keithley2600.ibek.support.yaml`](keithley2600.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `keithley2600.keithley2600chan` | Controls a Keithley 2600 source meter channel |
| `keithley2600.keithley2600` | Controls a Keithley 2600 source meter |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `keithley2600.ibek.support.yaml`
- `keithley2600.proto`
- `keithley2600.template`
- `keithley2600chan.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
