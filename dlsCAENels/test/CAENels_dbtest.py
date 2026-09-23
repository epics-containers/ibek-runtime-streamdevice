'''
    2015 - Nicoletta De Maio
'''

from pkg_resources import require
require('dls_autotestframework==2.16')
from dls_autotestframework import *

from CAENels_cases import *
import pyclbr


class CAENelsSimDbTestSuite( TestSuite ):
    '''Test suite for the CAENels HV-Adaptos high-voltage power supply EPICS database'''

    def loadCasePlugins( self, testclasses ):
        '''The ideas in this method were shamelessly copied from lakeshore340_test.py'''

        classes = pyclbr.readmodule( 'CAENels_cases' )

        for c in classes:

            if not ( c.endswith( 'TestCase' ) ):
                classobj = eval( c )

                if issubclass( classobj, TestCase ):
                    testclasses.append( classobj )

    def createTests(self):
        '''Define the targets for this test suite'''

        Target( 'simulation', self, [
                BuildEntity( 'dlsCAENels' ),
                IocEntity( 'ioc', directory='iocs/example_sim', bootCmd='./bin/linux-x86_64/stexample.sh' ),
                SimulationEntity( 'controller1', directory='etc/simulations', runCmd='dls-python ./CAENels_sim.py' )] )

        testclasses = []
        self.loadCasePlugins( testclasses )

        for testclass in testclasses:
            testclass( self )


if __name__ == '__main__':
    '''Create and run the test sequence'''
    CAENelsSimDbTestSuite()