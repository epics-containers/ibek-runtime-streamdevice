# norhofLN2

Runtime StreamDevice pattern imported from the DLS support module `norhofLN2`, release
`2-3` (`/dls_sw/prod/R3.14.12.7/support/norhofLN2/2-3`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`norhofLN2.ibek.support.yaml`](norhofLN2.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `norhofLN2.norhofLN2` | Controls a Norhof LN2 Pump |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `norhof.proto`
- `norhofLN2.ibek.support.yaml`
- `norhofLN2.template`
- `norhofLN2_positions.req`
- `norhofLN2_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
