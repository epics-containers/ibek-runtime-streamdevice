# thermocube

Runtime StreamDevice pattern imported from the DLS support module `thermocube`, release
`1-0` (`/dls_sw/prod/R3.14.12.7/support/thermocube/1-0`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`thermocube.ibek.support.yaml`](thermocube.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `thermocube.thermoCube` | ThermoCube chiller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `thermocube.ibek.support.yaml`
- `thermocube.proto`
- `thermocube.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
