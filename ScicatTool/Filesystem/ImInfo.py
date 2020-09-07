from skimage import io


TIFF = "tiff"

 
def get_tif_info_dict(filename):
    img = io.imread(filename)
    result = {
        "{} datatype".format(TIFF): img.dtype.name,
    }
    for dim, ext in enumerate(img.shape):
        result["{} shape[{}]".format(TIFF, dim)] = ext
    return result
