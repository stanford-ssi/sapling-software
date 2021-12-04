import asyncio
import serial_asyncio
import json

def ping(transport):
    transport.write('coral says hello!')

def take_picture(transport):
    transport.write('taking picture')

def send_file(transport):
    transport.write('sending file')

callbacks = {
    'ping': ping,
    'take_picture': take_picture,
    'send_file': send_file
}

buffer = b''

def parse_and_run_command(transport):
    string = buffer.decode('ascii')
    print(string)
    #packet = json.loads(string)
    #callbacks[packet['command'](transport)]

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
    coro = serial_asyncio.create_serial_connection(loop, OutputProtocol, '/dev/ttyS0', baudrate=115200)
    transport, protocol = loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main()