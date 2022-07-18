"""Share the PTP object. Only one task sends/recieves from the host, the
other task just looks in the inbox (queue)
"""
import usb_cdc
from async_wrappers import AsyncUARTOverUSB
from ptp import AsyncPacketTransferProtocol

protocol = AsyncUARTOverUSB(usb_cdc.data)
aptp = AsyncPacketTransferProtocol(protocol)
