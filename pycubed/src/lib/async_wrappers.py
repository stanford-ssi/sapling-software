import busio
import usb_cdc
from tasko.loop import _yield_once
import gc
import math

class AsyncUART():

    def __init__(self, serial_conn):
        """
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

class AsyncUARTOverUSB():

    def __init__(self, serial_conn):
        """
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


class RadioProtocol:

    def __init__(self, radio):
        self.radio = radio

    def write(self, packet):
        # break into < 250 characters
        num_packets = math.ceil(len(packet)/250)
        if num_packets != 1:
            print("TRYING TO SEND MPP")
        for i in range(num_packets):
            self.radio.send(packet[i*250:(i+1)*250])

    async def readline(self):
        packet = b''
        while True:
            radio_packet = await self.radio.await_rx()
            if not radio_packet:
                yield
                continue
            print(f"received radio packet: {radio_packet}") # ({type(radio_packet)})")
            if '\n' in radio_packet:
                break
            else:
                print("RCVD PKT W/O \n")
            packet += radio_packet # check this
        return packet

    def readline_sync(self):
        packet = self.radio.receive(timeout=10)
        return packet
        

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

