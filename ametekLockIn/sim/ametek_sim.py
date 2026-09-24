#!/dls_sw/prod/tools/RHEL6-x86_64/Python/2-7-3/prefix/bin/python2.7

from pkg_resources import require
require("dls_serial_sim==1.17")

from dls_serial_sim import serial_device
import time

class ametek_sim(serial_device):
    Terminator = "\r\n"
    def __init__(self):
        self.vals = {"X": 3.2, "TC": 0.01}
    def reply(self, cmd):
        if cmd == "X.":
            return self.vals["X"]
        elif cmd == "TC.":
            return self.vals["TC"]
        elif cmd[:3] == "TC ":
            tc = int(cmd[3:])
            mult = 10**(tc/3)
            mant = (tc%3)**2 + 1
            print tc, mult, mant
            self.vals["TC"] = mult*mant*1e-5
        else:
            return "Unknown command"

if __name__ == "__main__":
    dev = ametek_sim()
    dev.start_ip(9004)
    dev.start_debug(9006)
    while True:
        time.sleep(1)
