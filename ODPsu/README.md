# ODPsu

Runtime StreamDevice pattern imported from the DLS support module `ODPsu`, release `3-2`
(`/dls_sw/prod/R3.14.12.7/support/ODPsu/3-2`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ODPsu.ibek.support.yaml`](ODPsu.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `ODPsu.ODPsu` | ODPsu power supply control |
| `ODPsu.ODPsuV2` | ODPsu V2 power supply control |
| `ODPsu.ODPsuChannel` | ODPsu power supply channel control |
| `ODPsu.ODPsuChannelV2` | ODPsu V2 power supply channel control |
| `ODPsu.ODPsuBank` | ODPsu power supply bank control |
| `ODPsu.ODPsuBankV2` | ODPsu V2 power supply bank control |
| `ODPsu.ODPsuFormat16` | ODPsu 16-channel format control |
| `ODPsu.ODPsuFormat22` | ODPsu 22-channel format control |
| `ODPsu.ODPsugda` | ODPsu GDA-tagged channel-count summary records, configurable channel count |
| `ODPsu.ODPsugdaV2` | ODPsu V2 GDA-tagged channel-count summary records, configurable channel count |
| `ODPsu.ODPsugda24` | ODPsu GDA-tagged channel-count summary records for a 24-channel PSU |
| `ODPsu.ODPsugda16` | ODPsu GDA-tagged channel-count summary records for a 16-channel PSU |
| `ODPsu.ODPsugda14` | ODPsu GDA-tagged channel-count summary records for a 14-channel PSU |
| `ODPsu.ODPsugda12` | ODPsu GDA-tagged channel-count summary records for a 12-channel PSU |
| `ODPsu.ODPsugda8` | ODPsu GDA-tagged channel-count summary records for an 8-channel PSU |
| `ODPsu.ODPsugda7` | ODPsu GDA-tagged channel-count summary records for a 7-channel PSU |
| `ODPsu.ODPsugda24V2` | ODPsu V2 GDA-tagged channel-count summary records for a 24-channel PSU |
| `ODPsu.ODPsugda16V2` | ODPsu V2 GDA-tagged channel-count summary records for a 16-channel PSU |
| `ODPsu.ODPsugda14V2` | ODPsu V2 GDA-tagged channel-count summary records for a 14-channel PSU |
| `ODPsu.ODPsugda12V2` | ODPsu V2 GDA-tagged channel-count summary records for a 12-channel PSU |
| `ODPsu.ODPsugda8V2` | ODPsu V2 GDA-tagged channel-count summary records for an 8-channel PSU |
| `ODPsu.ODPsugda7V2` | ODPsu V2 GDA-tagged channel-count summary records for a 7-channel PSU |
| `ODPsu.ODPsu16DUpdate` | ODPsu 16-channel display-format update records |
| `ODPsu.ODPsu22DUpdate` | ODPsu 22-channel display-format update records |
| `ODPsu.ODPsu24DUpdate` | ODPsu 24-channel display-format update records |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ODPsu.ibek.support.yaml`
- `ODPsu.protocol`
- `ODPsu.template`
- `ODPsu16DUpdate.template`
- `ODPsu22DUpdate.template`
- `ODPsu24DUpdate.template`
- `ODPsuBank.template`
- `ODPsuBankV2.template`
- `ODPsuChannel.template`
- `ODPsuChannelV2.template`
- `ODPsuFormat16.template`
- `ODPsuFormat22.template`
- `ODPsuV2.protocol`
- `ODPsuV2.template`
- `ODPsuV2_settings.req`
- `ODPsugda.template`
- `ODPsugda12.template`
- `ODPsugda12V2.template`
- `ODPsugda14.template`
- `ODPsugda14V2.template`
- `ODPsugda16.template`
- `ODPsugda16V2.template`
- `ODPsugda24.template`
- `ODPsugda24V2.template`
- `ODPsugda7.template`
- `ODPsugda7V2.template`
- `ODPsugda8.template`
- `ODPsugda8V2.template`
- `ODPsugdaV2.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
