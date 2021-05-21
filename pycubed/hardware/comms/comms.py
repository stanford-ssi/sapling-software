# CircuitPython modules

# Adafruit libraries

# Internal libraries

# Module
from dipole_antenna import DipoleAntenna
from uhf_radio import UHFRadio

"""
The COMMS class handles the UHF radio and dipole antenna as to fully encompass
the communication systems on PyCubed.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class COMMS:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
