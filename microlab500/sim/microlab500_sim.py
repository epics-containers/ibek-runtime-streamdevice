'''
    Simulator for Hamilton Microlab 500 series syringe pump controllers
    2015 - Andrew Wilson
'''


from pkg_resources import require
require('dls_serial_sim==1.17')
from dls_serial_sim import serial_device
require('dls_simulationlib==3.1')
from dls_simulationlib.beamline import Beamline

import math, random, re

random.seed( 0xcaffe )


def generate_status():
    '''generate a random status response (0 or 1)'''
    res = random.uniform( 0, 2 )
    res = math.floor( res )
    res = int( res )
    res = str( res )
    return res


class microlab500DummyBeamline( Beamline ):
    '''This is just a dummy class to run the device in'''
    def createSimulation( self ):
        self.hvadaptos = microlab500()


class microlab500( serial_device ):
    '''
        TODO: description of class here - simulates communication only, command handlers are stubs, no sanity checking wrt #channels and channel number, etc.
    '''
    errors = { 'success'      : 'Command execution OK',
               'unknown'      : '*** ERROR unknown command',
               'execution'    : '*** ERROR command execution',
               'wronggroup'   : '*** ERROR command aborted: wrong group number',
               'wrongchannel' : '*** ERROR command aborted: wrong channel number',
               'busy'         : '*** ERROR command aborted: channel busy',
               'limit'        : '*** ERROR command aborted: limit voltage violation',
               'unsafe'       : '*** ERROR command aborted: unsafe voltage setting',
               'alreadyon'    : '*** ERROR command aborted: group is already powered on',
               'weird'        : 'This is a Weird Error(TM). It shouldn\'t happen at all. Are you up to date on your sacrifices to Cthulhu?'
    }

    # Successful GET responses
    get_responses = { 'grouplist'     : '0;1;',
                      'mode'          : 'FAST',
                      'lasterr'       : 0,
                      'temperatures'  : '10;20',
                      'channels'      : 16,
                      'channelstatus' : 8,
                      'voltage'       : 1.0
    }

    # Serial protocol
    Terminator = '\r'
    # Temporary terminator for use with Telnet
    #Terminator = "\r\n"

    def __init__( self, name="microlab500", ui=None, tcpPort=5555 ):
        self.name = name
        self.tcpPort = tcpPort
        serial_device.__init__( self, ui=ui )
        self.start_ip( tcpPort )
        
        # Initialise device status
        self.addressed = False
        self.syringe = {}
        self.syringe["B"] = {"position": 123, 
                             "speed": 4,
                             "return": 0,
                             "positionV": 1}
        self.syringe["C"] = {"position": 456,
                             "speed": 4,
                             "return": 0,
                             "positionV": 1}


    def reply( self, command ):
        '''This function must be defined. It is called by the serial_sim system
        whenever an asyn command is send down the line. Must return a string
        with a response to the command or None.'''
        self.diagnostic( "Rx: %s" % repr( command ), 4 )
        print "Received request", command
        handler = None
        result = None

        if command is None:
            return None
        
        # Reusable bits of regex and string
        begin = r"^"
        findAddress = r"(?P<address>[:ab])"
        findSide = r"(?P<side>[BC]?)"
        findSteps = r"(?P<steps>[0-9]+)"
        findSpeed = r"(?P<speed>[0-9]+)"
        findValvePos = r"(?P<valvePos>[xIWO])"
        execute = r"R"
        end = r"$"
        echo = command + "\r"
        ack = "\06"
        
        # Prepare a list of regex patterns to check commands for
        patterns = {}
        
        patterns["autoAddress"] =   begin + r"1a" + end
        patterns["init"] =          begin + findAddress + r"X" + execute + end
        patterns["pickup"] =        begin + findAddress + findSide + r"P" + findSteps + execute + end
        patterns["dispense"] =      begin + findAddress + findSide + r"D" + findSteps + execute + end
        patterns["idle"] =          begin + findAddress + r"F" + end
        patterns["move"] =          begin + findAddress + findSide + r"M" + findSteps + execute + end
        patterns["speed"] =         begin + findAddress + findSide + r"YSS" + findSpeed + end
        patterns["return"] =        begin + findAddress + findSide + r"YSN" + findSteps + end
        patterns["positionS"] =     begin + findAddress + findSide + r"YQE" + end
        patterns["positionV"] =     begin + findAddress + findSide + r"LQP" + end
        patterns["setValve"] =      begin + findAddress + findSide + findValvePos + execute + end
        patterns["halt"] =          begin + findAddress + r"K" + end
        patterns["busybyte"] =      begin + findAddress + r"T1" + end
        
        # Try each pattern and drop out if we find a match
        matchedPattern = None
        for key, pattern in patterns.iteritems():
            matches = re.match(pattern, command)
            if (matches is not None):
                matchedPattern = key
                break
         
        if matchedPattern == "autoAddress":
        
            # Set flag to denote addressing has been done
            self.addressed = True
            # Deal with only one unit for now
            result = "1b"
            
        elif self.addressed == False:
        
            # Can't execute any commands yet
            result = ""
            print "Command rejected: device not auto-addressed yet"
               
        elif matchedPattern == "init":
        
            address = matches.group("address")
            result = echo + ack
        
        elif matchedPattern == "pickup":
            
            side = matches.group("side")
            steps = matches.group("steps")
            address = matches.group("address")  
            
            if (side is None or side == ""):
                side = "B" 
            
            print "Pickup requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            print "\tSize of move: " + steps
            
            # First implementation: move is instantaneous
            if (self.value_valid_int(steps)):
                print "...which is a valid integer"
                print "Old position: " + str(self.syringe[side]["position"])
                self.syringe[side]["position"] = self.syringe[side]["position"] + int(steps)
                print "New position: " + str(self.syringe[side]["position"])
                
                # Acknowledge command
                result = echo + ack
            else:
                print "...which is not a valid integer."
                result = ""
        
        elif matchedPattern == "dispense":

            side = matches.group("side")
            steps = matches.group("steps")
            address = matches.group("address")  
            
            if (side is None or side == ""):
                side = "B" 
            
            print "Pickup requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            print "\tSize of move: " + steps
            
            # First implementation: move is instantaneous
            if (self.value_valid_int(steps)):
                print "...which is a valid integer"
                print "Old position: " + str(self.syringe[side]["position"])
                self.syringe[side]["position"] = self.syringe[side]["position"] - int(steps)
                print "New position: " + str(self.syringe[side]["position"])
                
                # Acknowledge command
                result = echo + ack
            else:
                print "...which is not a valid integer."
                result = ""
            
        elif matchedPattern == "idle":
        
            # Always idle for now
            result = echo + ack + "*"
            
        elif matchedPattern == "move":
        
            side = matches.group("side")
            steps = matches.group("steps")
            address = matches.group("address")  
            
            if (side is None or side == ""):
                side = "B" 
            
            print "Move requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            print "\tTo: " + steps
            
            # First implementation: move is instantaneous
            if (self.value_valid_int(steps)):
                print "...which is a valid integer"
                print "Old position: " + str(self.syringe[side]["position"])
                self.syringe[side]["position"] = int(steps)
                print "New position: " + str(self.syringe[side]["position"])
                
                # Acknowledge command
                result = echo + ack
            else:
                print "...which is not a valid integer."
                result = ""
            
        elif matchedPattern == "speed":
        
            side = matches.group("side")
            address = matches.group("address")
            speed = matches.group("speed")
            
            print "Set speed requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            print "\tTo: " + speed
            
            # If speed is valid, update stored value
            if (self.value_valid_int(speed)):
                print "...which is a valid integer"
                print "Old speed: " + str(self.syringe[side]["speed"])
                self.syringe[side]["speed"] = int(speed)
                print "New speed: " + str(self.syringe[side]["speed"])
                
                # Acknowledge command
                result = echo + ack
            else:
                print "...which is not a valid integer."
                result = ""
        
        elif matchedPattern == "return":
        
            side = matches.group("side")
            address = matches.group("address")
            steps = matches.group("steps")
            
            print "Set return steps requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            print "\tTo: " + steps
            
            # If speed is valid, update stored value
            if (self.value_valid_int(steps)):
                print "...which is a valid integer"
                print "Old return: " + str(self.syringe[side]["return"])
                self.syringe[side]["return"] = int(steps)
                print "New return: " + str(self.syringe[side]["return"])
                
                # Acknowledge command
                result = echo + ack
            else:
                print "...which is not a valid integer."
                result = ""
                
        elif matchedPattern == "positionS":
        
            side = matches.group("side")
            address = matches.group("address")
            
            print "Syringe position readback requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            
            result = echo + ack + str(self.syringe[side]["position"])
            
        elif matchedPattern == "positionV":
        
            side = matches.group("side")
            address = matches.group("address")
            
            print "Valve position readback requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            
            
            result = echo + ack + str(self.syringe[side]["positionV"])

        elif matchedPattern == "setValve":
        
            side = matches.group("side")
            address = matches.group("address")
            valvePos = matches.group("valvePos")
            
            print "Set valve position requested"
            print "\tAddress: " + address
            print "\tSide: " + side
            print "\tNew position: " + valvePos
            
            numericPos = 0
            if valvePos == "I":
                numericPos = 1
            elif valvePos == "W":
                numericPos = 3
            elif valvePos == "O":
                numericPos = 4
            
            print "Old position: " + str(self.syringe[side]["positionV"])
            self.syringe[side]["positionV"] = numericPos
            print "New position: " + str(self.syringe[side]["positionV"])
            
            result = echo + ack
        
        elif matchedPattern == "halt":
        
            # TODO: Implement motion stop here
            #       For now, there is no motion so nothing to stop
            
            address = matches.group("address")
            print "Abort motion requested." 
            print "\tAddress:" + address
            result = echo + ack
        
        elif matchedPattern == "busybyte":
            
            address = matches.group("address")
            print "Busy byte requested."
            print "\tAddress:" + address

            result = echo + ack + "{"

        else:
        
            # Handle unrecognised commands
            print "ERROR, unrecognised command."
            
            # Don't think the controller says anything:
            # Return an empty string
            result = ""


        if result is not None:
            self.diagnostic( "Tx: %s" % repr( result ), 4 )
            print "Responding with", result

        else:
            print "No result.", self.errors['weird']

        return result

    def channel_valid( self, channelnumber ):
        '''Check the channel number - must be -1 < <number> < 16'''
        if not self.value_valid_int( channelnumber ):
            return False

        if int( channelnumber ) > -1 and int( channelnumber ) < 16:
            return True
        else:
            return False

        return self.errors['weird']


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
    hvps = microlab500DummyBeamline( 'HVAdaptos' )
