#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example shows how to get general information about the device capabilities.
"""

from pr22 import DocumentReaderDevice, Event, exceptions, processing
import pr22

pr = DocumentReaderDevice()


def open_dev():
    """ Open the first document reader device. """
    print("Opening a device")
    print()

    pr.add_event_handler(Event.Connection, on_connection)
    pr.add_event_handler(Event.DeviceUpdate, on_device_update)

    try: pr.use_device(0)
    except exceptions.NoSuchDevice:
        print("No device found!")
        return 1

    print(f"The device {pr.device_name} is opened.")
    print()
    return 0


def program():
    # Devices can be manipulated only after opening.
    if open_dev() != 0: return 1

    print("SDK versions:")
    print("\tInterface:", pr.get_version('A'))
    print("\tSystem:", pr.get_version('S'))
    print()

    scannerinfo = pr.scanner.info

    # Devices provide proper image quality only if they are calibrated.
    # Devices are calibrated by default. If you receive the message "not calibrated"
    # then please contact your hardware supplier.
    print("Calibration state of the device:")
    if scannerinfo.is_calibrated():
        print("\tcalibrated")
    else:
        print("\tnot calibrated")
    print()

    print("Available lights for image scanning:")
    lights = scannerinfo.list_lights()
    for light in lights:
        print("\t", light, sep="")
    print()

    print("Available object windows for image scanning:")
    for ix in range(scannerinfo.get_window_count()):
        frame = scannerinfo.get_size(ix)
        print("\t", ix, ": ", frame[2] / 1000.0, " x ", frame[3] / 1000.0, " mm", sep="")
    print()

    print("Scanner component versions:")
    print("\tFirmware:", scannerinfo.get_version('F'))
    print("\tHardware:", scannerinfo.get_version('H'))
    print("\tSoftware:", scannerinfo.get_version('S'))
    print()

    print("Available card readers:")
    readers = pr.readers
    for ix, reader in enumerate(readers):
        info = reader.info
        print(f"\t{ix}:", info.hw_type)
        print("\t\tFirmware:", info.get_version('F'))
        print("\t\tHardware:", info.get_version('H'))
        print("\t\tSoftware:", info.get_version('S'))
    print()

    print("Available status LEDs:")
    leds = pr.peripherals.status_led_list
    for ix, led in enumerate(leds):
        print(f"\t{ix}: color", led.light)
    print()

    engineinfo = pr.engine.info

    print("Engine version:", engineinfo.get_version('E'))
    licok = ["no presence info", "not available", "present", "expired"]
    lictxt = engineinfo.required_license.name
    if engineinfo.required_license == processing.EngineLicense.MrzOcrBarcodeReading:
        lictxt = "MrzOcrBarcodeReadingL or MrzOcrBarcodeReadingF"
    print("Required license:", lictxt, "-", licok[test_license(engineinfo)])
    print("Engine release date:", engineinfo.required_license_date)
    print()

    print("Available licenses:")
    licenses = engineinfo.list_licenses()
    for ix, lic in enumerate(licenses):
        print("\t", lic, " (", engineinfo.get_license_date(lic), ")", sep="")
    print()

    print("Closing the device.")
    pr.close_device()
    return 0


def test_license(info):
    """ Test if the required OCR license is present. """
    if info.required_license == processing.EngineLicense.Unknown: return 0
    availdate = info.get_license_date(info.required_license)
    if availdate == "-": return 1
    if info.required_license_date == "-": return 2
    if availdate[0] != 'X' and availdate > info.required_license_date: return 2
    return 3


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
