# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The SolarPanel class is a hardware abstraction for interacting with solar panel 
PCBs

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class SolarPanel:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
