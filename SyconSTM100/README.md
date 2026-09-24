# SyconSTM100

Runtime StreamDevice pattern imported from the DLS support module `SyconSTM100`, release
`0-2` (`/dls_sw/prod/R3.14.12.7/support/SyconSTM100/0-2`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`SyconSTM100.ibek.support.yaml`](SyconSTM100.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `SyconSTM100.SyconSTM100` | Sycon STM-100 thin film deposition monitor |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `SyconSTM100.ibek.support.yaml`
- `SyconSTM100.proto`
- `SyconSTM100.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
