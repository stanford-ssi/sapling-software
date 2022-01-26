class Coral:

    def __init__(self, uart):
        self.uart = uart
        self.uart.timeout = 5

    def request(self):
        self.uart.write(bytes)
        return self.uart.read()