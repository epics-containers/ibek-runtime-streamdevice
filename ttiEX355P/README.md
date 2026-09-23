# ttiEX355P

Runtime StreamDevice pattern imported from the DLS support module `ttiEX355P`, release
`2-0` (`/dls_sw/prod/R3.14.12.7/support/ttiEX355P/2-0`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ttiEX355P.ibek.support.yaml`](ttiEX355P.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `ttiEX355P.ttiEX355P` | Imported from DLS module ttiEX355P (ttiEX355P.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ttiEX355P.ibek.support.yaml`
- `ttiEX355P.proto`
- `ttiEX355P.template`
- `ttiEX355P_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
