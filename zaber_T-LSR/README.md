# zaber_T-LSR

Runtime StreamDevice pattern imported from the DLS support module `zaber_T-LSR`, release
`2-0` (`/dls_sw/prod/R3.14.12.7/support/zaber_T-LSR/2-0`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`zaber_T-LSR.ibek.support.yaml`](zaber_T-LSR.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `zaber_T-LSR.Zaber_T_LSR` | Zaber T-LSR linear stage controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `zaber_T-LSR.ibek.support.yaml`
- `zaber_T-LSR.proto`
- `zaber_T-LSR.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
