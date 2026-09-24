# chillax

Runtime StreamDevice pattern imported from the DLS support module `chillax`, release
`2-3-1` (`/dls_sw/prod/R3.14.12.7/support/chillax/2-3-1`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`chillax.ibek.support.yaml`](chillax.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `chillax._chillaxOpiTemplate` | Chillax cryocooler CSS screen association template |
| `chillax._chillaxSubstituionsTemplate` | Chillax cryocooler records template |
| `chillax.chillaxController` | Chillax cryocooler controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `chillax.ibek.support.yaml`
- `chillax.proto`
- `chillax_abs.db`
- `chillax_opi.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
