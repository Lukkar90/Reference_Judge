# import the necessary packages
from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2

from utlis import url_to_image, uri_validator  # internal lib


def compute_image_diffrences(similar_pair):  # https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/

	# construct the argument
	paths = {
		"first": similar_pair["original_reference_path"],
		"second": similar_pair["app_reference_path"]
	}

	# Upload name which would be used to save file in output directory
	original_name = similar_pair["original_reference_name"]

	# load the two input images
	if uri_validator(paths["first"]):
		print("A")
		imageA = url_to_image(paths["first"])
	else:
		imageA = cv2.imread(paths["first"])

	if uri_validator(paths["second"]):
		print("B")
		imageB = url_to_image(paths["second"])
	else:
		imageB = cv2.imread(paths["second"])

	# compute diffrence between imageA and imageB in BGR
	diff_BGR = cv2.subtract(imageA, imageB)

	# convert the images to grayscale
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

	# compute the Structural Similarity Index (SSIM) between the two
	# images, ensuring that the difference image is returned
	diff = structural_similarity(grayA, grayB, full=True)[1]
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
		cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)


	# Images to latter process
	computed_images = {

		"Original_name": original_name,
		"Original": imageA,
		"Modified": imageB,
		"Diffrence_RGB": diff_BGR,
		"Diffrence_Structure": diff,
		"Thresh": thresh

	}

	return computed_images