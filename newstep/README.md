# newstep

Runtime StreamDevice pattern imported from the DLS support module `newstep`, release
`2-6` (`/dls_sw/prod/R3.14.12.7/support/newstep/2-6`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`newstep.ibek.support.yaml`](newstep.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `newstep.NSC200` | Newport NSC200 single axis motion controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `NSC200.proto`
- `NSC200.template`
- `NSC200_settings.req`
- `newstep.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
