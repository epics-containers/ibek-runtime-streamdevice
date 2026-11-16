# scientificInstSCM10

Runtime StreamDevice pattern for the Scientific Instruments SCM10 single channel
cryogenic temperature monitor. It started from the SCM10 files in the DLS support
module `BL21I`: `SCM10.proto` (every release from 3-0) and the template, named
`SCM10.template` in 3-0 to 3-4-3 and `BL21I_SCM10_CryoTemp_Monitor.template` from 3-5.
They read the temperature only (3-0 to 3-4-3), then also the identity, IP address,
sensor reading and error status (3-5 on). Everything else was written with the help of
Claude (Anthropic) from the Model SCM10 manual (ASCII command set, printed pages 27-32),
and the files are rewritten rather than copied: `$(P):IDN_RBV` and its protocol keep
BL21I's form, so i21 sees the same record type and value.

## Entity models

| Entity model | Description |
|---|---|
| `scientificInstSCM10.scm10` | Temperature and sensor readings, error status, alarm and relay state, alarm set-points and deadbands, sensor curve and noise filter |

```yaml
  - type: scientificInstSCM10.scm10
    P: BL21I-EA-TMON-01
    PORT: scm10
    INTERFACE: RS232
```

`PORT` is an asyn port made by an asyn IP or serial entity in the same IOC. The
instrument has both interfaces:

- **RS232** (DB9, DCE): 9600, 19200, 57600 or 115200 baud, 8 data bits, no parity,
  1 stop bit, no flow control. The baud rate is set on the front panel.
- **Ethernet** (RJ45): a raw TCP data socket on port 9760, with the same ASCII
  commands. The address is set on the front panel; the instrument does not use DHCP.

Set `INTERFACE` to how the instrument is connected: `RS232` (the default) for its serial
port, directly or through a terminal server, and `TCP` for its Ethernet socket. It picks
the protocols the output records write with, because only the Ethernet socket answers a
set command (see below).

## Notes

- **Nothing is written at start-up.** Each output record reads the instrument's current
  value when the IOC starts, and there is no autosave. Restarting the IOC never changes
  the instrument's settings. These start-up reads time out after 500 ms each, so an
  SCM10 that does not answer delays `iocInit` by about 3 seconds at most.
- **Units of `$(P):SENSOR_RBV`.** Volts for a diode curve, ohms for an RTD curve, so the
  record has no `EGU`.
- **Sensor curve.** `$(P):CURVE` must match the sensor fitted. A wrong curve gives wrong
  temperatures or an out-of-range error in `$(P):ERROR_RBV`. The user curve (`User`) can only
  be loaded with the vendor's GUI.
- **Alarms.** Set-points and deadbands are in kelvin. `$(P):ALARM1_RBV` and `ALARM2_RBV` show
  the alarm state and go MAJOR when it is on. Enabling an alarm, and choosing high or low and
  latching, is not exposed (see below), so do that on the front panel or in the vendor GUI.
- **Polling load.** Temperature, sensor, error, alarm and relay state are read every
  second, the rest every 5 seconds. The instrument measures at up to 5 readings a second.
- **Replies over TCP.** The manual says the TCP socket ends replies with CR LF and sends
  `OK` after every command that sets something; over RS232 replies end with CR. The manual
  mentions `OK` only for TCP, so the pattern infers that a set command over RS232 gets no
  answer; one set command in a hardware smoke test would confirm it. With `INTERFACE: TCP` each output record's protocol reads the
  `OK` before it gives up the port; otherwise whichever query runs next on the port could
  take the `OK` as its reply and go INVALID. With `INTERFACE: RS232` the protocol only
  writes, since waiting for an answer that never comes would time out. A wrong
  `INTERFACE` shows as exactly those errors: INVALID readings after a write (`RS232` on
  the TCP socket) or every write timing out (`TCP` on RS232).
  Replies are read up to the CR; the LF after it is discarded with the rest of any input
  waiting before the next command.
- **Identity.** `$(P):IDN_RBV` is a `stringin` holding the `*IDN?` reply less its
  `Scientific Instruments,` prefix, e.g. `SCM10,1859,1.05`.

### Unknowns

- **Error replies.** The manual does not say what `T?` returns when the sensor is open or
  out of range; `$(P):ERROR_RBV` shows the reason.

### Left out on purpose for now

- `ALA` (alarm enable, high/low and latching): one command sets all three, so it needs a
  record that writes three values at once;
- `RELY` (relay mode): the manual does not give the values of the mode field;
- `ANAST`, `ANAT`, `ANAM`, `AOUT`: the analog output;
- `SHDR`, `CDAT`: user curve upload, which the vendor GUI does;
- `FDEF`: restores the factory calibration.

The "Excluded commands" section at the end of the protocol file lists them too.

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC instance's
`config/`:

- `scientificInstSCM10.ibek.support.yaml`
- `scientificInstSCM10.proto`
- `scientificInstSCM10.template`
- `scm10.pvi.device.yaml`, hand-maintained: `generate-pvi.py` would pair each alarm
  set-point with the alarm state rather than with its own readback

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
