# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The Coral class is a hardware abstraction for interacting with a Google Coral

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class Coral:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
