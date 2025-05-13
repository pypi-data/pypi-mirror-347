#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example shows how to generate document type string.
"""

from pr22            import DocumentReaderDevice, Event, exceptions, imaging, task
from pr22.processing import FieldReference, FieldSource, FieldId
import pr22
from pr22ext         import documenttype, countrycode

pr = DocumentReaderDevice()


class StrCon:
    """ This class makes string concatenation with spaces and prefixes. """

    def __init__(self, bounder=None):
        self.cstr = (bounder+" ") if bounder else ""
        self.fstr = ""

    def __add__(self, arg):
        """  StrCon + arg """
        if arg: arg = self.cstr + arg
        if self.fstr and arg and arg[0] != ',': self.fstr += " "
        return self.fstr + arg

    def __radd__(self, arg):
        """  arg + StrCon  """
        self.fstr = arg
        return self


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

    print("Reading all the field data.")
    reading_task = task.EngineTask()
    # Specify the fields we would like to receive.
    reading_task.add(FieldSource.All, FieldId.All)

    ocr_doc = ocr_engine.analyze(doc_page, reading_task)

    print()
    print("Document code:", ocr_doc.to_variant().to_int())
    print("Document type:", get_doc_type(ocr_doc))
    print("Status:", ocr_doc.get_status())

    pr.close_device()
    return 0


def get_field_value(ocr_doc, field_id):
    ref_filter = FieldReference(FieldSource.All, field_id)
    fields = ocr_doc.list_fields(ref_filter)

    for fld in fields:
        try:
            value = ocr_doc.get_field(fld).get_best_string_value()
            if len(value) > 0: return value
        except exceptions.EntryNotFound: pass
    return ""


def get_doc_type(ocr_doc):
    document_code = ocr_doc.to_variant().to_int()
    document_type_name = documenttype.get_document_name(document_code)
    if len(document_type_name) > 0: return document_type_name

    issue_country = get_field_value(ocr_doc, FieldId.IssueCountry)
    issue_state   = get_field_value(ocr_doc, FieldId.IssueState)
    doc_type      = get_field_value(ocr_doc, FieldId.DocType)
    doc_page      = get_field_value(ocr_doc, FieldId.DocPage)
    doc_subtype   = get_field_value(ocr_doc, FieldId.DocTypeDisc)

    tmpval = countrycode.get_country_code_name(issue_country)
    if len(tmpval) > 0: issue_country = tmpval

    return issue_country + StrCon() + issue_state \
        + StrCon() +  documenttype.get_doc_type_name(doc_type) \
        + StrCon("-") + documenttype.get_page_name(doc_page) \
        + StrCon(",") + doc_subtype


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
