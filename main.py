from sys import argv
from create_similar_images_list import create_similar_images_list
from compute_image_diffrences import compute_image_diffrences
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os


def check_if_argv_is_correct(argv):

    program_name = argv[0]

    #  argv[0] == program name, argv[1] == data.csv
    if len(argv) < 3 or len(argv) > 6:
        print(f"Usage: python {program_name} <directory_orignal_refs> <directory_app_refs> <mode> [directory_diffrences_output] [width]")  # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
        print("For more information:")
        print(f"Usage: python {program_name} help")
        exit(1)


def resize_with_wspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):  # https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display

    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def resize_all(images, width):

    for image in images:
        if not image == "Original_name":  # This is the only value in dict which is not a image
            resize = resize_with_wspect_ratio(images[image], width)
            images[image] = resize

    return images

def show_images(images, width):

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Diffrence_RGB"]
    diff = images["Diffrence_Structure"]
    thresh = images["Thresh"]

    # Show images
    cv2.imshow("Original", original)
    cv2.imshow("Modified", modified)
    cv2.imshow("Diffrence_RGB", diff_BGR)
    cv2.imshow("Diffrence_Structure", diff)
    cv2.imshow("Thresh", thresh)


def save_images_as_one(images, output_directory, width):

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images to display
    original_name = images["Original_name"]
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Diffrence_RGB"]
    diff = images["Diffrence_Structure"]
    thresh = images["Thresh"]

    # All images have to be RGB, changing grayscale back to RGB
    diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    # Combining all images into one
    numpy_horizontal_concat = np.concatenate([original, modified, diff_BGR, diff, thresh], axis=1)

    # User notfication where to search saved image
    print("Saved reference : {} in {}".format(original_name, output_directory))

    # Check if choosed loaction is directory or file like
    root_dir, ext_dir = os.path.splitext(output_directory)
    if ext_dir:
        output_path = output_directory
    else:
        output_path = os.path.join(output_directory, original_name)

    # Save image into choosed loaction
    cv2.imwrite(output_path, numpy_horizontal_concat)


def main():

    check_if_argv_is_correct(argv)

    # Init variables
    original_ref_path = argv[1]
    app_ref_path = argv[2]
    mode = argv[3]

    similar_list = create_similar_images_list(original_ref_path, app_ref_path)

    if mode == "save":

        # Optional args
        if len(argv) >= 5:
            output_directory = argv[4]
        else:
            output_directory = None

        if len(argv) == 6:
            width = int(argv[5])  # Input user is width of reference image size
        else:
            width = 360  # Default

        

        # Process all images, save each sequence in choosed director
        for similar_pair in similar_list:

            images = compute_image_diffrences(similar_pair)

            save_images_as_one(images, output_directory, width)

    elif mode == "show":

        # Optional arg
        if len(argv) == 5:
            width = int(argv[4])
        else:
            width = 360  # Default

        # Process all images, show user each sequence one by one
        for similar_pair in similar_list:

            images = compute_image_diffrences(similar_pair)

            show_images(images, width)
            cv2.waitKey(0)

    exit(0)

if __name__ == "__main__":
    main()