# CircuitPython modules

# Adafruit libraries

# Internal libraries

# Module
from battery_board import BatteryBoard
from solar_panel import SolarPanel
from usb_charger import USBCharger

"""
The EPS class handles the battery board, solar panels, and usb chargering as to
fully encompass the power system of the satellite.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class EPS:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
