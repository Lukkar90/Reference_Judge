# Python libs
import os
import sys

# external libs
import cv2
import numpy as np

# internal libs
from compute_image_differences.compute_image_differences import compute_image_differences
from add_text_to_image.add_text_to_image import add_text_to_image, is_bigger_than

# same module
from modes.utils import check_width_argv_exists, check_correctness_optional_argvs, retrieve_argv_width, resize_all


def save(width, similar_list, by_ratio):
    """save matched images in chosen directory"""

    if len(sys.argv) >= 5:
        output_path = sys.argv[4]
    else:
        output_path = None

    # Optional args
    if len(sys.argv) >= 6:
        check_correctness_optional_argvs(sys.argv, 7)
        if check_width_argv_exists(sys.argv, 7):
            width = retrieve_argv_width(sys.argv, 7, width)

    # Process all images, save each sequence in chosen director
    for similar_pair in similar_list:

        if not similar_pair is None:

            images = compute_image_differences(similar_pair, by_ratio)

            save_images_as_one(images, output_path, width)


def save_images_as_one(images, output_path, width):
    """save app and ref images with images showing differences in one image"""

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images to display
    original_name = images["Original_name"]
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Difference_RGB"]
    diff = images["Difference_Structure"]
    thresh = images["Thresh"]

    # All images have to be RGB, changing grayscale back to RGB
    diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    # check if canvas is to small to add text
    if is_bigger_than(100, original):

        original = add_text_to_image(original, "Original")
        modified = add_text_to_image(modified, "Modified")
        diff_BGR = add_text_to_image(diff_BGR, "Difference_RGB")
        diff = add_text_to_image(diff, "Difference_Structure")
        thresh = add_text_to_image(thresh, "Thresh")

    # Combining all images into one
    numpy_horizontal_concat = np.concatenate(
        [original, modified, diff_BGR, diff, thresh], axis=1)

    # Check if choosed loaction is file like
    ext_file = os.path.splitext(output_path)[1]

    # Define output path
    if not ext_file:
        output_path = os.path.join(output_path, original_name)

    # Check if file already exists, if so, add new one with name incremented by one
    if os.path.exists(output_path):
        output_path = next_path(output_path)

    # User notfication where to search saved image
    print("Saved reference : {} in {}".format(original_name, output_path))

    # Save image into choosed loaction
    cv2.imwrite(output_path, numpy_horizontal_concat)


def next_path(path_pattern):  # https://stackoverflow.com/a/47087513/12490791
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-00001.txt
    file-00002.txt
    file-00003.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """
    temp_dir = os.path.dirname(path_pattern)
    temp_full_name = os.path.basename(path_pattern)
    # https://stackoverflow.com/a/6670331/12490791
    temp_name, temp_ext = temp_full_name.split('.', 1)

    i = 1

    # First do an exponential search
    while os.path.exists(format_path(temp_dir, temp_name, i, temp_ext)):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (first..last] and narrow it down until first + 1 = last
    first, last = (i // 2, i)
    while first + 1 < last:
        mid = (first + last) // 2  # interval midpoint
        first, last = (mid, last) if os.path.exists(format_path(
            temp_dir, temp_name, mid, temp_ext)) else (first, mid)

    # .replace("\\", "/") to make path string more consistent
    return format_path(temp_dir, temp_name, last, temp_ext).replace("\\", "/")


def format_path(temp_dir, temp_name, index, temp_ext):
    """example_dir_path/file-0000%.ext"""

    return f"{temp_dir}/{temp_name}-{str(index).zfill(5)}.{temp_ext}"
