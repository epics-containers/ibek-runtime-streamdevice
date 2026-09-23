#!/bin/env dls-python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

################################################
# Test suite for the strainGauge module
    
class StrainGaugeTestSuite(TestSuite):

    def createTests(self):
        # Define the targets for this test suite
        Target("simulation", self, simulationCmds=['data/strainGauge_sim.py -i 8001 -d 9001'],
            iocDirectory="iocs/example_sim",
		runIocInScreenUnderHudson=True,
            iocBootCmd="bin/linux-x86/stexample.sh",
            epicsDbFiles="db/example_expanded.db",
            simDevices=[SimDevice("gauge1", 9001)],
            guiCmds=['edm -m "P=TEST-GAUGE,gauge=-01" -eolc -x data/strainGaugeLimits.edl'])
        Target("hardware", self,
            iocDirectory="iocs/example",
            iocBootCmd="bin/linux-x86/stexample.sh",
            epicsDbFiles="db/example_expanded.db",
            guiCmds=['edm -m "P=TEST-GAUGE,gauge=-01" -eolc -x data/strainGaugeLimits.edl'])

        # The tests
        CaseVerifyLimits(self)
        CaseChangeLimits(self)
        

################################################
# Test cases
    
# Make sure that the limits make sense, i.e. low limit < high limit
class CaseVerifyLimits(TestCase):
    def runTest(self):
        lowLim = self.getPv("TEST-GAUGE-01:LOWLIMIT")
        print "***LOW LIMIT = ", lowLim
        highLim = self.getPv("TEST-GAUGE-01:HIGHLIMIT")
        print "***HIGH LIMIT = ", highLim
        limitsGood = lowLim < highLim
        self.verify(limitsGood,1)    

            
# Change the limits and ensure that the records go into
# HIHI / LOLO alarm state
class CaseChangeLimits(TestCase):
    def runTest(self):
        self.command("gauge1","filteredValue 500")
        self.command("gauge1","unfilteredValue 501")
        # Wait for records to be updated
        self.sleep(2)
        self.verifyPv("TEST-GAUGE-01:POLLVALUE.STAT", 3)
        self.verifyPv("TEST-GAUGE-01:FILTEREDVALUE.STAT", 3)
        
        self.command("gauge1","filteredValue -500")
        self.command("gauge1","unfilteredValue -501")
        self.sleep(2)
        self.verifyPv("TEST-GAUGE-01:POLLVALUE.STAT", 5)
        self.verifyPv("TEST-GAUGE-01:FILTEREDVALUE.STAT", 5)
                
################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    StrainGaugeTestSuite()

    
