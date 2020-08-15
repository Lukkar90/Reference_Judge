# python libs
import os
import sys

# internal libs
from config import ARGV, IMAGES_SIZES


def check_width_values(argv_):
    """check if width value is lower or equal IMAGES_SIZES["biggest dimmension"] in save or show mode"""

    mode = argv_[3]

    if len(argv_) >= 5:
        if mode in ARGV["show"]:
            check_legal_value(argv_, 6)

        elif mode in ARGV["save"]:
            check_legal_value(argv_, 7)


def check_legal_value(argv_, cap_len_argv):
    """check if width value is lower or equal IMAGES_SIZES["biggest dimmension"]"""

    n = cap_len_argv

    if len(argv_) >= (n - 1) and argv_[n - 2].isnumeric():

        # Input user is width of reference image size
        width = int(argv_[n - 2])

        # check if value is too high
        if width > IMAGES_SIZES["biggest dimmension"]:
            sys.exit(
                f"Width value is too high: {width}. It should not be higher than: {IMAGES_SIZES['biggest dimmension']}")
