# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The UHFRadio class is a hardware abstraction for interacting with RFM98PW LoRa
Radios

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class UHFRadio:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
