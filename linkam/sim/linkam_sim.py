#!/dls_sw/prod/tools/RHEL6-x86_64/Python/2-7-3/prefix/bin/python2.7
# Simulates a Linkam MDS600 module. 

from pkg_resources import require
require("dls_serial_sim==1.17")
from dls_serial_sim import serial_device, CreateSimulation
from optparse import OptionParser
import time, math

OnState = "On"
OffState = "Off"
HoldState = "Hold"

def getNewVal(current, target, increment):
    if current != target:
        diff = target - current
        return (diff/abs(diff))*min(increment,abs(diff))
    else:
        return 0    

class MDS600_sim(serial_device):
    # Actual device uses carriage return only as terminator, but this seems to 
    # make it hard to telnet to the simulation.
    Terminator = "\r"
    debugLevel = 1
    def __init__(self):
    # need an init function to start the schedule function
	# Also set default starting values for internal variables.
        self.vals = {"EqTemperature":235, "Temperature":255, "RampRate":20.0, "RampLimit":30, "State":OffState, "XPos":0, "YPos":0, "XTarg":0, "YTarg":0, "XVelocity":5, "YVelocity":5, "Limit":3000, "Moving":False, "Paused":False}
        print "Starting Linkam MDS600 simulation", __file__
        self.schedule(self.inc,1.0)
    def inc(self):
        # Adjust the temperature
        if self.vals["State"] == OnState:
            newtemp = self.getNewTemp(self.vals["RampLimit"])
            self.vals["Temperature"] = newtemp
        elif self.vals["State"] == OffState:
            newtemp = self.getNewTemp(self.vals["EqTemperature"])
            self.vals["Temperature"] = newtemp
        # Move the motors
        if self.vals["XPos"] != self.vals["XTarg"] or self.vals["YPos"] != self.vals["YTarg"]:
            (x0,y0,xt,yt,vx,vy,r)=(self.vals["XPos"],self.vals["YPos"],self.vals["XTarg"],self.vals["YTarg"],self.vals["XVelocity"],self.vals["YVelocity"],self.vals["Limit"])
            (newX, newY) = (getNewVal(x0,xt,vx),getNewVal(y0,yt,vy))
            if newX == 0 and newY == 0:
                self.vals["Moving"] = False

            if not self.vals["Moving"] or self.vals["Paused"]:
                return

            # Manual suggests limit is circular, but in fact it is square.
            # Note testing shows actual limit checking is done when command
            # is queued, not when motor reaches limit - so changing limit once
            # already moving will do nothing.
            #if math.hypot(newXY[0]+x0,newXY[1]+y0) > r:
            # if abs(newX + x0) > self.vals["Limit"]:
            #     if self.debugLevel > 1:
            #         print "At x limit", self.vals["XPos"], self.vals["Limit"]
            #     self.vals["XTarg"] = self.vals["XPos"]
            # else:
            self.vals["XPos"] = x0+newX
            if self.debugLevel > 1:
                print "Moved X to ", self.vals["XPos"]

            # if abs(newY + y0) > self.vals["Limit"]:
            #     if self.debugLevel > 1:
            #         print "At y limit", self.vals["YPos"], self.vals["Limit"]
            #     self.vals["YTarg"] = self.vals["YPos"]
            # else:
            self.vals["YPos"] = y0+newY
            if self.debugLevel > 1:
                print "Moved Y to ", self.vals["YPos"]



    def reply(self, command):
        if self.debugLevel > 1:
            print command
        if command.startswith("T"):
            # Return full status string
            retStr = "{0}{1}{2}{3}{4}{5:0>4}".format(chr(self.getStatus()) ,chr(0x80), chr(0x80), self.getMotorStatus(), "MM", self.getRetTemp())
            return retStr
        elif command.startswith("R1"):
            # Set temp ramp rate
            rr = int(command[2:])/10/60.0
            if self.debugLevel > 1:
                print "Set ramp rate to %i" % rr
            self.vals["RampRate"] = rr
            return ""

        elif command.startswith("L1"):
            # Set temp ramp limit
            rl = int(command[2:])
            if self.debugLevel > 1:
                print "Set ramp limit to %i" % rl
            self.vals["RampLimit"] = rl
            return ""
# 'E' is End, 'S' is Start, 'O' is Off (on the GUI these are Stop, Start and Hold, respectively). 
        elif command in ("E", "S", "O"):
            # Set temperature ramp mode
            if command == "S":
                self.vals["State"] = OnState
            elif command == "E":
                self.vals["State"] = OffState
            else:
                self.vals["State"] = HoldState
            if self.debugLevel > 1:
                print "Temperature ramp set to ", command
            return ""
        elif command == "\xefS":
            # Get device name
            return "MDS600 Sim"
        elif command == "M?":
            # Get status byte
            return self.getMotorStatus()
        elif command == "Mp":
            # Get current position
            # Note motor status byte is returned as second byte, not a ?.
            return "M{0}{1},{2},{3}".format(self.getMotorStatus(),self.vals["XPos"], self.vals["YPos"], 0)
        elif command == "MF2":
            # Move motors to reference (home)
            if self.debugLevel > 1:
                print "Homing"
            self.vals["XTarg"] = 0
            self.vals["YTarg"] = 0
            self.vals["Moving"] = True
            return "{0}".format(self.getMotorStatus())
        elif command == "MF1":
            # Set reference position
            if self.debugLevel > 1:
                print "Setting current position as reference", self.vals["XPos"], self.vals["YPos"]
            # Testing shows the motors stop if we reset the reference during 
            # a move. 
            self.vals["XTarg"] = 0
            self.vals["YTarg"] = 0
            self.vals["XPos"] = 0
            self.vals["YPos"] = 0
            return "{0}".format(self.getMotorStatus())
        elif command == "MSX":
            # Stop motors
            if self.debugLevel > 1:
                print "Stopped"
            self.vals["XTarg"] = self.vals["XPos"]
            self.vals["YTarg"] = self.vals["YPos"]
            return "{0}".format(self.getMotorStatus())
        elif command == "MP":
            # Pause motors
            self.vals["Paused"] = True
            return "{0}".format(self.getMotorStatus())
        elif command == "MR":
            # Resume motors
            self.vals["Paused"] = False
            return "{0}".format(self.getMotorStatus())
        elif command.startswith("MVX"):
            # Set velocity
            # Note this isn't exactly how the device handles -ve args - 
            # but it does at least still result in a positive velocity, so 
            # not going to worry about this. 
            self.vals["XVelocity"] = min(abs(int(command[3:])), 60000)
            if self.debugLevel > 1:
                print "Set x velocity to ", self.vals["XVelocity"]
            return "{0}".format(self.getMotorStatus())
        elif command.startswith("MVY"):
            # Set velocity
            self.vals["YVelocity"] = min(abs(int(command[3:])), 60000)
            if self.debugLevel > 1:
                print "Set y velocity to ", self.vals["YVelocity"]
            return "{0}".format(self.getMotorStatus())
        elif command.startswith("MM"):
            # Move to position
            # Note testing shows MMX and MMY are relative, not absolute moves.
            if command[2]=="X":
                self.vals["XTarg"] = self.vals["XPos"] + int(command[3:])
                # Note limit testing is done here, not during the move itself.
                # Hence also why MMR ignores the limit.
                if abs(self.vals["XTarg"]) > self.vals["Limit"]:
                    self.vals["XTarg"] = int(math.copysign(self.vals["Limit"], self.vals["XTarg"]))
                self.vals["Moving"] = True
                self.vals["Paused"] = False
            elif command[2]=="Y":
                self.vals["YTarg"] = self.vals["YPos"] + int(command[3:])
                if abs(self.vals["YTarg"]) > self.vals["Limit"]:
                    self.vals["YTarg"] = int(math.copysign(self.vals["Limit"], self.vals["YTarg"]))
                self.vals["Moving"] = True
                self.vals["Paused"] = False
            elif command[2]=="R":
                # This command actually ignores software limits, and moves to
                # absolute rather than relative positions.
                targets = command[3:].split(',')
                self.vals["XTarg"] = int(targets[0])
                self.vals["YTarg"] = int(targets[1])                
                self.vals["Moving"] = True
                self.vals["Paused"] = False
            else:
                print "Unrecognised command", command
            if self.debugLevel > 1:
                print "Move command, targets:", self.vals["XTarg"], self.vals["YTarg"]
            return "{0}".format(self.getMotorStatus())
        elif command.startswith("MLX"):
            # Set travel limit
            self.vals["Limit"] = int(command[3:])
            if self.debugLevel > 1:
                print "Set move limit to ", self.vals["Limit"]
            return "{0}".format(self.getMotorStatus())            
        else:
            return "Unrecognised command %s" % command

    def getNewTemp(self, target):
        return self.vals["Temperature"] + int(getNewVal(self.vals["Temperature"],target,self.vals["RampRate"]))
    def getStatus(self):
        temp = self.vals["Temperature"]
        if self.vals["State"] == OnState:
            if temp > self.vals["RampLimit"]:
                #Cooling
                return 32
            elif temp < self.vals["RampLimit"]:
                #Heating
                return 16
            else:
                #Hold limit/end
                return 48
        elif self.vals["State"] == OffState:
            if temp > self.vals["EqTemperature"]:
                #Cooling
                return 32
            elif temp < self.vals["EqTemperature"]:
                #Heating
                return 16
            else:
                #Stopped
                return 1
        else:
            #Hold temperature
            return 80
    def getMotorStatus(self):
        # Bits 0-3 are X,Y,Z stopped respectively. No Z axis so hard code this to On. 
        status = 0b00000100
        if self.vals["XTarg"] == self.vals["XPos"]:
            status |= 0b00000001
        if self.vals["YTarg"] == self.vals["YPos"]:
            status |= 0b00000010
        if self.vals["Paused"]:
            status |= 0b00100000
        return chr(status)
    def getRetTemp(self):
        temp = self.vals["Temperature"]
        # -ve temperatures are handled by shifting them into the upper 2^8 bits
        # of the 16 bit unsigned integer. The IOC then reverses this process to
        # get the display temperature.
        if temp < 0:
            temp += (2**16)
        return hex(temp)[2:]


if __name__ == "__main__":
    #CreateSimulation(THMS600_sim)
    # little test function that runs only when you run this file
    parser = OptionParser("usage: %prog")
    parser.add_option("-i", dest = "ip", help = "Start an ip port on PORT", default=9004)
    parser.add_option("-r", dest = "rpc", help = "Start an rpc port on PORT", default=9005)    
    parser.add_option("-d", dest = "debug", help = "Start a debug port on PORT", default=9006) 
    parser.add_option("-l", dest = "diag", help = "Set diagnostic level", default=0)
    options, args = parser.parse_args()

    dev = MDS600_sim()
    dev.debugLevel = options.diag
    ip = int(options.ip)
    dev.start_ip(ip)
    debug = int(options.debug)
    dev.start_debug(debug)
    while 1 :
        time.sleep(1)
