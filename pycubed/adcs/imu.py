# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The IMU class is a hardware abstraction interacting with the BMX160

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class IMU:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
