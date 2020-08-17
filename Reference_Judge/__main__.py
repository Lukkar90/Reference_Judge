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
from help import help_detailed_usage, user_commanded_help
from check_argv_correctness.check_argv_correctness import check_argv_correctness
from create_similar_images_list.create_similar_images_list import create_similar_images_list
from config import ARGV, IMAGES_SIZES
from utils import check_ratio_argv

# same module
from modes.show import show
from modes.save import save


def main():
    """Parsing sys.argv to invoke in chosen paths modes: save or show, or to get help"""

    check_argv_correctness(sys.argv)
    if user_commanded_help(sys.argv):
        return help_detailed_usage()

    # Init variables
    original_ref_path = sys.argv[1]
    app_ref_path = sys.argv[2]
    mode = sys.argv[3]

    by_ratio = check_ratio_argv(sys.argv)

    similar_list = create_similar_images_list(
        original_ref_path, app_ref_path, by_ratio)

    width = IMAGES_SIZES["default width"]  # Default value for mobiles apps

    if mode in ARGV["save"]:

        save(width, similar_list, by_ratio)

    elif mode in ARGV["show"]:

        show(width, similar_list, by_ratio)

    else:
        raise ValueError("Error: Invalid mode value\n"
                         f" {mode}")

    sys.exit(0)


if __name__ == "__main__":
    main()
