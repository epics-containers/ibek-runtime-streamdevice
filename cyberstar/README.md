# cyberstar

Runtime StreamDevice pattern imported from the DLS support module `cyberstar`, release
`2-3-1` (`/dls_sw/prod/R3.14.12.7/support/cyberstar/2-3-1`). Its files are pristine
copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`cyberstar.ibek.support.yaml`](cyberstar.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `cyberstar.CBY_2206` | Cyberstar CBY-2206 scintillation detector amplifier/discriminator |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `CBY-2206.proto`
- `CBY-2206.template`
- `cyberstar.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
