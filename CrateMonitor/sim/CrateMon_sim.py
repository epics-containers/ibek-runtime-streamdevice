#! /dls_sw/tools/bin/python2.4

from pkg_resources import require 
require("dls_serial_sim") 
from dls_serial_sim import serial_device 

import string

class CrateMonitor_sim(serial_device):

	Terminator = "\r"
	
	def __init__(self):
	
		serial_device.__init__(self)
		print "serial_sim"
		return
		
	def reply(self, command):
	
#		print "command = " + command
		command =  string.strip(command)
		
		if command == "S,7F":
#			print "System",
			s = "s,FF,"
			cs = self.checksum(s)
#			print "checksum 0x%X" % cs
			return "%s%X" % (s, cs)
			
		if command == "R,7E":
#			print "Reset",
			s = "r,"
			cs = self.checksum(s)
#			print "checksum 0x%X" % cs
			return "%s%X" % (s, cs)
			
		if command == "X,74":
#			print "Shutdown",
			s = "x,"
			cs = self.checksum(s)
#			print "checksum 0x%X" % cs
			return "%s%X" % (s, cs)
			
		if command == "Y,75":
#			print "Fans",
			s = "y,1,2,3,4,5,6,7,8,"
			cs = self.checksum(s)
#			print "checksum 0x%X" % cs
			return "%s%X" % (s, cs)

		if command == "V,7A":
#			print "Supply",
			s = "v,1388,CE4,2EE0,2EE0,"
			cs = self.checksum(s)
#			print "checksum 0x%X" % cs
			return "%s%X" % (s, cs)

		if command == "T,78":
#			print "Temps",
			s = "t,1,2,3,"
			cs = self.checksum(s)
#			print "checksum 0x%X" % cs
			return "%s%X" % (s, cs)

#		print "Unknown", command
		return None

	def checksum(self, command):
	
		cs = ord(command[0])
		n = len(command)
		
		for i in range(1, n): cs ^= ord(command[i])
		
		return cs
			
if __name__ == "__main__":
	dev = CrateMonitor_sim()
	dev.start_ip(12345)
	raw_input()
