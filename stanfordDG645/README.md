# stanfordDG645

Runtime StreamDevice pattern imported from the DLS support module `stanfordDG645`,
release `1-3` (`/dls_sw/prod/R3.14.12.7/support/stanfordDG645/1-3`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`stanfordDG645.ibek.support.yaml`](stanfordDG645.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `stanfordDG645.stanfordDG645` | Support for Stanford DG645 digital delay generator |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `stanfordDG645.ibek.support.yaml`
- `stanfordDG645.proto`
- `stanfordDG645.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (1 file)
