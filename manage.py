from Reference_Judge.Reference_Judge import Reference_Judge
from UI.MainUIApp import MainGUIApp


def execute_from_command_line(_argv):
    if len(_argv) == 1:
        MainGUIApp()
    else:
        Reference_Judge(_argv)
