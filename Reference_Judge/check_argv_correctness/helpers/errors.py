from Reference_Judge.config import ARGV

ERRORS_MESSAGES = {
    "no file": "Error: File does not exists:",
    "no output": "Error: No output path",
    "4th last arg": f"Error: 4th, last argument should be numeric or be {ARGV['search by ratio'][0]} or {ARGV['search by ratio'][1]}:",
    "5th last arg": f'Error: 5th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:',
}
