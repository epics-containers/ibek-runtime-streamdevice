	
	#!/dls_sw/prod/tools/RHEL7-x86_64/defaults/bin/dls-python

'''
    Simulator for Chemyx Fusion Pump 4000
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

class pump(serial_device):

    status = 0

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
            print makeGreen,"Command: ", command
            #self.printFrame(command) # just if we want to print hex representation of frame

            if command.startswith('status'):
                response = str(self.status)
            elif command.startswith('start'):
                response = 'Pump started!'
                self.status = 1
            elif command.startswith('pause'):
                response = 'Pump pause!'
                self.status = 2
            elif command.startswith('stop'):
                response = 'Pump stop!'
                self.status = 0
            else:
                response = "Bad command"

            print makeBlue,"Response: ", response
            print endColour
        return response

if __name__ == "__main__":
    CreateSimulation(pump)
    while 1 :
        time.sleep(1)