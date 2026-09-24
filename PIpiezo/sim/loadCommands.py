#!/bin/env dls-python

from pkg_resources import require
require("cothread")
from cothread.catools import *
import cothread
import time



linestring = open('waveformSetup.commands', 'r').read()
print 'Setup commands:'
print linestring
print
caput("BL16I-EA-PIEZO-01:C1:WFSETUP:WR", linestring, timeout = 5, datatype=DBR_CHAR_STR)

linestring = open('waveformStart.commands', 'r').read()
print 'Start commands:'
print linestring
print
caput("BL16I-EA-PIEZO-01:C1:WFSTART:WR", linestring, timeout = 5, datatype=DBR_CHAR_STR)

linestring = open('waveformStop.commands', 'r').read()
print 'Stop commands:'
print linestring
print
caput("BL16I-EA-PIEZO-01:C1:WFSTOP:WR", linestring, timeout = 5, datatype=DBR_CHAR_STR)


