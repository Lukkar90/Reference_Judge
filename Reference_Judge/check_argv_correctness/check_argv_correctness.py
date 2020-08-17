"""
This module is responsible for checking if program arguments are correct
"""


# python lib
import os
import sys
from urllib import error, request

# internal libs
from config import ARGV, IMAGES_SIZES, LEGIT_EXTENSIONS
from help import help_command_line, help_tip
from utils import dir_exists, error_check_path_is_empty_string, uri_validator

# same lib
from check_argv_correctness.helpers.check_paths import check_paths
from check_argv_correctness.helpers.check_mode import check_mode
from check_argv_correctness.helpers.check_width_values import check_width_values


def check_argv_correctness(argv_):
    """check if all argvs have correct paths, modes and width values"""

    program_name = argv_[0]

    # incorrect number of arguments
    if not (len(argv_) == 2 or (len(argv_) >= 4 and len(argv_) <= 7)):
        sys.exit(f"{help_command_line()}\n"
                 f"{help_tip()}")

    # invalid usage
    elif len(argv_) == 2 and not argv_[1] in ARGV["help"]:
        sys.exit(f"Error: invalid 1st argument. Usage: python {program_name} {ARGV['help'][0]} or {ARGV['help'][1]}:\n"
                 f" {argv_[1]}")

    # correct number of arguments
    elif len(argv_) >= 4 and len(argv_) <= 7:

        check_paths(argv_)

        check_mode(argv_)

        check_width_values(argv_)
