#!/dls_sw/prod/tools/RHEL6-x86_64/Python/2-7-3/prefix/bin/python2.7

from pkg_resources import require

require("dls_serial_sim==1.17")

from dls_serial_sim import serial_device
import time

NOT_DEFINED = "Command error CMD_NOT_DEFINED"
INVALID_ARG = "Command error CMD_ARG_INVALID"

HELP = """
Commands:                                                                                                                   
                                                                                                                            
id?     - Identification Query                                                                                              
?       - Commands Query                                                                                                    
channel - Set Current Channel                                                                                               
channel?        - Get Current Channel                                                                                       
target  - Set Target Temperature (C)                                                                                        
target? - Get Target Temperature (C)
temp?   - Get Actual Temperature (C)
current - Set Current (mA)
current?        - Get Current (mA)
power?  - Get Power (mW)
enable  - Set Channel Enable (1: Enable, 0:Disabled)
enable? - Get Channel Enable (1: Enable, 0:Disabled)
system  - Set System Enable (1: Enable, 0:Disabled)
system? - Get System Enable (1: Enable, 0:Disabled)
specs?  - Show Laser Diode Specifications
step    - Set Arrow Key Step Size (.01->10)
step?   - Get Arrow Key Step Size
save    - Save Parameters
statword?       - Get Status
Arrow Keys      - up, down, left, right
"""


class Temperature:
    def __init__(self, target, actual, maximum, minimum):
        self.target = target
        self.actual = actual
        self.maximum = maximum
        self.minimum = minimum


class PowerSystem:
    def __init__(self, power, current, max_power=None, max_current=None):
        if not max_power:
            max_power = power
        if not max_current:
            max_current = current
        self.power = power
        self.current = current
        self.max_power = max_power
        self.max_current = max_current


class Channel:
    def __init__(self, serial_number, enabled, wavelength, power_system, temperature):
        self.serial_number = serial_number
        self.is_enabled = enabled
        self.wavelength = wavelength
        self.power_system = power_system
        self.temperature = temperature

    def specs(self):
        return """
        Wavelength = %s
        POut = %s
        IOp = %s
        IMon = 0.0
        ITh = 20.0
        SerialNumber = %s
        """ % (self.wavelength, self.power_system.max_power,
               self.power_system.max_current, self.serial_number)


def make_default_channels():
    return [
        Channel(
            serial_number="110721-59",
            enabled=0, wavelength=406,
            power_system=PowerSystem(7.36, 49),
            temperature=Temperature(20, 23.2, 30, 20)),
        Channel(
            serial_number="110723-57",
            enabled=0, wavelength=638,
            power_system=PowerSystem(14.72, 82.7),
            temperature=Temperature(20, 23.2, 30, 20)),
        Channel(
            serial_number="110308-62",
            enabled=0, wavelength=642,
            power_system=PowerSystem(21.04, 104.3),
            temperature=Temperature(20, 23.2, 30, 20)),
        Channel(
            serial_number="110831-55",
            enabled=0, wavelength=808,
            power_system=PowerSystem(20.41, 100.7),
            temperature=Temperature(20, 23.2, 30, 20))
    ]


class ThorlabsMcls1Simulation(serial_device):
    Terminator = "\r"

    def __init__(self, model="THORLABS MCLS", firmware="1.06", channel=1):
        self.id = "%s vers %s" % (model, firmware)
        self.channels = make_default_channels()
        self.channel = channel - 1
        self.system_enabled = 0

    def reply(self, command):
        return self.__reply(command)

    def __reply(self, command):
        try:
            if command == "?":
                return HELP
            elif command.endswith("?"):
                return self.__get(command[:-1])
            elif "=" in command:
                parts = command.split("=")
                return self.__set(parts[0], parts[1])
            else:
                raise KeyError
        except KeyError:
            return NOT_DEFINED

    def __set(self, key, value):
        if key == "channel":
            try:
                channel = int(value) - 1
                if 0 <= channel < len(self.channels):
                    self.channel = channel
                else:
                    raise ValueError
            except ValueError:
                return INVALID_ARG
        elif key == "system":
            try:
                system = int(value)
                if 0 <= system <= 1:
                    self.system_enabled = system
                else:
                    raise ValueError()
            except ValueError:
                return INVALID_ARG
        elif key == "enable":
            try:
                enabled = int(value)
                if 0 <= enabled <= 1:
                    self.__current_channel().is_enabled = enabled
                else:
                    raise ValueError()
            except ValueError:
                return INVALID_ARG
        elif key == "current":
            power_system = self.__current_channel().power_system
            try:
                current = float(value) % power_system.max_current
                power_system.current = current
            except ValueError:
                power_system.current = 0
                return INVALID_ARG
        elif key == "target":
            temperature = self.__current_channel().temperature
            try:
                target = (float(value) % (temperature.minimum - temperature.maximum)) + temperature.minimum
                temperature.target = target
            except ValueError:
                temperature.target = 0
        else:
            raise KeyError
        return None

    def __get(self, key):
        if key == "id":
            return self.id
        elif key == "channel":
            return str(self.channel + 1)
        elif key == "system":
            return str(self.system_enabled)
        elif key == "enable":
            return str(self.__current_channel().is_enabled)
        elif key == "power":
            return str(self.__current_channel().power_system.power)
        elif key == "temp":
            return str(self.__current_channel().temperature.actual)
        elif key == "current":
            return str(self.__current_channel().power_system.current)
        elif key == "target":
            return str(self.__current_channel().temperature.target)
        elif key == "specs":
            return self.__current_channel().specs()
        elif key == "statword":
            return "000%i%s" % (self.system_enabled, "".join([str(c.is_enabled) for c in self.channels]))
        else:
            raise KeyError

    def __current_channel(self):
        return self.channels[self.channel]


if __name__ == "__main__":
    dev = ThorlabsMcls1Simulation()
    dev.start_ip(9004)
    dev.start_debug(9006)
    while True:
        time.sleep(1)
