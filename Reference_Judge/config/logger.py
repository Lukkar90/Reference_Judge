"""Tools to read, process and save logger.ini"""


# python libs
from datetime import datetime
import sys
import os

# internal libs
from Reference_Judge.utils import read_config_file, get_output_dir


class Logger():
    """defining all attributes of logger functionality"""

    def __init__(self):
        self.logger_path = self.define_log_path()
        self.logger = read_config_file(self.logger_path)

    def set_saving_bool(self):
        """SETTING logger state for saving any errors during running reference_judge module
        in selected output folder"""

        value_start = self.logger.get("ERRORS", "save errors")
        value_to_save = "yes" if value_start == "no" else "no"

        self.logger.set("ERRORS", "save errors", value_to_save)

        try:
            with open(self.logger_path, "w") as configfile:
                self.logger.write(configfile)
        except IOError:
            return "Error!", f"Logger saving status is not changed\nvalue now:\n{value_start}"

        return f"Succes!\nYour saving logs are set to:\n{value_to_save}"

    def load_saving_bool(self):
        """LOADING logger state for saving any errors during running reference_judge module
        in selected output folder"""

        return self.logger.getboolean("ERRORS", "save errors")

    def get_saving_value(self):
        """GET logger state for saving any errors during running reference_judge module
        in selected output folder"""

        return self.logger.get("ERRORS", "save errors")

    def define_log_path(self):
        """define log path depending if is run test or just app"""

        program_name = sys.argv[0]

        path = "Reference_Judge\\config\\logger.ini"

        if program_name == "Reference_Judge":
            append_path = "Reference_Judge\\"
            path = append_path + path

        return path


def write_in_log(section, output_file_path, script_run_date):
    """
    append new record every time or when log does not exist it
    creates new one in output file
    """

    # initial variables
    output_dir_path = get_output_dir(output_file_path)

    file_path = _get_log_path(output_dir_path, script_run_date)

    current_date = get_current_date()

    file_exists = check_if_file_exists(output_dir_path, file_path)

    output_file_name = os.path.basename(output_file_path)

    # write path to file
    text_to_paste = f"{section}\n{current_date} {output_file_name}"

    if file_exists:

        new_line = create_new_line_to_log(file_path, section, text_to_paste)

        write_line_into_log(file_path, new_line)

    else:

        write_line_into_log(file_path, text_to_paste)


def create_new_line_to_log(file_path, section, text_to_paste):
    """takes old string and return new string with new line"""

    with open(file_path, 'r') as errors_file:
        content = errors_file.read()
        new_line = content.replace(
            section,
            text_to_paste
        )
    return new_line


def write_line_into_log(file_path, text_to_paste):
    """overwrite or write provided string in provided file path"""

    with open(file_path, "w") as new_file:
        new_file.write(text_to_paste)


def check_if_file_exists(output_dir_path, file_path):
    """returns bool"""

    output_dir_path = get_output_dir(output_dir_path)

    file_exists = False
    for name in os.listdir(output_dir_path):
        if os.path.isfile(file_path) and name.endswith(".txt"):
            file_exists = True
            break
    return file_exists


def get_current_date():
    """retruns fromated string"""

    datetime_object = datetime.now()
    current_date = datetime_object.strftime("%Y_%m_%d-%H_%M")
    return current_date


def _get_log_path(output_dir_path, script_run_date):
    """returns string path"""

    file_name = f"ERRORS-{script_run_date}.txt"
    file_path = os.path.join(output_dir_path, file_name)

    return file_path
