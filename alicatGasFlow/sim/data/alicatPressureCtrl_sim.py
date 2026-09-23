#!/dls_sw/tools/bin/python2.4

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation

# create a class that represents the device
class alicatPressureCtrl(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r"
	# create an internal dict of values 
	# implement a reply function			
	def __init__(self):
		self.vals = { "Pressure":15.0, "DemandP":14.0, "Hold":1, "Pgain":65000, "Dgain":5000 } 
		self.schedule(self.inc,1.0)

	def inc(self): 
		if self.vals["Hold"] == 0:
		    self.vals["Pressure"] += (self.vals["DemandP"] - self.vals["Pressure"])/4
		    if abs(self.vals["DemandP"] - self.vals["Pressure"])<0.1: self.vals["Pressure"] = self.vals["DemandP"]

	def pressures(self):
		self.press = 'A  ' + str(self.vals["Pressure"]) + ' ' +  str(self.vals["DemandP"])
		if self.vals["Hold"] == 1:
			self.press += ' HLD'
		return  self.press

	def reply(self, command):
		command = command.lstrip('\n')
		lastcmd = command
		try:
			if command.startswith('A$$C'):
				self.vals["Hold"] = 0
				return self.pressures()
			elif command.startswith('A$$H'):
				self.vals["Hold"] = 1
				return self.pressures()
			elif command.startswith('A'):
				if (len(command)>1):
					self.vals["DemandP"] = float(command[1:])/64000.0*30.0
				return self.pressures()
			elif command.startswith('*W21='):
				self.vals["Pgain"] = float(command[5:])
				return 'A  021 = ' +  str(self.vals["Pgain"])
			elif command.startswith('*W22='):
				self.vals["Dgain"] = float(command[5:])
				return 'A  022 = ' +  str(self.vals["Dgain"])
			elif command.startswith('*R21'):
				return 'A  021 = ' +  str(self.vals["Pgain"])
			elif command.startswith('*R22'):
				return 'A  022 = ' +  str(self.vals["Dgain"])
			else:
				# error
				print 'error'
				print 'command[' + str(len(lastcmd)) + ']: ' + lastcmd
				return ''
		except:
			# error
			print 'error'
			print 'command[' + str(len(lastcmd)) + ']: ' + lastcmd
			return ''
			

if __name__ == "__main__":
	# little test function that runs only when you run this file
	dev = alicatPressureCtrl()
	dev.start_ip(9004)
	dev.start_debug(9006)
	# do a raw_input() to stop the program exiting immediately
	raw_input()
