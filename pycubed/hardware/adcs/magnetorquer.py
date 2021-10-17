# CircuitPython modules
import time

# Adafruit libraries

# Internal libraries
from lib.drivers.drv8830 import DRV8830, COAST, REVERSE, FORWARD, BRAKE

"""
The Magnetorquer class is a hardware abstraction for monitoring and controlling
PCB magnetorquers

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""


class Magnetorquer:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """

    def blink_test():
        driver = DRV8830()
        while(True):
            driver.mode = FORWARD
            time.sleep(1)
            driver.mode = BRAKE
            time.sleep(1)
