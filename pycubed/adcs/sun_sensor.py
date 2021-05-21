# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The SunSensor class is a hardware abstraction for interacting with OPT3001
sensors

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class SunSensor:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
