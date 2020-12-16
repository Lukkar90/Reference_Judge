"""Place to hold program's global const"""


# Python
import os
import sys


# https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
# must be tuple to provide multiply extensions
LEGAL_EXTENSIONS = tuple(".png")

ARGV = {
    "search by ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_SIZES = {
    "highest scale":  4.0,  # to avoid image distortions
    "lowest scale": 0.5,  # to avoid image distortions
    "biggest dimension": 1080,  # to avoid performance issues
    "smallest dimension": 1,
    "default width": 360,
}

SIMILARITY = {
    "enough": 0.95,  # SSMI value in calculating resemblance, 1 is Max
    # Why so low? Well... this is the lowest value in which matching makes any sense
    "not enough": 0.10
}


def set_app_path():

    if getattr(sys, 'frozen', False):
        application_path = ""  # relative ./
    elif __file__:
        application_path = f"{sys.argv[0]}/"
    else:
        raise IOError("no path")

    return application_path
