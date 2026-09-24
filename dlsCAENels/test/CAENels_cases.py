'''
    2015 - Nicoletta De Maio
'''

from pkg_resources import require
require('dls_autotestframework==2.16')
from dls_autotestframework import TestCase
from numbers import Number
import re, time


class CAENelsTestCase( TestCase ):
    '''Base class for all CAENels database test cases'''

    def __init__( self, suite ):
        super( CAENelsTestCase, self ).__init__( suite )
        self.pvbase = 'BL16B-MO-PSU-01'
        self.groups = [ ':GROUP0', ':GROUP1']
        self.channels = [ ':CH0', ':CH1', ':CH2',  ':CH3',  ':CH4',  ':CH5',  ':CH6',  ':CH7',
                          ':CH8', ':CH9', ':CH10', ':CH11', ':CH12', ':CH13', ':CH14', ':CH15']
        self.modes = [ 'FAST', 'NORMAL', 'HI' ]


class GenericResponse( CAENelsTestCase ):

    def __init__( self, suite ):
        super( GenericResponse, self ).__init__( suite )

    def runTest( self ):
        result = None
        pv = self.pvbase + ':RESPONSE'
        result = self.getPv( pv )
        self.assertIsNotNone( result, 'Test GenericResponse failed')

class NumberOfGroups( CAENelsTestCase ):
    '''Get the number of groups'''

    def __init__( self, suite ):
        super( NumberOfGroups, self ).__init__( suite )

    def runTest( self ):
        result = None
        pv = self.pvbase + ':GROUPS'
        result = self.getPv( pv )
        self.assertEqual( result, 2, 'Test NumberOfGroups failed: pvget returned ' + repr( result ) )


class GroupCalc( CAENelsTestCase ):
    '''Test the CALC conversion between ListGroups and NumberOfGroups'''

    def __init__( self, suite ):
        super( GroupCalc, self ).__init__( suite )

    def runTest( self ):
        result = None
        pv = self.pvbase + ':GRSTRING.AA'
        result = self.getPv( pv )
        self.assertEqual( result, '0;1;', 'Test GroupCalc failed: pvget returned ' + repr( result ) )
        pv = self.pvbase + ':GRSTRING'
        result = self.getPv( pv )
        self.assertEqual( result, 2, 'Test GroupCalc failed: pvget returned ' + repr( result ) )


class ListGroups( CAENelsTestCase ):
    '''Get the list of groups configured on the device'''

    def __init__( self, suite ):
        super( ListGroups, self ).__init__( suite )

    def runTest( self ):
        result = None
        pv = self.pvbase + ':GETGRSTRING'
        result = self.getPv( pv )
        self.assertEqual( result, '0;1;', 'Test ListGroups failed: pvget returned ' + repr( result ) )

class GroupGetStatus( CAENelsTestCase ):
    '''Get the group status'''

    def __init__( self, suite ):
        super( GroupGetStatus, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':STATUS'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1 ], 'Test GroupGetStatus failed: pvget returned ' + repr( result ) )

class GroupGetMode( CAENelsTestCase ):
    '''Get the operation mode of a group'''

    def __init__( self, suite ):
        super( GroupGetMode, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':MODE_RBV'
            result = self.getPv( pv )
            self.assertIn( result, self.modes, 'Test GroupGetMode failed: pvget returned ' + repr( result ) )


class GroupGetLasterror( CAENelsTestCase ):
    '''Get the last error for a group'''

    def __init__( self, suite ):
        super( GroupGetLasterror, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':LASTERROR'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1 ], 'Test GroupGetLastError failed: pvget returned ' + repr( result ) )


class GroupGetTemperatures( CAENelsTestCase ):
    '''Get the list of board temperatures for a group'''

    def __init__( self, suite ):
        super( GroupGetTemperatures, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':TEMPS'
            result = self.getPv( pv )
            regex = re.compile( "^$|^\d+(;\d+)*$" )
            self.assertIsNotNone( regex.match( result ),
                                  'Test GroupGetTemperatures failed: pvget returned ' + repr( result ) )


class GroupGetChannels( CAENelsTestCase ):
    '''Get the number of channels in a group'''

    def __init__( self, suite ):
        super( GroupGetChannels, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':CHANNELS'
            result = self.getPv( pv )
            self.assertEqual( result, 16, 'Test  failed: pvget returned ' + repr( result ) )


class GroupSetMode( CAENelsTestCase ):
    '''Set the operation mode of a group'''

    def __init__( self, suite ):
        super( GroupSetMode, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':MODE'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1, 2 ], 'Test GroupSetMode failed: pvget returned ' + repr( result ) )
            for mode in self.modes:
                pv = self.pvbase + group + ':MODE'
                self.putPv( pv, mode, timeout=10 )
                pv = self.pvbase + ':RESPONSE'
                result = self.getPv( pv )
                self.assertEqual( result, 'Command execution OK',
                                  'Test GroupSetMode failed: response field contains ' + repr( result ) )


class GroupResetError( CAENelsTestCase ):
    '''Reset the error status of a group'''

    def __init__( self, suite ):
        super( GroupResetError, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':RESETERROR'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1 ], 'Test GroupResetError failed: pvget returned ' + repr( result ) )
            self.putPv( pv, 1, timeout=10 )
            pv = self.pvbase + ':RESPONSE'
            result = self.getPv( pv )
            self.assertEqual( result, 'Command execution OK',
                              'Test GroupResetError failed: response field contains ' + repr( result ) )


class GroupSetAllOn( CAENelsTestCase ):
    '''Turn all channels in a group on'''

    def __init__( self, suite ):
        super( GroupSetAllOn, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':ALLON'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1 ], 'Test GroupSetAllOn failed: pvget returned ' + repr( result ) )
            self.putPv( pv, 1, timeout=10 )
            pv = self.pvbase + ':RESPONSE'
            result = self.getPv( pv )
            self.assertEqual( result, 'Command execution OK',
                              'Test GroupSetAllOn failed: response field contains ' + repr( result ) )


class GroupSetAllOff( CAENelsTestCase ):
    '''Turn all channels in a group off'''

    def __init__( self, suite ):
        super( GroupSetAllOff, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':ALLOFF'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1 ], 'Test GroupSetAllOff failed: pvget returned ' + repr( result ) )
            self.putPv( pv, 1, timeout=10 )
            pv = self.pvbase + ':RESPONSE'
            result = self.getPv( pv )
            self.assertEqual( result, 'Command execution OK',
                              'Test GroupSetAllOff failed: response field contains ' + repr( result ) )


class GroupSetVout( CAENelsTestCase ):
    '''Set the voltages of a group'''

    def __init__( self, suite ):
        super( GroupSetVout, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':VOUT'
            result = self.getPv( pv )
            self.assertTrue( isinstance( result, Number ), 'Test GroupSetVout failed: pvget returned ' + repr( result ) )
            self.putPv( pv, 1.0, timeout=10 )
            pv = self.pvbase + ':RESPONSE'
            result = self.getPv( pv )
            self.assertEqual( result, 'Command execution OK',
                              'Test GroupSetVout failed: response field contains ' + repr( result ) )


class GroupSetVtrgt( CAENelsTestCase ):
    '''Set the target voltages on a group'''

    def __init__( self, suite ):
        super( GroupSetVtrgt, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':TARGET'
            result = self.getPv( pv )
            self.assertIn( result, [ 0, 1 ], 'Test GroupSetVtrgt failed: pvget returned ' + repr( result ) )
            self.putPv( pv, 1, timeout=10 )
            pv = self.pvbase + ':RESPONSE'
            result = self.getPv( pv )
            self.assertEqual( result, 'Command execution OK',
                              'Test GroupSetVtrgt failed: response field contains ' + repr( result ) )


class GroupSetShift( CAENelsTestCase ):
    '''Set the shift voltages of a group'''

    def __init__( self, suite ):
        super( GroupSetShift, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            result = None
            pv = self.pvbase + group + ':SHIFT'
            result = self.getPv( pv )
            self.assertTrue( isinstance( result, Number ), 'Test GroupSetShift failed: pvget returned ' + repr( result ) )
            self.putPv( pv, 2.0, timeout=10 )
            pv = self.pvbase + ':RESPONSE'
            result = self.getPv( pv )
            self.assertEqual( result, 'Command execution OK',
                              'Test GroupSetShift failed: response field contains ' + repr( result ) )


class ChannelGetStatus( CAENelsTestCase ):
    '''Get the channel status'''

    def __init__( self, suite ):
        super( ChannelGetStatus, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':STATUS'
                result = self.getPv( pv )
                self.assertIn( result, [ 0, 1, 2, 4 ],
                               'Test ChannelGetStatus failed: pvget returned ' + repr( result ) )


class ChannelGetRealStatus( CAENelsTestCase ):
    '''Get the real channel status'''

    def __init__( self, suite ):
        super( ChannelGetRealStatus, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':GETSTATUS'
                result = self.getPv( pv )

                self.assertIn( result, [ 0, 8, 16, 32 ],
                               'Test ChannelGetRealStatus failed: pvget returned ' + repr( result ) )


class ChannelGetVout( CAENelsTestCase ):
    '''Get the channel voltage'''

    def __init__( self, suite ):
        super( ChannelGetVout, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':VOUT_RBV'
                result = self.getPv( pv )
                self.assertTrue( isinstance( result, Number ),
                                 'Test ChannelGetVout failed: pvget returned ' + repr( result ) )


class ChannelGetTrgt( CAENelsTestCase ):
    '''Get the target voltage of a channel'''

    def __init__( self, suite ):
        super( ChannelGetTrgt, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':VTRGT_RBV'
                result = self.getPv( pv )
                self.assertTrue( isinstance( result, Number ),
                                 'Test ChannelGetTrgt failed: pvget returned ' + repr( result ) )


class ChannelSetVout( CAENelsTestCase ):
    '''Set the channel voltage'''

    def __init__( self, suite ):
        super( ChannelSetVout, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':VOUT'
                result = self.getPv( pv )
                self.assertTrue( isinstance( result, Number ),
                                 'Test ChannelSetVout failed: pvget returned ' + repr( result ) )
                self.putPv( pv, 3.0, timeout=10 )
                pv = self.pvbase + ':RESPONSE'
                result = self.getPv( pv )
                self.assertEqual( result, 'Command execution OK',
                                  'Test ChannelSetVout failed: response field contains ' + repr( result ) )


class ChannelSetTrgt( CAENelsTestCase ):
    '''Set the target voltage of a channel'''

    def __init__( self, suite ):
        super( ChannelSetTrgt, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':VTRGT'
                result = self.getPv( pv )
                self.assertTrue( isinstance( result, Number ),
                                 'Test ChannelSetTrgt failed: pvget returned ' + repr( result ) )
                self.putPv( pv, 4.0, timeout=10 )
                pv = self.pvbase + ':RESPONSE'
                result = self.getPv( pv )
                self.assertEqual( result, 'Command execution OK',
                                  'Test ChannelSetTrgt failed: response field contains ' + repr( result ) )


class ChannelSetShift( CAENelsTestCase ):
    '''Set the shift voltage of a channel'''

    def __init__( self, suite ):
        super( ChannelSetShift, self ).__init__( suite )

    def runTest( self ):
        for group in self.groups:
            for channel in self.channels:
                result = None
                pv = self.pvbase + group + channel + ':SHIFT'
                result = self.getPv( pv )
                self.assertTrue( isinstance( result, Number ),
                                 'Test ChannelSetShift failed: pvget returned ' + repr( result ) )
                self.putPv( pv, 5.0, timeout=10 )
                pv = self.pvbase + ':RESPONSE'
                result = self.getPv( pv )
                self.assertEqual( result, 'Command execution OK',
                                  'Test ChannelSetShift failed: response field contains ' + repr( result ) )