# python libs
from urllib.parse import urlparse

# external libs
import numpy as np
import urllib.request
import cv2


def get_rid_end_slashes(path):  # It can be used only to the last argument
    # Get rid of "/" or "\", if User mistakenly add it at the end of string
    return path.rstrip('/\\\"\'')


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