"""
The Sapling class is the highest level class for interfacing with PyCubed and
other payload hardware.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class Sapling:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return status

    """ ****************************** METHODS ***************************** """
