# digitelMpc

Runtime StreamDevice pattern imported from the DLS support module `digitelMpc`, release
`6-24` (`/dls_sw/prod/R3.14.12.7/support/digitelMpc/6-24`). Its files are pristine
copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`digitelMpc.ibek.support.yaml`](digitelMpc.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

The models are ibek-support's `digitelMpc` models, which mirror the DLS `builder.py`:
`digitelMpc` has an id (`name`) and takes its asyn `port` as an object, and
`digitelMpcIonp` takes its controller as `MPC`, from which it reads `port`, `unit` and
`proto`.

| Entity model | Description |
|---|---|
| `digitelMpc.digitelMpc` | digitel MPC controller/head unit |
| `digitelMpc.digitelMpcIonp` | Template database for digitel MPC - Ion Pump, on the controller `MPC` |
| `digitelMpc.digitelMpcTsp` | Template database for digitel MPC - Titanium Sublimation Pump |
| `digitelMpc.digitelMpcqTsp` | Template database for digitel MPCq - Titanium Sublimation Pump |
| `digitelMpc.digitelMpcIonpGroup` | Template database for a group of up to 8 digitel MPC Ion Pumps |
| `digitelMpc.digitelMpcTspGroup` | Template database for a group of up to 8 digitel MPC TSPs |
| `digitelMpc.dummyIonp` | Template database for dummy Ion Pump. |
| `digitelMpc.digitelMpcIonpSps` | Ion pump setpoint records (`digitelMpcIonpSps.template`; no `builder.py` class) |
| `digitelMpc.digitelMpcTspDummy` | Template dummy records for digitel MPC - Titanium Sublimation Pump (no `builder.py` class) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `digitelMpc.ibek.support.yaml`
- `digitelMpc.proto`
- `digitelMpc.pvi.device.yaml`
- `digitelMpc.template`
- `digitelMpcIonp.pvi.device.yaml`
- `digitelMpcIonp.template`
- `digitelMpcIonpGroup.pvi.device.yaml`
- `digitelMpcIonpGroup.template`
- `digitelMpcIonpSps.pvi.device.yaml`
- `digitelMpcIonpSps.template`
- `digitelMpcTsp.pvi.device.yaml`
- `digitelMpcTsp.template`
- `digitelMpcTspDummy.pvi.device.yaml`
- `digitelMpcTspDummy.template`
- `digitelMpcTspGroup.pvi.device.yaml`
- `digitelMpcTspGroup.template`
- `digitelMpcq.proto`
- `digitelMpcqTsp.pvi.device.yaml`
- `digitelMpcqTsp.template`
- `dummyIonp.pvi.device.yaml`
- `dummyIonp.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (3 files)
