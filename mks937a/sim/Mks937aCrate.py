#!/bin/env dls-python2.6

if __name__=="__main__":
    from pkg_resources import require
    require("dls_serial_sim")

from dls_serial_sim import serial_device, CreateSimulation

# Represents a single channel of the gauge control crate.
class Mks937aChannel(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.pressure = 0.0001
        self.controlSetPoint = 0.0
        self.relaySetPoint = 0.0
        self.protectionSetPoint = 0.0
        self.coldCathodeEnable = True

    def getPressure(self):
        result = '%.1E' % self.pressure
        if self.type == 'img':
            if not self.coldCathodeEnable:
                result = 'HV_OFF'
            elif self.pressure > 0.01:
                result = 'HI'
        elif self.type == 'pirani':
            if self.pressure < 0.001:
                result = 'LO'
        else:
            result = 'NOGAUGE!'
        return result

# The MKS937A gauge control crate.  Each crate has five channels, two IMG, two
# pirani and one unused.  The crate can supply interlock source signals.
class Mks937aCrate(serial_device):

    def __init__(self, name='', tcpPort=None, ui=None):
        self.name = name
        serial_device.__init__(self, ui=ui)
        self.gauges = {}
        self.gauges[1] = Mks937aChannel(name+':1', 'img')
        self.gauges[2] = Mks937aChannel(name+':2', 'img')
        self.gauges[3] = Mks937aChannel(name+':3', '')
        self.gauges[4] = Mks937aChannel(name+':4', 'pirani')
        self.gauges[5] = Mks937aChannel(name+':5', 'pirani')
        serial_device.Terminator = "\r"
        if tcpPort:
            self.start_ip(tcpPort)
        self.diagnostic("Created MKS937A crate %s" % name)

    def createUi(self):
        '''Override to create the user interface for the simulation.'''
        return TerminalWindow()
    
    def getInterlock(self, signal, bit):
        result = False
        gauge = self.gauges[signal]
        if bit == 0:
            result = gauge.pressure <= gauge.relaySetPoint
        return result

    def gauge(self, number):
        result = None
        if number in self.gauges:
            result = self.gauges[number]
        return result

    def reply(self, command):
        result = None
        param = None
        printMessage = True
        cmd = command.strip()
        if '=' in cmd:
            parts = cmd.split('=')
            cmd = parts[0]
            param = parts[1]
        if len(cmd) > 1:
            n = None
            if cmd[-1] in '12345':
                n = int(cmd[-1])
                cmd = cmd[:-1]
            if cmd == 'R' and n is not None and param is None:
                result = "%s" % self.gauges[n].getPressure()
                printMessage = False
            elif cmd == 'CTL' and n is not None:
                if param is None:
                    result = "%s" % self.gauges[n].controlSetPoint
                    printMessage = False
                else:
                    self.gauges[n].controlSetPoint = float(param)
                    result = "OK"
            elif cmd == 'PRO' and n is not None:
                if param is None:
                    result = "%s" % self.gauges[n].protectionSetPoint
                    printMessage = False
                else:
                    self.gauges[n].protectionSetPoint = float(param)
                    result = "OK"
            elif cmd == 'RLY' and n is not None:
                if param is None:
                    result = "%s" % self.gauges[n].relaySetPoint
                    printMessage = False
                else:
                    self.gauges[n].relaySetPoint = float(param)
                    result = "OK"
            elif cmd == 'ECC' and n is not None and param is None:
                self.gauges[n].coldCathodeEnable = True
                result = "OK"
            elif cmd == 'XCC' and n is not None and param is None:
                self.gauges[n].coldCathodeEnable = False
                result = "OK"
            elif cmd == 'VER' and n is None and param is None:
                result = "1.00,1.10"
                printMessage = False
            elif cmd == 'FREQ' and n is None and param is None:
                result = "50Hz"
                printMessage = False
            elif cmd == 'UNIT' and n is None and param is None:
                result = "mbar"
                printMessage = False
            elif cmd == 'GAUGES' and n is None and param is None:
                result = "CcCcCv"
                printMessage = False
        if printMessage:
            text = "%s==>%s" % (repr(command), repr(result))
            self.diagnostic(text, 4)
        return result

if __name__=="__main__":
    # run our simulation on the command line. Run this file with -h for help
    CreateSimulation(Mks937aCrate)
    raw_input()

