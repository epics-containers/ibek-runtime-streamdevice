# mks937b

Runtime StreamDevice pattern imported from the DLS support module `mks937b`, release
`2-98` (`/dls_sw/prod/R3.14.12.7/support/mks937b/2-98`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`mks937b.ibek.support.yaml`](mks937b.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `mks937b.mks937b` | Template database for an MKS937B Multi-Sensor System (vacuum gauge controller) read over StreamDevice. |
| `mks937b.mks937bCap` | Imported from DLS module mks937b (mks937bCap.template) |
| `mks937b.mks937bFastRelay` | Imported from DLS module mks937b (mks937bFastRelay.template) |
| `mks937b.mks937bGauge` | Imported from DLS module mks937b (mks937bGauge.template) |
| `mks937b.mks937bGaugeGroup` | Imported from DLS module mks937b (mks937bGaugeGroup.template) |
| `mks937b.mks937bHcg` | Imported from DLS module mks937b (mks937bHcg.template) |
| `mks937b.mks937bHcgGroup` | Imported from DLS module mks937b (mks937bHcgGroup.template) |
| `mks937b.mks937bHy8401` | Imported from DLS module mks937b (mks937bHy8401.template) NOTE: needs a generic IOC built with mks937b (not the plain generic image). |
| `mks937b.mks937bImg` | Imported from DLS module mks937b (mks937bImg.template) |
| `mks937b.mks937bImgDummy` | Imported from DLS module mks937b (mks937bImgDummy.template) |
| `mks937b.mks937bImgGroup` | Imported from DLS module mks937b (mks937bImgGroup.template) |
| `mks937b.mks937bImgMean` | Imported from DLS module mks937b (mks937bImgMean.template) NOTE: needs a generic IOC built with mks937b (not the plain generic image). |
| `mks937b.mks937bInterlock` | Imported from DLS module mks937b (mks937bInterlock.template) |
| `mks937b.mks937bPirg` | Imported from DLS module mks937b (mks937bPirg.template) |
| `mks937b.mks937bPirgDummy` | Imported from DLS module mks937b (mks937bPirgDummy.template) |
| `mks937b.mks937bPirgGroup` | Imported from DLS module mks937b (mks937bPirgGroup.template) |
| `mks937b.mks937bPlogEGU` | Imported from DLS module mks937b (mks937bPlogEGU.template) |
| `mks937b.mks937bRelays` | Imported from DLS module mks937b (mks937bRelays.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `mks937b.ibek.support.yaml`
- `mks937b.protocol`
- `mks937b.template`
- `mks937bCap.template`
- `mks937bFastRelay.template`
- `mks937bGauge.template`
- `mks937bGaugeGroup.template`
- `mks937bGauge_positions.req`
- `mks937bHcg.template`
- `mks937bHcgGroup.template`
- `mks937bHy8401.template`
- `mks937bImg.template`
- `mks937bImgDummy.template`
- `mks937bImgGroup.template`
- `mks937bImgMean.template`
- `mks937bInterlock.template`
- `mks937bPirg.template`
- `mks937bPirgDummy.template`
- `mks937bPirgGroup.template`
- `mks937bPlogEGU.template`
- `mks937bRelays.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (3 files)
- `sim/` - device simulator from the DLS source release (2 files)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[BUILD-TIME-ONLY.md](../BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `mks937bHy8401.template`, `mks937bImgMean.template` | `DTYP "Hy8401ip"`; compiled aSub routines `mks937bMeanInit`, `mks937bMeanCalc` |
