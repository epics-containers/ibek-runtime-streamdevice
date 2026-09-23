#!/dls_sw/tools/bin/python2.4

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation
import time

# create a class that represents the device
class gp307(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r\n"
	# create an internal dict of values 
	# implement a reply function			
	def __init__(self):
		self.vals = { "PressureIG1":0.0000001723,"PressureIG2":0.0000001456,"PressureCG1":0.00134,"PressureCG2":0.00329,"IG1":0,"IG2":0,"Degas":0} 
		self.chanNum = 0
		self.chanOn = [0,0,0,0,0,0]
		self.schedule(self.inc,1.0)

	def inc(self): 
		self.vals["PressureIG1"] = self.vals["PressureIG1"] - 0.0000000013 
		if self.vals["PressureIG1"]<0.0000000013: self.vals["PressureIG1"] = 0.0000001723
		self.vals["PressureIG2"] = self.vals["PressureIG2"] - 0.0000000013 
		if self.vals["PressureIG2"]<0.0000000013: self.vals["PressureIG1"] = 0.0000001456
		self.vals["PressureCG1"] = self.vals["PressureCG1"] - 0.000013 
		if self.vals["PressureCG1"]<0.000013: self.vals["PressureCG1"] = 0.00134
		self.vals["PressureCG2"] = self.vals["PressureCG2"] - 0.000013 
		if self.vals["PressureCG2"]<0.000013: self.vals["PressureCG2"] = 0.00134
		self.chanOn[self.chanNum] = 0
		self.chanNum += 1
		if self.chanNum>5: self.chanNum = 1
		self.chanOn[self.chanNum] = 1
		

	def reply(self, command):
		command = command.lstrip('\r\n')
		command = command.upper()
		lastcmd = command
		try:
			if command.startswith('DS CG1'):
				return "%2e" % (self.vals["PressureCG1"])
			elif command.startswith('DS CG2'):
				return "%2e" % (self.vals["PressureCG2"])
			elif command.startswith('DS IG1'):
				if self.vals["IG1"] == 0:
					return '9.90E+09'
				else:
					return "%2e" % (self.vals["PressureIG1"])
			elif command.startswith('DS IG2'):
				if self.vals["IG2"] == 0:
					return '9.90E+09'
				else:
					return "%2e" % (self.vals["PressureIG2"])
			elif command.startswith('IG1 ON'):
				self.vals["IG1"] = 1
				self.vals["IG2"] = 0
			elif command.startswith('IG1 OFF'):
				self.vals["IG1"] = 0
			elif command.startswith('IG2 ON'):
				self.vals["IG2"] = 1
				self.vals["IG1"] = 0
			elif command.startswith('IG2 OFF'):
				self.vals["IG2"] = 0
			elif command.startswith('DG OFF'):
				self.vals["Degas"] = 0
			elif command.startswith('DG ON'):
				if (self.vals["IG2"] == 1) or (self.vals["IG1"] == 1):
					self.vals["Degas"] = 1
			elif command.startswith('DGS'):
				return "%1d" % (self.vals["Degas"])
			elif command.startswith('PCS'):
				return "%d,%d,%d,%d,%d,%d" % (self.chanOn[0],self.chanOn[1],self.chanOn[2],self.chanOn[3],self.chanOn[4],self.chanOn[5])
			else:
				# error
				print 'error - command[' + str(len(lastcmd)) + ']: ' + lastcmd
				return 'SYNTAX ERROR'
		except:
			# error
			print 'exception - command[' + str(len(lastcmd)) + ']: ' + lastcmd
			return 'gp307_sim.py simululator exception'


# Command line
# gp307_sim.py -i <iport> -r <rport> -d<dport>
# -i <the ip port number e.g.9004>
# -r <the rpc port number> 
# -d <the debug port number e.g.9006>
# to test run simulation and use telnet 127.0.0.1 <iport>
#
if __name__ == "__main__":
	CreateSimulation(gp307)
	# do a raw_input() to stop the program exiting immediately
	while 1 :
		time.sleep(1)
	#raw_input()
