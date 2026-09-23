#!/bin/env dls-python2.6

import re
from datetime import timedelta
from pkg_resources import require
require("dls_serial_sim")

from dls_serial_sim import serial_device, CreateSimulation


def check_type(value, dtype):
    try:
        return dtype(value)
    except ValueError:
        return False

class harvardSyringe(serial_device):

    OutTerminator = "\x11"
    Terminator = "\r\n"

    def __init__(self):
        self.pump_state = ":"
        self.properties = {
            "force": {
                "values": [20],
                "types": [int],
                "get format": "\n{values[0]}%\r\n{pump}",
                "test": lambda val: val if 1 <= val[0] <= 100 else False,
                "error format": "Argument error: %s\n   Out of range"},
            "poll": {
                "values": ["OFF"],
                "types": [str],
                "get format": "Polling mode is {values[0]}\r\n{pump}",
                "test": lambda val:
                    val if val[0].upper() in ("ON", "OFF") else False,
                "error format": ""},
            "diameter": {
                "values": [10.0],
                "types": [float],
                "get format": "\n{values[0]:.4f} mm\r\n{pump}",
                "test": lambda val:
                    val if 0.1 <= round(val[0], 4) <= 99 else False,
                "error format": "Argument error: %s\n   Diameter out of range"},
            "irun": {
                "new pump state": ">"},
            "wrun": {
                "new pump state": "<"},
            "stop": {
                "new pump state": ":"},
            "stp": {
                "new pump state": ":"},
            "irate": {
                "values": [0.0, "ul/min"],
                "types": [float, str],
                "get format":
                    "\n{values[0]:.4f} {values[1]}\r\n{pump}",
                "test": lambda val:
                    (val if 0.0 <= round(val[0], 4) <= 10000000 and
                     re.search("^[pnum]l/sec|min|hr", val[1],
                               re.IGNORECASE) else False),
                "error format": "Argument error: {0[0]} {0[1]} {pump}"},
            "wrate": {
                "values": [0.0, "ul/min"],
                "types": [float, str],
                "get format":
                    "\n{values[0]:.4f} {values[1]}\r\n{pump}",
                "test": lambda val:
                    (val if 0.0 <= round(val[0], 4) <= 10000000 and
                     re.search("^[pnum]l/sec|min|hr", val[1],
                               re.IGNORECASE) else False),
                "error format": "Argument error: {0[0]} {0[1]} {pump}"},
            "tvolume": {
                "values": [0.0, "nl"],
                "types": [float, str],
                "get format": "\n{values[0]} {values[1]}\r\n{pump}",
                "test": self.tvolume_test,
                "error format": "Argument error: {0[0]} {0[1]} {pump}"},
            "ivolume": {
                "values": [0.0, "nl"],
                "types": [float, str],
                "get format": "\n{values[0]} {values[1]}\r\n{pump}"},
            "wvolume": {
                "values": [0.0, "nl"],
                "types": [float, str],
                "get format": "\n{values[0]} {values[1]}\r\n{pump}"},
            "ttime": {
                "values": ["0 seconds"],
                "types": [str, str],
                "get format": "\n{values[0]}\r\n{pump}",
                "test": self.ttime_test}
            }
        serial_device.__init__(self)

    def tvolume_test(self, vals):
        units = re.search("^[pnum]l", vals[1])
        if 0.0 <= round(vals[0], 4) <= 100 and units:
            return [round(vals[0], 4), units.group(0)]
        elif units:
            return [0, units.group(0)]
        else:
            return False

    def ttime_test(self, vals):
        print vals
        if len(vals) > 1:
            try:
                float(vals[0])
            except ValueError:
                return False
            if vals[1][:3].lower() == "sec":
                if vals[0] < 60:
                    return ["%s seconds" % vals[0]]
                else:
                    return [str(timedelta(seconds=int(vals[0])))]
            else:
                return False
        else:
            hours, mins, secs = vals[0].split(":")
            full_time = timedelta(hours=int(hours),
                                  minutes=int(mins),
                                  seconds=int(secs))
            return [str(full_time)]

    def reply(self, command):
        print "command", command
        split = command.strip().split(" ")
        try:
            prop = self.properties[split[0]]
        except KeyError:
            return("No property %s" % split[0])
        if prop.has_key("values"):
            if len(split) == 1:
                print prop["get format"].format(pump=self.pump_state, **prop)
                return prop["get format"].format(pump=self.pump_state, **prop)
            else:
                try:
                    # Check arguments have the correct type
                    new_vals = [val_type(val) for val, val_type in zip(
                            split[1:], prop["types"])]
                except ValueError:
                    print "Wrong Type"
                    print prop["error format"].format(split[1:],
                                                      pump=self.pump_state)
                    return prop["error format"].format(split[1:],
                                                       pump=self.pump_state)
                checked_vals = prop["test"](new_vals)
                if checked_vals != False:
                    prop["values"] = checked_vals
                    print "\n:"
                    return "\n:"
                else:
                    print checked_vals
                    print prop["error format"].format(split[1:],
                                                      pump=self.pump_state)
                    return prop["error format"].format(split[1:],
                                                       pump=self.pump_state)
        else:
            self.pump_state = prop["new pump state"]
            print "\n" + self.pump_state
            return "\n" + self.pump_state

if __name__=="__main__":
    # run our simulation on the command line. Run this file with -h for help
    CreateSimulation(harvardSyringe)
    raw_input()
