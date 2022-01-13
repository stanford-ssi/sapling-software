import asyncio
import serial_asyncio
import json
import os

def poweroff():
    os.system("sudo poweroff")

def ping(transport):
    transport.write(b'coral says hello!')

def take_picture(transport):
    transport.write(b'taking picture')

def send_file(transport):
    transport.write(b'sending file')

callbacks = {
    'ping': ping,
    'take_picture': take_picture,
    'send_file': send_file,
    'poweroff': poweroff
}

buffer = b''

def parse_and_run_command(transport):
    global buffer
    string = buffer.decode('ascii').strip('\n')
    print(f"{string}\n")
    packet = json.loads(string)
    callbacks[packet['command']](transport)
    buffer = b''

class OutputProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        global buffer
        buffer += data
        if b'\n\n' in data:
            parse_and_run_command(self.transport)

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
