# pr4000

Runtime StreamDevice pattern imported from the DLS support module `pr4000`, release
`3-2` (`/dls_sw/prod/R3.14.12.7/support/pr4000/3-2`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`pr4000.ibek.support.yaml`](pr4000.ibek.support.yaml). That header is vendored with the
pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `pr4000.pr4000chan` | Template database for a PR4000 Baratron gauge controller channel |
| `pr4000.pr4000` | Template database for a PR4000 Baratron gauge controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `pr4000.ibek.support.yaml`
- `pr4000.protocol`
- `pr4000.template`
- `pr4000chan.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (1 file)
