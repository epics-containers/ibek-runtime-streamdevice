# gssExplorIR

Runtime StreamDevice pattern imported from the DLS support module `gssExplorIR`, release
`1-2` (`/dls_sw/prod/R3.14.12.7/support/gssExplorIR/1-2`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`gssExplorIR.ibek.support.yaml`](gssExplorIR.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `gssExplorIR.explorir` | GSS ExplorIR-M-100 CO2 Sensor |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `explorir.proto`
- `explorir.template`
- `gssExplorIR.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
