# VatLeakValve590

Runtime StreamDevice pattern imported from the DLS support module `VatLeakValve590`,
release `1-5` (`/dls_sw/prod/R3.14.12.7/support/VatLeakValve590/1-5`). Its files are
pristine copies of that release, apart from the scripted changes its support yaml header
lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`VatLeakValve590.ibek.support.yaml`](VatLeakValve590.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `VatLeakValve590._VatLeakValve590seriesTemplate` | Template database for VAT Variable Leak Valve 590 Series |
| `VatLeakValve590.VatLeakValve590series` | VAT Variable Leak Valve 590 Series |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `V590.proto`
- `VATLeakValve590series.template`
- `VATLeakValve590series_settings.req`
- `VatLeakValve590.ibek.support.yaml`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
