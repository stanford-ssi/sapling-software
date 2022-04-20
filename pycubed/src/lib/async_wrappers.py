import busio
import usb_cdc
from tasko.loop import _yield_once

class AsyncUART(busio.UART):

    def __init__(self, *args, **kwargs):
        super(AsyncUART, self).init(args, kwargs)

    async def readline(self):
        """Yields if there are no characters waiting.
        TODO: reimplement so that it yields if there is a gap in
        characters recieved while reading a line.

        Returns:
            (): line of data
        """
        while not self.in_waiting:
            _yield_once()
       
        return super().readline()

class AsyncUARTOverUSB():

    def __init__(self, serial_conn):
        """TODO: figure out how to create child object from object of parent 
        class

        Args:
            serial_conn (_type_): _description_
        """
        self.serial_conn = serial_conn

    async def readline(self):
        """Yields if there are no characters waiting.
        TODO: reimplement so that it yields if there is a gap in
        characters recieved while reading a line.

        Returns:
            (): line of data
        """
        while not self.serial_conn.in_waiting:
            yield
        
        line = self.serial_conn.readline()
        return line

    def write(self, data):
        self.serial_conn.write(data)
        