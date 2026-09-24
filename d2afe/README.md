# d2afe

Runtime StreamDevice pattern imported from the DLS support module `d2afe`, release `0-1`
(`/dls_sw/prod/R3.14.12.7/support/d2afe/0-1`). Its files are pristine copies of that
release.

How each file was obtained, and any change made to it, is recorded in the header of
[`d2afe.ibek.support.yaml`](d2afe.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `d2afe.attenuator_cmd` | Imported from DLS module d2afe (attenuator_cmd.template) |
| `d2afe.attenuators_set_fan` | Imported from DLS module d2afe (attenuators_set_fan.template) |
| `d2afe.cal_table` | Imported from DLS module d2afe (cal_table.template) |
| `d2afe.d2afeStatus` | Imported from DLS module d2afe (d2afeStatus.template) |
| `d2afe.d2ptg` | Imported from DLS module d2afe (d2ptg.template) |
| `d2afe.d2ptg_cal_scan_list` | Imported from DLS module d2afe (d2ptg_cal_scan_list.template) |
| `d2afe.d2ptg_mon_scan_list` | Imported from DLS module d2afe (d2ptg_mon_scan_list.template) |
| `d2afe.d2ptg_scan` | Imported from DLS module d2afe (d2ptg_scan.template) |
| `d2afe.fwVersionCheck` | Imported from DLS module d2afe (fwVersionCheck.template) NOTE: needs a generic IOC built with d2afe (not the plain generic image). |
| `d2afe.generic_cmd` | Imported from DLS module d2afe (generic_cmd.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `attenuator_cmd.template`
- `attenuators_set_fan.template`
- `cal_table.template`
- `d2afe.ibek.support.yaml`
- `d2afe.proto`
- `d2afeStatus.template`
- `d2ptg.template`
- `d2ptg_cal_scan_list.template`
- `d2ptg_mon_scan_list.template`
- `d2ptg_scan.template`
- `fwVersionCheck.template`
- `generic_cmd.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `fwVersionCheck.template` | compiled aSub routine `checkFW` |
