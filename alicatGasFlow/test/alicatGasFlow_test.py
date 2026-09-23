#!/dls_sw/tools/bin/python2.4

#from pkg_resources import require
#require('dls.autotestframework')
#from dls.autotestframework import *
import sys
sys.path.append("/dls_sw/work/common/python/autotestframework")
from src import *

macros = {'P': 'UP45',
          'S': 'ONE',
          'PORT': 'asynport',
          'simport': 9001,
          'rpcport': 9002}

class ReadBackPv:
    def __init__(self, testcase, pvname, value=None, delta=None, validrange=None):
        self.pvname = pvname
        self.value = value
        if delta==None:
            self.delta = 0.0
        else:
            self.delta = delta
        self.validrange = validrange
        self.testcase = testcase
    
    def verify(self, value = None):
        valtype = type(self.value)
        val = self.value
        tc = self.testcase
        
        if self.value == None:
            val = value
        if val == None:
            tc.fail( "ReadBackPv.verify() verify-value %s not valid!"%str(val))
            return
             
        if valtype == float:
            if self.delta != None:
                tc.verifyPvFloat( self.pvname, val, self.delta)
            elif self.validrange != None:
                (lower, upper) = self.validrange
                tc.verifyPvInRange( self.pvname, val, lower, upper )
        elif valtype == int:
            if self.validrange != None:
                (lower, upper) = self.validrange
                tc.verifyPvInRange( self.pvname, val, lower, upper )
            elif self.delta != None:
                tc.verifyPvFloat( self.pvname, float(val), self.delta )
            else:
                tc.verifyPv( self.pvname, val )
        elif valtype == str:
            tc.verifyPv( self.pvname, val )
        else:
            tc.fail( "ReadBackPv (%s, %s, %s, %s) not valid!"% \
                     (self.pvname, str(self.value), str(self.delta), str(self.validrange)))
    

class AlicatGasFlowTestSuite( TestSuite ):
    def createTests(self):
        Target( "simulation", self,
                iocDirectory="iocs/example_sim",
                iocBootCmd="screen -D -m -L bin/linux-x86_64/stexample.sh",
                epicsDbFiles="db/example.expanded.db",
                simDevices=[SimDevice(macros['PORT'], macros['rpcport'], rpc=True)],
                guiCmds=['edm -x -m "P=%s,S=%s" -eolc data/alicatGasFlow.edl'%(macros['P'],macros['S'])])
        for i in range(1):
            CaseChangeGasType( self )
        CaseSetZero( self )

class AlicatGasFlowTestCase( TestCase ):
    # Build up the full PV names of all the records in the database
    basePvName = macros['P']+macros['S']
    pvGas    = basePvName+':SELECTGAS'
    pvGasRbv = basePvName+':GAS'
    pvFlow   = basePvName+':FLOW'
    pvSetZero= basePvName+':SETZERO'
    
    # PVs that are only used as part of the db logic but not
    # seen by end-user
    pvCalc   = basePvName+':CALC'
        
    # mbbinary options
    gasTypes = {0: r'Air',
                1: r'Argon',
                2: r'Methane',
                3: r'Helium',
                4: r'75% Ar 25% He',
                5: r'75% He 25% Ar'}

    def putPvAndVerify(self, setpv, value, rbvpvs, delay=0.0):
        '''Convenience function to set a PV and verify it has taken effect in the module.
           The set PV will always be verified after put and if a readback PV has been specified
           in rbvpv it's value will be verified against either the set value or rbvvalue if it
           has been defined.
           The optional delay parameter can be used between the putPv and the readback/verify.'''
        self.putPv( setpv, value )
        self.sleep(delay)
        for rbvpv in rbvpvs:
            rbvpv.verify( value )
    

class CaseChangeGasType( AlicatGasFlowTestCase ):
    '''Test Case to test the selection of all the gas types'''
    def runTest(self):
        listKeys = self.gasTypes.keys()
        listKeys.reverse()
        for gas in listKeys:
            rbvpv = ReadBackPv( self, self.pvGasRbv, self.gasTypes[gas] )
            self.putPvAndVerify( self.pvGas, gas, 
                                 [rbvpv], 
                                 delay=2.0)

class CaseSetZero( AlicatGasFlowTestCase ):
    '''Testing the set to zero command which clears the reading and sets
       the current cas flow level to be zero.'''
    def runTest(self):
        simdev = macros['PORT']
        simobj = self.simulation(simdev)
        simobj.simulationActive = False
        self.sleep(2.5)
        rbvpv = ReadBackPv( self, self.pvFlow, 0.0, 0.1 )
        for val in [1,0]:
            simobj.simulationActive = False
            self.sleep(2.5)
            self.putPvAndVerify( self.pvSetZero, val, [rbvpv], delay=2.5 )
            simobj.simulationActive = True
            self.sleep(2.5)
        

if __name__ == "__main__":
    # Create and run the test sequence
    AlicatGasFlowTestSuite()
