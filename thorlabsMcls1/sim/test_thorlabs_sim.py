from unittest import TestCase
from thorlabs_sim import ThorlabsMcls1Simulation, HELP, NOT_DEFINED, INVALID_ARG


class TestThorlabsMcls1Simulation(TestCase):
    def setUp(self):
        self.laser = ThorlabsMcls1Simulation()

    # Invalid commands
    def test_mcls1_rejects_unknwon_command(self):
        self.assert_not_defined("qwerty")

    def test_mcls1_rejects_unknwon_query(self):
        self.assert_not_defined("hello?")

    def test_mcls1_rejects_unknwon_setter(self):
        self.assert_not_defined("hello=4")

    def assert_not_defined(self, command):
        reply = self.laser.reply("%s" % command)
        assert reply == NOT_DEFINED

    # Static laser info (getters only)
    def test_mcls1_gives_help_screen(self):
        reply = self.laser.reply("?")
        assert reply == HELP

    def test_mcls1_uses_default_model(self):
        reply = self.laser.reply("id?")
        assert reply.startswith("THORLABS MCLS")

    def test_mcls1_uses_non_default_model(self):
        self.laser = ThorlabsMcls1Simulation(model="THORLABS MCLS2")
        reply = self.laser.reply("id?")
        assert reply.startswith("THORLABS MCLS2")

    def test_mcls1_uses_default_firmware_version(self):
        reply = self.laser.reply("id?")
        assert reply.endswith("vers 1.06")

    def test_mcls1_uses_non_default_firmware_version(self):
        self.laser = ThorlabsMcls1Simulation(firmware="1.02")
        reply = self.laser.reply("id?")
        assert reply.endswith("vers 1.02")

    def test_mcls1_gives_correct_id(self):
        self.laser = ThorlabsMcls1Simulation(model="THORLABS MCLS2", firmware="1.02")
        reply = self.laser.reply("id?")
        assert reply == "THORLABS MCLS2 vers 1.02"

    # Active channel
    def test_mcls1_uses_default_starting_active_channel(self):
        reply = self.laser.reply("channel?")
        assert reply == "1"

    def test_mcls1_uses_non_default_starting_active_channel(self):
        self.laser = ThorlabsMcls1Simulation(channel=2)
        reply = self.laser.reply("channel?")
        assert reply == "2"

    def test_mcls1_can_set_channel(self):
        self.laser.reply("channel=2")
        reply = self.laser.reply("channel?")
        assert reply == "2"

    def test_mcls1_gives_error_when_setting_channel_too_big(self):
        reply = self.laser.reply("channel=5")
        assert reply == INVALID_ARG

    def test_mcls1_cannot_set_channel_too_big(self):
        self.laser.reply("channel=5")
        reply = self.laser.reply("channel?")
        assert reply == "1"

    def test_mcls1_gives_error_when_setting_channel_too_small(self):
        reply = self.laser.reply("channel=0")
        assert reply == INVALID_ARG

    def test_mcls1_cannot_set_channel_too_small(self):
        self.laser.reply("channel=0")
        reply = self.laser.reply("channel?")
        assert reply == "1"

    def test_mcls1_gives_error_when_setting_channel_negative(self):
        reply = self.laser.reply("channel=-1")
        assert reply == INVALID_ARG

    def test_mcls1_cannot_set_channel_negative(self):
        self.laser.reply("channel=-1")
        reply = self.laser.reply("channel?")
        assert reply == "1"

    def test_mcls1_gives_error_when_setting_channel_to_invalid_value(self):
        reply = self.laser.reply("channel=A")
        assert reply == INVALID_ARG

    def test_mcls1_cannot_set_channel_to_invalid_value(self):
        self.laser.reply("channel=A")
        reply = self.laser.reply("channel?")
        assert reply == "1"

    # System enable
    def test_mcls1_system_disabled_at_start(self):
        reply = self.laser.reply("system?")
        assert reply == "0"

    def test_mcls1_rejects_greater_than_1_for_system(self):
        reply = self.laser.reply("system=2")
        assert reply == INVALID_ARG

    def test_mcls1_does_not_change_system_for_values_greater_than_1(self):
        self.laser.reply("system=2")
        reply = self.laser.reply("system?")
        assert reply == "0"

    def test_mcls1_rejects_less_than_0_for_system(self):
        reply = self.laser.reply("system=-1")
        assert reply == INVALID_ARG

    def test_mcls1_does_not_change_system_for_values_less_than_0(self):
        self.laser.reply("system=-1")
        reply = self.laser.reply("system?")
        assert reply == "0"

    def test_mcls1_rejects_invalid_value_for_system(self):
        reply = self.laser.reply("system=A")
        assert reply == INVALID_ARG

    def test_mcls1_does_not_change_system_for_invalid_values(self):
        self.laser.reply("system=A")
        reply = self.laser.reply("system?")
        assert reply == "0"

    def test_mcls1_can_enable_system(self):
        self.laser.reply("system=1")
        reply = self.laser.reply("system?")
        assert reply == "1"

    def test_mcls1_can_enable_and_disable_system(self):
        self.laser.reply("system=1")
        self.laser.reply("system=0")
        reply = self.laser.reply("system?")
        assert reply == "0"

    # Channel enable
    def test_first_channel_dsabled_by_default(self):
        reply = self.laser.reply("enable?")
        assert reply == "0"

    def test_mcls1_rejects_greater_than_1_for_channel_enable(self):
        reply = self.laser.reply("enable=2")
        assert reply == INVALID_ARG

    def test_mcls1_does_not_change_channel_enable_for_values_greater_than_1(
            self):
        self.laser.reply("enable=2")
        reply = self.laser.reply("enable?")
        assert reply == "0"

    def test_mcls1_rejects_less_than_0_for_channel_enable(self):
        reply = self.laser.reply("enable=-1")
        assert reply == INVALID_ARG

    def test_mcls1_does_not_change_channel_enable_for_values_less_than_0(self):
        self.laser.reply("enable=-1")
        reply = self.laser.reply("enable?")
        assert reply == "0"

    def test_mcls1_rejects_invalid_value_for_channel_enable(self):
        reply = self.laser.reply("enable=A")
        assert reply == INVALID_ARG

    def test_mcls1_does_not_change_channel_enable_for_invalid_values(self):
        self.laser.reply("enable=A")
        reply = self.laser.reply("enable?")
        assert reply == "0"

    def test_mcls1_can_enable_channel(self):
        self.laser.reply("enable=1")
        reply = self.laser.reply("enable?")
        assert reply == "1"

    def test_mcls1_can_enable_and_disable_channel(self):
        self.laser.reply("enable=1")
        self.laser.reply("enable=0")
        reply = self.laser.reply("enable?")
        assert reply == "0"

    def test_mcls1_can_enable_channel_without_enabling_other_channel(self):
        self.laser.reply("enable=1")
        self.laser.reply("channel=2")
        reply = self.laser.reply("enable?")
        assert reply == "0"

    # Channel read only values
    def test_mcls1_reads_channel_power(self):
        reply = self.laser.reply("power?")
        assert reply == "7.36"

    def test_mcls1_reads_channel_temperature(self):
        reply = self.laser.reply("temp?")
        assert reply == "23.2"

    def test_mcls1_includes_wavelength_in_specs(self):
        reply = self.laser.reply("specs?")
        assert "Wavelength = 406" in reply

    def test_mcls1_includes_max_power_in_specs(self):
        reply = self.laser.reply("specs?")
        assert "POut = 7.36" in reply

    def test_mcls1_includes_max_current_in_specs(self):
        reply = self.laser.reply("specs?")
        assert "IOp = 49" in reply

    # Guessing it is a standby current as there is nothing in the spec
    def test_mcls1_includes_standby_current_in_specs(self):
        reply = self.laser.reply("specs?")
        assert "IMon = 0.0" in reply

    def test_mcls1_includes_ideal_channel_temperature_in_specs(self):
        reply = self.laser.reply("specs?")
        assert "ITh = 20.0" in reply

    def test_mcls1_includes_channel_serial_number_in_specs(self):
        reply = self.laser.reply("specs?")
        assert "SerialNumber = 110721-59" in reply

    def test_mcls1_specs(self):
        reply = self.laser.reply("specs?")
        assert reply == """
        Wavelength = 406
        POut = 7.36
        IOp = 49
        IMon = 0.0
        ITh = 20.0
        SerialNumber = 110721-59
        """

    def test_mcls1_gives_statword_0_when_everything_off(self):
        reply = self.laser.reply("statword?")
        assert reply == "00000000"

    def test_mcls1_gives_correct_statword_for_system_enable_only(self):
        self.laser.reply("system=1")
        reply = self.laser.reply("statword?")
        assert reply == "00010000"

    def test_mcls_gives_correct_statword_for_channel_1_enable_only(self):
        self.laser.reply("enable=1")
        reply = self.laser.reply("statword?")
        assert reply == "00001000"

    def test_mcls_gives_correct_statword_for_channel_2_enable_only(self):
        self.laser.reply("channel=2")
        self.laser.reply("enable=1")
        reply = self.laser.reply("statword?")
        assert reply == "00000100"

    def test_mcls_gives_correct_statword_for_channel_3_enable_only(self):
        self.laser.reply("channel=3")
        self.laser.reply("enable=1")
        reply = self.laser.reply("statword?")
        assert reply == "00000010"

    def test_mcls_gives_correct_statword_for_channel_4_enable_only(self):
        self.laser.reply("channel=4")
        self.laser.reply("enable=1")
        reply = self.laser.reply("statword?")
        assert reply == "00000001"

    def test_mcls_gives_correct_statword_for_channel_1_and_system_enable(self):
        self.laser.reply("enable=1")
        self.laser.reply("system=1")
        reply = self.laser.reply("statword?")
        assert reply == "00011000"

    def test_mcls_gives_correct_statword_for_channel_2_and_system_enable(self):
        self.laser.reply("channel=2")
        self.laser.reply("enable=1")
        self.laser.reply("system=1")
        reply = self.laser.reply("statword?")
        assert reply == "00010100"

    # Current
    def test_mcls1_reads_channel_current(self):
        reply = self.laser.reply("current?")
        assert reply == "49"

    def test_mcls1_sets_channel_current(self):
        self.laser.reply("current=23")
        reply = self.laser.reply("current?")
        assert reply == "23.0"

    def test_mcls1_modulates_negative_current(self):
        self.laser.reply("current=-1")
        reply = self.laser.reply("current?")
        assert reply == "48.0"

    def test_mcls1_modulates_too_high_current(self):
        self.laser.reply("current=50")
        reply = self.laser.reply("current?")
        assert reply == "1.0"

    def test_mcls1_sets_current_to_0_if_given_not_float(self):
        self.laser.reply("current=a")
        reply = self.laser.reply("current?")
        assert reply == "0"

    # Target temperature
    def test_mcls1_reads_channel_target_temperature(self):
        reply = self.laser.reply("target?")
        assert reply == "20"

    def test_mcls1_modulates_negative_target_temperature(self):
        self.laser.reply("target=-1")
        reply = self.laser.reply("target?")
        assert reply == "19.0"

    def test_mcls1_modulates_too_high_target_temperature(self):
        self.laser.reply("target=50")
        reply = self.laser.reply("target?")
        assert reply == "20.0"

    def test_mcls1_sets_target_temperature_to_0_if_given_not_float(self):
        self.laser.reply("target=a")
        reply = self.laser.reply("target?")
        assert reply == "0"
