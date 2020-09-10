"""
NAME

    Reference-Judge

DESCRIPTION

    Showing visual differences between images
    ========================================

    Reference-Judge is used for developers to show visual differences
    between the app's particular screen and reference created by the app's designer.

    It aims to improve workflow for the programmer and also designer.

    For a programmer this tool available instant check of the screen,
    if it is done according to references.

    For the designer, this tool relieve him/her from the task of constant checking,
    if a particular screen was done according to the reference.

    Of course, it can be used for any other matching images purposes

    This program uses image recognition algorithms from https://opencv.org/

AUTHOR

    Karol Łukaszczyk
    e-mail: lukkarcontact@gmail.com
"""


import sys
from manage import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
