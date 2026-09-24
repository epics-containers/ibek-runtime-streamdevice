#!/bin/env dls-python2.4

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

#import sys
#sys.path.append("/dls_sw/work/common/python/autotestframework")
#from src import *

from random import randrange as r

P = "TESTNX100:"

class Nx100TestSuite(TestSuite):
    def createTests(self):
        Target( "simulation", self, simulationCmds=['data/nx100_sim.py -i 8001 -r 9001 -d 9050'],
                iocDirectory="iocs/example_sim",
                iocBootCmd="bin/linux-x86/stexample.sh",
                runIocInScreenUnderHudson=True,          
                epicsDbFiles="db/example_expanded.db",
                simDevices=[SimDevice('Nx100',9001,rpc=True)],
                guiCmds=['edm -x -m "robot=%s" -eolc data/nx100.edl' % P[:-1]])
        CaseRunJob(self)
        CaseRunJobErr(self)
        

class Nx100TestCase( TestCase ):
                
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
        
class CaseRunJob(Nx100TestCase):
    def runTest(self):
        # start it
        self.putPv(P+"SVON", 1)           
        t = time.time()
        self.putPv(P+"START", 1, timeout=600)   
        diff = time.time() - t
        assert diff < 13 and diff > 12, "Job took %f seconds, should take about 12 seconds" % diff

class CaseRunJobErr(Nx100TestCase):
    def runTest(self):
        # start it
        self.putPvAndVerify(P+"SVON", 0, P+"STA2", 0, delay=1)           
        t = time.time()
        self.putPv(P+"START", 1)   
        diff = time.time() - t
        assert diff < 1, "Job took %f seconds, should take less than a second" % diff
        self.verifyPv(P+"ERR", 1111) 

if __name__ == "__main__":
    # Create and run the test sequence
    Nx100TestSuite()
