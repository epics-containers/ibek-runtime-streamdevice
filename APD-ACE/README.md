# APD-ACE

Runtime StreamDevice pattern imported from the DLS support module `APD-ACE`, release
`2-3` (`/dls_sw/prod/R3.14.12.7/support/APD-ACE/2-3`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`APD-ACE.ibek.support.yaml`](APD-ACE.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `APD-ACE.APDACE` | APD ACE avalanche photodiode bias/control unit |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `APD-ACE.ibek.support.yaml`
- `ace.proto`
- `apd-ace.template`
- `apd-ace_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file

## Upstream defects carried as-is

- `ERRORSTATUS` has a stream INP but a bare `SIOL "@"` (`apd-ace.template:281`)
