# CircuitPython modules

# Adafruit libraries

# Internal libraries

"""
The DipoleAntenna class is a hardware abstraction for deploying and interacting
with deployed antennae

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class DipoleAntenna:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
