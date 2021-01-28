from .FSInfo import get_ext

from skimage import io, color
from pydicom import dcmread
import base64
import numpy
import cv2


TYPE_TIFF = "tiff"
TYPE_IMG = "img"
TYPE_HDR = "hdr"
TYPE_HDF = "hdf"
TYPE_PNG = "png"
TYPE_NDPI = "ndpi"
TYPE_VGL = "vgl"
TYPE_SVG = "svg"
TYPE_DCM = "dcm"
TYPE_JPEG = "jpeg"
TYPES = {
    "tif": TYPE_TIFF,
    "tiff": TYPE_TIFF,
    "img": TYPE_IMG,
    "hdr": TYPE_HDR,
    "h5": TYPE_HDF,
    "h4": TYPE_HDF,
    "hdf": TYPE_HDF,
    "png": TYPE_PNG,
    "vgl": TYPE_VGL,
    "ndpi": TYPE_NDPI,
    "svg": TYPE_SVG,
    "dcm": TYPE_DCM,
    "jpg": TYPE_JPEG,
    "jpeg": TYPE_JPEG
}
SUPPORTED_IMAGE_TYPES = [TYPE_TIFF, TYPE_PNG, TYPE_DCM, TYPE_JPEG]
URI_PNG_PREFIX = "data:image/png;base64,"
TMP_PATH = "/tmp/mdlmaattachuri.png"

 
def load_numpy_from_image(filename):
    img_array = None
    img_format = TYPES[get_ext(filename)]
    img_meta = None
    if img_format == TYPE_TIFF or img_format == TYPE_PNG or img_format == TYPE_JPEG:
        img = io.imread(filename)
        if len(img.shape) == 2:  # only work with 2D grayscale image slices
            img_array = img
        elif len(img.shape) == 3 and img.shape[2] == 3:  # RGB images
            img_array = img
        elif len(img.shape) == 3 and img.shape[2] == 4:  # remove alpha
            img_array = color.rgba2rgb(img)
    elif img_format == TYPE_DCM:
        img_meta = dcmread(filename)
        img = img_meta.pixel_array
        if len(img.shape) == 2:  # only work with 2D grayscale image slices
            img_array = img
    return img_array, img_format, img_meta


def get_uri_from_numpy(img_array, target_size=(150, 150)):
    img = img_array.astype(numpy.float32)
    img = cv2.resize(img, target_size, cv2.INTER_LINEAR)
    max_val = numpy.max(img)
    min_val = numpy.min(img)
    img -= min_val
    diff = max_val - min_val
    if diff != 0:
        img /= diff
    io.imsave(TMP_PATH, img)
    b64 = base64.b64encode(open(TMP_PATH, "rb").read())
    return URI_PNG_PREFIX + str(b64)[2:-1]