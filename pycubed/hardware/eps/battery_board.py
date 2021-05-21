# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The BatteryBoard class is a hardware abstraction for interacting with PyCubed
Battery boards

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class BatteryBoard:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
