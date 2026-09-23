	
	#!/dls_sw/prod/tools/RHEL7-x86_64/defaults/bin/dls-python

'''
    Simulator for thermo cube
    2021 - Mateusz Hoppe
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
import re, string

class thermocube(serial_device):

    #Terminator = '\x00'

    def __init__(self, name=" ", ui=None, tcpPort=9001):
        self.name = name
        self.tcpPort = tcpPort
        serial_device.__init__(self, ui=ui)
        self.start_ip(tcpPort)
        self.addressed = False

    def printFrame(self,frame):
        f = bytearray(frame)
        print (", ".join("\\x%02X" % v for v in f))

    def reply(self, command):
        response = None

        if command: # if command is not empty
            makeBlue = "\033[94m"
            makeGreen = "\033[32m"
            endColour = "\033[0m"

            print datetime.datetime.utcnow()
            print makeGreen,"Command: "
            self.printFrame(command) 

            if command == '\xC1':
                response = '\x64\x00'
            elif command == '\xC9':
                response = '\x58\x02'
            elif command.startswith('anotherCommand'):
                response = 'anotherResponse'
            else:
                response = ""
            
            print makeBlue,"Response: "
            self.printFrame(response) 
            print endColour

        return response

if __name__ == "__main__":
    CreateSimulation(thermocube)
    while 1 :
        time.sleep(1)