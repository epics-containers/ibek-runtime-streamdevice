# agilentTurboPump

Runtime StreamDevice pattern imported from the DLS support module `agilentTurboPump`,
release `2-1` (`/dls_sw/prod/R3.14.12.7/support/agilentTurboPump/2-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`agilentTurboPump.ibek.support.yaml`](agilentTurboPump.ibek.support.yaml). That header
is vendored with the pattern, so the provenance travels into every IOC instance that
uses it.

## Entity models

| Entity model | Description |
|---|---|
| `agilentTurboPump.twisTorr305IC` | Agilent TwisTorr 305 turbo pump with integrated controller (IC) |
| `agilentTurboPump.twisTorr305FS` | Agilent TwisTorr 305 turbo pump with free-standing controller (FS) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `agTurboP.proto`
- `agilentTurboPump.ibek.support.yaml`
- `agilentTwisTorr305-FS.template`
- `agilentTwisTorr305-IC.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
