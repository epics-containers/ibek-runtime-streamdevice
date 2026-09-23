# millik

Runtime StreamDevice pattern imported from the DLS support module `millik`, release
`1-2` (`/dls_sw/prod/R3.14.12.7/support/millik/1-2`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`millik.ibek.support.yaml`](millik.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `millik.millik` | milliK precision temperature measurement device |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `millik.ibek.support.yaml`
- `millik.proto`
- `millik.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
