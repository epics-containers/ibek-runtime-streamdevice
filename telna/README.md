# telna

Runtime StreamDevice pattern imported from the DLS support module `telna`, release `1-3`
(`/dls_sw/prod/R3.14.12.7/support/telna/1-3`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`telna.ibek.support.yaml`](telna.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `telna.telna` | Reads out the 8 channel Telna temperature logger |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `telna.ibek.support.yaml`
- `telna.proto`
- `telna.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
