"""Enable both console and data USB ports
"""
import usb_cdc
usb_cdc.enable(console=True, data=True)

version = "V5" # "Sapling.3"