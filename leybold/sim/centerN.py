
#!dls-python2.6

from pkg_resources import require
require('dls_serial_sim')
from dls_serial_sim import serial_device
import re, os, time

#*!*Section simulationProtocol begin*!*
class MsgAck(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x06\r\n')
class MsgNack(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x15\r\n')
class MsgEnq(Message):
    def __init__(self):
        Message.__init__(self)
        self.pre = ConstStr(self, '\x05')
class MsgBinaryReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val = TextInt(self, 2)
        self.post = ConstStr(self, '\r\n')
class MsgIntReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextInt(self, 10)
        self.sep = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntIntReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntIntIntIntIntReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextInt(self, 10)
        self.sep3 = ConstStr(self, ',')
        self.val4 = TextInt(self, 10)
        self.sep4 = ConstStr(self, ',')
        self.val5 = TextInt(self, 10)
        self.sep5 = ConstStr(self, ',')
        self.val6 = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgIntFloatEIntFloatEIntFloatEReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 1, True)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextInt(self, 10)
        self.sep3 = ConstStr(self, ',')
        self.val4 = TextFloat(self, 1, True)
        self.sep4 = ConstStr(self, ',')
        self.val5 = TextInt(self, 10)
        self.sep5 = ConstStr(self, ',')
        self.val6 = TextFloat(self, 1, True)
        self.post = ConstStr(self, '\r\n')
class MsgFloatFloatFloatReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextFloat(self, 1, False)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 1, False)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 1, False)
        self.post = ConstStr(self, '\r\n')
class MsgIntFloatEFloatEReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 1, True)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 1, True)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntFloatEFloatEReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 1, True)
        self.sep3 = ConstStr(self, ',')
        self.val4 = TextFloat(self, 1, True)
        self.post = ConstStr(self, '\r\n')
class MsgFloatEFloatEFloatEReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val1 = TextFloat(self, 1, True)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 1, True)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 1, True)
        self.post = ConstStr(self, '\r\n')
class MsgStringStringStringReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.str1 = TerminatedStr(self, ',')
        self.str2 = TerminatedStr(self, ',')
        self.str3 = TerminatedStr(self, '\r\n')
class MsgStringReply(Message):
    def __init__(self):
        Message.__init__(self)
        self.val = TerminatedStr(self, '\r\n')
class MsgRequest(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, '\r\n')
class MsgIntSet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntSet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val1 = TextInt(self, 10)
        self.sep = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntIntSet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextInt(self, 10)
        self.post = ConstStr(self, '\r\n')
class MsgFloatFloatFloatSet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val1 = TextFloat(self, 2, False)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 2, False)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 2, False)
        self.post = ConstStr(self, '\r\n')
class MsgFloatEFloatEFloatESet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val1 = TextFloat(self, 4, True)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 4, True)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 4, True)
        self.post = ConstStr(self, '\r\n')
class MsgIntIntFloatEFloatESet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextInt(self, 10)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 4, True)
        self.sep3 = ConstStr(self, ',')
        self.val4 = TextFloat(self, 4, True)
        self.post = ConstStr(self, '\r\n')
class MsgIntFloatEFloatESet(Message):
    def __init__(self):
        Message.__init__(self)
        self.cmd = TerminatedStr(self, ',')
        self.val1 = TextInt(self, 10)
        self.sep1 = ConstStr(self, ',')
        self.val2 = TextFloat(self, 4, True)
        self.sep2 = ConstStr(self, ',')
        self.val3 = TextFloat(self, 4, True)
        self.post = ConstStr(self, '\r\n')
#*!*Section simulationProtocol end*!*

class centerN(serial_device):
    Terminator = "\r"

    def __init__(self, name="none", ui=None, tcpPort=9015, rpcPort=9016):
        # Constructor.  Remember to call the base class constructor.
        self.name = name
        serial_device.__init__(self, ui=ui)
        self.diagnostic("Initialising centerN simulator, V1.0")
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
    dev = centerN()
    # cheesy wait to stop the program exiting immediately
    while True:
        time.sleep(1)
