# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The SDCard class is a hardware abstraction for interacting with an SD card

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class SDCard:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
