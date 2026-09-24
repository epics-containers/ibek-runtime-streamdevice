# EdwardsNextTurbo

Runtime StreamDevice pattern imported from the DLS support module `EdwardsNextTurbo`,
release `3-4` (`/dls_sw/prod/R3.14.12.7/support/EdwardsNextTurbo/3-4`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`EdwardsNextTurbo.ibek.support.yaml`](EdwardsNextTurbo.ibek.support.yaml). That header
is vendored with the pattern, so the provenance travels into every IOC instance that
uses it.

## Entity models

| Entity model | Description |
|---|---|
| `EdwardsNextTurbo.EdwardsNextTurbo` | Support for Edwards nEXT series turbo pump controllers, which control Edwards turbo pumps. NOTE: These are interlocked by a PLC, you need another template from a different module for that. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `EdNxtT.proto`
- `EdwardsNextTurbo.ibek.support.yaml`
- `EdwardsNextTurbo.template`
- `EdwardsNextTurbo_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
