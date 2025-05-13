
What is pr22
------------

The Passport Reader is a travel document reader and analyzer system
by ADAPTIVE RECOGNITION.
 
The main features of the PR system are:
 - Image scanning with different illuminations
 - Document, character and barcode recognition
 - Authentication of visual elements of documents
 - Reading and authenticating of electronic documents

This software component is the general python SDK for the Passport Reader
system.

Installation and dependencies
-----------------------------

The pr22 requires the Passport Reader software to be installed, and it
works with special ID scanner hardware only. On Windows OS, the required
bitness (32/64) of the Passport Reader software depends on the used
python.exe and not on the operating system architecture.

The pr22 can cooperate with PyQt as it can pass and get images, but
installation of PyQt is not mandatory.

Install with the following command
```commandline
py -m pip install pr22
```
After that, the ready state of pr22 can be tested with
```commandline
py -m pr22
```
The documentation of classes and functions is available through pydoc
documentation starting as
```commandline
py -m pydoc -b
```
and then selecting the pr22 package.

Usage
-----

The source distribution of pr22 contains a tutorial folder with command
line sample programs. With the help of these programs, you can go through
the options of different topics. Also, there is a gui folder with more
lifelike examples but these demonstrate fewer options of the API than
command line samples.

### Tutorial programs:

#### pr01_open

Shows the possibilities of opening a device.

The following tutorials show the easy way of opening in their open_dev()
methods.

#### pr02_hwinfo

Shows how to get general information about the device capabilities.

#### pr03_scanning

Shows how to parametrize the image scanning process.

#### pr04_analyze

Shows the main capabilities of the image processing analyzer function.

#### pr05_doctype

Shows how to generate document type string. This example needs some additional
source files from the pr22ext folder.

#### pr06_ecard

Shows how to read and process data from ECards (including RFID documents).
After ECard selection, before starting reading ECard data, some authentication
processes have to be called for accessing the data files. This program performs
the steps of the reading process one by one.

### GUI programs:

Currently, only the PyQt dependent version of these examples are available.

#### ScannerSample

At first, it captures images with selected illuminations, utilizing motion
detection. Then, it analyzes image data. Finally, it shows the read data in
different representation forms.

#### ReadCard

Reads ECard data after executing the related authentications. The files read
can be saved by right-click on the filenames. The program performs the entire
reading process in the background.
