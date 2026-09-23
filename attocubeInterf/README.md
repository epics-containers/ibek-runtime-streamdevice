# attocubeInterf

Runtime StreamDevice pattern imported from the DLS support module `attocubeInterf`,
release `2-1` (`/dls_sw/prod/R3.14.12.7/support/attocubeInterf/2-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`attocubeInterf.ibek.support.yaml`](attocubeInterf.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `attocubeInterf.ids3010` | Controls an attocube ids3010 interferometer |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `attocubeInterf.ibek.support.yaml`
- `ids3010.proto`
- `ids3010.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
