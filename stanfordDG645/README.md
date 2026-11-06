# stanfordDG645

Runtime StreamDevice pattern imported from the DLS support module `stanfordDG645`,
release `1-3` (`/dls_sw/prod/R3.14.12.7/support/stanfordDG645/1-3`). Its files started
as copies of that release and have since been extended to cover the DG645 command set,
so they are no longer pristine. The original `getDelay` and `setDelay` protocols and the
PV names of the original delay and width records are unchanged.

How each file was obtained, and any change made to it, is recorded in the header of
[`stanfordDG645.ibek.support.yaml`](stanfordDG645.ibek.support.yaml). That header is
vendored with the pattern, so the provenance travels into every IOC instance that uses
it.

## Entity models

| Entity model | Description |
|---|---|
| `stanfordDG645.stanfordDG645` | Instrument-wide records: common IEEE-488.2, status, trigger and burst |
| `stanfordDG645.stanfordDG645Channel` | One delay channel pair (`CH`: `AB`, `CD`, `EF` or `GH`): delay, width, step sizes and the output prescaler. Add one per output you use |
| `stanfordDG645.stanfordDG645Output` | One front-panel output's levels (`CH`: `T0`, `AB`, `CD`, `EF` or `GH`): amplitude, offset and polarity. Add one per output you use |

`P` and `PORT` are the same on all three. The delay channel and output numbers the
DG645 uses are worked out from `CH`.

### Upgrading from the single-entity version

The delay and width PVs (`$(P):AB:DELAY`, `$(P):AB:WIDTH` and their `_RBV`
readbacks, for AB, CD, EF and GH) used to belong to `stanfordDG645.stanfordDG645`. They
now belong to `stanfordDG645.stanfordDG645Channel`, so an `ioc.yaml` that only has the
`stanfordDG645` entity **loses them** when it picks up this version. Add one
`stanfordDG645Channel` entity per channel pair to keep them:

```yaml
  - type: stanfordDG645.stanfordDG645Channel
    P: BL19I-EA-DG645-01
    PORT: dg645
    CH: AB
```

## Notes

- **Delays are fixed-reference.** `DELAY` is always relative to T0 and `WIDTH` to the
  leading edge, because the DG645's `DLAY` command sets the link and the time together.
  Re-linking a channel from the front panel changes what the readbacks mean.
- **Controls.** The `:STEP` records are Down/Up button pairs. `AUTOCAL`, `SELFTEST`,
  `OPC`, `ESR`, `INSR` and `LERR` are Passive queries, so their screens have a button
  that processes them (`pvi-overrides.yaml`). `ESR`, `INSR` and `LERR` change instrument
  state when read.
- **`SELFTEST` resets the unit to its default settings**, according to the manual.
- **`AUTOCAL` and `SELFTEST` hold the port.** The proto sets a long `LockTimeout` so
  other records queue behind them, but how long they take is not in the manual, and the
  reply timeouts in the proto are guesses to check on a real unit.
- **Polling.** The delay and width readbacks scan every second, as before. Other
  readbacks scan every 10 seconds, except step sizes and the status enables, which are
  read at start-up and after each write, so a change made at the front panel shows only
  after the next write or restart. All 4 channels and 5 outputs come to about 13 reads a
  second.
- **Some commands are left out.** The interface commands (`IFCF`, `EPHY`, `IFRS`,
  `XTRM`, `LCAL`, `REMT`, `LOCK?`/`UNLK?`, `EMAC?`) can reconfigure or cut off the comms
  link, and the calibration commands (`CALT`, `CALL`) overwrite factory calibration
  data, so the proto has no protocols for them. `LINK` is left out because `DLAY` sets
  the link anyway, and display select (`DISP`) because it only affects the front panel.
  The "Excluded commands" section at the end of the proto lists them.

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `stanfordDG645.ibek.support.yaml`
- `stanfordDG645.proto`
- `stanfordDG645.pvi.device.yaml`
- `stanfordDG645.template`
- `stanfordDG645Channel.pvi.device.yaml`
- `stanfordDG645Channel.template`
- `stanfordDG645Output.pvi.device.yaml`
- `stanfordDG645Output.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
- `pvi-overrides.yaml` - steers `generate-pvi.py` (see the repo README)
- `docs/` - documentation from the DLS source release (1 file)
- `sim/` - device simulator from the DLS source release (1 file)
