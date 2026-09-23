# ip

Runtime StreamDevice pattern imported from the DLS support module `ip`, release `4-5`
(`/dls_sw/prod/R3.14.12.7/support/ip/4-5`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ip.ibek.support.yaml`](ip.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `ip.SR830` | Imported from DLS module ip (SR830.db) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `SR830.db`
- `SR830.proto`
- `ip.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (12 files)
