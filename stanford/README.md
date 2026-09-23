# stanford

Runtime StreamDevice pattern imported from the DLS support module `stanford`, release
`2-7` (`/dls_sw/prod/R3.14.12.7/support/stanford/2-7`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`stanford.ibek.support.yaml`](stanford.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `stanford.sr570` | Controls a Stanford SR570 current amplifier |
| `stanford.dummy_stanford_ai` | Imported from DLS module stanford (dummy_stanford_ai.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `dummy_stanford_ai.template`
- `sr570.proto`
- `sr570.template`
- `sr570_settings.req`
- `stanford.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
