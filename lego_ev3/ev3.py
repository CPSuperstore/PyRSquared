"""
This module contains the class definition for the EV3 Programmable Brick

Bricks tested with this class:
  - 95646
"""
import struct
import typing
import warnings

import ev3_dc

import PyRSquared.lego_ev3.enums as enums

if typing.TYPE_CHECKING:
    import PyRSquared.lego_ev3.motor.motor as motor
    import PyRSquared.lego_ev3.sensor.sensor as sensor


class EV3:
    """
    This object represents an EV3 Programmable Brick

    Bricks tested with this class:
      - 95646
    """
    def __init__(self, ev3: ev3_dc.EV3):
        """
        Please use one of the class methods instead of the default constructor:
        bluetooth_connection, usb_connection, wifi_connection

        If you insist on establishing your own connection to your EV3 brick
        This constructor is how this is done
        :param ev3: the EV3 object from the ev3_dc library
        """
        self.ev3 = ev3
        self.motors = {}            # type: typing.Dict[enums.MotorPort, motor.Motor]
        self.sensors = {}            # type: typing.Dict[enums.SensorPort, sensor.Sensor]

        self.actuator_map = ev3.sensors

    @classmethod
    def bluetooth_connection(cls, brick_id_or_mac: str):
        """
        Connects to an EV3 brick over Bluetooth connection.

        NOTE 1: This is the most reliable way to connect to the brick,
        however it may stop working after a few runs.
        In this case go to the settings tab (with the wrench icon)
        and scroll down and click on the Bluetooth option.
        Scroll up to the "Connections" option, and select your computer.
        In the following menu, select "Disconnect"

        NOTE 2: Your computer must have Bluetooth on for this to work.
        Checking this first will save you hours of hair pulling.

        :param brick_id_or_mac: The ID of the brick/MAC address of the brick to connect to
        This can be found by going to the settings tab (with the wrench icon) and
        scrolling down and selecting the "Brick Info" option.
        The value is listed under "ID:"
        """
        return cls(ev3_dc.EV3(protocol=ev3_dc.BLUETOOTH, host=brick_id_or_mac))

    @classmethod
    def usb_connection(cls):
        """
        Connects to an EV3 brick over USB connection.
        """
        return cls(ev3_dc.EV3(protocol=ev3_dc.USB))

    @classmethod
    def wifi_connection(cls):
        """
        Connects to an EV3 brick over WIFI connection.
        """
        return cls(ev3_dc.EV3(protocol=ev3_dc.WIFI))

    def __del__(self):
        """
        This destructor stops all motors and safely closes the connection to the brick
        Without this, the connection between your computer and the brick
        may persist after the program is run which will cause re-connection issues
        See "Note 1" in the bluetooth_connection class method

        Note: this method is wrapped by the "close" method for code clarity
        """
        for motor_obj in self.motors.values():
            motor_obj.stop()

        self.ev3.__del__()

    def close(self):
        """
        Stops all motors and safely closes the connection to the brick
        By not calling this, the connection between your computer and the brick
        may persist after the program is run which will cause re-connection issues
        See "Note 1" in the bluetooth_connection class method

        Note: this functionality is the default destructor functionality
        """
        self.__del__()

    def add_motor(self, port: enums.MotorPort, motor_object: 'motor.Motor'):
        """
        This method adds a motor to the brick.
        Note that a motor will not work unless it has been added to an EV3 brick
        This is done automatically in the Motor class constructor

        Note: if you add two motors on the same port,
        a warning will be raised (but not an exception)
        :param port: the port the motor is connected to
        :param motor_object: the motor object to add
        """
        if port in self.motors:
            warnings.warn("The specified port '{}' already has a motor assigned.".format(port))

        self.motors[port] = motor_object

    def add_sensor(self, port: enums.SensorPort, sensor_object: 'sensor.Sensor'):
        """
        This method adds a sensor to the brick.
        Note that a sensor will not work unless it has been added to an EV3 brick
        This is done automatically in the Sensor class constructor

        Note: if you add two motors on the same port,
        a warning will be raised (but not an exception)
        :param port: the port the sensor is connected to
        :param sensor_object: the sensor object to add
        """
        if port in self.motors:
            warnings.warn("The specified port '{}' already has a sensor assigned.".format(port))

        self.sensors[port] = sensor_object

    def set_status_light(
            self, color: enums.LightColor, effect: enums.LightEffect = enums.LightEffect.SOLID
    ):
        """
        Sets the status light (the light of the buttons on the EV3 brick)
        :param color: The color to set the lights to (or OFF to turn off the lights)
        :param effect: The effect to run the lights as
        """
        mode = ev3_dc.LED_OFF

        if color == enums.LightColor.RED:
            if effect == enums.LightEffect.SOLID:
                mode = ev3_dc.LED_RED
            elif effect == enums.LightEffect.FLASH:
                mode = ev3_dc.LED_RED_FLASH
            elif effect == enums.LightEffect.PULSE:
                mode = ev3_dc.LED_RED_PULSE

        elif color == enums.LightColor.ORANGE:
            if effect == enums.LightEffect.SOLID:
                mode = ev3_dc.LED_ORANGE
            elif effect == enums.LightEffect.FLASH:
                mode = ev3_dc.LED_ORANGE_FLASH
            elif effect == enums.LightEffect.PULSE:
                mode = ev3_dc.LED_ORANGE_PULSE

        elif color == enums.LightColor.GREEN:
            if effect == enums.LightEffect.SOLID:
                mode = ev3_dc.LED_GREEN
            elif effect == enums.LightEffect.FLASH:
                mode = ev3_dc.LED_GREEN_FLASH
            elif effect == enums.LightEffect.PULSE:
                mode = ev3_dc.LED_GREEN_PULSE

        ops = b''.join([
            ev3_dc.opUI_Write,
            ev3_dc.LED,
            mode,
        ])

        self.ev3.send_direct_cmd(ops)

    def display_image(
            self, image: enums.DrawableImage, x_pos: int = 0, y_pos: int = 0,
            color: enums.DrawableColor = enums.DrawableColor.BLACK
    ):
        """
        Display the specified image on the display screen of the EV3 brick
        :param image: the name of the image to display
        :param x_pos: the x position to display the image
        :param y_pos: the y position to display the image
        :param color: The color to draw the image as (black - default, or white)
        """
        ops = b''.join([
            ev3_dc.opUI_Draw,
            ev3_dc.TOPLINE,
            ev3_dc.LCX(0),  # ENABLE
            ev3_dc.opUI_Draw,
            ev3_dc.BMPFILE,
            ev3_dc.LCX(color.value),  # COLOR
            ev3_dc.LCX(x_pos),  # X0
            ev3_dc.LCX(y_pos),  # Y0
            ev3_dc.LCS(image.value),  # NAME
            ev3_dc.opUI_Draw,
            ev3_dc.UPDATE
        ])
        self.ev3.send_direct_cmd(ops)

    def clear_display(
            self, color: enums.DrawableColor = enums.DrawableColor.WHITE
    ):
        """
        Clears the display by filling it with the specified color (black, or white - default)
        """
        ops = b''.join([
            ev3_dc.opUI_Draw,
            ev3_dc.TOPLINE,
            ev3_dc.LCX(1),
            ev3_dc.opUI_Draw,
            ev3_dc.FILLWINDOW,
            ev3_dc.LCX(color.value),
            ev3_dc.LCX(0),
            ev3_dc.LCX(0),
            ev3_dc.opUI_Draw,
            ev3_dc.UPDATE
        ])
        self.ev3.send_direct_cmd(ops)

    def display_line(
            self, x_1: int, y_1: int, x_2: int, y_2: int,
            color: enums.DrawableColor = enums.DrawableColor.BLACK
    ):
        """
        Draws a single line on the display
        :param x_1: the starting x position of the line
        :param y_1: the starting y position of the line
        :param x_2: the ending x position of the line
        :param y_2: the ending y position of the line
        :param color: the color to draw the line as (black - default, or white)
        """
        ops = b''.join([
            ev3_dc.opUI_Draw,
            ev3_dc.LINE,
            ev3_dc.LCX(color.value),  # COLOR
            ev3_dc.LCX(x_1),  # X0
            ev3_dc.LCX(y_1),  # Y0
            ev3_dc.LCX(x_2),  # X1
            ev3_dc.LCX(y_2),  # Y1
            ev3_dc.opUI_Draw,
            ev3_dc.UPDATE,
        ])
        self.ev3.send_direct_cmd(ops)

    def simulate_button_press(self, button: enums.Buttons, wait_for_completion: bool = True):
        """
        Simulates a button press
        (in other words, tricks the EV3 brick
        into thinking one of the buttons on it was pressed)
        :param button: The button to simulate the press of
        :param wait_for_completion: If the method call should block
        until the press is complete (default = true)
        (this only takes a few milliseconds to complete and is safer)
        """
        ops = b''.join([
            ev3_dc.opUI_Button,
            ev3_dc.PRESS,
            button.value
        ])

        if wait_for_completion:
            ops += b''.join([
                ev3_dc.opUI_Button,
                ev3_dc.WAIT_FOR_PRESS,
            ])

        self.ev3.send_direct_cmd(ops)

    def play_tone(self, volume: int, frequency: int, duration: int):
        """
        Plays a single tone from the EV3 brick
        :param volume: the volume as a percent.
        This volume is not affected by the volume set in the EV3 brick's settings
        :param frequency: The frequency of the tone to play in Hz.
        This can range from 250 - 10000
        :param duration: The total amount of time to play the tone for in ms
        """
        ops = b''.join([
            ev3_dc.opSound,
            ev3_dc.TONE,
            ev3_dc.LCX(volume),  # VOLUME
            ev3_dc.LCX(frequency),  # FREQUENCY
            ev3_dc.LCX(duration),  # DURATION
        ])
        self.ev3.send_direct_cmd(ops)

    def play_sound(self, sound_file: enums.SoundFile, volume: int, repeat: bool = False):
        """
        Plays the specified sound file
        :param sound_file: the name of the sound file to play
        :param volume: the volume as a percent.
        This volume is not affected by the volume set in the EV3 brick's settings
        :param repeat: If the sound should be repeated forever after it is played
        Use the "stop_sound" method to stop playing the sound
        """
        ops = b''.join([
            ev3_dc.opSound,
            ev3_dc.REPEAT if repeat else ev3_dc.PLAY,
            ev3_dc.LCX(volume),  # VOLUME
            ev3_dc.LCS(sound_file.value)  # NAME
        ])
        self.ev3.send_direct_cmd(ops)

    def stop_sound(self):
        """
        Stops all sounds from being played from the EV3 brick
        """
        ops = b''.join([
            ev3_dc.opSound,
            ev3_dc.BREAK
        ])
        self.ev3.send_direct_cmd(ops)

    def get_brick_name(self) -> str:
        """
        Returns the name assigned to the EV3 brick,
        which is set in the EV3 brick's settings
        """
        ops = b''.join([
            ev3_dc.opCom_Get,
            ev3_dc.GET_BRICKNAME,
            ev3_dc.LCX(16),  # LENGTH
            ev3_dc.GVX(0)  # NAME
        ])
        reply = self.ev3.send_direct_cmd(ops, global_mem=16)
        (brick_name,) = struct.unpack('16s', reply)
        return brick_name.split(b'\x00')[0].decode("ascii")
