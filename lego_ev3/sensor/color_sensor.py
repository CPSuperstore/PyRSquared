"""
This module contains the class definition for a the EV3 Color Sensor

Sensors tested with this class:
  - 95650
"""
import typing

import PyRSquared.lego_ev3.enums as enums
import PyRSquared.lego_ev3.sensor.sensor as sensor

if typing.TYPE_CHECKING:
    import PyRSquared.lego_ev3.ev3 as ev3


class ColorSensor(sensor.Sensor):
    """
    This object represents the EV3 Color Sensor

    Sensors tested with this class:
      - 95650
    """

    def __init__(self, ev3_parent: 'ev3.EV3', port: enums.SensorPort):
        """
        :param ev3_parent: The EV3 object this sensor is attached to
        :param port: The port the sensor is connected to
        """
        super().__init__(ev3_parent, port)
        self.type_number = 29

    def reflected_light_intensity(self) -> float:
        """
        Returns the reflected light intensity
        This can be between 0 and 100, where 0 = no light and 100 = full light
        """
        return self.read_mode(0)

    def color(self) -> enums.Color:
        """
        Returns the color detected by the color sensor (see the Color enum)
        This can be one of 7 colors, or NO_COLOR if the color can not be resolved
        """
        return enums.Color(int(self.read_mode(2)))

    def ambient_light_intensity(self) -> float:
        """
        Returns the reflected light intensity
        This can be between 0 and 100, where 0 = darkness and 100 = pointing at sunlight
        """
        return self.read_mode(1)
