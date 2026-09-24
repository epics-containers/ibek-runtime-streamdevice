#!/dls_sw/tools/bin/python2.4

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation
import time

# create a class that represents the device
class mks647C(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r\n"
	# create an internal dict of values 
	# implement a reply function			
	def __init__(self):
		self.vals = { "GasMenu":'1', "Flow":0, "statusBits":16, "Range":0 } 
		self.chanOn = [0,0,0,0,0,0,0,0]
		self.schedule(self.inc,1.0)

	def inc(self): 
		self.vals["Flow"] += 10
		if self.vals["Flow"] > 1100:
			self.vals["Flow"] = 0
		if self.vals["statusBits"] == 0:
			self.vals["statusBits"] = 16
		else:
			self.vals["statusBits"] *= 2
			if self.vals["statusBits"] > 512:
				self.vals["statusBits"] = 0
		self.vals["Range"] += 1
		if self.vals["Range"] > 39:
			self.vals["Range"] = 0

	def reply(self, command):
		command = command.lstrip('\r\n')
		command = command.upper()
		lastcmd = command
		try:
			if command.startswith('GM R'):
				return self.vals["GasMenu"]
			elif command.startswith('GM'):
				gm = int(command.lstrip('GM'))
				if gm >=0 and gm <= 5: 
					self.vals["GasMenu"] = int(command.lstrip('GM'))
					return ''
				else:
					return 'E4'
			elif command.startswith('ON'):
				chanNum = int(command.lstrip('ON')) 
				if chanNum >=0 and chanNum <= 8: 
					if chanNum == 0:
						self.chanOn = [1,1,1,1,1,1,1,1]
					else:
						self.chanOn[chanNum-1] = 1
					return ''
				else:
					return 'E4'				
			elif command.startswith('OF'):
				chanNum=int(command.lstrip('OF'))
				if chanNum >=0 and chanNum <= 8: 
					if chanNum == 0:
						self.chanOn = [0,0,0,0,0,0,0,0]
					else:
						self.chanOn[chanNum-1] = 0
					return ''
				else:
					return 'E4'				
			elif command.startswith('ST'):
				chanNum=int(command.lstrip('ST'))
				if chanNum >=1 and chanNum <= 8: 
					return "%05d" % (self.chanOn[chanNum-1]+self.vals["statusBits"])
				else:
					return 'E4'				
			elif command.startswith('FL'):
				chanNum=int(command.lstrip('FL'))
				if chanNum >=1 and chanNum <= 8: 
					return "%05d" % (self.vals["Flow"])
				else:
					return 'E4'				
			elif command.startswith('RA') and command.endswith('R'):
				chanNum=int(command.lstrip('RA').rstrip('R'))
				if chanNum >=1 and chanNum <= 8: 
					return "%02d" % (self.vals["Range"])
				else:
					return 'E4'				
			elif command.startswith('GC') and command.endswith('R'):
				chanNum=int(command.lstrip('GC').rstrip('R'))
				if chanNum >=1 and chanNum <= 8: 
					return '00050'
				else:
					return 'E4'				
			else:
				# error
				print 'error - command[' + str(len(lastcmd)) + ']: ' + lastcmd
				return 'E1'
		except:
			# error
			print 'exception - command[' + str(len(lastcmd)) + ']: ' + lastcmd
			return 'E1'
			

# Command line
# mks647C_sim.py -i <iport> -r <rport> -d<dport>
# -i <the ip port number e.g.9004>
# -r <the rpc port number> 
# -d <the debug port number e.g.9006>
# to test run simulation and use telnet 127.0.0.1 <iport>
#
if __name__ == "__main__":
	CreateSimulation(mks647C)
	# do a raw_input() to stop the program exiting immediately
	while 1 :
		time.sleep(1)
	#raw_input()
