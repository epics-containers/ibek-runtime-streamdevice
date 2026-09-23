#!/bin/env dls-python2.4

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

#import sys
#sys.path.append("/dls_sw/work/common/python/autotestframework")
#from src import *

from random import randrange as r

P = "EUROTHERM2K:"

class Eurotherm2kTestSuite(TestSuite):
    def createTests(self):
        Target( "simulation", self, simulationCmds=['data/eurotherm2k_sim.py -i 8100 -r 9001'],
                iocDirectory="iocs/example_sim",
                iocBootCmd="bin/linux-x86/stexample.sh",
                runIocInScreenUnderHudson=True,          
                epicsDbFiles="db/example_expanded.db",
                simDevices=[SimDevice('eurotherm',9001,rpc=True)],
                guiCmds=['edm -x -m "eurotherm=%s" -eolc data/eurotherm2k.edl' % P[:-1]])
        CaseRamp(self)
        CasePowerOnOff(self)
        CasePIDs(self)
        

class Eurotherm2kTestCase( TestCase ):
                
    # Convenience function to set a PV and verify it has taken effect in the module.
    # The set PV will always be verified after put and if a readback PV has been specified
    # in rbvpv it's value will be verified against either the set value or rbvvalue if it
    # has been defined.
    # The optional delay parameter can be used between the putPv and the readback/verify.
    def putPvAndVerify(self, setpv, value, rbvpv = None, rbvvalue = None, validrange=None, delay=None, delta=0.0):
        self.putPv( setpv, value )
        if delay!=None:
            self.sleep(delay)
        self.verifyPv( setpv, value )
        if ( rbvpv ):
            verifyvalue = value
            if rbvvalue!=None:
                verifyvalue = rbvvalue
            #print "Verify PV: %s against value: %s"%(rbvpv, str(verifyvalue))
            if type(verifyvalue)==float:
                self.verifyPvFloat( rbvpv, verifyvalue, delta )
            else:
                self.verifyPv( rbvpv, verifyvalue )
                
    def ramp(self, ramp, rr = 0.5):                
        # set ramp rate to 0.5 degrees / second     
        self.putPvAndVerify(P+"RR", rr, P+"RR:RBV", delay=1.0)
        # work out how long to wait
        current = self.getPv(P+"PV:RBV")
        new = r(60.0,80.0)
        time = abs(new - current) / rr
        # check it ramps
        self.putPvAndVerify(P+"SP", new, P+"PV:RBV", delay = time + 1.0)    
        
class CaseRamp(Eurotherm2kTestCase):
    def runTest(self):
        # first enable it
        self.putPv(P+"DISABLE", 0)   
        # now set the update rate
        self.putPv(P+"UPDATE.SCAN", "1 second")           
        # now ramp it
        for x in range(2):        
            self.ramp(r(60.0,80.0))

class CasePowerOnOff(Eurotherm2kTestCase):
    def runTest(self):
        self.simulation('eurotherm').power = True
        # first enable it
        self.putPv(P+"DISABLE", 0)   
        # now ramp it
        self.ramp(r(60.0, 80.0))
        # now turn it off
        self.simulation('eurotherm').power = False
        # set the value
        self.simulation('eurotherm').vals["S1"] = 40.0
        self.simulation('eurotherm').vals["PV"] = 40.0        
        # wait
        self.sleep(2)
        # turn it back on
        self.simulation('eurotherm').power = True
        # wait
        self.sleep(1)        
        
        # check it's the right value
        self.verifyPv(P+"PV:RBV", 40.0)
        

class CasePIDs(Eurotherm2kTestCase):
    def runTest(self):
        # first enable it
        self.putPv(P+"DISABLE", 0)   
        # now set the update rate
        self.putPv(P+"PID.SCAN", "10 second")           
        # set a random value for PIDs
        for x in range(10):
            for x in "PID":
                new = r(0.0,150.0)
                # check it sets and gets
                self.putPvAndVerify(P+x, new, P+x+":RBV", delay = 0.1)


if __name__ == "__main__":
    # Create and run the test sequence
    Eurotherm2kTestSuite()
