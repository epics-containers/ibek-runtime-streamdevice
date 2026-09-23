# agilent33220A

Runtime StreamDevice pattern imported from the DLS support module `agilent33220A`,
release `1-7` (`/dls_sw/prod/R3.14.12.7/support/agilent33220A/1-7`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`agilent33220A.ibek.support.yaml`](agilent33220A.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `agilent33220A.agilent33220A` | Agilent 33220A function/arbitrary waveform generator |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `agilent33220A.ibek.support.yaml`
- `agilent33220A.proto`
- `agilent33220A.template`
- `agilent33220A_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (1 file)
