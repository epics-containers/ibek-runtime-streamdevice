#!/bin/env dls-python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

#################################
# Test suite for the ODPsu module
    
class ODPsuTestSuite(TestSuite):
    
    def createTests(self):
        # Define the targets for this test suite
        Target("simulation", self, simulationCmds=['data/ODPsu_sim.py -i 8001 -d 9001'],
            iocDirectory="iocs/example_sim",
            iocBootCmd="bin/linux-x86/stexample.sh",
            runIocInScreenUnderHudson=True,
            #epicsDbFiles="db/example.expanded.db",
            simDevices=[SimDevice("controller1", 9016)],
            guiCmds=['edm -m "P=RJQ35657,Q=:BM" -eolc -x data/ODPsu-MX.edl'])
        Target("hardware", self,
            iocDirectory="iocs/example_sim",
            iocBootCmd="bin/linux-x86/stexample.sh",
            epicsDbFiles="db/example.expanded.db",
            guiCmds=['edm -m "P=RJQ35657,Q=:BM" -eolc -x data/ODPsu-MX.edl'])

        # The tests
        CaseSetSlewRate(self)
        CaseIncreaseHfmOutput(self)
        CaseGoOverLimit(self)


################################################
# Test cases
class CaseIncreaseHfmOutput(TestCase):
    def runTest(self):
        self.putPv("RJQ35657:BM:OUTPUT:SET","Off", timeout=200)
        self.verifyPv("RJQ35657:BM:OUTP:SEV", 2) # success
        
        self.putPv("RJQ35657:BM:V0D" ,100, timeout = 5)
        self.verifyPv("RJQ35657:BM:V0DSEV", 2) # FAIL
        
        self.putPv("RJQ35657:BM:SLEW:SET", 100)
        self.putPv("RJQ35657:BM:SLEW2:SET", 100)
        
        self.putPv("RJQ35657:BM:OUTPUT:SET","On", timeout=200)
        self.verifyPv("RJQ35657:BM:OUTP:SEV", 2) # success

        intended = 100
        for i in range(14):
            self.putPv("RJQ35657:BM:V%dD" % i,intended, timeout = 200)
            self.verifyPv("RJQ35657:BM:V%dD" % i, intended)
            self.verifyPv("RJQ35657:BM:V%dDR" % i, intended)

        self.putPv("RJQ35657:BM:STEPSIZE:SET", 20)
        self.putPv("RJQ35657:BM:B0:INC", 1)

        for i in range(14):
            self.verifyPv("RJQ35657:BM:V%dDR" % i, intended + 20)

        self.putPv("RJQ35657:BM:B0MAX:SET" , 1500)
        
        self.putPv("RJQ35657:BM:V0D" ,1490)
        # should fail because the difference between channels 0 and 1 is
        # greater than 450 V
        self.verifyPv("RJQ35657:BM:V0DSEV", 2) # FAIL
        self.verifyPv("RJQ35657:BM:V0DR" ,120) # should be old value


class CaseGoOverLimit(TestCase):
    def runTest(self):
        self.putPv("RJQ35657:BM:OUTPUT:SET","On", timeout=200)
        self.putPv("RJQ35657:BM:B0MAX:SET" , 1000)
        self.verifyPv("RJQ35657:BM:B0MAX", 1000)
        self.putPv("RJQ35657:BM:V0D" ,120, timeout = 200)
        self.verifyPv("RJQ35657:BM:V0D" , 120)
        self.verifyPv("RJQ35657:BM:V0DR", 120)
        
        self.putPv("RJQ35657:BM:STEPSIZE:SET", 20)
        self.putPv("RJQ35657:BM:B0MAX:SET" , 130)  
                          
        self.putPv("RJQ35657:BM:B0:INC", 1)

        # should still be 120, because it would otherwise go over the
        # limit
        self.verifyPv("RJQ35657:BM:V0DR" , 120 )

class CaseSetSlewRate(TestCase):
    def runTest(self):
        self.putPv("RJQ35657:BM:SLEW:SET", 20, timeout=200)
        self.sleep(15.0)
        self.verifyPv("RJQ35657:BM:SLEW", 20 )
        
class CaseSetFormat(TestCase):
    def runTest(self):
        self.putPv("RJQ35657:BM:FMT:GET", 0) # read format 0
        self.putPv("RJQ35657:BM:B0MAX:SET", 1500)
        self.putPv("RJQ35657:BM:B1MAX:SET", 1500)
        
        for i in range(22):
            self.putPv("RJQ35657:BM:FMT:V%dD" % i, 1490)
        self.putPv("RJQ35657:BM:FMT:SET", 1) # set format
        self.verifyPv("RJQ35657:BM:FMTDSEV", 1) # OK
        self.verifyPv("RJQ35657:BM:FMTDSEV2",1) # OK
        self.putPv("RJQ35657:BM:FORMAT:SET", 0) # set format 0
        
        

################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    ODPsuTestSuite()

    
