#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" General enumerations and classes. """

__version__ = '2.2.0.22'

from ctypes import c_int, c_wchar_p, c_void_p, c_byte, c_wchar, c_double, c_longlong, Structure
from ctypes import sizeof as _sizeof, cast, pointer as _pointer, POINTER as _POINTER, _Pointer

from pr22 import prins, exceptions
from pr22.types import PrEnum, chk_ver
chk_ver(__version__)


class VariantId(PrEnum):
    """ Ids of Variant data. """
    Root                = 0,            "The root document structure."
    PageList            = 1,            "List of pages."
    TaskList            = 2,            "List of tasks."
    MergeList           = 5,            "List of merged documents."
    Document            = 0xD0000000,   """Document type.

    Integer value to distinguish different document pages."""
    FieldList           = 0xD0000001,   "List of fields."
    Field               = 0xD0000002,   """Field code.

    It encodes the FieldId and the FieldSource values."""
    FieldValue          = 0xD0000003,   "Raw field value data."
    Checksum            = 0xD0000004,   "Field Status."
    Confidence          = 0xD0000005,   """Field confidence.

    Value is in 0-1000 range, or -1 if not set."""
    WindowFrame         = 0xD0000006,   "Frame coordinates in micrometers."
    WindowFullFrame     = 0xD0000007,   "Nominal Frame coordinates in micrometers."
    FormattedValue      = 0xD0000009,   "Formatted field value data."
    StandardizedValue   = 0xD000000A,   "Standardized field value data."
    Correction          = 0xD000000B,   "Number of corrected errors."
    FieldCompares       = 0xD000000C,   "Array of FieldCompare data."
    CheckDetails        = 0xD000000D,   "Array of field Checking details."
    AMID                = 0xD000000E,   "Authentication method type."
    RelatedPages        = 0xD000000F,   "Related document pages."
    Origin              = 0xD0000010,   "Origin of the field."
    Image               = 0xD0100000,   "imaging.RawImage object."
    ImageList           = 0xD0100001,   "List of images."
    ImageFrame          = 0xD0100002,   "Frame coordinates in 1/16 pixel."
    Sample              = 0xD0100003,   "Sample imaging.RawImage for the field."
    DeviceInfo          = 0xD0200000,   "The root of the device info data."
    DeviceId            = 0xD0200001,   "Device name."
    Light               = 0xD0200002,   "A Light value."
    CapTime             = 0xD0200003,   "Timestamp of the scan."
    Page                = 0xD0200004,   "Page Id."
    IdHWType            = 0xD0200009,   "Hardware module type HWType."
    StatledList         = 0xD020000A,   "List of status led colors."
    Keyboard            = 0xD020000B,   "List of available key code values."
    Power               = 0xD020000C,   "Power testing capability."
    Version             = 0xD020000D,   "Version info data."
    WindowList          = 0xD020000E,   "List of object window sizes."
    Capability          = 0xD020000F,   "Scanning window capability info."
    Display             = 0xD0200010,   "Display info."
    Barcode             = 0xD0300000,   "Barcode type."
    BarcodeValue        = 0xD0300001,   "Barcode binary data."
    BarcodeList         = 0xD0300002,   "List of barcodes."
    Ocr                 = 0xD0400000,   "OCR module version."
    OcrRowList          = 0xD0400001,   "List of OCR rows."
    OcrRow              = 0xD0400002,   "OCR row."
    OcrChar             = 0xD0400003,   "OCR character."
    OQCA                = 0xD0480000,   "Quality assurance alert signals."
    OQCRotation         = 0xD0480001,   "Rotation value for quality assurance."
    OQCHeight           = 0xD0480002,   "Height value for quality assurance."
    OQCWidth            = 0xD0480003,   "Width value for quality assurance."
    OQCHangout          = 0xD0480004,   "Hangout value for quality assurance."
    OQCDistance         = 0xD0480005,   "Distance value for quality assurance."
    OQCContrast         = 0xD0480006,   "Contrast value for quality assurance."
    OQCShape            = 0xD0480007,   "Shape confidence for quality assurance."
    Engine              = 0xD04A0000,   "Version of the engine."
    EngineLicense       = 0xD04A0001,   "Required license of the engine."
    EngineLicDate       = 0xD04A0002,   "License date of the engine."
    EngineLicType       = 0xD04A0003,   "License type of the engine."
    ECard               = 0xD0500000,   "RFU"
    ECardFileList       = 0xD0500002,   "List of ECard files."
    ECardFile           = 0xD0500003,   "ECard file Id."
    ECardFileData       = 0xD0500004,   "Data of an ECard file."
    CertIdList          = 0xD0500005,   "List of certificate Ids."
    DGList              = 0xD0500006,   "List of ECard file Ids."
    Card                = 0xD0600000,   "Serial number of an ECard."
    CardType            = 0xD0600001,   "ECard type string."
    CardAtr             = 0xD0600002,   "ECard ATR data."
    MemorySize          = 0xD0600004,   "Size of the memory area of a Storage Card in bytes."
    MemoryBlock         = 0xD0600005,   \
        "Size of one block of memory area of a Storage Card in bytes."
    CardCap             = 0xD0600006,   "ECard capability data."
    ChipType            = 0xD0600007,   "Chip type data."
    Common              = 0xD0700000,   "RFU"
    TimeStamp           = 0xD0700001,   "Timestamp."
    Duration            = 0xD0700002,   "Duration."
    WarnList            = 0xD0700003,   "RFID communication warning list."
    Task                = 0xD0700004,   "RFU"
    OData               = 0xD0700005,   "Optimization data."
    Finger              = 0xD0800000,   "FingerPosition."
    FingerType          = 0xD0800001,   "Finger ImpressionType."
    FingerNistQuality   = 0xD0800002,   "NIST finger image quality value."
    FingerDryWet        = 0xD0800003,   "Finger humidity level."
    FingerFraction      = 0xD0800004,   "Finger fraction level."


class HWType(PrEnum):
    """ Hardware module types. """
    Peripherals     = 0,        "Peripheral controller device module."
    Scanner         = 1,        "Document scanner module."
    RFIDReader      = 2,        "RFID card reader module."
    ContactReader   = 3,        "Contact smart card reader module."
    MagneticReader  = 4,        "Magnetic stripe card reader module."


class PresenceState(PrEnum):
    """ Presence detection statuses.

    Refers to the presence of documents,  ECard chips,  fingers or face.
    Not  all  the states  will  be  reported  by the  different  kind of
    detectors.
    """
    Empty           = 0,        "No object detected."
    Moving          = 1,        "Movement is detected."
    NoMove          = 2,        "Document is still on the scanner's object window."
    Dirty           = 3,        "Platen needs cleaning."
    Present         = 4,        "Object is detected."
    Preparing       = 5,        "Preparing to scan."


class _VariantCallCodes(PrEnum):
    CallCodes       = 0x10040000
    Ref             = CallCodes
    Unref           = CallCodes +  1
    Duplicate       = CallCodes +  4
    Convert         = CallCodes +  8
    ChangeId        = CallCodes + 29
    Create          = CallCodes + 30
    Update          = CallCodes + 31
    UpdateData      = CallCodes + 32
    ChangeName      = CallCodes + 33
    GetInfo         = CallCodes + 34
    GetItem         = CallCodes + 35
    CutItem         = CallCodes + 36
    FindItem        = CallCodes + 37
    AddItem         = CallCodes + 38
    GetChild        = CallCodes + 39
    CutChild        = CallCodes + 40
    FindChild       = CallCodes + 41
    AddChild        = CallCodes + 42
    GetValue        = CallCodes + 19
    CutValue        = CallCodes + 20
    AddValue        = CallCodes + 22
    GetByPath       = CallCodes + 24
    ConvertByPath   = CallCodes + 26


class _StGXVariant(Structure):                  # pylint: disable=R0903
    pass


st_gxVARIANT = _POINTER(_StGXVariant)


class Frame:
    """
    Data for a quadrangle.  A quadrangle is in normal orientation if the
    coordinates of its top left corner (x1, y1) have the lowest values.

    :ivar x1, y1:       Coordinates of the top left corner.
    :ivar x2, y2:       Coordinates of the top right corner.
    :ivar x3, y3:       Coordinates of the bottom right corner.
    :ivar x4, y4:       Coordinates of the bottom left corner.
    """

    # pylint: disable=R0902

    def __init__(self, x1=0, y1=0, x2=0, y2=0, x3=0, y3=0, x4=0, y4=0):
        # pylint: disable=C0103, R0913
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.y4 = y4

    def __str__(self):
        return self.to_string()

    def to_string(self):
        """ Return string representation of the frame. """
        return f'({self.x1},{self.y1}),({self.x2},{self.y2}),' \
               f'({self.x3},{self.y3}),({self.x4},{self.y4})'


class VariantPos:
    """ Container of Variant list item and child indexing parameters. """

    class _Flags(PrEnum):
        ByIndex = 0x0002
        ById = 0x0001
        ByIndexAndId = 0x0003
        ByOrderAndId = 0x0004
        ByName = 0x0008
        ByIndexAndName = 0x000a
        ByOrderAndName = 0x0010
        Append = 0x0100
        Last = 0x0200

    def __init__(self, flags, ix, id_v):
        self.flags = flags  # Indexing flag
        self.ix = ix  # Index of the requested item
        self.id_v = id_v  # Id of the requested item
        self.name = None  # Name of the requested item

    @staticmethod
    def by_index(ix):
        """ Select the item with ordinal number of ix.

        :param ix:      The index.
        :return:        A Variant selection parameter.
        """
        return VariantPos(VariantPos._Flags.ByIndex, ix, 0)

    @staticmethod
    def by_id(id_v, ix=0):
        """
        Search for the item with ordinal number of ix among items having
        the same Ids.

        :param id_v:    The Id.
        :param ix:      The index.
        :return:        A Variant selection parameter.
        """
        return VariantPos(VariantPos._Flags.ByOrderAndId, ix, id_v)

    @staticmethod
    def by_name(name, ix=0):
        """
        Search for the item with ordinal number of ix among items having
        the same names.

        :param name:    The name.
        :param ix:      The index.
        :return:        A Variant selection parameter.
        """
        vpp = VariantPos(VariantPos._Flags.ByOrderAndName, ix, 0)
        vpp.name = name
        return vpp

    @staticmethod
    def last():
        """ Select the last item.

        :return:        A Variant selection parameter.
        """
        return VariantPos(VariantPos._Flags.Last, 0, 0)

    def append(self):
        """ Inserting after the index position.

        :return:        The modified Variant selection parameter.
        """
        self.flags |= VariantPos._Flags.Append
        return self


def _var_call(cmd, param):
    return prins.glob_call(0, cmd, param)


class VariantTypes(PrEnum):
    """ Available VariantTypes use it as Variant.Types.

    The values with AC and AS tags are usable for creation only. For
    AC types the value is automatically converted to the proper data
    type. For AS  types the value is automatically converted to  the
    proper string type.
    """

    # Basic types (size = size of one element in bytes, nitems = number of items)
    Null        = 0x00, "NULL type (size: 0; nitems: 1)"
    Int         = 0x01, "Integer type (size: 0, 1, 2, 4, 8; nitems: 1)"
    Uint        = 0x02, "Unsigned integer type (size: 0, 1, 2, 4, 8; nitems: 1)"
    Float       = 0x03, "Floating point type (size: 0, 4, 8; nitems: 1)"
    DateTime    = 0x04, "Datetime type (size: 0, 8; nitems: 1)"

    # Array types, bit 6 set defines the array type.
    # (size = size of the element in bytes, nitems = number of items)
    Array       = 0x40, "NULL type array /NULL array/ (size: 0; nitems: x)"
    IntArray    = 0x41, "Integer type array (size: 0, 1, 2, 4, 8; nitems: x)"
    UintArray   = 0x42, "Unsigned integer type array (size: 0, 1, 2, 4, 8; nitems: x)"
    FloatArray  = 0x43, "Floating point type array (size: 0, 4, 8; nitems: x)"
    DateTimeArray = 0x44, "Datetime type array (size: 0, 8; nitems: x)"

    # Other dynamically sized types
    List        = 0x80, "List type (size=nitems: number of items)"
    Binary      = 0x81, "Binary type (size=number of bytes; nitems: 1)"
    Ascii       = 0x82, "String type in ASCII format (size=number of chars; nitems: 1)"
    Unicode     = 0x83, "String type in unicode format (size=number of chars; nitems: 1)"
    Container   = 0x84, "Internally used binary structure (size=number of codes; nitems: 1)"

    # Types for creation operation only
    ACAscii     = 0x1082, "String type in ASCII format (size=number of chars; nitems: 1)"
    ACUnicode   = 0x1083, "String type in unicode format (size=number of chars; nitems: 1)"
    ASAscii     = 0x2082, "String type in ASCII format (size=number of chars; nitems: 1)"
    ASUnicode   = 0x2083, "String type in unicode format (size=number of chars; nitems: 1)"


class Variant:
    """ Class for variant data management.

    The Variant class stores references to the variant data objects.

    The  Variant  object  was  introduced  to  easily  form  dynamically
    expandable  complex data  structures  that  are usable  in different
    programming languages under various operational environments.
    The  Variant  object  is  the  basic  unit  of  these  complex  data
    structures, and it has the following important features:
      - Stores basic data types as well as arrays or strings.
      - Uses run-time type information  for automatic data conversion on
        user request.
      - Stores Id or name that can be used to identify data in a complex
        structure.
      - Stores children. The variants can be connected together in a way
        that they form a tree through parent-child relationships.
      - Uses  reference counting  to save  memory  and to form  a closed
        tree.
      - It can be a list,  in which the items are connected according to
        parent-children  hierarchy.  The list  and list  items  can have
        children too.

    """

    Types = VariantTypes

    def __iadd__(self, var):  # operator +=
        """ Append an item to the list type variant.

        If  the variant  type is  not list  but NULL  type,  this method
        automatically converts it. For other types an error is reported.

        The variant  lists  contain  references  to variants,  so if the
        appended item is  changed the modification  affects the  item in
        the list too. To avoid this behaviour the item can be duplicated
        before appending with the operator ~().

        item.value = 2
        list += ~item

        :param var:     The item to add to the list.
        :return:        The variant list object.
        """
        try:
            return self.add_list_item(var)
        except exceptions.InvalidParameter as exc:
            if self._get_type() != Variant.Types.Null:
                raise exc
        self.change_to_list()
        return self.add_list_item(var)

    def __invert__(self):  # operator ~
        """ Substitution operator to the duplicate() method. """
        return self.duplicate()

    def __getitem__(self, ix):  # operator []
        """ Substitution operator to the get_list_item() method. """
        return self.get_list_item(ix)

    def __setitem__(self, key, value):  # operator []
        """ Modify an item of the list type variant.

        :param key:     The position of the requested item.
        :param value:   The new value to set.
        :return:        The new value.
        """
        self.get_list_item(key).update(value)

    def __call__(self, *args, **kwargs):    # operator ()
        """ Return a child of a variant.

        If the requested child  is missing and  the index parameter is 0
        this method creates the child automatically.

        :param args:    The Id or name of the requested child.
                        The index of the requested child.
        :return:        The requested child.
        """
        ix = args[1] if len(args) > 1 and args[1] else 0
        if not isinstance(args[0], int) and not isinstance(args[0], str):
            raise exceptions.InvalidParameter(f"[pr22] Variant({type(args[0])}:{args[0]} ...)")
        try:
            return self.get_child(args[0], ix)
        except exceptions.EntryNotFound as exc:
            if ix: raise exc
        var = Variant(args[0], Variant.Types.Null)
        self.add_child(var)
        return var

    def __str__(self):
        try:    return self.to_string()
        except exceptions.General: return ''

    def __init__(self, idon=None, value=None):
        """ A new variant data.

        :param idon:    The Id or name of the variant.
        :param value:   The value of the variant.
        """
        self.var_data = None
        if idon is None and value is None:
            pass
        elif value is None and isinstance(idon, st_gxVARIANT):
            self.var_data = idon
        elif value is None and isinstance(idon, Variant):
            self.var_data = idon.duplicate().var_data
        elif isinstance(idon, str):
            self._construct(0, idon, value)
        elif isinstance(idon, int):
            self._construct(idon, None, value)
        else:
            raise exceptions.InvalidParameter(
                f"[pr22] Variant({type(idon)}:{idon}, {type(value)}:{value})")

    def __del__(self):
        """ Finalizer. """
        try:    self.leave()
        except exceptions.General: pass

    def __enter__(self):
        """ Enter the runtime context. """
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """ Exit the runtime context. """
        try:    self.leave()
        except exceptions.General: pass
        return False

    def leave(self):
        """ Finish working with the actual variant object.

        The object became an empty variant object. Empty variants cannot
        be modified without using a create() method.

        :return:        self
        """
        if self.var_data is not None:
            _var_call(_VariantCallCodes.Unref, self.var_data)
        del self.var_data
        self.var_data = None
        return self

    def _construct(self, id_v, name, value):
        par = self._prepare_data(value)
        return self._do_create(id_v, name, *par)

    def _do_create(self, id_v, name, type_=Types.Null, size=0, data=None, nitems=1):
        self.leave()
        if data is not None and not isinstance(data, _Pointer): data = _pointer(data)

        cvp = Variant._StgxVariantUpdate(None, id_v, name, type_, size, nitems,
                                         cast(data, c_void_p))
        _var_call(_VariantCallCodes.Create, cvp)
        self.var_data = cvp.variant
        return self

    def _do_update(self, type_, size, data, nitems=1):
        if data is not None and not isinstance(data, _Pointer): data = _pointer(data)

        uvp = Variant._StgxVariantUpdate(self.var_data, 0, None, type_, size, nitems,
                                         cast(data, c_void_p))
        _var_call(_VariantCallCodes.UpdateData, uvp)
        return self

    def _prepare_data(self, value):
        if value is None: return Variant.Types.Null, 0, None, 0

        if isinstance(value, Variant.Types) and value in [Variant.Types.Null, Variant.Types.List]:
            return value, 0, None, 0
        if isinstance(value, int):
            if -(2**31) <= value < 2**31:
                return Variant.Types.Int, _sizeof(c_int), c_int(value), 1
            return Variant.Types.Int, _sizeof(c_longlong), c_longlong(value), 1
        if isinstance(value, float):
            return Variant.Types.Float, _sizeof(c_double), c_double(value), 1
        if isinstance(value, str):
            tmp = (c_wchar * (len(value) + 1))()
            tmp.value = value
            return Variant.Types.Unicode, len(tmp), tmp, 1
        if isinstance(value, Frame):
            tmp = (c_int * 8)(value.x1, value.y1, value.x2, value.y2,
                              value.x3, value.y3, value.x4, value.y4)
            return Variant.Types.IntArray, _sizeof(c_int), tmp, 8
        if isinstance(value, (list, tuple)):
            if not value:
                return Variant.Types.IntArray, _sizeof(c_int), None, 0
            tmp = (c_int * len(value))()
            for ix, val in enumerate(value): tmp[ix] = val
            return Variant.Types.IntArray, _sizeof(c_int), tmp, len(value)
        if isinstance(value, (bytes, bytearray)):
            if not value:
                return Variant.Types.UintArray, _sizeof(c_byte), None, 0
            tmp = (c_byte * len(value))()
            for ix, val in enumerate(value): tmp[ix] = val
            return Variant.Types.UintArray, _sizeof(c_byte), tmp, len(value)
        raise exceptions.InvalidParameter(f"[pr22] Variant.type({type(value)}:{value})")

    def update(self, value):
        """ Modify the type and the value of an existing variant.

        :param value:   The new value of the variant.
        :return:        self
        """
        par = self._prepare_data(value)
        return self._do_update(*par)

    def create(self, idon, secp, value=None):
        """ Create a typed variant structure.

        The method can be called with two or three parameters.  The last
        one is always  the value.  The first two  are the Id  and/or the
        name of the variant. e.g.
            variant.create(id, name, value), or
            variant.create(id_or_name, value)

        :param idon:    The Id or name of the variant.
        :param secp:    The name or value of the variant.
        :param value:   The value of the variant.
        :return:        self
        """
        if value is not None: return self._construct(idon, secp, value)
        if isinstance(idon, int): return self._construct(idon, None, secp)
        if isinstance(idon, str): return self._construct(0, idon, secp)
        raise exceptions.InvalidParameter(f"[pr22] Variant.create({type(idon)}:{idon},"
                                          f" {type(secp)}:{secp}, {type(value)}:{value})")

    @property
    def n_items(self):
        """ Number of items in the variant.
 
        This value is useful for array and list type variants.
        """
        try:
            if not self.is_valid(): return 0
            param = Variant._StgxGetVariantInfo(variant=self.var_data)
            _var_call(_VariantCallCodes.GetInfo, param)
            return param.nitems
        except exceptions.General:
            return 0

    @property
    def n_children(self):
        """ Number of children in the variant. """
        try:
            if not self.is_valid(): return 0
            param = Variant._StgxGetVariantInfo(variant=self.var_data)
            _var_call(_VariantCallCodes.GetInfo, param)
            return param.children
        except exceptions.General:
            return 0

    def all_children(self):
        """ Generator for children. """
        for ix in range(self.n_children):
            child = self.get_child_by_index(ix)
            yield ix, child

    def all_items(self):
        """ Generator for items. """
        for ix in range(self.n_items):
            item = self.get_list_item(ix)
            yield ix, item

    def get_item_by_path(self, path):
        """ Return a variant from a tree.

        The variant  data type  can constitute  a tree structure:  every
        item in  the tree is  a variant.  These variants  can have child
        items that are also variants.  The trees can be traversed  level
        by level  with  the  help  of  get_child()  and  get_list_item()
        methods or the special operators (operator [] and operator()).

        If there is a need  to reach a  descendant variant  located on a
        lower level, this method should be used instead. The item in the
        tree can be obtained  by the path string  that defines the exact
        location of the requested variant and has the following format:

        condition[=value] [,condition[=value]]
                          [/condition[=value] [,condition[=value]]]

        The path contains separators:
        - the '/' separates the levels of the tree,
        - the ',' separates the search conditions of a node,
        - the '=' signs that a value follows,

        and identifiers:
        - the 'C' selects a child item,
        - the 'L' selects a list item,
        - the 'X' signs that the value defines the index of the item,
        - the 'D' signs that the value defines the Id of the item,
        - the 'N' signs that the value defines the name of the item,
        - the 'V' signs that the value defines the value of the item.

        The values are used as 32-bit integers except 'name' values that
        have to be quoted with " or ' character; and 'value' values that
        may  be  quoted  with  " or '  character  to  sign  that  string
        comparison is required. Indexing is made by order.

        :param path:    The path string.
        :return:        The requested descendant item.
        """
        param = Variant._StgxGetVariantByPath(self.var_data, path, None)
        _var_call(_VariantCallCodes.GetByPath, param)
        return Variant(param.item)

    def add_child(self, item, pos=None):
        """ Add a child element to the variant.

        :param item:    The new child to add to the children list.
        :param pos:     The  VariantPos  position  where  to  insert  or
                        append the new child.
        :return:        self
        """
        if pos is None: pos = VariantPos.last()
        icp = Variant._StgxVariantItem(self.var_data, pos.flags,
            pos.id_v, pos.ix, pos.name, item.var_data)
        _var_call(_VariantCallCodes.AddChild, icp)
        return self

    def get_child(self, pos, ix_=0):
        """ Return a child of a variant.

        :param pos:     The Id, name or VariantPos position of the child
                        variant.
        :param ix_:     The index of the requested child.
        :return:        The requested child.
        """
        if isinstance(pos, int): pos = VariantPos.by_id(pos, ix_)
        elif isinstance(pos, str): pos = VariantPos.by_name(pos, ix_)
        if not isinstance(pos, VariantPos):
            raise exceptions.InvalidParameter(f"[pr22] Variant.get_child({type(pos)}:{pos}, ...)")
        ivp  = Variant._StgxVariantItem(self.var_data, pos.flags,
            pos.id_v, pos.ix, pos.name, None)
        _var_call(_VariantCallCodes.GetChild, ivp)
        return Variant(ivp.item)

    def get_child_by_index(self, ix):
        """ Return a child of a variant.

        :param ix:      The index of the requested child.
        :return:        The requested child.
        """
        return self.get_child(VariantPos.by_index(ix))

    def add_list_item(self, item, pos=None):
        """ Add an item to the list type variant.

        The variant  lists  contain  references  to variants,  so if the
        appended item is  changed the modification  affects the  item in
        the list too. To avoid this behaviour the item can be duplicated
        before appending with the duplicate() method.

        :param item:    The item to add to the list.
        :param pos:     The  VariantPos  position  where  to  insert  or
                        append the new item.
        :return:        The variant list object.
        """
        if pos is None: pos = VariantPos.last()
        ivp = Variant._StgxVariantItem(self.var_data, pos.flags,
            pos.id_v, pos.ix, pos.name, item.var_data)
        _var_call(_VariantCallCodes.AddItem, ivp)
        return self

    def get_list_item(self, pos):
        """ Return an item of the list type variant.

        :param pos:     The index or VariantPos position  of the variant
                        list item.
        :return:        The requested item.
        """
        if isinstance(pos, int): pos = VariantPos.by_index(pos)
        if not isinstance(pos, VariantPos):
            raise exceptions.InvalidParameter(f"[pr22] Variant.get_list_item({type(pos)}:{pos})")
        ivp  = Variant._StgxVariantItem(self.var_data, pos.flags,
            pos.id_v, pos.ix, pos.name, None)
        _var_call(_VariantCallCodes.GetItem, ivp)
        return Variant(ivp.item)

    def _get_data(self, type_, target, tgtlen, size=0, nitems=0):
        if size == 0: size = tgtlen
        if nitems == 0: nitems = 1
        param = Variant._StgxConvertVariant(self.var_data, 0, type_, size, nitems, target, tgtlen)
        return _var_call(_VariantCallCodes.Convert, param)

    @property
    def size(self):
        """ The item size of the variant. """
        try:
            if not self.is_valid(): return 0
            ivp = Variant._StgxGetVariantInfo(variant=self.var_data)
            _var_call(_VariantCallCodes.GetInfo, ivp)
            return ivp.size
        except exceptions.General:
            return 0

    def to_int(self):
        """ Return the value of the variant converted to integer.
     
        :return:        The value of the variant converted to int.
        """
        target = c_longlong()
        tgtlen = _sizeof(c_longlong)
        self._get_data(Variant.Types.Int, cast(_pointer(target), c_void_p), tgtlen)
        return target.value

    def to_float(self):
        """ Return the value of the variant converted to floating point.

        :return:        The value of the variant converted to float.
        """
        target = c_double()
        tgtlen = _sizeof(c_double)
        self._get_data(Variant.Types.Float, cast(_pointer(target), c_void_p), tgtlen)
        return target.value

    def to_int_array(self):
        """ Return the value of the integer array variant.

        :return:        The value of the integer array variant converted
                        to list of int values.
        """
        nitems = self.n_items
        if nitems <= 0: return []
        int_arr = (c_int * nitems)()
        target = cast(int_arr, c_void_p)
        tgtlen = _sizeof(c_int) * nitems
        self._get_data(Variant.Types.IntArray, target, tgtlen, _sizeof(c_int), nitems)
        return list(int_arr)

    def to_byte_array(self):
        """ Return the value of the byte array variant.

        :return:        The value of the variant converted to bytearray.
        """
        nitems, size = self.n_items, self.size
        if nitems*size <= 0: return bytearray()
        nitems *= size
        byte_arr = (c_byte * nitems)()
        target = cast(byte_arr, c_void_p)
        tgtlen = _sizeof(c_byte) * nitems
        self._get_data(Variant.Types.UintArray, target, tgtlen, _sizeof(c_byte), nitems)
        return bytearray(byte_arr)

    def to_string(self):
        """ Return the value of the variant converted to string.

        :return:        The value of the variant converted to str.
        """
        size = self.size + 64
        wchar_arr = (c_wchar * size)()
        target = cast(wchar_arr, c_void_p)
        tgtlen = _sizeof(c_wchar) * size
        self._get_data(Variant.Types.Unicode, target, tgtlen)
        return wchar_arr.value

    def to_frame(self):
        """ Return the value of the variant converted to frame.

        :return:        The value of the variant converted to Frame.
        """
        frame = (c_int * 8)()
        target = cast(frame, c_void_p)
        tgtlen = _sizeof(frame)
        size = _sizeof(c_int)
        self._get_data(Variant.Types.IntArray, target, tgtlen, size, 8)
        return Frame(*frame)

    def _get_value(self):
        """ The value of the variant. """
        typ = self._get_type()
        if typ in [Variant.Types.Int, Variant.Types.Uint]: return self.to_int()
        if typ in [Variant.Types.DateTime, Variant.Types.Ascii, Variant.Types.Unicode]:
            return self.to_string()
        if typ == Variant.Types.IntArray: return self.to_int_array()
        if typ in [Variant.Types.Binary, Variant.Types.UintArray]:
            return self.to_byte_array()
        if typ == Variant.Types.Float: return self.to_float()
        if typ == Variant.Types.Null: return None
        raise exceptions.InvalidParameter(f"[pr22] Unable to convert Variant.type({typ})")

    def is_valid(self):
        """ Return if the variant is valid or empty.

        :return:        True if the variant  is valid or false  if it is
                        empty.
        """
        return self.var_data is not None

    def _get_id(self):
        """ The Id of the variant. """
        try:
            if not self.is_valid(): return -1
            gvi = Variant._StgxGetVariantInfo(variant=self.var_data)
            _var_call(_VariantCallCodes.GetInfo, gvi)
            return gvi.idv if gvi.idv >= 0 else gvi.idv + 0x1_0000_0000
        except exceptions.General:
            return -1

    def _t_id(self):
        # for debugging purposes
        idv = self._get_id()
        if VariantId.has_value(idv): return VariantId(idv)
        return chr(idv) if 0x20 < idv < 0x80 else hex(idv)

    def _set_id(self, id_v):
        cvp = Variant._StgxVariantUpdate(variant=self.var_data, idv=c_int(id_v))
        _var_call(_VariantCallCodes.ChangeId, cvp)

    def _get_name(self):
        """ The name of the variant. """
        try:
            if not self.is_valid(): return ""
            namebuff = (c_wchar * 256)()
            gvi = Variant._StgxGetVariantInfo(variant=self.var_data,
                namebuff=cast(namebuff, c_wchar_p), namebuffsize=256)
            _var_call(_VariantCallCodes.GetInfo, gvi)
            return str(namebuff.value)
        except exceptions.General:
            return ""

    def _set_name(self, name):
        cvp = Variant._StgxVariantUpdate(variant=self.var_data, name=c_wchar_p(name))
        _var_call(_VariantCallCodes.ChangeName, cvp)

    def _get_type(self):
        """ The type of the variant. """
        try:
            if not self.is_valid(): return Variant.Types.Null
            gvi = Variant._StgxGetVariantInfo(variant=self.var_data)
            _var_call(_VariantCallCodes.GetInfo, gvi)
            return Variant.Types(gvi.type)
        except exceptions.General:
            return Variant.Types.Null

    def new_ref(self):
        """ Reference an existing variant to enable multiple disposing.

        :return:        The new variant object references this variant.
        """
        _var_call(_VariantCallCodes.Ref, self.var_data)
        return Variant(self.var_data)

    def duplicate(self):
        """ Duplicate, copy the variant and all of its descendants.

        The Variant  class stores  references to  variant data  objects.
        Modifying  the data  structure  of a  variant  affects  all  the
        variables  that  references  the same  memory area.  In order to
        avoid  this  behaviour  the  variant  can be  duplicated  before
        modification.

        :return: The variant object references the copy of this variant.
        """
        dvp = Variant._StgxDuplicateVariant(self.var_data, None)
        _var_call(_VariantCallCodes.Duplicate, dvp)
        return Variant(dvp.target)

    def clear(self):
        """ Modify an existing variant to NULL type.

        :return:        self
        """
        return self.update(None)

    def create_list(self, id_v, name):
        """ Create a list type variant structure.

        :param id_v:    The Id of the variant.
        :param name:    The name of the variant.
        :return:        self
        """
        return self._construct(id_v, name, Variant.Types.List)

    def change_to_list(self):
        """ Modify an existing variant to list type.

        :return:        self
        """
        return self.update(Variant.Types.List)

    ID = property(_get_id, _set_id)
    name = property(_get_name, _set_name)
    value = property(_get_value, update)
    var_type = property(_get_type)
    _tID = property(_t_id)

    class _StgxGetVariantInfo(Structure):       # pylint: disable=R0903
        _fields_ = [("variant", st_gxVARIANT), ("idv", c_int),
            ("namebuff", c_wchar_p), ("namebuffsize", c_int), ("type", c_int),
            ("size", c_int), ("nitems", c_int), ("children", c_int)]

    class _StgxVariantItem(Structure):          # pylint: disable=R0903
        _fields_ = [("parent", st_gxVARIANT), ("flags", c_int), ("idv", c_int),
                    ("ix", c_int), ("name", c_wchar_p), ("item", st_gxVARIANT)]

    class _StgxVariantUpdate(Structure):        # pylint: disable=R0903
        _fields_ = [("variant", st_gxVARIANT), ("idv", c_int), ("name", c_wchar_p),
            ("type", c_int), ("size", c_int), ("nitems", c_int), ("data", c_void_p)]

    class _StgxGetVariantByPath(Structure):     # pylint: disable=R0903
        _fields_ = [("root", st_gxVARIANT), ("path", c_wchar_p), ("item", st_gxVARIANT)]

    class _StgxConvertVariant(Structure):   # pylint: disable=R0903
        _fields_ = [("variant", st_gxVARIANT), ("idv", c_int),
                    ("type", c_int), ("size", c_int), ("nitems", c_int),
                    ("target", c_void_p), ("tgtlen", c_int)]

    class _StgxDuplicateVariant(Structure):  # pylint: disable=R0903
        _fields_ = [("source", st_gxVARIANT), ("target", st_gxVARIANT)]
