# leybold

Runtime StreamDevice pattern imported from the DLS support module `leybold`, release
`2-2` (`/dls_sw/prod/R3.14.12.7/support/leybold/2-2`). Its files are pristine copies of
that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`leybold.ibek.support.yaml`](leybold.ibek.support.yaml). That header is vendored with
the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `leybold.centerN` | Imported from DLS module leybold (centerN.template) NOTE: needs a generic IOC built with leybold (not the plain generic image). |
| `leybold.coolpak` | Imported from DLS module leybold (coolpak.template) NOTE: needs a generic IOC built with leybold (not the plain generic image). |
| `leybold.read_floatE` | Imported from DLS module leybold (read_floatE.template) |
| `leybold.read_float_float_float` | Imported from DLS module leybold (read_float_float_float.template) |
| `leybold.read_int` | Imported from DLS module leybold (read_int.template) |
| `leybold.read_int_floatE` | Imported from DLS module leybold (read_int_floatE.template) |
| `leybold.read_string` | Imported from DLS module leybold (read_string.template) |
| `leybold.read_write_float` | Imported from DLS module leybold (read_write_float.template) |
| `leybold.read_write_floatE_floatE` | Imported from DLS module leybold (read_write_floatE_floatE.template) |
| `leybold.read_write_int` | Imported from DLS module leybold (read_write_int.template) |
| `leybold.read_write_int_floatE` | Imported from DLS module leybold (read_write_int_floatE.template) |
| `leybold.write_raw_int` | Imported from DLS module leybold (write_raw_int.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `centerN.template`
- `centerN_settings.req`
- `coolpak.template`
- `coolpak_settings.req`
- `leybold.ibek.support.yaml`
- `leybold.proto`
- `read_floatE.template`
- `read_float_float_float.template`
- `read_int.template`
- `read_int_floatE.template`
- `read_int_floatE_settings.req`
- `read_string.template`
- `read_write_float.template`
- `read_write_floatE_floatE.template`
- `read_write_int.template`
- `read_write_int_floatE.template`
- `read_write_int_floatE_settings.req`
- `read_write_int_settings.req`
- `write_raw_int.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (4 files)

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[BUILD-TIME-ONLY.md](../BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `centerN.template`, `coolpak.template` | compiled asyn drivers (`centerNConfig`, `coolpakConfig`) |

## Upstream defects carried as-is

- `read_floatE` calls protocol `get_floatE`, which `leybold.proto` does not define
