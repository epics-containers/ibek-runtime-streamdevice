#!/dls_sw/tools/bin/python2.4

# require a fixed version of serial_sim to be imported
from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation
import time

# create a class that represents the device
class viciE2CA(serial_device):
	# set the terminator to control when a string is passed to reply
	Terminator = "\r"
	# create an internal dict of values 
	# implement a reply function			
	def __init__(self):
		self.vals = { "Position":'A', "Count":1 } 

	def reply(self, command):
		command = command.lstrip('\n')
		command = command.upper()
		lastcmd = command
		try:
			if command.startswith('CW'):
				self.vals["Position"] = 'A'
				self.vals["Count"] +=1
				return ''
			elif command.startswith('CC'):
				self.vals["Position"] = 'B'
				self.vals["Count"] +=1
				return ''
			elif command.startswith('GOA'):
				self.vals["Position"] = 'A'
				self.vals["Count"] +=1
				return ''
			elif command.startswith('GOB'):
				self.vals["Position"] = 'B'
				self.vals["Count"] +=1
				return ''
			elif command.startswith('CP'):
				return 'Position is ' + self.vals["Position"]			
			elif command.startswith('CNT'):
				return 'CNT = ' + str(self.vals["Count"]) 
			elif command.startswith('VR'):
				return 'I-PD-EDF56RC.7\r08/19/2010'
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
			

# Command line
# viciE2CA_sim.py -i <port> -r <port> -d<port>
# -i <the ip port number e.g.9004>
# -r <the rpc port number> 
# -d <the debug port number e.g.9006>
#
if __name__ == "__main__":
	CreateSimulation(viciE2CA)
	# do a raw_input() to stop the program exiting immediately
	while 1 :
		time.sleep(1)
	#raw_input()
