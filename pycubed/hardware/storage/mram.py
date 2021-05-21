# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The MRAM class is a hardware abstraction for interacting with MRAM

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class MRAM:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
