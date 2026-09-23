#! /dls_sw/tools/bin/python2.4 

from pkg_resources import require 
require("dls_serial_sim") 
from dls_serial_sim import serial_device 

import string
import sys

"""

Format	@         00       ##      *     ##    '*' CR
	header | unit | command | text | FCS | terminator

	e.g. @00RD00000001xx*\r = Data memory read of 1 word from address 0000, unit 0

"""

MP = 1
GB = 2
ID = 3
V4 = 4
V6 = 6
TP = 7

class hostlink(serial_device):

	Terminator = "\r"
	
	def __init__(self, ptype = 0):
	
		serial_device.__init__(self, protocolBranches=["MP", "GB", "V4", "V6", "TP", "ID"])
		print "HostLink cmode simulator"
		
		self.type = ptype
		
	# memory map dictionaries
	
		self.DM = {}
		self.AR = {}
		self.IO = {}
		
	# set data memory address 0000
	
		self.DM["0000"] = 1
		
		return
		
	def reply(self, command):
	
#		print "command = " + command
		command =  string.strip(command)

		print "Type", self.type
		
		n = len(command)
		
	# parse the command string
	
		unit = command[1:3]
		comm = command[3:5]

	# PLCs are set to unit 00 so ignore messages not intended for us
	
		if unit != "00":
			return None
			
	# check header - format error
	
		if command[0:1] != "@":
			resp = "@00%s14" % comm
			cs = self.checksum(resp)
			return "%s%02X*\r" % (resp, cs)
			
	# checksum error - checksum error
	
		if command[n-3:n-1] != "%02X" % self.checksum(command[:-3]):
			resp = "@00%s13" % comm
			cs = self.checksum(resp)
			return "%s%02X*\r" % (resp, cs)
				
	# DM, IO, AR, Counter/Timer Read #######################################
		
		if (comm == "RD") or (comm == "RR") or (comm == "RC") or (comm == "RJ"):
					
			addr = command[5:9]
			size = command[9:13]

			if self.DM.has_key("0000"):
				mem = self.DM["0000"]
			else:
				mem = 0
			
			resp = "@00%s00%s" % (comm, mem * size)
			cs = self.checksum(resp)
			return "%s%02X*\r" % (resp, cs)
	
	# DM Write #############################################################
	
		if comm == "WD":

			addr = command[5:9]
			
			resp = "@00WD00"
			cs = self.checksum(resp)
			return "%s%02X*\r" % (resp, cs)

	# FINS over cmode ######################################################
	
		if comm == "FA":
		
			sub = command[14:18]
			
		# CPU UNIT STATUS READ
		
			if sub == "0601":
				return "@00FA004000000006010000050200000000000000002020202020202020202020202020202043*\r"
		
		# CPU UNIT DATA READ
		
			if sub == "0502":
				return "@00FA0040000000050200008100434A314D5F4350553132202020202020202020203F*\r"
				
		# CYCLE TIME READ
		
			if (sub == "0620") and (command[18:20] == "01"):
				return "@00FA00400000000620000000000014000000210000001242*\r"

			if (sub == "0620") and (command[18:20] == "00"):
				resp = "@00FA004000000006209999"
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)
				
		# CLOCK READ
		
			if sub == "0701":
				resp = "@00FA00400000000701000001020304050607";
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)

		# MULTIPLE MEMORY AREA READ
		
			if (sub == "0104") and (command[20:26] == "015000"):
				resp = "@00FA004000000001040000999901990203990405";
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)
				
			if (sub == "0104") and (command[20:26] == "020200"):
				resp = "@00FA004000000001040000990001990002990003990004";
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)

		# MEMORY AREA WRITE
		
			if sub == "0102":
				resp = "@00FA004000000001029999"
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)
			
		# MEMORY AREA READ
		
			if sub == "0101":
				addr = command[20:24]
				size = command[26:30]
				
				resp = "@00FA004000000001019999%s" % ("0001" * size)
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)

		# STOP

			if sub == "0402":
				resp = "@00FA004000000004029999"
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)
				
		# RUN / MONITOR
		
			if (sub == "0401") and (command[22:24] == "04"):
				resp = "@00FA004000000004019999"
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)
				
			if (sub == "0401") and (command[22:24] == "02"):
				resp = "@00FA004000000004019999"
				cs = self.checksum(resp)
				return "%s%02X*\r" % (resp, cs)

		print "Unknown", sub, command
		return None

	def checksum(self, command):
	
		cs = ord(command[0])
		n = len(command)
		
		for i in range(1, n): cs ^= ord(command[i])
		
		return cs
		
if __name__ == "__main__":
	dev = hostlink()
        if len(sys.argv) > 1:
            print "Starting host link on port %s" % int(sys.argv[1])
            dev.start_ip(int(sys.argv[1]))
        else:
            print "Starting host link on port 12345"
	    dev.start_ip(12345)
#	dev.start_serial()
	raw_input()

"""

	if self.simulationDevicePresent("PLC")
"""
