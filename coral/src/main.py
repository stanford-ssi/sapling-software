import serial
import msgpack
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


def main():
    with serial.Serial('/dev/ttyS1', 9600, timeout=1) as uart:
    while True:
        if uart.in_waiting:
            packet = uart.read(uart.in_waiting)

if __name__ == "__main__":
    main()
