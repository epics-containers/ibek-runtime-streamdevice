#!/dls_sw/tools/bin/python2.4

from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation

#import sys
#sys.path.append("/dls_sw/work/common/python/serial_sim")
#from src import serial_device

from random import randrange as r

STX = "\x02"
ETX = "\x03"
EOT = "\x04"
ENQ = "\x05"
ACK = "\x06"


class eurotherm2k(serial_device):

    OutTerminator = ""
    vals = {}
    
    def __init__(self,gad=0,lad=1):
        # store gad and lad, and initialise internal dict
        self.gad = str(gad)
        self.lad = str(lad)
        self.vals = { "XP": 100,
                      "TI": 150,
                      "TD": 200,
                      "S1": 70.0,
                      "PV": 60.0,
                      "RR": 1.0,
                      "OP": 100.0,
                      "EE": ">0",
                      "mA": "0" }
        self.branches = self.vals.keys() + [ x + "_WRITE" for x in self.vals ]
        self.schedule(self.inc,0.1)              
    
    def inc(self): 
        # increment PV by RR until it is at S1
        if self.vals["PV"] < self.vals["S1"]:
            self.vals["PV"] = min(self.vals["S1"],self.vals["PV"]+self.vals["RR"]/10.0)
        elif self.vals["PV"] > self.vals["S1"]:
            self.vals["PV"] = max(self.vals["S1"],self.vals["PV"]-self.vals["RR"]/10.0)

    def listen(self,command):
        """Reimplemented to return anything between EOT and ETX or ENQ"""
        if not command.startswith(EOT):
            return ""
        if command.endswith(ETX) or command.endswith(ENQ):
            return ("",command[:-1])
        else:
            return EOT + command.lstrip(EOT) 

    def reply(self,command):
        if not (self.gad == command[1] == command[2]):
            return
        if not (self.lad == command[3] == command[4]):
            return
        if len(command)<9:
            # this is a read command, note ENQ stripped off
            # [EOT](GID)(GID)(UID)(UID)(CHAN)(C1)(C2)[ENQ}
            key = command[-2:]
            chan = command[5:-2]
            # return junk as epics throws away bcc
            # [STX](CHAN)(C1)(C2)<DATA>[ETX](BCC)
            try:
                v = "%5f" % self.vals[key]
            except:
                v = str(self.vals[key])                
            self.covered(key)            
            return STX + chan + key + v + ETX + "11"
        else:
            # this is a write command, note ETX and BCC stripped off
            # [EOT](GID)(GID)(UID)(UID)[STX](CHAN)(C1)(C2)<DATA>[ETX](BCC)
            try:
                chan = int(command[6])
            except ValueError:
                chan = ""
                command = command[:6]+" "+command[6:]
            key = command[7:9]
            self.covered(key+"_WRITE")                                        
            self.vals[key] = float(command[9:])
            return ACK            

if __name__=="__main__":
    CreateSimulation(eurotherm2k)
    raw_input()
