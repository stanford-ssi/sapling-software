"""
The WDT class handles the watchdog timer on pycubed.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class WDT:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
