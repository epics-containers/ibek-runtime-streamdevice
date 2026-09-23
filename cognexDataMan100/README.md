# cognexDataMan100

Runtime StreamDevice pattern imported from the DLS support module `cognexDataMan100`,
release `1-2` (`/dls_sw/prod/R3.14.12.7/support/cognexDataMan100/1-2`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`cognexDataMan100.ibek.support.yaml`](cognexDataMan100.ibek.support.yaml). That header
is vendored with the pattern, so the provenance travels into every IOC instance that
uses it.

## Entity models

| Entity model | Description |
|---|---|
| `cognexDataMan100.dataman100` | Cognex DataMan 100 barcode reader |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `cognexDataMan100.ibek.support.yaml`
- `dataman.proto`
- `dataman100.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
