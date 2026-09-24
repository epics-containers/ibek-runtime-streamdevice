
#!dls-python2.6

from pkg_resources import require
require('dls_serial_sim')
from dls_serial_sim import serial_device
import re, os, time

#*!*Section simulationProtocol begin*!*
class MsgSysOff(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'SYS0\r')
class MsgSysOn(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'SYS1\r')
class MsgHeadOneOff(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'SC10\r')
class MsgHeadOneOn(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'SC11\r')
class MsgHeadTwoOff(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'SC20\r')
class MsgHeadTwoOn(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'SC21\r')
class MsgDatReq(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'DAT\r')
class MsgDatRsp(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'DAT')
        self.swVer = TerminatedStr(self, '/')
        self.int1 = TerminatedStr(self, '/')
        self.hours = TerminatedStr(self, '/')
        self.int2 = TerminatedStr(self, '/')
        self.uptime = TerminatedStr(self, '/')
        self.dat = TerminatedStr(self, '\r')
class MsgErrReq(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'ERR\r')
class MsgErrRsp(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x02')
        self.mn = ConstStr(self, 'ERR')
        self.dat = TerminatedStr(self, '\r')
#*!*Section simulationProtocol end*!*

class coolpak(serial_device):
    Terminator = "\r"

    def __init__(self, name="none", ui=None, tcpPort=9015, rpcPort=9016):
        # Constructor.  Remember to call the base class constructor.
        self.name = name
        serial_device.__init__(self, ui=ui)
        self.diagnostic("Initialising coolpak simulator, V1.0")
        self.start_ip(tcpPort)
        self.start_rpc(rpcPort)

    def listen(self, command):
        # This function breaks the data stream into messages.  The base class
        # version uses the InTerminator to detect message ends.  Replace if
        # another method of message detection is required.
        return serial_device.listen(self, command)

    def reply(self, command):
        # This function must be defined. It is called by the serial_sim system
        # whenever an asyn command is send down the line. Must return a string
        # with a response to the command or None.
        result = None

        # Parse the command
        # TODO

        # Handle the request
        #*!*Section simulation begin*!*
        #*!*Section simulation end*!*

        return result

    def initialise(self):
        # Called by the framework when the power is switched on.
        pass

if __name__ == "__main__":
    # little test function that runs only when you run this file
    dev = coolpak()
    # cheesy wait to stop the program exiting immediately
    while True:
        time.sleep(1)
