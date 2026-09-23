# ametekLockIn

Runtime StreamDevice pattern imported from the DLS support module `ametekLockIn`,
release `1-17special2` (`/dls_sw/prod/R3.14.12.7/support/ametekLockIn/1-17special2`).
Its files are pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`ametekLockIn.ibek.support.yaml`](ametekLockIn.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `ametekLockIn.ametekLockIn` | Ametek (Signal Recovery) lock-in amplifier |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `ametekLockIn.ibek.support.yaml`
- `ametekLockIn.proto`
- `ametekLockIn.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
