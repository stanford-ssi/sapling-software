# FTP test

## PyCubed

```python
import ftp
import board, busio, binascii
from pycubed import cubesat

p = busio.UART(board.PB16,board.PB17, baudrate=9600)
f = ftp.FileTransferProtocol(p)
f.receive_file('/sd/tree.png')
```

## Coral

```python
import ftp, serial, binascii
p = serial.Serial('/dev/ttyS1', baudrate=115200)
f = ftp.FileTransferProtocol(p)
f.send_file('./tree.png')
```
