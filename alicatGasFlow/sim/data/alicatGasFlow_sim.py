from pkg_resources import require
#require('dls_serial_sim==1.7')
#from dls_serial_sim import serial_device
import sys
sys.path.append("/dls_sw/work/common/python/serial_sim")
from src import serial_device

#from autotestframework import serial_device
import re, os, time, math

class alicatGasFlowSim( serial_device ):
    Terminator = "\r"
    agfDebug = True
    
    # The state of the device is defined by the following three variables
    devId = "A"
    value = float(0.0)
    gasType = int(0)
    gasTypeToStr = {0: "Air", 1: "Argon", 2: "Methane", 7: "Helium", 25: "75% Ar 25% He", 26: "75% He 25% Ar" }
    
    def __init__(self):
        serial_device.__init__(self, protocolBranches = ["simulationActive"])
        self.msg( "Initialising alicatGasFlowSim simulator")
        self.startTime = time.time()
        self.simulationActive = True
        self.schedule(self.generateData, 0.5)
        return
        
    def generateData( self ):
        if not self.simulationActive:
            return
        t = time.time() - self.startTime
        f = 0.01
        self.value = math.sin(t * 2*math.pi*f) + 0.5
        
    def reply(self, command):
        self.msg("Got command: %s"%command)
        retstr = "response"
        # Init getData command
        if (command.find("*@=") >= 0):
            self.devId = command.split("=")[1]
            retstr = self.devId + " %.3f"%self.value
        # getData request for data
        elif (command == self.devId):
            retstr = "%c %.3f"%(self.devId, self.value)
        elif (command.find("%c$$"%self.devId) >= 0):
            tmp = command.split("$$")[1]
            # setZero command
            if (tmp == "V"):
                retstr = ""
                self.value = 0.0
                self.startTime = time.time()
            # gasSelect - and the output is read by getGas
            else:
                self.gasType = int( command.split("$$")[1] )
                retstr = "%c %.3f %s"%(self.devId, self.value, self.gasTypeToStr[ self.gasType ])
        self.msg("Responding with: %s"%retstr)
        return retstr
    
       
    # print debug statements
    def msg(self, msg):
        if self.agfDebug:
            print "alicatGasFlowSim: %s"%msg
        
