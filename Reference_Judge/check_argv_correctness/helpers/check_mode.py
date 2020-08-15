# Python libs
import sys

# internal libs
from help import help_tip
from config import ARGV


def check_mode(argv_):
    """Check if images have to be saved or they will be shown"""

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

    if len(argv_) < 5:
        sys.exit("Error: No output path\n"
                 f"{help_tip()}")

    elif len(argv_) == 6 and not (argv_[5].isnumeric() or argv_[5] in ARGV["search by ratio"]):

        sys.exit(f'Error: 5th, last argument should be numeric or be {ARGV["search by ratio"][0]}:\n'
                 f" {argv_[5]}\n"
                 f"{help_tip()}")

    elif len(argv_) == 7 and argv_[6] not in ARGV["search by ratio"]:

        if not argv_[5].isnumeric():
            print('Error: 5th should be numeric.\n')

        if argv_[6] not in ARGV["search by ratio"]:
            sys.exit(f'Error: 6th, last argument should be {ARGV["search by ratio"][0]}:\n'
                     f" {argv_[6]}\n"
                     f"{help_tip()}")


def check_mode_show(argv_):
    """check correctness all argv in show mode"""

    if len(argv_) == 5 and not (argv_[4].isnumeric() or argv_[4] in ARGV["search by ratio"]):
        sys.exit(f'Error: 4th, last argument should be numeric or be {ARGV["search by ratio"][0]}:\n'
                 f" {argv_[4]}\n"
                 f"{help_tip()}")

    elif len(argv_) == 6:

        if not argv_[4].isnumeric():
            print('Error: 4th should be numeric.\n')

        if argv_[5] not in ARGV["search by ratio"]:
            sys.exit(f'Error: 5th, last argument should be {ARGV["search by ratio"][0]}:\n'
                     f" {argv_[5]}\n"
                     f"{help_tip()}")

    elif len(argv_) == 7:
        sys.exit("Error: one argument too much:\n"
                 f" {argv_[6]}\n"
                 f"{help_tip()}")
