#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Task data and task control classes. """

__version__ = '2.2.0.22'

from ctypes     import Structure, c_int

from pr22.types import chk_ver
from pr22.processing import FieldReference
from pr22.imaging import Light
from pr22.prins import CommonApi
from pr22.ecardhandling import FileId
from pr22 import exceptions
chk_ver(__version__)


class TaskControl:
    """ Process controller class.

    Returned by methods which start processes in background.
    """
    def __init__(self, handle=None, pid=0):
        """ Do not create instances directly. """
        self.api_handle = handle
        self.pid = pid

    def stop(self):
        """ Stop a previously started background task.
        
        :return:        self
        """
        if self.pid != 0:
            opr = TaskControl._StprProcess(self.pid, 0)
            self.api_handle.api_call(CommonApi.StopProc, opr)
            self.pid = opr.ProcessId
        return self

    def wait(self):
        """ Wait for a previously started background task.

        This method  has to be called  always,  even when  the task  has
        already  finished.  This  method  must  not  be called  directly
        inside  the ScanFinished  and ReadFinished events.  The intended
        use of the method is to schedule it  for later execution or call
        it from  another thread.  Calling it from  a Qt slot is also  an
        appropriate solution.
        """
        if self.pid != 0:
            opr = TaskControl._StprProcess(self.pid, 0)
            self.api_handle.api_call(CommonApi.WaitProc, opr)
            self.pid = 0

    def get_state(self):
        """
        Return the state of the previously started background task.

        :return:        percentage
        """
        try:
            opr = TaskControl._StprProcess(self.pid, -1)
            self.api_handle.api_call(CommonApi.GetProcStatus, opr)
            return opr.Status
        except exceptions.General:
            return 0

    class _StprProcess(Structure):              # pylint: disable=R0903
        _fields_ = [("ProcessId", c_int), ("Status", c_int)]


class FreerunTask:
    """ DocScanner freerun mode tasks. """

    def __init__(self, task):
        self.task = task

    @staticmethod
    def live_stream():
        """ Declares a live stream scanning task. """
        return FreerunTask(0x579ea8)

    @staticmethod
    def detection():
        """ Declares a document presence detection task. """
        return FreerunTask(0xde7ec7)


class DocScannerTask:
    """ List of image scanning requirements.

    The concerning Light values are defined in imaging.Light
    enumeration.
    """

    def __init__(self):
        self.lights = []
        self._window = 0

    def add(self, light):
        """ Append a Light to the list.

        :param light:   The requested Light.
        :return:        self
        """
        if light == int(Light.All): self.lights.clear()
        self.lights.append(light)
        return self

    def remove(self, light):
        """ Remove a Light from the list.

        :param light:   The Light not to scan.
        :return:        self
        """
        if light == int(Light.All): self.lights.clear()
        else:                       self.lights.append(-light)
        return self

    object_window = property(lambda self: self._window,
        lambda self, wnd: setattr(self, '_window', wnd), None,
        """ The object window.

        Most devices have only one object window, so this value should
        not be modified.
        """)


class EngineTask:
    """ List of field references to read by the engine.

    The concerning FieldReference class, the FieldSource and FieldId
    values are defined in processing module.
    """

    def __init__(self):
        self.fields = []

    def add(self, field, field_id=None):
        """ Append a data field reference to the list.

        Can be called with FieldReference as only parameter, or with
        FieldSource and FieldId parameter pair.

        :param field:       FieldSource or FieldReference.
        :param field_id:    FieldId or None.
        :return:            self
        """
        if field_id is not None and not isinstance(field, FieldReference):
            field = FieldReference(field, field_id)
        if field.code == 0: self.fields.clear()
        self.fields.append(field.code)
        return self

    def remove(self, field, field_id=None):
        """ Remove a data field reference from the list.

        Can be called with FieldReference as only parameter, or with
        FieldSource and FieldId parameter pair.

        :param field:       FieldSource or FieldReference.
        :param field_id:    FieldId or None.
        :return:            self
        """
        if field_id is not None and not isinstance(field, FieldReference):
            field = FieldReference(field, field_id)
        if field.code == 0: self.fields.clear()
        else:               self.fields.append(-field.code)
        return self


class ECardTask:
    """ List of data reading and authentication requirements.

    The concerning File identifier class, the FileId and AuthLevel
    values are defined in ecardhandling module.
    """

    def __init__(self):
        self._security_level = None
        self.files = []

    def add(self, file):
        """ Append a file to the list.

        :param file:    File identifier.
        :return:        self
        """
        if file.id_v == FileId.All: self.files.clear()
        self.files.append(file.id_v)
        return self

    def remove(self, file):
        """ Remove a file from the list.

        :param file:    File identifier.
        :return:        self
        """
        if file.id_v == FileId.All: self.files.clear()
        else:                     self.files.append(-file.id_v)
        return self

    authlevel = property(lambda self: self._security_level,
        lambda self, level: setattr(self, '_security_level', level), None,
        "The required authentication level.")
