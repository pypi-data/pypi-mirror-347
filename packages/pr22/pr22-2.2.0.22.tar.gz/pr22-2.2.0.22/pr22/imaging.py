#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Image-related enumerations and classes. """

__version__ = '2.2.0.22'

# import sys
# import traceback
from ctypes import Structure, c_int, cast, c_void_p, c_wchar_p
from ctypes import pointer as _pointer,  sizeof as _sizeof

from pr22 import exceptions, prins, util, processing
from pr22.types import PrEnum, chk_ver
from pr22.prins import PrApi
chk_ver(__version__)


class _RawImageCallCodes(PrEnum):
    CallCodes        = 0x11040000
    GetPixelSize     = CallCodes
    AllocImage       = CallCodes | 0x0007
    RefImage         = CallCodes | 0x0009
    UnrefImage       = CallCodes | 0x000A
    CreateImage      = CallCodes | 0x000B
    ConvertImage     = CallCodes | 0x000C
    LoadRawPixels    = CallCodes | 0x0014
    IsValidImage     = CallCodes | 0x0016
    DuplicateImage   = CallCodes | 0x0021
    ImageToVariant   = CallCodes | 0x0022
    ImageFromVariant = CallCodes | 0x0023
    SaveImage        = CallCodes | 0x0029


class Light(PrEnum):
    """ Usable illuminations. """
    All      =  0,      "All the lights or light off."
    Off      =  0,      "All the lights or light off."
    White    =  1,      """White light.

    Reflection removing is applied if this technology is supported by
    the scanner.
    """
    Infra    =  2,      "Infrared light. ~900 nm"
    UV       =  3,      "Ultraviolet light. ~365 nm"
    Coaxial  =  4,      """Specially directed (coaxial) white light.
    For examination of certain security foils."""
    OVD      =  5,      """White light with accumulated hologram effects.
    It is designed for visualization of holograms."""
    Photo    =  6,      """High resolution white image.
    It is targeted and focused on the photo area of passports."""
    Blue     = 16,      "Blue light."
    Red      = 17,      "Red light."
    CleanUV  = 19,      "Modified UV image with background masking."
    CleanOVD = 21,      """Modified OVD image with background masking.
    For hologram visualization."""
    Edge     = 25,      "Infra-red oblique light."


class PagePosition(PrEnum):
    """ Page selection values. """
    Next    = 0,        """The next page will be scanned.
    i.e. another page of the current document even another document."""
    Current = 1,        "The images to be scanned will be appended to the current page."
    First   = 2,        """The first page will be scanned.

    It means that all the internally stored data (images, documents)
    will be removed from the system."""


class FingerPosition(PrEnum):
    """
    Finger position codes as specified in ANSI/NIST-ITL 1 documentation.
    """
    Unknown            =  0     # Unknown.
    RightThumb         =  1     # Right thumb.
    RightIndex         =  2     # Right index finger.
    RightMiddle        =  3     # Right middle finger.
    RightRing          =  4     # Right ring finger.
    RightLittle        =  5     # Right little finger.
    LeftThumb          =  6     # Left thumb.
    LeftIndex          =  7     # Left index finger.
    LeftMiddle         =  8     # Left middle finger.
    LeftRing           =  9     # Left ring finger.
    LeftLittle         = 10     # Left little finger.
    PlainRightThumb    = 11     # Plain right thumb.
    PlainLeftThumb     = 12     # Plain left thumb.
    PlainRight4Fingers = 13     # Plain right 4 fingers.
    PlainLeft4Fingers  = 14     # Plain left 4 fingers.
    PlainThumbs        = 15,    "Left and right thumbs."
    BothIndexes        = 46,    "Left and right index fingers."


class FileFormat(PrEnum):
    """ FileFormat for images. """
    Bmp             = 1,        "BMP format."
    Jpeg            = 2,        "JPEG format (ISO/IEC 10918-1)."
    Jpeg2kStream    = 3,        "JPEG-2000 Code stream syntax (ISO/IEC 15444-1)."
    Jpeg2k          = 4,        "JPEG-2000 JP2 format syntax (ISO/IEC 15444-1)."
    Raw             = 5,        "Raw format (uncompressed pixel data without header)."
    Png             = 6,        "PNG format (Portable Network Graphics)."
    Wsq             = 7,        "WSQ format (Wavelet Scalar Quantization)."


class RawImage:
    """ Low level image data of the system that can be saved. """

    class PixelFormat(PrEnum):
        """ Available pixel formats """
        Undef   = 0x0000        # Undefined format for Load functions
        Gray    = 0x0001        # 8 bit: 8 bit (grayscale)
        RGB555  = 0x0002        # 16 bit: 1-5-5-5 bit (0,R,G,B)
        BGR555  = 0x0003        # 16 bit: 1-5-5-5 bit (0,B,G,R)
        RGB565  = 0x0004        # 16 bit: 5-6-5 bit (R,G,B)
        BGR565  = 0x0005        # 16 bit: 5-6-5 bit (B,G,R)
        RGB     = 0x0006        # 24 bit: 8-8-8 bit (R,G,B)
        BGR     = 0x0007        # 24 bit: 8-8-8 bit (B,G,R)
        RGBA    = 0x0008        # 32 bit: 8-8-8-8 bit (R,G,B,A)
        BGRA    = 0x0009        # 32 bit: 8-8-8-8 bit (B,G,R,A)
        YUV422  = 0x000A        # 32 bit/2 pixel: 8-8-8-8 bit (U,Y1,V,Y2)
        Gray12  = 0x000B        # 16 bit: 4-12 bit (0,grayscale)
        RGB12   = 0x000C        # 48 bit: 4-12-4-12-4-12 bit (0,R,0,G,0,B)
        BGR12   = 0x000D        # 48 bit: 4-12-4-12-4-12 bit (0,B,0,G,0,R)
        GBRG    = 0x000E        # 32 bit/4 pixel: 8-8-8-8 bit Bayern-pattern (G,B,R,G)
        BGGR    = 0x000F        # 32 bit/4 pixel: 8-8-8-8 bit Bayern-pattern (B,G,G,R)
        RGGB    = 0x0010        # 32 bit/4 pixel: 8-8-8-8 bit Bayern-pattern (R,G,G,B)
        GRBG    = 0x0011        # 32 bit/4 pixel: 8-8-8-8 bit Bayern-pattern (G,R,B,G)

    FileFormat = FileFormat

    def __init__(self, image=None):
        self.image = image
        self._ref_image()

    def __del__(self):
        """ Finalizer. """
        self._unref_image()

    def __enter__(self):
        """ Enter the runtime context. """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the runtime context. """
        try: self._unref_image()
        except exceptions.General: pass
        return False

    @staticmethod
    def _api_call(cmd, params):
        return prins.glob_call(0xffff1104, cmd, params)

    def _unref_image(self):
        if self.image is not None:
            RawImage._api_call(_RawImageCallCodes.UnrefImage, self.image)
        self.image = None
        return self

    def is_valid(self):
        """ Check if the image is valid.

        :return:            True for a valid image.
        """
        try: return not RawImage._api_call(_RawImageCallCodes.IsValidImage, self.image)
        except exceptions.General: return False

    def _ref_image(self):
        if self.image is not None:
            RawImage._api_call(_RawImageCallCodes.RefImage, self.image)
        return self

    def _t(self):
        return self.image is not None

    def _p(self, ix):
        return c_int.from_address(self.image.value
            + ix * _sizeof(c_int) + _sizeof(c_void_p)).value

    def duplicate(self):
        """ Duplicate the image.

        :return:        The duplicated image.
        """
        img = RawImage()
        img.alloc()
        dpp = RawImage._StimDuplicate(img.image, self.image)
        RawImage._api_call(_RawImageCallCodes.DuplicateImage, dpp)
        return img

    def load(self, buffer):
        """ Load an image from the memory.

        :param buffer:  Image file data in processing.BinData structure.
        :return:        self
        """
        self.alloc()

        lrp = RawImage._StimLoad(self.image, cast(buffer.raw_data, c_void_p), buffer.raw_size, 0)
        RawImage._api_call(_RawImageCallCodes.LoadRawPixels, lrp)
        return self

    def save(self, file_format, properties=None, comments=None):
        """ Save the image to the memory in a specific file format.

        :param file_format: The FileFormat.
        :param properties:  Properties for saving. The properties are
                            described in the reference manual.
        :param comments:    Comments for save.
        :return:            Saved image file data in processing.BinData.
        """
        properties = 0 if properties is None else properties.var_data
        if comments is None: comments = 0
        else:
            varcomm = util.Variant(0, util.Variant.Types.List)
            varcomm += util.Variant(0, comments)
            comments = varcomm.var_data

        params = RawImage._StimSaveImageToMem2()
        # pylint: disable=W0201
        params.pimage = self.image
        formats = ["", "bmp", "jpeg", "jpeg2k_jpc", "jpeg2k", "raw", "png", "wsq"]
        tmpbuff = c_void_p(None)
        params.buffer = cast(_pointer(tmpbuff), c_void_p)
        bufflen = c_int(0)
        params.buflen = cast(_pointer(bufflen), c_void_p)
        params.fileformat = formats[file_format]
        params.properties = cast(properties, c_void_p)
        params.comments   = cast(comments, c_void_p)
        RawImage._api_call(_RawImageCallCodes.SaveImage, params)
        return processing.BinData.from_gx(tmpbuff, bufflen.value)

    def to_variant(self, varid, varname):
        """ Embed the image into a util.Variant.

        :param varid:       The Id for the created variant.
        :param varname:     The name for the created variant.
        :return:            The created Variant.
        """
        itv = RawImage._StimToVariant(self.image, varid, None)
        RawImage._api_call(_RawImageCallCodes.ImageToVariant, itv)
        retvar = util.Variant(itv.variant)
        if len(varname): retvar.name = varname
        return retvar

    def from_variant(self, variant_image):
        """ Get an embedded image from a variant.

        :param variant_image:   Variant with an embedded image.
        :return:                self
        """
        self._unref_image()

        params = RawImage._StimFromVariant(None, variant_image.var_data)
        RawImage._api_call(_RawImageCallCodes.ImageFromVariant, params)
        self.image = cast(params.pimage, c_void_p)
        return self

    #############################################
    try:
        from PyQt5.QtCore import QByteArray, QBuffer, QIODevice

        def to_qimage(self, qimage_cls):
            """ Return the image as a Qt QImage or QPixmap object.

            :param qimage_cls:  Image type to convert to.
            :return:            QImage or QPixmap object.
            """
            buffer = self.save(RawImage.FileFormat.Bmp)
            img = qimage_cls()
            img.loadFromData(bytes(buffer.raw_data), "bmp")
            return img

        def from_qt(self, qimage):
            """ Convert a Qt QImage or QPixmap object to RawImage.

            :param qimage:  A Qt image to be converted to RawImage.
            :return:        self
            """
            datas  = self.QByteArray()
            buffer = self.QBuffer(datas)
            buffer.open(self.QIODevice.WriteOnly)
            qimage.save(buffer, "bmp")
            bdt = processing.BinData()
            bdt.data = datas.data()
            return self.load(bdt)
    except:
        # print( sys.exc_info() )
        # print( traceback.format_exc() )
        pass
    #############################################

    def alloc(self):
        """ Internally used method. """
        self._unref_image()
        img = c_void_p()
        RawImage._api_call(_RawImageCallCodes.AllocImage, _pointer(img))
        self.image = img
        return self

    def create(self, pixl_format, xsize, ysize, sline):
        """ Create an image.

        :param pixl_format: RawImage.PixelFormat.
        :param xsize:   Horizontal size of image in pixels.
        :param ysize:   Vertical size of image in pixels.
        :param sline:   Length of a row in bytes  (min.: xsize * size of
                        a pixel in bytes).  If this parameter is 0,  the
                        system computes the correct value.
        :return:        self
        """
        self.alloc()
        cip = RawImage._StimCreate(self.image, pixl_format, xsize, ysize, sline)
        RawImage._api_call(_RawImageCallCodes.CreateImage, cip)
        return self

    def convert(self, pixl_format, xsize, ysize, sline):
        """ Convert the image to a specific pixel format and size.

        :param pixl_format: RawImage.PixelFormat of the target image. If
                        this parameter is PixelFormat.Undef or None, the
                        format remains the same.
        :param xsize:   Horizontal size  of the target image  in pixels.
                        If  this parameter is 0,  the width remains  the
                        same.
        :param ysize:   Vertical size of the target image in pixels.  If
                        this  parameter  is 0,  the height  remains  the
                        same.
        :param sline:   Length of a row in bytes  (min.: xsize * size of
                        a pixel in bytes).  If this parameter is 0,  the
                        system computes the correct value.
        :return:        The converted image with the desired parameters.
        """
        img = RawImage()
        img.alloc()
        cpp = RawImage._StimConvert()
        # pylint: disable=W0201
        cpp.pdest  = img.image
        cpp.psrc   = self.image
        if pixl_format == RawImage.PixelFormat.Undef: pixl_format = None
        cpp.format = pixl_format if pixl_format is not None else self.image.format
        cpp.xsize  = xsize if xsize != 0 else self.size[0]
        cpp.ysize  = ysize if ysize != 0 else self.size[1]
        cpp.sline  = sline
        RawImage._api_call(_RawImageCallCodes.ConvertImage, cpp)
        return img

    pixel_format = property(lambda self:
        RawImage.PixelFormat.parse(self._p(3)) if self._t() else
        RawImage.PixelFormat.Undef, None, None, "PixelFormat of the image.")

    size = property(lambda self: [self._p(4), self._p(5)] if self._t() else [-1, -1],
                    None, None, """Size of the image in pixels.
                    (a list of int values; width, height)""")

    s_line = property(lambda self: self._p(6) if self._t() else -1,
                      None, None, "Length of a row in bytes.")

    resolution = property(lambda self: [self._p(7), self._p(8)] if self._t() else [-1, -1],
                     None, None, """Resolution of the image in pixel/meters.
                     (a list of int values; horizontal, vertical)""")

    raw_data = property(lambda self: c_void_p.from_address(self.image.value
        + 2 * _sizeof(c_int)) if self._t() else None, None, None,
        """Address of the buffer of the raw pixel data.
        (in unmanaged memory)""")

    raw_size = property(lambda self: self._p(2) if self._t() else -1,
                        None, None, "Size of the raw pixel data.")

    class _StimDuplicate(Structure):  # pylint: disable=R0903
        _fields_ = [("target", c_void_p), ("source", c_void_p)]

    class _StimLoad(Structure):             # pylint: disable=R0903
        _fields_ = [("pimage", c_void_p), ("buffer", c_void_p),
                    ("buflen", c_int), ("format", c_int)]

    class _StimSaveImageToMem2(Structure):  # pylint: disable=R0903
        _fields_ = [("pimage", c_void_p), ("buffer", c_void_p), ("buflen", c_void_p),
                    ("fileformat", c_wchar_p), ("properties", c_void_p), ("comments", c_void_p)]

    class _StimToVariant(Structure):        # pylint: disable=R0903
        _fields_ = [("pimage", c_void_p), ("varid", c_int), ("variant", util.st_gxVARIANT)]

    class _StimFromVariant(Structure):      # pylint: disable=R0903
        _fields_ = [("pimage", c_void_p), ("variant", util.st_gxVARIANT)]

    class _StimCreate(Structure):           # pylint: disable=R0903
        _fields_ = [("pimage", c_void_p), ("format", c_int),
                    ("xsize", c_int), ("ysize", c_int), ("sline", c_int)]

    class _StimConvert(Structure):          # pylint: disable=R0903
        _fields_ = [("pdest", c_void_p), ("psrc", c_void_p), ("format", c_int),
                    ("xsize", c_int), ("ysize", c_int), ("sline", c_int)]


class DocImage:
    """ Scanned document image data. """

    def __init__(self, api_handle, variant, page_number, image_type=0):
        """ Do not create instances directly. """
        self.prapi = api_handle
        self._var_image = variant.new_ref()
        self.page_number = page_number
        self.type = image_type

    def __del__(self):
        """ Finalizer. """
        del self._var_image
        self._var_image = None
        self.prapi = None

    def __enter__(self):
        """ Enter the runtime context. """
        self._var_image.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the runtime context. """
        try: self._var_image.__exit__(exc_type, exc_val, exc_tb)
        except exceptions.General: pass
        self._var_image = None
        self.prapi = None
        return False

    def get_image(self):
        """ Return the related RawImage.

        :return:                The related RawImage.
        """
        if self.type == 0: return RawImage().from_variant(self._var_image)
        param = DocImage._StprGetImage(c_int(self.page_number), c_int(self.light),
                                       c_int(self.type), None)
        self.prapi.api_call(PrApi.GetImage, param)
        with util.Variant(param.Img) as var:
            return RawImage().from_variant(var)

    def doc_view(self):
        """ Return a rotated and cropped image.

        For top-bottom orientation, the Page.analyze() method must be
        called before.

        :return:        A DocImage representing the cropped document.
        """
        return DocImage(self.prapi, self._var_image, self.page_number, 1)

    def to_page(self):
        """ Convert image to processing.Page object.

        :return:                A processing.Page object.
        """
        imglist = util.Variant(util.VariantId.ImageList, util.Variant.Types.List)
        imglist.add_list_item(self._var_image)
        return processing.Page(self.prapi, self.page_number, imglist)

    def generate_latent_image(self, decoding_params):
        """ Generate a decoded IPI image for visual inspection.

        This method has the same role as Engine.generate_latent_image().

        :param decoding_params: IPI image decoding parameters in a str.
        :return:                A generated RawImage.
        """
        param = DocImage._StprDecodeLatentImage(self.page_number, self.light, self.type,
                                                decoding_params, 0)

        self.prapi.api_call(PrApi.DecodeLatentImage, param)

        with util.Variant(param.image) as var:
            return RawImage().from_variant(var)

    def read_field(self, reading_params):
        """ Read character or barcode data from an image.

        This method has the same role as Engine.read_field().

        :param reading_params:  Reading  parameters  in  a  util.Variant
                                which  are  described  in  the  Passport
                                Reader reference manual.
        :return:                A processing.Document result structure.
        """
        param = DocImage._StprGetOCRV(self.page_number, self.light, self.type, None,
                                      reading_params.var_data)

        self.prapi.api_call(PrApi.GetOCRV, param)

        var = util.Variant(param.Doc)
        return processing.Document(self.prapi, var)

    def to_variant(self):
        """ Return low level data to access special image information.

        :return:                Low level util.Variant data.
        """
        return self._var_image

    light = property(lambda self:
        Light.parse(self._var_image.get_child(util.VariantId.Light, 0).to_int()),
        None, None, 'Light "illumination" used at image scanning.')

    class _StprGetImage(Structure):  # pylint: disable=R0903
        _fields_ = [("Page", c_int), ("Light", c_int), ("Type", c_int),
                    ("Img", util.st_gxVARIANT)]

    class _StprDecodeLatentImage(Structure):  # pylint: disable=R0903
        _fields_ = [("page", c_int), ("light", c_int), ("type", c_int),
                    ("decpar", c_wchar_p), ("image", util.st_gxVARIANT)]

    class _StprGetOCRV(Structure):          # pylint: disable=R0903
        _fields_ = [("page", c_int), ("light", c_int), ("type", c_int),
                    ("doc", util.st_gxVARIANT), ("Params", util.st_gxVARIANT)]


class ScannerInformation:
    """ Class for storing information on a DocScanner. """

    def __init__(self, api_handle: prins.GxModule):
        """ Do not create instances directly. """
        self.prapi = api_handle
        param = ScannerInformation._StprGetDeviceInfo(None)
        self.prapi.api_call(prins.CommonApi.GetDeviceInfo, param)
        self.info = util.Variant(param.devInfo).get_item_by_path("L/V=1")

    def list_lights(self):
        """ Return the list of usable Lights.

        :return:            The Light list.
        """
        lights = []
        tmp = self.info.get_child(util.VariantId.Light, 0).to_int_array()
        for ix in tmp: lights.append(Light.parse(ix))
        return lights

    def get_version(self, component):
        """ Return version information of the scanner.

        :param component:   Character 'H'  for version  of the hardware,
                            character 'F'  for version  of the firmware,
                            or character 'S'  for version  of the device
                            handling software library.
        :return:            Version information string of the scanner.
        """
        try:
            pos = util.VariantPos.by_id(ord(component))
            return self.info.get_child(util.VariantId.Version, 0).get_list_item(pos).to_string()
        except exceptions.General:
            return "-"

    def is_calibrated(self, object_window=-1):
        """ Return if an object window of the scanner is calibrated.

        :param object_window:   Ordinal number of the object window of
                                the scanner. See get_window_count()
        :return:                True if the object window is calibrated.
        """
        param = ScannerInformation._StprIsCalibrated((object_window + 1) << 24)
        try:
            return not self.prapi.api_call(PrApi.Iscalibrated, param)
        except exceptions.EntryNotFound:
            return False

    def get_size(self, object_window):
        """ Return the size of an object window of the scanner.

        :param object_window:   Ordinal number  of the object  window of
                                the scanner. See get_window_count()
        :return:                A  rectangle  of  the  object  window in
                                micrometers.  It is a list of int values
                                such as left and top coordinates,  width
                                and height.
        """
        vfr = self.info.get_child(util.VariantId.WindowList, 0)[object_window]
        frm = vfr.to_frame()
        return [frm.x1, frm.y1, frm.x3 - frm.x1, frm.y3 - frm.y1]

    def get_window_count(self):
        """ Return the number of object windows of the scanner.

        More object windows  are available only  in double-page document
        readers and in devices equipped with photo camera.  For scanning
        with photo camera,  use Light.Photo  instead of handling  object
        window.

        :return:            The number of object windows of the scanner.
        """
        return self.info.get_child(util.VariantId.WindowList, 0).n_items

    class _StprGetDeviceInfo(Structure):    # pylint: disable=R0903
        _fields_ = [("devInfo", util.st_gxVARIANT)]

    class _StprIsCalibrated(Structure):     # pylint: disable=R0903
        _fields_ = [("objectWindow", c_int)]
