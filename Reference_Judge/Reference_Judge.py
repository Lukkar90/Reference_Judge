"""
NAME

    Reference-Judge

DESCRIPTION

    Showing visual differences between images
    ========================================

    Reference-Judge is used for developers to show visual differences
    between mobile app particular screen and reference created by mobile app designer.

    It's aims to improve workflow for programmer and also designer.

    For programmer this tool availables instant check of screen,
    if it is done according to references.

    For designer this tool relieve him/she from task of constant checking,
    if particular screen was done according to the reference.

    This program uses image recognition algorithms from https://opencv.org/
"""


# python libs
import sys

# internal libs
from Reference_Judge.check_argv_correctness.check_argv_correctness import check_argv_correctness
from Reference_Judge.config import ARGV, IMAGES_SIZES
from Reference_Judge.create_similar_images_list.create_similar_images_list import create_similar_images_list
from Reference_Judge.help import help_detailed_usage, user_commanded_help
from Reference_Judge.modes.save import save
from Reference_Judge.modes.show import show
from Reference_Judge.utils import check_ratio_argv


def Reference_Judge(_argv):
    """Parsing sys.argv to invoke in chosen paths modes: save or show, or to get help"""

    check_argv_correctness(_argv)
    if user_commanded_help(_argv):
        return help_detailed_usage()

    # Init variables
    original_ref_path = _argv[1]
    app_ref_path = _argv[2]
    mode = _argv[3]

    by_ratio = check_ratio_argv(_argv)

    similar_list = create_similar_images_list(
        original_ref_path, app_ref_path, by_ratio)

    width = IMAGES_SIZES["default width"]  # Default value for mobiles apps

    if mode in ARGV["save"]:

        save(width, similar_list, by_ratio, _argv)

    elif mode in ARGV["show"]:

        show(width, similar_list, by_ratio, _argv)

    else:
        raise ValueError("Error: Invalid mode value\n"
                         f" {mode}")

    sys.exit(0)
