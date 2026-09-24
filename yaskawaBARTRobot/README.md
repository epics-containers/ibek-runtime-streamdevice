# yaskawaBARTRobot

Runtime StreamDevice pattern imported from the DLS support module `yaskawaBARTRobot`,
release `0-1-I22-ONLY`
(`/dls_sw/prod/R3.14.12.7/support/yaskawaBARTRobot/0-1-I22-ONLY`). Its files are
pristine copies of that release, apart from the scripted changes its support yaml header
lists.

How each file was obtained, and any change made to it, is recorded in the header of
[`yaskawaBARTRobot.ibek.support.yaml`](yaskawaBARTRobot.ibek.support.yaml). That header
is vendored with the pattern, so the provenance travels into every IOC instance that
uses it.

## Entity models

| Entity model | Description |
|---|---|
| `yaskawaBARTRobot.yaskawaPosition` | Define yaskawa robot controller Position variables that can be set and read in EPICS |
| `yaskawaBARTRobot.yaskawaLong` | Define yaskawa robot controller Long (int32) variables that can be set and read in EPICS. Yaskawa refers to these as a "double precision variables" |
| `yaskawaBARTRobot.yaskawaLongNoSync` | Define yaskawa robot controller Long (int32) variables that can be set and read in EPICS without syncing the target value with the RBV. Yaskawa refers to these as a "double precision variables" |
| `yaskawaBARTRobot.yaskawaLongReadOnly` | Define yaskawa robot controller Long (int32) variables that can not be changed from EPICS. Yaskawa refers to these as a "double precision variables" |
| `yaskawaBARTRobot.yaskawaByte` | Define yaskawa robot controller Byte variables that can be set and read in EPICS |
| `yaskawaBARTRobot.yaskawaInput` | Define yaskawa robot controller Network Inputs that can be set in EPICS, typically 27010-29567 |
| `yaskawaBARTRobot.yaskawaOutput` | Define yaskawa robot controller Network Outputs that can be read from EPICS, typically 37010-39567 |
| `yaskawaBARTRobot.yaskawa` | Yaskawa robot controller: status, position, servo and job control |
| `yaskawaBARTRobot.yaskawaReal` | Define yaskawa robot controller Real (float) variables that can be set and read in EPICS |
| `yaskawaBARTRobot.BARTRobot` | Yaskawa controller type and jobs run from EPICS, plus: Yaskawa variable numbers used by the sample exchange jobs for Carrier Column, Row and Slot (jobs can be prevented from running if these variables have not been received by the controller within 1 second), and a PLC port for reading the gripper and barcode reader. NOTE: needs a generic IOC built with yaskawaBARTRobot (not the plain generic image). |

## Files

[`ibek.manifest.yaml`](ibek.manifest.yaml) vendors these files into an IOC
instance's `config/`:

- `BARTRobot.db`
- `BARTRobot_settings.req`
- `yaskawa.proto`
- `yaskawa.template`
- `yaskawaBARTRobot.ibek.support.yaml`
- `yaskawaByte.template`
- `yaskawaInput.template`
- `yaskawaLong.template`
- `yaskawaLongNoSync.template`
- `yaskawaLongReadOnly.template`
- `yaskawaOutput.template`
- `yaskawaPosition.template`
- `yaskawaReal.template`
- `yaskawa_settings.req`

Everything else in this folder stays in the library and is never vendored:

- `README.md` - this file

## Needs more than the generic image

These templates load only in a generic IOC built with the support they
need; the others run in the generic `ioc-streamdevice` image. See
[_docs/BUILD-TIME-ONLY.md](../_docs/BUILD-TIME-ONLY.md).

| Template(s) | Needs |
|---|---|
| `BARTRobot.db` | compiled aSub routines `DecToAsc`, `GripperState`; compiled FINS asyn driver |
