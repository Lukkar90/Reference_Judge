# python libs
import os
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

# external libs
import cv2
import numpy as np


def dir_from_path(path):

    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def dir_exists(path):

	file_ext = Path(path).suffix  # https://docs.python.org/3/library/pathlib.html

	# if path is file
	if file_ext:
		path = dir_from_path(path)
		return os.path.exists(path)
    # if path is already dir
	else:
		return os.path.isdir(path)


def url_to_image(url):  # https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format

	response = urllib.request.urlopen(url)
	image = np.asarray(bytearray(response.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image


def uri_validator(x):  # https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False
