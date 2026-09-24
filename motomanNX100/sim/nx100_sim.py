#!/bin/env python2.6

from pkg_resources import require
require("dls_serial_sim")
from random import randrange as r

from dls_serial_sim import serial_device, CreateSimulation

class nx100(serial_device):

    OutTerminator = "\r";
    InTerminator = "\r\n"
    SetCmds = ["SVON", "HOLD", "START"]
    TwoPartCmds = ["SAVEV", "LOADV", "RPOSC"]
    
    def __init__(self):
        # place your initialisation code here
        serial_device.__init__(self)
        self.cmd = None
        self.vals = dict(SVON="0", HOLD="0", START="", S=1, L=2, U=3, R=4, B=5, T=6)
        self.vvars = { "1, 0": "9,8,7,6,5,4,0,0", # RPOSC
                        }
        self.schedule(self.tick, 0.08)        
        self.running = False                

    def tick(self):
        if self.running:  
            if self.vals["S"] > 300 or self.vals["SVON"]=="0" or self.vals["HOLD"]=="1":
                self.running = False
            else:
                self.vals["S"] += 2
                for ax in "LURBT":
                    self.vals[ax] += r(-4,4)
                self.vvars["1, 0"] = "%d,%d,%d,%d,%d,%d,0,0" % tuple([
                    self.vals["SLURBT"[i]] + self.vals["URBTSL"[i]] for i in range(6) ])

    def err(self, cmd, num):
        return "ERROR: %s is not successful(%04d)" % (cmd, num)
                        
    def reply(self,command):
        # reply to commands here
        if self.cmd is not None:
            ret = "0000"        
            if self.cmd in self.SetCmds:
                self.vals[self.cmd] = command
                if self.cmd == "START":
                    if command.strip():
                        self.running = True
                        if self.vals["SVON"]=="0":
                            ret = self.err(self.cmd, 1111)
                        elif self.vals["HOLD"]=="1":
                            ret = self.err(self.cmd, 2222)
                        else:
                            for x in "SLURBT":
                                self.vals[x] = 0
                    else:
                        ret = self.err(self.cmd, 3333)
            elif self.cmd == "LOADV":
                split = command.split(", ", 2)
                self.vvars[", ".join(split[:2])] = split[2]
            else:
                ret = self.vvars[command]               
            self.cmd = None
            return ret
        elif command.startswith("CONNECT"):
            return "OK: NX Information Server( TEST) Keep-Alive:-1."
            self.cmd = None
        elif command.startswith("HOSTCTRL_REQUEST"):
            cmd = command.split()[1]
            if cmd in self.SetCmds + self.TwoPartCmds:
                self.cmd = cmd
                return "OK: %s" % cmd
            elif cmd=="RSTATS":
                sta1 = self.running and 8 or 0
                sta1 += 128
                sta2 = (self.vals["SVON"] == "1") and 64 or 0
                sta2 += (self.vals["HOLD"] == "1") and 8 or 0
                ret = "%s,%s" % (sta1, sta2)
            elif cmd=="RPOSJ":
                ret = "%(S)d,%(L)d,%(U)d,%(R)d,%(B)d,%(T)d,0,0,0,0,0,0" % self.vals
            return "\r".join(["OK: %s" % cmd, ret])
                            

if __name__=="__main__":
    CreateSimulation(nx100)
    raw_input()
