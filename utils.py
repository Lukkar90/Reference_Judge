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

def error_check_variable_is_empty_string(variable):
    """
    Used to fail fast than too late.
    Also to avoid empty string in os path (when path is empty it takes script directory)
    """
    if variable == "":
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

    file_ext = Path(path).suffix  # https://docs.python.org/3/library/pathlib.html

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
    except:
        return False
