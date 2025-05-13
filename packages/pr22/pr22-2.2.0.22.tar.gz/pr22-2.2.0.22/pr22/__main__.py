#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PR Python Interface """

import sys
import pr22

_sign = "PR Python Interface\n"
_sign += "Version: " + pr22.__version__ + "\n"

try:
    _sign += "System: " + pr22.DocumentReaderDevice().get_version('S')
except pr22.exceptions.General as ex:
    _sign += "System: " + str(ex)

if sys.argv[0].endswith('pydoc.py'):
    __doc__ = _sign
else:
    print(_sign)
