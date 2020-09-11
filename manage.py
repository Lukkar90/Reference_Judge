"""Deciding if CLI or UI is invoke"""


# Internal libs
from Reference_Judge.Reference_Judge import Reference_Judge
from UI.MainUIApp import MainGUIApp


def execute_from_command_line(_argv):
    """invoke UI or CLI"""

    if len(_argv) == 1:
        MainGUIApp()
    else:
        Reference_Judge(_argv)
