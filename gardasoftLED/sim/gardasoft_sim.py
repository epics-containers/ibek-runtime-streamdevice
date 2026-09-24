#!/bin/env python2.6

from pkg_resources import require
require("dls_serial_sim")

from dls_serial_sim import serial_device, CreateSimulation

class gardasoft(serial_device):

	OutTerminator = "\n\r>"
	InTerminator = "\r"

	ch1Output = "0"
	ch1MaxRating = "10"

	ch2Output = "0"
	ch2MaxRating = "10"

	def __init__(self):
		# place your initialisation code here
		serial_device.__init__(self)
		print "Initialising gardasoftLED simulator, V1.0"
		return

	# Functions below are the backdoor RPC API
	
	def getCh1Output(self):
		return self.ch1Output

	def getCh2Output(self):
		return self.ch2Output

	def getCh1Max(self):
		return self.ch1MaxRating

	def getCh2Max(self):
		return self.ch2MaxRating
		
	def setCh1Output(self, val):
		self.ch1Output = val
		return

	def setCh2Output(self, val):
		self.ch2Output = val
		return

	def setCh1Max(self, val):
		self.ch1MaxRating = val
		return

	def setCh2Max(self, val):
		self.ch2MaxRating = val
		return

  
	def reply(self,command):
		# Save settings
		if command == "AW":
			return "AW"

		# Reset errors
		if command == "GR":
			return "GR"

		# Set mode
		if command.startswith("RS"):
			return "RS"+command[2]+"S0"

		# Set output
		if command.startswith("RC"):
			channel=command[2]
			outStart=command.find("V")
			maxStart=command.find("E")
			if channel=="1":
				self.ch1Output=command[outStart+1:maxStart]
				self.ch1MaxRating=command[maxStart+1:len(command)]
				return "RC1C0V"+self.ch1Output+"E"+self.ch1MaxRating
			else:
				self.ch2Output=command[outStart+1:maxStart]
				self.ch2MaxRating=command[maxStart+1:len(command)]
				return "RC2C0V"+self.ch2Output+"E"+self.ch2MaxRating
		
		# Query settings
		if command == "ST":
			return "ST\n\r 01 M 00 E "+self.ch1MaxRating+ " V " +self.ch1Output+",0,0,0, \n\r 02 M 00 E "+self.ch2MaxRating+ " V " +self.ch2Output+",0,0,0, \n\r FACTORY TEST"
		return command

if __name__=="__main__":
    CreateSimulation(gardasoft)
    raw_input()
