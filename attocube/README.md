# attocube

Runtime StreamDevice pattern imported from the DLS support module `attocube`, release
`1-8` (`/dls_sw/prod/R3.14.12.7/support/attocube/1-8`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`attocube.ibek.support.yaml`](attocube.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `attocube.ANC150` | Controls an attocube ANC150 pico motor controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ANC150.proto`
- `ANC150.template`
- `attocube.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
