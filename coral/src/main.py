import asyncio
import serial_asyncio
import json
import os

def poweroff():
    os.system("poweroff")

def ping(transport):
    transport.write(b'coral says hello!')

def take_picture(transport):
    transport.write(b'taking picture')

def send_file(transport):
    transport.write(b'sending file')

class CoralCommandHandler:
    
    def __init__(self, buffsize=256):
        self.transport = None
        self.buffsize = buffsize
        self._input_buffer = bytearray()
        self.callbacks = {
            'ping': ping,
            'take_picture': take_picture,
            'send_file': send_file,
            "poweroff": poweroff
        }

    @property
    def input_buffer(self):
        return self._input_buffer

    @input_buffer.setter
    def input_buffer(self, value):
        if value > self.buffsize:
            raise BufferError('Input buffer overflow!')
        self._input_buffer = value
        if b'\n\n' in value:
            self.dispatch()
    
    # TODO add packetizer in the middle of these classes
    def dispatch(self):
        packet = self._input_buffer.decode('ascii').strip('\n')
        print(f"recieved a packet: {packet}\n")
        self._input_buffer = bytearray()
        packet = json.loads(packet)
        loop = asyncio.get_running_loop()
        loop.call_soon(self.callbacks[packet['command']], self.transport)

class OutputProtocol(asyncio.Protocol):

    def __init__(self, *args, **kwargs):
        super.__init__(args, kwargs)
        self.buffsize = 256
        self.command_handler = CoralCommandHandler(self.buffsize)

    def connection_made(self, transport):
        self.transport = transport
        self.transport.set_buffer_size(rx_size = self.buffsize, tx_size = self.buffsize)
        print('port opened, initiating handshake', transport)
        transport.serial.rts = False
        transport.write(b'Hello, World!\n')  # TODO implement handshake protocol

    def data_received(self, data):
        self.command_handler.input_buffer += data

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')


def main():

    loop = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(loop, OutputProtocol, '/dev/ttyS1', baudrate=9600)
    transport, protocol = loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main()
