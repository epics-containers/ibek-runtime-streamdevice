'''
    2015 - Nicoletta De Maio
'''

from CAENels_sim_cases import *
from unittest import TestSuite, TextTestRunner
import pyclbr, socket


class CAENelsSimTestSuite( TestSuite ):
    '''Test suite for the simulation of the CAENels HV-Adaptos high-voltage power supply'''

    def __init__( self ):
        super( CAENelsSimTestSuite, self ).__init__()

        # Initialise connection to the simulation
        self.connection = socket.socket()
        self.connection.connect( ( 'localhost', 5555 ) )

        # Define the targets for this test suite
        self.loadCasePlugins( self.connection )


    def loadCasePlugins( self, connection ):
        '''The skeleton of this method was shamelessly copied from lakeshore340_test.py'''
        classes = pyclbr.readmodule( 'CAENels_sim_cases' )

        for c in classes:

            if not ( c.endswith( 'TestCase' ) ):
                classobj = eval( c )
                classinstance = classobj( connection )
                self.addTest( classinstance )



if __name__ == '__main__':
    '''Create and run the test sequence'''
    ts = CAENelsSimTestSuite()
    r = TextTestRunner()
    r.run(ts)
