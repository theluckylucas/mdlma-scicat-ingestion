from skimage import io
import base64
import numpy
import cv2


TIFF = "tiff"
URI_PNG_PREFIX = "data:image/png;base64,"
TMP_PATH = "/tmp/mdlmaattachuri.png"

 
def get_tif_info_dict(filename):
    img = io.imread(filename)
    result = {
        "{} datatype".format(TIFF): img.dtype.name,
    }
    for dim, ext in enumerate(img.shape):
        result["{} shape[{}]".format(TIFF, dim)] = ext
    return result


def get_uri_from_tif(filename, target_size=(50, 50)):
    img = io.imread(filename).astype(numpy.float32)
    img = cv2.resize(img, target_size, cv2.INTER_LINEAR)
    max_val = numpy.max(img)
    min_val = numpy.min(img)
    img -= min_val
    img /= max_val - min_val
    #img *= 255
    #img = img.astype(numpy.int8)
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #enc = cv2.imencode('.png', img)[1]
    
    io.imsave(TMP_PATH, img)
    b64 = base64.b64encode(open(TMP_PATH, "rb").read())
    return URI_PNG_PREFIX + str(b64)[2:-1]