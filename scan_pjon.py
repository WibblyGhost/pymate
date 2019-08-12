#!/usr/bin/python
#
# Scans the Mate bus for any attached devices,
# and displays the result.
#

from pymate.matenet import MateNET, MateNETOverPJON, MateDevice
from settings import SERIAL_PORT
import logging

ch = logging.StreamHandler()

#log = logging.getLogger('mate.pjon')
#log.setLevel(logging.DEBUG)
#log.addHandler(ch)

print("MATE Bus Scan")

# Create a MateNET bus connection, connected via PJON bus
bus = MateNETOverPJON(SERIAL_PORT)

def print_device(d):
    dtype = d.scan()

    # No response from the scan command.
    # there is nothing at this port.
    if dtype is None:
        print('Port%d: -' % (
            d.port
        ))
    else:
        try:
            rev = d.revision
        except Exception as e:
            rev = str(e)

        if dtype not in MateNET.DEVICE_TYPES:
            print("Port%d: Unknown device type: %d" % (
                d.port,
                dtype
            ))
        else:
            print("Port%d: %s (Rev: %s)" % (
                d.port,
                MateNET.DEVICE_TYPES[dtype],
                rev
            ))
    return dtype

# The root device
d0 = MateDevice(bus, port=0)
dtype = d0.scan()
if not dtype:
    print('No device connected!')
    exit()
print_device(d0)

# Child devices attached to a hub
# (Only valid if the root device is a hub)
if dtype == MateNET.DEVICE_HUB:
    for i in range(1,10):
        subdev = MateDevice(bus, port=i)
        print_device(subdev)

print
print('Finished!')