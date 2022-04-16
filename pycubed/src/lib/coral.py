import json
import board, busio

class Coral:

    def __init__(self, uart):
        self.uart = uart
        print(self.uart.read())

    @property
    def ping(self):
        ping = b'{"command": "ping"}\n\n'
        self.uart.write(ping)
        if self.uart.in_waiting != len('coral says hello!'):
            return False
        else:
            print(self.uart.read(self.uart.in_waiting))
        return True

uart = busio.UART(board.PA16, board.PA17)
coral = Coral(uart)