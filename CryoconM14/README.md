# CryoconM14

Runtime StreamDevice pattern imported from the DLS support module `CryoconM14`, release
`2-2` (`/dls_sw/prod/R3.14.12.7/support/CryoconM14/2-2`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`CryoconM14.ibek.support.yaml`](CryoconM14.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `CryoconM14.M14_system` | System wide features of the Cryocon M14 Temperature Monitor |
| `CryoconM14.M14_sensor` | Cryocon M14 Temperature Monitor individual sensor details. There are 4 channels. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `CryoconM14.ibek.support.yaml`
- `M14.protocol`
- `M14_sensor.template`
- `M14_system.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
