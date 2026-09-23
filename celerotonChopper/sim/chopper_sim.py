	
	#!/dls_sw/prod/tools/RHEL7-x86_64/defaults/bin/dls-python

'''
    Simulator for Celeroton Chopper Interface
    2019 - Mateusz Hoppe
'''
from pkg_resources import require
import imp
require('dls_serial_sim')
from dls_serial_sim import serial_device, CreateSimulation
import time
from time import gmtime, strftime
import datetime
from timeit import default_timer as timer
import math, random, re
from random import randint
import struct
import chopper_dictionary
from chopper_dictionary import Commands, VariableTypes, Variables, ErrorCodes, OKCode, WarningCode, InfoCode

StartTime  = 0
StopTime   = 0
ProcTime   = 0


class DataFrame:
    def __init__(self):
        self.Length     = 0 
        self.Command    = 0
        self.Data       = 0
        self.Checksum   = 0


class chopper(serial_device):

    def __init__(self, name="chopper", ui=None, tcpPort=9004):
        self.name = name
        self.tcpPort = tcpPort
        serial_device.__init__(self, ui=ui)
        self.start_ip(tcpPort)
        self.addressed = False

    def printFrame(self,frame, frame_type):
        makeBlue = "\033[94m"
        makeGreen = "\033[32m"
        endColour = "\033[0m"
        f = bytearray(frame)
        if frame_type == "command":
            print makeGreen,"Command OK : "
        elif frame_type == "reply":
            print makeBlue, "Sending response"
        print (", ".join("\\x%02X" % v for v in f))
        print endColour

    def parseCommand(self,command):
        cmd=DataFrame()
        cmdBytes = bytes(command)
        cmd.Length = cmdBytes[0]
        cmd.Command = cmdBytes[1]
        dataLength = ord(cmd.Length)-2 # -2 because one is command, one is checksum
        if dataLength > 0: # if we expect data bytes
            cmd.Data = cmdBytes[2:2+dataLength]
            cmd.Checksum = cmdBytes[2+dataLength-1]
        else:
            cmd.Checksum = cmdBytes[2]
        return cmd

    def randomizeReplyValue(self,value):
        value = random.uniform(0.95,1.05)*value
        return value

    def findpFormat(self,var_bc):
        for t, t_data in VariableTypes.items():
            if t_data['ByteCode'] == var_bc:
                return t_data['pFormat']
        return 0

    def generateReply(self,cmd):
        frame = bytearray([
            Commands[cmd.Command]["ReplyLength"], cmd.Command
            ])
        ############################ get status ###########################################################
        if cmd.Command == '\x00':
            global StartTime
            StartTime = timer()
            words = 0
            for t, t_data in ErrorCodes.items():
                if t_data['Simulate'] == 1:
                    frame.extend(tuple(t_data['ByteSequence']))
                    words += 1
                if words == 2:
                    break # send maximum 2 error codes
            while words < 2:
                frame.extend(tuple(OKCode))
                words += 1
            frame.extend(tuple(WarningCode))
            frame.extend(tuple(InfoCode))                                
        ########################## acknowledge errors #####################################################
        elif cmd.Command == '\x01': 
            ErrorCodesReceived = [cmd.Data[0:4],cmd.Data[4:8]]
            for t, t_data in ErrorCodes.items():
                if t_data['ByteSequence'] in ErrorCodesReceived:
                    t_data['Simulate'] = 0
        ############################ read value ############################################################
        elif cmd.Command == '\x04':
            if (cmd.Data) == '\x08':
                global StopTime
                StopTime = timer()
            VarType = Variables[cmd.Data]['Type']
            frame.append(VariableTypes[VarType]['ByteCode'])
            if Variables[cmd.Data]['Fluctuating']:
                Value = self.randomizeReplyValue(Variables[cmd.Data]['SimValue'])
            else:
                Value = Variables[cmd.Data]['SimValue']
            value_bytearray = tuple(struct.pack(VariableTypes[VarType]['pFormat'], Value))
            frame.extend(value_bytearray)
        ############################ write value ############################################################
        elif cmd.Command == '\x05': 
            Variables[cmd.Data[0]]['SimValue'] = struct.unpack(self.findpFormat(cmd.Data[1]),cmd.Data[2:])[0]
        #####################################################################################################
        checksum = (~sum(frame) + 1) & 0xff
        frame.append(checksum)
        return frame

    def reply(self, command):
        result = None
        reload(chopper_dictionary)
        print datetime.datetime.utcnow()
        self.printFrame(command,"command")
        cmd = self.parseCommand(command)
        result = self.generateReply(cmd)
        self.printFrame(result,"reply")

        global ProcTime
        if (StartTime!=0) & (StopTime!=0) & (StopTime>StartTime):
            ProcTime = StopTime - StartTime
            print "StartTime: " 
            print StartTime
            print "StopTime: "
            print StopTime
            print "ProcTime: " 
            print ProcTime
        return result

if __name__ == "__main__":
    CreateSimulation(chopper)
    while 1 :
        time.sleep(1)