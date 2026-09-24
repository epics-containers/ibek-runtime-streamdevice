#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
'''
    Simulator for Knauer BlueShadow 40P pump & Azura V2.1S valve
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

    # Status at startup
    status =        { 'state'           : '6',
                      'current_error'   : 0,
                      'flow'            : 0,
                      'LPG_0'           : 100,
                      'LPG_1'           : 0,
                      'LPG_2'           : 0,
                      'LPG_3'           : 0,
                      'event'           : [0,0,0,0,0,0,0,0,0],
                      'pressure_kPa'    : 1234,
                      'start_in'        : 0,
                      'error_in'        : 0
    }
    
    # Some configuration params
    flow_max = 10000 # uL / min
    flow_min = 1     # uL / min
    
    # We'll keep a note of any errors
    error = None

    # Serial protocol
    Terminator = '\r'
    # Temporary terminator for use with Telnet
    #Terminator = "\r\n"
    
    # Device state at startup

    def __init__( self, name="knauer", ui=None, tcpPort=5555 ):
        self.name = name
        self.tcpPort = tcpPort
        serial_device.__init__( self, ui=ui )
        self.start_ip( tcpPort )
        

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
        end = r"$"
        echo = command# + "\r"
        ack = "OK"
        
        # Prepare a list of regex patterns to check commands for
        patterns = {}
        
        patterns["status?"] =       begin + r"STATUS\?" + end
        patterns["remote"] =        begin + r"REMOTE" + end
        patterns["powerup"] =       begin + r"POWERUP" + end
        patterns["shutdown"] =      begin + r"SHUTDOWN" + end
        patterns["ramp"] =          (begin + r"RAMP:(?P<speedupTime>[0-9]+)"
                                    + r",(?P<flow>[0-9]+)"
                                    + r",(?P<A>[0-9]+)"
                                    + r",(?P<B>[0-9]+)"
                                    + r",(?P<C>[0-9]+)"
                                    + r",(?P<D>[0-9]+)"
                                    + r",[0-3],[0-3],[0-3],[0-3],[0-3],[0-3],[0-3],[0-3],[0-3]" + end)
        patterns["stop"] =          begin + r"STOP:[0-2],[0-1]" + end #Greedy stop command
        
        # Try each pattern and drop out if we find a match
        matchedPattern = None
        for key, pattern in patterns.iteritems():
            matches = re.match(pattern, command)
            if (matches is not None):
                matchedPattern = key
                break
         
        if matchedPattern == "status?":
        
            # Set flag to denote addressing has been done
            self.addressed = True

            st_timestamp =  generate_random(99999)
            st_state =      self.status['state']
            st_error =      self.status['current_error']
            st_prg_runtime= generate_random(9999)
            st_flowrate =   self.status['flow']
            st_a =          self.status['LPG_0']
            st_b =          self.status['LPG_1']
            st_c =          self.status['LPG_2']
            st_d =          self.status['LPG_3']
            st_pressure =   self.status['pressure_kPa']
            result = "STATUS:{0},{1},{2},{3},{4},{5},{6},{7},{8},0,1,0,1,0,1,0,0,{9},0,0".format(st_timestamp,
                                                        st_state,
                                                        st_error,
                                                        st_prg_runtime,
                                                        st_flowrate,
                                                        st_a, st_b, st_c, st_d,
                                                        st_pressure)

        elif matchedPattern == "remote":
            
            # Pretend we've set to remote mode
            result = "OK";
            
        elif matchedPattern == "shutdown":
            
            self.status["state"] = 6
            result = "OK"
            
        elif matchedPattern == "powerup":
            
            self.status["state"] = 1
            result = "OK"
        
        elif matchedPattern == "stop":
            
            if self.status["state"] == 3:
                result = "OK"
                self.status["state"] = 1;
            else:
                # Handle unrecognised commands
                self.error = 21
                
        elif matchedPattern == "ramp":
            
            if (self.status["state"] in [1, 3]):
                
                # Get input parameters
                a = int(matches.group("A"))
                b = int(matches.group("B"))
                c = int(matches.group("C"))
                d = int(matches.group("D"))
                flow = int(matches.group("flow"))
                
                # Rudimentary check of parameters
                if ((a + b + c + d == 100) and (flow >= self.flow_min) and (flow <= self.flow_max)):
                
                    # Simulate this flow (instantaneously)
                    result = "OK"
                    self.status["state"] = 3;
                    
                    self.status["LPG_0"] = a
                    self.status["LPG_1"] = b
                    self.status["LPG_2"] = c
                    self.status["LPG_3"] = d
                    
                    self.status["flow"] = flow
                    
                else:
                    
                    # Throw invalid parameters error
                    self.error = 17
            
        else:
        
            # Default to invalid command
            self.error = 16


        if result is not None:
            
            # Print correspondence to terminal
            self.diagnostic( "Tx: %s" % repr( result ), 4 )
            print "Tx: ", result

        else: # Presuambly an error
        
            # No error set? Default to invalid command
            if self.error is None:
                self.error = 16
                
            # Handle unrecognised commands
            err = self.format_error(self.error)
            
            # Debug for console
            print err
            
            # Don't think the controller says anything:
            # Return an empty string
            result = err
            
            # Clear error
            self.error = None

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
