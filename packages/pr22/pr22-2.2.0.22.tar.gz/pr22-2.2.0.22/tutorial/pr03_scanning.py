#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example shows how to parametrize the image scanning process.
"""

import time

from pr22       import DocumentReaderDevice, Event, exceptions, imaging
from pr22.processing import Document
from pr22.task       import DocScannerTask, FreerunTask
from pr22.imaging    import RawImage
import pr22

pr = DocumentReaderDevice()
doc_present = None
MAX_WAIT_SEC = 15


def open_dev():
    """ Open the first document reader device. """
    print("Opening a device")
    print()

    pr.add_event_handler(Event.Connection, on_connection)
    pr.add_event_handler(Event.DeviceUpdate, on_device_update)

    try: pr.use_device(0)
    except  exceptions.NoSuchDevice:
        print("No device found!")
        return 1

    print(f"The device {pr.device_name} is opened.")
    print()
    return 0


def program():
    global doc_present
    print("This tutorial guides you through a complex image scanning process.")
    print("This will demonstrate all possible options of page management.")
    print("The stages of the scan process will be saved into separate zip files")
    print("in order to provide the possibility of comparing them to each other.")
    print()

    # Devices can be manipulated only after opening.
    if open_dev() != 0: return 1

    # Subscribing to scan events
    pr.add_event_handler(Event.ScanStarted, on_scan_started)
    pr.add_event_handler(Event.ImageScanned, on_image_scanned)
    pr.add_event_handler(Event.ScanFinished, on_scan_finished)
    pr.add_event_handler(Event.DocFrameFound, on_doc_frame_found)
    pr.add_event_handler(Event.PresenceDetection, on_doc_state_changed)

    scanner = pr.scanner

    live_task = scanner.start_task(FreerunTask.detection())

    # first page
    try:
        first_task = DocScannerTask()

        print("At first the device scans only a white image...")
        first_task.add(imaging.Light.White)
        page1 = scanner.scan(first_task, imaging.PagePosition.First)

        print("And then the program saves it as a PNG file.")
        page1.select(imaging.Light.White).get_image().save(RawImage.FileFormat.Png).save("original.png")

        print("Saving stage 1.")
        pr.engine.get_root_document().save(Document.FileFormat.Zipped).save("1stScan.zip")
        print()

        print("If scanning of an additional infra image of the same page is required...")
        print("We need to scan it into the current page.")
        first_task.add(imaging.Light.Infra)
        scanner.scan(first_task, imaging.PagePosition.Current)

        try:
            print("If a cropped image of the document is available")
            print(" then the program saves it as a PNG file.")
            scanner.get_page(0).select(imaging.Light.White).doc_view().get_image().save(
                RawImage.FileFormat.Png).save("document.png")
        except exceptions.ImageProcessingFailed:
            print("Cropped image is not available!")

        print("Saving stage 2.")
        pr.engine.get_root_document().save(Document.FileFormat.Zipped).save("2ndScan.zip")
        print()
    finally: pass

    # second page
    try:
        print("At this point, if scanning of an additional page of the document is needed")
        print("with all of the available lights except the infra light.")
        print("It is recommended to execute in one scan process")
        print(" - as it is the fastest in such a way.")
        print()

        second_task = DocScannerTask()
        second_task.add(imaging.Light.All).remove(imaging.Light.Infra)

        doc_present = False
        print("At this point, the user has to change the document on the reader.")
        for ix in range(MAX_WAIT_SEC * 10):
            if doc_present: break
            time.sleep(0.1)

        print("Scanning the images.")
        scanner.scan(second_task, imaging.PagePosition.Next)

        print("Saving stage 3.")
        pr.engine.get_root_document().save(Document.FileFormat.Zipped).save("3rdScan.zip")
        print()

        print("Upon putting incorrect page on the scanner, the scanned page has to be removed.")
        scanner.cleanup_last_page()

        doc_present = False
        print("And the user has to change the document on the reader again.")
        for ix in range(MAX_WAIT_SEC * 10):
            if doc_present: break
            time.sleep(0.1)

        print("Scanning...")
        scanner.scan(second_task, imaging.PagePosition.Next)

        print("Saving stage 4.")
        pr.engine.get_root_document().save(Document.FileFormat.Zipped).save("4thScan.zip")
        print()
    finally: pass

    live_task.stop()

    print("Scanning processes are finished.")
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


def on_scan_started(page, dr_dev):
    print("Scan started. Page:", page)


def on_image_scanned(page, light, dr_dev):
    print(f"Image scanned. Page: {page} Light: {light}")
    fnam = f"page_{page}_light_{light}.bmp"
    dr_dev.scanner.get_page(page).select(light).get_image().save(RawImage.FileFormat.Bmp).save(fnam)


def on_scan_finished(page, status, dr_dev):
    print("Page scanned. Page:", page, "Status:", status)


def on_doc_frame_found(page, dr_dev):
    print("Document frame found. Page:", page)


def on_doc_state_changed(state, dr_dev):
    global doc_present
    if state == pr22.util.PresenceState.Present: doc_present = True


if __name__ == "__main__":
    try:
        program()
    except pr22.exceptions.General as ex:
        print(ex.message)
