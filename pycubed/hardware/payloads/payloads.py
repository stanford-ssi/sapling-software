# CircuitPython modules

# Adafruit libraries

# Internal libraries

# Module
from coral import Coral

"""
The Payloads class handles the payload computer and any other external payloads
directly connected to pycubed not in the critical operation systems.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class Payloads:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
