# python libs
import sys

# internal libs
from Reference_Judge.utils import read_config_file


class Logger():
    """defining all attributes of logger functionality"""

    def __init__(self):
        self.logger_path = f"{sys.argv[0]}\\Reference_Judge\\config\\logger.ini"
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
