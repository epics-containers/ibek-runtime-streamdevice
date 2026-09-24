# gardasoftLED

Runtime StreamDevice pattern imported from the DLS support module `gardasoftLED`,
release `2-13` (`/dls_sw/prod/R3.14.12.7/support/gardasoftLED/2-13`). Its protocol files
are pristine copies of that release; its templates are **derived** from the release's
VDCT sources.

How each file was obtained, and any change made to it, is recorded in the header of
[`gardasoftLED.ibek.support.yaml`](gardasoftLED.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `gardasoftLED.gardasoftLED` | Gardasoft PP612 LED controller |
| `gardasoftLED.gardasoftLEDChannel` | Gardasoft PP600 series LED controller channel |
| `gardasoftLED.gardasoftLED420` | Gardasoft PP420 LED controller |
| `gardasoftLED.gardasoftLED400Channel` | Gardasoft PP400 series LED controller channel |
| `gardasoftLED.gardasoftLED420Profile` | Gardasoft PP420 LED controller pulse profile |
| `gardasoftLED.gardasoftLED420ProfileChannel` | Gardasoft PP420 LED controller pulse profile channel |
| `gardasoftLED.gardasoftLED820` | Gardasoft PP820 LED controller |
| `gardasoftLED.gardasoftLED800Channel` | Gardasoft PP800 series LED controller channel |
| `gardasoftLED.gardasoftLEDRTSeries` | Gardasoft RT series LED controller |
| `gardasoftLED.gardasoftLEDRTSeriesChannel` | Gardasoft RT series LED controller channel |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `PP400Series.protocol`
- `PP400SeriesChannel.template`
- `PP400SeriesChannel_settings.req`
- `PP420LED.template`
- `PP420LED_settings.req`
- `PP420Profile.template`
- `PP420ProfileChannel.template`
- `PP420ProfileChannel_settings.req`
- `PP420Profile_settings.req`
- `PP600Series.protocol`
- `PP600SeriesChannel.template`
- `PP612LED.template`
- `PP800Series.protocol`
- `PP800SeriesChannel.template`
- `PP820LED.template`
- `PP820LED_settings.req`
- `RTSeries.protocol`
- `RTSeriesChannel.template`
- `RTSeriesChannel_settings.req`
- `RTSeriesLED.template`
- `gardasoftLED.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
