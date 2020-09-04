# python libs
import sys

# internal libs
from Reference_Judge.config import ARGV, IMAGES_SIZES
from Reference_Judge.check_argv_correctness.helpers.errors import get_error_width_too_high


def check_width_values(argv_):
    """
    check if width value is lower or equal IMAGES_SIZES["biggest dimension"]
    in save or show mode
    """

    mode = argv_[3]

    if len(argv_) >= 5:
        if mode in ARGV["show"]:
            check_legal_value(argv_, 6)

        elif mode in ARGV["save"]:
            check_legal_value(argv_, 7)


def check_legal_value(argv_, cap_len_argv):
    """check if width value is lower or equal IMAGES_SIZES["biggest dimension"]"""

    n = cap_len_argv

    if check_argv_len_with_width(argv_, n) and check_if_width_is_legal(argv_, n):

        # Input user is width of reference image size
        width = int(argv_[n - 2])

        # check if value is too high
        if width > IMAGES_SIZES["biggest dimension"]:
            sys.exit(get_error_width_too_high(width))


def check_argv_len_with_width(argv_, n):
    """return bool"""
    return len(argv_) >= (n - 1)


def check_if_width_is_legal(argv_, n):
    """return bool"""
    return argv_[n - 2].isnumeric()
