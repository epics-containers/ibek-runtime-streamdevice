# Build-time-only StreamDevice modules (NOT runtime patterns)

These DLS `*BUILDER` support modules talk to their device over StreamDevice, but they
**cannot** be vendored as runtime patterns in this repo. Each one needs something the
generic `ioc-streamdevice` image does **not** ship — a module-specific **compiled**
library, `.dbd`, or state-notation (SNL) program — so it must be built into a custom
image and wired up with a build-time `ibek-support` definition instead.

The litmus test (same one used to admit the runtime patterns): a module is runtime-able
only if every record uses device support already in the generic image (StreamDevice +
asyn + EPICS base) and its `builder.py` init methods emit **no** module-specific
compiled iocsh command. The modules below each fail that test for the reason given.

## Needs a compiled device-configuration command

The driver-init iocsh function is compiled into the module's own library.

| Module | Version | Compiled iocsh command |
|---|---|---|
| `capaNCDT6200` | 1-0 | `capaNCDT6200Config` |
| `leybold` | 2-2 | `centerNConfig` |
| `linkamMotor` | 1-1 | `linkamMDS600Config` |
| `PLV1000` | 1-1 | `PLV1000Config` |
| `specsIQE1135` | 0-4 | `specsIQE1135Config` |
| `YLRLasers` | 3-1 | `YLRLaserConfig` |
| `rga` | 4-26 | `MVPlusInit` |

## Needs a compiled SNL sequencer program

`seq <program>` loads a state-notation-language program that is compiled into the
module's library (and registered by its `.dbd`). `seq` appears in **0 of the 80**
admitted runtime patterns.

| Module | Version | SNL program / library |
|---|---|---|
| `hidenRGA` | 1-12 | `seq(sncDegas, ...)` — `hidenRGA` lib, `sncHidenRGA` dbd |
| `pmacUtil` | 5-13 | `seq(gather, ...)` — `pmacUtil` lib, `pmacUtilSupport` dbd |
| `filters` | 2-19-4 | `seq &xiaArrayTable` — `xiaArray` lib, `xiaArraySupport` dbd |
| `transfocator` | 4-9 | `seq recover` — `transfocator` lib/dbd |

## Needs the motor record + a compiled motor driver

| Module | Version | Compiled iocsh command(s) |
|---|---|---|
| `motomanNX100` | 1-17-1 | `drvAsynMotorConfigure`, `motomanCreate` |
| `pmacCoord` | 1-74 | `drvAsynMotorConfigure`, `pmacAsynCoordCreate`, `pmacSetCoordIdlePollPeriod`, `pmacSetCoordMovingPollPeriod` |

## Needs compiled Modbus support

| Module | Version | Compiled iocsh command(s) |
|---|---|---|
| `eurotherm2k` | Rx-y | `eurothermModbusCtrlConfigure`, `modbusInterposeConfig` (imports the `modbus` module) |

## Needs a compiled aSub / record-support library

The device's records reference subroutines or record/device support compiled into the
module's own library and registered by its `.dbd`.

| Module | Version | Why |
|---|---|---|
| `mecaRobot` | 1-7 | `mecaRobot` lib/dbd with `asubFunctions.c` (the `PostIocInitialise` itself only emits base `dbpf`, but the records need the compiled aSub support) |
| `insertionDevice` | 6-70 | `idExclusion8` compiled command; `Compax3`/`ID` compiled support |

---

## Skipped (not a StreamDevice pattern at all)

| Module | Version | Why |
|---|---|---|
| `ZoomLightLevel` | 1-1 | Ships no protocol file (its `ProtocolFiles` is commented out); records are mostly `asynFloat64`/`asynInt32` bindings and the few stream records depend on another module's `robotPLC.proto`. Not self-contained. |

## Generated, but contains records that reference non-stream device support

These **are** shipped as runtime patterns (their primary device class works over
StreamDevice and their `builder.py` emits no compiled iocsh command), but a subset of
their records reference compiled device support (a Hytec IP ADC/DAC, an ORNL serial
card, the npoint LC400 array support, or module-specific aSub routines). Those records
will not process in a generic `ioc-streamdevice` image unless the relevant support is
present. Maintainers may wish to trim those entity models or document the limitation.

| Module | Non-stream support referenced |
|---|---|
| `mks937a` | `DTYP="$(aitype=Hy8401ip)"` — Hytec 8401 IP ADC (overridable macro; 2 records) |
| `mks937b` | `DTYP="Hy8401ip"` — Hytec 8401 IP ADC (2 records) |
| `PIpiezo` | `DTYP="PIE516"` — PI E-516 interface (records outside the 4 shipped stream classes) |
| `jena` | `DTYP="Hy8401ip"`/`"Hy8402ao"` — Hytec IP ADC/DAC (the `aoPiezoControl` class) |
| `LC400-OEM` | `DTYP="LC400ArrayRead"/"LC400ArrayWrite"` — npoint LC400 compiled array support |
| `digitelMpc` | `DTYP="ornlSerial"` — ORNL serial support (the TSP/Ion-pump sub-templates) |
| `d2afe` | aSub records using `asubMethods.c` (compiled), plus a `d2afe` lib/dbd |
| `tecPeltier` | aSub records using `asubMethods.c` (compiled), plus a `tecPeltier` lib/dbd |
