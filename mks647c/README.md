# mks647c

Runtime StreamDevice pattern imported from the DLS support module `mks647c`, release
`0-1-4` (`/dls_sw/prod/R3.14.12.7/support/mks647c/0-1-4`). Its files are pristine copies
of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`mks647c.ibek.support.yaml`](mks647c.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `mks647c.mks647cChan` | MKS 647C mass flow controller channel |
| `mks647c.mks647c8ChanCtrl` | MKS 647C 8 channel mass flow controller |
| `mks647c.mks647c4ChanCtrl` | MKS 647C 4 channel mass flow controller |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `mks647C.proto`
- `mks647c.ibek.support.yaml`
- `mks647c4ChanCtrl.template`
- `mks647c8ChanCtrl.template`
- `mks647cChan.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
