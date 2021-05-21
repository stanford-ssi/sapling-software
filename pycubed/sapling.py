# CircuitPython modules

# Adafruit libraries

# Internal libraries

# Modules
from hardware.adcs.adcs import ADCS
from hardware.comms.comms import COMMS
from hardware.eps.eps import EPS
from hardware.gnss import GNSS
from hardware.payloads.payloads import Payloads
from hardware.storage.storage import Storage
from hardware.wdt import WDT

"""
The Sapling class is the highest level class for interfacing with PyCubed and
other payload hardware.

Attributes:
    status (bool): TO BE IMPLIMENTED
    comms (COMMS): Communication system on PyCubed (see class for more details)
    gnss (GNSS): GNSS system on PyCubed (see class for more details)
    storage (Storage): Memory storage on 


Methods:
    XXX: Summary

"""
class Sapling:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
