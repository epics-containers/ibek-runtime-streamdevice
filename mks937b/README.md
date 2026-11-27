# mks937b

Runtime StreamDevice pattern imported from the DLS support module `mks937b`, release
`2-98` (`/dls_sw/prod/R3.14.12.7/support/mks937b/2-98`). Its files are pristine copies
of that release, except `mks937bImgMean.template`: its aSub record called the module's
only compiled routine, `mks937bMeanCalc`, and is replaced by base calc records that
give the same results. So no template needs the compiled `mks937b` module.

Its entity models are ibek-support's `mks937b` models, which mirror the DLS `builder.py`
(object references such as `GCTLR` and `GAUGE`, with port, address and device derived
in Jinja), so an IOC that builder2ibek converts for the compiled module uses this
pattern unchanged. Their databases load this pattern's templates.

How each file was obtained, and any change made to it, is recorded in the header of
[`mks937b.ibek.support.yaml`](mks937b.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Loads | Description |
|---|---|---|
| `mks937b.mks937b` | `mks937b.template` | An MKS937B Multi-Sensor System (vacuum gauge controller) read over StreamDevice. |
| `mks937b.mks937bCap` | `mks937bCap.template` | A capacitance manometer on the controller `GCTLR`. |
| `mks937b.mks937bFastRelay` | `mks937bFastRelay.template` | The fast relay of the gauge `GAUGE` (an Img, Pirg or `auto_mks937bHcg`). |
| `mks937b.mks937bGauge` | `mks937bGauge.template` | A combination gauge: two channels of an MKS937B, its log pressure from `plog_adc_pv`. |
| `mks937b.mks937bGaugeEGU` | `mks937bPlogEGU.template`, `mks937bGauge.template` | A combination gauge whose pressure comes in mbar from `input`, through `mks937bPlogEGU.template`. |
| `mks937b.mks937bGaugeGroup` | `mks937bGaugeGroup.template` | A group of up to 8 combination gauges. |
| `mks937b.mks937bHy8401` | `mks937bHy8401.template` | A Hytec Hy8401 VME ADC channel feeding a gauge's log pressure. NOTE: needs an image with Hytec Hy8401ip device support (DTYP "Hy8401ip", e.g. an RTEMS/VME IOC), not mks937b. |
| `mks937b.mks937bImg` | `mks937bImg.template` | An inverted magnetron gauge (IMG) on the controller `GCTLR`. |
| `mks937b.mks937bImgDummy` | `mks937bImgDummy.template` | A dummy IMG, enough for a combination gauge. |
| `mks937b.mks937bImgGroup` | `mks937bImgGroup.template` | A group of up to 8 IMGs. |
| `mks937b.mks937bImgMean` | `mks937bImgMean.template` | The mean pressure of up to 10 IMGs. The compiled aSub is replaced by base calc records (see below). |
| `mks937b.mks937bPirg` | `mks937bPirg.template` | A Pirani gauge on the controller `GCTLR`. |
| `mks937b.mks937bPirgDummy` | `mks937bPirgDummy.template` | A dummy Pirani gauge, enough for a combination gauge. |
| `mks937b.mks937bPirgGroup` | `mks937bPirgGroup.template` | A group of up to 8 Pirani gauges. |
| `mks937b.mks937bRelays` | `mks937bRelays.template` | A setpoint relay of the gauge `GAUGE` (an Img, Pirg or `auto_mks937bHcg`), numbered in order per gauge. |
| `mks937b.auto_mks937bHcg` | `mks937bHcg.template` | A hot cathode gauge (HCG), with the controller's `port` and `address` given directly; a `GAUGE` for relays. Not in ibek-support. |
| `mks937b.auto_mks937bHcgGroup` | `mks937bHcgGroup.template` | A group of up to 8 HCGs. Not in ibek-support. |
| `mks937b.auto_mks937bInterlock` | `mks937bInterlock.template` | Overrides gauge interlock values, after the gauge templates load them. Not in ibek-support. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `auto_mks937bHcg.pvi.device.yaml`
- `auto_mks937bHcgGroup.pvi.device.yaml`
- `auto_mks937bInterlock.pvi.device.yaml`
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
- `mks937bGaugeEGU.pvi.device.yaml`
- `mks937bGaugeGroup.pvi.device.yaml`
- `mks937bGaugeGroup.template`
- `mks937bGauge_positions.req`
- `mks937bHcg.template`
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
- `mks937bInterlock.template`
- `mks937bPirg.pvi.device.yaml`
- `mks937bPirg.template`
- `mks937bPirgDummy.pvi.device.yaml`
- `mks937bPirgDummy.template`
- `mks937bPirgGroup.pvi.device.yaml`
- `mks937bPirgGroup.template`
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
