#!/dls_sw/prod/tools/RHEL6-x86_64/Python/2-7-3/prefix/bin/python2.7

from pkg_resources import require
require("dls_serial_sim==1.17")

from dls_serial_sim import serial_device
import time


Remote = "Remote"
Local = "Local"

class stanfordDG645_sim(serial_device):
    Terminator = "\r\n"
    def __init__(self):
        self.vals = {"Remote":Local, "2":[0,0.0], "3":[0,0.0], "4":[0,0.0], "5":[0,0.0], "6":[0,0.0], "7":[0,0.0], "8":[0,0.0], "9":[0,0.0]}
    def reply(self, cmd):
        print cmd
        if cmd == "REMT":
            self.vals["Remote"] = Remote
        elif cmd == "LCAL":
            self.vals["Remote"] = Local
        elif cmd.startswith("DLAY"):        
            chan = cmd[5]
            if chan in self.vals.keys():
                if cmd[4] == '?':
                    return "%d,+%f"% (self.vals[chan][0], self.vals[chan][1])
                elif self.vals["Remote"] == Local:
                    return "REMERR"
                else:
                    lnchan = int(cmd[7])
                    self.vals[chan][0]=lnchan
                    arg = float(cmd[9:])
                    self.vals[chan][1]=arg
            else:
                return "SYNERR"
        else:
            return "COMERR"
            
        return cmd
    
        

if __name__ == "__main__":
    dev = stanfordDG645_sim()
    dev.start_ip(9015)
    dev.start_debug(9017)
    while True:
        time.sleep(1)
