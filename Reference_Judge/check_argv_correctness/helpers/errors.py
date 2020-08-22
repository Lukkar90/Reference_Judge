"""list of errors in module Reference_Judge"""

# internal libs
from Reference_Judge.config import ARGV, IMAGES_SIZES

ERRORS_MESSAGES = {
    "no file": "Error: File does not exists:",
    "no output": "Error: No output path",
    "4th last arg": f"Error: 4th, last argument should be numeric or be {ARGV['search by ratio'][0]} or {ARGV['search by ratio'][1]}:",
    "5th last arg": f'Error: 5th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:',
    "6th last arg": f'Error: 6th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}',
    "output does not exists": "Error: Output directory does not exists:",
    "cant be url": "Error: output can\'t be url:",
    "Original App same": 'Error: "original references" and "app references" directories are the same:',
    "Original > App": 'Error: There are more images in "original references" dir than in "app references" dir:',
    "Original App same files": "Error: Both files have the same path:"
}


def get_error_directory_does_not_exists(dir_kind):

    return f"Error: Directory with {dir_kind} does not exist:"


def get_error_width_too_high(width):

    return f"Width value is too high: {width}. It should not be higher than: {IMAGES_SIZES['biggest dimmension']}"
