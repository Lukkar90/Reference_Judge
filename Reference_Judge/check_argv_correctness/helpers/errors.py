"""list of errors in module Reference_Judge"""

# internal libs
from Reference_Judge.config import ARGV, IMAGES_SIZES

ERRORS_MESSAGES = {
    "no file": "Error: File does not exists:",
    "no output": "Error: No output path",
    "4th last arg": f"Error: 4th, last argument should be positive integer or be {ARGV['search by ratio'][0]} or {ARGV['search by ratio'][1]}:",
    "5th last arg": f'Error: 5th, last argument should be positive integer or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:',
    "6th last arg": f'Error: 6th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}',
    "output does not exists": "Error: Output directory does not exists:",
    "cant be url": "Error: output can\'t be url:",
    "Source App same": 'Error: "original references" and "app references" directories are the same:',
    "Source > App": 'Error: There are more images in "original references" dir than in "app references" dir:',
    "Source App same files": "Error: Both files have the same path:",
    "Original dir App file": "Error: Original reference path can't be directory, if app reference is only one file:",
    "404": "Error: path http: HTTP Error 404: Not Found:",
    "5th numeric": "Error: 5th should be positive integer.",
    "4th numeric": "Error: 4th should be positive integer.",
    "5th last arg -br": f'Error: 5th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:',
    "one arg too much": "Error: one argument too much:",
    "not mode": f'Error: 3th argument is invalid. It\'s not mode: {ARGV["show"][0]} or {ARGV["save"][0]}:',
    "output same as original": 'Output directory can\'t be the same as "original references":',
    "output same as app": 'Output directory can\'t be the same as "app references":',
}


def get_error_directory_does_not_exists(dir_kind):
    """dir kind = [dir, file ,url]"""

    return f"Error: Directory with {dir_kind} does not exist:"


def get_error_width_too_high(width):

    return f"Width value is too high: {width}. It should not be higher than: {IMAGES_SIZES['biggest dimension']}"


def get_error_width_too_low(width):

    return f"Width value is too low: {width}. It should not be smaller than: {IMAGES_SIZES['smallest dimension']}"


def get_error_no_images_in_dir(dir_kind):
    """dir kind = [dir, file ,url]"""

    return f"Error: There is no images in Directory with {dir_kind}:"


def get_error_wrong_web_path(web_type, alert):
    """web_type in ["http", "url"]"""

    return f"Error: path {web_type}: {alert}:"
