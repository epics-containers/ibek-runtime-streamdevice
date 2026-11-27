# eurotherm2k

Runtime StreamDevice pattern imported from the DLS support module `eurotherm2k`, release
`2-10` (`/dls_sw/prod/R3.14.12.7/support/eurotherm2k/2-10`). Its templates and protocol
file are pristine copies of that release. The `eurotherm2k.eurotherm2k` entity model is
hand-written
([ibek-runtime-streamdevice#22](https://github.com/epics-containers/ibek-runtime-streamdevice/issues/22));
its defaults for `SPMAX` (`1000`), `SPMIN` (`0`) and `EGU` (`C/s`) are
`eurotherm2k.template`'s own.

How each file was obtained, and any change made to it, is recorded in the header of
[`eurotherm2k.ibek.support.yaml`](eurotherm2k.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `eurotherm2k.eurotherm2k` | Eurotherm 2k temperature controller |

Only the StreamDevice `eurotherm2k` device is in this pattern. The release's
`eurothermModbus`, `eurothermModbusLoop` and `eurothermModbusPV` classes need the
compiled Modbus driver, and `eurothermParam.template`, `eurothermConfParam.template`
and `eurothermPV.template` are loaded by no `builder.py` class, so none of them are
here; see [_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `eurotherm2k.ibek.support.yaml`
- `eurotherm2k.proto`
- `eurotherm2k.pvi.device.yaml`
- `eurotherm2k.template`
- `eurotherm2k_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `docs/` - documentation from the DLS source release (3 files)
- `sim/` - device simulator from the DLS source release (1 file)
- `test/` - device tests from the DLS source release (1 file)
