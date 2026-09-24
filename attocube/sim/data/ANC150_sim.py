#!dls-python2.4

'''
This is a simulation of the Attocube model ANC150 controller. This controller type has following characteristics:
* usable for open-loop driving of Attocube piezo motors/actuators.
* the piezos are driven in stepping mode (i.e. by application of small pushes causes by pulses to voltage accross the piezo).
* the piezos cannot be driven in scanning mode (i.e. by continuous extension due to slowly changed voltage accross the piezo).
* this is the standard model ANC150/3 with 3 axes on it (an extended model ANC150/6 has 6 axes)

This simulation does *not* support/recognize the following commands: "setpu", "setpd", "getpu", "getpd", "setp", "getp" and "ResetP";
these are used to change the step signal variation patterns, which determine how voltage accross a piezo axis is gradually changed during each step of the piezo.
In this simulation it is assumed that the pattern stays the same all the time; in a real situation, if it changed,
then the distance traveled per step would also change. I recommend that, as for now, the users only use the default (linear) pattern.

The simulation also does *not* support/recognize the short movement commands, nor the "ver" (i.e. print version) and "help" commands.
'''

# [TODO] Finish implementing threading for asynchronous movements (make sure proper locking of shared variables happens)

import re
from threading import Thread
from time import sleep
from pkg_resources import require
require("dls.serial_sim==1.3")
from dls.serial_sim import serial_device

class Axis(Thread):
    '''
    Encapsulates a single independent axis on an ANC150 controller.
    '''
    def __init__(self):
        # Call parent class's constructor
        Thread.__init__(self)

        # Set up defaults
        self.mode = 'gnd'                # [MADEUP] (not sure if this is the default startup value)
        self.position = 0.0
        self.voltage = 1.0               # [MADEUP] (use default)
        self.frequency = 1000            # [MADEUP] (use default)
        self.capacity = 123              # just a random number, say 123 nF
        self.stepDistPerVoltage = 0.01   # [MADEUP] (use measured/empirical value)

        # For future multithreaded operation 
        self.refreshPeriod = 0.010       # thread refresh 10 ms
        self.noRemainingSteps = 0.0      # number of steps that are remaining to finish the move
        self.movementDirection = 0       # direction of movement, or 0 if the axis is not moving

        self.computerControlled = True   # is the mode switch on the axis control panel of the ANC150 in "CC" (=computer-controlled) position? 

    # Throw this error if a requested method cannot be executed while the axis is in the current mode
    class WrongModeError(Exception):
        pass

    # Throw this error if the parameter value (e.g. voltage, frequency) is out of range
    class ValueOutOfRangeError(Exception):
        pass

    # Throw this error if a command is run but the axis has been switched (externally, manually, by a user) out of the computer control mode
    class NotInComputerControlModeError(Exception):
        pass

    def checkComputerControlled(self):
        if self.computerControlled == False:
            raise Axis.NotInComputerControlModeError()

    def setMode(self, modeStr):
        self.checkComputerControlled()
        if modeStr in ['ext', 'stp', 'gnd', 'cap']:
            self.mode = modeStr
        else:
            raise Axis.WrongModeError()

    def getMode(self):
        self.checkComputerControlled()
        return self.mode

    def setFrequency(self, freqInt):
        self.checkComputerControlled()
        if freqInt < 1 or freqInt > 8000:
            raise Axis.ValueOutOfRangeError()
        self.frequency = freqInt

    def getFrequency(self):
        self.checkComputerControlled()
        return self.frequency

    def setVoltage(self, voltageInt):
        self.checkComputerControlled()
        if voltageInt < 1 or voltageInt > 70:
            raise Axis.ValueOutOfRangeError()
        self.voltage = voltageInt

    def getVoltage(self):
        self.checkComputerControlled()
        return self.voltage

    def getCapacity(self):
        self.checkComputerControlled()
        if self.mode != 'cap':
            raise Axis.WrongModeError('Not in cap mode')
        return self.capacity

    def stepu(self, noSteps):
        self.checkComputerControlled()
        if self.mode != 'stp':
            raise Axis.WrongModeError('Not in stp mode')
        self.position += noSteps * self.stepDistPerVoltage * self.voltage

    def stepd(self, noSteps):
        self.checkComputerControlled()
        if self.mode != 'stp':
            raise Axis.WrongModeError('Not in stp mode')
        self.position -= noSteps * self.stepDistPerVoltage * self.voltage

    def stop(self):
        self.checkComputerControlled()
        pass

    # This method will be running in a separate thread
    def run(self):
        pass
##         if self.movementDirection != 0:
##             noStepsInRefreshPeriod = self.frequency * refreshPeriod
##             self.noRemainingSteps -= noStepsInRefreshPeriod
##         sleep(self.refreshPeriod)

class ANC150_sim(serial_device):
    '''
    A serial_device simulation of the ANC150 controller.
    '''
    Terminator = '\r\n'
    dets = {}
    
    def __init__(self, debug = False, anc150Debug = False):
        self.axes = [Axis(), Axis(), Axis()]  #  create 3 axes
        # Start a "realtime" thread for each axis.
        # [TODO] These threads don't do anything at the moment -- make them do.
        self.axes[0].start()
        self.axes[1].start()
        self.axes[2].start()
        self.debug = debug              # self.debug gets checked by serial_device
        self.anc150Debug = anc150Debug  # self.anc150Debug is used by this class
        if self.anc150Debug:
            print 'ANC150_sim initialized'

    def reply(self, command):
        if self.anc150Debug:
            print 'ANC150 received: "%s"' % command
        r = self._reply(command) # do the actual reply
        if self.anc150Debug:
            print 'ANC150 replies: "%s"' % r
        return r
            
    def _reply(self, command):        
        try:
            # ------- Slow commands --------
            # [CHECK] (what if mode string is wrong; what would ANC say?)
            # Set mode
            mo = re.match(r'setm (1|2|3) (ext|stp|gnd|cap)', command)
            if mo:
                axisId = int(mo.group(1))
                modeStr = mo.group(2)
                try:
                    self.axes[axisId-1].setMode(modeStr)
                except Axis.ValueOutOfRangeError:
                    return 'Value out of range\r\nERROR'
                return 'OK'

            # Get mode
            mo = re.match(r'getm (1|2|3)', command)
            if mo:
                axisId = int(mo.group(1))
                modeStr = self.axes[axisId-1].getMode()
                return 'mode = %s\r\nOK' % modeStr

            # [CHECK] (what if chosen axis no is wrong -- what would ANC say?)
            # Step up (positive)
            mo = re.match(r'stepu (1|2|3) (\d+)', command)
            if mo:
                (axisId, noSteps) = map(int, mo.groups())
                try:
                    self.axes[axisId-1].stepu(noSteps)
                except Axis.WrongModeError:
                    return 'Axis in wrong mode\r\nERROR'
                return 'OK'

            # [CHECK] (what if chosen axis no is wrong -- what would ANC say?)
            # Step down (negative)
            mo = re.match(r'stepd (1|2|3) (\d+)', command)
            if mo:
                (axisId, noSteps) = map(int, mo.groups())
                try:
                    self.axes[axisId-1].stepd(noSteps)
                except Axis.WrongModeError:
                    return 'Axis in wrong mode\r\nERROR'
                return 'OK'

            mo = re.match(r'stop (1|2|3)', command)
            if mo:
                axisId = int(mo.group(1))
                self.axes[axisId-1].stop()
                return 'OK'

            # Set frequency
            mo = re.match(r'setf (1|2|3) (\d+)', command)
            if mo:
                (axisId, freq) = map(int, mo.groups())
                try:
                    self.axes[axisId-1].setFrequency(freq)
                except Axis.ValueOutOfRangeError:
                    return 'Value out of range\r\nERROR'
                return 'OK'

            # [CHECK] (what if chosen axis no is wrong -- what would ANC say?)
            # Get frequency
            mo = re.match(r'getf (1|2|3)', command)
            if mo:
                axisId = int(mo.group(1))
                freqInt = self.axes[axisId-1].getFrequency()
                return 'frequency = %i\r\nOK' % freqInt

            # Set voltage
            mo = re.match(r'setv (1|2|3) (\d+)', command)
            if mo:
                (axisId, v) = map(int, mo.groups())
                try:
                    self.axes[axisId-1].setVoltage(v)
                except Axis.ValueOutOfRangeError:
                    return 'Value out of range\r\nERROR'
                return 'OK'

            # [CHECK] (what if wrong axis no -- what would ANC say?)
            # Get voltage
            mo = re.match(r'getv (1|2|3)', command)
            if mo:
                axisId = int(mo.group(1))
                v = self.axes[axisId-1].getVoltage()
                return 'voltage = %i V\r\nOK' % v

            # [CHECK] (what if wrong axis no -- what would ANC say?)
            # Get capacity
            mo = re.match(r'getc (1|2|3)', command)
            if mo:
                axisId = int(mo.group(1))
                try:
                    c = self.axes[axisId-1].getCapacity()
                except Axis.WrongModeError:
                    return 'Axis in wrong mode\r\nERROR'
                return 'capacity = %i nF\r\nOK' % c

            # ------- Fast commands -------
            # Uncovered at the moment

            # ------- Else -------
            # Unrecognized command syntax
            return 'ERROR'

        except Axis.NotInComputerControlModeError:
            return 'Axis not in computer control mode\r\nERROR'

def run_tests():
    '''
    Run tests. This checks whether the ANC150_sim class behaves correctly. Each test tests a new, just-initialized, ANC150_sim instance.
    '''
    def test_nonsense(anc):
        return (
            anc.reply('nonsense 1 2') == 'ERROR'
            )
    #def test_not_computer_controlled(anc):
    #    anc.axis[2-1].isComputerControlled = False
    #    return (
    #        anc.reply('setm 2 stp') == 'Axis not in computer control mode\r\nERROR'
    #        )
    def test_setm_getm(anc):
        return (
            anc.reply('setm 1 ext') == 'OK' and anc.reply('getm 1') == 'mode = ext\r\nOK'
            )
    def test_stepu_error(anc):
        anc.reply('setm 1 gnd')
        return (
            anc.reply('stepu 1 1000') == 'Axis in wrong mode\r\nERROR'
            )
    def test_stepu_stepd_success(anc):
        anc.reply('setm 1 stp')
        res = anc.reply('stepu 1 1000')
        if res == 'OK' and anc.axes[0].position == 10.0:
            res = anc.reply('stepd 1 500')
            if res == 'OK' and anc.axes[0].position == 5.0:
                return True
        return False
    def test_stepu_stop(anc):
        return (
            anc.reply('setm 2 stp') == 'OK'
            and
            anc.reply('stepu 2 10000') == 'OK'
            and
            anc.reply('stop 2') == 'OK'
            )
    def test_freq(anc):
        return (
            anc.reply('setf 1 10000') == 'Value out of range\r\nERROR'
            and
            anc.reply('setf 1 2000') == 'OK'
            and
            anc.reply('getf 1') == 'frequency = 2000\r\nOK'
            )
    def test_voltage(anc):
        return (
            anc.reply('setv 1 80') == 'Value out of range\r\nERROR'
            and
            anc.reply('setv 1 10') == 'OK'
            and
            anc.reply('getv 1') == 'voltage = 10 V\r\nOK'
            )   
    def test_capacity(anc):
        if anc.reply('getc 2') == 'Axis in wrong mode\r\nERROR':
            anc.reply('setm 2 cap')
            if anc.reply('getc 2') == 'capacity = 123 nF\r\nOK':
                return True
        return False
    def test_not_in_computer_mode_error(anc):
        anc.axes[1].computerControlled = False # simulate user manually switching the axis off the "CC" (computer controlled) mode
        return anc.reply('getv 2') == 'Axis not in computer control mode\r\nERROR'
    for test in [test_nonsense, test_setm_getm, test_stepu_error, test_stepu_stepd_success,
                 test_stepu_stop, test_freq, test_voltage, test_capacity, test_not_in_computer_mode_error]:
        anc = ANC150_sim()
        if not test(anc):
            print 'FAILED TEST "%s". STOP.' % test.__name__
            return
if __name__ == "__main__":
    run_tests()
