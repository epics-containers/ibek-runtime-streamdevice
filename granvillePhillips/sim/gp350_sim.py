#!/dls_sw/tools/bin/python2.4

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation
import time

# create a class that represents the device
class gp350(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r"
	# create an internal dict of values 
	# implement a reply function			
	def __init__(self):
		self.vals = { "PressureRD1":0.0000001723,"PressureRD2":0.0000001456,"PressureRDA":0.00134,"PressureRDB":0.00329,"F1":0,"F2":0,"Degas":0} 
		self.chanNum = 0
		self.chanOn = [0,0,0,0,0,0]
		self.schedule(self.inc,1.0)

	def inc(self): 
		self.vals["PressureRD1"] = self.vals["PressureRD1"] - 0.0000000013 
		if self.vals["PressureRD1"]<0.0000000013: self.vals["PressureRD1"] = 0.0000001723
		self.vals["PressureRD2"] = self.vals["PressureRD2"] - 0.0000000013 
		if self.vals["PressureRD2"]<0.0000000013: self.vals["PressureRD1"] = 0.0000001456
		self.vals["PressureRDA"] = self.vals["PressureRDA"] - 0.000013 
		if self.vals["PressureRDA"]<0.000013: self.vals["PressureRDA"] = 0.00134
		self.vals["PressureRDB"] = self.vals["PressureRDB"] - 0.000013 
		if self.vals["PressureRDB"]<0.000013: self.vals["PressureRDB"] = 0.00134
		self.chanOn[self.chanNum] = 0
		self.chanNum += 1
		if self.chanNum>5: self.chanNum = 1
		self.chanOn[self.chanNum] = 1
		

	def reply(self, command):
		command = command.lstrip('\r\n')
		command = command.upper()
		lastcmd = command
		try:
			if command.startswith('#RDA'):
				return "* %2e" % (self.vals["PressureRDA"])
			elif command.startswith('#RDB'):
				return "* %2e" % (self.vals["PressureRDB"])
			elif command.startswith('#RD1'):
				if self.vals["F1"] == 0:
					return '* 9.90E+09'
				else:
					return "* %2e" % (self.vals["PressureRD1"])
			elif command.startswith('#RD2'):
				if self.vals["F2"] == 0:
					return '* 9.90E+09'
				else:
					return "* %2e" % (self.vals["PressureRD2"])
			elif command.startswith('#RD'):
				if self.vals["F2"] == 0 and self.vals["F1"] == 0:
					return '* 9.90E+09'
				else:
					return "* %2e" % (self.vals["PressureRD1"])
			elif command.startswith('#IGS'):
				return "* %1d%1d      " % (self.vals["F2"],self.vals["F1"])
			elif command.startswith('#F1 1'):
				self.vals["F1"] = 1
				self.vals["F2"] = 0
				return "* 1IG1 ON "
			elif command.startswith('#F1 0'):
				self.vals["F1"] = 0
				return "* 0IG1 OFF"
			elif command.startswith('#F2 1'):
				self.vals["F2"] = 1
				self.vals["F1"] = 0
				return "* 1IG2 ON "
			elif command.startswith('#F2 0'):
				self.vals["F2"] = 0
				return "* 0IG2 OFF"
			elif command.startswith('#DG 0'):
				self.vals["Degas"] = 0
				return "* 0DG OFF "
			elif command.startswith('#DG 1'):
				if (self.vals["F2"] == 1) or (self.vals["F1"] == 1):
					self.vals["Degas"] = 1
					return "* 1DG ON  "
			elif command.startswith('#DGS'):
				if self.vals["Degas"] == 1:
					return "* 1DG ON  "
				else:
				    return "* 0DG OFF "
			elif command.startswith('#PCS'):
				return "* %d%d%d%d    " % (self.chanOn[0],self.chanOn[1],self.chanOn[2],self.chanOn[3])
			else:
				# error
				print 'error - command[' + str(len(lastcmd)) + ']: ' + lastcmd
				return 'SYNTAX ERROR'
		except:
			# error
			print 'exception - command[' + str(len(lastcmd)) + ']: ' + lastcmd
			return 'gp350_sim.py simululator exception'


# Command line
# gp350_sim.py -i <iport> -r <rport> -d<dport>
# -i <the ip port number e.g.9004>
# -r <the rpc port number> 
# -d <the debug port number e.g.9006>
# to test run simulation and use telnet 127.0.0.1 <iport>
#
if __name__ == "__main__":
	CreateSimulation(gp350)
	# do a raw_input() to stop the program exiting immediately
	while 1 :
		time.sleep(1)
	#raw_input()
