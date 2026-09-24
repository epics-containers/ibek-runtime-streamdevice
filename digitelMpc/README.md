# digitelMpc

Runtime StreamDevice pattern imported from the DLS support module `digitelMpc`, release
`6-24` (`/dls_sw/prod/R3.14.12.7/support/digitelMpc/6-24`). Its files are pristine
copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`digitelMpc.ibek.support.yaml`](digitelMpc.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `digitelMpc._digitelMpcTemplate` | Template database for digitel MPC - Controller |
| `digitelMpc.digitelMpc` | digitel MPC Controller (multi-drop serial vacuum pump controller). |
| `digitelMpc.digitelMpcTsp` | Template database for digitel MPC - Titanium Sublimation Pump |
| `digitelMpc.digitelMpcqTsp` | Template database for digitel MPCq - Titanium Sublimation Pump |
| `digitelMpc._digitelMpcIonpTemplate` | Template database for digitel MPC - Ion Pump |
| `digitelMpc.digitelMpcIonp` | Template database for digitel MPC - Ion Pump |
| `digitelMpc.digitelMpcIonpGroup` | Template database for a group of up to 8 digitel MPC Ion Pumps |
| `digitelMpc.digitelMpcTspGroup` | Template database for a group of up to 8 digitel MPC TSPs |
| `digitelMpc.dummyIonp` | Template database for dummy Ion Pump. |
| `digitelMpc.digitelMpcIonpSps` | Imported from DLS module digitelMpc (digitelMpcIonpSps.template) |
| `digitelMpc.digitelMpcTspDummy` | Template dummy records for digitel MPC - Titanium Sublimation Pump |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `digitelMpc.ibek.support.yaml`
- `digitelMpc.proto`
- `digitelMpc.template`
- `digitelMpcIonp.template`
- `digitelMpcIonpGroup.template`
- `digitelMpcIonpSps.template`
- `digitelMpcTsp.template`
- `digitelMpcTspDummy.template`
- `digitelMpcTspGroup.template`
- `digitelMpcq.proto`
- `digitelMpcqTsp.template`
- `dummyIonp.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (3 files)
