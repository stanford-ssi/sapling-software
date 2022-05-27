"""Share the PTP object. Only one task sends/recieves from the host, the
other task just looks in the inbox (queue)
"""
import usb_cdc
from async_wrappers import AsyncUARTOverUSB
from ftp import FileTransferProtocol, PacketTransferProtocol

p = AsyncUARTOverUSB(usb_cdc.data)
ptp = PacketTransferProtocol(p)
f = FileTransferProtocol(ptp.inbox, ptp.outbox)
