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
