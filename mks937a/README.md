# mks937a

Runtime StreamDevice pattern imported from the DLS support module `mks937a`, release
`2-97` (`/dls_sw/prod/R3.14.12.7/support/mks937a/2-97`). Its files are pristine copies
of that release, except `mks937aImgMean.template`: its aSub record called the module's
only compiled routine, `mks937aMeanCalc`, and is replaced by base calc records that
give the same results. So no template needs the compiled `mks937a` module.

Its entity models are ibek-support's `mks937a` models, which mirror the DLS `builder.py`
(object references such as `GCTLR` and `GAUGE`, with port, address and device derived
in Jinja), so an IOC that builder2ibek converts for the compiled module uses this
pattern unchanged. Their databases load this pattern's templates.

How each file was obtained, and any change made to it, is recorded in the header of
[`mks937a.ibek.support.yaml`](mks937a.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Loads | Description |
|---|---|---|
| `mks937a.mks937a` | `mks937a.template` | An MKS937A Multi-Sensor System (vacuum gauge controller) read over StreamDevice. |
| `mks937a.mks937aGauge` | `mks937aGauge.template` | A combination gauge: two channels of an MKS937A. NOTE: the default aitype needs an image with Hytec Hy8401ip device support (DTYP "Hy8401ip", e.g. an RTEMS/VME IOC), not mks937a; with aitype "Soft Channel" and aiinp it runs in the generic image, as mks937aGaugeEGU does. |
| `mks937a.mks937aGaugeEGU` | `mks937aGauge.template`, `mks937aPlogEGU.template` | A combination gauge whose pressure comes in mbar from `input`, through `mks937aPlogEGU.template`. |
| `mks937a.mks937aGaugeGroup` | `mks937aGaugeGroup.template` | A group of up to 8 combination gauges. |
| `mks937a.mks937aImg` | `mks937aImg.template` | An inverted magnetron gauge (IMG) on the controller `GCTLR`. |
| `mks937a.mks937aImgDummy` | `mks937aImgDummy.template` | A dummy IMG, enough for a combination gauge. |
| `mks937a.mks937aImgGroup` | `mks937aImgGroup.template` | A group of up to 8 IMGs. |
| `mks937a.mks937aImgMean` | `mks937aImgMean.template` | The mean pressure of up to 10 IMGs. The compiled aSub is replaced by base calc records (see below). |
| `mks937a.mks937aPirg` | `mks937aPirg.template` | A Pirani gauge on the controller `GCTLR`. |
| `mks937a.mks937aPirgDummy` | `mks937aPirgDummy.template` | A dummy Pirani gauge, enough for a combination gauge. |
| `mks937a.mks937aPirgGroup` | `mks937aPirgGroup.template` | A group of up to 8 Pirani gauges. |
| `mks937a.auto_mks937aInterlock` | `mks937aInterlock.template` | Overrides gauge interlock values, after the gauge templates load them. |
| `mks937a.auto_mks937aPlogADC` | `mks937aPlogADC.template` | A virtual calibrated ADC, scaling a raw 0..32767 ADC PV for :PLOG. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `auto_mks937aInterlock.pvi.device.yaml`
- `auto_mks937aPlogADC.pvi.device.yaml`
- `mks937a.ibek.support.yaml`
- `mks937a.protocol`
- `mks937a.pvi.device.yaml`
- `mks937a.template`
- `mks937aGauge.pvi.device.yaml`
- `mks937aGauge.template`
- `mks937aGaugeEGU.pvi.device.yaml`
- `mks937aGaugeGroup.pvi.device.yaml`
- `mks937aGaugeGroup.template`
- `mks937aGauge_positions.req`
- `mks937aImg.pvi.device.yaml`
- `mks937aImg.template`
- `mks937aImgDummy.pvi.device.yaml`
- `mks937aImgDummy.template`
- `mks937aImgGroup.pvi.device.yaml`
- `mks937aImgGroup.template`
- `mks937aImgMean.pvi.device.yaml`
- `mks937aImgMean.template`
- `mks937aInterlock.template`
- `mks937aPirg.pvi.device.yaml`
- `mks937aPirg.template`
- `mks937aPirgDummy.pvi.device.yaml`
- `mks937aPirgDummy.template`
- `mks937aPirgGroup.pvi.device.yaml`
- `mks937aPirgGroup.template`
- `mks937aPlogADC.template`
- `mks937aPlogEGU.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (3 files)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

This template loads with its default `aitype` only in an image with the device
support it needs; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `mks937aGauge.template` | `DTYP "$(aitype=Hy8401ip)"`: Hytec IP ADC device support, as in an RTEMS/VME IOC; not `mks937a`. With `aitype` `Soft Channel` and `aiinp` it runs in the generic image |

## `mks937aImgMean.template`

The DLS template's aSub `$(device):MEAN` called `mks937aMeanCalc`. Here `MEAN` is a
fanout on the same scan that drives base `calc`/`calcout` records: they find the good
gauges, then write `:STA`, `:P`, `:PMAX` and `:PMIN` every scan. The results match
`mks937aMeanCalc` exactly, including a bit-identical mean. In 2-97 the aSub wrote
them only when no gauge was good, because `mks937aMeanCalc` returns the number of
good gauges and the aSub record takes a non-zero return as failure; this follows
`mks937b`, whose routine returns 0. Archived `MEAN` remains, with value 0 (2-97's
was the number of good gauges). The aSub's `VALA`-`VALD` fields are gone.

One difference from the aSub: if a gauge's input link fails (for example a
disconnected PV from another IOC), the aSub froze all four outputs, while here only
that gauge's `MEAN:G<n>` keeps its last value and the outputs carry on updating.
