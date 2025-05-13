#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The  Passport Reader  is  a travel document  reader and analyzer  system
by ADAPTIVE RECOGNITION.

The main features of the PR system are:
    - Image scanning with different illuminations
    - Document, character and barcode recognition
    - Authentication of visual elements of documents
    - Reading and authenticating of electronic documents

The device controller class can be found in the pr22 package.  At first,
the program  must take  control  over  the devices  by the  use_device()
method.  Then, the `scanner`,  `engine` and `readers`  properties return
the corresponding  components  of the  reader.  Their functions  can  be
parameterized through Task objects. 

The following quick reference diagram shows the organization of the main
component classes.

             +---------------------------------------------------------+
Device       |                                                         |
 central     |                  DocumentReaderDevice                   |
  classes    |                                                         |
             +-------------+----------------+-------------+------------+
Device       | Peripherals |   DocScanner   | ECardReader |   Engine   |
 modules     |             |                | / ECard /   |            |
             +-------------+----------------+-------------+------------+
Tasks to be performed      | DocScannerTask |  ECardTask  | EngineTask |
                           |  FreerunTask   |             |            |
                           +----------------+-------------+------------+
Composite result structures|      Page      |             |  Document  |
                           +----------------+             +------------+
Main result elements       |    DocImage    |             |   Field    |
                           +----------------+-------------+------------+
General low level          |    RawImage    |   BinData   |  Variant   |
 data containers           |                |             |            |
                           +----------------+-------------+------------+

"""

__version__ = '2.2.0.22'
__all__ = ['DocumentReaderDevice']

from .core import *
