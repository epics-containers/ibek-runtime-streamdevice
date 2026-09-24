# Streamdevice rescan: changes against `main`

This branch refreshes every pattern from its DLS source module's latest
`/dls_sw/prod/R3.14.12.7` release, adds the StreamDevice modules that pass the runtime
gate and are not on `main`, and removes the three patterns that fail it. Hand-shaped
patterns (`currAmp`, `eurotherm2k`, `fw102`, `gardasoftLED`, `microlab500`, `ODPsu`,
`oxCryo`) keep their hand work, with the release's other files merged in.

The table has one row per pattern folder that differs from `main`: 11 new,
90 changed, 3 removed (104 rows). Folders not listed are byte-identical to `main`
apart from the annotation strip described below. **Source** is the DLS module and
release the folder is imported from. **What changed** is relative to `main`; **Why** names the rule or
decision behind it; **Flag** is what to look at: a template marked as needing more
than the generic image, an upstream defect carried as-is, a patch or trim of an
upstream file, or a change that breaks an existing `ioc.yaml`.

Terms used below: *marked* templates need a generic IOC built with extra support (see
[BUILD-TIME-ONLY.md](BUILD-TIME-ONLY.md)); *docs/sim/test* are upstream extras stored
in the folder but not vendored (the folder's `ibek.manifest.yaml` vendors only the
runtime files); *.req* files are autosave request files generated from the templates'
`# % autosave` tags.

Every folder's databases also have their DLS `gui`/`gdatag`/`gda` annotation comments
stripped by [`strip-dls-annotations.py`](../strip-dls-annotations.py) (see the README).
Record content is unchanged; the rows below do not repeat this.

## Changes that break an existing `ioc.yaml`

An instance picks these up only when it moves its pin to a release containing them.

- **`name` parameter removed** wherever no template uses it (hard rule). An `ioc.yaml`
  that sets `name:` on these entities fails validation with *Extra inputs are not
  permitted*; delete the line. Patterns: `agilent33220A`, `agilent4UHV`, `agilent53220`, `agilentTurboPump`, `alicatGasFlow`, `APD-ACE`, `attocube`, `attocubeInterf`, `axisCameraControl`, `belektronig_btc`, `caenN1470`, `chemyxFusion`, `chillax`, `cognexDataMan100`, `CrateMonitor`, `CryoconM14`, `cyberstar`, `digitelMpc`, `EdwardsNextTurbo`, `EdwardsRangeGauge`, `EdwardsScroll`, `elmitecLEEM`, `enzLoCuM4`, `ETLdetector`, `fw102`, `gardasoftLED`, `GR150`, `gssExplorIR`, `harvardSyringe`, `keithley2400`, `keithley2600`, `Keithley6487`, `KeithleyDMM6500`, `keysight33500B`, `knauer`, `kriIonBeam`, `lakeshore218`, `lakeshore331`, `lakeshore340`, `laudaRE2xx`, `leyboldCenterOne`, `linkam`, `microlab500`, `mks937a`, `mks937b`, `newstep`, `norhofLN2`, `omegaIR2C`, `OxInstCryojet`, `OxInstIPS`, `PIpiezo`, `pr4000`, `SierraInstMassFlowMeters`, `specsVCU1000`, `SQC-310`, `SycosH-Hot`, `tdklambda`, `thermocube`, `thorlabsMcls1`, `VatLeakValve590`, `VCH10Light`, `vici`, `watson-marlow`, `WS300scale`, `zaber_T-LSR`.
- **Other parameters removed** (each used only in template comments; accepted as
  consumer breaks and tracked in [ibek#377](https://github.com/epics-containers/ibek/issues/377),
  except `IPADDR`, whose asyn port the instance creates itself):
  - `attocubeInterf` `ids3010`: `label1`, `label2`, `label3` removed
  - `axisCameraControl` `axisCameraControl`: `IPADDR` removed
  - `CryoconM14` `M14_sensor`: `desc` removed
  - `gssExplorIR` `explorir`: `SCAN` removed
  - `harvardSyringe` `harvardSyringe`: `desc` removed
  - `lakeshore218` `lakeshore218`: `lakeshore218Path` removed
  - `laudaRE2xx` `lIntegralT`: `DESC` removed
  - `laudaRE2xx` `lMCxxx`: `DESC` removed
  - `laudaRE2xx` `lRE2xx`: `DESC` removed
  - `laudaRE2xx` `lVariocool`: `DESC` removed
  - `OxInstIPS` `OxInstIPS`: `desc` removed
  - `PIpiezo` `E816`: `DESC` removed
  - `pr4000` `pr4000`: `ch1pv`, `ch2pv` removed
  - `stanford` `sr570`: `DESC` removed
  - `thorlabsMcls1` `thorlabsMcls1`: `desc` removed
  - `VCH10Light` `VCH10Light`: `shortdesc` removed
- **Parameter retyped**:
  - `elmitecLEEM` `leemPSValue.SCAN` int->str (default `10 second`; an instance setting `SCAN: 10` must write `10 second`)
- **Patterns removed**: `LC400-OEM`, `jena`, `ozone`. An instance vendoring any of
  these keeps working at its pinned release; to move on it needs a generic IOC built
  with the module.

## Pattern changes

| Module | Status | Source | What changed vs main | Why | Flag |
|---|---|---|---|---|---|
| `agilent33220A` | CHANGED | agilent33220A 1-7 | docs/ (2 files); sim/ (1 file); +1 .req; `name` param removed (`agilent33220A`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `agilent4UHV` | CHANGED | agilent4UHV 0-1 | `name` param removed (`_agilent4UHVIonpTemplate`, `_agilent4UHVTemplate`, `agilent4UHV`, `agilent4UHVIonp`) | no template uses `name` (hard rule) | consumer break: `name` |
| `agilent53220` | CHANGED | agilent53220 1-3-4 | +1 .req; `name` param removed (`agilent53220`) | autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `agilentE364xA` | CHANGED | agilentE364xA 1-2-1 | +1 template(s); +entities `caputcallback` | release templates not covered on main | - |
| `agilentTurboPump` | CHANGED | agilentTurboPump 2-1 | `name` param removed (`twisTorr305FS`, `twisTorr305IC`) | no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `alicatGasFlow` | CHANGED | alicatGasFlow 2-15 | docs/ (1 file); sim/ (3 files); test/ (1 file); +3 .req; `name` param removed (`alicatGasFlow`, `alicatMassCtrl`, `alicatPressureCtrl`); source 2-14 -> 2-15: `getGasLong` protocol, `GASNAMEPROTOCOL` param (default `getGas`) | newer prod release; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `ametekLockIn` | CHANGED | ametekLockIn 1-17special2 | sim/ (1 file) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `APD-ACE` | CHANGED | APD-ACE 2-3 | +1 .req; `name` param removed (`APDACE`) | `getIntRate` protocol from the prod release; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `attocube` | CHANGED | attocube 1-8 | sim/ (1 file); `name` param removed (`ANC150`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `attocubeInterf` | CHANGED | attocubeInterf 2-1 | docs/ (2 files); `name` param removed (`ids3010`); `ids3010` params removed: `label1`, `label2`, `label3`; databases args give comment-only macros an empty value (`label1`, `label2`, `label3`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); used only in template comments; no `macLib: macro ... is undefined` at boot | consumer break: `name`; consumer break: dropped `label1`, `label2`, `label3` |
| `axisCameraControl` | CHANGED | axisCameraControl 2-4 | `name` param removed (`axisCameraControl`); `axisCameraControl` params removed: `IPADDR` | no template uses `name` (hard rule); used only in template comments (or only for builder.py's own asyn port) | consumer break: `name`; consumer break: `IPADDR` (connection params are the instance's asyn port, per ruling) |
| `belektronig_btc` | CHANGED | belektronig_btc 2-2 | `name` param removed (`belektronig_btc`) | no template uses `name` (hard rule) | consumer break: `name` |
| `caenN1470` | CHANGED | caenN1470 1-4 | docs/ (1 file); +2 .req; `name` param removed (`_caenN1470`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `CanberraG64` | NEW | CanberraG64 1-7 | 1 template, 1 protocol file(s); entities `CanberraG64` | StreamDevice module that passes the runtime gate, not on main | - |
| `celerotonChopper` | CHANGED | celerotonChopper 1-1 | `DRVH`/`DRVL` dropped from one `ai` record; sim/ (2 files); header lists the change | not `ai` fields: EPICS 7 rejects the file; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | scripted trim of the upstream template |
| `chemyxFusion` | CHANGED | chemyxFusion 1-0 | `name` param removed (`Fusion4000`); sim/ (1 file) | no template uses `name` (hard rule); publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | consumer break: `name` |
| `chillax` | CHANGED | chillax 2-3-1 | `name` param removed (`_chillaxOpiTemplate`, `chillaxController`) | no template uses `name` (hard rule) | consumer break: `name` |
| `cognexDataMan100` | CHANGED | cognexDataMan100 1-2 | docs/ (1 file); `name` param removed (`dataman100`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `Compax3` | CHANGED | Compax3 0-2 | header: records that `Compax3.proto` ships as `compax3.protocol` | provenance header must describe the stored files | - |
| `CrateMonitor` | CHANGED | CrateMonitor 2-4 | sim/ (1 file); test/ (1 file); `name` param removed (`CrateMonitor`); `CrateMonitor.template` refreshed: `:ALARM` sums `STATUS6.SEVR` in place of `STA:TEMP.SEVR`/`STA:FAN.SEVR` | main tracked an unreleased work copy; source is now the 2-4 release; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | `:ALARM` inputs differ from main (upstream 2-4 content); consumer break: `name` |
| `CryoconM14` | CHANGED | CryoconM14 2-2 | sim/ (1 file); `name` param removed (`M14_sensor`); `M14_sensor` params removed: `desc`; provenance header | main tracked an unreleased work copy; source is now the 2-2 release; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); used only in template comments | consumer break: `name`; consumer break: dropped `desc` |
| `CryoconM32` | CHANGED | CryoconM32 1-7 | +2 template(s); +entities `CryoconM32_control`, `CryoconM32_sensor`; docs/ (1 file); sim/ (1 file); test/ (1 file) | control/sensor templates of the release not covered on main (entities keep builder class names); publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | upstream: `STS:SINKTEMP` has a stream INP but no DTYP |
| `currAmp` | CHANGED | currAmp 1-45 | sim/ (new, 3 files: `YMCS0009_sim.template`, `YMCS0012_sim.template`, `currAmp_ai_sim.template`); +`ibek.manifest.yaml` (new, needed once sim/ exists) | three `_sim` templates imported per Q1 (load); publishable upstream extra, kept out of vendoring by the new `ibek.manifest.yaml` | new files only - no existing `currAmp` file touched, to keep the unmerged `I03-1110` branch's edits to this pattern mergeable |
| `cyberstar` | CHANGED | cyberstar 2-3-1 | `name` param removed (`CBY_2206`) | no template uses `name` (hard rule) | consumer break: `name` |
| `d2afe` | NEW | d2afe 0-1 | 10 templates, 1 protocol file(s); entities `attenuator_cmd`, `attenuators_set_fan`, `cal_table`, `d2afeStatus`, `d2ptg`, `d2ptg_cal_scan_list` +4 more | StreamDevice module that passes the runtime gate, not on main | marked non-image: `fwVersionCheck.template` (compiled `checkFW`); storage-ring specific (builder hard-codes `SR{cell}C-DI-...`); `CELL`, `D2AFE_MASK` typed int per builder.py |
| `digitelMpc` | CHANGED | digitelMpc 6-24 | +2 template(s); +1 protocol file(s); +entities `digitelMpcIonpSps`, `digitelMpcTspDummy`; docs/ (1 file); sim/ (3 files, +2 `simulation_digitelMpc.template`/`simulation_digitelMpcTsp.template`); header notes `simulation_digitelMpcIonp.template` not imported; `name` param removed (`_digitelMpcIonpTemplate`, `digitelMpc`, `digitelMpcIonp`, `digitelMpcTsp` +1 more) | release templates not covered on main; two `_sim`/`simulation_*` templates imported per Q1 (load); `simulation_digitelMpcIonp.template` not imported - `pressRanProcess`/`pressRanInit` are not registered in the generic image; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | upstream: nothing marked; `digitelMpcIonpSps`/`digitelMpcTspDummy` keep template-stem entity names; consumer break: `name` |
| `dlsCAENels` | NEW | dlsCAENels 2-6 | 3 templates, 1 protocol file(s); entities `dlsCAENels`, `dlsCAENelsChannel`, `dlsCAENelsGroup`; sim/ (3 files); test/ (2 files) | `wipeStates` genSubs replaced by `sseq` records that write the same constant; nothing marked; StreamDevice module that passes the runtime gate, not on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `EdwardsNextTurbo` | CHANGED | EdwardsNextTurbo 3-4 | docs/ (2 files); +1 .req; `name` param removed (`EdwardsNextTurbo`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `EdwardsRangeGauge` | CHANGED | EdwardsRangeGauge 23-4 | `name` param removed (`EdwardsRangeGauge`) | no template uses `name` (hard rule) | consumer break: `name` |
| `EdwardsScroll` | CHANGED | EdwardsScroll 1-15 | +1 template(s); +entities `EdwardsScroll_SerialOnOffExtra`; docs/ (1 file); `name` param removed (`EdwardsScroll`) | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `elmitecLEEM` | CHANGED | elmitecLEEM 1-7 | +2 .req; `name` param removed (`leem`, `leemPSValue`); `leemPSValue.SCAN` is `str`, default `10 second` | the template default is `10 second`; the int `10` rendered an illegal SCAN; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `SCAN` int -> str (an instance setting `SCAN: 10` must write `10 second`); consumer break: `name` |
| `enzLoCuM4` | CHANGED | enzLoCuM4 2-42 | +4 template(s); +entities `enzLoCuM4Readback`, `enzLoCuM4Readback_generic_diagonal`, `enzLoCuM4Readback_generic_vertical`; docs/ (1 file); sim/ (2 files, +1 `simulation_enzLoCuM4.template`); test/ (1 file); `name` param removed (`enzLoCuM4`); header lists the scripted include-name and CALC-paren fixes to `enzLoCuM4Readback_generic_diagonal.template` | Readback templates of the release not covered on main; `simulation_enzLoCuM4.template` imported per Q1 (loads); EPICS 7 rejects the unfixed file; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | marked non-image: `enzLoCuM4Readback.template` (`DTYP Hy8401ip`); consumer break: `name` |
| `ETLdetector` | CHANGED | ETLdetector 1-21 | +1 template(s); +entities `ETLdetectorDebug`; sim/ (3 files, +1 `ETLdetector_sim.template`); +1 .req; `name` param removed (`ETLdetector`) | release templates not covered on main; `_sim` template imported per Q1 (loads); publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `eurotherm2k` | CHANGED | eurotherm2k 2-10 | +6 template(s); 1 template(s) refreshed; +entities `eurothermConfParam`, `eurothermModbus`, `eurothermModbusLoop`, `eurothermModbusPV`, `eurothermPV`, `eurothermParam`; docs/ (3 files); sim/ (1 file); test/ (1 file); +2 .req; provenance header | hand-written `eurotherm2k` entity kept; other release templates added; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates | marked non-image: 3 Modbus templates (compiled Modbus driver); hand-written entity defaults `EGU` `C/min`, `SPMAX` 100 differ from the template defaults (as on main) |
| `eurotherm903` | CHANGED | eurotherm903 1-9-2 | +1 .req | autosave tags in the templates | - |
| `fw102` | CHANGED | fw102 2-1 | `name` param removed (`_fw102Template`); header records the one-line `setPos` protocol change (reads the device echo) | provenance header must describe the stored files; no template uses `name` (hard rule) | protocol deviates from upstream by one line (as on main); consumer break: `name` |
| `gardasoftLED` | CHANGED | gardasoftLED 2-13 | docs/ (1 file); sim/ (1 file); test/ (1 file); +6 .req; `name` param removed (`gardasoftLED420`, `gardasoftLED820`, `gardasoftLEDRTSeries`); `PP600SeriesChannel.template`: `@gardasoft.protocol` -> `@PP600Series.protocol` in `SETMODE`/`SETOUTPUT` (scripted, in header) | upstream bug: no release of the module ships `gardasoft.protocol`; builder.py's `ProtocolFiles` for both PP600 classes is `PP600Series.protocol`, which defines `setMode($1)` and `setOutput($1,$2)` with the same arguments the records pass; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | patched upstream template (evidence in Why); consumer break: `name` |
| `GR150` | CHANGED | GR150 2-5-5 | sim/ (2 files, +1 `simulation_gr150.template`); `name` param removed (`gr150`) | `simulation_gr150.template` imported per Q1 (loads; `transform` records not load-validated by the softIoc harness); publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `granvillePhillips` | CHANGED | granvillePhillips 2-10 | +10 template(s); +entities `gp307Gauge`, `gp307Hcg`, `gp307HcgDummy`, `gp307Pirg`, `gp307PirgDummy`, `gp350Gauge` +4 more; sim/ (2 files) | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no `macLib: macro ... is undefined` at boot | - |
| `gssExplorIR` | CHANGED | gssExplorIR 1-2 | `name` param removed (`explorir`); `explorir` params removed: `SCAN` | no template uses `name` (hard rule); used only in template comments | consumer break: `name`; consumer break: dropped `SCAN` |
| `harvardSyringe` | CHANGED | harvardSyringe 1-12 | sim/ (1 file); `name` param removed (`harvardSyringe`); `harvardSyringe` params removed: `desc`; 2 `DESC` strings shortened to 40 characters; header lists the change | EPICS 7 rejects longer `DESC`; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); used only in template comments | scripted trim of the upstream template; consumer break: `name`; consumer break: dropped `desc` |
| `HostLink` | CHANGED | HostLink 3-3 | sim/ (1 file); test/ (1 file) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `ip` | NEW | ip 4-5 | 1 template, 1 protocol file(s); entities `SR830`; docs/ (12 files) | StreamDevice module that passes the runtime gate, not on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `isegHVPSU` | CHANGED | isegHVPSU 2-1 | +1 template(s); +entities `trigger_process`; sim/ (1 file); +2 .req | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates | - |
| `jena` | REMOVED | jena 4-3 | pattern removed (4 templates, protocol, support yaml) | half its templates need Hytec IP I/O or the motor record: no runtime-able majority (see BUILD-TIME-ONLY.md) | consumer break: any instance vendoring `jena` must move to a generic IOC built with the module |
| `keithley2400` | CHANGED | keithley2400 1-23 | docs/ (1 file); +2 .req; `name` param removed (`Keithley2400`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `keithley2600` | CHANGED | keithley2600 2-3 | docs/ (1 file); `name` param removed (`keithley2600chan`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `Keithley6487` | CHANGED | Keithley6487 1-1dls8 | docs/ (4 files); `name` param removed (`Keithley6487`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `KeithleyDMM6500` | CHANGED | KeithleyDMM6500 1-1 | docs/ (1 file); `name` param removed (`dmm6500`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `keysight33500B` | CHANGED | keysight33500B 1-6 | +2 .req; `name` param removed (`keysight33500Bchan`) | autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `keysightLCR` | CHANGED | keysightLCR 0-2 | +1 .req | autosave tags in the templates | - |
| `knauer` | CHANGED | knauer 0-6 | +1 template(s); +entities `ConnectionManagement`; docs/ (1 file); sim/ (2 files); `name` param removed (`Azura21S`, `BlueShadow40P`); `docs/doxygen/manual` without its internal share path | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `kriIonBeam` | CHANGED | kriIonBeam 3-1 | `name` param removed (`Autocontroller`, `KaufmanSourceController`, `ProgramParameters`) | no template uses `name` (hard rule) | consumer break: `name` |
| `lakeshore218` | CHANGED | lakeshore218 2-9 | +1 .req; `name` param removed (`lakeshore218`); `lakeshore218` params removed: `lakeshore218Path` | autosave tags in the templates; no template uses `name` (hard rule); used only in template comments; no `macLib: macro ... is undefined` at boot | consumer break: `name`; consumer break: dropped `lakeshore218Path` |
| `lakeshore224` | CHANGED | lakeshore224 0-6 | docs/ (1 file) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `lakeshore331` | CHANGED | lakeshore331 1-13 | +1 .req; `name` param removed (`lakeshore331`) | autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `lakeshore340` | CHANGED | lakeshore340 2-6 | sim/ (1 file); test/ (2 files); +1 .req; `name` param removed (`lakeshore340`); `test/` without the empty log file | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `laudaRE2xx` | CHANGED | laudaRE2xx 2-9-9 | +1 template(s); +1 protocol file(s); +entities `lRE2xx_RS485`; sim/ (1 file); +5 .req; `name` param removed (`lIntegralT`, `lMCxxx`, `lRE2xx`, `lVariocool`); `lIntegralT` params removed: `DESC`; `lMCxxx` params removed: `DESC`; `lRE2xx` params removed: `DESC`; `lVariocool` params removed: `DESC` | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); used only in template comments; no `macLib: macro ... is undefined` at boot | consumer break: `name`; consumer break: dropped `DESC`; consumer break: dropped `DESC`; consumer break: dropped `DESC`; consumer break: dropped `DESC` |
| `LC400-OEM` | REMOVED | LC400-OEM 1-3 | pattern removed (template, protocol, support yaml) | half its templates need compiled npoint support: no runtime-able majority (see BUILD-TIME-ONLY.md) | consumer break: any instance vendoring `LC400-OEM` must move to a generic IOC built with the module |
| `leybold` | NEW | leybold 2-2 | 12 templates, 1 protocol file(s), 5 .req; entities `centerN`, `coolpak`, `read_floatE`, `read_float_float_float`, `read_int`, `read_int_floatE` +6 more; sim/ (4 files) | StreamDevice module that passes the runtime gate, not on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | marked non-image: `centerN.template`, `coolpak.template` (compiled asyn drivers); upstream: `read_floatE` calls protocol `get_floatE`, which `leybold.proto` does not define |
| `leyboldCenterOne` | CHANGED | leyboldCenterOne 1-1 | +1 template(s); +1 .req; `name` param removed (`centerOne`); `centerOne.db` replaced by the release's template | refreshed from the source release; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `linkam` | CHANGED | linkam 2-15 | sim/ (1 file); `name` param removed (`linkam`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `macroSensors` | CHANGED | macroSensors 2-0 | +1 .req; `OFF` param key quoted | an unquoted `OFF:` key parses as YAML boolean; autosave tags in the templates | - |
| `microlab500` | CHANGED | microlab500 1-5 | docs/ (1 file); sim/ (1 file); `name` param removed (`microlab500`); provenance header | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | marked non-image: `microlab500whole.template` (motor record) - its only entity; consumer break: `name` |
| `millik` | CHANGED | millik 1-2 | support yaml only | refreshed from the source release | - |
| `mks647c` | CHANGED | mks647c 0-1-4 | sim/ (1 file) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `mks937a` | CHANGED | mks937a 2-97 | +12 template(s); +entities `mks937aGauge`, `mks937aGaugeGroup`, `mks937aImg`, `mks937aImgDummy`, `mks937aImgGroup`, `mks937aImgMean` +6 more; docs/ (2 files); sim/ (3 files, +2 `simulation_mks937a.template`/`simulation_mks937aGauge.template`); test/ (1 file); +1 .req; `name` param removed (`mks937a`); provenance header extended: `simulation_mks937aImg.template`/`simulation_mks937aPirg.template` not imported | release templates not covered on main; two `simulation_*` templates imported per Q1 (load); `simulation_mks937aImg.template`/`simulation_mks937aPirg.template` not imported - `pressRanProcess`/`pressRanInit` are not registered in the generic image; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | marked non-image: `mks937aGauge.template` (`Hy8401ip`), `mks937aImgMean.template` (compiled aSub); consumer break: `name` |
| `mks937b` | CHANGED | mks937b 2-98 | +17 template(s); +entities `mks937bCap`, `mks937bFastRelay`, `mks937bGauge`, `mks937bGaugeGroup`, `mks937bHcg`, `mks937bHcgGroup` +11 more; docs/ (3 files); sim/ (2 files); test/ (1 file); +1 .req; `name` param removed (`mks937b`); source 2-97 -> 2-98 | newer prod release; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | marked non-image: `mks937bHy8401.template` (`Hy8401ip`), `mks937bImgMean.template` (compiled aSub); consumer break: `name` |
| `motomanNX100` | NEW | motomanNX100 1-17-1 | 4 templates, 1 protocol file(s); entities `nx100`, `nx100dvar`, `nx100io`, `nx100pvar`; docs/ (2 files); sim/ (1 file); test/ (1 file); `docs/doxygen/manual` without its internal share path | compiled motor support sits in a builder class with no template; StreamDevice module that passes the runtime gate, not on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `newstep` | CHANGED | newstep 2-6 | +1 .req; `name` param removed (`NSC200`) | autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `norhofLN2` | CHANGED | norhofLN2 2-3 | +2 .req; sim/ (new, 1 file: `norhofLN2_sim.template`); +`ibek.manifest.yaml` (new, needed once sim/ exists); `name` param removed (`norhofLN2`) | autosave tags in the templates; `norhofLN2_sim.template` imported per Q1 (loads; `asyn` record not load-validated by the softIoc harness); publishable upstream extra, kept out of vendoring by the new `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `ODPsu` | CHANGED | ODPsu 3-2 | docs/ (1 file); test/ (1 file); +1 .req | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates | unmerged `I03-1087` branch also touches this pattern |
| `omegaIR2C` | CHANGED | omegaIR2C 1-5 | `name` param removed (`omegaIR2C`) | no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `oxCryo` | CHANGED | OXCryo 1-4 | +2 template(s); +4 .req; templates are the VDCT-derived msi hierarchy (`OXcommon`, `OXcommonCB` include targets); the `ALARM` genSub is replaced by DB-only `ALARM_INDEX`/`ALARM_SEVR`/`ALARM_TABLE`/`ALARM` records | genSub and `alarmlookupProcess` are not in the image; DB-only lookup verified against the C routine; autosave tags in the templates | clients reading `:ALARM.VALA` must read `:ALARM` or use ioc-oxcryo; upstream: `OXPH700`/`OXCB700` protocols redirect into records their templates lack |
| `OxInstCryojet` | CHANGED | OxInstCryojet 2-28 | +3 template(s); +1 protocol file(s); +entities `ILM201`, `ITC4`, `MercuryiTC_SCPI`; sim/ (2 files); test/ (1 file); +4 .req; `name` param removed (`cryojet`); `cryojetITC503S_settings.req` lists only records that exist (commented-out `SAMPLEFLW:SET`/`SHIELDFLW:SET` left out) | ITC4, ILM201 and MercuryiTC SCPI templates of the release not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule) | consumer break: `name` |
| `OxInstIPS` | CHANGED | OxInstIPS 2-0 | docs/ (3 files); sim/ (1 file); test/ (1 file); +1 .req; `name` param removed (`OxInstIPS`); `OxInstIPS` params removed: `desc` | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); used only in template comments | consumer break: `name`; consumer break: dropped `desc` |
| `ozone` | REMOVED | ozone 2-3 | pattern removed (1 template, support yaml) | its only template needs `DTYP "Hy8001"` (Hytec VME digital I/O): no runtime-able majority (see BUILD-TIME-ONLY.md) | consumer break: any instance vendoring `ozone` must move to a generic IOC built with the module |
| `PIpiezo` | CHANGED | PIpiezo 1-23 | +4 template(s); +entities `E871-absGrp`, `E871-relGrp`, `PI-E516`, `actuatorcallback`; docs/ (1 file); sim/ (3 files); +5 .req; `name` param removed (`E725`, `E816`, `E871`); `E816` params removed: `DESC`; provenance header | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); used only in template comments; no `macLib: macro ... is undefined` at boot | marked non-image: `E871-absGrp.template`, `PI-E516.template` (motor record); upstream: `C877` `REF:MODE` has a stream INP but no DTYP; consumer break: `name`; consumer break: dropped `DESC` |
| `pr4000` | CHANGED | pr4000 3-2 | docs/ (1 file); `name` param removed (`pr4000`); `pr4000` params removed: `ch1pv`, `ch2pv`; databases args give comment-only macros an empty value (`domain`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); used only in template comments; no `macLib: macro ... is undefined` at boot | consumer break: `name`; consumer break: dropped `ch1pv`, `ch2pv` |
| `QPC` | CHANGED | QPC 2-3 | +1 template(s); +entities `digitelQpcIonp`; docs/ (2 files); sim/ (1 file); databases args give comment-only macros an empty value (`PMP`, `SYSTEM`, `controller`); `SPLY`/`SPT` are `int`, rendered 2-digit through databases args (`'%02d' \| format(...)`), as builder.py does; `docs/test_cmds.txt` | builder.py types `SPLY`/`SPT` int and formats them `%02d`; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no `macLib: macro ... is undefined` at boot | - |
| `SierraInstMassFlowMeters` | CHANGED | SierraInstMassFlowMeters 1-0 | `name` param removed (`SierraInstMassFlowMeters`) | no template uses `name` (hard rule) | consumer break: `name` |
| `smc` | NEW | smc 1-8 | 3 templates, 1 protocol file(s), 2 .req; entities `magnet`, `smc`, `smcTripleAxis`; docs/ (2 files); sim/ (1 file: `simulation_magnet.template`) | StreamDevice module that passes the runtime gate, not on main; `simulation_magnet.template` imported per Q1 (loads; `transform` records not load-validated by the softIoc harness); publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `specsEBE` | CHANGED | specsEBE 0-7 | docs/ (1 file); sim/ (7 files); +1 .req | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates | - |
| `specsVCU1000` | CHANGED | specsVCU1000 1-9-2 | docs/ (3 files); sim/ (1 file); `name` param removed (`specsVCU1000`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `SQC-310` | CHANGED | SQC-310 0-2 | docs/ (2 files); `name` param removed (`SQC310`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `stanford` | CHANGED | stanford 2-7 | +1 template(s); +entities `dummy_stanford_ai`; sim/ (1 file); +1 .req; `sr570` params removed: `DESC` | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; used only in template comments; no `macLib: macro ... is undefined` at boot | consumer break: dropped `DESC` |
| `stanfordDG645` | CHANGED | stanfordDG645 1-3 | docs/ (1 file); sim/ (1 file) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `strainGauge` | NEW | strainGauge 2-9 | 3 templates, 2 protocol file(s); entities `motorInit`, `strainGauge`, `strainGaugeOmegaPt`; sim/ (1 file); test/ (1 file) | StreamDevice module that passes the runtime gate, not on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | marked non-image: `strainGauge.template` (genSub -> aSub, compiled `parseSetpointValue`) |
| `SycosH-Hot` | CHANGED | SycosH-Hot 1-8 | sim/ (1 file); `name` param removed (`SycosH_Hot`) | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule) | consumer break: `name` |
| `tdklambda` | CHANGED | tdklambda 1-6 | `name` param removed (`Gen3300w`) | no template uses `name` (hard rule) | consumer break: `name` |
| `tenmaPSU` | CHANGED | tenmaPSU 0-4-3 | +1 .req; source 0-4-2 -> 0-4-3 (header only; files identical) | newer prod release; autosave tags in the templates | - |
| `thermocube` | CHANGED | thermocube 1-0 | `name` param removed (`thermoCube`); sim/ (1 file) | no template uses `name` (hard rule); publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | consumer break: `name` |
| `thorlabsMcls1` | CHANGED | thorlabsMcls1 0-4 | sim/ (3 files); `name` param removed (`thorlabsMcls1`); `thorlabsMcls1` params removed: `desc` | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; no template uses `name` (hard rule); used only in template comments; no `macLib: macro ... is undefined` at boot | consumer break: `name`; consumer break: dropped `desc` |
| `ttiCPX` | CHANGED | ttiCPX 3-0 | docs/ (1 file); +1 template(s); +entities `ttiCPXChannel`; +1 .req | publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; release templates not covered on main; autosave tags in the templates; no `macLib: macro ... is undefined` at boot | - |
| `ttiEX355P` | NEW | ttiEX355P 2-0 | 1 template, 1 protocol file(s), 1 .req; docs/ (1 file); entities `ttiEX355P` | StreamDevice module that passes the runtime gate, not on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml` | - |
| `ttiMX` | NEW | ttiMX 1-5 | 2 templates, 1 protocol file(s), 1 .req; entities `ttiMX_channel`, `ttiMX_general` | StreamDevice module that passes the runtime gate, not on main | - |
| `twickenhamHDI` | NEW | twickenhamHDI 2-3 | 1 template, 1 protocol file(s); entities `twickenhamHDI` | StreamDevice module that passes the runtime gate, not on main | - |
| `VatLeakValve590` | CHANGED | VatLeakValve590 1-5 | +1 .req; `name` param removed (`VatLeakValve590series`, `_VatLeakValve590seriesTemplate`); source corrected to 1-5 (the newest release; `1.1` sorted after it by name); protocol refreshed; template = 1-5 plus scripted EPICS 7 load fixes listed in the header | provenance header must describe the stored files; 1-5 is the latest release; autosave tags in the templates; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | record set differs from main: 1-5 adds the `HOLD` and `POSITIONLIMIT` records; consumer break: `name` |
| `VCH10Light` | CHANGED | VCH10Light 1-1 | `name` param removed (`VCH10Light`); `VCH10Light` params removed: `shortdesc` | no template uses `name` (hard rule); used only in template comments | consumer break: `name`; consumer break: dropped `shortdesc` |
| `vici` | CHANGED | vici 1-14 | +5 template(s); +entities `eightGasSelect`, `fourGasSelect`, `sixteenGasSelect_2EMT_1E2CA`, `sixteenGasSelect_2EMT_1VALVE`, `viciEMT_dummy`; sim/ (2 files); +5 .req; `name` param removed (`viciE2CA`, `viciEMT`, `viciEUTA`, `viciUM`) | release templates not covered on main; publishable upstream extras, kept out of vendoring by `ibek.manifest.yaml`; autosave tags in the templates; no template uses `name` (hard rule); no `macLib: macro ... is undefined` at boot | consumer break: `name` |
| `watson-marlow` | CHANGED | watson-marlow 1-5 | `name` param removed (`Pump323Du`) | no template uses `name` (hard rule) | consumer break: `name` |
| `WS300scale` | CHANGED | WS300scale 1-5 | `name` param removed (`WS300`) | no template uses `name` (hard rule) | consumer break: `name` |
| `yaskawaBARTRobot` | CHANGED | yaskawaBARTRobot 0-1-I22-ONLY | +3 template(s); 7 template(s) refreshed; +entities `BARTRobot`, `yaskawa`, `yaskawaReal`; +2 .req; `DISV` `str` (`"64"`) on every entity, `yaskawaReal` `DRVL`/`DRVH` `str`, as builder.py types them | source is the newest prod release; genSub -> aSub; autosave tags in the templates | source is the beamline-named release `0-1-I22-ONLY` (user decision, for now); marked non-image: `BARTRobot.db` (compiled `DecToAsc`/`GripperState`, FINS) |
| `zaber_T-LSR` | CHANGED | zaber_T-LSR 2-0 | `name` param removed (`Zaber_T_LSR`) | no template uses `name` (hard rule) | consumer break: `name` |

## Modules considered and left out

Each module below ships a StreamDevice protocol in its latest DLS release but is not
a pattern. [BUILD-TIME-ONLY.md](BUILD-TIME-ONLY.md) has the detail.

- `FQCRBarcodeCamera`: compiled `AscToDec` routine and asyn driver
- `I400`: compiled `i400parse` routine (1 of 2 templates plain stream)
- `OXCS700`: compiled `alarmlookupProcess`; the `oxCryo` pattern covers the device family
- `bronkhorstFlowBus`: compiled conversion routines
- `capaNCDT`: compiled `capaNCDTInit`/`capaNCDTProc` routines
- `cmsIon`: compiled routines and MRF event-receiver records
- `debenOF`: compiled routines and the motor record
- `digitelSpc`: compiled `versionCheck` routine
- `huberChiller`: compiled command/decode routines
- `lakeshore336`: compiled `extractFirmwareVersion`, included by the main template
- `laserPuckPointer`: compiled `isbWrite`/`sendPuckDemand` routines
- `mecaRobot`: compiled aSub routines
- `mitsubishiRobot`: compiled lookup/logging routines and asyn driver
- `pfeifferTC400`: compiled error-parse routines
- `picotechPT104`: compiled conversion routines
- `tecPeltier`: compiled `asubMethods.c` routines (4 working entity models could be admitted alone)
- `capaNCDT6200`: compiled `capaNCDT6200Config` driver
- `delaygen`: compiled `drvAsynDG645` driver and `dg535` device support
- `hls`: compiled `HlsDriverCreate` driver; no stream records
- `linkamMotor`: compiled `linkamMDS600Config` driver; no stream records
- `PLV1000`: compiled `PLV1000Config` driver
- `queensgate`: compiled asyn motor driver and the motor record
- `rga`: compiled `MVPlusInit` driver and routines
- `specsIQE1135`: compiled `specsIQE1135Config` driver
- `YLRLasers`: compiled `YLRLaserConfig` driver (1 of 2 variants plain stream)
- `filters`: compiled SNL program `xiaArrayTable`
- `hexapod`: motor record, PMAC-VME and compiled routines
- `hidenRGA`: compiled SNL program and aSub routines
- `pmacCoord`: tpmac comms port and compiled motor driver; belongs with a pmac/motor IOC
- `pmacUtil`: compiled SNL `gather`, tpmac comms port, motor records; covered by `pmac`
- `transfocator`: compiled SNL program and `transfocatorMask` routine
- `LC400-OEM`: npoint array device support and compiled routines on half its templates (removed from the library)
- `jena`: Hytec IP I/O and the motor record on half its templates (removed from the library)
- `ozone`: `DTYP "Hy8001"` (Hytec VME digital I/O) on its only template (removed from the library)
- `asyn`: already in the generic image
- `streamDevice`: already in the generic image
- `BELEKTRONIG_BTC`: case-variant name of the module behind `belektronig_btc`
- `FW102`: case-variant name of the module behind `fw102`
- `BL05I`: beamline collection module, not a device
- `BL15I-BUILDER`: beamline collection module, not a device
- `BL21I`: beamline collection module, not a device
- `BR-LLRF`: accelerator RF module: fixed machine PVs, Hytec and MRF hardware
- `RFPGU`: accelerator RF module: fixed machine PVs, Hytec hardware
- `Thales-RF`: accelerator RF module: fixed machine PVs, Hytec and MRF hardware
- `CRE-331M`: S7 PLC device support, not stream
- `MPS`: machine-protection system: Hytec, EtherIP, FINS, compiled routines
- `insertionDevice`: insertion-device control: compiled driver, Hytec, motor
- `DLS8515`: installs no templates
- `epics-sc-dld-ioc-v1.7`: installs no templates
- `epics-twincat-ads`: installs no templates
- `ZoomLightLevel`: ships no protocol file

Upstream extras (manuals, private notes, files holding personal or site-internal
details) that are not imported are listed per file in
[REJECTED_EXTRAS.md](REJECTED_EXTRAS.md).
