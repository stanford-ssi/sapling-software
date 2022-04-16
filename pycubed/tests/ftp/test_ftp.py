# does not run in the harness yet
import ftp

host_type = ""
try:
    import board, busio
    from pycubed import cubesat
    host_type = "pycubed"
    print("pycubed detected")
except ModuleNotFoundError:
    import serial
    host_type = "coral"
    print("coral detected")
except ModuleNotFoundError:
    print("Make sure your environment is set up correctly. TODO add instructions")

f = None
p = None

if host_type == "pycubed":
    p = busio.UART(board.PB16,board.PB17)
    f = ftp.FileTransferProtocol(p)
    payload = "hello"
    if f.receive_file('/sd/tree.png', packet_length=65):
        print("successfully recieved a file!")

if host_type == "coral":
    p = serial.Serial('/dev/ttyS1')
    f = ftp.FileTransferProtocol(p)
    packet = f.send_file('./tree.png', packet_length=65)