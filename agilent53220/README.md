# agilent53220

Runtime StreamDevice pattern imported from the DLS support module `agilent53220`,
release `1-3-4` (`/dls_sw/prod/R3.14.12.7/support/agilent53220/1-3-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`agilent53220.ibek.support.yaml`](agilent53220.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `agilent53220.agilent53220` | Agilent 53220 frequency analyser |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `agilent53220.ibek.support.yaml`
- `agilent53220.proto`
- `agilent53220.template`
- `agilent53220_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
