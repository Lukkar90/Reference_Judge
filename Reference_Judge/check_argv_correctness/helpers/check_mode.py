"""check correctness of mode args and accompanying arguments"""


# Python libs
import sys

# internal libs
from Reference_Judge.config import ARGV
from Reference_Judge.help import help_tip

# same lib
from Reference_Judge.check_argv_correctness.helpers.errors import ERRORS_MESSAGES


def check_mode(argv_):
    """Check if images have to be saved or they have be shown"""

    mode = argv_[3]

    # check modes arguments
    if mode in ARGV["save"]:

        check_mode_save(argv_)

    elif mode in ARGV["show"]:

        check_mode_show(argv_)

    else:
        sys.exit(f'{ERRORS_MESSAGES["not mode"]}\n'
                 f" {argv_[3]}\n"
                 f"{help_tip()}")

    return mode


def check_mode_save(argv_):
    """check correctness all argv in save mode"""

    # USE ONLY HERE
    def is_output_path(argv_):
        return len(argv_) < 5

    def is_last_argv_by_ratio(argv_):
        return argv_[6] in ARGV["search by ratio"]

    def is_5th_legit_argv(argv_):
        return is_legit_width(argv_, 5) or is_5th_by_ratio(argv_)

    if is_output_path(argv_):
        sys.exit(f"{ERRORS_MESSAGES['no output']}\n"
                 f"{help_tip()}")

    elif len(argv_) == 6 and not is_5th_legit_argv(argv_):

        sys.exit(f'{ERRORS_MESSAGES["5th last arg"]}:\n'
                 f" {argv_[5]}\n"
                 f"{help_tip()}")

    elif len(argv_) == 7:

        if not is_legit_width(argv_, 5):
            sys.exit(f'{ERRORS_MESSAGES["5th numeric"]}\n'
                     f" {argv_[5]}\n"
                     f"{help_tip()}")

        if not is_last_argv_by_ratio(argv_):
            sys.exit(f'{ERRORS_MESSAGES["6th last arg"]}:\n'
                     f" {argv_[6]}\n"
                     f"{help_tip()}")


def check_mode_show(argv_):
    """check correctness all argv in show mode"""

    # USE ONLY HERE
    def is_4th_legit_argv(argv_):
        return is_legit_width(argv_, 4) or argv_[4] in ARGV["search by ratio"]

    if len(argv_) == 5 and not is_4th_legit_argv(argv_):
        sys.exit(f'{ERRORS_MESSAGES["4th last arg"]}\n'
                 f" {argv_[4]}\n"
                 f"{help_tip()}")

    elif len(argv_) == 6:

        if not is_legit_width(argv_, 4):

            sys.exit(f'{ERRORS_MESSAGES["4th numeric"]}\n'
                     f" {argv_[4]}\n"
                     f"{help_tip()}")

        if not is_5th_by_ratio(argv_):
            sys.exit(f'{ERRORS_MESSAGES["5th last arg -br"]}\n'
                     f" {argv_[5]}\n"
                     f"{help_tip()}")

    elif len(argv_) == 7:
        sys.exit(f"{ERRORS_MESSAGES['one arg too much']}\n"
                 f" {argv_[6]}\n"
                 f"{help_tip()}")


def is_5th_by_ratio(argv_):
    """return bool"""
    return argv_[5] in ARGV["search by ratio"]


def is_legit_width(argv_, i):
    """return bool"""
    return argv_[i].isnumeric()
