# celerotonChopper

Runtime StreamDevice pattern imported from the DLS support module `celerotonChopper`,
release `1-1` (`/dls_sw/prod/R3.14.12.7/support/celerotonChopper/1-1`). Its files are
pristine copies of that release, apart from the scripted changes its support yaml header
lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`celerotonChopper.ibek.support.yaml`](celerotonChopper.ibek.support.yaml). That header
is vendored with the pattern, so the provenance travels into every IOC instance that
uses it.

## Entity models

| Entity model | Description |
|---|---|
| `celerotonChopper.celerotonChopper` | Celeroton chopper magnetic bearing motor controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `celerotonChopper.ibek.support.yaml`
- `celerotonChopper.proto`
- `celerotonChopper.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (2 files)
