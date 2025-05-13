#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Exception classes and error identification constants. """

__version__ = '2.2.0.22'

from ctypes     import c_wchar, c_int, cast, c_wchar_p, Structure
from pr22.types import PrEnum, chk_ver, gx_call
chk_ver(__version__)

_GXCALL_GET_ERROR = 0x10010000


class ErrorCodes(PrEnum):
    """ System error codes. """
    NoErr       = 0x0000,       "No error."
    NoEnt       = 0x0002,       "Entry not found."
    NoMem       = 0x000c,       "Memory allocation error."
    Acces       = 0x000d,       "Permission denied."
    Fault       = 0x000e,       "Bad address or program error."
    Busy        = 0x0010,       "Resource busy."
    Exist       = 0x0011,       "File already exists."
    NoDev       = 0x0013,       "No such device."
    Inval       = 0x0016,       "Invalid parameter."
    Range       = 0x0022,       "Data out of range."
    Data        = 0x003D,       "No data available."
    Comm        = 0x0046,       "Communication error."
    TimedOut    = 0x006E,       "Function timed out."
    Open        = 0x1000,       "File open error."
    Creat       = 0x1001,       "File creation error."
    Read        = 0x1002,       "File read error."
    Write       = 0x1003,       "File write error."
    File        = 0x1004,       "Invalid data content."
    InvImg      = 0x1010,       "Invalid image."
    InvFunc     = 0x1011,       "Invalid function."
    HWKey       = 0x1012,       "Hardware key does not work properly."
    Version     = 0x1013,       "Invalid version."
    Assert      = 0x1014,       "Assertion occurred."
    Discon      = 0x1015,       "Device is disconnected."
    ImgProc     = 0x1016,       "Image processing failed."
    Auth        = 0x1017,       "Authenticity cannot be determined."
    Capture     = 0x20088001,   "Image capture error."
    WeakDev     = 0x20088005,   "Insufficient hardware configuration e.g.USB 1.0 port."
    CertExpired = 0x20088030,   "Certificate is expired."
    CertRevoked = 0x20088031,   "Certificate is revoked."
    Check       = 0x20088032,   "Validation checking failed."


def throw_exception(error_code=None, error_text=None):
    """ Throw an exception.

    :param error_code:  ErrorCodes value. This value determines the type
                        of exception raised. If it is None, the function
                        will use the underlying gx system error code and
                        message values.
    :param error_text:  Error message.
    """
    if error_code is None:
        errstr = (c_wchar * 1024)()
        param = _StgxGetErrorMessage(c_int(0), cast(errstr, c_wchar_p), c_int(1024))
        ret = gx_call(0, _GXCALL_GET_ERROR, param)
        if ret != 0:
            error_code = param.errcode
            error_text = errstr.value
        else:
            error_code = ErrorCodes.Open
            error_text = "[pr22] GXSD not found!"

    if not ErrorCodes.has_value(error_code): raise General(   error_code,    error_text )
    error_code = ErrorCodes(error_code)
    if error_code == ErrorCodes.NoErr:
        raise General(ErrorCodes.NoErr,                 "[pr22] Error is not specified!")
    if error_code == ErrorCodes.NoEnt:       raise EntryNotFound(            error_text )
    if error_code == ErrorCodes.NoMem:       raise MemoryAllocation(         error_text )
    if error_code == ErrorCodes.Acces:       raise PermissionDenied(         error_text )
    if error_code == ErrorCodes.Fault:       raise ProgramFault(             error_text )
    if error_code == ErrorCodes.Busy:        raise ResourceBusy(             error_text )
    if error_code == ErrorCodes.Exist:       raise FileExists(               error_text )
    if error_code == ErrorCodes.NoDev:       raise NoSuchDevice(             error_text )
    if error_code == ErrorCodes.Inval:       raise InvalidParameter(         error_text )
    if error_code == ErrorCodes.Range:       raise DataOutOfRange(           error_text )
    if error_code == ErrorCodes.Data:        raise NoDataAvailable(          error_text )
    if error_code == ErrorCodes.Comm:        raise CommunicationError(       error_text )
    if error_code == ErrorCodes.TimedOut:    raise FunctionTimedOut(         error_text )
    if error_code == ErrorCodes.InvImg:      raise InvalidImage(             error_text )
    if error_code == ErrorCodes.InvFunc:     raise InvalidFunction(          error_text )
    if error_code == ErrorCodes.HWKey:       raise HardwareKey(              error_text )
    if error_code == ErrorCodes.Version:     raise InvalidVersion(           error_text )
    if error_code == ErrorCodes.Assert:      raise AssertionOccurred(        error_text )
    if error_code == ErrorCodes.Discon:      raise DeviceIsDisconnected(     error_text )
    if error_code == ErrorCodes.ImgProc:     raise ImageProcessingFailed(    error_text )
    if error_code == ErrorCodes.Auth:        raise AuthenticityFailed(       error_text )
    if error_code == ErrorCodes.Open:        raise FileOpen(                 error_text )
    if error_code == ErrorCodes.Creat:       raise FileCreation(             error_text )
    if error_code == ErrorCodes.Read:        raise FileRead(                 error_text )
    if error_code == ErrorCodes.Write:       raise FileWrite(                error_text )
    if error_code == ErrorCodes.File:        raise InvalidFileContent(       error_text )
    if error_code == ErrorCodes.Capture:     raise ImageScanFailed(          error_text )
    if error_code == ErrorCodes.WeakDev:     raise InsufficientHardware(     error_text )
    if error_code == ErrorCodes.CertExpired: raise CertificateExpired(       error_text )
    if error_code == ErrorCodes.CertRevoked: raise CertificateRevoked(       error_text )
    if error_code == ErrorCodes.Check:       raise ValidationCheckingFailed( error_text )
    raise RuntimeError(f"Error code <{ErrorCodes.compat_str(error_code)}> Not handled!")


class _StgxGetErrorMessage(Structure):  # pylint: disable=R0903
    _fields_ = [("errcode", c_int), ("errstr", c_wchar_p), ("maxlen", c_int)]


class _PrExceptionType(type):

    def __dir__(cls):
        return cls.__dir__(cls)


class General(Exception, metaclass=_PrExceptionType):
    """ Base exception class for error handling. """

    def __init__(self, errcode=None, errtext=None):
        super(General, self).__init__()
        self.errcode = errcode
        self.errtext = errtext

    def __str__(self):
        return f"ERROR -> {ErrorCodes.compat_str(self.errcode)} : {self.message}"

    def __dir__(self):
        if self is not General: return []
        return dir(Exception) + ['message', 'error_code']

    message = property(
        lambda self: self.errtext if self.errtext else "[pr22] No error message specified!",
        None, None, "Last error message.")

    error_code = property(lambda self: self.errcode, None, None, "Error code of exception.")


class EntryNotFound(General):
    """ Entry not found exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.NoEnt, errtext)


class MemoryAllocation(General):
    """ Memory allocation exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.NoMem, errtext)


class PermissionDenied(General):
    """ Permission denied exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Acces, errtext)


class ProgramFault(General):
    """ Program fault exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Fault, errtext)


class ResourceBusy(General):
    """ Resource busy exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Busy, errtext)


class NoSuchDevice(General):
    """ No such device exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.NoDev, errtext)


class InvalidParameter(General):
    """ Invalid parameter exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Inval, errtext)


class DataOutOfRange(General):
    """ Data out of range exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Range, errtext)


class NoDataAvailable(General):
    """ No data available exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Data, errtext)


class CommunicationError(General):
    """ Communication error exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Comm, errtext)


class FunctionTimedOut(General):
    """ Function timed out exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.TimedOut, errtext)


class InvalidImage(General):
    """ Invalid image exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.InvImg, errtext)


class InvalidFunction(General):
    """ Invalid function exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.InvFunc, errtext)


class HardwareKey(General):
    """ Hardware key exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.HWKey, errtext)


class InvalidVersion(General):
    """ Invalid version exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Version, errtext)


class AssertionOccurred(General):
    """ Assertion occurred exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Assert, errtext)


class DeviceIsDisconnected(General):
    """ Device is disconnected exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Discon, errtext)


class ImageProcessingFailed(General):
    """ Image processing failed exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.ImgProc, errtext)


class AuthenticityFailed(General):
    """ Authenticity failed exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Auth, errtext)


class FileException(General):
    """ File exception. """

    def __init__(self, errcode=ErrorCodes.File, errtext=None):
        super().__init__(errcode, errtext)


class FileExists(FileException):
    """ File exists exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Exist, errtext)


class FileOpen(FileException):
    """ File open exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Open, errtext)


class FileCreation(FileException):
    """ File creation exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Creat, errtext)


class FileRead(FileException):
    """ File read exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Read, errtext)


class FileWrite(FileException):
    """ File write exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Write, errtext)


class InvalidFileContent(FileException):
    """ Invalid file content exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.File, errtext)


class ImageScanFailed(General):
    """ Image scan failed exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Capture, errtext)


class InsufficientHardware(General):
    """ Insufficient hardware configuration. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.WeakDev, errtext)


class CertificateExpired(General):
    """ Certificate expired exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.CertExpired, errtext)


class CertificateRevoked(General):
    """ Certificate revoked exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.CertRevoked, errtext)


class ValidationCheckingFailed(General):
    """ Validation checking failed exception. """

    def __init__(self, errtext=None):
        super().__init__(ErrorCodes.Check, errtext)
