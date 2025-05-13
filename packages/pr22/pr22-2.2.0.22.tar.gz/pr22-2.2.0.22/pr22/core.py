#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controller classes of device modules.

Use these classes directly from pr22 package.
"""

__version__ = '2.2.0.22'

import threading
import traceback
from platform      import system
from ctypes        import c_wchar_p, c_int, c_void_p, pointer, cast, POINTER, Structure
from typing        import Callable

from pr22.ecardhandling import AuthProcess, Certificates, File, Application
from pr22.exceptions    import ErrorCodes
from pr22.prins    import GxModule, PrApi, CommonApi, CertScope, GxMem, ImageType
from pr22.types    import PrEnum, chk_ver

from pr22 import exceptions, util, control, processing, imaging, ecardhandling, task
chk_ver(__version__)

if system() == 'Linux':
    from ctypes import CFUNCTYPE
    EVTFUNC = CFUNCTYPE(None, c_int, c_int, c_int, c_void_p)
if system() == 'Windows':
    from ctypes import WINFUNCTYPE
    EVTFUNC = WINFUNCTYPE(None, c_int, c_int, c_int, c_void_p)

__all__ = ['Event', 'Peripherals', 'DocScanner', 'Engine', 'ECard',
           'ECardReader', 'DocumentReaderDevice']


class Event(PrEnum):
    """ Event types.

    The PreviewCaptured and PresenceStateChanged events occur only if
    the appropriate task.FreerunTask has been started.
    """
    UVLedWarming      =  0,   """Occurs when UV tube warming started."""
    ScanFinished      =  1,   """Occurs when a scanning task is finished.

                                 parameters: page_no, error_code, pr_dev
                                 """
    ImageScanned      =  2,   """Occurs when an image is scanned.

                                 parameters: page_no, light_id, pr_dev
                                 """
    ScanStarted       =  3,   """Occurs when scanning of a page is started.

                                 parameters: page_no, pr_dev
                                 """
    NoImageInfo       =  4,   """Occurs when no image captured because it contains no
                                 information."""
    PreviewCaptured   =  5,   """Occurs when a preview (live) image is captured.

                                 parameters: pr_dev
                                 """
    PresenceDetection =  6,   """Occurs when the state of the presence detection is changed.

                                 parameters: presence_state, pr_dev
                                 """
    Button            =  7,   """Occurs when a button of the device is pressed or released.

                                 parameters: key_code, key_state, pr_dev
                                 """
    Power             =  8,   """Occurs when the state of the power is changed.

                                 parameters: pwr_state, rfu, pr_dev
                                 """
    Connection        =  9,   """Occurs when the used device is disconnected, or when the number
                                 of devices is changed while no device is used.

                                 parameters: dev_no     Positive  for connection,  negative  for
                                                        disconnection, 0 for non changed.
                                             pr_dev
                                 """
    DocFrameFound     = 10,   """Occurs when a new cropped document image is available.

                                 parameters: page_no, pr_dev
                                 """
    AuthBegin         = 12,   """Occurs when an authentication task of an ECard is started.

                                 parameters: auth_proc, pr_dev
                                 """
    AuthWaitForInput  = 13,   """Occurs when an authentication task of an ECard is waiting for
                                 some input data.

                                 parameters: auth_proc, pr_dev
                                 """
    AuthFinished      = 14,   """Occurs when an authentication task of an ECard is finished.

                                 parameters: auth_proc, error_code, pr_dev
                                 """
    ReadBegin         = 15,   """Occurs when a reading task of an ECard is started.

                                 parameters: file_id, pr_dev
                                 """
    ReadFinished      = 16,   """Occurs when a reading task of an ECard is finished.

                                 parameters: file_id, error_code, pr_dev
                                 """
    FileChecked       = 17,   """Occurs when a file hash checking task of an ECard is finished.

                                 parameters: file_id, error_code, pr_dev
                                 """
    DeviceUpdate      = 18,   """Occurs when reading or writing of a file stored on the device is
                                 started.

                                 parameters: part, pr_dev
                                 """


class Peripherals:
    """ Peripheral controller device component.

    Related classes are defined in the control module.
    """

    Information = control.DeviceInformation
    Information.__doc__ = """ See control.Information for details. """

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        self.prapi = api_handle

    def __str__(self):
        """ Return the name of the device. """
        try:    return self.to_string()
        except exceptions.General: return ''

    def to_string(self):
        """ Return the name of the device.

        :return:        Device name string.
        """
        return self.info.device_name

    @property
    def info(self):
        """ The device Information data. """
        return Peripherals.Information(self.prapi)

    @property
    def power_control(self):
        """ The PowerControl component of the device. """
        return control.PowerControl(self.prapi)

    @property
    def status_led_list(self):
        """ List of the controllable StatusLed-s. """
        leds = []
        try:
            int_arr = self.info.to_variant().get_child(
                                util.VariantId.StatledList, 0).to_int_array()
            for ix, val in enumerate(int_arr):
                leds.append(control.StatusLed(self.prapi, val, 1 << ix))
        finally:
            return leds

    @property
    def user_data(self):
        """ The UserData storage controller component. """
        return control.UserData(self.prapi)


class DocScanner:
    """ Document scanner component. """

    Information = imaging.ScannerInformation
    Information.__doc__ = """See imaging.ScannerInformation for details."""

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        self.prapi = api_handle

    @property
    def info(self):
        """ The scanner Information data. """
        return DocScanner.Information(self.prapi)

    def get_page(self, page_index):
        """ Return a previously scanned page.

        :param page_index:  Ordinal number of the requested page.
        :return:            A processing.Page value.
        """
        param = DocScanner._StprGetDocumentRootV(None)
        self.prapi.api_call(PrApi.GetDocRootV, param)
        path = f"C,D={c_int(util.VariantId.PageList).value}/L,X={page_index}"
        with util.Variant(param.document) as root_doc, root_doc.get_item_by_path(
                path) as image_list:
            return processing.Page(self.prapi, page_index, image_list)

    def scan(self, scan_task, page_pos):
        """ Take images from an object window of the scanner.

        :param scan_task:   List of lights and the object window Id in a
                            task.DocScannerTask value.
        :param page_pos:    An imaging.PagePosition target page selector
                            value.
        :return:            A processing.Page value  containing the list
                            of the scanned images.
        """
        lights_no = len(scan_task.lights)
        light_array = (c_int * lights_no)()
        for ix in range(lights_no): light_array[ix] = int(scan_task.lights[ix])

        param = DocScanner._StprStartScanning(cast(pointer(light_array), POINTER(c_int)),
                          lights_no, scan_task.object_window, int(page_pos), 0)

        self.prapi.api_call(PrApi.Scan, param)
        page_num = self.prapi.get_property("act_page")
        return self.get_page(int(page_num))

    def start_scanning(self, scan_task, page_pos):
        """
        Take images from an object window of the scanner in a background
        thread.

        After the process is finished the TaskControl.wait() method must
        be called.

        :param scan_task:   List of lights and the object window Id in a
                            task.DocScannerTask value.
        :param page_pos:    An imaging.PagePosition target page selector
                            value.
        :return:            A task.TaskControl object.
        """
        lights_no = len(scan_task.lights)
        light_array = (c_int * lights_no)()
        for ix in range(lights_no): light_array[ix] = int(scan_task.lights[ix])

        param = DocScanner._StprStartScanning(cast(pointer(light_array), POINTER(c_int)),
                                   lights_no, scan_task.object_window, int(page_pos), 0)

        self.prapi.api_call(PrApi.StartScanning, param)
        return task.TaskControl(self.prapi, param.reqid)

    def start_task(self, freerun_task):
        """ Start a task declared by the freerun_task parameter.

        After the process is finished the TaskControl.wait() method must
        be called.

        :param freerun_task:    The task.FreerunTask to start.
        :return:                A task.TaskControl object.
        """
        opp = DocScanner._StprProcess(int(freerun_task.task), 0)
        self.prapi.api_call(CommonApi.StartFrvTask, opp)
        return task.TaskControl(self.prapi, opp.ProcessId)

    def cleanup_data(self):
        """
        Remove all the internally  stored data (images, documents)  from
        the system.
        """
        param = DocScanner._StprResetDocument(0)
        self.prapi.api_call(PrApi.ResetDocument, param)

    def cleanup_last_page(self):
        """
        Remove the  internally stored  data (images,  documents)  of the
        last page from the system.
        
        Removing the last page is useful  when a wrong page has scanned,
        e.g. because the scanned image  is blurred or accidentally wrong
        document page has been scanned.
        """
        param = DocScanner._StprResetDocument(1)
        self.prapi.api_call(PrApi.ResetDocument, param)

    def load_document(self, buffer):
        """ Load the data of a "Root document" saved earlier.

        This method  removes  all the  internally  stored data  (images,
        documents) from the system.
        See Document.save()

        :param buffer:      The processing.BinData to load.
        :return:            Root  processing.Document object  represents
                            all the loaded data.
        """
        param = DocScanner._StprLoadDocumentFromMem(None, cast(buffer.raw_data, c_void_p),
                                         buffer.raw_size)
        self.prapi.api_call(PrApi.LoadDocumentFromMem, param)
        with util.Variant(param.doc) as root_doc:
            return processing.Document(self.prapi, root_doc)

    def get_preview(self):
        """ Return the last captured preview image.

        To get preview images a FreerunTask.live_stream() task should be
        started before.

        :return:            The requested imaging.RawImage.
        """
        param = DocScanner._StprGetImage(Type=ImageType.Preview)
        self.prapi.api_call(PrApi.GetImage, param)
        with util.Variant(param.Img) as var:
            return imaging.RawImage().from_variant(var)

    class _StprResetDocument(Structure):        # pylint: disable=R0903
        _fields_ = [("lastpage", c_int)]

    class _StprGetDocumentRootV(Structure):  # pylint: disable=R0903
        _fields_ = [("document", util.st_gxVARIANT)]

    class _StprStartScanning(Structure):    # pylint: disable=R0903
        _fields_ = [("lights", POINTER(c_int)), ("nlight", c_int), ("window", c_int),
                    ("position", c_int), ("reqid", c_int)]

    class _StprProcess(Structure):          # pylint: disable=R0903
        _fields_ = [("ProcessId", c_int), ("Status", c_int)]

    class _StprLoadDocumentFromMem(Structure):  # pylint: disable=R0903
        _fields_ = [("doc", util.st_gxVARIANT), ("buffer", c_void_p), ("buflen", c_int)]

    class _StprGetImage(Structure):         # pylint: disable=R0903
        _fields_ = [("Page", c_int), ("Light", c_int), ("Type", c_int),
                    ("Img", util.st_gxVARIANT)]


class Engine:
    """ Data analyzer component. """

    Information = processing.EngineInformation
    Information.__doc__ = """See processing.EngineInformation for details."""

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        self.prapi = api_handle

    @property
    def info(self):
        """ The engine Information data. """
        return Engine.Information(self.prapi)

    def analyze(self, par1, engine_task=None):
        """ Analyze already scanned images or some binary data.

        Analyze images  of an already  scanned document page  or a given
        binary data  and return  textual and  logical data  according to
        task.

        :param par1:        A processing.Page object referencing scanned
                            images,   or  a  processing.BinData   object
                            storing an ecard file or MRZ data.
        :param engine_task: Specifies  data field references  to analyze
                            in task.EngineTask structure. This parameter
                            is omitted in case of analyzing binary data.
        :return:            The result processing.Document structure.
        """
        if isinstance(par1, processing.Page):
            return par1.analyze(engine_task)

        param = Engine._StprAnalyzeC(cast(par1.raw_data, c_void_p),
                              par1.raw_size, None, par1.comment)
        self.prapi.api_call(PrApi.AnalyzeC, param)
        with util.Variant(param.doc) as doc:
            return processing.Document(self.prapi, doc)

    def generate_latent_image(self, image, dec_param):
        """ Generate a decoded IPI image for visual inspection.

        This method has the same role as
                            DocImage.generate_latent_image().

        :param image:       Source imaging.DocImage.
        :param dec_param:   IPI image decoding parameters in a str.
        :return:            A generated imaging.RawImage.
        """
        return image.generate_latent_image(dec_param)

    def read_field(self, image, read_param):
        """ Read character or barcode data from an image.

        This method has the same role as DocImage.read_field().

        :param image:       The input imaging.DocImage to read from.
        :param read_param:  Reading  parameters in a  util.Variant which
                            are   described   in   the  Passport  Reader
                            reference manual.
        :return:            A processing.Document result structure.
        """
        return image.read_field(read_param)

    def get_root_document(self):
        """ Return the "Root Document" containing all data to save.

        See Document.get_part()

        :return:            A processing.Document data structure.
        """
        param = Engine._StprGetDocumentRootV(None)
        self.prapi.api_call(PrApi.GetDocRootV, param)
        with util.Variant(param.document) as root_doc:
            return processing.Document(self.prapi, root_doc)

    class _StprAnalyzeC(Structure):     # pylint: disable=R0903
        _fields_ = [("buffer", c_void_p), ("bufflen", c_int),
                    ("doc", util.st_gxVARIANT), ("comment", c_wchar_p)]

    class _StprGetDocumentRootV(Structure):  # pylint: disable=R0903
        _fields_ = [("document", util.st_gxVARIANT)]


class ECard:
    """
    Electronically readable card (Contact Smartcard, RFID card or
    Magnetic stripe card).
    """

    Information = ecardhandling.CardInformation
    Information.__doc__ = """See ecardhandling.CardInformation for details."""

    def __init__(self, api_handle, serial_no=""):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.serial_no = serial_no
        self.auth_data = None

    @property
    def info(self):
        """ The card Information data. """
        return ECard.Information(self.prapi, self.serial_no)

    def get_auth_reference_data(self):
        """ Return data necessary for the next authentication process.

        :return:        A processing.BinData structure.
        """
        return self.auth_data

    def disconnect(self):
        """ Finish usage of the card. """
        param = ECard._StprRfidCard(self.serial_no)
        self.prapi.api_call(PrApi.DisconnectRfidCard, param)

    def list_applications(self):
        """ Return a list of available ecard applications.

        When the list is empty  or contains only Application.NoApp  that
        means that the list  cannot be requested from the card,  and the
        system should try to probe applications on card.

        :return:        A list of ecardhandling.Application values.
        """
        param = ECard._StprRfidGetApps(Card=self.serial_no)
        self.prapi.api_call(PrApi.GetApplications, param)
        return GxMem.to_list(Application.parse, param.Apps, param.nApps)

    def list_files(self):
        """ Return a list of available files on the ecard.

        :return:        A list of ecardhandling.File values.
        """
        param = ECard._StprRfidGetFiles(Card=self.serial_no)
        self.prapi.api_call(PrApi.GetFileList, param)
        return GxMem.to_list(File, param.Files, param.nFiles)

    def get_file(self, file):
        """ Return the data of a file.

        :param file:    An ecardhandling.File or FileId value.
        :return:        A processing.BinData structure.
        """
        file = file.id_v if isinstance(file, File) else int(file)
        param = ECard._StprRfidGetFile(self.serial_no, file)
        self.prapi.api_call(PrApi.GetRfidFile, param)

        bdp = processing.BinData.from_gx(param.data, param.sdata)
        bdp.comment = self.serial_no + ":" + str(file)
        return bdp

    def check_hash(self, file):
        """ Check the integrity of a file.

        :param file:    An ecardhandling.File or FileId value.
        :return:        True/False value.
        """
        file = file.id_v if isinstance(file, File) else int(file)
        param = ECard._StprCheckRfidFileHash(self.serial_no, file)

        try:
            self.prapi.api_call(PrApi.CheckFileHash, param)
        except exceptions.General:
            return False
        return True

    def get_next_authentication(self, force_next):
        """
        Return the  identifier of the  next suggested  authentication to
        proceed.

        :param force_next:  Skip the next authentication  and return the
                            one suggested after that.
        :return:            An ecardhandling.Authentication identifier.
        """
        param = ECard._StprGetNextAuth(self.serial_no, 0, (1 if force_next else 0))
        self.prapi.api_call(PrApi.GetNextAuth, param)
        return AuthProcess.parse(param.ProcessName)

    def authenticate(self, authentication, additional_data, selector):
        """ Execute an authentication process.

        In  some  special  cases,   additional  system   information  is
        necessary for computing additional_data parameter.  These pieces
        of information can be requested by the get_auth_reference_data()
        method.

        :param authentication:  An ecardhandling.Authentication value.
        :param additional_data: Data  needed  for  authentication  in  a
                                processing.BinData structure.
        :param selector:        Selector parameter for certain
                                authentications.
        """
        if authentication == AuthProcess.InitTerminal:
            param = ECard._StprTerminalAuth(Card=self.serial_no)
            self.prapi.api_call(PrApi.InitTerminalAuth, param)
            self.auth_data = processing.BinData.from_gx(param.Data, param.Sdata)
        else:
            param = ECard._StprDoAuthentication(self.serial_no, authentication,
                                                None, 0, selector)
            # pylint: disable=W0201

            if authentication == AuthProcess.CompleteTerminal:
                param.lines = additional_data.raw_size
                param.authdata = cast(additional_data.raw_data, c_void_p)
            else:
                param.lines = 1
                tmpptr = cast(additional_data.raw_data, c_void_p)
                tmpptr = pointer(tmpptr)
                param.authdata = cast(tmpptr, c_void_p)
            self.prapi.api_call(PrApi.DoAuth, param)

    @property
    def certificate_manager(self):
        """
        The certificate manager that stores certificates for the current
        ECard only.

        The value is an ecardhandling.Certificates object.
        """
        return Certificates(self.prapi, CertScope.Card, self.serial_no)

    def convert_fileid(self, file):
        """
        Convert file identifier values: general IDs to data group number
        and vice versa.

        :param file:    File Id  to convert.  An  ecardhandling.File  or
                        FileId value.
        :return:        Converted file Id in an ecardhandling.File data.
        """
        file = file.id_v if isinstance(file, File) else int(file)
        param = ECard._StprConvertFileNames(self.serial_no, file)
        self.prapi.api_call(PrApi.ConvertFileNames, param)
        return File(param.Fid)

    def get_auth_result(self):
        """ Return the ECard authentication results in document form.

        :return:        A processing.Document data structure.
        """
        param = ECard._StprRfidGetAuthResult(self.serial_no, None)
        self.prapi.api_call(PrApi.GetAuthResult, param)
        with util.Variant(param.Doc) as doc:
            return processing.Document(self.prapi, doc)

    @property
    def serial(self):
        """ Serial number of the card.

        In numerous cases,  the serial number  is random.  In some other
        cases,  cards have no serial at all.  For such cards, the system
        generates a fictional number.
        """
        return self.serial_no

    class _StprRfidCard(Structure):         # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p)]

    class _StprRfidGetApps(Structure):      # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("Apps", POINTER(c_int)), ("nApps", c_int)]

    class _StprRfidGetFiles(Structure):     # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("Files", POINTER(c_int)), ("nFiles", c_int)]

    class _StprRfidGetFile(Structure):      # pylint: disable=R0903
        _fields_ = [("card", c_wchar_p), ("fileid", c_int),
                    ("data", c_void_p), ("sdata", c_int)]

    class _StprCheckRfidFileHash(Structure):  # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("FileId", c_int)]

    class _StprGetNextAuth(Structure):      # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("ProcessName", c_int), ("ForceNext", c_int)]

    class _StprTerminalAuth(Structure):  # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("Data", c_void_p), ("Sdata", c_int)]

    class _StprDoAuthentication(Structure):  # pylint: disable=R0903
        _fields_ = [("card", c_wchar_p), ("processname", c_int), ("authdata", c_void_p),
                    ("lines", c_int), ("passwordtype", c_int)]

    class _StprConvertFileNames(Structure):  # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("Fid", c_int)]

    class _StprRfidGetAuthResult(Structure):  # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("Doc", util.st_gxVARIANT)]


class ECardReader:
    """
    Electronic card reader (Contact Smartcard, RFID card or Magnetic
    stripe card) component.
    """

    Information = ecardhandling.ReaderInformation
    Information.__doc__ = """See ecardhandling.ReaderInformation for details."""

    def __init__(self, api_handle, reader_name, info):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.name = reader_name
        self.information = info
        self.cards = []
        self._opened = True

    @property
    def info(self):
        """ The card reader Information data. """
        return ECardReader.Information(self.information)

    def list_cards(self):
        """ Return a list of the available ECards.

        :return:        A list of ECard serial number strings.
        """
        param = ECardReader._StprGetReaderCardList(Reader=self.name)
        self.cards.clear()
        self.prapi.api_call(PrApi.GetReaderCardList, param)
        self.cards = GxMem.to_list(str, param.Cards, param.NCards)
        return self.cards

    def connect_card(self, card_no):
        """ Start using an ECard.

        :param card_no: The  ordinal  number  of the  card  in the  last
                        requested cardlist.
        :return:        The ECard handling object.
        """
        if card_no < 0 or card_no >= len(self.cards):
            raise exceptions.DataOutOfRange("[pr22] (card_no)")

        param = ECardReader._StprRfidCard(self.cards[card_no])
        self.prapi.api_call(PrApi.ConnectRfidCard, param)
        return ECard(self.prapi, self.cards[card_no])

    def use(self):
        """ Start using the current ECardReader. """
        if self._opened: return

        param = ECardReader._StprRfidOpenDevice(self.name, 0)
        self.prapi.api_call(PrApi.OpenCardReader, param)
        self._opened = True

    def ignore(self):
        """ End the usage of the current ECardReader.

        This method is usable to communicate with an ECardReader outside
        our SDK.
        """
        if not self._opened or not self.prapi.IsValid():
            return

        param = ECardReader._StprRfidOpenDevice(self.name, 0)
        self.prapi.api_call(PrApi.CloseCardReader, param)
        self._opened = False

    def start_read(self, card, ecard_task):
        """
        Begin  the authentication  and reading  process in  a background
        thread.

        After the process is finished the TaskControl.wait() method must
        be called.

        :param card:        The ECard to process.
        :param ecard_task:  List of files and  authentication level in a
                            task.ECardTask value.
        :return:            A task.TaskControl object.
        """
        size = len(ecard_task.files)
        int_array = (c_int * size)()
        for ix in range(size): int_array[ix] = int(ecard_task.files[ix])

        param = ECardReader._StprStartEcardReading(card.serial, cast(pointer(int_array),
                                            POINTER(c_int)), size, ecard_task.authlevel, 0)

        self.prapi.api_call(PrApi.StartEcardReading, param)
        return task.TaskControl(self.prapi, param.reqid)

    @property
    def certificate_manager(self):
        """
        The certificate manager that stores certificates for the current
        ECardReader device only.

        The value is an ecardhandling.Certificates object.
        """
        return Certificates(self.prapi, CertScope.CardReader, self.name)

    class _StprGetReaderCardList(Structure):  # pylint: disable=R0903
        _fields_ = [("Reader", c_wchar_p), ("Cards", POINTER(c_wchar_p)), ("NCards", c_int)]

    class _StprRfidCard(Structure):         # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p)]

    class _StprRfidOpenDevice(Structure):   # pylint: disable=R0903
        _fields_ = [("Device", c_wchar_p), ("DevInfo", util.st_gxVARIANT)]

    class _StprStartEcardReading(Structure):  # pylint: disable=R0903
        _fields_ = [("card", c_wchar_p), ("files", POINTER(c_int)), ("nfiles", c_int),
                    ("authlevel", c_int), ("reqid", c_int)]


class DocumentReaderDevice:
    """
    Central class for a document reader device.

    A device is composed of several components.  These components can be
    accessed through this class.
    """

    def _event_func(self, evt, param1, param2, uparam):
        if evt < 0 or evt >= len(self._events) or not self._event_filter: return

        cur_ev: list[Callable] = self._events[evt]
        with self._evlsmx:
            cur_ev = cur_ev.copy()
        event = Event(evt)
        pars = None

        if event == Event.ScanFinished:
            pars = param1, ErrorCodes.parse(param2), self
        elif event == Event.ImageScanned:
            pars = param1, imaging.Light.parse(param2), self
        elif event == Event.ScanStarted:
            pars = param1, self
        elif event == Event.PreviewCaptured:
            pars = self
        elif event == Event.PresenceDetection:
            pars = util.PresenceState.parse(param1), self
        elif event == Event.Button:
            pars = param1, param2, self
        elif event == Event.Power:
            pars = param1, param2, self
        elif event == Event.Connection:
            pars = param1, self
        elif event == Event.DocFrameFound:
            pars = param1, self
        elif event == Event.AuthBegin:
            pars = AuthProcess.parse(param1), self
        elif event == Event.AuthWaitForInput:
            pars = AuthProcess.parse(param1), self
        elif event == Event.AuthFinished:
            pars = AuthProcess.parse(param1), ErrorCodes.parse(param2), self
        elif event == Event.ReadBegin:
            pars = File(param1), self
        elif event == Event.ReadFinished:
            pars = File(param1), ErrorCodes.parse(param2), self
        elif event == Event.FileChecked:
            pars = File(param1), ErrorCodes.parse(param2), self
        elif event == Event.DeviceUpdate:
            pars = param1, self

        for func in cur_ev:
            try:
                func(*pars)
            except Exception as ex:
                ex.add_note("Exception not handled in event")
                print(traceback.format_exc())

    def __init__(self, prop_path="default"):
        """ Initialize the Document Reader software.

        :param prop_path:   Name of  the xml node  of the gxsd.dat  file
                            from where the initial data should be read.
        """
        self.prapi = GxModule()
        self.prapi.open("prapi", prop_path)
        self.prapi.set_property("sdk", __version__ + " [py]")
        self.prapi.set_property("event_filter", "0")
        self.prapi.set_property("async_callback", "1")

        self._event_filter = 0
        self._events = [[] for ix in range(19)]
        self._evlsmx = threading.Lock()
        self._evarmx = threading.Lock()
        self._callback = EVTFUNC(self._event_func)

        param = DocumentReaderDevice._StprSetEventFunction(cast(self._callback, c_void_p), None)
        self.prapi.api_call(CommonApi.SetEventFunction, param)
        self._scanner = None
        self._readers = []
        self._engine  = Engine(self.prapi)
        self._devname = ""

    def __del__(self):
        """ Finalizer. """
        self._event_filter = 0
        try: self.close_device()
        except exceptions.General: pass
        try: self.prapi.close()
        except exceptions.General: pass

    @staticmethod
    def list_devices(devcls=None):
        """ Collect a list of device names for useDevice method.

        :param devcls:      An opened DocumentReaderDevice can be passed
                            as argument to speed up list generation.
        :return:            A list of device name strings.
        """
        if not devcls:
            try:
                devcls = GxModule("prapi", "default")
                return DocumentReaderDevice.list_devices(devcls)
            finally: del devcls

        param = DocumentReaderDevice._StprGetDeviceList("PR", pointer(c_wchar_p(None)), 0)
        if isinstance(devcls, DocumentReaderDevice):
            devcls.prapi.api_call(CommonApi.GetDeviceList, param)
        else: devcls.api_call(CommonApi.GetDeviceList, param)
        return GxMem.to_list(str, param.devices, param.ndevices)

    def use_device(self, device_nom):
        """ Start using a device.

        :param device_nom:  Ordinal number or name of the device to use.
        :return:            self

        The list  of available  device  names can  be obtained  from the
        list_devices() method.
        """
        if isinstance(device_nom,  int):
            devices = self.list_devices(self)
            if device_nom < 0:
                raise exceptions.InvalidParameter("[pr22] (devno)")
            if device_nom >= len(devices):
                raise exceptions.NoSuchDevice("[pr22] (devno)")
            device_nom = devices[device_nom]

        self._scanner = None
        self._readers.clear()
        self._devname = ""

        param = DocumentReaderDevice._StprUseDevice(device_nom, 2)
        self.prapi.api_call(CommonApi.UseDevice, param)

        self._scanner = DocScanner(self.prapi)

        param2 = DocumentReaderDevice._StprGetDeviceInfo(None)
        self.prapi.api_call(CommonApi.GetDeviceInfo, param2)
        devinfo = util.Variant(param2.devInfo).get_list_item(0)
        self._devname = devinfo.to_string()

        for ix, childvar in devinfo.all_children():
            reader_type = childvar.to_int()
            if reader_type in [util.HWType.ContactReader, util.HWType.RFIDReader]:
                chidchild = childvar.get_child(util.VariantId.DeviceId, 0)
                tmp = chidchild.to_string()
                self._readers.append(ECardReader(self.prapi, tmp, childvar))
            elif reader_type == util.HWType.MagneticReader:
                self._readers.append(ECardReader(self.prapi, "MS Reader", childvar))

        return self

    def get_version(self, component):
        """ Return version information of the API.

        :param component:   Character 'A'  for version  of the interface
                            files,
                            or character 'S' for version of the Passport
                            Reader system.
        :return:            Version information string.
        """
        if component == 'A':
            return __version__
        if component == 'S':
            return self.prapi.get_property("api_version")
        return "-"

    def close_device(self):
        """ End using of the current device. """
        self._scanner = None
        if self.prapi.is_valid(): self._readers.clear()
        self._devname = ""

        if self.prapi:
            param = DocumentReaderDevice._StprUseDevice(None, c_int(0))
            self.prapi.api_call(CommonApi.UseDevice, param)

    def set_property(self, name, value):
        """ Set a property value of the Passport Reader system.

        The names  and values  of the properties  are documented  in the
        Passport Reader reference manual.

        :param name:        The name string of the property.
        :param value:       The value of the property.
        """
        return self.prapi.set_property(name, value)

    def get_property(self, name):
        """ Return a property value of the Passport Reader system.

        The names  and values  of the properties  are documented  in the
        Passport Reader reference manual.

        :param name:        The name string of the property.
        :return:            The string value of the property.
        """
        return self.prapi.get_property(name)

    @property
    def scanner(self):
        """ The document scanner component of the used device. """
        return self._scanner

    @property
    def readers(self):
        """
        The list of all the  electronic card reader  (Contact Smartcard,
        RFID  card or  Magnetic  stripe  card)  components  of the  used
        device.
        """
        return self._readers

    @property
    def peripherals(self):
        """ The device peripheral controller component of the used device. """
        return Peripherals(self.prapi)

    @property
    def engine(self):
        """ The data analyzer component of the used device. """
        return self._engine

    def add_event_handler(self, event, handler):
        """ Set an event handler function to a specified event.

        :param event:       The specified Event to handle.
        :param handler:     The event handler function.
        """
        efv = int(event)
        if efv < 0 or efv >= len(self._events) or not handler: return

        with self._evarmx:
            no_old_handlers = not self._events[efv]
            with self._evlsmx:
                self._events[efv].append(handler)
            self.trigger_event(efv)

            if no_old_handlers:
                self._event_filter |= 1 << efv
                if self.prapi.is_valid():
                    self.prapi.set_property("event_filter", str(self._event_filter))

    def remove_event_handler(self, event, handler):
        """ Remove an event handler function from a specified event.

        Because of the multithreading environment, pending events may be
        still raised for a short period,  even after their event handler
        was removed.

        :param event:       The specified Event to handle.
        :param handler:     A previously registered function.
        """
        if event < 0 or event >= len(self._events): return

        with self._evarmx:
            evs = self._events[int(event)]
            with self._evlsmx:
                evs.remove(handler)

            if not evs:
                self._event_filter &= ~(1 << event)
                if self.prapi.is_valid():
                    self.prapi.set_property("event_filter", str(self._event_filter))

    def trigger_event(self, event):
        """ Trigger an event.

        :param event:       The specified Event to trigger.  Not all the
                            events can be triggered.
        """
        efv = int(event)
        if efv < 0 or efv >= len(self._events) or not self._events[efv]: return
        if self.prapi.is_valid():
            self.prapi.set_property("trigger_event", str(1 << event))

    @property
    def global_certificate_manager(self):
        """
        The certificate manager that stores certificates for all task of
        the entire process.

        The value is an ecardhandling.Certificates object.
        """
        return Certificates(self.prapi, CertScope.Global, "")

    @property
    def certificate_manager(self):
        """
        The certificate manager that stores certificates for task of the
        current DocumentReaderDevice device.

        The value is an ecardhandling.Certificates object.
        """
        return Certificates(self.prapi, CertScope.DocumentReader, self.device_name)

    device_name = property(lambda self: self._devname, None, None, "The name of the device.")

    class _StprSetEventFunction(Structure):  # pylint: disable=R0903
        _fields_ = [("func", c_void_p), ("param", c_void_p)]

    class _StprGetDeviceList(Structure):    # pylint: disable=R0903
        _fields_ = [("filter", c_wchar_p), ("devices", POINTER(c_wchar_p)), ("ndevices", c_int)]

    class _StprUseDevice(Structure):        # pylint: disable=R0903
        _fields_ = [("devname", c_wchar_p), ("mode", c_int)]

    class _StprGetDeviceInfo(Structure):    # pylint: disable=R0903
        _fields_ = [("devInfo", util.st_gxVARIANT)]
