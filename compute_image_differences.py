"""
This module return images differences between image original reference and app reference
"""
# external libs
import cv2
import imutils
from skimage.metrics import structural_similarity

# internal libs
from utils import uri_validator, url_to_image


def compute_image_differences(similar_pair):  # https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/

    # construct the argument
    paths = {
		"first": similar_pair["original_reference_path"],
		"second": similar_pair["app_reference_path"]
    }

    # Upload name which would be used to save file in output directory
    original_name = similar_pair["original_reference_name"]

    # load the two input images
    if uri_validator(paths["first"]):

        image_A = url_to_image(paths["first"])
    else:
        image_A = cv2.imread(paths["first"])

    if uri_validator(paths["second"]):

        image_B = url_to_image(paths["second"])
    else:
        image_B = cv2.imread(paths["second"])

    # compute difference between imageA and imageB in BGR
    diff_BGR = cv2.subtract(image_A, image_B)

    # convert the images to grayscale
    gray_A = cv2.cvtColor(image_A, cv2.COLOR_BGR2GRAY)
    gray_B = cv2.cvtColor(image_B, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    diff = structural_similarity(gray_A, gray_B, full=True)[1]
    diff = (diff * 255).astype("uint8")

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
            				cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
           					cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image_A, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(image_B, (x, y), (x + w, y + h), (0, 0, 255), 2)


    # Images to latter process
    computed_images = {
		"Original_name": original_name,
		"Original": image_A,
		"Modified": image_B,
		"Difference_RGB": diff_BGR,
		"Difference_Structure": diff,
		"Thresh": thresh
    }

    return computed_images
