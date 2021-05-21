# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The USBCharger class is a hardware abstraction for interacting with

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class USBCharger:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
