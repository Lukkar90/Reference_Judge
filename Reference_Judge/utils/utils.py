"""
This module is snipsets of functions which are used in many places in code
"""

# python libs
import os
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

# external libs
import cv2
import numpy as np

# internal libs
from config.config import IMAGES_SIZES


# https://stackoverflow.com/a/58126805/12490791
def resize_with_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """Resize input image by width or height keeping proportion to the image"""

    dimension = None
    (h_source, w_source) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        resize = height / float(h_source)
        dimension = (int(w_source * resize), height)
    else:
        resize = width / float(w_source)
        dimension = (width, int(h_source * resize))

    return cv2.resize(image, dimension, interpolation=inter)


def error_check_path_is_empty_string(path):
    """
    Used to fail fast than too late.
    Also to avoid empty string in os path (when path is empty it takes script directory)
    """
    if path == "":
        raise ValueError("Error: variable is empty string")


def dir_from_path(path):
    """If path is file address. Strip file name and retrieve dir directory"""

    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def dir_exists(path):
    """
    Check if directory path exists. Even when path is dir + file.
    It is recommended to use when you want to check
    if directory in path where you want to create new file exists.
    """

    # https://docs.python.org/3/library/pathlib.html
    file_ext = Path(path).suffix

    # Retrieve dir path from file path
    if file_ext:
        path = dir_from_path(path)

    return os.path.isdir(path)


def url_to_image(url):  # https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
    """
    download the image, convert it to a NumPy array,
    and then read it into OpenCV format
    """

    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


def uri_validator(path):  # https://stackoverflow.com/a/38020041/12490791
    """Check if web address is syntacly valid"""

    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc, result.path])
    except:  # todo not sure what type exception is it
        return False


def make_sizes_of_images_the_same(source, target):
    """Resize target image to the same size as source if ratio between width and height are both the same"""

    # take dimensions
    (h_source, w_source) = source.shape[:2]
    (h_target, w_target) = target.shape[:2]

    # check if ratio of both images are the same
    source_ratio = w_source/h_source
    target_ratio = w_target/h_target

    same_ratio = (source_ratio == target_ratio)

    # to avoid too big size differences between images
    compared_ratio = w_target/w_source
    comparable_sizes = bool(
        IMAGES_SIZES["lowest ratio"] <= compared_ratio <= IMAGES_SIZES["highest ratio"])

    # resize image to the same size
    if same_ratio and comparable_sizes:
        target = resize_with_with_aspect_ratio(target, w_source)

    return target
