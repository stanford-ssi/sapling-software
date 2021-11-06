# serial util, pycubed side

import busio
from pycubed import cubesat
import usb_cdc

host = usb_cdc.console # stdin/stdout
host.timeout = 3

def main():
    f = None
    counter = 0
    while True:
        # perhaps try deinitializingt he uart and then reinitializing with baudrate 115200
        command = host.read(256).decode('ascii')
        host.write(b"hello from pycubed\n")
        # command = "send_me_the_fileXXXtree.jpgZZZ"
        if command.find('send_me_the_file') != -1:
            if f is None:
                begin = command.find("XXX") + len('XXX')
                end = command.find("ZZZ")
                filename = command[begin:end]
                f = open(f'/sd/{filename}', 'rb')
                # catch errors here (file not found, read only, etc.)
                host.write(b"BEGINNING_OF_FILE")
            else:
                chunk = f.read(4096)
                counter += 1
                # insert file integrity assert here for re-requesting
                host.write(chunk)
                if len(chunk) < 4096:
                    break
        else:
            pass
    f.close()

main()