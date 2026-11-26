# BL05I-streamdevice

Runtime StreamDevice pattern imported from the DLS beamline support module `BL05I`,
release `2-95` (`/dls_sw/prod/R3.14.12.7/support/BL05I/2-95`). It holds the builder
classes of that module that use StreamDevice, with their protocols; the rest of `BL05I`
is the `BL05I` pattern of
[ibek-runtime-support](https://github.com/epics-containers/ibek-runtime-support). Its
files are pristine copies of that release, and of `Hostlink.proto` from `HostLink` `3-3`,
the release `BL05I` `2-95` builds against.

The folder is not called `BL05I`, so that it does not collide with that pattern: an IOC
can vendor both. The entity model names are the `BL05I` builder classes and their
parameters the builder XML attributes, so builder2ibek can convert an XMLbuilder IOC to
them by changing only the module in each entity's type.

How each file was obtained, and any change made to it, is recorded in the header of
[`BL05I-streamdevice.ibek.support.yaml`](BL05I-streamdevice.ibek.support.yaml). That
header is vendored with the pattern, so the provenance travels into every IOC instance
that uses it.

## Entity models

| Entity model | Description |
|---|---|
| `BL05I-streamdevice.BL05I_changeHexapodMirror` | Change a hexapod set up from one mirror to another through a Delta Tau PLC; two mirrors |
| `BL05I-streamdevice.BL05I_changeHexapodMirror_withRef` | As above, with a third, reference, position; for the updated mirror change PLC |
| `BL05I-streamdevice.BL05I_waterchiller` | Monitoring and control of a DLS water chiller circuit run by an Omron PLC over HostLink |

```yaml
  - type: BL05I-streamdevice.BL05I_changeHexapodMirror_withRef
    P: BL05I-OP-RFM-01
    R: :MIRCTRL
    PLC: 12
    PORT: BRICK06_Port
    YMTR: BL05I-OP-RFM-01:Y
    M1NAME: M4
    M2NAME: M5

  - type: BL05I-streamdevice.BL05I_waterchiller
    P: BL05I-HO-CHILL-01
    PLCNAME: BL05I-HO-PLC-01
    port: chiller_plc
    T4PRES: 0
```

## Notes

- **Hexapod mirror: the device is a Delta Tau GeoBrick.** The records read and write
  the PLC's P-variables (`P<PLC>03` to `P<PLC>12`) and its run flag (`M50<PLC>`) with
  plain StreamDevice commands. `PORT` is the asyn IP port the IOC's pmac controller
  already uses, made by `pmac.pmacAsynIPPort` (`pmacAsynIPConfigure`), so these entities
  live in the motion IOC that drives the hexapod.
- **Hexapod mirror: image.** The records need StreamDevice, `calc` (`scalcout`) and
  `busy`. They load in the generic `ioc-streamdevice` image, but the IOCs that use them
  in practice are pmac IOCs, so their image needs StreamDevice as well as pmac.
- **Hexapod mirror: `YMTR`** names the hexapod's Y motor record, which this pattern does
  not create. Changing mirror writes that record's soft limits (`.HLM`, `.LLM`) and
  reads its position, so the motor is normally in the same IOC.
- **Water chiller: `port`** is an asyn IP or serial port to the Omron PLC, which talks
  HostLink. `Hostlink.proto` is the `HostLink` module's protocol file; the `HostLink`
  pattern ships only `HostlinkFINS.proto`, so this pattern carries its own copy.
- **Water chiller: absent sensors.** Set `<sensor>PRES` to `0` for each pressure, flow
  or temperature sensor or valve the system does not have.
- **Water chiller: `WPDESC` and `UVDESC` defaults.** The template gives each of these two
  different defaults in different records; the model's defaults are the longer of each
  pair (`<PLCNAME> Water turbine pump`, `<PLCNAME> UV Steriliser.`), so a record that
  used the shorter one gets the longer description when the macro is not set.
- **Water chiller: alarm limits.** The pressure, flow and valve alarm limits and the
  flow `HOPR`/`LOPR` have no default in the template (empty), so they are text
  parameters here; the temperature ones are numbers.

## Upstream defects carried as-is

The templates are pristine, so these `BL05I` `2-95` defects are kept:

- `BL05I_changeHexapodMirror.template`: the completion sequence processes
  `$(P)$(R):GET:RVB:STATUS`, a record that does not exist (the template has
  `GET:STATUS`), so its forced status refresh does nothing and the next poll updates
  the status instead. The `_withReference` template has this fixed.
- Both hexapod templates build the change command from `DMD:MIRROR`'s `VAL`, the state
  number, not `RVAL`, the mirror index the PLC reported. The two agree only while the
  PLC numbers its mirrors 1 and 2 (and 3 for the reference).
- The generated PVI screens label the soft-limit records with their `DESC` cut at its
  inner quote (`$(M1NAME=`), because `generate-pvi.py` reads the label up to the first
  `"`.

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `BL05I-streamdevice.ibek.support.yaml`
- `BL05I_changeHexapodMirror.pvi.device.yaml`
- `BL05I_changeHexapodMirror.template`
- `BL05I_changeHexapodMirror_withRef.pvi.device.yaml`
- `BL05I_changeHexapodMirror_withReference.template`
- `BL05I_waterChiller.template`
- `BL05I_waterChiller_settings.req`
- `BL05I_waterchiller.pvi.device.yaml`
- `Hostlink.proto`
- `changeHexapod.proto`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file
