# internal libs
from config import ARGV
from utils import resize_with_with_aspect_ratio


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


def resize_all(images, width):
    """Change all image size keeping ratio"""

    for image in images:
        if not image == "Original_name":  # This is the only value in dict which is not a image
            resize = resize_with_with_aspect_ratio(images[image], width)
            images[image] = resize

    return images


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
