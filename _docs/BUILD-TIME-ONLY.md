# StreamDevice modules that are not runtime patterns

The DLS support modules listed here talk to their device over StreamDevice (or ship a
protocol file), but they are not in this library. The generic `ioc-streamdevice` image
provides EPICS base 7.0.9 plus `asyn`, `StreamDevice`, `calc`, `std`, `sscan`, `busy`,
`autosave`, `iocStats`, `pvlogging` and the sequencer. Anything else a template needs
(a compiled `sub`/`genSub`/`aSub` routine, a compiled asyn port driver, a module
`.dbd`, a compiled SNL program, the motor record, Hytec or other hardware device
support) must be built into a custom image and wired up with a build-time
`ibek-support` definition instead.

## How a module is admitted

Each template of the module's latest `/dls_sw/prod/R3.14.12.7` release is checked
against the image: every record type, `DTYP`, `SNAM`/`INAM` routine and protocol file
it uses must be provided by the image or the module's own runtime files, and its
`builder.py` must not need a module-specific compiled iocsh command.

- **All templates pass** - the module is a runtime pattern.
- **A majority pass** - the module is a runtime pattern and each failing template is
  marked in the pattern's `*.ibek.support.yaml` header and in its entity model's
  description ("needs a generic IOC built with `<module>`"). See the table
  [Runtime patterns with marked templates](#runtime-patterns-with-marked-templates).
- **Half or fewer pass** - the module is not a runtime pattern and is listed below.

A pattern can drop a failing template instead, when that is a small scripted change
that removes nothing a user needs; its header then records the change.

## Needs compiled routines (`sub` / `genSub` / `aSub`)

The records call C routines compiled into the module's own library and registered by
its `.dbd`. Converting `genSub` to the base `aSub` record does not help: the routine
still has to be linked in.

| Module | Version | Routine(s) |
|---|---|---|
| `FQCRBarcodeCamera` | 2-7 | `AscToDec`, plus a compiled asyn port driver |
| `I400` | 3-6-2 | `i400parse` (the `IC101` template alone is plain stream: 1 of 2) |
| `OXCS700` | 2-22 | `alarmlookupProcess` - the `oxCryo` pattern covers this device family with a DB-only alarm lookup |
| `bronkhorstFlowBus` | 1-5 | `asciiToString10`, `floatToInt`, `intToFloat` |
| `capaNCDT` | 3-4 | `capaNCDTInit` (`INAM`), `capaNCDTProc` |
| `cmsIon` | 4-11 | `UpdateWeekEndTime` (`INAM`), `ResetManualDose`, `RunEndReset`, `ResetTime`, `Check4hrReset`; also MRF event-receiver records |
| `debenOF` | 2-0 | `mySubInit` (`INAM`), `parseStatusString`; also the motor record |
| `digitelSpc` | 1-13 | `versionCheck` |
| `huberChiller` | 1-3 | `alarmCommand`, `controlCommand`, `decodeGeneral`, `decodeLimit`, `setpointCommand` |
| `lakeshore336` | 2-19-1 | `extractFirmwareVersion`, in `lakeshore336-FirmwareVersion.template`, which `lakeshore336.template` always includes |
| `laserPuckPointer` | 2-16 | `isbWrite`, `sendPuckDemand` |
| `mecaRobot` | 1-7 | `copyReadbacksToSetPoints`, `jog`, `moveSampleHolder`, `prepareMoveArray`, `robotPositionParser`, `statusParser` |
| `mitsubishiRobot` | 4-36 | `CmdErrorLookup`, `DecToAsc`, `ErrorLookup`, `LocationLookup`, `LogError`, `Logging`, `PuckLabel`, `Regex`; also a compiled asyn port driver |
| `pfeifferTC400` | 2-5 | `pfeifferErrorCodeParse`, `pfeifferErrorMessageParse`, `pfeifferParamSetVetolistCheck` |
| `picotechPT104` | 2-3 | `pt104_resToT`, `pt104_ucharToUInt` |
| `tecPeltier` | 1-6 | `SNAM` is the `$(CONVERT)` macro, naming a routine from the module's compiled `asubMethods.c` |

Some of these modules also hold templates that do work in the image. They could be
admitted as patterns without their failing templates:

| Module | Failing entity model(s) | Working entity model(s) |
|---|---|---|
| `I400` | `I400` | `IC101` |
| `tecPeltier` | `read_parameter`, `read_channel_parameter`, `write_channel_parameter` | `parameters`, `read_firmware`, `tecPeltier`, `tec1122` |

## Needs a compiled driver or device-configuration command

The asyn port or device is created by an iocsh command compiled into the module's
library; the image's IP and serial ports provide only `asynOctet`.

| Module | Version | Compiled command / support |
|---|---|---|
| `capaNCDT6200` | 1-0 | `capaNCDT6200Config` |
| `delaygen` | 1-2-1dls3 | `drvAsynDG645`; `DTYP "dg535"` |
| `hls` | 2-0 | `HlsDriverCreate`; no template uses `DTYP "stream"` |
| `linkamMotor` | 1-1 | `linkamMDS600Config`; no template uses `DTYP "stream"` |
| `PLV1000` | 1-1 | `PLV1000Config` |
| `queensgate` | 2-2 | compiled asyn motor driver, the motor record, `getPos` |
| `rga` | 4-26 | `MVPlusInit`; `rgaGroupStatusCalc`, `rgaGroupStatusInit` |
| `specsIQE1135` | 0-4 | `specsIQE1135Config` |
| `YLRLasers` | 3-1 | `YLRLaserConfig` (the protocol-only variant is plain stream: 1 of 2) |

## Needs a compiled SNL program or the motor record

| Module | Version | Needs |
|---|---|---|
| `filters` | 2-19-4 | `seq &xiaArrayTable` - `xiaArray` lib, `xiaArraySupport` dbd |
| `hexapod` | 4-13 | the motor record, `DTYP "PMAC-VME"`, the `status` record and compiled aSub routines |
| `hidenRGA` | 1-12 | `seq(sncDegas, ...)` - `hidenRGA` lib, `sncHidenRGA` dbd; compiled aSub routines |
| `pmacCoord` | 1-74 | `drvAsynMotorConfigure`, `pmacAsynCoordCreate` and the tpmac comms port; belongs with a pmac/motor IOC |
| `pmacUtil` | 5-13 | `seq(gather, ...)`, tpmac comms port, motor records, `genSub` parse routines; the `pmac` support covers it |
| `transfocator` | 4-9 | `seq recover`, `transfocatorMask` (1 of 2 templates plain stream) |

## Needs hardware device support

| Module | Version | Needs |
|---|---|---|
| `LC400-OEM` | 1-3 | `npointChannel.template` needs `DTYP "LC400ArrayRead"`/`"LC400ArrayWrite"` and the compiled `aSub` routines `createPeriodicData`, `readWtdataFile`; `npointController.template` alone is plain stream (1 of 2) |
| `jena` | 4-3 | `aoPiezoControl.template` needs `DTYP "Hy8401ip"`/`"Hy8402ao"` (Hytec IP ADC/DAC); `edaMotor.template` needs the motor record and a compiled motor driver; `eda.template` and `edaSimple.template` are plain stream (2 of 4) |
| `ozone` | 2-3 | `ML9810B.db`, its only template, needs `DTYP "Hy8001"` (Hytec VME digital I/O): no template passes |

## Not a device module

| Module | Version | Why |
|---|---|---|
| `asyn` | 4-41dls2 | already in the image; its protocols are test files |
| `streamDevice` | 2-5dls14 | already in the image |
| `BELEKTRONIG_BTC` | 2-0 | case-variant name of the module behind the `belektronig_btc` pattern |
| `FW102` | 1.0 | case-variant name of the module behind the `fw102` pattern |
| `BL05I`, `BL15I-BUILDER`, `BL21I` | 2-95, 26-4, 3-11 | beamline collection modules; their protocols belong to device modules |
| `BR-LLRF`, `RFPGU`, `Thales-RF` | 4-0, 4-0, 6-1-2 | accelerator RF modules: fixed machine PV names, Hytec and MRF timing hardware |
| `CRE-331M` | 1-4-1 | S7 PLC device support, not stream; no `builder.py` |
| `MPS` | 4-4-7 | machine-protection system: Hytec, EtherIP and FINS hardware, compiled routines |
| `insertionDevice` | 6-71 | insertion-device control: `idExclusion8`, Hytec, motor and compiled aSub routines |
| `DLS8515` | 1-0 | installs no templates (`DLS8515DevConfigure` is compiled) |
| `epics-sc-dld-ioc-v1.7`, `epics-twincat-ads` | 1-7dls1sim8, 2-1-0dls1 | install no templates |
| `ZoomLightLevel` | 1-1 | ships no protocol file; its few stream records use another module's `robotPLC.proto` |

## Runtime patterns with marked templates

These patterns work in the generic image except for the templates listed, which load
only in a generic IOC built with the named support. Each is marked in the pattern's
support yaml header and entity model description.

| Pattern | Template(s) | Needs |
|---|---|---|
| `PIpiezo` | `E871-absGrp.template`, `PI-E516.template` | the motor record |
| `d2afe` | `fwVersionCheck.template` | compiled aSub routine `checkFW` |
| `enzLoCuM4` | `enzLoCuM4Readback.template` | `DTYP "Hy8401ip"` (Hytec IP ADC) |
| `eurotherm2k` | `eurothermModbus.template`, `eurothermModbusLoop.template`, `eurothermModbusPV.template` | compiled Modbus asyn driver (`drvModbusAsynConfigure`, `eurothermModbusCtrlConfigure`) |
| `leybold` | `centerN.template`, `coolpak.template` | compiled asyn drivers (`centerNConfig`, `coolpakConfig`) |
| `microlab500` | `microlab500whole.template` | the motor record |
| `mks937a` | `mks937aGauge.template`, `mks937aImgMean.template` | `DTYP "$(aitype=Hy8401ip)"`; compiled aSub routines `mks937aMeanInit`, `mks937aMeanCalc` |
| `mks937b` | `mks937bHy8401.template`, `mks937bImgMean.template` | `DTYP "Hy8401ip"`; compiled aSub routines `mks937bMeanInit`, `mks937bMeanCalc` |
| `strainGauge` | `strainGauge.template` | compiled aSub routine `parseSetpointValue` |
| `yaskawaBARTRobot` | `BARTRobot.db` | compiled aSub routines `DecToAsc`, `GripperState`; compiled FINS asyn driver |
| `currAmp` | `currAmp_ai.template` | `DTYP` is the instance-supplied `$(DTYPE)`, so an instance can name device support the image lacks |

`microlab500` stays in the library although its main template is marked, so in the
plain generic image it provides nothing that loads.

`motomanNX100`'s compiled motor support (`drvAsynMotorConfigure`, `motomanCreate`) is
confined to a builder class with no template, so its four stream templates are all
imported. `dlsCAENels` replaces its `wipeStates` genSubs with `sseq` records, and
`oxCryo` replaces `alarmlookupProcess` with `calcout`/`calc`/`aai`/`subArray` records,
so both run in the generic image with nothing marked.
