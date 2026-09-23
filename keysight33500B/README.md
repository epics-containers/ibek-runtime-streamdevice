# keysight33500B

Runtime StreamDevice pattern imported from the DLS support module `keysight33500B`,
release `1-6` (`/dls_sw/prod/R3.14.12.7/support/keysight33500B/1-6`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`keysight33500B.ibek.support.yaml`](keysight33500B.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `keysight33500B.keysight33500Bchan` | Controls a Keysight 33500B function generator channel |
| `keysight33500B.keysight33500B` | Controls a Keysight 33500B function generator |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `keysight33500B.ibek.support.yaml`
- `keysight33500B.template`
- `keysight33500B_settings.req`
- `keysight33500Bchan.template`
- `keysight33500Bchan_settings.req`
- `ks33500B.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
