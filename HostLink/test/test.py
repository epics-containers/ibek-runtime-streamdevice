#! /dls_sw/tools/bin/python2.4

from pkg_resources import require
require("dls.autotestframework==1.13")
from dls.autotestframework import *

MP = 1
GB = 2
ID = 3
V4 = 4
V6 = 6
TP = 7

class HostlinkTest(TestSuite):

	def createTests(self):
	
		Target("simulation", self,
		iocDirectory=".",
		iocBootCmd="screen -D -m -L iocs/example_sim/bin/linux-x86/stexample.sh",
		epicsDbFiles="iocs/example_sim/db/HostLink.template",
		simDevices=[SimDevice("HostLink", 8002, rpc=True)])
		
	# tests
	
		HostLinkTest(self)
		
################################################################################

class HostLinkBase(TestCase):

	def Nothing():
		pass
		
class HostLinkTest(HostLinkBase):

	def runTest(self):
	
		sim = self.simulation("HostLink")

		sim.type = MP
		sim.DM["0000"] = 42
		
		self.putPv("TS-HOSTLINK-01:UPDATE", 1)

#		self.diagnostic("DM[\"0000\"] = %d" % sim.DM["0000"])
			
if __name__ == "__main__":

	HostlinkTest()
	
