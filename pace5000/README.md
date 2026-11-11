# pace5000

Runtime StreamDevice pattern for the Druck PACE5000 pressure controller. Unlike most
patterns here it is **not imported from a DLS support module**: no DLS module covers
the PACE. It was written with the help of Claude (Anthropic) from the PACE SCPI
Remote Communications Manual (K0472, rev J). The command list started from that of
the DLS `DruckDPI515` module, an older Druck controller with a similar SCPI command
set, and was changed wherever the PACE differs.

The protocol file cites the manual's page for each command.

## Entity models

| Entity model | Description |
|---|---|
| `pace5000.pace5000` | One control module: pressure readback, set-point, control mode, slew, in-limits, units, zero and vent |

`CH` is the control module and defaults to 1. A PACE6000 has two: add one entity per
module, with `CH: 1` and `CH: 2` and a different `P` for each.

```yaml
  - type: pace5000.pace5000
    P: BL19I-EA-PACE-01
    PORT: pace
```

`PORT` is an asyn port made by an asyn IP or serial entity in the same IOC.

## Notes

- **Nothing is written at start-up.** Each output record reads the instrument's
  current value when the IOC starts, and there is no autosave. Restarting the IOC
  never changes the instrument's settings. (The DLS `DruckDPI515` driver did the
  opposite: it wrote every setting back whenever it reconnected.) These start-up
  reads time out after 500 ms each, so a PACE that does not answer delays `iocInit`
  by about 5.5 seconds per entity at most.
- **Polling locks the front panel.** Most SCPI commands put the PACE in remote and
  disable its touch screen (manual p1), and this pattern polls every second. To use
  the front panel, set `$(P):POLL` to Paused, then press `$(P):LOCAL`. Set `POLL` back
  to Running to resume; the next poll returns the PACE to remote.
- **Isolation valve.** The manual warns that opening the isolation valve with high
  pressure in the external system can make the PACE malfunction. Equalize to zero
  gauge first.
- **Units.** Every pressure value, the set-point and the slew rates are in the units
  shown by `$(P):UNITS_RBV`. The records carry no `EGU` for them. `$(P):UNITS` takes a
  unit name such as `MBAR`, `BAR`, `KPA` or `PSI`.
- **Control range.** `$(P):CONTROLRANGE` must match one of the instrument's range
  names exactly, case included, e.g. `3.50barg`.
- **Errors.** `$(P):ERROR_RBV` reads the instrument's 5-entry error queue every 5
  seconds; each read removes one error. Write errors only show there, since the PACE
  does not reply to commands that set something.
- **Polling load.** About 6 reads a second: pressure, in-limits, effort and measured
  slew every second, zero and vent state every 2 seconds, everything else every 5.

### Untested on hardware

These protocols were written from the manual and have not yet been run against a
PACE. Check on a real unit:

- **The reply terminator.** The manual does not give it. The protocol expects LF; if
  replies end in CR LF, readbacks fail with "surplus input" and `InTerminator` in
  `pace5000.proto` needs to be `CR LF`.
- **Ethernet.** The manual covers only RS 232 and IEEE 488, so the TCP port and
  whether it is a raw socket are not documented there.
- **Reply headers.** The protocol skips each reply's header rather than matching it,
  because the manual's examples are not consistent about it.

### Left out on purpose

- serial interface settings (`:SYST:COMM:SER:*`): changing them cuts the link;
- calibration and password commands (`:CAL:PRES:*` apart from auto-zero,
  `:SYST:PASS:*`): they alter the factory calibration;
- local lockout (`:LLO`);
- `*SRE`: a non-zero value makes the PACE send unsolicited `:SRQ` messages over RS 232,
  which these protocols do not expect;
- the sense range (`:SENS:PRES:RANG`, `:SENS:PRES?`), which only matters for
  calibration; `$(P):PRESSURE_RBV` reads the control sensor instead.

The "Excluded commands" section at the end of the protocol file lists them too.

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC instance's
`config/`:

- `pace5000.ibek.support.yaml`
- `pace5000.proto`
- `pace5000.pvi.device.yaml`
- `pace5000.template`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
