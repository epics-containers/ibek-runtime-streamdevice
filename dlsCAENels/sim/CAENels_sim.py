'''
    2015 - Nicoletta De Maio
'''


from pkg_resources import require
require('dls_serial_sim==1.17')
from dls_serial_sim import serial_device
require('dls_simulationlib==3.1')
from dls_simulationlib.beamline import Beamline

import math, random

random.seed( 0xcaffe )


def generate_status():
    '''generate a random status response (0 or 1)'''
    res = random.uniform( 0, 2 )
    res = math.floor( res )
    res = int( res )
    res = str( res )
    return res


class CAENelsDummyBeamline( Beamline ):
    '''This is just a dummy class to run the device in'''
    def createSimulation( self ):
        self.hvadaptos = HVAdaptos()


class HVAdaptos( serial_device ):
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
    Terminator = '\r\n'

    def __init__( self, name="CAENels HVAdaptos", ui=None, tcpPort=5555 ):
        self.name = name
        self.tcpPort = tcpPort
        serial_device.__init__( self, ui=ui )
        self.start_ip( tcpPort )


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

        tokens = command.split( ':' )

        if len( tokens ) > 3:
            self.diagnostic( "Tx: %s" % repr( self.errors['execution'] ), 4 )
            print "Responding with", self.errors['execution']
            return self.errors['execution']

        elif len( tokens ) < 2:
            self.diagnostic( "Tx: %s" % repr( self.errors['unknown'] ), 4 )
            print "Responding with", self.errors['unknown']
            return self.errors['unknown']

        elif tokens[0] == '':

            if tokens[1] == 'GROUPSLIST?':
                print "Responding with", self.get_responses['grouplist']
                return self.get_responses['grouplist']

            else:
                self.diagnostic( "Tx: %s" % repr( self.errors['unknown'] ), 4 )
                print "Responding with", self.errors['unknown']
                return self.errors['unknown']

        else:

            if tokens[-1].endswith( '?' ):

                if self.value_valid_int( tokens[-1][-2] ):
                    handler = self.channel_get

                else:
                    handler = self.group_get

            else:

                if self.value_valid_int( tokens[-2][-1] ) and len( tokens ) == 3:
                    handler = self.channel_set

                else:
                    handler = self.group_set

        if handler is not None:
            result = handler( tokens )

        if result is not None:
            self.diagnostic( "Tx: %s" % repr( result ), 4 )
            print "Responding with", result

        else:
            print "No result.", self.errors['weird']


        return result


    def group_get( self, tokens ):
        '''Process a GET command on a group of channels'''
        if self.group_valid( tokens[0] ):

            if tokens[-1] == 'STATUS?':
                return generate_status()

            elif tokens[-1] == 'OPMODE?':
                return self.get_responses['mode']

            elif tokens[-1] == 'ERR?':
                return self.get_responses['lasterr']

            elif tokens[-1] == 'TEMP?':
                return self.get_responses['temperatures']

            elif tokens[-1] == 'CHANNELS?':
                return self.get_responses['channels']

            else:
                return self.errors['unknown']

        else:
            return self.errors['wronggroup']

        return self.errors['weird']


    def group_set( self, tokens ):
        '''Process a SET command on a group of channels'''
        if self.group_valid( tokens[0] ):

            if len( tokens ) == 2:

                if tokens[-1] in ['RESETERR', 'ALLTRGT']:
                    return self.errors['success']

                else:
                    return self.errors['unknown']

            elif len( tokens ) == 3:

                if not self.value_valid_double( tokens[-1] ):

                    if tokens[-2] == 'ALL' and ( tokens[-1] in ['ON', 'OFF'] ):
                        return self.errors['success']

                    elif tokens[-2] == 'OPMODE' and ( tokens[-1] in ['HI', 'NORMAL', 'FAST'] ):
                        return self.errors['success']

                    else:
                        return self.errors['unknown']

                else:

                    if tokens[-2] in ['ALLVOLT', 'ALLSHIFT']:
                        return self.errors['success']

                    else:
                        return self.errors['unknown']

            else:
                return self.errors['weird']

        else:
            return self.errors['wronggroup']

        return self.errors['weird']


    def channel_get( self, tokens ):
        '''Process a GET command on an individual channel'''
        if self.group_valid(tokens[0]):

            if tokens[-1].startswith( 'STATUS' ):

                if self.channel_valid( tokens[-1][6:-1] ):
                    return self.get_responses['channelstatus']

                else:
                    return self.errors['wrongchannel']

            elif tokens[-1].startswith( 'VOUT' ):

                if self.channel_valid( tokens[-1][4:-1] ):
                    return self.get_responses['voltage']

                else:
                    return self.errors['wrongchannel']

            elif tokens[-1].startswith( 'VTRGT' ):

                if self.channel_valid( tokens[-1][5:-1] ):
                    return self.get_responses['voltage']

                else:
                    return self.errors['wrongchannel']

            else:
                return self.errors['unknown']

        else:
            return self.errors['wronggroup']

        return self.errors['weird']


    def channel_set( self, tokens ):
        '''Process a SET command on an individual channel'''
        if self.group_valid( tokens[0] ):

            if tokens[-2].startswith( 'VOUT' ):

                if self.channel_valid( tokens[-2][4:] ):
                    return self.errors['success']

                else:
                    return self.errors['wrongchannel']

            elif tokens[-2].startswith( 'VTRGT' ):

                if  self.channel_valid( tokens[-2][5:] ):
                    return self.errors['success']

                else:
                    return self.errors['wrongchannel']

            elif tokens[-2].startswith( 'SHIFT' ):

                if self.channel_valid( tokens[-2][5:] ):
                    return self.errors['success']

                else:
                    return self.errors['wrongchannel']

            else:
                return self.errors['unknown']


        else:
            return self.errors['wronggroup']

        return self.errors['weird']


    def group_valid( self, groupname ):
        '''Check the format of the group name - must be GROUP<number>'''
        if groupname is None:
            return False

        if groupname.startswith( 'GROUP' ) and self.value_valid_int( groupname[5:] ):
            return True
        else:
            return False

        return self.errors['weird']


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
    hvps = CAENelsDummyBeamline( 'HVAdaptos' )