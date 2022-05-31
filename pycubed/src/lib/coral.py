import time
import digitalio

class Coral:

    def __init__(self, uart, reset: digitalio.DigitalInOut, enable_power: digitalio.DigitalInOut):
        self.uart = uart
        self.reset = reset
        self.enable_power = enable_power
        self.turn_off() # turn Coral off if it is on
        
    def turn_on(self):
        self.enable_power.value = True
        time.sleep(1)
        self.reset.value = False # LOW
        time.sleep(1)
        self.reset.value = True # HIGH

    def turn_off(self):
        self.reset.value = False # LOW
        time.sleep(3)
        self.reset.value = True # HIGH
        self.enable_power.value = False

    @property
    def ping(self):
        # clean out the pipes
        self.uart.read(self.uart.in_waiting)

        # send a ping
        ping = b'{"command": "ping"}\n\n'
        self.uart.write(ping)

        # receive response
        if self.uart.in_waiting != len('coral says hello!'):
            return False
        else:
            print(self.uart.read(self.uart.in_waiting))
        return True