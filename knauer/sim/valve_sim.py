#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
'''
    Simulator for Knauer Azura V2.1S valve
    2016 - Andrew Wilson
    Based on dlsCaenEls simulator by Nicoletta de Maio
'''


from pkg_resources import require
require('dls_serial_sim==1.17')
from dls_serial_sim import serial_device
require('dls_simulationlib==3.1')
from dls_simulationlib.beamline import Beamline

import math, random, re

random.seed( 0xcaffe )


def generate_random(maximum, rounded=True):
    '''generate a random status response (0 or 1)'''
    res = random.uniform( 0, maximum )
    if rounded:
        res = math.floor( res )
        res = int( res )
#    res = str( res )
    return res

class knauerDummyBeamline( Beamline ):
    '''This is just a dummy class to run the device in'''
    def createSimulation( self ):
        self.hvadaptos = knauer()


class knauer( serial_device ):
    '''
        TODO: description of class here - simulates communication only, command handlers are stubs, no sanity checking wrt #channels and channel number, etc.
    '''
    errors = { 0              : 'System error',
               16             : 'Invalid command',
               17             : 'Invalid parameter)s)',
               20             : 'Instrument in standalone mode',
               21             : 'Instrument in standby mode',
               27             : 'Instrument remote controlled',
               58             : 'Sum of component is not 100',
               59             : 'Maximum pressure: System stopped',
               60             : 'Minimum pressure: System stopped',
    }



    # Serial protocol
    Terminator = '\r'
    # Temporary terminator for use with Telnet
    #Terminator = "\r\n"

    def __init__( self, name="knauer", ui=None, tcpPort=5556 ):
        self.name = name
        self.tcpPort = tcpPort
        serial_device.__init__( self, ui=ui )
        self.start_ip( tcpPort )
        # Status at startup
        self.currentPosition = 1;

    def reply( self, command ):
        '''This function must be defined. It is called by the serial_sim system
        whenever an asyn command is send down the line. Must return a string
        with a response to the command or None.'''
        self.diagnostic( "Rx: %s" % repr( command ), 4 )
        print "Received request ", command
        handler = None
        result = None

        if command is None:
            return None
        
        # Reusable bits of regex and string
        begin = r"^"
        #findAddress = r"(?P<address>[:ab])"
        #findSide = r"(?P<side>[BC]?)"
        #findSteps = r"(?P<steps>[0-9]+)"
        #findSpeed = r"(?P<speed>[0-9]+)"
        #findValvePos = r"(?P<valvePos>[xIWO])"
        #execute = r"R"
        end = r"$"
        echo = command# + "\r"
        ack = "OK"
        
        # Prepare a list of regex patterns to check commands for
        patterns = {}
        
        patterns["identify?"] =         begin + r"IDENTIFY\?" + end
        patterns["goTo"] =              begin + r"(?P<newPos>[0-9])" + end
        patterns["goHome"] =            begin + r"H" + end
        patterns["reportPosition"] =    begin + r"P" + end
        
        # Try each pattern and drop out if we find a match
        matchedPattern = None
        for key, pattern in patterns.iteritems():
            matches = re.match(pattern, command)
            if (matches is not None):
                matchedPattern = key
                break
         
        if matchedPattern == "identify?":
        
            # Set flag to denote addressing has been done
            self.addressed = True
            
            valve_type_choices = ["VALVE LI","VALVE 6","VALVE 12","VALVE 16"]
            # Deal with only one unit for now
            st_magic_number     = 7
            st_manufacturer     = "Knauer"
            st_valve_type_key   = 1 # generate_random(3)
            st_valve_type       = valve_type_choices[st_valve_type_key]
            st_serial_num       = generate_random(99999)
            st_firmware_high    = generate_random(99999)
            st_firmware_low     = generate_random(99999)
  
            result = "IDENTIFY:{0},{1},{2},{3},{4},{5}".format(st_magic_number,
                                                        st_manufacturer,
                                                        st_valve_type,
                                                        st_serial_num,
                                                        st_firmware_high,
                                                        st_firmware_low)

        elif matchedPattern == "goTo":
            
            newPos = int(matches.group("newPos"))
            
            if (newPos <= 0 or newPos > 6):
                err = self.format_error(17)
                print err
                result = err
            else:
                print "Moving to position ", newPos
                self.currentPosition = newPos
                result = "OK"
            
        elif matchedPattern == "goHome":
            result = "OK"
            self.currentPosition = "1"
            print "Moving to home position (1)"
            
        elif matchedPattern == "reportPosition":
            
            result = "{0}".format(self.currentPosition)
            
        else:
        
            # Handle unrecognised commands
            err = self.format_error(16)
            
            # Debug for console
            print err
            
            # Don't think the controller says anything:
            # Return an empty string
            result = err


        if result is not None:
            self.diagnostic( "Tx: %s" % repr( result ), 4 )
            print "Tx: ", result

        else:
            print "No result. (?!)"

        return result

    def format_error(self, index ):
        
        if (self.errors[index] is None):
            index = 16
        ret = "ERROR:{0},{1}".format(index, self.errors[index])
        
        return ret


    def value_valid_double( self, value ):

        try:
            float( value )
            return True

        except ValueError:
            return False

    def value_valid_int( self, value ):

        try:
            int( value )
            return True

        except ValueError:
            return False


if __name__ == "__main__":
    hvps = knauerDummyBeamline( 'HVAdaptos' )
