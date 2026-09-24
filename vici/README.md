# vici

Runtime StreamDevice pattern imported from the DLS support module `vici`, release `1-14`
(`/dls_sw/prod/R3.14.12.7/support/vici/1-14`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`vici.ibek.support.yaml`](vici.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `vici.viciE2CA` | Controls a Valco Vici E2CA multiposition valve actuator controller |
| `vici.viciEMT` | Controls a Valco Vici EMT multiposition valve actuator controller |
| `vici.viciEUTA` | Controls a Valco Vici EUTA multiposition valve actuator controller |
| `vici.viciUM` | Controls a Valco Vici UMH/UMD/UMT modular universal valve actuator controller |
| `vici.eightGasSelect` | Imported from DLS module vici (eightGasSelect.template) |
| `vici.fourGasSelect` | Imported from DLS module vici (fourGasSelect.template) |
| `vici.sixteenGasSelect_2EMT_1E2CA` | Imported from DLS module vici (sixteenGasSelect_2EMT_1E2CA.template) |
| `vici.sixteenGasSelect_2EMT_1VALVE` | Imported from DLS module vici (sixteenGasSelect_2EMT_1VALVE.template) |
| `vici.viciEMT_dummy` | Imported from DLS module vici (viciEMT_dummy.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `E2CA.proto`
- `EMT.proto`
- `EUTA.proto`
- `UM.proto`
- `eightGasSelect.template`
- `eightGasSelect_positions.req`
- `fourGasSelect.template`
- `fourGasSelect_positions.req`
- `sixteenGasSelect_2EMT_1E2CA.template`
- `sixteenGasSelect_2EMT_1E2CA_positions.req`
- `sixteenGasSelect_2EMT_1VALVE.template`
- `sixteenGasSelect_2EMT_1VALVE_positions.req`
- `vici.ibek.support.yaml`
- `viciE2CA.template`
- `viciEMT.template`
- `viciEMT_dummy.template`
- `viciEUTA.template`
- `viciUM.template`
- `viciUM_positions.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (2 files)
