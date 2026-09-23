Keithley2600 EPICS module
-------------------------

There are three options currently implemented for gathering readings.

1)	Free running: 
Adjust the "Setup" GUI panel parameters and turn the "Output" on. 
Your selected bias is then applied and "Actual V", "Actrual I" and "Actual R" return the readings.

2)	Measure Overlapped: 
This uses the Keithleys smuX.meaure.overlappediv command (manual P 7-207). 
Data is collected in the Keithley for the period and collection interval specified in the "Measure Overlapped" and "Setup" GUI panel. 
The collected data is averaged and displayed as "Mean V" and "Mean I" at the end of the scan.

3)	Pulse Sweep: 
This uses pre-programmed scripts in the Keithley ConfigPulseIMeasureVSweepLin (manual P 7-35) or 
ConfigPulseVMeasureISweepLin (manual P 7-41).  Data is collected in the Keithley for the period and collection 
interval specified in "Pulse Sweep" and "Setup" GUI panels. The bias is pulsed on each time a measurement is 
taken during the collection period, it is not on continuously. The bias can be a fixed value or swept linearly 
during the measurement period. An array of measurements is returned.
