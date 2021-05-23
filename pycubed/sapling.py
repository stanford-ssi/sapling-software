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
from hardware.neopixel import NeoPixel

"""
The Sapling class is the highest level class for interfacing with PyCubed and
other payload hardware.

Attributes:
    status (bool): TO BE IMPLIMENTED
    neopixel (NeoPixel): NeoPixel controls on Pycubed (see class for
        more details)
    comms (COMMS): Communication system on PyCubed (see class for more details)
    gnss (GNSS): GNSS system on PyCubed (see class for more details)
    storage (Storage): Memory storage on PyCubed (see class for more details)
    wtd (WDT): Watch-dog Timer on PyCubed (see class for more details)
    payloads (Payloads): All external payloads not associated with critcal
        systems like the payload science computer (see class for more details)
    eps (EPS): Electrical power system of satellite, monitored and controlled by
        PyCubed
    adcs (ADCS): Attitude determination and control system of satellite

Methods:
    XXX: Summary

"""
class Sapling:
    def __init__(self):
        self.__status = False
        self.__neopixel = NeoPixel()
    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    @property
    def neopixel(self):
        return self.__neopixel

    """ ****************************** METHODS ***************************** """
