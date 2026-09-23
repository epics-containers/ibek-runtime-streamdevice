#!/usr/bin/env dls-python

#from pkg_resources import require
#require('dls_asynaid==1.6')
from dls_asynaid.dls_asynaid import *

if __name__ == "__main__":
    
    # The CENTER TWO/THREE controller
    centerController = Asyn("centerN")
    # PVs
    centerController.add(Pv("connection", enum=['Disconnected', 'Connected'],
        accessMode=Asyn.readOnly, archiverTag=True, group='status'))
    centerController.add(Pv('error', accessMode=Asyn.readOnly, group='status'))
    centerController.add(Pv('firmwareVer', dataType=Asyn.stringType, accessMode=Asyn.readOnly, group='status'))
    centerController.add(Pv('units', enum=['mBar', 'Torr', 'Pascal', 'Micron'],
        autosaveTag=True, archiverTag=True, group='main'))
    centerController.add(Pv('recorderChannel', enum=['Channel1', 'Channel2', 'Channel3'],
        autosaveTag=True, archiverTag=True, group='iface'))
    centerController.add(Pv('recorderCurveMode', enum=['Logarithmic', 'Linear'],
        autosaveTag=True, archiverTag=True, group='iface'))
    centerController.add(Pv('recorderCurveLog', enum=['Log', 'Log A', 'Log -6',
        'Log -3', 'Log +0', 'Log +3', 'Log C1', 'Log C2', 'Log C3'],
        autosaveTag=True, archiverTag=True, group='iface'))
    centerController.add(Pv('recorderCurveLin', enum=['Lin -10', 'Lin -9', 'Lin -8',
        'Lin -7', 'Lin -6', 'Lin -5', 'Lin -4', 'Lin -3', 'Lin -2', 'Lin -1', 'Lin +0',
        'Lin +1', 'Lin +2', 'Lin +3'],
        autosaveTag=True, archiverTag=True, group='iface'))
    centerController.add(Pv('errorRelay', enum=['All errors', 'Device errors',
        'Sensor 1 & device', 'Sensor 2 & device', 'Sensor 3 & device'],
        autosaveTag=True, archiverTag=True, group='iface'))
    centerController.add(Pv('parameterLock', enum=['Off', 'On'],
        autosaveTag=True, archiverTag=True, group='status'))
    centerController.add(Pv('factoryDefault', accessMode=Asyn.command, group='status'))
    centerController.add(Pv('save', accessMode=Asyn.command, group='status'))
    for chan in [1,2,3]:
        centerController.add(Pv("status%s" % chan,
            enum=['Ok', 'Underrange', 'Overrange',
            'Sensor Error', 'Sensor Off', 'No Sensor', 'Ident Error', 'ITR Error'],
            accessMode=Asyn.readOnly, archiverTag=True, group='main'))
        centerController.add(Pv('pressure%s' % chan,
            dataType=Asyn.floatType, accessMode=Asyn.readOnly, archiverTag=True, group='main'))
        centerController.add(Pv('sensorType%s' % chan,
            dataType=Asyn.stringType, accessMode=Asyn.readOnly, group='status'))
        centerController.add(Pv('corrFactor%s' % chan,
            dataType=Asyn.floatType, prec=2, autosaveTag=True, archiverTag=True, defaultValue=1.0, group='config%d'%chan))
        centerController.add(Pv('degas%s' % chan,
            enum=['off', 'on'], archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('filter%s' % chan, enum=['Fast', 'Medium', 'Slow'],
            autosaveTag=True, archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('gas%s' % chan,
            enum=['Nitrogen/Air', 'Argon', 'Hydrogen', 'Other'],
            autosaveTag=True, archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('highVacuum%s' % chan,
            enum=['Off', 'On'], autosaveTag=True, archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('offsetCorrMode%s' % chan,
            enum=['Off', 'On', 'Calculate'], autosaveTag=True, archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('offsetCorrValue%s' % chan,
            dataType=Asyn.floatType, prec=4,
            autosaveTag=True, archiverTag=True, defaultValue=0.0, group='config%d'%chan))
        centerController.add(Pv('sensorActivationMode%s' % chan,
            enum=['Manual', 'Hot start', 'By chan 1', 'By chan 2', 'By chan 3'],
            autosaveTag=True, archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('sensorDeactivationMode%s' % chan,
            enum=['Manual', 'Hot start', 'By chan 1', 'By chan 2', 'By chan 3'],
            autosaveTag=True, archiverTag=True, group='config%d'%chan))
        centerController.add(Pv('sensorActivationValue%s' % chan,
            dataType=Asyn.floatType, prec=4,
            autosaveTag=True, archiverTag=True, defaultValue=0.0, group='config%d'%chan))
        centerController.add(Pv('sensorDeactivationValue%s' % chan,
            dataType=Asyn.floatType, prec=4,
            autosaveTag=True, archiverTag=True, defaultValue=0.0, group='config%d'%chan))
    for switch in [1,2,3,4,5,6]:
        centerController.add(Pv('switchMode%s' % switch,
            enum=['Channel 1', 'Channel 2', 'Channel 3'],
            autosaveTag=True, archiverTag=True, group='iface'))
        centerController.add(Pv('switchLower%s' % switch,
            dataType=Asyn.floatType, prec=4,
            autosaveTag=True, archiverTag=True, defaultValue=0.0, group='iface'))
        centerController.add(Pv('switchUpper%s' % switch,
            dataType=Asyn.floatType, prec=4,
            autosaveTag=True, archiverTag=True, defaultValue=0.0, group='iface'))
        centerController.add(Pv('switchStatus%s' % switch,
            enum=['Off', 'On'], archiverTag=True, accessMode=Asyn.readOnly, group='iface'))
    centerController.add(Pv('torrLock', enum=['Off', 'On'],
        autosaveTag=True, archiverTag=True, group='status'))
    # Messages
    centerController.add(Msg('MsgAck', [ConstStr('pre', '\x06\r\n')]))
    centerController.add(Msg('MsgNack', [ConstStr('pre', '\x15\r\n')]))
    centerController.add(Msg('MsgEnq', [ConstStr('pre', '\x05')]))
    centerController.add(Msg('MsgBinaryReply', [TextInt('val', base=2), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntReply', [TextInt('val'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntReply', [TextInt('val1'), ConstStr('sep', ','),
        TextInt('val2'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntIntReply', [TextInt('val1'), ConstStr('sep1', ','),
        TextInt('val2'), ConstStr('sep2', ','), TextInt('val3'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntIntIntIntIntReply', [
        TextInt('val1'), ConstStr('sep1', ','), TextInt('val2'), ConstStr('sep2', ','),
        TextInt('val3'), ConstStr('sep3', ','), TextInt('val4'), ConstStr('sep4', ','),
        TextInt('val5'), ConstStr('sep5', ','), TextInt('val6'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntFloatEIntFloatEIntFloatEReply', [
        TextInt('val1'), ConstStr('sep1', ','), TextFloat('val2', exponentMode=True), ConstStr('sep2', ','),
        TextInt('val3'), ConstStr('sep3', ','), TextFloat('val4', exponentMode=True), ConstStr('sep4', ','),
        TextInt('val5'), ConstStr('sep5', ','), TextFloat('val6', exponentMode=True), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgFloatFloatFloatReply', [TextFloat('val1'), ConstStr('sep1', ','),
        TextFloat('val2'), ConstStr('sep2', ','), TextFloat('val3'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntFloatEFloatEReply', [
        TextInt('val1'), ConstStr('sep1', ','),
        TextFloat('val2', exponentMode=True), ConstStr('sep2', ','),
        TextFloat('val3', exponentMode=True), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntFloatEFloatEReply', [
        TextInt('val1'), ConstStr('sep1', ','),
        TextInt('val2'), ConstStr('sep2', ','),
        TextFloat('val3', exponentMode=True), ConstStr('sep3', ','),
        TextFloat('val4', exponentMode=True), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgFloatEFloatEFloatEReply', [
        TextFloat('val1', exponentMode=True), ConstStr('sep1', ','),
        TextFloat('val2', exponentMode=True), ConstStr('sep2', ','),
        TextFloat('val3', exponentMode=True), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgStringStringStringReply', [
        TerminatedStr('str1', ','),
        TerminatedStr('str2', ','),
        TerminatedStr('str3', '\r\n')]))
    centerController.add(Msg('MsgStringReply', [TerminatedStr('val', '\r\n')]))
    centerController.add(Msg('MsgRequest', [TerminatedStr('cmd', '\r\n')]))
    centerController.add(Msg('MsgIntSet', [
        TerminatedStr('cmd', ','), TextInt('val'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntSet', [
        TerminatedStr('cmd', ','), TextInt('val1'), ConstStr('sep', ','),
        TextInt('val2'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntIntSet', [
        TerminatedStr('cmd', ','), TextInt('val1'), ConstStr('sep1', ','),
        TextInt('val2'), ConstStr('sep2', ','), TextInt('val3'), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgFloatFloatFloatSet', [
        TerminatedStr('cmd', ','), TextFloat('val1', decimalPlaces=2), ConstStr('sep1', ','),
        TextFloat('val2', decimalPlaces=2), ConstStr('sep2', ','),
        TextFloat('val3', decimalPlaces=2), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgFloatEFloatEFloatESet', [TerminatedStr('cmd', ','),
        TextFloat('val1', decimalPlaces=4, exponentMode=True), ConstStr('sep1', ','),
        TextFloat('val2', decimalPlaces=4, exponentMode=True), ConstStr('sep2', ','),
        TextFloat('val3', decimalPlaces=4, exponentMode=True), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntIntFloatEFloatESet', [TerminatedStr('cmd', ','),
        TextInt('val1'), ConstStr('sep1', ','),
        TextInt('val2'), ConstStr('sep2', ','),
        TextFloat('val3', decimalPlaces=4, exponentMode=True), ConstStr('sep3', ','),
        TextFloat('val4', decimalPlaces=4, exponentMode=True), ConstStr('post', '\r\n')]))
    centerController.add(Msg('MsgIntFloatEFloatESet', [TerminatedStr('cmd', ','),
        TextInt('val1'), ConstStr('sep1', ','),
        TextFloat('val2', decimalPlaces=4, exponentMode=True), ConstStr('sep2', ','),
        TextFloat('val3', decimalPlaces=4, exponentMode=True), ConstStr('post', '\r\n')]))
    # Protocols
    centerController.add(Protocol('protocolCommand', ['MsgAck', 'MsgNack'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntReply', ['MsgIntReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntIntReply', ['MsgIntIntReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntIntIntReply', ['MsgIntIntIntReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntIntIntIntIntIntReply', ['MsgIntIntIntIntIntIntReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolFloatFloatFloatReply', ['MsgFloatFloatFloatReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolFloatEFloatEFloatEReply', ['MsgFloatEFloatEFloatEReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolBinaryReply', ['MsgBinaryReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolStringStringStringReply',
        ['MsgStringStringStringReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntFloatEIntFloatEIntFloatEReply', ['MsgIntFloatEIntFloatEIntFloatEReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolStringReply', ['MsgStringReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntIntFloatEFloatEReply', ['MsgIntIntFloatEFloatEReply'], rxPollPeriod=2.0))
    centerController.add(Protocol('protocolIntFloatEFloatEReply', ['MsgIntFloatEFloatEReply'], rxPollPeriod=2.0))
    # Create things
    centerController.generate()

    # The COOLPAK controller
    coolpak = Asyn("coolpak")
    # PVs
    coolpak.add(Pv("connection", enum=['Disconnected', 'Connected'],
        accessMode=Asyn.readOnly, archiverTag=True))
    coolpak.add(Pv('systemMode', enum=['Off', 'On'], autosaveTag=True, archiverTag=True))
    coolpak.add(Pv('head1Mode', enum=['Off', 'On'], autosaveTag=True, archiverTag=True))
    coolpak.add(Pv('head2Mode', enum=['Off', 'On'], autosaveTag=True, archiverTag=True))
    coolpak.add(Pv('swVer', dataType=Asyn.stringType, accessMode=Asyn.readOnly))
    coolpak.add(Pv('loggedTime', dataType=Asyn.stringType, accessMode=Asyn.readOnly, egu='hrs'))
    coolpak.add(Pv('upTime', dataType=Asyn.stringType, accessMode=Asyn.readOnly, egu='s'))
    coolpak.add(Pv('data', dataType=Asyn.longStringType, accessMode=Asyn.readOnly))
    coolpak.add(Pv('errors', dataType=Asyn.longStringType, accessMode=Asyn.readOnly))
    # Messages
    coolpak.add(Msg('MsgSysOff', [ConstStr('pre','\002'),ConstStr('mn','SYS0\r')]))
    coolpak.add(Msg('MsgSysOn', [ConstStr('pre','\002'),ConstStr('mn','SYS1\r')]))
    coolpak.add(Msg('MsgHeadOneOff', [ConstStr('pre','\002'),ConstStr('mn','SC10\r')]))
    coolpak.add(Msg('MsgHeadOneOn', [ConstStr('pre','\002'),ConstStr('mn','SC11\r')]))
    coolpak.add(Msg('MsgHeadTwoOff', [ConstStr('pre','\002'),ConstStr('mn','SC20\r')]))
    coolpak.add(Msg('MsgHeadTwoOn', [ConstStr('pre','\002'),ConstStr('mn','SC21\r')]))
    coolpak.add(Msg('MsgDatReq', [ConstStr('pre','\002'),ConstStr('mn','DAT\r')]))
    coolpak.add(Msg('MsgDatRsp', [ConstStr('pre','\002'),ConstStr('mn','DAT'), 
    	TerminatedStr('swVer', '/'), TerminatedStr('int1', '/'), TerminatedStr('hours', '/'), 
    	TerminatedStr('int2', '/'), TerminatedStr('uptime', '/'), TerminatedStr('dat', '\r')]))
    coolpak.add(Msg('MsgErrReq', [ConstStr('pre','\002'),ConstStr('mn','ERR\r')]))
    coolpak.add(Msg('MsgErrRsp', [ConstStr('pre','\002'),ConstStr('mn','ERR'), TerminatedStr('dat', '\r')]))
    # Protocols
    coolpak.add(Protocol('protocolSys', ['MsgSysOff', 'MsgSysOn'], rxPollPeriod=2.0))
    coolpak.add(Protocol('protocolHeadOne', ['MsgHeadOneOff', 'MsgHeadOneOn'], rxPollPeriod=2.0))
    coolpak.add(Protocol('protocolHeadTwo', ['MsgHeadTwoOff', 'MsgHeadTwoOn'], rxPollPeriod=2.0))
    coolpak.add(Protocol('protocolDat', ['MsgDatRsp'], rxPollPeriod=2.0))
    coolpak.add(Protocol('protocolErr', ['MsgErrRsp'], rxPollPeriod=2.0))
    # Create things
    coolpak.generate()

