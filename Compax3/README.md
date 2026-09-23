# Compax3

Runtime StreamDevice pattern imported from the DLS support module `Compax3`, release
`0-2` (`/dls_sw/prod/R3.14.12.7/support/Compax3/0-2`). Its files are pristine copies of
that release, apart from the scripted changes its support yaml header lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`Compax3.ibek.support.yaml`](Compax3.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `Compax3.Compax3` | Parker Compax3 motor controller (ASCII serial interface) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `Compax3.ibek.support.yaml`
- `Compax3.template`
- `compax3.protocol`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
