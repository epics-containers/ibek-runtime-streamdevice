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

Most were never admitted. The section [Removed after shipping](#removed-after-shipping--compiled-subgensubasub-routines)
covers modules that *were* shipped as patterns and have since been withdrawn.

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
module's library (and registered by its `.dbd`). `seq` appears in **0 of the 100**
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

## Removed after shipping — compiled `sub`/`genSub`/`aSub` routines

These 19 modules were generated and shipped as runtime patterns before this failure mode
was spotted, and have now been **removed from the repo**. Their `builder.py` emits no
compiled iocsh command — which is what let them through the original gate — but their
records include `sub`, `genSub` or `aSub` records whose `SNAM`/`INAM` names a C routine
compiled into the module's own library and registered by its `.dbd`. None of those
routines are registered by anything in the generic image (EPICS base 7.0.9 +
`asyn`, `StreamDevice`, `calc`, `std`, `sscan`, `busy`, `autosave`, `iocStats`,
`pvlogging`), so the record fails `init_record` and never processes in a vendored IOC.

Converting `genSub` to a base-native `aSub` does **not** rescue these — the routine is
still C that has to be linked in.

| Module | Version | Unresolvable routine(s) |
|---|---|---|
| `FQCRBarcodeCamera` | 2-7 | `AscToDec` |
| `I400` | 3-6-2 | `i400parse` |
| `OXCS700` | 2-22 | `alarmlookupProcess` (in `OXcommon700.template`, `include`d by both entities) |
| `OXCryo` | 1-4 | `alarmlookupProcess` (in `OXcommon.template`, reached by all five entities) |
| `bronkhorstFlowBus` | 1-5 | `asciiToString10`, `floatToInt`, `intToFloat` |
| `capaNCDT` | 3-4 | `capaNCDTInit` (`INAM`), `capaNCDTProc` |
| `cmsIon` | Rx-y | `UpdateWeekEndTime` (`INAM`), `ResetManualDose`, `RunEndReset`, `WeekEndCheck` |
| `d2afe` | 0-1 | `checkFW` |
| `debenOF` | 2-0 | `mySubInit` (`INAM`), `parseStatusString` |
| `digitelSpc` | 1-13 | `versionCheck` |
| `dlsCAENels` | 2-6 | `wipeStates` |
| `huberChiller` | 1-3 | `alarmCommand`, `controlCommand`, `decodeGeneral`, `decodeLimit`, `setpointCommand` |
| `lakeshore336` | 2-19-1 | `extractFirmwareVersion` (in `lakeshore336-FirmwareVersion.template`, unconditionally `include`d by `lakeshore336.template`) |
| `laserPuckPointer` | 2-16 | `isbWrite`, `sendPuckDemand` |
| `mitsubishiRobot` | 4-36 | `CmdErrorLookup`, `DecToAsc`, `ErrorLookup`, `LocationLookup`, `LogError`, `Logging`, `PuckLabel`, `Regex` |
| `pfeifferTC400` | 2-5 | `pfeifferErrorCodeParse`, `pfeifferErrorMessageParse`, `pfeifferParamSetVetolistCheck` |
| `picotechPT104` | 2-3 | `pt104_resToT`, `pt104_ucharToUInt` |
| `strainGauge` | 2-9 | `parseSetpointValue` |
| `tecPeltier` | 1-6 | `SNAM` is the `$(CONVERT)` macro — the instance names a routine from the module's compiled `asubMethods.c` |

### Collateral — working entity models withdrawn with them

Removal was **whole-pattern**, so five of the above took usable entity models down with
them. Nothing else in the repo referenced their files, so re-admitting any of these
later is a self-contained job: re-generate the pattern and drop the offending
template/`db` and its `entity_model` from the support yaml.

| Module | Broken entity model(s) | Entity models lost as collateral |
|---|---|---|
| `I400` | `I400` | `IC101` |
| `dlsCAENels` | `dlsCAENelsGroup` | `dlsCAENels`, `dlsCAENelsChannel` |
| `strainGauge` | `strainGauge` | `strainGaugeOmegaPt` |
| `d2afe` | `_fwVersionCheck` | `d2ptg`, `_d2afeStatus`, `_cal_table`, `_d2ptg`, `_d2ptg_scan`, `_d2ptg_cal_scan_list`, `_d2ptg_mon_scan_list` |
| `tecPeltier` | `read_parameter`, `read_channel_parameter`, `write_channel_parameter` | `parameters`, `read_firmware`, `tecPeltier`, `tec1122` |

### A note on how strict this gate is

The gate rejects a **whole pattern** when **any** reachable record needs support the
generic image lacks. That is deliberately conservative, and it is stricter than real
deployments require: a site that never instantiates the offending entity model — or
that reads the device over Channel Access links from another IOC instead — is
unaffected by the missing routine. This is exactly the case for `currAmp`, whose `DTYP`
is instance-supplied via `currAmp_ai.template`: it remains shipped because its known
consumer does not use that entity model — it reads the device over Channel Access
instead.

Withdrawal was chosen over case-by-case trimming because it keeps the shipped set
honest with no per-site caveats. Patterns can be re-admitted individually, trimmed to
their runtime-able entity models, whenever someone actually needs one.

---

## Skipped (not a StreamDevice pattern at all)

| Module | Version | Why |
|---|---|---|
| `ZoomLightLevel` | 1-1 | Ships no protocol file (its `ProtocolFiles` is commented out); records are mostly `asynFloat64`/`asynInt32` bindings and the few stream records depend on another module's `robotPLC.proto`. Not self-contained. |

## Generated, but contains records that reference non-stream device support

These **are** shipped as runtime patterns (their primary device class works over
StreamDevice and their `builder.py` emits no compiled iocsh command), but a subset of
their records reference compiled device support (a Hytec IP ADC/DAC, an ORNL serial
card, or the npoint LC400 array support). Those records will not process in a generic
`ioc-streamdevice` image unless the relevant support is present. Maintainers may wish to
trim those entity models or document the limitation — see
[A note on how strict this gate is](#a-note-on-how-strict-this-gate-is) for why these
are still shipped when the compiled-routine cases above were withdrawn.

| Module | Non-stream support referenced |
|---|---|
| `mks937a` | `DTYP="$(aitype=Hy8401ip)"` — Hytec 8401 IP ADC (overridable macro; 2 records) |
| `mks937b` | `DTYP="Hy8401ip"` — Hytec 8401 IP ADC (2 records) |
| `PIpiezo` | `DTYP="PIE516"` — PI E-516 interface (records outside the 4 shipped stream classes) |
| `jena` | `DTYP="Hy8401ip"`/`"Hy8402ao"` — Hytec IP ADC/DAC (the `aoPiezoControl` class) |
| `LC400-OEM` | `DTYP="LC400ArrayRead"/"LC400ArrayWrite"` — npoint LC400 compiled array support |
| `digitelMpc` | `DTYP="ornlSerial"` — ORNL serial support (the TSP/Ion-pump sub-templates) |
| `currAmp` | `DTYP, "$(DTYPE)"` in `currAmp_ai.template` — instance-supplied, so an instance can name device support the image lacks (the other five entity models are pure `stream`) |
