# watson-marlow

Runtime StreamDevice pattern imported from the DLS support module `watson-marlow`,
release `1-5` (`/dls_sw/prod/R3.14.12.7/support/watson-marlow/1-5`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`watson-marlow.ibek.support.yaml`](watson-marlow.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `watson-marlow.Pump323Du` | Controls a Watson Marlow 323Du Pump |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `323Du.proto`
- `323Du.template`
- `watson-marlow.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
