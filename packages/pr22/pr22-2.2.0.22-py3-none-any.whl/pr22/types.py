#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" General types. """

__version__ = '2.2.0.22'

from enum       import IntEnum, EnumMeta
from ctypes     import RTLD_GLOBAL as _RTLD_GLOBAL, Structure, pointer as _pointer
from platform   import system


class _NoGx:                                    # pylint: disable=R0903
    @staticmethod
    def gx_call(handle, function, arguments):   # pylint: disable=W0613
        """ Internally used method. """
        return 0


try:
    if system() == 'Linux':
        from ctypes import CDLL
        _gxsdLibrary = CDLL("libgxsd.so.7", _RTLD_GLOBAL)
    if system() == 'Windows':
        from ctypes import WinDLL
        _gxsdLibrary = WinDLL("gxsd7")
except FileNotFoundError:
    _gxsdLibrary = _NoGx


class _PrEnumType(EnumMeta):

    def __dir__(cls):
        return cls._member_names_ + cls.__dir__(cls)
#        return super().__dir__()


class PrEnum(IntEnum, metaclass=_PrEnumType):
    """ Enum converter class. """

    def __new__(cls, value, doc=None):
        self = int.__new__(cls, value)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self

    def __dir__(self):
        if self is not PrEnum: return []
        return ['has_value', 'has_key', 'compat_str', 'parse']

    def __str__(self):
        return self.name

    @classmethod
    def has_value(cls, value):
        """ Return whether enum contains a numeric value. """
        return value in cls.__members__.values()

    @classmethod
    def has_key(cls, value):
        """ Return whether enum defines the given named value. """
        return value in cls.__members__

    @classmethod
    def compat_str(cls, value):
        """ Return a forward compatible string representation of the enum.

        The function can handle non-covered numeric values too.
        """
        if cls.has_value(value): return cls(value).name
        return cls.__name__ + str(value)

    @classmethod
    def parse(cls, value):
        """ Convert value to enum. """
        if cls.has_value(value): return cls(value)
        if cls.has_key(value): return cls[value]
        if isinstance(value, str):
            typname = cls.__name__
            lnt = len(typname)
            if value[:lnt] == typname: return cls.parse(int(value[lnt:]))
            raise ValueError("[pr22] Enum string not found!")
        return value


def gx_call(handle, function, arguments):
    """ Call a module process with the specified parameters.

    :param handle:      Handle of an opened module or special system
                        handle.
    :param function:    Identifier of the function.
    :param arguments:   Parameters to give for the function.
    :return:            Module defined, usually non-zero on success.
    """
    if isinstance(arguments, Structure) and hasattr(arguments, "_fields_"):
        p_arguments = _pointer(arguments)
    else:
        p_arguments = arguments

    ret = _gxsdLibrary.gx_call(handle, int(function), p_arguments)
    return ret  # on error returns 0


def chk_ver(tver):
    """ Check file version compatibility. """
    if tver != __version__:
        raise RuntimeError(f'Version mix-up {tver} vs. {__version__}')
