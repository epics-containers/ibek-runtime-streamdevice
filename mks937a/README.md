# mks937a

Runtime StreamDevice pattern imported from the DLS support module `mks937a`, release
`2-97` (`/dls_sw/prod/R3.14.12.7/support/mks937a/2-97`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`mks937a.ibek.support.yaml`](mks937a.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `mks937a.mks937a` | Template database for an MKS937A Multi-Sensor System (vacuum gauge controller) read over StreamDevice. |
| `mks937a.mks937aGauge` | Imported from DLS module mks937a (mks937aGauge.template) NOTE: needs a generic IOC built with mks937a (not the plain generic image). |
| `mks937a.mks937aGaugeGroup` | Imported from DLS module mks937a (mks937aGaugeGroup.template) |
| `mks937a.mks937aImg` | Imported from DLS module mks937a (mks937aImg.template) |
| `mks937a.mks937aImgDummy` | Imported from DLS module mks937a (mks937aImgDummy.template) |
| `mks937a.mks937aImgGroup` | Imported from DLS module mks937a (mks937aImgGroup.template) |
| `mks937a.mks937aImgMean` | Imported from DLS module mks937a (mks937aImgMean.template) NOTE: needs a generic IOC built with mks937a (not the plain generic image). |
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
- `mks937a.template`
- `mks937aGauge.template`
- `mks937aGaugeGroup.template`
- `mks937aGauge_positions.req`
- `mks937aImg.template`
- `mks937aImgDummy.template`
- `mks937aImgGroup.template`
- `mks937aImgMean.template`
- `mks937aInterlock.template`
- `mks937aPirg.template`
- `mks937aPirgDummy.template`
- `mks937aPirgGroup.template`
- `mks937aPlogADC.template`
- `mks937aPlogEGU.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (2 files)
- `sim/` - device simulator from the DLS source release (3 files)
- `test/` - device tests from the DLS source release (1 file)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[BUILD-TIME-ONLY.md](../BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `mks937aGauge.template`, `mks937aImgMean.template` | `DTYP "$(aitype=Hy8401ip)"`; compiled aSub routines `mks937aMeanInit`, `mks937aMeanCalc` |
