# knauer

Runtime StreamDevice pattern imported from the DLS support module `knauer`, release
`0-6` (`/dls_sw/prod/R3.14.12.7/support/knauer/0-6`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`knauer.ibek.support.yaml`](knauer.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `knauer.BlueShadow40P` | Controls a Knauer BlueShadow 40P HPLC pump |
| `knauer.Azura21S` | Controls a Knauer Azuar V2.1S valve drive |
| `knauer.ConnectionManagement` | Monitors a connection to a Knauer device |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `azuraV2-1S.proto`
- `azuraV2-1S.template`
- `blueShadow40P.proto`
- `blueShadow40P.template`
- `connectionManagement.template`
- `knauer.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (2 files)
