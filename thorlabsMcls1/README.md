# thorlabsMcls1

Runtime StreamDevice pattern imported from the DLS support module `thorlabsMcls1`,
release `0-4` (`/dls_sw/prod/R3.14.12.7/support/thorlabsMcls1/0-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`thorlabsMcls1.ibek.support.yaml`](thorlabsMcls1.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `thorlabsMcls1.thorlabsMcls1` | Thorlabs MCLS1 laser source |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `thorlabsMcls1.ibek.support.yaml`
- `thorlabsMcls1.proto`
- `thorlabsMcls1.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (3 files)
