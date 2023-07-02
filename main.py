import usb.core
import usb.util
import usb.backend.libusb1
import sys
import codecs
from time import sleep

VENDOR_ID = 0x0320F
PRODUCT_ID = 0x5000

BACKEND = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.so")


dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise ValueError('Device not found')

# dev.set_configuration()

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

# assert ep is not None

payload = '0x00001c001020fe8689a6ffff000000001b00001000040001000002480000000021090402002001004000040200020000000000000000003000000000000000000000000000000000004000000000000000000000000000000000005000000000000000000000000000000000006000000000'.encode()
payload_hex = codecs.encode(payload, encoding="hex", errors="strict")

dev.write(0x81, payload_hex)

sleep(0.5)

usb.util.dispose_resources(dev)
dev.attach_kernel_driver(0)