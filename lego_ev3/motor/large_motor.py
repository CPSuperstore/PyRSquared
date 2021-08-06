"""
This module contains the class definition for a large EV3 motor

Motors tested with this class:
  - 95658
"""
import typing

import PyRSquared.lego_ev3.enums as enums
import PyRSquared.lego_ev3.motor.motor as motor

if typing.TYPE_CHECKING:
    import PyRSquared.lego_ev3.ev3 as ev3


class LargeMotor(motor.Motor):
    """
    This object represents a large EV3 motor

    Motors tested with this class:
      - 95658
    """

    def __init__(self, ev3_parent: 'ev3.EV3', port: enums.MotorPort):
        """
        :param ev3_parent: The EV3 object this motor is attached to
        :param port: The port the motor is connected to
        """
        super().__init__(ev3_parent, port)
        self.max_rpm = 170
