"""Share the PTP object. Only one task sends/recieves from the host, the
other task just looks in the inbox (queue)
"""
import usb_cdc
from ftp import PacketTransferProtocol

p = usb_cdc.data
f = ftp.PacketTransferProtocol(p)
