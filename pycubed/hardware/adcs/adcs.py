# CircuitPython modules
# Adafruit libraries
# Internal libraries
# Modules
# from imu import IMU
# from magnetorquer import Magnetorquer
# from sun_sensor import SunSensor

"""
The ADCS class handles the sun sensors, imu, and magnetorquers as to fully
encompass the attitude of the satellite.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class ADCS:
    def __init__(self):
        self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    """ ****************************** METHODS ***************************** """
