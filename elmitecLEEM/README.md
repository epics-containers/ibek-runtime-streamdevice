# elmitecLEEM

Runtime StreamDevice pattern imported from the DLS support module `elmitecLEEM`, release
`1-7` (`/dls_sw/prod/R3.14.12.7/support/elmitecLEEM/1-7`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`elmitecLEEM.ibek.support.yaml`](elmitecLEEM.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `elmitecLEEM.leem` | Elmitec LEEM control and monitoring |
| `elmitecLEEM.leemPSValue` | Elmitec LEEM power supply value parameter |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `elmitecLEEM.ibek.support.yaml`
- `leem-PSValue.template`
- `leem-PSValue_settings.req`
- `leem.proto`
- `leem.template`
- `leem_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
