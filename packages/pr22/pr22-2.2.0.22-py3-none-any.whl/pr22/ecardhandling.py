#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" ECard-related enumerations and classes. """

__version__ = '2.2.0.22'

from ctypes import c_wchar_p, c_int, c_void_p, Structure, cast

from pr22 import exceptions
from pr22.types import PrEnum, chk_ver
from pr22.prins import PrApi
from pr22.util  import Variant, VariantId, HWType, VariantPos, st_gxVARIANT
chk_ver(__version__)


class Application(PrEnum):
    """ Applications on the ECard. """
    NoApp       = 0,        "No application."
    Passport    = 1,        "ePassport application."
    ID          = 2,        "eID application."
    Sign        = 3,        "eSign application."
    ISODL       = 4,        "ISO Driving License application."
    NFC         = 5,        "Near Field Communication application."
    EDL         = 6,        "European Driving License application."


class AuthLevel(PrEnum):
    """ Level of the authentication. """
    Max         = 0,        """Maximal authentication.

    Executes all of the authentications,  even if they are redundant
    or not necessary to read the files."""
    Min         = 1,        """Minimal authentication.

    Executes only those  authentications that are  essential to read
    the files."""
    Opt         = 2,        """Optimal authentication.

    Executes  all  of  those  authentications  that  are  absolutely
    necessary  to determine the authenticity  of the document.  This
    method avoids  performing authentications that are  redundant or
    not necessary to read the files."""


class CertSelection(PrEnum):
    """ Certificate selection filtering constants. """
    All         =     0,    "Select all the certificates."
    Expired     = 0x100,    "Select the expired certificates."
    Revoked     = 0x200,    "Select the revoked certificates."


class AuthProcess(PrEnum):
    """ Authentication Ids. """
    NoAuth          =  0,   "No authentication."
    Passive         =  1,   "Passive Authentication."
    Terminal        =  2,   "Terminal Authentication."
    PACE            =  3,   "Password Authenticated Connection Establishment."
    BAC             =  4,   "Basic Access Control."
    Chip            =  5,   "Chip Authentication."
    Active          =  6,   "Active Authentication."
    SelectApp       =  7,   "Select Application."
    BAP             =  8,   "Basic Access Protection."
    Block           =  9,   "Block authentication."
    InitTerminal    = 10,   "Init Terminal Authentication."
    CompleteTerminal = 11,  "Complete Terminal Authentication."
    StorageCard     = 12,   "Storage Card authentication."

    @classmethod
    def _missing_(cls, value):
        if hasattr(value, 'to_ecard'):
            res = value.to_ecard() - 50
            if cls.has_value(res): return cls(res)
        return None

    def to_fref(self):
        """ Internally used method. """
        return int(self) + 50


class FileId(PrEnum):
    """ Logical file identifiers for files on the ECard.

    See File for details.
    """
    Com                 =    0,     "Common content file."
    CardAccess          =   28,     "Card Access parameter file."
    CardSecurity        =   29,     "Card Security parameter file."
    Cvca                =   30,     "Card Verifiable parameter file."
    Sod                 =   31,     "Security Object file."
    CertDS              =   32,     "Document Signer certificate file."
    CertCSCA            =   33,     "Country Signing CA certificate file."
    All                 =  999,     "All files."
    GeneralData         = 1000,     "General data."
    PersonalDetails     = 1001,     "Personal details."
    IssuerDetails       = 1002,     "Issuer details."
    Portrait            = 1003,     "Portrait."
    Signature           = 1004,     "Signature."
    Face                = 1005,     "Biometric face."
    Finger              = 1006,     "Biometric finger."
    Iris                = 1007,     "Biometric iris."
    OtherBiometricData  = 1008,     "Other biometric data."
    DomesticData        = 1009,     "Domestic data."
    AAData              = 1010,     "Active authentication data."
    AnyFace             = 1011,     "Any face or portrait."
    TocFile             = 1012,     "Table of content data."
    EapData             = 1013,     "Extended access control/protection data."


class File:
    """ ECard file identifier class.

    Generally ECards contain data in files called Data Groups. Different
    type of documents  (e.g. ePassport and ISO-DL)  stores the same data
    in different  data group.  Our SDK contains  FileId-s - logical file
    identifiers - to identify  data groups by their  content next to the
    numerical  file identifiers - File.dg().  Both of them are usable in
    certain  situations.  They can  be converted  to each  other by  the
    ECard.convert_fileid() method.

    :ivar id_v:             Id of the file.
    """

    def __init__(self, file_index=0):
        """ New file identifier.

        :param file_index:  Id of the file. Can be numeric or FileId.

        The file_index parameter alternatively can be used to conversion
        from processing.FieldReference.
        """
        if hasattr(file_index, 'to_ecard'):
            self.id_v = file_index.to_ecard()
            if 0 <= self.id_v < 50: return
            raise exceptions.InvalidParameter("[pr22] No data group!")
        self.id_v = int(file_index)

    def __str__(self):
        return self.to_string()

    def to_string(self):
        """ Return string representation of the file Id. """
        if FileId.has_value(self.id_v):
            return FileId(self.id_v).name

        fno = self.id_v >> 29
        if fno < 0 or fno > 3: fno = 0
        return ("DG", "Block", "Address", "Sector")[fno] + str(self.id_v & 0xFFFF)

    @staticmethod
    def dg(dgid):
        """ New file identifier.

        :param dgid:        Data group number.
        :return:            The file identifier.
        """
        return File(dgid)

    @staticmethod
    def block(block, memsize=0):
        """ New file identifier of a storage card.

        :param block:       Block number.
        :param memsize:     Number of bytes to read.
        :return:            The file identifier.
        """
        if memsize < 0 or memsize >= 256: memsize = 0
        return File(0x20000000 + (memsize << 16) + block)

    @staticmethod
    def mem_address(addr, memsize=0):
        """ New file identifier of a storage card.

        :param addr:        Memory address to read from.
        :param memsize:     Number of bytes to read.
        :return:            The file identifier.
        """
        if memsize < 0 or memsize >= 256: memsize = 0
        return File(0x40000000 + (memsize << 16) + addr)

    @staticmethod
    def sector(sector, memsize=0):
        """ New file identifier of a storage card.

        :param sector:      Sector number.
        :param memsize:     Number of bytes to read.
        :return:            The file identifier.
        """
        if memsize < 0 or memsize >= 256: memsize = 0
        return File(0x60000000 + (memsize << 16) + sector)

    def to_fref(self):
        """ Internally used method. """
        if 0 <= self.id_v < 50: return self.id_v
        raise exceptions.InvalidParameter("[pr22] No data group!")


class Certificates:
    """ Certificate manager class.

    The system is  equipped with different  certificate manager  objects
    that are designed  to realize  different ways  of certificate usage.
    Certificates can be used globally  (for all readers of all devices),
    or specifically  for one DocumentReaderDevice  or one ECardReader or
    one ECard.
    """

    def __init__(self, api_handle, scope, owner):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self.owner = owner
        self.scope = scope

    def load(self, public_key, private_key=None):
        """ Load a certificate and its private key to the manager.

        :param public_key:      The certificate to load.
        :param private_key:     The private key to load.
        :return:                Id of the certificate.
        """
        param = Certificates._StprLoadCertScope()
        # pylint: disable=W0201
        param.scope = self.scope
        param.owner = self.owner
        param.certificate_data = cast(public_key.raw_data, c_void_p)
        param.certificate_length = public_key.raw_size
        if private_key:
            param.private_key_data = cast(private_key.raw_data, c_void_p)
            param.private_key_length = private_key.raw_size
        param.idv = 0
        self.prapi.api_call(PrApi.LoadCertScope, param)
        return param.idv

    def load_from_store(self, store_name):
        """ Load certificates from a certificate store.

        :param store_name:      The name of the certificate store.
        """
        param = Certificates._StprLoadCertFromStore(store_name)
        self.prapi.api_call(PrApi.LoadCertFromStore, param)

    def clear(self, authid, certprop):
        """
        Remove  certificates  from  the manager  by authentication  type
        and/or validity status.
     
        :param authid:      Certificate selection AuthProcess filter for
                            authentications.   Use  value  of  None  for
                            selecting all the authentications.
        :param certprop:    CertSelection filter.
        """
        if authid is None: authid = AuthProcess.NoAuth
        self.remove(authid.value + certprop.value)

    def remove(self, cert_id):
        """ Remove certificate from the manager by Id.
     
        :param cert_id:     Id of a  certificate returned  by the load()
                            method.
        """
        param = Certificates._StprClearCertListScope(cert_id, self.scope, self.owner)
        self.prapi.api_call(PrApi.ClearCertListScope, param)

    class _StprLoadCertScope(Structure):    # pylint: disable=R0903
        _fields_ = [("scope", c_int), ("owner", c_wchar_p), ("certificate_data", c_void_p),
                    ("certificate_length", c_int), ("private_key_data", c_void_p),
                    ("private_key_length", c_int), ("idv", c_int)]

    class _StprLoadCertFromStore(Structure):  # pylint: disable=R0903
        _fields_ = [("StoreName", c_wchar_p)]

    class _StprClearCertListScope(Structure):  # pylint: disable=R0903
        _fields_ = [("Sel", c_int), ("Scope", c_int), ("Owner", c_wchar_p)]


class CardInformation:                          # pylint: disable=R0903
    """ Class for storing information on an ECard. """

    def __init__(self, api_handle, card):
        """ Do not create instances directly. """
        param = CardInformation._StprGetRfidCardInfo(card, 0)
        api_handle.api_call(PrApi.GetRfidCardInfo, param)
        self.info = Variant(param.CardInfo)

    def to_variant(self):
        """ Return low level data to access special ECard information.

        :return:            Low level util.Variant data.
        """
        return self.info

    @property
    def card_type(self):
        """ The ECard type identifier string. """
        return self.info.get_child(VariantId.CardType, 0).to_string()

    class _StprGetRfidCardInfo(Structure):  # pylint: disable=R0903
        _fields_ = [("Card", c_wchar_p), ("CardInfo", st_gxVARIANT)]


class ReaderInformation:
    """ Class for storing information on an ECardReader. """

    def __init__(self, var_info):
        """ Do not create instances directly. """
        self.info = var_info

    @property
    def hw_type(self):
        """ util.HWType of the reader. """
        return HWType.parse(self.info.to_int())

    def get_version(self, component):
        """ Return version information of the reader.

        :param component:   Character 'H'  for version  of the hardware,
                            character 'F'  for version  of the firmware,
                            or character 'S'  for version  of the device
                            handling software library.
        :return:            Version information string of the reader.
        """
        try:
            child = self.info.get_child(VariantId.Version, 0)
            item = child.get_list_item(VariantPos.by_id(ord(component)))
            return item.to_string()
        except exceptions.General:
            return "-"
