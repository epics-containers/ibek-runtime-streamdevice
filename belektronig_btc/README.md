# belektronig_btc

Runtime StreamDevice pattern imported from the DLS support module `belektronig_btc`,
release `2-2` (`/dls_sw/prod/R3.14.12.7/support/belektronig_btc/2-2`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`belektronig_btc.ibek.support.yaml`](belektronig_btc.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `belektronig_btc.belektronig_btc` | Belektronig BTC M10 temperature controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `belektronig_btc.ibek.support.yaml`
- `m10.proto`
- `m10.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
