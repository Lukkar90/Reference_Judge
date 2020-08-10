"""
NAME

    Reference-Judge

DESCRIPTION

    Showing visual differences between images
    ========================================

    Reference-Judge is used for developers to show visual differences
    between mobile app particular screen and reference created by mobile app designer.

    It's aims to improve workflow for programmer and also designer.

    For programmer this tool available instant check of screen if it is done according to references
    For designer this tool relieve him/she from task of checking if particular screen was done according to reference.

    This program uses image recognition algorithms from https://opencv.org/
"""

# python libs
import os
import sys

# external libs
import cv2
import numpy as np

# internal libs
from check_if_argv_is_correct import check_if_argv_is_correct, help_content
from compute_image_differences import compute_image_differences
from create_similar_images_list import create_similar_images_list
from utils import resize_with_with_aspect_ratio
from app_data import ARGV


def resize_all(images, width):
    """Change all image size keeping ratio"""

    for image in images:
        if not image == "Original_name":  # This is the only value in dict which is not a image
            resize = resize_with_with_aspect_ratio(images[image], width)
            images[image] = resize

    return images


def format_path(temp_dir, temp_name, index, temp_ext):
    """example_dir_path/file-0000%.ext"""

    return f"{temp_dir}/{temp_name}-{str(index).zfill(5)}.{temp_ext}"


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


def show_images(images, width):
    """show user differences between app image and reference"""

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Difference_RGB"]
    diff = images["Difference_Structure"]
    thresh = images["Thresh"]

    # Show images
    cv2.imshow("Original", original)
    cv2.imshow("Modified", modified)
    cv2.imshow("Difference_RGB", diff_BGR)
    cv2.imshow("Difference_Structure", diff)
    cv2.imshow("Thresh", thresh)


def save_images_as_one(images, output_path, width):
    """save app and ref images with images showing differences in one file"""

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


def program_help(argv_):
    """showing user "usage" of program"""

    program_name = argv_[0]

    if len(argv_) == 2 and argv_[1] in ARGV["help"]:
        sys.exit("\n"
                 f"{help_content()}\n"
                 "\n"
                 "On desktop:\n"
                 " save:\n"
                 f"  python {program_name} path_dir path_dir {ARGV['save'][0]} path_dir [px] [ratio]\n"
                 f"  python {program_name} path_dir path_dir {ARGV['save'][0]} path_file [px] [ratio]\n"
                 f"  python {program_name} path_file path_dir {ARGV['save'][0]} path_dir [px] [ratio]\n"
                 f"  python {program_name} path_file path_file {ARGV['save'][0]} path_dir [px] [ratio] *\n"
                 f"  python {program_name} path_file path_file {ARGV['save'][0]} path_file [px] [ratio] *\n"
                 "\n"
                 " show:\n"
                 f"  python {program_name} path_dir path_dir {ARGV['show'][0]} [px] [ratio]\n"
                 f"  python {program_name} path_file path_dir {ARGV['show'][0]} [px] [ratio]\n"
                 f"  python {program_name} path_file path_file {ARGV['show'][0]} [px] [ratio] *\n"
                 "\n"
                 "HTTPS:\n"
                 " save:\n"
                 f"  python {program_name} https/address.com/image.img https/address.com/image.img {ARGV['save'][0]} path_dir [px] [ratio] *\n"
                 f"  python {program_name} https/address.com/image.img https/address.com/image.img {ARGV['save'][0]} path_file [px] [ratio] *\n"
                 f"  python {program_name} https/address.com/image.img path_dir {ARGV['save'][0]} path_dir [px] [ratio]\n"
                 f"  python {program_name} https/address.com/image.img path_dir {ARGV['save'][0]} path_file [px] [ratio]\n"
                 f"  python {program_name} path_file https/address.com/image.img {ARGV['save'][0]} path_dir [px] [ratio] *\n"
                 f"  python {program_name} path_file https/address.com/image.img {ARGV['save'][0]} path_file [px] [ratio] *\n"
                 "\n"
                 " show:\n"
                 f"  python {program_name} https/address.com/image.img https/address.com/image.img {ARGV['show'][0]} [px] [ratio] *\n"
                 f"  python {program_name} path_file https/address.com/image.img {ARGV['show'][0]} [px] [ratio] *\n"
                 f"  python {program_name} https/address.com/image.img path_file {ARGV['show'][0]} [px] [ratio] *\n"
                 f"  python {program_name} https/address.com/image.img path_dir {ARGV['show'][0]} [px] [ratio]\n"
                 "\n"
                 " * images have to be the same size\n"
                 " [px] is optional value of width of each image\n"
                 f" abbr of {ARGV['save'][0]} is {ARGV['save'][1]}\n"
                 f" abbr of {ARGV['show'][0]} is {ARGV['show'][1]}\n"
                 f" [ratio] {ARGV['search by ratio'][0]} or {ARGV['search by ratio'][1]} -> images could be different sizes but they have to be the same ratio"
                 )


def check_correctness_optional_argvs(argv_, cap_len_argv):
    """notify developer when problem occurs"""

    #  init variable
    n = cap_len_argv

    # check correctness
    if len(argv_) == (n - 1):

        if argv_[n - 2] not in ARGV["search by ratio"] and not argv_[n - 2].isnumeric():
            raise ValueError(f'Error: Invalid argument value. It should be numeric or {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}\n'
                             f" {argv_[n -2]}")

    elif len(argv_) == n:

        if argv_[n - 1] not in ARGV["search by ratio"]:
            raise ValueError(f'Error: Invalid argument value. It should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}\n'
                             f" {argv_[n -1]}")


def retrieve_width(argv_, cap_len_argv, DEFAULT_width):
    """take width from argv, dependably by numeber of argv"""

    # init variables
    n = cap_len_argv
    width = None

    # check width param
    if len(argv_) >= (n - 1) and argv_[n - 2].isnumeric():

        # Input user is width of reference image size
        width = int(argv_[n - 2])

    if width is not None:
        return width
    else:
        return DEFAULT_width


def parse_optional_argvs(argv_, cap_len_argv, DEFAULT_width):
    """check if width, search_by_ratio are correct. If both are it returns width"""

    check_correctness_optional_argvs(argv_, cap_len_argv)

    return retrieve_width(argv_, cap_len_argv, DEFAULT_width)


def main():
    """Parsing sys.argv to pass them into right functions"""

    check_if_argv_is_correct(sys.argv)
    program_help(sys.argv)

    # Init variables
    original_ref_path = sys.argv[1]
    app_ref_path = sys.argv[2]
    mode = sys.argv[3]

    # [-1] To avoid checking 3 places at one, this argument is always last
    by_ratio = bool(sys.argv[-1] in ARGV["search by ratio"])

    similar_list = create_similar_images_list(
        original_ref_path, app_ref_path, by_ratio)

    width = 360  # Default

    if mode in ARGV["save"]:

        mode_save(width, similar_list, by_ratio)

    elif mode in ARGV["show"]:

        # Optional args
        mode_show(width, similar_list, by_ratio)
    else:
        raise ValueError("Error: Invalid mode value\n"
                         f" {mode}")

    sys.exit(0)


def mode_show(width, similar_list, by_ratio):
    """show matched images"""

    # Optional args
    if len(sys.argv) >= 6:
        width = parse_optional_argvs(sys.argv, 6, width)

    # Process all images, show user each sequence one by one
    for similar_pair in similar_list:

        if not similar_pair is None:

            images = compute_image_differences(similar_pair, by_ratio)

            show_images(images, width)

            print('NOTE: Press the "0" key, to close opened windows')
            cv2.waitKey(0)


def mode_save(width, similar_list, by_ratio):
    """save matched images in chosen directory"""

    if len(sys.argv) >= 5:
        output_path = sys.argv[4]
    else:
        output_path = None

    # Optional args
    if len(sys.argv) >= 6:
        width = parse_optional_argvs(sys.argv, 7, width)

    # Process all images, save each sequence in chosen director
    for similar_pair in similar_list:

        if not similar_pair is None:

            images = compute_image_differences(similar_pair, by_ratio)

            save_images_as_one(images, output_path, width)


if __name__ == "__main__":
    main()
