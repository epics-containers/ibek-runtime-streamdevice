#!/bin/env python2.6

import time
from pkg_resources import require
require('dls_serial_sim')
from dls_serial_sim import serial_device, CreateSimulation
#from autotestframework import serial_device
import re, os, time

class OxInstIPS(serial_device):
    Terminator = "\n"
    
    def __init__(self):
        '''Constructor.  Remember to call the base class constructor.'''
        # See file OxInstIPS.protocol for comment on what these functions do.
        serial_device.__init__(
            self,
            protocolBranches = ["getVersion" ,
                                "getDemandCurrent" ,
                                "getSupplyVoltage" ,
                                "getMeasuredMagnetCurrent",
                                "getSetPointCurrent",
                                "getCurrentSweepRate",
                                "getDemandField",
                                "getSetPointField",
                                "getFieldSweepRate",
                                "getSoftwareVoltageLimit",
                                "getPersistentMagnetCurrent",
                                "getTripCurrent",
                                "getPersistentMagnetField",
                                "getTripField",
                                "getHeaterCurrent",
                                "getNegCurrentLimit",
                                "getPosCurrentLimit",
                                "getLeadResistance",
                                "getMagnetInductance",
                               ])

        print "OxInstIPS_sim: Initialising."

        # The string seems to include a copyright symbol
        self.version = 'Simulation of IPS120-10 Version 123 \xc2\xa9 OXFORD INSTRUMENTS 1999'

        # Demand Current.
        self.R0 = 0.0
        # Measured power supply voltage
        self.R1 = 0.0
        # Measured magnet current.
        self.R2 = 0.0
        # Set point (target current).
        self.R5 = 0.0
        # Current sweep rate (amp/minute).
        self.R6 = 0.0
        # Demand field (output field).
        self.R7 = 0.0
        # Set point (target field).
        self.R8 = 0.0
        # Field sweep rate.
        self.R9 = 0.0
        # Software voltage limit.  Set in the configuration as S10.
        self.R15 = 20.0
        # Persistent magnet current.
        self.R16 = 0.0
        # Trip current.
        self.R17 = 0.0
        # Persistent magnet field.
        self.R18 = 0.0
        # Trip field.
        self.R19 = 0.0
        # Switch heater current (milliamp). Fixed property set in the configuration as S15.
        self.R20 = 5.0
        # Safe current limit, most negative.  Set in the configuration as S03.
        self.R21 = -100.0
        # Safe current limit, most positive.  Set in the configuration as S04.
        self.R22 = 100.0
        # Lead resistance.
        self.R23 = 7.0
        # Magnet inductance (henry).  This is a fixed property of the magnet entered
        # in configuration as S11.
        self.R24 = 5.2

        # Manual states relationship between current and field is linear.  Make up a calibration.
        # Amps/tesla.  Set in the configuration as S01.
        self.S01 = 10.7
        
        # Current supply current limit. Set in the configuration as S02.
        self.S02 = 110.0

        # There is also a load of stuff about sweep limiting choices.  Not implemented in simulation for now.

        # The protocol file at present has a carriage return character in its format
        # definition.  Need to test this against the real instrument to figure out
        # what is going on.

        print "OxInstIPS_sim: Initialised."
        return

    def getVersion(self):
        self.covered("getVersion")
        return self.version
    
    def getDemandCurrent(self):
        self.covered("getDemandCurrent")
        return self.R0

    def getSupplyVoltage(self):
        self.covered("getSupplyVoltage")
        return self.R1

    def getMeasuredMagnetCurrent(self):
        self.covered("getMeasuredMagnetCurrent")
        return self.R2
    
    def getSetPointCurrent(self):
        self.covered("getSetPointCurrent")
        return self.R5
    
    def getCurrentSweepRate(self):
        self.covered("getCurrentSweepRate")
        return self.R6
    
    def getDemandField(self):
        self.covered("getDemandField")
        return self.R7
    
    def getSetPointField(self):
        self.covered("getSetPointField")
        return self.R8
    
    def getFieldSweepRate(self):
        self.covered("getFieldSweepRate")
        return self.R9

    def getSoftwareVoltageLimit(self):
        self.covered("getSoftwareVoltageLimit")
        return self.R15

    def getPersistentMagnetCurrent(self):
        self.covered("getPersistentMagnetCurrent")
        return self.R16

    def getTripCurrent(self):
        self.covered("getTripCurrent")
        return self.R17

    def getPersistentMagnetField(self):
        self.covered("getPersistentMagnetField")
        return self.R18

    def getTripField(self):
        self.covered("getTripField")
        return self.R19
    
    def getHeaterCurrent(self):
        self.covered("getHeaterCurrent")
        return self.R20

    def getNegCurrentLimit(self):
        self.covered("getNegCurrentLimit")
        return self.R21

    def getPosCurrentLimit(self):
        self.covered("getPosCurrentLimit")
        return self.R22
    
    def getLeadResistance(self):
        self.covered("getLeadResistance")
        return self.R23

    def getMagnetInductance(self):
        self.covered("getMagnetInductance")
        return self.R24
    
    def reply(self, arg_command):
        '''This function must be defined. It is called by the serial_sim system
        whenever an asyn command is send down the line. Must return a string
        with a response to the command or None.'''
#        print "###REPLYING### to %s" %arg_command
        if self.diagnosticLevel() > 4:
            print "OxInstIPS_sim: Received command " + arg_command
        result = None

        my_command = arg_command.strip()

        if len(my_command) == 0:
            #if self.diagnosticLevel() > 1:
            print "OxInstIPS_sim: Empty command string."
            result = "? ERROR in command string."
            return result

        # Parse the command.
        # Grab the leading letter of the command, which is the command word.
        my_letter = my_command[0]
        
        if not my_letter.isupper() :
            print "OxInstIPS_sim: Faulty command letter syntax: " + my_letter + " is not an upper case letter."
            result = "? ERROR in command string."
            return result

        # Grab the rest of the string, which is the parameter if there is one.
        my_param = my_command[1:]

        if my_letter == "V":
            result = self.getVersion()
            self.covered("getVersion")
            if len(my_param) != 0:
                print "OxInstIPS_sim: Ignoring stray trailing syntax to V command: " + my_param
            
#       elif my_word == "R":
#            
# Try to grab integer index parameter to R command to find out which parameter.                        
#                else :
#                    if self.diagnosticLevel() > 2:
 #                       print "OxInstIPS_sim: no match to parameter " + my_param + " in word " + my_word + " in command " + my_command


        else :
            # No letter match if you get here.
            if self.diagnosticLevel() > 2:
                print "OxInstIPS_sim: no match to recognised letter command for " + my_letter + " in command " + my_command
            result = "? ERROR in command string."

        if self.diagnosticLevel() > 4:
            print "OxInstIPS: Returning result " + result
        if self.diagnosticLevel() > 2 and set:
            print "OxInstIPS: Returning result " + result

#        print "###REPLYING### %s->%s" %(arg_command,result) 
        return result
                                        
#    def initialise(self):
#        '''Called by the framework when the power is switched on.'''
#        self.on = 1

    # This is the backdoor.
    def command(self, text):
        '''Interface function for commands from the test suite.'''
        return

if __name__ == "__main__":
    CreateSimulation(OxInstIPS)
    while(True):
        time.sleep(1)
