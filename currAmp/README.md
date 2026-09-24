# currAmp

Runtime StreamDevice pattern imported from the DLS support module `currAmp`, release
`1-45` (`/dls_sw/prod/R3.14.12.7/support/currAmp/1-45`). Its protocol files are pristine
copies of that release; its templates are **derived** from the release's VDCT sources.

How each file was obtained, and any change made to it, is recorded in the header of
[`currAmp.ibek.support.yaml`](currAmp.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `currAmp.YMCS0012` | Oxford Danfysik YMCS0012 current amplifier / quad beam position monitor |
| `currAmp.YMCS0009` | Oxford Danfysik YMCS0009 current amplifier / quad beam position monitor |
| `currAmp.currAmpOffsets` | Per-range dark-current offsets for a current amplifier. Stores a set of offsets for each of the six amplifier ranges and pushes the correct set down to the amplifier whenever the range changes. Works with both YMCS0009 and YMCS0012 as they have the same number of ranges. Also provides offset-calibrated and ring-current-normalised intensity. Includes currAmpRange.template six times via msi. |
| `currAmp.currAmpADC` | Calculates calibrated currents (in uA) from ADC channels wired to the voltage outputs of an OD current amplifier, using the range selected over serial by YMCS0009/YMCS0012 plus configurable dark-current offsets. Includes currAmpRangeADC.template six times via msi. |
| `currAmp.currAmpSingle` | Interface for extracting a single value from a current amplifier, copying the amplifier's high and low limits across to the derived record. |
| `currAmp.currAmp_ai` | Simple ai record to use with an ADC input for reading an individual amplifier current. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `YMCS0009.template`
- `YMCS0012.template`
- `currAmp.ibek.support.yaml`
- `currAmpADC.template`
- `currAmpOffsets.template`
- `currAmpRange.template`
- `currAmpRangeADC.template`
- `currAmpSingle.template`
- `currAmp_ai.template`
- `ymcs.protocol`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (3 files)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[BUILD-TIME-ONLY.md](../BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `currAmp_ai.template` | `DTYP` is the instance-supplied `$(DTYPE)`, so an instance can name device support the image lacks |
