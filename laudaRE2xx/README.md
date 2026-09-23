# laudaRE2xx

Runtime StreamDevice pattern imported from the DLS support module `laudaRE2xx`, release
`2-9-9` (`/dls_sw/prod/R3.14.12.7/support/laudaRE2xx/2-9-9`). Its files are pristine
copies of that release.

How each file was obtained, and any change made to it, is recorded in the header of
[`laudaRE2xx.ibek.support.yaml`](laudaRE2xx.ibek.support.yaml). That header is vendored
with the pattern, so the provenance travels into every IOC instance that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `laudaRE2xx.lRE2xx` | Lauda ecoline star edition recirculating chiller, also valid for ecoline silver, ecoline gold and proline devices. |
| `laudaRE2xx.lIntegralT` | Lauda Integral T process thermostat / recirculating chiller. |
| `laudaRE2xx.lVariocool` | Lauda Variocool recirculating chiller (uses the lREVariocool protocol). |
| `laudaRE2xx.lMCxxx` | Lauda Microcool recirculating chiller. |
| `laudaRE2xx.lRE2xx_RS485` | Imported from DLS module laudaRE2xx (lRE2xx_RS485.template) |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `lIntegralT.proto`
- `lIntegralT.template`
- `lIntegralT_settings.req`
- `lMCxxx.proto`
- `lMCxxx.template`
- `lMCxxx_settings.req`
- `lRE2xx.proto`
- `lRE2xx.template`
- `lRE2xx_RS485.proto`
- `lRE2xx_RS485.template`
- `lRE2xx_RS485_settings.req`
- `lRE2xx_settings.req`
- `lREVariocool.proto`
- `lVariocool.template`
- `lVariocool_settings.req`
- `laudaRE2xx.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `sim/` - device simulator from the DLS source release (1 file)
