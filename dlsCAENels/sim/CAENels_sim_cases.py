'''
    2015 - Nicoletta De Maio
'''

from unittest import TestCase


class CAENelsSimTestCase(TestCase):
    '''This is the base class for the simulation tests'''

    #TODO: errors is a static variable in class HVAdaptos and should be imported from there
    errors = { 'success'      : 'Command execution OK',
               'unknown'      : '*** ERROR unknown command',
               'execution'    : '*** ERROR command execution',
               'wronggroup'   : '*** ERROR command aborted: wrong group number',
               'wrongchannel' : '*** ERROR command aborted: wrong channel number',
             }

    def __init__( self, connection, terminator='\r\n' ):
        super( CAENelsSimTestCase, self ).__init__()
        self.requests = []
        self.response = None
        self.comparisons = []
        self.assertionfailed = []
        self.connection = connection
        self.terminator = terminator

    def runTest( self ):
         for request, comparison, message in zip(self.requests, self.comparisons, self.assertionfailed):
             self.connection.send( request + self.terminator )
             self.response = self.connection.recv( 256 )
             self.response = self.response[:-len(self.terminator)]
             self.assertEqual( self.response, comparison, message )


class BasicFailures( CAENelsSimTestCase ):
    '''Send some basic malformed requests'''

    def setUp(self):
        self.requests = [ 'BLA:BLI:BLA:BLUBB', 'DUMDIDUM' ]
        self.comparisons = [ self.errors['execution'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test BasicFailures failed: the first request should have provoked an error',
                                 'Test BasicFailures failed: the second request should have provoked an error' ]


class ListGroups( CAENelsSimTestCase ):
    '''Get the list of groups configured on the device'''

    def setUp( self ):
        self.requests = [ ':GROUPSLIST?', ':FAILURETEST?' ]
        self.comparisons = [ '0;1;', self.errors['unknown'] ]
        self.assertionfailed = [ 'Test ListGroups failed: the simulation did not return the expected group list',
                                 'Test ListGroups failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupGetStatus( CAENelsSimTestCase ):
    '''Get the group status'''

    def setUp( self ):
        self.requests = [ 'GROUP0:STATUS?', 'GROUP1:STATUS?', 'GROUPX:FTEST?', 'GROUP0:FTEST?' ]
        self.comparisons = [ [ '0', '1' ], [ '0', '1' ], self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupGetStatus failed: received an unexpected status value for the first group',
                                 'Test GroupGetStatus failed: received an unexpected status value for the second group',
                                 'Test GroupGetStatus failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupGetStatus failed: the request should have provoked error ' + self.errors['unknown'] ]

    def runTest( self ):
        for request, comparison, message in zip(self.requests, self.comparisons, self.assertionfailed):
             self.connection.send( request + self.terminator )
             self.response = self.connection.recv( 256 )
             self.response = self.response[:-len(self.terminator)]
             if request == self.requests[0] or request == self.requests[1]:
                self.assertIn( self.response, comparison, message )
             else:
                 self.assertEqual( self.response, comparison, message )


class GroupGetMode(CAENelsSimTestCase):
    '''Get the operation mode of a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:OPMODE?', 'GROUP1:OPMODE?', 'GROUPX:FTEST?', 'GROUP0:FTEST?' ]
        self.comparisons = [ 'FAST', 'FAST', self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupGetMode failed: received an unexpected mode string for the first group',
                                 'Test GroupGetMode failed: received an unexpected mode string for the second group',
                                 'Test GroupGetMode failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupGetMode failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupGetLasterror( CAENelsSimTestCase ):
    '''Get the last error for a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:ERR?', 'GROUP1:ERR?', 'GROUPX:FTEST?', 'GROUP0:FTEST?' ]
        self.comparisons = [ '0', '0', self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupGetLasterror failed: received an unexpected error status for the first group',
                                 'Test GroupGetLasterror failed: received an unexpected error status for the second group',
                                 'Test GroupGetLasterror failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupGetLasterror failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupGetTemperatures( CAENelsSimTestCase ):
    '''Get the list of board temperatures for a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:TEMP?', 'GROUP1:TEMP?', 'GROUPX:FTEST?', 'GROUP0:FTEST?' ]
        self.comparisons = [ '10;20', '10;20', self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupGetTemperatures failed: received an unexpected temperatures for the first group',
                                 'Test GroupGetTemperatures failed: received an unexpected temperatures for the second group',
                                 'Test GroupGetTemperatures failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupGetTemperatures failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupGetChannels( CAENelsSimTestCase ):
    '''Get the number of channels in a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:CHANNELS?', 'GROUP1:CHANNELS?', 'GROUPX:FTEST?', 'GROUP0:FTEST?' ]
        self.comparisons = [ '16', '16', self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupGetChannels failed: received the wrong number of channels for the first group',
                                 'Test GroupGetChannels failed: received the wrong number of channels for the second group',
                                 'Test GroupGetChannels failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupGetChannels failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupSetMode( CAENelsSimTestCase ):
    '''Set the operation mode of a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:OPMODE:FAST', 'GROUP0:OPMODE:NORMAL', 'GROUP0:OPMODE:HI',
                          'GROUP1:OPMODE:FAST', 'GROUP1:OPMODE:NORMAL', 'GROUP1:OPMODE:HI',
                          'GROUP0:OPMODE:FAIL', 'GROUP1:FTEST:FAIL' ]
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['success'],
                             self.errors['success'], self.errors['success'], self.errors['success'],
                             self.errors['unknown'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupSetMode: failed to set operation mode to FAST for the first group',
                                 'Test GroupSetMode: failed to set operation mode to NORMAL for the first group',
                                 'Test GroupSetMode: failed to set operation mode to HI for the first group',
                                 'Test GroupSetMode: failed to set operation mode to FAST for the second group',
                                 'Test GroupSetMode: failed to set operation mode to NORMAL for the second group',
                                 'Test GroupSetMode: failed to set operation mode to HI for the second group',
                                 'Test GroupSetMode failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test GroupSetMode failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupResetError( CAENelsSimTestCase ):
    '''Reset the error status of a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:RESETERR', 'GROUP1:RESETERR', 'GROUPX:FTEST', 'GROUP1:FTEST' ]
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupResetError: failed to reset the error status on the first group',
                                 'Test GroupResetError: failed to reset the error status on the second group',
                                 'Test GroupResetError failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupResetError failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupSetAllOnOff( CAENelsSimTestCase ):
    '''Turn all channels in a group on or off'''

    def setUp( self ):
        self.requests = [ 'GROUP0:ALL:ON', 'GROUP0:ALL:OFF', 'GROUP1:ALL:ON', 'GROUP1:ALL:OFF',
                          'GROUP0:ALL:FAIL', 'GROUP1:FTEST:FAIL']
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['success'],
                             self.errors['success'], self.errors['unknown'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupSetAllOnOff: failed to turn the first group on',
                                 'Test GroupSetAllOnOff: failed to turn the first group off',
                                 'Test GroupSetAllOnOff: failed to turn the second group on',
                                 'Test GroupSetAllOnOff: failed to turn the second group off',
                                 'Test GroupSetAllOnOff failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test GroupSetAllOnOff failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupSetVout( CAENelsSimTestCase ):
    '''Set the voltages of a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:ALLVOLT:0', 'GROUP1:ALLVOLT:0', 'GROUP1:FTEST:0' ]
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupSetVout: failed to set the output voltage on the first group',
                                 'Test GroupSetVout: failed to set the output voltage on the second group',
                                 'Test GroupSetVout failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupSetVtrgt( CAENelsSimTestCase ):
    '''Set the target voltages on a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:ALLTRGT', 'GROUP1:ALLTRGT', 'GROUPX:FTEST', 'GROUP1:FTEST' ]
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['wronggroup'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupSetVtrgt: failed to set the target voltage on the first group',
                                 'Test GroupSetVtrgt: failed to set the target voltage on the second group',
                                 'Test GroupSetVtrgt failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test GroupSetVtrgt failed: the request should have provoked error ' + self.errors['unknown'] ]


class GroupSetShift( CAENelsSimTestCase ):
    '''Set the shift voltages of a group'''

    def setUp( self ):
        self.requests = [ 'GROUP0:ALLSHIFT:0', 'GROUP1:ALLSHIFT:0', 'GROUP1:FTEST:0' ]
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['unknown'] ]
        self.assertionfailed = [ 'Test GroupSetShift: failed to set the voltage shift for the first group',
                                 'Test GroupSetShift: failed to set the voltage shift for the second group',
                                 'Test GroupSetShift failed: the request should have provoked error ' + self.errors['unknown'] ]


class ChannelGetStatus( CAENelsSimTestCase ):
    '''Get the channel status'''

    def setUp( self ):
        self.requests = [ 'GROUP0:STATUS0?', 'GROUP0:STATUS1?', 'GROUP1:STATUS0?', 'GROUP1:STATUS1?',
                          'GROUPX:FTEST0?', 'GROUP0:FTEST0?', 'GROUP1:STATUSX?', 'GROUP0:STATUS16?' ]
        self.comparisons = [ '8', '8', '8', '8', self.errors['wronggroup'], self.errors['unknown'],
                             self.errors['unknown'], self.errors['wrongchannel'] ]
        self.assertionfailed = [ 'Test ChannelGetStatus failed: received an unexpected status value for the first channel',
                                 'Test ChannelGetStatus failed: received an unexpected status value for the second channel',
                                 'Test ChannelGetStatus failed: received an unexpected status value for the third channel',
                                 'Test ChannelGetStatus failed: received an unexpected status value for the fourth channel',
                                 'Test ChannelGetStatus failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test ChannelGetStatus failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelGetStatus failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelGetStatus failed: the request should have provoked error ' + self.errors['wrongchannel'] ]


class ChannelGetVout( CAENelsSimTestCase ):
    '''Get the channel voltage'''

    def setUp( self ):
        self.requests = [ 'GROUP0:VOUT0?', 'GROUP0:VOUT1?', 'GROUP1:VOUT0?', 'GROUP1:VOUT1?',
                          'GROUPX:FTEST0?', 'GROUP0:FTEST0?', 'GROUP1:VOUTX?', 'GROUP0:VOUT16?']
        self.comparisons = [ '1.0', '1.0', '1.0', '1.0', self.errors['wronggroup'], self.errors['unknown'],
                             self.errors['unknown'], self.errors['wrongchannel'] ]
        self.assertionfailed = [ 'Test ChannelGetVout failed: received an unexpected voltage for the first channel',
                                 'Test ChannelGetVout failed: received an unexpected voltage for the second channel',
                                 'Test ChannelGetVout failed: received an unexpected voltage for the third channel',
                                 'Test ChannelGetVout failed: received an unexpected voltage for the fourth channel',
                                 'Test ChannelGetVout failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test ChannelGetVout failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelGetVout failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelGetVout failed: the request should have provoked error' + self.errors['wrongchannel'] ]


class ChannelGetTrgt( CAENelsSimTestCase ):
    '''Get the target voltage of a channel'''

    def setUp( self ):
        self.requests = [ 'GROUP0:VTRGT0?', 'GROUP0:VTRGT1?', 'GROUP1:VTRGT0?', 'GROUP1:VTRGT1?',
                          'GROUPX:FTEST0?', 'GROUP0:FTEST0?', 'GROUP1:VTRGTX?', 'GROUP0:VTRGT16?' ]
        self.comparisons = [ '1.0', '1.0', '1.0', '1.0', self.errors['wronggroup'], self.errors['unknown'],
                             self.errors['unknown'], self.errors['wrongchannel'] ]
        self.assertionfailed = [ 'Test ChannelGetTrgt failed: received an unexpected target voltage for the first channel',
                                 'Test ChannelGetTrgt failed: received an unexpected target voltage for the second channel',
                                 'Test ChannelGetTrgt failed: received an unexpected target voltage for the third channel',
                                 'Test ChannelGetTrgt failed: received an unexpected target voltage for the fourth channel',
                                 'Test ChannelGetTrgt failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test ChannelGetTrgt failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelGetTrgt failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelGetTrgt failed: the request should have provoked error ' + self.errors['wrongchannel'] ]


class ChannelSetVout( CAENelsSimTestCase ):
    '''Set the channel voltage'''

    def setUp( self ):
        self.requests = [ 'GROUP0:VOUT0:0', 'GROUP0:VOUT1:0', 'GROUP1:VOUT0:0', 'GROUP1:VOUT1:0',
                          'GROUPX:FTEST0:0', 'GROUP1:FTEST0:0', 'GROUP0:VOUTX:0', 'GROUP0:VOUT16:0' ]
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['success'], self.errors['success'],
                             self.errors['wronggroup'], self.errors['unknown'], self.errors['unknown'], self.errors['wrongchannel'] ]
        self.assertionfailed = [ 'Test ChannelSetVout: failed to set the output voltage for the first channel',
                                 'Test ChannelSetVout: failed to set the output voltage for the second channel',
                                 'Test ChannelSetVout: failed to set the output voltage for the third channel',
                                 'Test ChannelSetVout: failed to set the output voltage for the fourth channel',
                                 'Test ChannelSetVout failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test ChannelSetVout failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelSetVout failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelSetVout failed: the request should have provoked error ' + self.errors['wrongchannel'] ]


class ChannelSetTrgt( CAENelsSimTestCase ):
    '''Set the target voltage of a channel'''

    def setUp( self ):
        self.requests = [ 'GROUP0:VTRGT0:0', 'GROUP0:VTRGT1:0', 'GROUP1:VTRGT0:0', 'GROUP1:VTRGT1:0',
                          'GROUPX:FTEST0:0', 'GROUP1:FTEST0:0', 'GROUP1:VTRGTX:0', 'GROUP0:VTRGT16:0']
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['success'], self.errors['success'],
                             self.errors['wronggroup'], self.errors['unknown'], self.errors['unknown'], self.errors['wrongchannel'] ]
        self.assertionfailed = [ 'Test ChannelSetTrgt: failed to set the target voltage for the first channel',
                                 'Test ChannelSetTrgt: failed to set the target voltage for the second channel',
                                 'Test ChannelSetTrgt: failed to set the target voltage for the third channel',
                                 'Test ChannelSetTrgt: failed to set the target voltage for the fourth channel',
                                 'Test ChannelSetTrgt failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test ChannelSetTrgt failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelSetTrgt failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelSetTrgt failed: the request should have provoked error ' + self.errors['wrongchannel'] ]


class ChannelSetShift( CAENelsSimTestCase ):
    '''Set the shift voltage of a channel'''

    def setUp( self ):
        self.requests = [ 'GROUP0:SHIFT0:0', 'GROUP0:SHIFT1:0', 'GROUP1:SHIFT0:0', 'GROUP1:SHIFT1:0',
                          'GROUPX:FTEST0:0', 'GROUP1:FTEST0:0', 'GROUP0:SHIFTX:0', 'GROUP1:SHIFT16:0']
        self.comparisons = [ self.errors['success'], self.errors['success'], self.errors['success'], self.errors['success'],
                             self.errors['wronggroup'], self.errors['unknown'], self.errors['unknown'], self.errors['wrongchannel'] ]
        self.assertionfailed = [ 'Test ChannelSetShift: failed to set the voltage shift for the first channel',
                                 'Test ChannelSetShift: failed to set the voltage shift for the second channel',
                                 'Test ChannelSetShift: failed to set the voltage shift for the third channel',
                                 'Test ChannelSetShift: failed to set the voltage shift for the fourth channel',
                                 'Test ChannelSetShift failed: the request should have provoked error ' + self.errors['wronggroup'],
                                 'Test ChannelSetShift failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelSetShift failed: the request should have provoked error ' + self.errors['unknown'],
                                 'Test ChannelSetShift failed: the request should have provoked error ' + self.errors['wrongchannel'] ]