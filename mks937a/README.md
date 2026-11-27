# mks937a

Runtime StreamDevice pattern imported from the DLS support module `mks937a`, release
`2-97` (`/dls_sw/prod/R3.14.12.7/support/mks937a/2-97`). Its files are pristine copies
of that release, except `mks937aImgMean.template`: its aSub record called the module's
only compiled routine, `mks937aMeanCalc`, and is replaced by base calc records that
give the same results. So no template needs the compiled `mks937a` module.

How each file was obtained, and any change made to it, is recorded in the header of
[`mks937a.ibek.support.yaml`](mks937a.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `mks937a.mks937a` | Template database for an MKS937A Multi-Sensor System (vacuum gauge controller) read over StreamDevice. |
| `mks937a.mks937aGauge` | Imported from DLS module mks937a (mks937aGauge.template) NOTE: the default aitype needs an image with Hytec Hy8401ip device support (DTYP "Hy8401ip", e.g. an RTEMS/VME IOC), not mks937a; with aitype "Soft Channel" and aiinp it runs in the generic image. |
| `mks937a.mks937aGaugeGroup` | Imported from DLS module mks937a (mks937aGaugeGroup.template) |
| `mks937a.mks937aImg` | Imported from DLS module mks937a (mks937aImg.template) |
| `mks937a.mks937aImgDummy` | Imported from DLS module mks937a (mks937aImgDummy.template) |
| `mks937a.mks937aImgGroup` | Imported from DLS module mks937a (mks937aImgGroup.template) |
| `mks937a.mks937aImgMean` | Derived from DLS module mks937a (mks937aImgMean.template): the compiled aSub is replaced by base calc records. |
| `mks937a.mks937aInterlock` | Imported from DLS module mks937a (mks937aInterlock.template) |
| `mks937a.mks937aPirg` | Imported from DLS module mks937a (mks937aPirg.template) |
| `mks937a.mks937aPirgDummy` | Imported from DLS module mks937a (mks937aPirgDummy.template) |
| `mks937a.mks937aPirgGroup` | Imported from DLS module mks937a (mks937aPirgGroup.template) |
| `mks937a.mks937aPlogADC` | Imported from DLS module mks937a (mks937aPlogADC.template) |
| `mks937a.mks937aPlogEGU` | Imported from DLS module mks937a (mks937aPlogEGU.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `mks937a.ibek.support.yaml`
- `mks937a.protocol`
- `mks937a.pvi.device.yaml`
- `mks937a.template`
- `mks937aGauge.pvi.device.yaml`
- `mks937aGauge.template`
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
- `mks937aInterlock.pvi.device.yaml`
- `mks937aInterlock.template`
- `mks937aPirg.pvi.device.yaml`
- `mks937aPirg.template`
- `mks937aPirgDummy.pvi.device.yaml`
- `mks937aPirgDummy.template`
- `mks937aPirgGroup.pvi.device.yaml`
- `mks937aPirgGroup.template`
- `mks937aPlogADC.pvi.device.yaml`
- `mks937aPlogADC.template`
- `mks937aPlogEGU.pvi.device.yaml`
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
