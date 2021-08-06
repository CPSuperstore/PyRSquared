# PyRSquared
A library for interacting with various robotics kits in Python

The following is a list of each supported robotics kit. Each kit is explained in subsequent sections
- Lego EV3

## Lego EV3
The [Lego EV3](https://www.lego.com/en-ca/product/lego-mindstorms-ev3-31313) robotics kit is a kit which allows you to easily build robots using Lego. 
Traditionally, to use Python to interact with an EV3 brick, you would need to install a custom OS.

But fear not! There is another way! We can send direct hardware commands to the brick and control it without installing anything!

To learn how to use the EV3 library, head over to the repository's [Wiki](https://github.com/CPSuperstore/PyRSquared/wiki).

### Credits
The Lego EV3 library is an object-oriented wrapper for the [ev3-dc Library](https://pypi.org/project/ev3-dc/).

In addition, the following resources were used for understanding the hardware commands which are sent to and from the Lego EV3 brick:
- https://www.mikrocontroller.net/attachment/338591/hardware_developer_kit.pdf
- http://ev3directcommands.blogspot.com/2016/
