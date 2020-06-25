from sys import argv
from create_similar_images_list import create_similar_images_list  # internal lib
from compute_image_diffrences import compute_image_diffrences  # internal lib
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

def format_path(temp_dir, temp_name, index, temp_ext):

    return "{0}/{1}-{2}.{3}".format(temp_dir, temp_name, str(index).zfill(5), temp_ext)  # example_dir_path/file-0000%.ext


def next_path(path_pattern):  # https://stackoverflow.com/a/47087513/12490791
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """

    temp_dir = os.path.dirname(path_pattern)
    temp_full_name = os.path.basename(path_pattern)
    temp_name, temp_ext = temp_full_name.split('.', 1)  # https://stackoverflow.com/a/6670331/12490791

    i = 1

    # First do an exponential search
    while os.path.exists(format_path(temp_dir, temp_name, i, temp_ext)):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2 # interval midpoint
        a, b = (c, b) if os.path.exists(format_path(temp_dir, temp_name, c, temp_ext)) else (a, c)

    return format_path(temp_dir, temp_name, b, temp_ext).replace("\\", "/")  # .replace("\\", "/") to make path string more consistent


def save_images_as_one(images, output_path, width):

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

    # Check if choosed loaction is file like
    root_dir, ext_file = os.path.splitext(output_path)
    # If it is dir path
    if not ext_file:
        output_path = os.path.join(output_path, original_name)
    else:
        if os.path.exists(output_path):
            output_path = next_path(output_path)

    # User notfication where to search saved image
    print("Saved reference : {} in {}".format(original_name, output_path))

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
            output_path = argv[4]
        else:
            output_path = None

        if len(argv) == 6:
            width = int(argv[5])  # Input user is width of reference image size
        else:
            width = 360  # Default

        
        # Process all images, save each sequence in choosed director
        for similar_pair in similar_list:

            images = compute_image_diffrences(similar_pair)

            save_images_as_one(images, output_path, width)

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