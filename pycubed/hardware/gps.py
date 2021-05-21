"""
The GNSS class handles the GNSS module on PyCubed.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class GNSS:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
