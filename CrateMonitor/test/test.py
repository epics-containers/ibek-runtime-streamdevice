#! /dls_sw/tools/bin/python2.4

from pkg_resources import require
require("dls.autotestframework")
from dls.autotestframework import *

class CrateMonitorTest(TestSuite):

	def createTests(self):
	
		Target("simulation", self,
			iocDirectory=".",
			iocBootCmd="screen -D -m -L iocs/example_sim/bin/linux-x86/stexample.sh",
			epicsDbFiles="iocs/example_sim/db/CrateMon.db",
			environment=[('EPICS_CA_REPEATER_PORT','6065'),('EPICS_CA_SERVER_PORT','6064')])
	# tests
	
		CommsTest(self)
		
################################################################################

class CrateMonitorBase(TestCase):

	def Nothing():
		pass
	
class CommsTest(CrateMonitorBase):

	def runTest(self):
		"""Tests basic protocol"""

		self.putPv("TS-TS-CMON-01:ENABLE", 1)
		self.putPv("TS-TS-CMON-01:SHUTDOWN", 1)
		
		self.putPv("TS-TS-CMON-01:ENABLE", 1)
		self.putPv("TS-TS-CMON-01:RESET", 1)

		self.verifyPv("TS-TS-CMON-01:STATUS", 255)
	# fans
		self.verifyPvInRange("TS-TS-CMON-01:FAN1", 0.9, 1.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN2", 1.9, 2.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN3", 2.9, 3.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN4", 3.9, 4.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN5", 4.9, 5.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN6", 5.9, 6.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN7", 6.9, 7.1)
		self.verifyPvInRange("TS-TS-CMON-01:FAN8", 7.9, 8.1)
	# psu
		self.verifyPvInRange("TS-TS-CMON-01:P33VSUPPLY", 3.2, 3.4)
		self.verifyPvInRange("TS-TS-CMON-01:P50VSUPPLY", 4.9, 5.1)
		self.verifyPvInRange("TS-TS-CMON-01:P12VSUPPLY", +11.9, +12.1)
		self.verifyPvInRange("TS-TS-CMON-01:M12VSUPPLY", -12.1, -11.9)
	# temps
		self.verifyPvInRange("TS-TS-CMON-01:INLET",    0.9, 1.1)
		self.verifyPvInRange("TS-TS-CMON-01:INTERNAL", 1.9, 2.1)
		self.verifyPvInRange("TS-TS-CMON-01:OUTLET",   2.9, 3.1)

################################################################################

if __name__ == "__main__":

	CrateMonitorTest()
