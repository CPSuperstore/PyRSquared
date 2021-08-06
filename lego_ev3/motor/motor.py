"""
This module contains the class definition for a generic EV3 motor

Motors tested with this class:
  - 95658
  - 99455
"""
import struct
import time
import typing

import ev3_dc

import PyRSquared.lego_ev3.enums as enums

if typing.TYPE_CHECKING:
    import PyRSquared.lego_ev3.ev3 as ev3


class Motor:
    """
    This object represents a generic EV3 motor

    Motors tested with this class:
      - 95658
      - 99455
    """

    def __init__(self, ev3_parent: 'ev3.EV3', port: enums.MotorPort):
        """
        :param ev3_parent: The EV3 object this motor is attached to
        :param port: The port the motor is connected to
        """
        self.ev3 = ev3_parent
        self.port = port

        self.ev3.add_motor(port, self)

        self.max_rpm = None

    def rotate_degrees(self, speed: int, angle: float):
        """
        Rotates the motor by the specified number of degrees at the specified
        NOTE: This is not usually 100% accurate

        :param speed: The speed as a percentage
        :param angle: The angle to rotate in degrees

        :raises NotImplementedError: If the Motor class is instantiated directly.
        To use this functionality, instantiate either the LargeMotor or MediumMotor class.
        """
        if self.max_rpm is None:
            raise NotImplementedError(
                "Max RPM must be set in order to use this function. "
                "Please use the LargeMotor or MediumMotor class "
                "(they are child classes so no code changes are required) "
                "to take advantage of this functionality"
            )

        rpm = (speed / 100) * self.max_rpm
        seconds_per_degree = 1 / (rpm * 6)

        self.rotate_for_time(speed, seconds_per_degree * angle)

    def rotate(self, speed: int):
        """
        Begins rotating this motor at the specified speed.
        The motor will spin indefinitely until stopped,
        the .close() method is called on the brick, or the program is terminated cleanly
        :param speed: The speed as a percentage
        """
        ops = b''.join([
            ev3_dc.opOutput_Speed,
            ev3_dc.LCX(0),  # LAYER
            ev3_dc.LCX(self.port.value),  # NOS
            ev3_dc.LCX(speed),  # SPEED
            ev3_dc.opOutput_Start,
            ev3_dc.LCX(0),                       # LAYER
            ev3_dc.LCX(self.port.value)  # NOS
        ])
        self.ev3.ev3.send_direct_cmd(ops)

    def rotate_for_time(self, speed: int, duration: float):
        """
        Begins rotating this motor at the specified speed for the specified amount of time.
        Note that this command will block execution.
        :param speed: The speed as a percentage
        :param duration: The time to spin for in seconds
        """
        self.rotate(speed)
        time.sleep(duration)
        self.stop()

    def stop(self):
        """
        Stops the motor from spinning
        """
        ops = b''.join([
            ev3_dc.opOutput_Stop,
            ev3_dc.LCX(0),  # LAYER
            ev3_dc.LCX(self.port.value),  # NOS
            ev3_dc.LCX(0)  # BRAKE
        ])
        self.ev3.ev3.send_direct_cmd(ops)

    def get_rotation(self) -> float:
        """
        Returns the current motor rotation in degrees
        """
        ops = b''.join([
            ev3_dc.opInput_Device,
            ev3_dc.READY_SI,
            ev3_dc.LCX(0),  # LAYER
            ev3_dc.port_motor_input(self.port.value),  # NO
            ev3_dc.LCX(7),  # TYPE
            ev3_dc.LCX(0),  # MODE
            ev3_dc.LCX(1),  # VALUES
            ev3_dc.GVX(0),  # VALUE1
        ])
        self.ev3.ev3.send_direct_cmd(ops)
        reply = self.ev3.ev3.send_direct_cmd(ops, global_mem=4)
        return struct.unpack('f', reply)[0]

    def get_port(self) -> enums.MotorPort:
        """
        Returns the port this sensor is connected to
        """
        return self.port
