# granvillePhillips

Runtime StreamDevice pattern imported from the DLS support module `granvillePhillips`,
release `2-10` (`/dls_sw/prod/R3.14.12.7/support/granvillePhillips/2-10`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`granvillePhillips.ibek.support.yaml`](granvillePhillips.ibek.support.yaml). That
header is vendored with the pattern, so the provenance travels into every IOC instance
that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `granvillePhillips.gp350` | Support for a Granville Phillips GP350 gauge controller, typically for Hot Cathode Gauges on End Stations. |
| `granvillePhillips.gp307` | Support for a Granville Phillips GP307 gauge controller, typically used on End Stations for Hot Cathode Gauges. |
| `granvillePhillips.gp307Gauge` | Imported from DLS module granvillePhillips (gp307Gauge.template) |
| `granvillePhillips.gp307Hcg` | Imported from DLS module granvillePhillips (gp307Hcg.template) |
| `granvillePhillips.gp307HcgDummy` | Imported from DLS module granvillePhillips (gp307HcgDummy.template) |
| `granvillePhillips.gp307Pirg` | Imported from DLS module granvillePhillips (gp307Pirg.template) |
| `granvillePhillips.gp307PirgDummy` | Imported from DLS module granvillePhillips (gp307PirgDummy.template) |
| `granvillePhillips.gp350Gauge` | Imported from DLS module granvillePhillips (gp350Gauge.template) |
| `granvillePhillips.gp350Hcg` | Imported from DLS module granvillePhillips (gp350Hcg.template) |
| `granvillePhillips.gp350HcgDummy` | Imported from DLS module granvillePhillips (gp350HcgDummy.template) |
| `granvillePhillips.gp350Pirg` | Imported from DLS module granvillePhillips (gp350Pirg.template) |
| `granvillePhillips.gp350PirgDummy` | Imported from DLS module granvillePhillips (gp350PirgDummy.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `gp307.proto`
- `gp307.template`
- `gp307Gauge.template`
- `gp307Hcg.template`
- `gp307HcgDummy.template`
- `gp307Pirg.template`
- `gp307PirgDummy.template`
- `gp350.proto`
- `gp350.template`
- `gp350Gauge.template`
- `gp350Hcg.template`
- `gp350HcgDummy.template`
- `gp350Pirg.template`
- `gp350PirgDummy.template`
- `granvillePhillips.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (2 files)
