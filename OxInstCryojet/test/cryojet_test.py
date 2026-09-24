#!/bin/env dls-python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

################################################
# Test suite for the Cryojet 
    
class CryojetTestSuite(TestSuite):

    def createTests(self):
        # Define the targets for this test suite
        Target("simulation", self,
            iocDirectory="example",
            iocBootCmd="bin/linux-x86/stexample_sim.boot",
            epicsDbFiles="db/example.db",
            simDevices=[SimDevice("controller1", 9006)],
            environment=[('EPICS_CA_REPEATER_PORT','6065'), ('EPICS_CA_SERVER_PORT','6064')],
            guiCmds=['edm -x -eolc -m "P=TS-EA-CJET-01,Q=\'\'" data/cryojet.edl'],
            simulationCmds=['data/OxInstCryojet_sim.py -i 9005 -d 9006'])
        Target("hardware", self,
            iocDirectory="example",
            iocBootCmd="bin/linux-x86/stexample.boot",
            epicsDbFiles="db/example.db",
            guiCmds=['edm -x -eolc -m "P=TS-EA-CJET-01,Q=\'\'" data/cryojet.edl'])

        # The tests
        CaseSetTarget(self)
        CaseCheckReadbacks(self)
        
################################################
# Intermediate test case class that provides some utility functions
# for this suite

class CryojetCase(TestCase):
    
    def enable(self):
        self.putPv("TS-EA-CJET-01:DISABLE", 0)
            
    def currTemp(self):
        ''' Get the current temperature from the device simulation
        '''
        result = 0
        self.command("controller1", "getcurrtemp")
        args = self.recvResponse("controller1", "currtemp", 1)
        if args is not None:
            result = int(args[0])
        return result

    def verifyTemp(self, intended):
        ''' Verify temperature
        '''
        if self.simulationDevicePresent("controller1"):
            self.verifyInRange(self.currTemp(), intended-0.1, intended+0.1)
        self.verifyPvInRange("TS-EA-CJET-01:STEMP", intended-0.1, intended+0.1)
        self.verifyPv("TS-EA-CJET-01:TTEMP", intended)

    def setValues(self, setpv, getpv, intended):
        for i in intended:
            # Now advance the wheel using channel access
            self.diagnostic("setPV %s, %f" % (setpv, i), 1)
            self.putPv(setpv, i)
            # Check readback
            self.sleep(2)
            self.verifyPv(getpv, i)
        
################################################
# Test cases
    
# The local increment switch
class CaseSetTarget(CryojetCase):
    def runTest(self):
        '''set pv and check readback pv'''
        self.enable()
        self.setValues("TS-EA-CJET-01:TTEMP:SET", "TS-EA-CJET-01:TTEMP", [1,3,10,999.9])
        self.setValues("TS-EA-CJET-01:P:SET", "TS-EA-CJET-01:P", [1,3,10,999.9])
        self.setValues("TS-EA-CJET-01:I:SET", "TS-EA-CJET-01:I", [1,3,10,9999.9])
        self.setValues("TS-EA-CJET-01:D:SET", "TS-EA-CJET-01:D", [1,3,10,9999.9])
        self.setValues("TS-EA-CJET-01:D:SET", "TS-EA-CJET-01:D", [1,3,10,9999.9])
        self.setValues("TS-EA-CJET-01:SHIELDFLW:SET", "TS-EA-CJET-01:SHIELDFLW", [1,3,10,99.9])
        self.setValues("TS-EA-CJET-01:SAMPLEFLW:SET", "TS-EA-CJET-01:SAMPLEFLW", [1,3,10,99.9])
        self.setValues("TS-EA-CJET-01:CTRL:SET", "TS-EA-CJET-01:CTRL", [0,1,2,3,1])
        self.setValues("TS-EA-CJET-01:ACTIVITY:SET", "TS-EA-CJET-01:ACTIVITY", [0,1,0])
        self.setValues("TS-EA-CJET-01:MAXV:SET", "TS-EA-CJET-01:MAXV:SET", [0,99.9])
        self.setValues("TS-EA-CJET-01:MANV:SET", "TS-EA-CJET-01:MANV:SET", [0,99.9])

class CaseCheckReadbacks(CryojetCase):
    def runTest(self):
        '''check readback pv'''
        self.enable()
        self.verifyPvInRange("TS-EA-CJET-01:CHANFREQ", 1, 10000)
        self.verifyPvInRange("TS-EA-CJET-01:HEATERP", 1, 100)
        self.verifyPvInRange("TS-EA-CJET-01:HEATERV", 0, 10)

            
################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    CryojetTestSuite()

    
