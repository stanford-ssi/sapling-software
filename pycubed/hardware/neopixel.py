# CircuitPython modules

# Adafruit libraries
import neopixel
import board
# Internal libraries

"""
The NeoPixel class handles the neopixel on PyCubed.

Attributes:
    status (bool):

Methods:
    XXX: Summary

"""
class NeoPixel:
    def __init__(self):
        try:
            # set neopixel hardware on board with corresponding pin, number of
            # neopixels, brightness, and pixel order
            self.__pixel = neopixel.NeoPixel(board.NEOPIXEL, 1,
                                                brightness=0.2,
                                                pixel_order='GRB')[0]
            # initialize pixel to be off
            self.__pixel = (0,0,0)
            # if worked, then set status to true
            self.__status = True
        except Exception as e:
            # set status to false and throw errror if neopixel not connecting
            print('Neopixel not responding: ', e)
            self.__status = False

    """ ***************************** ATTRIBUTES *************************** """

    @property
    def status(self):
        return self.__status

    @property
    def RGB(self):
        retun self.__pixel
    @RGB.setter
    def RGB(self,value):
        try:
            self.__pixel = value
        except Exception as e:
            print('Neopixel not responding: ', e)
            self.__status = False


    """ ****************************** METHODS ***************************** """

    def set_white(self):
        self.RGB = (50,50,50)
