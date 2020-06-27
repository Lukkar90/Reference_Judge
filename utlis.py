import numpy as np
import urllib.request
import cv2
from urllib.parse import urlparse

def url_to_image(url):  # https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format

	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image


def uri_validator(x):  # https://stackoverflow.com/a/38020041/12490791
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False