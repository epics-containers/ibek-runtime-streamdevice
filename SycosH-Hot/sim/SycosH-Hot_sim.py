#!/bin/env dls-python

from pkg_resources import require
require("dls_serial_sim")

from dls_serial_sim import serial_device

class SycosH-Hot(serial_device):

    Terminator = "\n"

    def __init__(self):
        # place your initialisation code here
        serial_device.__init__(self)

    def reply(self,command):
        # reply to commands here
        return command

if __name__=="__main__":
    # run our simulation on the command line. Run this file with -h for help
    CreateSimulation(SycosH-Hot)
    raw_input()
