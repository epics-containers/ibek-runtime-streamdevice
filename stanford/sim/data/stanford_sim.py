#!/bin/env python2.6
#
# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation

# create a class that represents the device
# This device just ecjoes the command back
class stanfordSR570(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r\n"
	# implement a reply function			
	def reply(self, command):
		lastcmd = command
		# echo the command back
		return command

##if __name__ == "__main__":
##	# little test function that runs only when you run this file
##	dev = stanfordSR570()
##	dev.start_ip(9004)
##	dev.start_debug(9006)
##	# do a raw_input() to stop the program exiting immediately
##	raw_input()

if __name__=="__main__": 
	CreateSimulation(stanfordSR570) 
	raw_input() 
