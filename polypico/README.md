# polypico

Runtime StreamDevice pattern imported from the DLS support module `polypico`, release
`1.0` (`/dls_sw/prod/R3.14.12.7/support/polypico/1.0`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`polypico.ibek.support.yaml`](polypico.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `polypico.polypico` | Polypico piezo dispenser StreamDevice control |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `polypico.ibek.support.yaml`
- `polypico.proto`
- `polypico.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
