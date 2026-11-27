# lakeshore336

Runtime StreamDevice pattern imported from the DLS support module `lakeshore336`,
release `2-19-1` (`/dls_sw/prod/R3.14.12.7/support/lakeshore336/2-19-1`). Its files
are pristine copies of that release, except `lakeshore336-FirmwareVersion.template`
(below).

How each file was obtained, and any change made to it, is recorded in the header of
[`lakeshore336.ibek.support.yaml`](lakeshore336.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `lakeshore336.lakeshore336` | Lakeshore 336 temperature controller: temperature/voltage readings for 4 input channels, control of 4 outputs, identification and comms disable. |

The model is ibek-support's `lakeshore336` model, which mirrors the DLS `builder.py`,
with `PORT` a str rather than an object.

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `lakeshore336-FirmwareVersion.template`
- `lakeshore336.ibek.support.yaml`
- `lakeshore336.proto`
- `lakeshore336.pvi.device.yaml`
- `lakeshore336.template`
- `lakeshore336_positions.req`
- `lakeshore336loop.template`
- `lakeshoreAout.template`

`lakeshore336.template` includes `lakeshore336loop.template` (once per loop),
`lakeshoreAout.template` (loops 3 and 4) and `lakeshore336-FirmwareVersion.template`.
`lakeshore336_positions.req` names the autosaved `$(P):MOUT:TRACKCL<n>` of each loop,
as the level-0 request files of the DLS IOCs do; it is not in the DLS release, which
leaves it to the builder.

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file

## `lakeshore336-FirmwareVersion.template`

The DLS template's aSub `$(P):FIRMWARE:CALC` called `extractFirmwareVersion`, the
module's only compiled code. Here `FIRMWARE:CALC` is an `scalcout` from the calc
module, which the generic image ships. On each new `$(P):ID` it writes to
`$(P):FIRMWARE:VERSION` the text after the last comma of the `*IDN?` reply, or
`not available` unless the reply holds `MODEL336` and a comma, as the aSub did. A
loopback test IOC running the compiled aSub and this record side by side gave the
same string for every reply tried, including extra commas, no comma, an empty reply,
a trailing comma and replies of the full 39 characters.

One difference from the aSub: the aSub wrote `FIRMWARE:VERSION` only when the text
changed, while the `scalcout` writes it each time `:ID` changes. The value, and so
its monitors, change only when the text does.
