"""
This module contains the class definition for a the EV3 IR Sensor

Sensors tested with this class:
  - 95654
"""
import struct
import typing

import ev3_dc

import PyRSquared.lego_ev3.enums as enums
import PyRSquared.lego_ev3.sensor.sensor as sensor

if typing.TYPE_CHECKING:
    import PyRSquared.lego_ev3.ev3 as ev3


class InfraredSensor(sensor.Sensor):
    """
    This object represents the EV3 IR Sensor

    Sensors tested with this class:
      - 95654
    """

    def __init__(self, ev3_parent: 'ev3.EV3', port: enums.SensorPort):
        """
        :param ev3_parent: The EV3 object this sensor is attached to
        :param port: The port the sensor is connected to
        """
        super().__init__(ev3_parent, port)
        self.type_number = 33

    def get_distance(self) -> float:
        """
        Returns the approximate distance to an object placed in front of the sensor
        """
        return self.read_mode(0)

    def beacon_proximity(self, channel: enums.BeaconChannel) -> typing.Tuple[int, int]:
        """
        Returns the approximate distance to the beacon if the beacon is on
        (push the wide button at the top of the beacon so that the green light is on)

        This returns a tuple containing the how far away the beacon is from the sensor,
        and lateral (sideways) distance the becaon is from the sensor

        Example:
            Sensor
           /
         /
        beacon

        would return (2, -2) - 2 units away and 2 units to the left

        :param channel: the channel of the beacon to listen on
        """
        ops_read = b''.join([
            ev3_dc.opInput_Device,
            ev3_dc.READY_RAW,
            ev3_dc.LCX(0),  # LAYER
            ev3_dc.LCX(self.port.value),  # NO
            ev3_dc.LCX(self.type_number),  # TYPE - IR
            ev3_dc.LCX(1),  # MODE - Seeker
            ev3_dc.LCX(8),  # VALUES
            ev3_dc.GVX(0),  # VALUE1 - heading   channel 1
            ev3_dc.GVX(4),  # VALUE2 - proximity channel 1
            ev3_dc.GVX(8),  # VALUE3 - heading   channel 2
            ev3_dc.GVX(12),  # VALUE4 - proximity channel 2
            ev3_dc.GVX(16),  # VALUE5 - heading   channel 3
            ev3_dc.GVX(20),  # VALUE6 - proximity channel 3
            ev3_dc.GVX(24),  # VALUE5 - heading   channel 4
            ev3_dc.GVX(28)  # VALUE6 - proximity channel 4
        ])
        reply = self.ev3.ev3.send_direct_cmd(ops_read, global_mem=32)
        states = struct.unpack('8i', reply)

        return states[channel.value * 2], states[channel.value * 2 + 1]

    def get_beacon_buttons_raw(self, channel: enums.BeaconChannel) -> enums.BeaconButtons:
        """
        Returns the combination of buttons currently pressed by the beacon.
        In the event multiple buttons are pressed, you will get a value like:
        RED_UPPER_AND_BLUE_UPPER

        In the event nothing is pressed, NO_BUTTON will be returned

        To get a list of individual pressed buttons, use the get_beacon_buttons method

        :param channel: the channel of the beacon to listen on
        """
        ops_read = b''.join([
            ev3_dc.opInput_Device,
            ev3_dc.READY_SI,
            ev3_dc.LCX(0),  # LAYER
            ev3_dc.LCX(self.port.value),  # NO
            ev3_dc.LCX(self.type_number),
            ev3_dc.LCX(2),
            ev3_dc.LCX(4),  # VALUES
            ev3_dc.GVX(0),  # VALUE1
            ev3_dc.GVX(4),  # VALUE1
            ev3_dc.GVX(8),  # VALUE1
            ev3_dc.GVX(16),  # VALUE1
        ])

        reply = self.ev3.ev3.send_direct_cmd(ops_read, global_mem=16)
        button_data = struct.unpack('4f', reply)
        return enums.BeaconButtons(int(button_data[channel.value]))

    def get_beacon_buttons(
            self, channel: enums.BeaconChannel
    ) -> typing.List[enums.BeaconButtons]:
        """
        Returns a list of all the buttons currently pressed by the beacon, or
        an empty list if no buttons are pressed
        """
        pressed = self.get_beacon_buttons_raw(channel)

        result = []

        if pressed.value <= 4 or pressed.value == 9:
            result = [pressed]

        elif pressed == enums.BeaconButtons.RED_UPPER_AND_BLUE_UPPER:
            result = [enums.BeaconButtons.RED_UPPER, enums.BeaconButtons.BLUE_UPPER]

        elif pressed == enums.BeaconButtons.RED_UPPER_AND_BLUE_LOWER:
            result = [enums.BeaconButtons.RED_UPPER, enums.BeaconButtons.BLUE_LOWER]

        elif pressed == enums.BeaconButtons.RED_LOWER_AND_BLUE_UPPER:
            result = [enums.BeaconButtons.RED_LOWER, enums.BeaconButtons.BLUE_UPPER]

        elif pressed == enums.BeaconButtons.RED_LOWER_AND_BLUE_LOWER:
            result = [enums.BeaconButtons.RED_LOWER, enums.BeaconButtons.BLUE_LOWER]

        elif pressed == enums.BeaconButtons.RED_UPPER_AND_RED_LOWER:
            result = [enums.BeaconButtons.RED_UPPER, enums.BeaconButtons.RED_LOWER]

        elif pressed == enums.BeaconButtons.BLUE_UPPER_AND_BLUE_LOWER:
            result = [enums.BeaconButtons.BLUE_UPPER, enums.BeaconButtons.BLUE_LOWER]

        return result
