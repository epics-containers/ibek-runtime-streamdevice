#!/bin/env dls-python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

################################################
# Test suite for the gardasoft LED controller
    
class GardasoftTestSuite(TestSuite):

	def createTests(self):
		# Define the targets for this test suite
		Target("simulation", self, simulationCmds=['data/gardasoft_sim.py -i 8001 -r 9016 -d 9001'],
			iocDirectory="iocs/example_sim",
			iocBootCmd="bin/linux-x86_64/stexample.sh",
			runIocInScreenUnderHudson=True,
			epicsDbFiles="db/example_expanded.db",
			simDevices=[SimDevice("gardasoftSim",9016,rpc=True)],
			guiCmds=['edm -m "P=TEST-LED-01,N=1" -eolc -x data/gardasoft.edl'])
		Target("hardware", self,
			iocDirectory="iocs/example",
			iocBootCmd="bin/linux-x86_64/stexample.sh",
			epicsDbFiles="db/example_expanded.db",
			simDevices=[SimDevice("gardasoftSim",9016,rpc=True)],
			guiCmds=['edm -m "P=TEST-LED-01,N=1" -eolc -x data/gardasoft.edl'])
			


        # The tests
		CaseSetOutput(self)
		CaseSetMaxRating(self)
		CaseSwitchOnAndOff(self)
                
################################################
# Intermediate test case class that provides some utility functions
# for this suite

class GardasoftCase(TestCase):

	pvPrefix="TEST-LED-01:"
	
	def verifyCh1Output(self, intended):
		self.verifyPv(self.pvPrefix+"CH1CURRENT",intended)
		self.verify(float(self.simulation("gardasoftSim").getCh1Output()),intended)
		
	def verifyCh2Output(self, intended):
		self.verifyPv(self.pvPrefix+"CH2CURRENT",intended)
		self.verify(float(self.simulation("gardasoftSim").getCh2Output()),intended)
			
	def verifyCh1Max(self, intended):
		self.verifyPv(self.pvPrefix+"CH1MAXCURRENT",intended)
		self.verify(float(self.simulation("gardasoftSim").getCh1Max()),intended)

	def verifyCh2Max(self, intended):
		self.verifyPv(self.pvPrefix+"CH2MAXCURRENT",intended)
		self.verify(float(self.simulation("gardasoftSim").getCh2Max()),intended)
		         
################################################
# Test cases

class CaseSetOutput(GardasoftCase):
	def runTest(self):
		# Test setup: ensure max current set appropriately and switch output on
		self.putPv(self.pvPrefix+"CH1SETMAXCURRENT",20)
		self.putPv(self.pvPrefix+"CH1ON",1)
		
		# Set desired output to some different values
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",5)
		self.verifyCh1Output(5)
		self.sleep(1)
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",12.45)
		self.verifyCh1Output(12.45)
		self.sleep(1)
		
		
class CaseSetMaxRating(GardasoftCase):
	def runTest(self):
		# Test setup: switch output on
		self.putPv(self.pvPrefix+"CH1ON",1)
		
		# Set max rating to 20mA
		self.putPv(self.pvPrefix+"CH1SETMAXCURRENT",20)
		self.verifyCh1Max(20)
		
		# Set output to some valid values
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",5)
		self.verifyCh1Output(5)
		self.sleep(1)
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",20)
		self.verifyCh1Output(20)
		
		# Try to exceed the max and verify output is capped to 20mA
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",100)
		self.verifyCh1Output(20)
		self.sleep(1)
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",20.1)
		self.verifyCh1Output(20)
		self.sleep(1)
		
		# Check can still set a valid value
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",10)
		self.verifyCh1Output(10)
		
		
		
class CaseSwitchOnAndOff(GardasoftCase):
	def runTest(self):
		# Test setup: set a starting output value
		self.putPv(self.pvPrefix+"CH1SETMAXCURRENT",20)
		self.putPv(self.pvPrefix+"CH1SETOUTPUT",10)
		self.putPv(self.pvPrefix+"CH1ON",1)
		self.sleep(1)
		
		# Switch the unit off and verify output goes to zero
		self.putPv(self.pvPrefix+"CH1ON",0)
		self.verifyCh1Output(0)
		self.sleep(1)
						
		# Switch back on and check output goes back to previous value
		self.putPv(self.pvPrefix+"CH1ON",1)
		self.verifyCh1Max(20)
		self.verifyCh1Output(10)


################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    GardasoftTestSuite()

    
