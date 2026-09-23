#!/dls_sw/prod/tools/RHEL5/bin/python2.6

# Test suite to use with pyUnit

from pkg_resources import require
require('dls_autotestframework')
from dls_autotestframework import *

################################################
# Test suite for the OxInstIPS Oxford Instruments superconducting magnet power supply controller.
    
class OxInstIPSTestSuite(TestSuite):

    def createTests(self):
        # Define the targets for this test suite
        # The ioc has to be started with screen for the sake of interfacing with Hudson, the integration engine.
        # Something to do with what happens to the IOC stdin.
        Target("simulation", self, entities=[\
            IocEntity('ioc', directory="iocs/example_sim", bootCmd="bin/linux-x86/stexample.sh"),
            EpicsDbEntity('db', directory="iocs/example_sim", fileName="db/example_expanded.db"),
            BuildEntity('OxInstIPS'), 
            SimulationEntity('SIM-TS-PS-01', runCmd='etc/simulations/OxInstIPS_sim.py -i 9015 -r 9016', rpcPort=9016),
            GuiEntity('gui',  runCmd='edm -m "P=SIM-EA-MAGPS-01,device=SIM-EA-MAGPS-01" -eolc -x data/OxInstIPSMain.edl')
            ])
        Target("hardware", self, entities=[\
            IocEntity('ioc', directory="iocs/example", bootCmd="bin/linux-x86/stexample.sh"),
            EpicsDbEntity('db', fileName="db/example_expanded.db"),
            BuildEntity('OxInstIPS'),            
            GuiEntity('gui', runCmd='edm -m "P=SIM-EA-MAGPS-01,device=SIM-EA-MAGPS-01" -eolc -x data/OxInstIPSMain.edl')
            ])
        
        # The tests
        CaseIdentifySystem(self)
#        CaseGetSensorTemperatures(self)
#        CasePowerOffOn(self)
#        CaseGetSensorRawReadings(self)
#        CaseGetSensorTemperatureStatistics(self)
#        CaseChangeLoopSetpoints(self)
#        CaseChangeLoopTypes(self)
#        CaseChangeLoopManualOutputs(self)
#        CaseChangeLoopPIDs(self)
#        CaseSystemStats(self)
#        CaseResetSystemStats(self)
        return

################################################
# Intermediate test case class that provides some utility functions
# for this suite

class OxInstIPSCase(TestCase):
    # This arg_a is needed for the parent class constructor.
    def __init__(self, arg_a):
        '''Constructor.  First calls the base class constructor.'''
        TestCase.__init__(self , arg_a)
        self.pvPrefix = "SIM-EA-MAGPS-01:"
        return
        
    def dummy(self):
        ''' Dummy for now til I think of some common functions.
        '''
        return
    
################################################
# Test cases
#
# Not at all written yet.
#
# -----------------------------------------------
# System tests

class CaseIdentifySystem( OxInstIPSCase ):
    def runTest(self):
        '''Get the unit to identify itself.'''
        print "Version = " + self.getPv(self.pvPrefix + "VERSION")
        return
    
################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    OxInstIPSTestSuite()

