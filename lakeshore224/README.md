# lakeshore224

Runtime StreamDevice pattern imported from the DLS support module `lakeshore224`,
release `0-6` (`/dls_sw/prod/R3.14.12.7/support/lakeshore224/0-6`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`lakeshore224.ibek.support.yaml`](lakeshore224.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `lakeshore224.lakeshore224` | Lakeshore 224 Temperature Monitor Notes: The loop dependant PVs are in a seperate template file, included in this one. |
| `lakeshore224.lakeshore224_input_dls` | Template to provide the records required for a Lakeshore 224 input. This makes use of the macros required by lakeshore224.template but also requires macros to specify the input channel and index. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `lakeshore224.ibek.support.yaml`
- `lakeshore224.proto`
- `lakeshore224.template`
- `lakeshore224_input_dls.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
