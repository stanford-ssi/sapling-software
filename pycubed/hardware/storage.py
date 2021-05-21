# CircuitPython modules

# Adafruit libraries

# Internal libraries

# Module
from storage.mram import MRAM
from storage.sd_card import SDCard

"""
The Storage class handles all memory storage on PyCubed including the MRAM and
SD card.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class Storage:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
