#!/bin/env python2.6

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation

# create a class that represents the device
class OxInstCryojet(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r"
	# create an internal dict of values 
	# implement a reply function			
	def __init__(self):
		self.vals = { "R0":80, "R1":77, "R4":3, "R5":50, "R6":10, "R8":55, "R9":44, "R10":33, "R11":100, "R18":21, "R19":31} 
		self.cx = "C1"
		self.ax = "A0"
		self.schedule(self.inc,1.0)

	def inc(self): 
		self.vals["R1"] += (self.vals["R0"] - self.vals["R1"])/4
		if abs(self.vals["R0"] - self.vals["R1"])<1: self.vals["R1"] = self.vals["R0"]
		self.vals["R4"] = (self.vals["R0"] - self.vals["R1"])

	def reply(self, command):
		lastcmd = command
		try:
			if command.startswith('A'):
				self.ax = command
				return command
			elif command.startswith('X'):
				return ('X0' + self.ax + self.cx)
			elif command.startswith('C'):
				self.cx = command
				return command
			elif command.startswith('D'):
				self.vals["R10"] = float(command[1:])
				return command[0]
			elif command.startswith('I'):
				self.vals["R9"] = float(command[1:])
				return command[0]
			elif command.startswith('J'):
				self.vals["R18"] = float(command[1:])
				return command[0]
			elif command.startswith('K'):
				self.vals["R19"] = float(command[1:])
				return command[0]
			elif command.startswith('M'):
				return command[0]
			elif command.startswith('O'):
				return command[0]
			elif command.startswith('P'):
				self.vals["R8"] = float(command[1:])
				return command[0]
			elif command.startswith('T'):
				self.vals["R0"] = float(command[1:])
				return command[0]
			elif command.startswith('R'):
				return 'R' + str(self.vals[command]) 
			else:
				# error
				print 'error'
				return '?' + command
		except:
			# error
			print 'error'
			return '?' + command

	def command(self, text):
		'''Interface function for commands from the test suite.'''
        #print text
		args = text.split()
		if args[0] == "getcurrtemp":
			self.response("currtemp %f" % self.vals["R1"])
		else:
			serial_device.command(self, text)
			

##if __name__ == "__main__":
##	# little test function that runs only when you run this file
##	dev = OxInstCryojet()
##	dev.start_ip(9004)
##	dev.start_debug(9006)
##	# do a raw_input() to stop the program exiting immediately
##	raw_input()

if __name__=="__main__": 
	CreateSimulation(OxInstCryojet) 
	raw_input() 
	
