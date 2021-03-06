"""common functions for helpers"""


# internal libs
from Show_Images_Differences.config.config import ARGV
from Show_Images_Differences.utils import resize_with_with_aspect_ratio


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
        if not image == "Source name":  # This is the only value in dict which is not a image
            resize = resize_with_with_aspect_ratio(images[image], width)
            images[image] = resize

    return images


def retrieve_argv_width(argv_, cap_len_argv):
    """take width from argv, dependably by number of argv"""

    # init variables
    n = cap_len_argv

    # Input user is width of reference image size
    width = int(argv_[n - 2])
    if not isinstance(width, int):
        raise "width value is not int"

    return width


def check_width_argv_exists(argv_, cap_len_argv):
    """return bool"""

    n = cap_len_argv
    return len(argv_) >= (n - 1) and argv_[n - 2].isnumeric()


def check_type_width(width):
    """raise error when it's not string"""

    if not isinstance(width, int):
        raise TypeError(f"Wrong type {type(width)}, it should be int")
