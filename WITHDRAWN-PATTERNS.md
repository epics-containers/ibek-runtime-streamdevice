# Withdrawn patterns, and modules the sweep cannot see

Hand-written analysis that [BUILD-TIME-ONLY.md](BUILD-TIME-ONLY.md) cannot carry.

That file is **generated** by `.claude/skills/streamdevice-sweep` in
[builder2ibek](https://github.com/epics-containers/builder2ibek) and is rewritten
whole on every sweep, so anything a sweep cannot rederive has to live here instead.
Three things qualify:

- **Patterns that were shipped and then withdrawn.** The sweep sees the modules and
  reports them as build-time-only like any other, but it has no memory that they were
  once folders in this repo, and it does not name the routines that made them
  unrunnable.
- **What the withdrawals cost.** Which working entity models went with them, so
  re-admitting one later is a self-contained job rather than an archaeology exercise.
- **Modules outside the candidate set.** The sweep seeds from modules carrying a
  protocol file. A module without one is invisible to it, however relevant.

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


## Never a candidate — no protocol file

The sweep seeds from modules containing a `.proto`/`.protocol`, so this one never
reaches the gates at all and will not appear in the generated report.

| Module | Version | Why |
|---|---|---|
| `ZoomLightLevel` | 1-1 | Ships no protocol file (its `ProtocolFiles` is commented out); records are mostly `asynFloat64`/`asynInt32` bindings and the few stream records depend on another module's `robotPLC.proto`. Not self-contained. |

