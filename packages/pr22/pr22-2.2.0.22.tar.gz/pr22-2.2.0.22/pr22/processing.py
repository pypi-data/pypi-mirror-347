#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Enumerations and classes of data processing. """

__version__ = '2.2.0.22'

from ctypes import c_wchar_p, c_wchar, cast, c_void_p, c_byte, c_int, sizeof as _sizeof
from ctypes import Structure, pointer as _pointer, POINTER as _POINTER, memmove as _memmove
from fnmatch import fnmatch
from os     import path, listdir as _listdir

from pr22 import exceptions, prins, imaging
from pr22.fieldid import FieldId
from pr22.types import PrEnum, chk_ver
from pr22.prins import ModuleCallCodes, PrApi
from pr22.util  import VariantId, Variant, st_gxVARIANT
chk_ver(__version__)


class FieldSource(PrEnum):
    """ Field source IDs. """
    All             =    0,         "Any source."
    Mrz             = 1000,         "Machine Readable Zone."
    Viz             = 2000,         "Visual Inspection Zone."
    Barcode         = 3000,         "Barcode."
    MagStripe       = 4000,         "Magnetic stripe."
    Manual          = 11000,        "Manually added."
    Preferred       = 12000,        "Preferred."
    ECard           = 0x400000,     "SmartCard (contact or contactless)."


class Checking(PrEnum):
    """ Field checking details. """
    Missing          = 0xD0080003,  "Mandatory entity is missing."
    SelfCheckOk      = 0xD0080010,  "Self checking is succeeded."
    SelfCheckInvalid = 0xD0080012,  """
    Self checking cannot be performed due to invalid data format.
    """
    SelfCheckFailed  = 0xD0080013,  "Self checking is failed."
    FormatOk         = 0xD0080020,  "Format test is succeeded."
    FormatInvalid    = 0xD0080023,  "Format test is failed."
    DateOk           = 0xD0080030,  "Datetime value is not expired."
    DateInvalid      = 0xD0080032,  "Past datetime value is greater than current date."
    DateExpired      = 0xD0080033,  "Datetime value is expired."
    Revoked          = 0xD0080043,  "Certificate has been revoked."


class FieldStatus(PrEnum):
    """
    Field status values. Result of checksum calculations, data integrity
    and environmental specific (e.g. expiry) tests.
    """
    Ok              =   0,          "All checks are passed successfully."
    NoChecksum      =   1,          "There is no checksum for the field."
    Warning         = 100,          "Warning occurred."
    DataIntegrity   = 101,          "Data integrity failed."
    OCRWarning      = 102,          "OCR warning occurred."
    Error           = 200,          "Error occurred."
    InvalidChar     = 201,          "Invalid character found."
    InvalidChecksum = 202,          "Invalid checksum value found."
    ChecksumError   = 203,          "Checksum failed."


class EngineLicense(PrEnum):
    """ Engine license IDs. """
    MrzOcrBarcodeReading  = 0xF4,   "MRZ OCR+Barcode Reading license."
    MrzOcrBarcodeReadingL = 0x74,   "MRZ OCR+Barcode Reading license (variable)."
    MrzOcrBarcodeReadingF = 0x84,   "MRZ OCR+Barcode Reading license (fixed)."
    VizOcrCountry         = 0x10,   "VIZ OCR Level1-Country license."
    VizOcrRegion          = 0x11,   "VIZ OCR Level2-Region license."
    VizOcrWorld           = 0x12,   "VIZ OCR Level3-World license."
    VizOcrAuthCountry     = 0x13,   "VIZ OCR+AUTH Level1-Country license."
    VizOcrAuthRegion      = 0x14,   "VIZ OCR+AUTH Level2-Region license."
    VizOcrAuthWorld       = 0x15,   "VIZ OCR+AUTH Level3-World license."
    PRSoftware            = 0xA1,   "PR Software license."
    PRAutoFill            = 0xA2,   "PR auto fill license."
    ECard                 = 0xEC,   "ECard Features license."
    HotelInterface        = 0xFA,   "Hotel Reader Interface license."
    Unknown               = 0,      "License information is not available."


class BinData:
    """ Class for storing binary or textual data. """

    def __init__(self):
        self._data = None  # c_byte[]
        self._dataformat = None
        self._comment = None

    def __str__(self):
        try:    return self.to_string()
        except exceptions.General: return ''

    @staticmethod
    def from_gx(address, length):
        """ Internally used method. """
        nval = BinData()
        nval._data = prins.GxMem.to_bytes(address, length)
        return nval

    @property
    def raw_data(self):
        """ A reference to data as c_byte array. """
        return self._data

    @property
    def raw_size(self):
        """ Size of the raw data in bytes. """
        return len(self._data) if self._data is not None else 0

    @property
    def data_format(self):
        """
        A file format identifier string that can be used as filename
        extension.
        """
        if self._dataformat is not None: return self._dataformat
        wchar_array = (c_wchar * 20)()
        ptp = cast(wchar_array, c_wchar_p)
        pdp = cast(self._data, c_void_p)
        params = BinData._StprGetDataFormat(pdp, self.raw_size, ptp, 20)
        api_module = prins.GxModule("prapi", "default")
        try:
            api_module.api_call(PrApi.GetDataFormat, params)
        finally:
            api_module.close()
        self._dataformat = wchar_array.value
        return self._dataformat

    def load(self, file_name):
        """ Load data from a file.

        :param file_name:   File name to load from.
        :return:            self
        """
        self._data       = None
        self._dataformat = None
        self._comment    = None
        param = BinData._StgxLoadBinary(0, c_wchar_p(file_name), 0, 2)

        prins.glob_call(0, ModuleCallCodes.LoadBinary, param)
        self._data = prins.GxMem.to_bytes(param.buffer, param.size)
        return self

    def save(self, file_name):
        """ Save data to a file.

        :param file_name:   File name to save to.
        :return:            self
        """
        param = BinData._StgxLoadBinary(cast(self._data, c_void_p),
                                c_wchar_p(file_name), self.raw_size, 2)

        prins.glob_call(0, ModuleCallCodes.SaveBinary, param)
        return self

    def set_byte_array(self, source):
        """ Set binary data.

        :param source:      Source binary data.
        :return:            self
        """
        self._data       = None
        self._dataformat = None
        self._comment    = None
        length = len(source) if source is not None else 0
        if length:
            self._data = (c_byte * length)()
            _memmove(self._data, source, length)
        return self

    def to_byte_array(self):
        """ Store data into a byte array.

        :return:            Data transformed to bytearray.
        """
        return bytearray(self._data) if self._data is not None else bytearray()

    def set_string(self, string_data):
        """ Generate binary data from a string.

        :param string_data: The string or list of strings to store.
        :return:            self
        """
        if isinstance(string_data, list):
            tmpstr = ""
            for string in string_data:
                tmpstr += "\n" + string
            string_data = tmpstr[1:] if tmpstr else ""
        if isinstance(string_data, str):
            self._dataformat = None
            self._comment    = None
            if not string_data or string_data[-1] != U"\x00": string_data += U"\x00"
            length = len(string_data) * _sizeof(c_wchar)
            self._data = (c_byte * length)()
            _memmove(self._data, c_wchar_p(string_data), length)
        else:
            raise exceptions.InvalidParameter("[pr22] Invalid parameter type!")
        return self

    def to_string(self):
        """ Store data into a string.

        :return:            Data transformed to string.
        """
        if self._data is None: return ""
        try:
            retstr = bytearray(self._data).decode('utf-' + str(_sizeof(c_wchar)*8))
            return retstr if not retstr or retstr[-1] != U"\x00" else retstr[:-1]
        except ValueError:
            pass
        try:
            retstr = bytearray(self._data).decode()
            return retstr if not retstr or retstr[-1] != U"\x00" else retstr[:-1]
        except ValueError as exc:
            raise exceptions.DataOutOfRange("[pr22] " + str(exc))

    comment = property(lambda self: self._comment,
        lambda self, comment: setattr(self, "_comment", comment), None,
        "Internally used data.")

    class _StprGetDataFormat(Structure):  # pylint: disable=R0903
        _fields_ = [("Buffer", c_void_p), ("BufLen", c_int),
                    ("Format", c_wchar_p), ("FormatLen", c_int)]

    class _StgxLoadBinary(Structure):       # pylint: disable=R0903
        _fields_ = [("buffer", c_void_p), ("filename", c_wchar_p),
                    ("size", c_int), ("strtype", c_int)]


class Page:
    """ Storage of images taken by the DocScanner.scan() method.

    Images scanned earlier are also available with the
    DocScanner.get_page() method.
    """

    def __init__(self, api_handle, page_num, image_list):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.page_number = page_num
        self.image_list = image_list.new_ref()

    def __del__(self):
        """ Finalizer. """
        del self.image_list
        self.image_list = None
        self.prapi = None

    def __enter__(self):
        """ Enter the runtime context. """
        self.image_list.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the runtime context. """
        try: self.image_list.__exit__(exc_type, exc_val, exc_tb)
        except exceptions.General: pass
        self.image_list = None
        self.prapi = None
        return False

    def remove(self, light):
        """ Remove an image from the page.

        This removal  is made only with  the current data object.  Other
        calls  of  DocScanner.get_page()  method  will  contain  all the
        scanned  images.  This  removal  is used  for  omitting  certain
        illuminations from an analyzing process.

        :param light:       Id of the Light to remove.
        :return:            self
        """
        image_list = Variant(VariantId.ImageList, Variant.Types.List)
        for ix in range(self.image_list.n_items):
            if self.image_list[ix].get_child(VariantId.Light, 0).to_int() != light:
                image_list.add_list_item(self.image_list[ix])
        self.image_list = image_list
        return self

    def select(self, light):
        """ Select one image from the page by its light.

        :param light:       Id of the Light.
        :return:            An imaging.DocImage object.
        """
        for ix, img in self.image_list.all_items():
            if img.get_child(VariantId.Light, 0).to_int() == light:
                return imaging.DocImage(self.prapi, img, self.page_number)
        raise exceptions.EntryNotFound("[pr22] (light)")

    def select_by_index(self, index):
        """ Select one image from the page.

        :param index:       Ordinal number of the image.
        :return:            An imaging.DocImage object.
        """
        if self.image_list.n_items > index:
            return imaging.DocImage(self.prapi, self.image_list[index], self.page_number)
        raise exceptions.DataOutOfRange("[pr22] (index)")

    def analyze(self, engine_task):
        """
        Analyze  the image data of the page  and return the  textual and
        logical data according to task.

        This method has the same role as Engine.analyze().

        :param engine_task: Specifies  data field references  to analyze
                            in task.EngineTask structure.
        :return:            The result Document structure.
        """
        param = Page._StprAnalyze()
        # pylint: disable=W0201
        param.page = self.image_list.var_data
        param.tasklen = len(engine_task.fields)
        int_array = (c_int*param.tasklen)()
        for ix in range(param.tasklen): int_array[ix] = engine_task.fields[ix]
        param.task = cast(_pointer(int_array), c_void_p)
        param.doc = None
        self.prapi.api_call(PrApi.Analyze, param)
        return Document(self.prapi, Variant(param.doc))

    class _StprAnalyze(Structure):          # pylint: disable=R0903
        _fields_ = [("page", st_gxVARIANT), ("tasklen", c_int),
                    ("task", c_void_p), ("doc", st_gxVARIANT)]


class FileFormat(PrEnum):
    """ FileFormat for saving documents. """
    Xml         = 1,        "Xml data file."
    Zipped      = 2,        """Zipped data file.

    Only  this file type  can be loaded back  to the Passport Reader
    system."""
    EncZip      = 4,        """Encrypted zip file.

    Such files  can be decrypted  if the appropriate  private key is
    available."""
    BsiAuthLog  = 5,        """Logging scheme declared in BSI TR-03135.

    Only overall and optical checks are saved."""


class Document:
    """ Storage for the results of analyzing tasks. """

    FileFormat = FileFormat

    def __init__(self, api_handle, variant):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.variant = variant.new_ref()

    def __del__(self):
        """ Finalizer. """
        del self.variant
        self.variant = None
        self.prapi = None

    def __enter__(self):
        """ Enter the runtime context. """
        self.variant.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the runtime context. """
        try: self.variant.__exit__(exc_type, exc_val, exc_tb)
        except exceptions.General: pass
        self.variant = None
        self.prapi = None
        return False

    def __add__(self, other):
        """ Generate an integrated document.

        This  document  will contain  field comparison results,  summary
        data and all general field data of the source documents.

        :param other:       Other document.
        :return:            The integrated document.
        """
        if not self.variant or not self.variant.is_valid(): return other
        if not other: return self
        if not isinstance(other, Document):
            raise exceptions.InvalidParameter("[pr22] Not expected type!")
        if not other.variant or not other.variant.is_valid(): return self

        param = Document._StprMergeDocuments(self.variant.var_data, other.variant.var_data, 0)
        self.prapi.api_call(PrApi.MergeDocuments, param)
        if param.NDoc: return Document(self.prapi, Variant(param.NDoc))
        return self

    def to_variant(self):
        """ Return low level data to access special document information.

        :return:            Low level util.Variant data.
        """
        return self.variant

    def _enabled_field(self, field, filt):
        ret = False
        filti = FieldReference()
        if len(filt) == 0: return True
        for fld in filt:
            filti.code = fld
            addv = filti.code >= 0
            if not addv: filti.code = -filti.code
            fid = field.id_v % 0x400000 % 1000
            if (filti.source in [field.source, FieldSource.All]
                    and (filti.id_v in [field.id_v, FieldId.All]
                    or (filti.id_v == FieldId.Authenticity and 500 <= fid < 600))):
                ret = addv
        return ret

    def list_fields(self, filt=None):
        """ Return a list of field references from the document.

        :param filt:        Filter for the list. Can be a FieldReference
                            or a task.EngineTask object.
        :return:            List of FieldReference IDs.
        """
        if                           not filt: filt = []
        elif isinstance(filt, FieldReference): filt = [filt.code]
        elif          hasattr(filt, 'fields'): filt = filt.fields  # task.EngineTask
        elif not isinstance(filt, list): raise exceptions.InvalidParameter("[pr22] (filt)")

        fields = []
        try: fieldlist = self.variant.get_child(VariantId.FieldList, 0)
        except exceptions.General: return fields

        for jxv in range(fieldlist.n_items):
            field = FieldReference()
            try: field.code = fieldlist[jxv].to_int()
            except exceptions.General: continue
            field.index = 0
            if not self._enabled_field(field, filt): continue
            for ix in range(len(fields), 0,  -1):
                if fields[ix-1].code == field.code:
                    field.index = fields[ix-1].index + 1
                    break
            fields.append(field)
        return fields

    def get_part(self, index):
        """
        Return a simple document data of a "Root document".

        It represents  the result of one analyzer method called  for the
        document before.  The Engine.get_root_document()  method returns
        a so-called  "Root document"  that contains  the results  of all
        methods called for the current document.

        :param index:       The ordinal number of the document part.
        :return:            The Document part.
        """
        paths = f"C,D={c_int(VariantId.TaskList).value}/L,X={index}"
        with self.variant.get_item_by_path(paths) as part:
            return Document(self.prapi, part)

    def get_field(self, field, field_id=None, index=0):
        """ Return a field of the document.

        Can be  called with  FieldReference  as only parameter,  or with
        FieldSource, FieldId and index parameter triplet.

        :param field:       FieldSource or FieldReference.
        :param field_id:    FieldId or None.
        :param index:       Index of the fields having the same Id.
        :return:            Field data.
        """
        if not isinstance(field, FieldReference):
            fld = FieldReference(field, field_id)
            fld.index = index
            field = fld
        paths = f"C,D={c_int(VariantId.FieldList).value}/L,V={field.code},X={field.index}"
        with self.variant.get_item_by_path(paths) as var_field:
            return Field(self.prapi, var_field, field, self.variant)

    def get_status(self):
        """ Return the overall status of the document.

        :return:            Composite FieldStatus of the document.
        """
        try: return FieldStatus.parse(self.variant.get_child(VariantId.Checksum, 0).to_int())
        except exceptions.General: return FieldStatus.NoChecksum

    def save(self, file_format):
        """ Save the document to the memory in a specific file format.

        Only  "Root documents"  returned  by  Engine.get_root_document()
        method can be loaded back to the system.
        See DocScanner.load_document()

        :param file_format: The FileFormat.
        :return:            Saved document file data in BinData object.
        """
        param = Document._StprSaveDocumentToMem()
        # pylint: disable=W0201
        param.doc = self.variant.var_data
        param.filetype = file_format
        tmp = c_void_p(None)
        param.buffer = cast(_pointer(tmp), c_void_p)
        bufflen = c_int(0)
        param.bufflen = cast(_pointer(bufflen), c_void_p)
        self.prapi.api_call(PrApi.SaveDocumentToMem, param)
        length = bufflen.value
        if file_format in [Document.FileFormat.BsiAuthLog, Document.FileFormat.Xml]: length -= 4

        return BinData.from_gx(tmp, length)

    def get_field_compare_list(self):
        """ Return the results of field value comparison tests.

        :return:            List of FieldCompare values.
        """
        fclist = []
        try:
            arr = self.variant.get_child(VariantId.FieldCompares, 0).to_int_array()
        except  exceptions.General:
            return fclist

        for ix in range(0, len(arr)-2, 3):
            fcv = FieldCompare(arr[ix], arr[ix + 1], arr[ix + 2])
            fclist.append(fcv)
        return fclist

    class _StprMergeDocuments(Structure):   # pylint: disable=R0903
        _fields_ = [("Doc1", st_gxVARIANT), ("NDoc", st_gxVARIANT), ("Relation", c_int)]

    class _StprSaveDocumentToMem(Structure):  # pylint: disable=R0903
        _fields_ = [("doc", st_gxVARIANT), ("filetype", c_int),
                    ("buffer", c_void_p), ("bufflen", c_void_p)]


class Field:
    """ The Field is the base element of document analyzing results.

    The Field always contains  an Id to give meaning  for the data,  the
    read data  that can be binary or textual  (or numeric values  can be
    handled  as textual data),  and the  status information  of checking
    algorithms.  If the field is image-related  then image data or image
    frame can be requested.
    """

    def __init__(self, api_handle, variant, field_ref, parent):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.parent = parent.new_ref()
        self.variant = variant.new_ref()
        self._field_reference = field_ref

    def __del__(self):
        """ Finalizer. """
        del self.variant
        self.variant = None
        del self.parent
        self.parent = None
        self.prapi = None

    def __enter__(self):
        """ Enter the runtime context. """
        self.variant.__enter__()
        self.parent.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the runtime context. """
        try: self.variant.__exit__(exc_type, exc_val, exc_tb)
        except exceptions.General: pass
        self.variant = None
        try: self.parent.__exit__(exc_type, exc_val, exc_tb)
        except exceptions.General: pass
        self.parent = None
        self.prapi = None
        return False

    def get_raw_string_value(self):
        """ Return the string data of the field as it is read.

        The string can contain separator characters and checksum.
        """
        return self.variant.get_child(VariantId.FieldValue, 0).to_string()

    def get_formatted_string_value(self):
        """ Return the formatted string data of the field.

        The separator characters  are replaced with spaces and  checksum
        values are not included.
        """
        return self.variant.get_child(VariantId.FormattedValue, 0).to_string()

    def get_standardized_string_value(self):
        """
        Return the data of the field converted to a standard format.

        Even the whole value can be replaced. E.g. converted from inches
        to centimeters.
        """
        return self.variant.get_child(VariantId.StandardizedValue, 0).to_string()

    def get_basic_string_value(self):
        """
        Return  the  string data  of the  field  in the  least  modified
        format.
        """
        try:    return self.variant.get_child(VariantId.FieldValue, 0).to_string()
        except exceptions.EntryNotFound: pass
        try:    return self.variant.get_child(VariantId.FormattedValue, 0).to_string()
        except exceptions.EntryNotFound: pass
        return self.variant.get_child(VariantId.StandardizedValue, 0).to_string()

    def get_best_string_value(self):
        """
        Return  the  string data  of the field  in the  most  convenient
        format.
        """
        try:    return self.variant.get_child(VariantId.StandardizedValue, 0).to_string()
        except exceptions.EntryNotFound: pass
        try:    return self.variant.get_child(VariantId.FormattedValue, 0).to_string()
        except exceptions.EntryNotFound: pass
        return self.variant.get_child(VariantId.FieldValue, 0).to_string()

    def get_binary_value(self):
        """ Return the binary data of the field. """
        return self.variant.get_child(VariantId.FieldValue, 0).to_byte_array()

    def get_status(self):
        """
        Return  the status  information of  checking algorithms  for the
        field.

        :return:            Composite FieldStatus value.
        """
        try:    return FieldStatus.parse(self.variant.get_child(VariantId.Checksum, 0).to_int())
        except exceptions.General: return FieldStatus.NoChecksum

    def get_detailed_status(self):
        """
        Return  a  list  of  detailed  status  information  of  checking
        algorithms for the field.

        :return:            List of Checking values.
        """
        stlist = []
        try:
            int_array = self.variant.get_child(VariantId.CheckDetails, 0).to_int_array()
            for stv in int_array:
                if stv < 0: stv += 0x1_0000_0000
                stlist.append(Checking.parse(stv))
        except exceptions.General: pass
        return stlist

    def get_image(self):
        """ Return the image of the field.

        :return:            An imaging.RawImage object.
        """
        param = Field._StprGetFieldIMageV(self.parent.var_data, self.field_ref.code,
                                    self.field_ref.index, None)
        self.prapi.api_call(PrApi.GetFieldImageV, param)
        with Variant(param.Img) as var:
            return imaging.RawImage().from_variant(var)

    def get_frame(self):
        """ Return the geometric location of the field.

        :return:            A util.Frame value.
        """
        return self.variant.get_child(VariantId.WindowFrame, 0).to_frame()

    def to_variant(self):
        """ Return low level data to access special field information.

        :return:            Low level util.Variant data.
        """
        return self.variant

    field_ref = property(lambda self: self._field_reference, None, None,
                         "Field identification data.")

    class _StprGetFieldIMageV(Structure):  # pylint: disable=R0903
        _fields_ = [("Doc", st_gxVARIANT), ("FieldCode", c_int),
                    ("Index", c_int), ("Img", st_gxVARIANT)]


class FieldReference:
    """ Class for storing Field identification data.

    :ivar code:         Internally used value of Field identification.
    :ivar index:        Ordinal number of the Field with the same code.
    """

    def __init__(self, fldsrc=0, fldid=None):
        """ A new Field identification data.

        :param fldsrc:      Id of the FieldSource.
        :param fldid:       Field Id.

        The fldsrc parameter alternatively can be used to conversion
        from ecardhandling.AuthProcess or ecardhandling.File.
        """
        self.index = 0
        self.code = -1
        if fldid is None and hasattr(fldsrc, 'to_fref'):
            self.code = int(FieldId.COM) + fldsrc.to_fref()
            return
        if fldid is None: fldid = 0
        if fldsrc == FieldSource.ECard:
            if fldid == FieldId.CompositeMrz:   self.code = 0x410000
            elif fldid == FieldId.Face:         self.code = 0x420000
            elif fldid == FieldId.Fingerprint:  self.code = 0x430000
            elif fldid == FieldId.Iris:         self.code = 0x440000
            elif fldid == FieldId.Signature:    self.code = 0x450000
            elif int(FieldId.COM) <= int(fldid) < int(FieldId.COM) + 100:
                self.code = int(fldid)

            if self.code != -1: return
        if fldid in [FieldId.B900, FieldId.CompositeVizAuth, FieldId.UVDullCheck,
                     FieldId.UVDullPhotoCheck, FieldId.SecurityFibres]:
            if fldsrc == FieldSource.Mrz and fldid == FieldId.UVDullCheck:
                self.code = 1552
                return
            self.code = int(fldid)
            return
        self.code = int(fldsrc) + int(fldid)

    def __str__(self):
        return self.to_string()

    def __format__(self, fmt):
        """
        Combine  application  of insert string  with the regular  string
        formatting options.

        :param fmt: The format string has the following form:

                [[":/" | "/"]<insert str><separator>]<str format_spec>

                    The separator is the last colon ':' by default.

                Special case 1:  When the colon is intended  as a filler
                    character, then the insert string has to be preceded
                    by a slash '/',  and the separator will be  the last
                    slash.
                Special case 2:  When insert string  starts with  slash,
                    then the format string  can be started  with a ":/",
                    and the separator is a colon in this case.

        :return:    String representation of the FieldReference.
        """
        altsep = 1 if fmt and fmt[0] == '/' else 0
        lof = fmt.rfind(':/'[altsep])
        if lof < 0: return format(self.to_string(), fmt)
        if fmt[0:2] == ':/': altsep = 2
        return format(self.to_string(fmt[altsep:lof]), fmt[lof + 1:])

    @property
    def source(self):
        """ Id of the FieldSource. """
        if self.code >= int(FieldSource.ECard): return FieldSource.ECard
        return FieldSource.parse(self.code - self.code % 1000)

    @property
    def id_v(self):
        """ The FieldId. """
        if self.code > int(FieldSource.ECard):
            if self.code == 0x410000: return FieldId.CompositeMrz
            if self.code == 0x420000: return FieldId.Face
            if self.code == 0x430000: return FieldId.Fingerprint
            if self.code == 0x440000: return FieldId.Iris
            if self.code == 0x450000: return FieldId.Signature
            if int(FieldId.COM) <= self.code < int(FieldId.COM) + 100:
                return FieldId.parse(self.code)
        if self.code == 1551: return FieldId.B900
        if self.code == 2500: return FieldId.CompositeVizAuth
        if self.code == 1552: return FieldId.UVDullCheck
        if self.code == 2551: return FieldId.UVDullCheck
        if self.code == 2553: return FieldId.SecurityFibres
        if self.code == 2560: return FieldId.UVDullPhotoCheck

        fid = (self.code - int(self.source)) % 1000
        return FieldId.parse(fid)

    def to_string(self, insert=None):
        """ Return string representation of the field reference.

        :param insert:      String to insert between  the source and the
                            id strings.
        :return:            String representation of the FieldReference.
        """
        if insert is None: insert = ""
        src = self.source
        s_src = src.name if isinstance(src, PrEnum) else str(int(src) // 1000)

        fid = self.id_v
        if isinstance(fid, PrEnum): s_id = fid.name
        elif fid // 100 == 5:       s_id = "Authenticity" + str(fid - 500)
        elif fid // 100 == 0:       s_id = "Composite" + str(fid)
        else:                       s_id = str(fid)

        s_x = "(" + str(self.index) + ")" if self.index else ""
        return f"{s_src}{insert}{s_id}{s_x}"

    def to_ecard(self):
        """ Internally used method. """
        return self.code - FieldId.COM.value


class FieldCompare:                             # pylint: disable=R0903
    """ Result data of Field comparison. """

    def __init__(self, val1, val2, conf):
        """ Do not create instances directly. """
        self._id1 = val1
        self._id2 = val2
        self._conf = conf

    field1 = property(lambda self: FieldReference(self._id1 & 0xff_ffff), None, None,
                      "FieldReference of the compared field #1.")

    page1 = property(lambda self: self._id1 >> 24, None, None,
                     "Page number of the compared field #1.")

    field2 = property(lambda self: FieldReference(self._id2 & 0xff_ffff), None, None,
                      "FieldReference of the compared field #2.")

    page2 = property(lambda self: self._id2 >> 24, None, None,
                     "Page number of the compared field #2.")

    confidence = property(lambda self: self._conf, None, None,
                          "Result of comparison in 0-1000 range.")


class EngineInformation:
    """ Class for storing information on an Engine. """

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.info = None
        param = EngineInformation._StprGetEngineInfo(None)
        try:
            self.prapi.api_call(PrApi.GetEngineInfo, param)
            self.info = Variant(param.info)
        except exceptions.FileOpen:
            pass

    def get_version(self, component):
        """ Return version information of the engine.

        :param component:   Character 'E' for version of the engine.
        :return:            Version information string of the engine.
        """
        try:
            if component == 'E': return self.info.to_string()
        except exceptions.General:
            pass
        return "-"

    @property
    def required_license(self):
        """ The required EngineLicense for the used engine. """
        try:
            if self.info:
                return EngineLicense.parse(self.info.get_child(VariantId.EngineLicense, 0).to_int())
        except exceptions.EntryNotFound:
            pass
        return EngineLicense.Unknown

    @property
    def required_license_date(self):
        """ The date string of the used engine. """
        try:
            if self.info:
                return self.info.get_child(VariantId.EngineLicDate, 0).to_string()
        except exceptions.EntryNotFound:
            pass
        return "-"

    def get_license_date(self, lic):
        """ Return the engine acceptance date of a license.

        :param lic:         The license to query for the date.
        :return:            The date string of the license.
        """
        param = EngineInformation._StprGetLicenseDate(lic, None)
        try:
            self.prapi.api_call(PrApi.GetLicenseDate, param)
            if not param.Date: return ""
            return cast(param.Date, c_wchar_p).value
        finally:
            prins.GxMem.free_mem(param.Date)

    def list_licenses(self):
        """ Return a list of the available engine licenses.

        :return:            A list of EngineLicense values.
        """
        param = EngineInformation._StprGetLicenses(None, 0)
        self.prapi.api_call(PrApi.GetLicenses, param)
        return prins.GxMem.to_list(EngineLicense.parse, param.Licenses, param.NLicenses)

    def list_engines(self):
        """ Return a list of the available OCR engines.

        :return:            A list of engine name strings.
        """
        dirname = self.prapi.get_property("module_dir")
        files = []
        for fname in _listdir(dirname):
            fpath = dirname + path.sep + fname
            if path.isfile(fpath) and (fnmatch(fname, "procr*.dll")
                                       or fnmatch(fname, "procr*.so")):
                files.append(fname[:fname.rfind(".")])
        return files

    class _StprGetEngineInfo(Structure):    # pylint: disable=R0903
        _fields_ = [("info", st_gxVARIANT)]

    class _StprGetLicenseDate(Structure):   # pylint: disable=R0903
        _fields_ = [("License", c_int), ("Date", c_void_p)]

    class _StprGetLicenses(Structure):      # pylint: disable=R0903
        _fields_ = [("Licenses", _POINTER(c_int)), ("NLicenses", c_int)]
