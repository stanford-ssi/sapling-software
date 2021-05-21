# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The Magnetorquer class is a hardware abstraction for monitoring and controlling
PCB magnetorquers

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class Magnetorquer:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
