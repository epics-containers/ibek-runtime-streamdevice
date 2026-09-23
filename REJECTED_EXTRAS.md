# Upstream extras not imported

Every non-runtime file (`documentation/`, `etc/`, top-level docs) in a pattern's DLS
source release is classified before import. Files that are safe to publish live in
`docs/`, `sim/` or `test/` inside the pattern folder; the pattern's
`ibek.manifest.yaml` keeps them out of a vendored IOC instance. The files below are
not imported: each is a third-party vendor manual, is marked private upstream, or holds
personal or site-internal details. Generated files, tooling files and empty
placeholders are skipped without being listed.

168 files across 54 modules.

| Module | Path | Reason |
|---|---|---|
| `APD-ACE` | `documentation/APD0002-UserManual.pdf` | third-party vendor manual or datasheet (copyright) |
| `CryoconM14` | `documentation/private/manufacturer/M14Brochure_2006.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM14` | `documentation/private/manufacturer/M14UserManual_5c_mar2007.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM14` | `documentation/private/manufacturer/M14UserManual_5e_sep2007.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM14` | `etc/test/CryoconM14_test.py` | hard-coded internal IP address |
| `CryoconM32` | `documentation/private/manufacturer/ApplNotes/CP100Install.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/ApplNotes/DitherInDigCtl.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/ApplNotes/ThermoApps.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32Brochure_g0806.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32QuickStart_2008.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32QuickStart_Rev5.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32QuickStart_Rev6.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32UserManual_4e_mar2006.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32UserManual_4f_dec2006.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32UserManual_6c_dec2006.pdf` | upstream keeps it under a `private/` directory |
| `CryoconM32` | `documentation/private/manufacturer/M32UserManual_6e_mar2008.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsNextTurbo` | `documentation/private/ManualTypos.txt` | upstream keeps it under a `private/` directory |
| `EdwardsNextTurbo` | `documentation/private/Manufacturer/Edwards/Edwards_nEXT_B80000840_ServiceManual_IssueB_2010.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsNextTurbo` | `documentation/private/Manufacturer/Edwards/Edwards_nEXT_B80000840_ServiceManual_IssueB_2010_Extract_Ch7TimeReset.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsNextTurbo` | `documentation/private/Manufacturer/Edwards/Edwards_nEXT_B80000880_InstructionManual_IssueA_2009.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsNextTurbo` | `documentation/private/Manufacturer/Edwards/Edwards_nEXT_B80000880_InstructionManual_IssueC_2011.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsNextTurbo` | `documentation/private/Manufacturer/Edwards/Edwards_nEXT_B80000880_InstructionManual_IssueD_2013.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/doxygen/manual` | names an individual outside an attribution line |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Replacement_Tip_Seal_Kit_Instruction_Manual_A735-02-840_IssueA_2012.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Scroll_Pump_Instruction_Manual_A735-01-880_IssueA_2012.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Scroll_Pump_Instruction_Manual_A735-01-880_IssueB_2013.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Scroll_Pump_Instruction_Manual_A735-01-880_IssueC_2017.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Scroll_Pump_Instruction_Manual_A735-01-880_IssueF_2018.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Scroll_Pump_Parts_Manual_A735-01-845_IssueD_2013.pdf` | upstream keeps it under a `private/` directory |
| `EdwardsScroll` | `documentation/private/Manufacturer/Edwards/Edwards_nXDS_Serial_Comms_Interface_Instruction_Manual_A735-01-860_IssueA_2012.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6482_Catalogue_2012-09-25.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6482_Reference_RevA_2015-09-17.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6482_Specification_RevA_2021-10-17.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6485_Catalogue_2012-09-25.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6485_Reference_RevC_2011-03-01.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6485_Specification_RevB_2021-08-04.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6487_Catalogue_2015-01-16.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6487_Reference_RevD_2020-10-28.pdf` | upstream keeps it under a `private/` directory |
| `Keithley6487` | `documentation/private/Manufacturer/Keithley/Keithley_6487_Specification_RevA_2021-02-16.pdf` | upstream keeps it under a `private/` directory |
| `KeithleyDMM6500` | `documentation/DMM6500-900-01B_User_Aug_2019.pdf` | third-party vendor manual or datasheet (copyright) |
| `KeithleyDMM6500` | `documentation/DMM6500-901-01_A_April_2018_Ref_DMM6500-901-01A.pdf` | third-party vendor manual or datasheet (copyright) |
| `ODPsu` | `etc/private/manufacturer/47544-21-appendix-A-revision-K.pdf` | upstream keeps it under a `private/` directory |
| `ODPsu` | `etc/private/manufacturer/Getting-Started-Guide-2.0.pdf` | upstream keeps it under a `private/` directory |
| `ODPsu` | `etc/private/manufacturer/S1400-Bimorph-Power-Supply-DLS-I18-USER-MANUAL-2.0a.pdf` | upstream keeps it under a `private/` directory |
| `ODPsu` | `etc/simulations/ODPsu_sim.py` | internal user identifier |
| `OxInstCryojet` | `documentation/ILM200_Family_Operators_Handbook_CNC0999.doc` | third-party vendor manual or datasheet (copyright) |
| `OxInstCryojet` | `documentation/ITC503_Operators_Handbook_CQI0999.pdf` | third-party vendor manual or datasheet (copyright) |
| `OxInstCryojet` | `documentation/MercuryiTC-Jan2012.pdf` | third-party vendor manual or datasheet (copyright) |
| `OxInstIPS` | `documentation/private/Manufacturer/OxfordInstruments/OxfordInstruments_ModularIPS_Operator_Handbook_Revision9_2006Jun_UMC0041.pdf` | upstream keeps it under a `private/` directory |
| `VCH10Light` | `documentation/private/Manufacturer/PreVac/VCH-10_CommunicationProtocolManual_English.pdf` | upstream keeps it under a `private/` directory |
| `VCH10Light` | `documentation/private/Manufacturer/PreVac/VCH-10_Datasheet.pdf` | upstream keeps it under a `private/` directory |
| `VCH10Light` | `documentation/private/Manufacturer/PreVac/VCH-10_UserManual_English_Rev2_Jan2014.pdf` | upstream keeps it under a `private/` directory |
| `WS300scale` | `documentation/notes.txt` | signed by an individual |
| `WS300scale` | `documentation/private/manufacturer/33m8NfUc.pdf` | upstream keeps it under a `private/` directory |
| `WS300scale` | `documentation/private/manufacturer/SBI 140_u.pdf` | upstream keeps it under a `private/` directory |
| `agilent33220A` | `documentation/private/33220-90002.pdf` | upstream keeps it under a `private/` directory |
| `agilent33220A` | `documentation/private/E4400-90506.pdf` | upstream keeps it under a `private/` directory |
| `agilent33220A` | `documentation/private/SCPI-99.PDF` | upstream keeps it under a `private/` directory |
| `agilent53220` | `documentation/53220-90001_users_guide.pdf` | third-party vendor manual or datasheet (copyright) |
| `agilentE364xA` | `documentation/doxygen/manual` | internal URLs and a personal contact email address |
| `agilentE364xA` | `documentation/private/E3646-90001.pdf` | upstream keeps it under a `private/` directory |
| `agilentTurboPump` | `documentation/manuals/TwisTorr305-IC.pdf` | third-party vendor manual or datasheet (copyright) |
| `agilentTurboPump` | `documentation/manuals/TwisTorrCtrl305-FS.pdf` | third-party vendor manual or datasheet (copyright) |
| `alicatGasFlow` | `documentation/Gas_Flow_Controller_Manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `ametekLockIn` | `documentation/private/197852-A-MNL-C-1.pdf` | upstream keeps it under a `private/` directory |
| `attocubeInterf` | `documentation/manufacturer/IDS_Manual_v2.2.0.pdf` | third-party vendor manual or datasheet (copyright) |
| `caenN1470` | `documentation/N1470_rev12.pdf` | third-party vendor manual or datasheet (copyright) |
| `cyberstar` | `documentation/Oxford-Scintillator-manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `digitelMpc` | `docs/Gamma-Serial-Commands.pdf` | third-party vendor manual or datasheet (copyright) |
| `digitelMpc` | `docs/MPC_J.pdf` | third-party vendor manual or datasheet (copyright) |
| `digitelMpc` | `docs/MPC_J.zip` | archive of a third-party vendor manual (copyright) |
| `digitelMpc` | `docs/MPC_J_68.pdf` | third-party vendor manual or datasheet (copyright) |
| `digitelMpc` | `docs/MPCq.pdf` | third-party vendor manual or datasheet (copyright) |
| `dlsCAENels` | `documentation/manufacturer/HV-ADAPTOS_TCP-IP_and_EPICS_Command_Reference_V1.3.pdf` | third-party vendor manual or datasheet (copyright) |
| `dlsCAENels` | `documentation/manufacturer/HV-ADAPTOS_Users_Manual_V1.1.pdf` | third-party vendor manual or datasheet (copyright) |
| `elmitecLEEM` | `documentation/private/Manufacturer/LEEM2000Script v37.pdf` | upstream keeps it under a `private/` directory |
| `elmitecLEEM` | `documentation/private/Manufacturer/LEEM2000Script v40.pdf` | upstream keeps it under a `private/` directory |
| `enzLoCuM4` | `docs/ENZ-LoCuM-4.pdf` | third-party vendor manual or datasheet (copyright) |
| `eurotherm2k` | `documentation/HA026230_3_2000 comms.pdf` | third-party vendor manual or datasheet (copyright) |
| `eurotherm2k` | `documentation/private/2404_and_2408_InstallationAndOperationHandbook.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/2408i_Datasheet.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/2416_HA025041_10.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/2704_EngHandbook.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/2704_Modbus.csv` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/2704_Spec.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/EPC3000 User Manual.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/HA025132_13 2408-04 User Manual.pdf` | upstream keeps it under a `private/` directory |
| `eurotherm2k` | `documentation/private/V6EIBisynch.csv` | upstream keeps it under a `private/` directory |
| `eurotherm903` | `documentation/doxygen/manual` | names an individual outside an attribution line |
| `gardasoftLED` | `documentation/private/PP612Manual.pdf` | upstream keeps it under a `private/` directory |
| `gardasoftLED` | `documentation/private/RT460Manual.pdf` | upstream keeps it under a `private/` directory |
| `granvillePhillips` | `documentation/manufacturer/307GCTRL.pdf` | third-party vendor manual or datasheet (copyright) |
| `granvillePhillips` | `documentation/manufacturer/Granville_Phillips_350_IG_Controller.pdf` | third-party vendor manual or datasheet (copyright) |
| `harvardSyringe` | `documentation/PHD ULTRA Manual-70-3xxx_5419-002REV1.0.pdf` | third-party vendor manual or datasheet (copyright) |
| `isegHVPSU` | `documentation/doxygen/manual` | names an individual outside an attribution line |
| `isegHVPSU` | `documentation/manual.src` | links to an internal Diamond intranet URL (`http://diamdocs/...`) |
| `isegHVPSU` | `documentation/private/TDI-CTRL-REQ-0019-ISEG-HVPSU-requirements.doc` | internal project requirements document |
| `isegHVPSU` | `documentation/private/nhqx2x_eng.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2400_Series_Datasheet_Apr2021_1KW-2798-3.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2400_Series_QuickStart_RevisionE_Sep2011_2400S-903-01E.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2400_Series_UserManual_RevisionG_May2002_2400S-900-01G.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2400_Series_UserManual_RevisionK_Sep2011_2400S-900-01K.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2400_ServiceManual_RevisionG_Feb2006_2400-902-01G.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2410_ServiceManual_RevisionB_Jul1998_2410-902-01B.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2410_ServiceManual_RevisionC_Apr2017_2410-902-01C.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2461_CalibrationManual_RevisionA_Feb2016_2461-905-01A.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2461_Datasheet_Dec2024_1KW-60288-2.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2461_QuickStart_RevisionB_Aug2019_2461-903-01B.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2461_ReferenceManual_RevisionA_Nov2015_2461-901-01A.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/private/Manufacturer/Keithley/Keithley2461_UserManual_RevisionB_Aug2019_2461-900-01B.pdf` | upstream keeps it under a `private/` directory |
| `keithley2400` | `documentation/requirements/Keithley-2400-requirements.doc` | internal project requirements document |
| `keithley2600` | `documentation/manufacturer/Keithley 2634B manual 2600BS-901-01.pdf` | third-party vendor manual or datasheet (copyright) |
| `keithley6514` | `documentation/6517B-900-01.pdf` | third-party vendor manual or datasheet (copyright) |
| `keithley6514` | `documentation/6517B-901-01.pdf` | third-party vendor manual or datasheet (copyright) |
| `keithley6517B` | `documentation/6517B-900-01.pdf` | third-party vendor manual or datasheet (copyright) |
| `keithley6517B` | `documentation/6517B-901-01.pdf` | third-party vendor manual or datasheet (copyright) |
| `keysight33500B` | `documentation/manufacturer/33500-90901.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/9007-0001_KSC1212_VE.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/9007-0003_KSC_AC_Generic_Manual_VB.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/AC1006_V2.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/EC12002_Emission_Controller_V2.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/KDC100_S_MO_2G_DI_12cm_V1.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/KRI_MFC_Manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `kriIonBeam` | `documentation/LFN2000_S_VB.pdf` | third-party vendor manual or datasheet (copyright) |
| `lakeshore340` | `documentation/doxygen_pages` | internal IP address |
| `lakeshore340` | `documentation/private/Manufacturer/Lakeshore/3300_Fundamentals.pdf` | upstream keeps it under a `private/` directory |
| `lakeshore340` | `documentation/private/Manufacturer/Lakeshore/Lakeshore340_CataloguePages_l.pdf` | upstream keeps it under a `private/` directory |
| `lakeshore340` | `documentation/private/Manufacturer/Lakeshore/Lakeshore340_UserManual_Rev2-1_2004-03-29.pdf` | upstream keeps it under a `private/` directory |
| `lakeshore340` | `documentation/private/Manufacturer/Lakeshore/Lakeshore340_UserManual_Rev3-3_2009-05-14.pdf` | upstream keeps it under a `private/` directory |
| `lakeshore340` | `documentation/requirements/TDI-CTRL-REQ-007-Lakeshore-340-requirements.doc` | internal project requirements document |
| `laudaRE2xx` | `documentation/doxygen/manual` | internal URLs and a personal contact email address |
| `laudaRE2xx` | `documentation/manual/LAUDA-Ecoline-RE-200-RE-300-Manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `laudaRE2xx` | `documentation/manual/LAUDA-Integral-T-Manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `laudaRE2xx` | `documentation/manual/LAUDA-Microcool-Manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `laudaRE2xx` | `documentation/manual/LAUDA-Variocool-Manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `laudaRE2xx` | `documentation/manual/YAAE0026_Lauda_EthernetUSB_V1R30en_US_16-03-24_Internet.pdf` | third-party vendor manual or datasheet (copyright) |
| `laudaRE2xx` | `documentation/manual/YACE0087_Lauda_ECO_Silver_f_EN_translation_2017-05.pdf` | third-party vendor manual or datasheet (copyright) |
| `laudaRE2xx` | `documentation/manual/YAEE013_V40d1_E2xx_Staredition_2005-08-30.pdf` | third-party vendor manual or datasheet (copyright) |
| `leybold` | `documentation/.~lock.leybold_centerone_manual.pdf#` | internal user identifier |
| `leybold` | `documentation/Mnemonics.ods` | third-party vendor manual or datasheet (copyright) |
| `leybold` | `documentation/leybold_centerone_manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `leyboldCenterOne` | `documentation/leybold_centerone_manual.pdf` | third-party vendor manual or datasheet (copyright) |
| `mks647c` | `documentation/manufacturer/MassFlowControllerManual647C.pdf` | third-party vendor manual or datasheet (copyright) |
| `mks937a` | `documentation/937A-man.pdf` | third-party vendor manual or datasheet (copyright) |
| `mks937a` | `documentation/HPS937-232-485MAN.pdf` | third-party vendor manual or datasheet (copyright) |
| `mks937a` | `documentation/setpoints-interlocks-lock.txt` | site-specific IOC instance names and interlock details |
| `mks937b` | `data/windowsize.py` | internal user identifier |
| `mks937b` | `documentation/937B-MAN.pdf` | third-party vendor manual or datasheet (copyright) |
| `omegaIR2C` | `documentation/manufacturer/IR2CcommsM4911.pdf` | third-party vendor manual or datasheet (copyright) |
| `omegaIR2C` | `documentation/manufacturer/IR2CpyrometerM3752.pdf` | third-party vendor manual or datasheet (copyright) |
| `omegaIR2C` | `documentation/manufacturer/M3629n.pdf` | third-party vendor manual or datasheet (copyright) |
| `pr4000` | `documentation/PR4000.pdf` | third-party vendor manual or datasheet (copyright) |
| `smc` | `documentation/private/InstrumentationDesignReportForFDR.pdf` | upstream keeps it under a `private/` directory |
| `smc` | `documentation/private/manufacturer/PSUManual.pdf` | upstream keeps it under a `private/` directory |
| `smc` | `documentation/private/manufacturer/drvHy8515CodeExtract.txt` | upstream keeps it under a `private/` directory |
| `specsVCU1000` | `documentation/SPECS_piezo_valve_controller_Manual VCU1000_v1.4.pdf` | third-party vendor manual or datasheet (copyright) |
| `stanfordDG645` | `documentation/private/DG645m.pdf` | upstream keeps it under a `private/` directory |
| `strainGauge` | `documentation/manufacturer/M5452.pdf` | third-party vendor manual or datasheet (copyright) |
| `strainGauge` | `documentation/manufacturer/M5460.pdf` | third-party vendor manual or datasheet (copyright) |
| `tenmaPSU` | `documentation/manufacturer/private/IM - 72-2685 72-2690 72-2695 72-2700 rev (1).pdf` | upstream keeps it under a `private/` directory |
| `tenmaPSU` | `documentation/manufacturer/private/KA Series Single Channel Remote Control Syntax V2.0.pdf` | upstream keeps it under a `private/` directory |
| `tenmaPSU` | `documentation/manufacturer/private/KA3000-6000 user manual (single channel power supply)1540951205511.pdf` | upstream keeps it under a `private/` directory |
| `tenmaPSU` | `documentation/manufacturer/private/Series Protocol V2.0 of Remote Control.pdf` | upstream keeps it under a `private/` directory |
| `ttiMX` | `documentation/private/MX-Q+MX-QP_Series_2_Instruction_Manual_EN_48511-1950_2.pdf` | upstream keeps it under a `private/` directory |
| `twickenhamHDI` | `docs/Manual-HLM-Alarm-Option.pdf` | third-party vendor manual or datasheet (copyright) |
| `twickenhamHDI` | `docs/Manual-HLM-basic.pdf` | third-party vendor manual or datasheet (copyright) |
| `vici` | `documentation/manufacturer/tn415.pdf` | third-party vendor manual or datasheet (copyright) |
| `vici` | `documentation/manufacturer/tn421.pdf` | third-party vendor manual or datasheet (copyright) |
