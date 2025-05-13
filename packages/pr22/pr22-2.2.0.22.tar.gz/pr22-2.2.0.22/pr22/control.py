#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Controller classes of miscellaneous hardware modules. """

__version__ = '2.2.0.22'

from ctypes import c_void_p, c_int, c_byte, pointer as _pointer, Structure, cast

from pr22 import exceptions
from pr22.prins import CommonApi, PrApi, GxMem
from pr22.types import PrEnum, chk_ver
from pr22.util  import Variant, st_gxVARIANT
chk_ver(__version__)


class DeviceInformation:
    """ Class for storing information on Peripherals. """

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        param = DeviceInformation._StprGetDeviceInfo(None)
        api_handle.api_call(CommonApi.GetDeviceInfo, param)
        variant = Variant(param.devInfo)
        self._dev_name = variant[0].to_string()
        self.info = variant.get_item_by_path("L/V=0")

    def to_variant(self):
        """ Return low level data to access special device information.

        :return:            Low level util.Variant data.
        """
        return self.info

    device_name = property(lambda self: self._dev_name, None, None,
                           "Name of the device.")

    class _StprGetDeviceInfo(Structure):  # pylint: disable=R0903
        _fields_ = [("devInfo", st_gxVARIANT)]


class PowerControl:
    """ Power controller component. """

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        self.prapi = api_handle

    def suspend(self):
        """ Suspend the device.

        :return:            self
        """
        self.prapi.api_call(CommonApi.Suspend, None)
        return self

    def wakeup(self):
        """ Wake up the device.

        :return:            self
        """
        self.prapi.api_call(CommonApi.WakeUp, None)
        return self


class UserData:
    """ User storage data controller class. """

    def __init__(self, api_handle):
        """ Do not create instances directly. """
        self.prapi = api_handle

    def get_size(self):
        """ Return the size of the user data.

        :return:            Size in bytes.
         """
        udi = UserData._StprGetUserDataInfo(0, 0)
        self.prapi.api_call(PrApi.UserDataInfo, udi)
        return udi.NBlocks * udi.SBlock

    def read(self):
        """ Return the stored user data.

        :return:            c_byte array.
        """
        udi = UserData._StprGetUserDataInfo(0, 0)
        self.prapi.api_call(PrApi.UserDataInfo, udi)

        rud = UserData._StprReadWriteUserData(0, udi.NBlocks, None)
        self.prapi.api_call(PrApi.ReadUserData, rud)

        return GxMem.to_bytes(rud.Data, udi.NBlocks * udi.SBlock)

    def write(self, source):
        """ Write user data to the device.
     
        :param source:      The data to store.
        :return:            self
        """
        udi = UserData._StprGetUserDataInfo(0, 0)
        self.prapi.api_call(PrApi.UserDataInfo, udi)

        datasize = udi.NBlocks * udi.SBlock
        if len(source) > datasize:
            raise exceptions.DataOutOfRange('[pr22] data length')

        tbuf = (c_byte * datasize)()
        if isinstance(source, str):
            for ix, val in enumerate(source):
                tbuf[ix] = c_byte(ord(val))
        else:
            for ix, val in enumerate(source):
                tbuf[ix] = c_byte(val)

        for ix in range(len(source), datasize):
            tbuf[ix] = 0

        wud = UserData._StprReadWriteUserData(0, udi.NBlocks, cast(_pointer(tbuf), c_void_p))
        self.prapi.api_call(PrApi.WriteUserData, wud)
        return self

    class _StprGetUserDataInfo(Structure):      # pylint: disable=R0903
        _fields_ = [("NBlocks", c_int), ("SBlock", c_int)]

    class _StprReadWriteUserData(Structure):    # pylint: disable=R0903
        _fields_ = [("FirstBlock", c_int), ("NBlocks", c_int), ("Data", c_void_p)]


class StatusLedColor(PrEnum):
    """ Usable StatusLedColor use it as StatusLed.Color.

    Both LED types and LED states are enumerated. LED type provides
    information and cannot be set. LED state is for setting.
    """
    Off     = 0,    "LED state: turn off."
    OG      = 0x02, "The LED type is bi-color: green/orange."
    ORG     = 0x03, "The LED type is tri-color: red/green/orange."
    System  = 0x10, "LED type. The LED is controlled by the system only."
    Green   = 0x81, "State/type. The color of the LED is green."
    Red     = 0x82, "State/type. The color of the LED is red."

    Orange  = 0x83, "State/type. The color of the LED is orange."
    Blue    = 0x84, "State/type. The color of the LED is blue."
    Auto    = 0xac, "LED state: turn on automatic LED control."
    On      = 0xff, "LED state: turn on any of the available lights."
    Buzzer  = 0xc0, "State/type. Buzzer."


class StatusLed:
    """ Controller for the status LEDs and buzzers. """

    Color = StatusLedColor

    def __init__(self, api_handle, color, index):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self._color = color
        self._index = index

    def turn(self, color=Color.On):
        """ Set the LED state.

        :param color:       Color to switch to.
        :return:            self
        """
        if self._color == StatusLed.Color.System:
            raise exceptions.ProgramFault("[pr22] This LED is controlled by the system!")
        if self._color == StatusLed.Color.Buzzer:
            raise exceptions.InvalidFunction("[pr22] Buzzer state cannot set!")
        if color not in [StatusLed.Color.On, StatusLed.Color.Off]:
            if self._color == StatusLed.Color.OG:
                if color not in [StatusLed.Color.Orange, StatusLed.Color.Green]:
                    raise exceptions.InvalidParameter("[pr22] Invalid color!")
            elif self._color == StatusLed.Color.ORG:
                if color not in [StatusLed.Color.Orange, StatusLed.Color.Red,
                                 StatusLed.Color.Green]:
                    raise exceptions.InvalidParameter("[pr22] Invalid color!")
            else:
                if color != self._color:
                    raise exceptions.InvalidParameter("[pr22] Invalid color!")

        param = StatusLed._StprSetStatusLed(self._index, color)
        self.prapi.api_call(CommonApi.SetStatus, param)
        return self

    def blink(self, sample, iteration, color=Color.On):
        """ Start a LED blinking or buzzer beeping background task.
     
        :param sample:      Durations of ON and OFF states in millisecs.
        :param iteration:   Number of repetitions (0 for infinite).
        :param color:       The Color to blink.
        :return:            self
        """
        tmp = (c_int * len(sample))()
        for ix, val in enumerate(sample): tmp[ix] = val

        param = StatusLed._StprBlinkStatus(1, iteration, self._index, color, len(sample),
                                 cast(tmp, c_void_p))
        self.prapi.api_call(CommonApi.BlinkStatus, param)
        return self

    light = property(lambda self: StatusLed.Color(self._color), None, None, "The LED type.")

    class _StprSetStatusLed(Structure):  # pylint: disable=R0903
        _fields_ = [("LedMask", c_int), ("Color", c_int)]

    class _StprBlinkStatus(Structure):  # pylint: disable=R0903
        _fields_ = [("Coding", c_int), ("Iteration", c_int), ("Mask", c_int),
                    ("Type", c_int), ("DataLength", c_int), ("Data", c_void_p)]
