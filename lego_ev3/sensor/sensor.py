"""
This module contains the class definition for a the EV3 Sensor Base
All sensors extend this class

Sensors tested with children of this class:
  - 95650
  - 95654
  - 95648
"""
import abc
import struct
import typing

import ev3_dc

import PyRSquared.lego_ev3.enums as enums

if typing.TYPE_CHECKING:
    import PyRSquared.lego_ev3.ev3 as ev3


class Sensor(abc.ABC):
    """
    This abstract object represents a generic EV3 Sensor

    Sensors tested with children of this class:
      - 95650
      - 95654
      - 95648
    """
    def __init__(self, ev3_parent: 'ev3.EV3', port: enums.SensorPort):
        """
        :param ev3_parent: The EV3 object this sensor is attached to
        :param port: The port the sensor is connected to
        """
        self.ev3 = ev3_parent
        self.port = port
        self.type_number = None

        self.ev3.add_sensor(port, self)

    def read_mode(self, mode: int) -> float:
        """
        Reads and returns a single 4 bit float from the EV3 brick stored at the specified mode
        :param mode: The mode to read
        """
        ops_read = b''.join([
            ev3_dc.opInput_Device,
            ev3_dc.READY_SI,
            ev3_dc.LCX(0),  # LAYER
            ev3_dc.LCX(self.port.value),  # NO
            ev3_dc.LCX(self.type_number),
            ev3_dc.LCX(mode),
            ev3_dc.LCX(1),  # VALUES
            ev3_dc.GVX(0),  # VALUE1
        ])

        reply = self.ev3.ev3.send_direct_cmd(ops_read, global_mem=4)
        return struct.unpack('f', reply)[0]

    def get_type_number(self):
        """
        Returns the sensor type number of this sensor type
        """
        return self.type_number

    def get_port(self) -> enums.SensorPort:
        """
        Returns the port this sensor is connected to
        """
        return self.port
