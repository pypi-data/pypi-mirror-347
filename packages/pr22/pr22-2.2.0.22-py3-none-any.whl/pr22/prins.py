#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Internally used api call codes, classes and parameters. """

__version__ = '2.2.0.22'

from ctypes     import c_wchar, c_void_p, c_wchar_p, c_int, c_uint32, c_byte
from ctypes     import Structure, cast, memmove as _memmove

from pr22       import exceptions
from pr22.types import PrEnum, chk_ver, gx_call
chk_ver(__version__)


class ImageType(PrEnum):
    """ Image types. """
    Original = 0
    Document = 1
    Preview  = 2
    Finger   = 3


class ModuleCallCodes(PrEnum):
    """ Module call codes. """
    CallCodes            = 0x10030000

    OpenModule           = 0x10030000
    CloseHandle          = 0x10030002

    RefHandle            = 0x10030006
    GetModuleProperty    = 0x10030008
    SetModuleProperty    = 0x1003000A

    SaveModuleProperties = 0x1003000e
    GetModuleProperties  = 0x10030008

    MemoryCallCodes      = 0x10020000
    LoadBinary           = 0x10020008
    SaveBinary           = 0x10020009


class CommonApi(PrEnum):
    """ Module call codes. """
    GROUPCOMMON      = 0x2008c000
    GetDeviceList    = GROUPCOMMON
    UseDevice        = GROUPCOMMON +  1
    SetEventFunction = GROUPCOMMON +  2
    GetDeviceInfo    = GROUPCOMMON +  3
    SelfTest         = GROUPCOMMON +  4
    GetProcStatus    = GROUPCOMMON +  5
    StopProc         = GROUPCOMMON +  6
    WaitProc         = GROUPCOMMON +  7
    Suspend          = GROUPCOMMON +  8
    WakeUp           = GROUPCOMMON +  9
    SetStatus        = GROUPCOMMON + 10
    BlinkStatus      = GROUPCOMMON + 11
    StartFrvTask     = GROUPCOMMON + 15


class PrApi(PrEnum):
    """ Module call codes. """
    GROUPPRAPI           = 0x20080000
    Capture              = GROUPPRAPI +  13
    CaptureStart         = GROUPPRAPI +  14
    Iscalibrated         = GROUPPRAPI +  61
    SetPagelight         = GROUPPRAPI +  62
    GetLightmask         = GROUPPRAPI +  65
    GetRfidFile          = GROUPPRAPI +  73
    UserDataInfo         = GROUPPRAPI +  94
    ReadUserData         = GROUPPRAPI +  95
    WriteUserData        = GROUPPRAPI +  96
    GetOCRV              = GROUPPRAPI +  97
    GetFieldImageV       = GROUPPRAPI + 107
    CompareFaceV         = GROUPPRAPI + 108
    GetDocRootV          = GROUPPRAPI + 113
    ConnectRfidCard      = GROUPPRAPI + 118
    DisconnectRfidCard   = GROUPPRAPI + 120
    CheckFileHash        = GROUPPRAPI + 128
    GetImage             = GROUPPRAPI + 130
    GetRfidCardInfo      = GROUPPRAPI + 134
    InitTerminalAuth     = GROUPPRAPI + 142
    CompleteTerminalAuth = GROUPPRAPI + 144
    DecodeLatentImage    = GROUPPRAPI + 154
    GetNextAuth          = GROUPPRAPI + 159
    LoadCertFromStore    = GROUPPRAPI + 165
    DoAuth               = GROUPPRAPI + 170
    GetApplications      = GROUPPRAPI + 174
    ResetDocument        = GROUPPRAPI + 176
    GetFileStart         = GROUPPRAPI + 177
    SaveDocumentToMem    = GROUPPRAPI + 182
    LoadDocumentFromMem  = GROUPPRAPI + 183
    Analyze              = GROUPPRAPI + 184
    GetReaderCardList    = GROUPPRAPI + 186
    GetFileList          = GROUPPRAPI + 187
    ClearCertListScope   = GROUPPRAPI + 191
    LoadCertScope        = GROUPPRAPI + 192
    OpenCardReader       = GROUPPRAPI + 193
    CloseCardReader      = GROUPPRAPI + 194
    ConvertFileNames     = GROUPPRAPI + 195
    GetAuthResult        = GROUPPRAPI + 196
    GetLicenses          = GROUPPRAPI + 197
    GetLicenseDate       = GROUPPRAPI + 198
    GetEngineInfo        = GROUPPRAPI + 199
    MergeDocuments       = GROUPPRAPI + 200
    AnalyzeC             = GROUPPRAPI + 201
    GetDataFormat        = GROUPPRAPI + 202
    StartScanning        = GROUPPRAPI + 203
    StartEcardReading    = GROUPPRAPI + 204
    Scan                 = GROUPPRAPI + 207


class CertScope(PrEnum):
    """ Certificate scopes. """
    Global         = 0
    DocumentReader = 1
    CardReader     = 2
    Card           = 3


def glob_call(handle, callcode, params):
    """ Call the gx system to do some functionality. """
    handle = _gxHANDLE(handle)
    if not gx_call(handle, callcode, params):
        exceptions.throw_exception()
    return 0


class GxMem:
    """ Gx memory handler functions. """

    @staticmethod
    def free_mem(addr):
        """ Free up internally allocated memory. """
        if not addr: return

        param = GxMem._StgxGlobalRealloc(cast(addr, c_void_p), 0)
        glob_call(0, ModuleCallCodes.MemoryCallCodes, param)

    @staticmethod
    def to_bytes(address, lengh):
        """ Convert gx memory to byte array. """
        try:
            data = (c_byte * lengh)()
            _memmove(data, address, lengh)
            return data
        finally:
            GxMem.free_mem(address)

    @staticmethod
    def to_list(conv_type, address, nitems):
        """ Convert gx memory to a list. """
        try:
            return [conv_type(address[ix]) for ix in range(nitems)]
        finally:
            GxMem.free_mem(address)

    class _StgxGlobalRealloc(Structure):    # pylint: disable=R0903
        _fields_ = [("buffer", c_void_p), ("size", c_int)]


# Handle of a GX module.
class _gxHANDLE(Structure):                     # pylint: disable=R0903
    _fields_ = [("handle", c_uint32)]


class GxModule:
    """ Low level module control class. """

    def __init__(self, module=None, group="default"):
        self.handle = 0
        if module:
            self.open(module, group)

    def __del__(self):
        """ Finalizer. """
        try:    self.close()
        except exceptions.General: pass
        self.handle = 0

    def is_valid(self):
        """ Check if the handle of the module is valid. """
        return self.handle != 0

    def open(self, modulename, groupname):
        """ Open a gx system compatible module.

        :param modulename:  Name of the module.
        :param groupname:   Property branch in the property tree.
        :return:            self
        """
        self.close()

        params = GxModule._StgxOpenModule(modulename, groupname)
        glob_call(0, ModuleCallCodes.OpenModule, params)
        self.handle = params.handle.handle
        return self

    def close(self):
        """ Close the previously opened module. """

        if not self.handle: return

        params = GxModule._StgxCloseModule()
        params.handle.handle = self.handle
        glob_call(0, ModuleCallCodes.CloseHandle, params)
        self.handle = 0

    def get_property(self, name):
        """ Return a property value.

        :param name:        The name string of the property.
        :return:            The string value of the property.
        """
        wchar_array = (c_wchar * 1024)()
        params = GxModule._StgxGetModuleProperty(c_wchar_p(name),
                                                 cast(wchar_array, c_wchar_p), 1024)
        glob_call(self.handle, ModuleCallCodes.GetModuleProperty, params)
        return params.value

    def set_property(self, name, value):
        """ Set a property value.

        :param name:        The name string of the property.
        :param value:       The value of the property.
        :return:            self
        """
        param = GxModule._StgxSetModuleProperty(c_wchar_p(name), c_wchar_p(str(value)))
        glob_call(self.handle, ModuleCallCodes.SetModuleProperty, param)
        return self

    def save_properties(self, name, level):
        """ Save current module properties to the gxsd.dat file.

        :param name:        Location of properties  in the property tree
                            to save to.
        :param level:       Detail level  of properties to save.  (0 for
                            basic properties, 100 for all properties and
                            -1 for modified properties only.)
        :return:            self
        """
        param = GxModule._StgxSaveModuleProperties(c_wchar_p(name), c_int(level))
        glob_call(self.handle, ModuleCallCodes.SaveModuleProperties, param)
        return self

    def api_call(self, callcode, params):
        """ Call the gx system to do some functionality. """
        return glob_call(self.handle, callcode, params)

    def ref_handle(self):
        """ Reference a handle. """
        params = _gxHANDLE(self.handle)
        glob_call(0, ModuleCallCodes.RefHandle, params)
        return self

    class _StgxOpenModule(Structure):       # pylint: disable=R0903
        _fields_ = [("modulename", c_wchar_p), ("groupname", c_wchar_p), ("handle", _gxHANDLE)]

    class _StgxCloseModule(Structure):      # pylint: disable=R0903
        _fields_ = [("handle", _gxHANDLE)]

    class _StgxGetModuleProperty(Structure):  # pylint: disable=R0903
        _fields_ = [("name", c_wchar_p), ("value", c_wchar_p), ("maxlen", c_int)]

    class _StgxSetModuleProperty(Structure):  # pylint: disable=R0903
        _fields_ = [("name", c_wchar_p), ("value", c_wchar_p)]

    class _StgxSaveModuleProperties(Structure):  # pylint: disable=R0903
        _fields_ = [("name", c_wchar_p), ("level", c_int)]
