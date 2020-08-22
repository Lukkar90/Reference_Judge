from Reference_Judge.config import ARGV

ERRORS_MESSAGES = {
    "no file": "Error: File does not exists:",
    "no output": "Error: No output path",
    "4th last arg": f"Error: 4th, last argument should be numeric or be {ARGV['search by ratio'][0]} or {ARGV['search by ratio'][1]}:",
    "5th last arg": f'Error: 5th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:',
    "6th last arg": f'Error: 6th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}',
}


def get_error_directory_does_not_exists(dir_kind):

    return f"Error: Directory with {dir_kind} does not exist:"
