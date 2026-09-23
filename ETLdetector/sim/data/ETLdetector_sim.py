#!/bin/env python2.4

from pkg_resources import require

require("dls.serial_sim==1.3")

from dls.serial_sim import serial_device
from random import randrange as r

class ETLdetector(serial_device):

    Terminator = "\r"
    dets = {}
    
    def __init__(self,addresses):
        # take a list of addresses
        for address in addresses:
            vals = {"v":0, # HV
                    "i":4088, # RefV
                    "#Du":0, # Upper limit
                    "#Dl":0 } # Lower limit
            address = str(address)
            # and create a detector value dictionary for each one
            self.dets["0"*(3-len(address))+address]=vals

    def reply(self,command):
        addr = command[:3]
        text = command[3:]
        # check the address is one of the detectors on the bus
        if addr not in self.dets.keys():
            return None
        elif text in ["v","i","#Du","#Dl"]:
            # readback something, e.g. 001v might return 001v123
            ret = command + "%03X"%self.dets[addr][text]
        elif text[:-3] in ["V","I","#DU","#DL"]:
            # set something, e.g. 001V010 sets v=int(0x010)=16
            name = text[:-4]+text[-4:-3].lower()
            val = int(text[-3:],16)
            self.dets[addr][name] = val
            ret = command
        elif text.startswith("r"):
            if command[4]=="1" or command[4]=="3":
                # readback 'real' HV voltage, e.g. 001r3010
                HV = r(self.dets[addr]["v"]-10,self.dets[addr]["v"]+10)
                if HV<0: HV=0
                ret = command+"%03X"%HV
            elif command[4]=="2":
                # readback generator current, e.g. 001r2300
                ret = command+"%03X"%r(400,500)
        elif text in ["?","#D?"]:
            # version strings
            ret = command + "SIMM"
        else:
            # Any other commands just need confirmation
            ret = command
    	# note the return of the command + terminator to mimic 8516 mode 1 (half duplex with local echo)
    	ret = command + self.Terminator + ret
        # protocol has a leading \r, because detector sometimes needs the buffer clearing, so add it
        if "#D" in ret:
        	ret = self.Terminator + ret
        return ret
        	
    	

if __name__ == "__main__":
    import os
    det = ETLdetector([0,1,2])
    det.start_ip(9004)
#    det.start_serial("port")
#    print os.environ["port"]
    det.start_debug(9006)
