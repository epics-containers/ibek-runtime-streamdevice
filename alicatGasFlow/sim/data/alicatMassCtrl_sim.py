#!/bin/env dls-python

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
require("rpyc")
from dls_serial_sim import serial_device, CreateSimulation
import time

from random import random, uniform

# create a class that represents the device
class alicatMassCtrl(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r"
	gasTypeStr = [ "Air","Ar","CH4","CO","CO2","C2H2","H2","He","N2","N2O","Ne","O2","C3H8","n-C4H10","C2H2","C2H4","i-C2H10","Kr","Xe","SF6","C-25","C-10","C-8","C-2","C-75","A-75","A-25","A1025","Star29","P-5"]

	# create an internal dict of values 
	def __init__(self):
		self.vals = { "AbsP":16.0, "Temp":21.0,"VFlow":15.0, "MFlow":15.0, "DemandMFlow":2.0, "Gas":7, "Pgain":65000, "Dgain":5000, "R20":9239 } 
		self.schedule(self.inc,1.0)

	def inc(self): 
		self.vals["MFlow"] += (self.vals["DemandMFlow"] - self.vals["MFlow"])/4
		if abs(self.vals["DemandMFlow"] - self.vals["MFlow"])<0.1: self.vals["MFlow"] = self.vals["DemandMFlow"]
		self.vals["AbsP"] = round(uniform(15,17),2)
		self.vals["Temp"] = round(uniform(19,21),2)
		self.vals["VFlow"] = round(uniform(14,16),2)

	def flowdata(self):
		self.press = 'A  ' + str(self.vals["AbsP"]) + ' ' + str(self.vals["Temp"]) + ' ' + str(self.vals["VFlow"]) + ' ' +str(round(self.vals["MFlow"],2)) + ' ' +  str(self.vals["DemandMFlow"] )
		self.press += ' ' + self.gasTypeStr[ self.vals["Gas"] ]
		return  self.press

	# implement a reply function
	def reply(self, command):
		# print 'command[' + str(len(command)) + ']: ' + command
		command = command.lstrip('\n')
		lastcmd = command
		try:
			if command.startswith('A$$'):
				newgas = int(command[3:])
				if (newgas >= 0 and newgas <30):
					self.vals["Gas"] = newgas
				return self.flowdata()
			elif command.startswith('A'):
				if (len(command)>1):
					self.vals["DemandMFlow"] = float(command[1:])/64000.0*100.0
				return self.flowdata()
			elif command.startswith('*W21='):
				self.vals["Pgain"] = float(command[5:])
				return 'A  021 = ' +  str(self.vals["Pgain"])
			elif command.startswith('*W22='):
				self.vals["Dgain"] = float(command[5:])
				return 'A  022 = ' +  str(self.vals["Dgain"])
			elif command.startswith('*W20='):
				self.vals["R20"] = float(command[5:])
				return 'A  020 = ' +  str(self.vals["R20"])
			elif command.startswith('*R21'):
				return 'A  021 = ' +  str(self.vals["Pgain"])
			elif command.startswith('*R22'):
				return 'A  022 = ' +  str(self.vals["Dgain"])
			elif command.startswith('*R20'):
				return 'A  020 = ' +  str(self.vals["R20"])
			else:
				# error
				print 'error'
				print 'command[' + str(len(lastcmd)) + ']: ' + lastcmd
				return ''
		except:
			# error
			print 'exception error'
			print 'command[' + str(len(lastcmd)) + ']: ' + lastcmd
			return ''
			
# Command line
# alicatMassCtrl_sim.py -i <port> -r <port> -d<port>
# -i <the ip port number e.g.9004>
# -r <the rpc port number> 
# -d <the debug port number e.g.9006>
#
if __name__ == "__main__":
	CreateSimulation(alicatMassCtrl)
	while 1 :
		time.sleep(1)
	#raw_input()

