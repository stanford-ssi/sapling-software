import busio
import usb_cdc
from tasko.loop import _yield_once
import gc
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
            yield #await _yield_once()
       
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
        

class AsyncQueue():

    def __init__(self, maxsize=5):
        self.maxsize = maxsize
        self.size = 0
        self.list = []

    async def put(self, item): # TODO add max len
        if self.size < self.maxsize:
            self.list.append(item)
            return True
        else:
            yield

    async def get(self):
        if len(self.list):
            val = self.list[0]
            del self.list[0]
            gc.collect()
            return val
        else:
            yield

    def qsize(self):
        return len(self.list)

    def empty(self):
        return len(self.list) == 0

class RadioProtocol:

    def __init__(self, cubesat):
        self.cubesat = cubesat

    def write(self, packet):
        num_packets = math.ceil(len(packet)/250)
        for i in range(num_packets):
            self.cubesat.radio1.send(packet[i*250:(i+1)*250])

    def readline(self):
        packet = b''
        while True:
            try:
                radio_packet = bytes(self.cubesat.radio1.receive(keep_listening=True))
                print(f"received radio packet: {radio_packet} ({type(radio_packet)})")
                if '\n' in radio_packet:
                    break
                packet += radio_packet # check this
            except TypeError:
                print(f"received empty radio packet")