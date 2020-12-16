"""Deciding if CLI or UI is invoke"""


# Internal libs
from Show_Images_Differences.Show_Images_Differences import Show_Images_Differences
from UI.MainUIApp import MainGUIApp


def execute_from_command_line(_argv):
    """invoke UI or CLI"""

    if len(_argv) == 1:
        MainGUIApp()
    else:
        Show_Images_Differences(_argv)
