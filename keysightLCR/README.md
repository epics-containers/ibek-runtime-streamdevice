# keysightLCR

Runtime StreamDevice pattern imported from the DLS support module `keysightLCR`, release
`0-2` (`/dls_sw/prod/R3.14.12.7/support/keysightLCR/0-2`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`keysightLCR.ibek.support.yaml`](keysightLCR.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `keysightLCR.keysightLCR` | Keysight LCR meter |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `keysightLCR.ibek.support.yaml`
- `keysightLCR.proto`
- `keysightLCR.template`
- `keysightLCR_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
