#!/bin/env python2.6

from pkg_resources import require
require('dls_serial_sim')
from dls_serial_sim import serial_device, CreateSimulation

class strainGauge(serial_device):
    Terminator = "\r"
    randomMessages = ["?randomerror1", "?randomerror2", "?randomerror3"]
    randomMessagesIndex = 0
    highLimit = "000100"
    lowLimit = "900050"
    filteredValue = "51.2"
    unfilteredValue = "50.8"
       
    def __init__(self):
        '''Constructor.  Remember to call the base class constructor.'''
        serial_device.__init__(self)
        #self.schedule(self.reportError,5)
        print "Initialising strainGauge simulator, V1.0"
        return
    
    def reportError(self):
        result = self.randomMessages[self.randomMessagesIndex]
        self.randomMessagesIndex = (self.randomMessagesIndex + 1)%3
        return result
        
    def reply(self, command):
        '''This function must be defined. It is called by the serial_sim system
        whenever an asyn command is send down the line. Must return a string
        with a response to the command or None.'''
        if self.diagnosticLevel() > 4:
            print "Rx: %s"%[command]
        result = None
        # Un-filtered value:
        if command == "*X01":
            result = "X01 " + self.unfilteredValue
        # Filtered value:
        elif command == "*X04":
            result = "X04 " + self.filteredValue
        # Alarm 1 value (low limit):
        elif command == "*R23":
            result = "R23 " + self.lowLimit
        # Alarm 2 value (high limit):
        elif command == "*R24":
            result = "R24 " + self.highLimit
        return result

    def command(self, text):
        '''Interface function for commands from the test suite.'''
        args = text.split()
        # Simulate limits being changed on the controller
        if args[0] == "highLim":
            self.highLimit = args[1]
        elif args[0] == "lowLim":
            self.lowLimit = args[1]
        elif args[0] == "filteredValue":
            self.filteredValue = args[1]
        elif args[0] == "unfilteredValue":
            self.unfilteredValue = args[1]
        else:
            serial_device.command(self, text)
 
        
if __name__=="__main__":
    CreateSimulation(strainGauge)
    raw_input()
