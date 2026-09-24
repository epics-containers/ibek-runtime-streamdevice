# dlsCAENels

Runtime StreamDevice pattern imported from the DLS support module `dlsCAENels`, release
`2-6` (`/dls_sw/prod/R3.14.12.7/support/dlsCAENels/2-6`). Its files are pristine copies
of that release, apart from the scripted changes its support yaml header lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`dlsCAENels.ibek.support.yaml`](dlsCAENels.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `dlsCAENels.dlsCAENels` | Instantiates the template for a CAENels high-voltage power supply |
| `dlsCAENels.dlsCAENelsGroup` | Instantiates the template for a group of channels |
| `dlsCAENels.dlsCAENelsChannel` | Instantiates the template for a single channel |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `dlsCAENels.ibek.support.yaml`
- `dlsCAENels.proto`
- `dlsCAENels.template`
- `dlsCAENels_channel.template`
- `dlsCAENels_group.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (3 files)
- `test/` - device tests from the DLS source release (2 files)
