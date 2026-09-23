# VCH10Light

Runtime StreamDevice pattern imported from the DLS support module `VCH10Light`, release
`1-1` (`/dls_sw/prod/R3.14.12.7/support/VCH10Light/1-1`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`VCH10Light.ibek.support.yaml`](VCH10Light.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `VCH10Light.VCH10Light` | Template database for a VCH-10 Light Controller. Typically used on End Stations to illuminate one or more vacuum chambers. All the lights are turned on/off together. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `VCH10Light.ibek.support.yaml`
- `VCH10Light.proto`
- `VCH10Light.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
