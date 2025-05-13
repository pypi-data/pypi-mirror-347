#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example shows how to read and process data from ECards.
After ECard selection before reading some authentication process have to
be called for accessing the data files.
"""

from fnmatch import fnmatch
from os      import path, listdir

from pr22.ecardhandling import AuthProcess, FileId, File
from pr22               import DocumentReaderDevice, Event, exceptions, imaging, task
from pr22.processing    import FieldSource, FieldId, Document, BinData
from pr22.imaging       import RawImage
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


def list_files(directory, mask):
    files = []
    if not path.isdir(directory): return []
    for fname in listdir(directory):
        fpath = directory + path.sep + fname
        if path.isdir(fpath):
            files.extend(list_files(fpath, mask))
        elif fnmatch(fname, mask):
            files.append(fpath)

    return files


def load_certificates(dirpath):
    """ Load certificates from a directory. """
    cnt = 0
    for ext in ["*.cer", "*.crt", "*.der", "*.pem", "*.crl", "*.cvcert", "*.ldif", "*.ml"]:
        for file_name in list_files(dirpath, ext):
            try:
                priv = BinData()
                if ext == "*.cvcert":
                    # Searching for private key
                    pknam = file_name[:file_name.rfind(".")+1] + "pkcs8"
                    if path.isfile(pknam): priv.load(pknam)
                pr.global_certificate_manager.load(BinData().load(file_name), priv)
                print(f'Certificate {file_name} is loaded{(" with private key." if priv.raw_size else ".")}')
                cnt += 1
            except exceptions.General:
                print(f"Loading certificate {file_name} is failed!")
    if cnt == 0: print(f"No certificates loaded from {dirpath}")
    print()


def authenticate(e_card, auth_process):
    """ Do an authentication after collecting the necessary information. """
    additional_auth_data = BinData()
    selector = 0

    if auth_process in [AuthProcess.BAC, AuthProcess.PACE, AuthProcess.BAP]:
        # Read MRZ (necessary for BAC, PACE and BAP)
        scan_task = task.DocScannerTask()
        scan_task.add(imaging.Light.Infra)
        first_page = pr.scanner.scan(scan_task, imaging.PagePosition.First)

        mrz_reading_task = task.EngineTask()
        mrz_reading_task.add(FieldSource.Mrz, FieldId.All)
        mrz_doc = pr.engine.analyze(first_page, mrz_reading_task)

        doc_field = mrz_doc.get_field(FieldSource.Mrz, FieldId.All)
        additional_auth_data.set_string(doc_field.get_raw_string_value())
        selector = 1
    elif auth_process in [AuthProcess.Passive, AuthProcess.Terminal]:
        # Load the certificates if not done yet
        pass
    elif auth_process == AuthProcess.SelectApp:
        if len(e_card.list_applications()) > 0: selector = e_card.list_applications()[0]
    else: pass
    try:
        print(f"- {auth_process} authentication ", end="", flush=True)
        e_card.authenticate(auth_process, additional_auth_data, selector)
        print("succeeded")
        return True
    except exceptions.General as ex:
        print(f"failed: {ex.message}")
        return False


def program():
    # Devices can be manipulated only after opening.
    if open_dev() != 0: return 1

    # Please set the appropriate path
    certdir = pr.get_property("rwdata_dir") + path.sep + "certs"
    load_certificates(certdir)

    card_readers = pr.readers

    # connecting to the 1st card of any reader
    selected_card = None
    card_count = 0
    print("Detected readers and cards:")
    for rdr in card_readers:
        print("\tReader:", rdr.info.hw_type)
        cards = rdr.list_cards()
        if not selected_card and len(cards) > 0:
            selected_card = rdr.connect_card(0)
        for ix, crd in enumerate(cards):
            print(f"\t\t({card_count})card: {crd}")
            card_count += 1
        print()

    if not selected_card:
        print("No card selected!")
        return 1

    print("Executing authentications:")
    current_auth = selected_card.get_next_authentication(False)
    passive_auth_implemented = False

    while current_auth != AuthProcess.NoAuth:
        if current_auth == AuthProcess.Passive:
            passive_auth_implemented = True
        auth_ok = authenticate(selected_card, current_auth)
        current_auth = selected_card.get_next_authentication(not auth_ok)
    print()

    print("Reading data:")
    files_on_selected_card = selected_card.list_files()
    if passive_auth_implemented:
        files_on_selected_card.append(File(FileId.CertDS))
        files_on_selected_card.append(File(FileId.CertCSCA))
    for file in files_on_selected_card:
        try:
            print(f"File: {file}.", end="", flush=True)
            raw_file_data = selected_card.get_file(file)
            raw_file_data.save(str(file) + ".dat")
            file_data = pr.engine.analyze(raw_file_data)
            file_data.save(Document.FileFormat.Xml).save(str(file) + ".xml")

            # Executing mandatory data integrity check for Passive Authentication
            if passive_auth_implemented:
                fdg = file
                if fdg.id_v >= int(FileId.GeneralData):
                    fdg = selected_card.convert_fileid(fdg)
                if 1 <= fdg.id_v <= 16:
                    print(" hash check...", end="", flush=True)
                    print(("OK" if selected_card.check_hash(fdg) else "failed"), end="", flush=True)

            print()
            print_doc_fields(file_data)
        except exceptions.General as ex:
            print(f" Reading failed: {ex.message}")
        print()

    print("Authentications:")
    auth_data = selected_card.get_auth_result()
    auth_data.save(Document.FileFormat.Xml).save("AuthResult.xml")
    print_doc_fields(auth_data)
    print()

    selected_card.disconnect()

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
            try: raw_value = current_field.get_raw_string_value()
            except exceptions.EntryNotFound: pass
            except exceptions.InvalidParameter: bin_value = current_field.get_binary_value()
            try: formatted_value = current_field.get_formatted_string_value()
            except exceptions.EntryNotFound: pass
            try: standardized_value = current_field.get_standardized_string_value()
            except exceptions.EntryNotFound: pass
            status = str(current_field.get_status())
            field_name = field_ref.to_string()
            if bin_value:
                print(f'  {field_name:<20}{status:<17}Binary({len(bin_value)})')
                # for cnt in range(0, len(bin_value), 16):
                #     print(print_binary(bin_value, cnt, 16))
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


if __name__ == "__main__":
    try:
        program()
    except pr22.exceptions.General as ex:
        print(ex.message)
