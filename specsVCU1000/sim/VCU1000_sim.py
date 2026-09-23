#!/dls_sw/prod/tools/RHEL5/bin/python2.6
# Simulates a SPECS VCU1000 module. 
# Communications protocol should replicate that in Appendix 3.1 of the 
# manual except where noted,  otherwise the simulation of the actual pressure
# regulation is quite crude, simply incrementing the current pressure toward
# the target pressure by 1% on each cycle. 
# Internally the device can be in one of four states:
#   Standby
#   InProgress
#   Regulating
#   Error
# The Timer is used to limit the period of regulation. If enabled it starts 
# immediately upon entering InProgress mode and pauses if we enter Standby or
# Error mode. Upon entering Standby mode, the TimerTarget variable is set to 
# CurrentCount of the timer, and if we entered Standby because the timer 
# expired, the timer is disabled. 
# There is also a separate RegulationTimeout which limits the amount of time 
# spent in the InProgress state. If this expires before we reach Regulating
# or Standby, the system transitions to Error state.
# We can also toggle RemoteMode on and off - this controls whether we accept
# SET messages or not. 

from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device
import time

# Constants
StandbyMode = "Standby"
InProgressMode = "InProgress"
RegulatingMode = "Regulating"
ErrorMode = "Error"

OnState = "On"
OffState = "Off"

RemoteState = "Remote"
LocalState = "Local"

MinVoltage = 0.0
MaxVoltage = 1000.0
MinPressure = 1.0e-10
MaxPressure = 9.9e-03
MinTolerance = 1
MaxTolerance = 50
MinKP = 1.0e+02
MaxKP = 1.0e+05
MinKI = 1.0e+01
MaxKI = 1.0e+04
MinTimeout = 20
MaxTimeout = 500

# Parameters for the linear voltage/pressure conversion
VGradient = -9.89999990e-06
PIntercept = 9.9e-03
VIncrement = 10.0

#Strips off a prefix from a string, removes trailing and leading whitespace,
#and if required converts it to a float or int.
def getNextArg(text, prefix, isFloat=False, isString=False):
    try:
        argument = text.split(prefix)[1].lstrip().rstrip()
        if (isFloat):
            ret = float(argument)
        elif (isString):
            ret = argument
        else:
            ret = int(argument)
    except:
        raise
    else:
        return ret
        


class my_device(serial_device):
    InTerminator = "\r\n"
    OutTerminator = ""
    def __init__(self):
    # need an init function to start the schedule function
	# Also set default starting values for internal variables.
        self.vals = {"Status":StandbyMode, "RemoteMode":LocalState, "PressureTarget":0.0099, "PressureTolerance":1, "ValveVoltage":0.00, "ValveVoltageMax":1000.00, "ValueKP":5.0e+03, "ValueKI":5.0e+02, "PersistentTimer":OffState, "Timer":OffState, "PersistentTimerTarget":0, "TimerTarget":0, "CurrentTimer":0, "RegulationTimeout":60, "TimeoutCounter":0, "CurrentTicks":0}
        self.schedule(self.inc,1.0)
    def inc(self):
    # CurrentTicks is the time in ms since the last reset.  
        self.vals["CurrentTicks"] = self.vals["CurrentTicks"] + 1000
    
        if self.vals["Status"] == InProgressMode:
            if self.vals["TimeoutCounter"] == 0:
                self.enterErrorMode()
            elif self.vals["Timer"] == OnState and self.vals["CurrentTimer"] == 0:
                self.vals["Timer"] = OffState
                self.enterStandbyMode()
            elif self.pressureIsInsideTolerance():
                self.enterRegulatingMode()
            else:
                self.adjustVoltage()
                self.vals["TimeoutCounter"] = self.vals["TimeoutCounter"] - 1
                if self.vals["Timer"] == OnState:
                    self.vals["CurrentTimer"] = self.vals["CurrentTimer"] - 1
        elif self.vals["Status"] == RegulatingMode:
            if not self.pressureIsInsideTolerance():
                self.enterInProgressMode()
            elif self.vals["Timer"] == OnState and self.vals["CurrentTimer"] == 0:
                self.vals["Timer"] = OffState
                self.enterStandbyMode()
            elif self.vals["Timer"] == OnState:
                self.vals["CurrentTimer"] = self.vals["CurrentTimer"] - 1

    def reply(self, command):
        # First parse the command type.
        # I've tried to get this as close as possible to how the device behaves 
        # - it will ignore whitespace in any command expecting 2 or more 
        # parameters (so for example "SET    PressureTarget   1.0e-8   " is 
        # valid) but requires exactly 1 space after the command for commands 
        # expecting 1 parameter (so "GET  RemoteMode  " will return 
        # BadParameter).
        print time.time(), "Sent", command 
        if command == "RESET":
            self.enterStandbyMode()
            self.vals["TimerTarget"] = self.vals["PersistentTimerTarget"]
            self.vals["CurrentTimer"] = self.vals["TimerTarget"]
            self.vals["Timer"] = self.vals["PersistentTimer"]
            return "OK"
        
        elif command == "Info":
            return "VCU1000 Version 0103.03\nCompiled Dec 21 2010 09:09:44\nSerialNo 28.61.a5.48.02.00.00"

        elif command.startswith("GET "):
            parameters = command.split("GET ", 1)[1]
            # Hard-coded responses
            if parameters == "DeviceType":
                return "OK \"VCU1000\""
            elif parameters == "DeviceId":
                return "OK 2861a548020000"
            elif parameters == "Version":
                return "OK \"Firmware 0103.03, compiled Dec 21 2010 09:09:44\""
            elif parameters == "PressureInterface":
                return "OK GP274_10mA"
                
            # Computed responses
            elif parameters == "CurrentValveVoltage":
                return "OK %.2f" % self.vals["ValveVoltage"]
            elif parameters == "CurrentValvePercentage":
                ratio = 100.0*self.vals["ValveVoltage"]/self.vals["ValveVoltageMax"]
                return "OK %.2f" % ratio
            elif parameters == "Regulation":
                if self.regulating():
                    return "OK On"
                else:
                    return "OK Off"
            elif parameters == "CurrentPressure":
                return "OK %.1e" % self.currentPressure()
            
            # Internal variables
            elif parameters in self.vals:
                value = self.vals[parameters]
                if parameters in ("TimerTarget", "PressureTolerance", "CurrentTimer", "RegulationTimeout", "CurrentTicks"):
                    return "OK %d" % value
                elif parameters in ("PressureTarget", "ValueKI", "ValueKP"):
                    return "OK %.1e" % value
                elif parameters in ("ValveVoltageMax",):
                    return "OK %.2f" % value
                else:
                    return "OK %s" % value
                    
            else:
                return "ERROR BadParameter \"%s\"" % parameters
            
        elif command.startswith("SET "):
            parameters = command.split("SET ", 1)[1].lstrip()
            # Handle RemoteMode first, so that we can stop processing if 
            # we aren't in Remote.
            if parameters.startswith("RemoteMode"):
                print "SET RemoteMode called"
                argument = parameters.split("RemoteMode")[1].lstrip().rstrip()
                if argument == LocalState:
                    self.vals["RemoteMode"] = LocalState
                    return "OK %s" % self.vals["RemoteMode"]
                elif argument == RemoteState:
                    self.vals["RemoteMode"] = RemoteState
                    return "OK %s" % self.vals["RemoteMode"]
                else:
                    return "ERROR BadRemoteMode \"%s\"" % argument
            elif self.vals["RemoteMode"] == LocalState:
                return "ERROR RemoteModeIsLocal"
                
            elif parameters.startswith("Timer"):
                if parameters.startswith("TimerTarget"):
                    try:
                        target = getNextArg(parameters, "TimerTarget")
                    except ValueError:
                        # Fall through to the logic for Timer
                        pass
                    else:
                        if self.regulating() and self.vals["Timer"] == OnState:
                            return "ERROR TimerIsRunning"
                        
                        # This is the exact bounds checking performed by the
                        # device. If TimerTarget is set negative, it will 
                        # count down and wrap around at -2^31.
                        if (target > 2**31-1):
                            target = 2**31-1
                        elif (target < -2**31):
                            target = -2**31
                            
                        self.vals["PersistentTimerTarget"] = target
                        self.vals["TimerTarget"] = target
                        self.vals["CurrentTimer"] = target
                        return "OK %d" % target
                    
                argument = getNextArg(parameters, "Timer", isString=True)
                if argument == OnState or argument == OffState:
                    self.vals["PersistentTimer"] = argument
                    self.vals["Timer"] = argument
                    return "OK %s" % argument
                else:
                    return "ERROR BadOnOff \"%s\"" % argument
                    
            elif parameters.startswith("ValveVoltageMax"):    
                try:
                    target = getNextArg(parameters, "ValveVoltageMax", isFloat=True)
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target > MaxVoltage or target < MinVoltage:
                        # Note this is same behaviour as device, which reports 
                        # ValveVoltageMax for the Max value rather than the 
                        # actual maximum of 1000.0
                        return "ERROR OutOfRange %.2f Min %.2f Max %.2f" % (target, MinVoltage, self.vals["ValveVoltageMax"])
                    
                    self.vals["ValveVoltageMax"] = target
                    return "OK %.2f" % target
                    
            elif parameters.startswith("ValveVoltage"):
                try:
                    target = getNextArg(parameters, "ValveVoltage", isFloat=True)    
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target > self.vals["ValveVoltageMax"] or target < MinVoltage:
                        return "ERROR OutOfRange %.2f Min %.2f Max %.2f" % (target, MinVoltage, self.vals["ValveVoltageMax"])
                    else:
                        # We report success now no matter what, but we only 
                        # actually change the value if in Standby or Error.
                        if not self.regulating():
                            self.vals["ValveVoltage"] = target
                            
                        return "OK %.2f" % target
                    
            elif parameters.startswith("ValueKP"):
                if self.regulating():
                    return "ERROR RegulationIsRunning"
                    
                try:
                    target = getNextArg(parameters, "ValueKP", isFloat=True)
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target < MinKP or target > MaxKP:
                        return "ERROR OutOfRange %.1e Min %.1e Max %.1e" % (target, MinKP, MaxKP)
                    else:
                        self.vals["ValueKP"] = target
                        return "OK %.1e" % target
                
            elif parameters.startswith("ValueKI"):
                if self.regulating():
                    return "ERROR RegulationIsRunning"
                    
                try:
                    target = getNextArg(parameters, "ValueKI", isFloat=True)
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target < MinKI or target > MaxKI:
                        return "ERROR OutOfRange %.1e Min %.1e Max %.1e" % (target, MinKI, MaxKI)
                    else:
                        self.vals["ValueKI"] = target
                        return "OK %.1e" % target
                        
            elif parameters.startswith("RegulationTimeout"):
                try:
                    target = getNextArg(parameters, "RegulationTimeout")
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target < MinTimeout or target > MaxTimeout:
                        return "ERROR OutOfRange %d Min %d Max %d" % (target, MinTimeout, MaxTimeout)
                    else:
                        self.vals["RegulationTimeout"] = target
                        return "OK %d" % target
                
            elif parameters.startswith("PressureTarget"):
                try:
                    target = getNextArg(parameters, "PressureTarget", isFloat=True)
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target < MinPressure or target > MaxPressure:
                        return "ERROR OutOfRange %.1e Min %.1e Max %.1e" % (target, MinPressure, MaxPressure)
                    else:
                        self.vals["PressureTarget"] = target
                        return "OK %.1e" % target
                
            elif parameters.startswith("PressureTolerance"):
                try:
                    target = getNextArg(parameters, "PressureTolerance")
                except:
                    return "ERROR BadParameter \"%s\"" % parameters
                else:
                    if target < MinTolerance or target > MaxTolerance:
                        return "ERROR OutOfRange %d Min %d Max %d" % (target, MinTolerance, MaxTolerance)
                    else:
                        self.vals["PressureTolerance"] = target
                        return "OK %d" % target
                
            elif parameters.startswith("Regulation"):
                argument = getNextArg(parameters, "Regulation", isString=True)
                # These transitions have been tested to behave correctly
                # regardless of the current state - in particular, the 
                # side effects of the transitions should be triggered
                # even if we are already in that state (so for example 
                # sending "SET Regulation On" while in InProgress should 
                # reset the regulation timeout). 
                if argument == OnState:
                    self.enterInProgressMode()    
                    return "OK On"
                elif argument == OffState:
                    self.enterStandbyMode()
                    return "OK Off"
                else:
                    return "ERROR BadOnOff \"%s\"" % argument
            
            else:
                return "ERROR BadParameter \"%s\"" % parameters         
        elif command == "GET" or command == "SET":
            # Special case for the "NoParameter" error
            return "ERROR NoParameter"
        else:
            return "ERROR BadCommand \"%s\"" % command

    def enterStandbyMode(self):
        self.vals["Status"] = StandbyMode
        self.vals["TimerTarget"] = self.vals["CurrentTimer"]
        self.vals["ValveVoltage"] = MinVoltage
    def enterInProgressMode(self):
        self.vals["Status"] = InProgressMode
        # This is slightly inaccurate since in the real device voltage doesn't 
        # actually get set to 0.0 when we enter InProgress from Regulating, 
        # but it does in any other case.
        self.vals["ValveVoltage"] = MinVoltage
        self.vals["TimeoutCounter"] = self.vals["RegulationTimeout"]
    def enterRegulatingMode(self):
        self.vals["Status"] = RegulatingMode
    def enterErrorMode(self):
        self.vals["Status"] = ErrorMode
        self.vals["TimerTarget"] = self.vals["CurrentTimer"]
        self.vals["ValveVoltage"] = MinVoltage
        
    def currentPressure(self):
        pressure = VGradient * self.vals["ValveVoltage"] + PIntercept
        return pressure
        
    def pressureIsInsideTolerance(self):
        upperBound = self.vals["PressureTarget"] * (1.0 + self.vals["PressureTolerance"]/100.0)
        lowerBound = self.vals["PressureTarget"] * (1.0 - self.vals["PressureTolerance"]/100.0)
        current = self.currentPressure()
        if (current < upperBound and current > lowerBound):
            return True
        else:
            return False
            
    def adjustVoltage(self):
        ratio = self.currentPressure()/self.vals["PressureTarget"]
        if abs(ratio) < 1.0:
            newVoltage = self.vals["ValveVoltage"] - VIncrement
            if newVoltage < MinVoltage:
               newVoltage = MinVoltage
            self.vals["ValveVoltage"] = newVoltage
        elif abs(ratio) > 1.0:
            newVoltage = self.vals["ValveVoltage"] + VIncrement
            if newVoltage > self.vals["ValveVoltageMax"]:
                newVoltage = self.vals["ValveVoltageMax"]
            self.vals["ValveVoltage"] = newVoltage
            
    def regulating(self):
        if self.vals["Status"] == RegulatingMode or self.vals["Status"] == InProgressMode:
            return True
        else:
            return False


if __name__ == "__main__":
    # little test function that runs only when you run this file
    dev = my_device()
    dev.start_ip(9004)
    dev.start_debug(9006)
    # do a raw_input() to stop the program exiting immediately
    while 1 :
        time.sleep(1)
