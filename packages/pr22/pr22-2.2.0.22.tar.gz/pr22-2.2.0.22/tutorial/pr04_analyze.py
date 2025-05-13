#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example shows the main capabilities of the image processing analyzer function.
"""

from pr22            import DocumentReaderDevice, Event, exceptions, imaging, task
from pr22.processing import FieldSource, FieldId, Document
from pr22.imaging    import RawImage
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

    # Subscribing to scan events
    pr.add_event_handler(Event.ScanStarted, on_scan_started)
    pr.add_event_handler(Event.ImageScanned, on_image_scanned)
    pr.add_event_handler(Event.ScanFinished, on_scan_finished)
    pr.add_event_handler(Event.DocFrameFound, on_doc_frame_found)

    scanner = pr.scanner
    ocr_engine = pr.engine

    print("Scanning some images to read from.")
    scan_task = task.DocScannerTask()
    # For OCR (MRZ) reading purposes, IR (infrared) image is recommended.
    scan_task.add(imaging.Light.White).add(imaging.Light.Infra)
    doc_page = scanner.scan(scan_task, imaging.PagePosition.First)
    print()

    print("Reading all the field data of the Machine Readable Zone.")
    mrz_reading_task = task.EngineTask()
    # Specify the fields we would like to receive.
    mrz_reading_task.add(FieldSource.Mrz, FieldId.All)
    mrz_doc = ocr_engine.analyze(doc_page, mrz_reading_task)

    print()
    print_doc_fields(mrz_doc)
    # Returned fields by the analyze() method can be saved to an XML file:
    mrz_doc.save(Document.FileFormat.Xml).save("MRZ.xml")

    print("Scanning more images for VIZ reading and image authentication.")
    # Reading from VIZ -except face photo- is available in special OCR engines only.
    scan_task.add(imaging.Light.All)
    doc_page = scanner.scan(scan_task, imaging.PagePosition.Current)
    print()

    print("Reading all the textual and graphical field data as well as",
          "authentication result from the Visual Inspection Zone.")
    viz_reading_task = task.EngineTask()
    viz_reading_task.add(FieldSource.Viz, FieldId.All)
    viz_doc = ocr_engine.analyze(doc_page, viz_reading_task)

    print()
    print_doc_fields(viz_doc)
    viz_doc.save(Document.FileFormat.Xml).save("VIZ.xml")

    print("Reading barcodes.")
    bc_reading_task = task.EngineTask()
    bc_reading_task.add(FieldSource.Barcode, FieldId.All)
    bcr_doc = ocr_engine.analyze(doc_page, bc_reading_task)

    print()
    print_doc_fields(bcr_doc)
    bcr_doc.save(Document.FileFormat.Xml).save("BCR.xml")

    pr.close_device()
    return 0


def print_binary(arr, pos, szv, split=True):
    """ Print a hexa dump line from a part of an array into a string.

    :param arr:     The whole array.
    :param pos:     Position of the first item to print.
    :param szv:     Number of items to print.
    :param split:   Put extra space character to middle of hex array and
                    between hex and ascii values.
    """
    str1, str2, epos = "", "", min(len(arr), pos+szv)
    for p0v in range(pos, epos):
        str1 += f"{arr[p0v] & 0xff:02x} "
        str2 += chr(arr[p0v]) if 0x21 <= arr[p0v] <= 0x7e else "."

    for p0v in range(epos, pos+szv):
        str1 += "   "
        str2 += " "
    if split:
        str1 = str1[:szv//2*3] + " " + str1[szv//2*3:] + " "
    return str1 + str2


def print_doc_fields(doc):
    """ Print out all fields of a document structure to console.

    Values are printed in three different forms: raw, formatted and standardized.
    Status (checksum result) is printed together with fieldname and raw value.
    At the end, images of all fields are saved into png format.
    """
    fields = doc.list_fields()

    print(f'  {"FieldId":<20}{"Status":<17}{"Value"}')
    print(f'  {"-------":<20}{"------":<17}{"-----"}')
    print()

    for field_ref in fields:
        try:
            current_field = doc.get_field(field_ref)
            raw_value = formatted_value = standardized_value = ""
            bin_value = None
            try: raw_value          = current_field.get_raw_string_value()
            except exceptions.EntryNotFound: pass
            except exceptions.InvalidParameter: bin_value = current_field.get_binary_value()
            try: formatted_value    = current_field.get_formatted_string_value()
            except exceptions.EntryNotFound: pass
            try: standardized_value = current_field.get_standardized_string_value()
            except exceptions.EntryNotFound: pass
            status = str(current_field.get_status())
            field_name = field_ref.to_string()
            if bin_value:
                print(f'  {field_name:<20}{status:<17}{"Binary"}')
                for cnt in range(0, len(bin_value), 16):
                    print(print_binary(bin_value, cnt, 16))
            else:
                print(f'  {field_name:<20}{status:<17}[{raw_value}]')
                print(f'\t{"   - Formatted   ":<31}[{formatted_value}]')
                print(f'\t{"   - Standardized":<31}[{standardized_value}]')

            stlist = current_field.get_detailed_status()
            for stv in stlist: print(stv)

            try: current_field.get_image().save(RawImage.FileFormat.Png).save(field_name+".png")
            except exceptions.General: pass
        except exceptions.General: pass
    print()

    comp_list = doc.get_field_compare_list()
    for comp in comp_list:
        print(f"Comparing {comp.field1} vs. {comp.field2} results {comp.confidence}")
    print()


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


def on_scan_finished(page, status, dr_dev):
    print("Page scanned. Page:", page, "Status:", status)


def on_doc_frame_found(page, dr_dev):
    print("Document frame found. Page:", page)


if __name__ == "__main__":
    try:
        program()
    except pr22.exceptions.General as ex:
        print(ex.message)
