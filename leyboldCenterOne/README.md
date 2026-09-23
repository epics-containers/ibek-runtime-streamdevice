# leyboldCenterOne

Runtime StreamDevice pattern imported from the DLS support module `leyboldCenterOne`,
release `1-1` (`/dls_sw/prod/R3.14.12.7/support/leyboldCenterOne/1-1`). Its files are
pristine copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`leyboldCenterOne.ibek.support.yaml`](leyboldCenterOne.ibek.support.yaml). That header
is vendored with the pattern, so the provenance travels into every IOC instance that
uses it.

## Entity models

| Entity model | Description |
|---|---|
| `leyboldCenterOne.centerOne` | Leybold CenterOne vacuum gauge controller - reads pressure with a validity watchdog over StreamDevice. |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `centerOne.proto`
- `centerOne.template`
- `centerOne_settings.req`
- `leyboldCenterOne.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
