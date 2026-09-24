
#!dls-python2.6

from pkg_resources import require
require('dls_serial_sim')
from dls_serial_sim import serial_device
import re, os, time

#*!*Section simulationProtocol begin*!*
class MsgFloatReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val = TextFloat(self, 8, False)
        self.post = ConstStr(self, '\r')
class MsgIntReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val = TextInt(self, 10)
        self.post = ConstStr(self, '\r')
class MsgGetMoveReady(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 q90\r')
class MsgGetPivotX(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q70=7 Q94\r')
class MsgSetPivotX(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q94=')
        self.val = TextFloat(self, 8, False)
        self.post = ConstStr(self, ' Q70=6 Q94\r')
class MsgGetPivotY(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q70=7 Q95\r')
class MsgSetPivotY(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q95=')
        self.val = TextFloat(self, 8, False)
        self.post = ConstStr(self, ' Q70=6 Q95\r')
class MsgGetPivotZ(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q70=7 Q96\r')
class MsgSetPivotZ(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q96=')
        self.val = TextFloat(self, 8, False)
        self.post = ConstStr(self, ' Q70=6 Q96\r')
class MsgSetLinearRes(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q98=')
        self.val = TextFloat(self, 8, False)
        self.post = ConstStr(self, ' Q98\r')
class MsgSetAngularRes(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 Q99=')
        self.val = TextFloat(self, 8, False)
        self.post = ConstStr(self, ' Q99\r')
class MsgGetM1(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '#1 P\r')
class MsgGetM2(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '#2 P\r')
class MsgGetM3(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '#3 P\r')
class MsgGetM4(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '#4 P\r')
class MsgGetM5(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '#5 P\r')
class MsgGetM6(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '#6 P\r')
class MsgGetSysErr(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 q91\r')
class MsgGetPosErr(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 q92\r')
class MsgResetSysErr(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '&2 q91=0\r')
class MsgInitialise(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre1 = ConstStr(self, '\x01&2 define lookahead 10,1\r')
        self.pre2 = ConstStr(self, '&2 q70=1\r')
#*!*Section simulationProtocol end*!*

class spacefab(serial_device):
    Terminator = "\r"

    def __init__(self, name="none", ui=None, tcpPort=9015, rpcPort=9016):
        # Constructor.  Remember to call the base class constructor.
        self.name = name
        serial_device.__init__(self, ui=ui)
        self.diagnostic("Initialising spacefab simulator, V1.0")
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
    dev = spacefab()
    # cheesy wait to stop the program exiting immediately
    while True:
        time.sleep(1)
