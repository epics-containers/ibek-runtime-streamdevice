# HostLink

Runtime StreamDevice pattern imported from the DLS support module `HostLink`, release
`3-3` (`/dls_sw/prod/R3.14.12.7/support/HostLink/3-3`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`HostLink.ibek.support.yaml`](HostLink.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

The pattern carries both of the release's StreamDevice protocols:

- `HostlinkFINS.proto`, the FINS protocol `HostLink.template` uses.
- `Hostlink.proto`, the C-mode (`RD`/`WD`) protocol. No model here uses it; it is for
  templates in other patterns that talk C-mode HostLink, such as
  `BL05I_waterChiller.template` in the `BL05I` pattern of
  [ibek-runtime-support](https://github.com/epics-containers/ibek-runtime-support).
  An IOC that loads such a template vendors this pattern as well, for the protocol
  file: no `HostLink` entity is needed.

## Entity models

| Entity model | Description |
|---|---|
| `HostLink.HostLink` | HostLink protocols (no records; Hostlink.proto and HostlinkFINS.proto are vendored with the pattern) |
| `HostLink.HostLinkTemplate` | Omron PLC HostLink FINS communications status and clock readbacks |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `HostLink.ibek.support.yaml`
- `HostLink.template`
- `HostLinkTemplate.pvi.device.yaml`
- `Hostlink.proto`
- `HostlinkFINS.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
