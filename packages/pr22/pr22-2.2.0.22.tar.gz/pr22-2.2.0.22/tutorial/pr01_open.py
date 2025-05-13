#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example shows the possibilities of opening a device.
The following tutorials show the easy way of opening in their open_dev() methods.
"""

import pr22.exceptions
from pr22 import DocumentReaderDevice, Event

pr = DocumentReaderDevice()


def program():
    # To open more than one device simultaneously, create more DocumentReaderDevice objects
    print("Opening system")
    print()

    pr.add_event_handler(Event.Connection, on_connection)
    pr.add_event_handler(Event.DeviceUpdate, on_device_update)

    devicelist = pr.list_devices(pr)

    if not devicelist:
        print("No device found!")
        return 0

    print(len(devicelist), "device" + ("s" if len(devicelist) > 1 else ""), "found.")
    for device in devicelist:
        print("  Device:", device)
    print()

    print('Connecting to the first device by its name:', devicelist[0])
    print()
    print('If this is the first usage of this device on this PC,')
    print('the "calibration file" will be downloaded from the device.')
    print('This can take a while.')
    print()

    pr.use_device(devicelist[0])

    print('The device is opened.')

    print('Closing the device.')
    pr.close_device()
    print()

    # Opening the first device without using any device lists.

    print("Connecting to the first device by its ordinal number: 0")

    pr.use_device(0)

    print("The device is opened.")

    print("Closing the device.")
    pr.close_device()
    return 0


def on_connection(devno, dr_dev):
    print(f"Connection event. Device number: {devno}")


def on_device_update(part, dr_dev):
    print("Update event.")
    if   part == 1: print("  Reading calibration file from device.")
    elif part == 2: print("  Scanner firmware update.")
    elif part == 4: print("  RFID reader firmware update.")
    elif part == 5: print("  License update.")
    else:          print(f"  Device update {part}")


if __name__ == "__main__":
    try:
        program()
    except pr22.exceptions.General as ex:
        print(ex.message)
