# CircuitPython modules

# Adafruit libraries

# Internal libraries

# Module
from eps.battery_board import BatteryBoard
from eps.solar_panel import SolarPanel
from eps.usb_charger import USBCharger

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
