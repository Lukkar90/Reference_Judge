"""check correctnes of mode args and accompanying arguments"""


# Python libs
import sys

# internal libs
from Reference_Judge.config import ARGV
from Reference_Judge.help import help_tip


def check_mode(argv_):
    """Check if images have to be saved or they have be shown"""

    mode = argv_[3]

    # check modes arguments
    if mode in ARGV["save"]:

        check_mode_save(argv_)

    elif mode in ARGV["show"]:

        check_mode_show(argv_)

    else:
        sys.exit(f'Error: 3th argument is invalid. It\'s not mode: {ARGV["show"][0]} or {ARGV["save"][0]}:\n'
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
        sys.exit("Error: No output path\n"
                 f"{help_tip()}")

    elif len(argv_) == 6 and not is_5th_legit_argv(argv_):

        sys.exit(f'Error: 5th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                 f" {argv_[5]}\n"
                 f"{help_tip()}")

    elif len(argv_) == 7:

        if not is_legit_width(argv_, 5):
            sys.exit('Error: 5th should be numeric.\n')

        if not is_last_argv_by_ratio(argv_):
            sys.exit(f'Error: 6th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                     f" {argv_[6]}\n"
                     f"{help_tip()}")


def check_mode_show(argv_):
    """check correctness all argv in show mode"""

    # USE ONLY HERE
    def is_4th_legit_argv(argv_):
        return is_legit_width(argv_, 4) or argv_[4] in ARGV["search by ratio"]

    if len(argv_) == 5 and not is_4th_legit_argv(argv_):
        sys.exit(f'Error: 4th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                 f" {argv_[4]}\n"
                 f"{help_tip()}")

    elif len(argv_) == 6:

        if not is_legit_width(argv_, 4):
            sys.exit('Error: 4th should be numeric.\n')

        if not is_5th_by_ratio(argv_):
            sys.exit(f'Error: 5th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                     f" {argv_[5]}\n"
                     f"{help_tip()}")

    elif len(argv_) == 7:
        sys.exit("Error: one argument too much:\n"
                 f" {argv_[6]}\n"
                 f"{help_tip()}")


def is_5th_by_ratio(argv_):
    """return bool"""
    return argv_[5] in ARGV["search by ratio"]


def is_legit_width(argv_, i):
    """return bool"""
    return argv_[i].isnumeric()
