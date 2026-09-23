# opSens

Runtime StreamDevice pattern imported from the DLS support module `opSens`, release
`1-1` (`/dls_sw/prod/R3.14.12.7/support/opSens/1-1`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`opSens.ibek.support.yaml`](opSens.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `opSens.opSens` | Controls opSens Optical Temperature sensor |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `opSens.ibek.support.yaml`
- `opSens.template`
- `opSensTempSens.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
