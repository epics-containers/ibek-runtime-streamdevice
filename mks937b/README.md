# mks937b

Runtime StreamDevice pattern imported from the DLS support module `mks937b`, release
`2-98` (`/dls_sw/prod/R3.14.12.7/support/mks937b/2-98`). Its files are pristine copies
of that release, except `mks937bImgMean.template`: its aSub record called the module's
only compiled routine, `mks937bMeanCalc`, and is replaced by base calc records that
give the same results. So no template needs the compiled `mks937b` module.

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
| `mks937b.mks937bHy8401` | Imported from DLS module mks937b (mks937bHy8401.template) NOTE: needs an image with Hytec Hy8401ip device support (DTYP "Hy8401ip", e.g. an RTEMS/VME IOC), not mks937b. |
| `mks937b.mks937bImg` | Imported from DLS module mks937b (mks937bImg.template) |
| `mks937b.mks937bImgDummy` | Imported from DLS module mks937b (mks937bImgDummy.template) |
| `mks937b.mks937bImgGroup` | Imported from DLS module mks937b (mks937bImgGroup.template) |
| `mks937b.mks937bImgMean` | Derived from DLS module mks937b (mks937bImgMean.template): the compiled aSub is replaced by base calc records. |
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
- `mks937b.pvi.device.yaml`
- `mks937b.template`
- `mks937bCap.pvi.device.yaml`
- `mks937bCap.template`
- `mks937bFastRelay.pvi.device.yaml`
- `mks937bFastRelay.template`
- `mks937bGauge.pvi.device.yaml`
- `mks937bGauge.template`
- `mks937bGaugeGroup.pvi.device.yaml`
- `mks937bGaugeGroup.template`
- `mks937bGauge_positions.req`
- `mks937bHcg.pvi.device.yaml`
- `mks937bHcg.template`
- `mks937bHcgGroup.pvi.device.yaml`
- `mks937bHcgGroup.template`
- `mks937bHy8401.pvi.device.yaml`
- `mks937bHy8401.template`
- `mks937bImg.pvi.device.yaml`
- `mks937bImg.template`
- `mks937bImgDummy.pvi.device.yaml`
- `mks937bImgDummy.template`
- `mks937bImgGroup.pvi.device.yaml`
- `mks937bImgGroup.template`
- `mks937bImgMean.pvi.device.yaml`
- `mks937bImgMean.template`
- `mks937bInterlock.pvi.device.yaml`
- `mks937bInterlock.template`
- `mks937bPirg.pvi.device.yaml`
- `mks937bPirg.template`
- `mks937bPirgDummy.pvi.device.yaml`
- `mks937bPirgDummy.template`
- `mks937bPirgGroup.pvi.device.yaml`
- `mks937bPirgGroup.template`
- `mks937bPlogEGU.pvi.device.yaml`
- `mks937bPlogEGU.template`
- `mks937bRelays.pvi.device.yaml`
- `mks937bRelays.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (3 files)
- `sim/` - device simulator from the DLS source release (2 files)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

This template loads only in an image with the device support it needs; the
others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `mks937bHy8401.template` | `DTYP "Hy8401ip"`: Hytec IP ADC device support, as in an RTEMS/VME IOC; not `mks937b` |

## `mks937bImgMean.template`

The DLS template's aSub `$(device):MEAN` called `mks937bMeanCalc`. Here `MEAN` is a
fanout on the same scan that drives base `calc`/`calcout` records: they find the good
gauges, then write `:STA`, `:P`, `:PMAX` and `:PMIN` every scan, as the aSub did. The
results match `mks937bMeanCalc` exactly, including a bit-identical mean. Archived
`MEAN` remains; its value is 0, as the aSub's was. The aSub's `VALA`-`VALD` fields
are gone.
