# HostLink

Runtime StreamDevice pattern imported from the DLS support module `HostLink`, release
`3-3` (`/dls_sw/prod/R3.14.12.7/support/HostLink/3-3`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`HostLink.ibek.support.yaml`](HostLink.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `HostLink.HostLink` | HostLink FINS protocol module (loads the stream protocol file) |
| `HostLink.HostLinkTemplate` | Omron PLC HostLink FINS communications status and clock readbacks |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `HostLink.ibek.support.yaml`
- `HostLink.template`
- `HostlinkFINS.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
