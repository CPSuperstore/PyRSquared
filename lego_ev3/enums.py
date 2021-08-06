"""
This module contains all the enums used by the library
"""
import enum
import ev3_dc


class MotorPort(enum.Enum):
    """
    The available ports for motors (A-D)
    """
    PORT_A = 1
    PORT_B = 2
    PORT_C = 4
    PORT_D = 8
    ALL = 15


class SensorPort(enum.Enum):
    """
    The available ports for sensors (1-4)
    """
    PORT_1 = 0
    PORT_2 = 1
    PORT_3 = 2
    PORT_4 = 3


class Color(enum.Enum):
    """
    The color which could be detected by the color sensor
    """
    NO_COLOR = 0
    BLACK = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5
    WHITE = 6
    BROWN = 7


class BeaconChannel(enum.Enum):
    """
    The channel of the beacon
    """
    CHANNEL_1 = 0
    CHANNEL_2 = 1
    CHANNEL_3 = 2
    CHANNEL_4 = 3


class BeaconButtons(enum.Enum):
    """
    The possible beacon button press combinations
    """
    NO_BUTTON = 0

    RED_UPPER = 1
    RED_LOWER = 2
    BLUE_UPPER = 3
    BLUE_LOWER = 4

    RED_UPPER_AND_BLUE_UPPER = 5
    RED_UPPER_AND_BLUE_LOWER = 6
    RED_LOWER_AND_BLUE_UPPER = 7
    RED_LOWER_AND_BLUE_LOWER = 8

    BEACON = 9

    RED_UPPER_AND_RED_LOWER = 10
    BLUE_UPPER_AND_BLUE_LOWER = 11


class LightColor(enum.Enum):
    """
    The possible colors the EV3 button lights could display
    (including OFF for no light)
    """
    OFF = 0
    RED = 1
    ORANGE = 2
    GREEN = 3


class LightEffect(enum.Enum):
    """
    The effect to use for the EV3 button lights
    """
    SOLID = 0
    FLASH = 1
    PULSE = 2


class DrawableImage(enum.Enum):
    """
    The list of images which could be shown on the EV3's display
    """

    # TODO: Complete the list of possible images

    MotorCtlAD = "../apps/Motor Control/MotorCtlAD.rgf"
    MotorCtlBC = "../apps/Motor Control/MotorCtlBC.rgf"


class DrawableColor(enum.Enum):
    """
    The list of colors which can be displayed by the EV3's display
    """
    WHITE = 0
    BLACK = 1


class Buttons(enum.Enum):
    """
    The buttons which are on the actual EV3 brick
    """
    BACK = ev3_dc.BACK_BUTTON
    RIGHT = ev3_dc.RIGHT_BUTTON
    LEFT = ev3_dc.LEFT_BUTTON
    UP = ev3_dc.UP_BUTTON
    DOWN = ev3_dc.DOWN_BUTTON


class SoundFile(enum.Enum):
    """
    The list of sounds which could be played by the EV3
    """

    # TODO: Complete the list of possible sounds

    # NOTE: DownloadSucces is spelled incorrectly on purpose!
    # This is due to a filename length constraint
    DOWNLOAD_SUCCESS = "./ui/DownloadSucces"
    OVERPOWER_ALERT = "./ui/OverpowerAlert"
    GENERAL_ALARM = "./ui/GeneralAlarm"
    POWER_DOWN = "./ui/PowerDown"
    STARTUP = "./ui/Startup"
    CLICK = "./ui/Click"
