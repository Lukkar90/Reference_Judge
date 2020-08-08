"""
This module is responsible for checking if program arguments are correct
"""
# python lib
import os
import sys
from urllib import error, request
import __main__

# internal libs
from app_data import legit_extensions
from utils import dir_exists, uri_validator, error_check_path_is_empty_string


def url_exists(url):
    """Check if url exists on web"""

    try:
        request.urlopen(url)
    except error.HTTPError as alert:
        sys.exit(f"Error: path http: {alert}:\n"
                 f" {url}")
    except error.URLError as alert:
        sys.exit(f"Error: path url: {alert}:\n"
                 f" {url}")

    return True


def count_legit_images(directory_path):
    """Count all images with legit_extensions"""

    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name)) and name.endswith(tuple(legit_extensions))])


def is_empty(directory_path):
    """Check if there are images with legit_extensions"""

    # Init variables
    there_are_files = False

    # check if there is any legit image in directory
    for file_name in os.listdir(directory_path):

        full_path = os.path.join(directory_path, file_name)

        if os.path.isfile(full_path) and file_name.endswith(tuple(legit_extensions)):
            there_are_files = True
            break

    return not there_are_files


def help_tip():
    """String to use when user write wrong input, showing him how to invoke help function"""

    # https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    program_name = __main__.__file__

    return f"For more information:\n Usage: python {program_name} --help"


def help_content():
    """Explaining user general usage of program"""

    # https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    program_name = __main__.__file__

    # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
    return f"Usage: python {program_name} <original_reference_path> <app_reference_path> <--mode> [directory_differences_output] [width] [--search_by_ratio]"


def check_mode(argv_):
    """Check if images have to be saved or they will be shown"""

    mode = argv_[3]

    # check modes arguments
    if mode == "--save":
        if len(argv_) < 5:
            sys.exit("Error: No output path\n"
                     f"{help_tip()}")

        elif len(argv_) == 6 and (not argv_[5].isnumeric() or argv_[5] != "--search_by_ratio"):

            sys.exit('Error: 5th, last argument should be numeric or be "--search_by_ratio":\n'
                     f" {argv_[5]}\n"
                     f"{help_tip()}")
        
        elif len(argv_) == 7 and argv_[6] != "--search_by_ratio":

            if not argv_[5].isnumeric():
                print('Error: 5th should be numeric.\n')

            sys.exit('Error: 6th, last argument should be"--search_by_ratio":\n'
                f" {argv_[5]}\n"
                f"{help_tip()}")
                     

    elif mode == "--show":
        if len(argv_) == 5 and (not argv_[4].isnumeric() or argv_[4] != "--search_by_ratio"):
            sys.exit('Error: 4th, last argument should be numeric or be "--search_by_ratio":\n'
                     f" {argv_[4]}\n"
                     f"{help_tip()}")

        elif len(argv_) == 6:

            if not argv_[4].isnumeric():
                print('Error: 4th should be numeric.\n')

            sys.exit('Error: 5th, last argument should be "--search_by_ratio":\n'
                f" {argv_[5]}\n"
                f"{help_tip()}")

        elif len(argv_) == 7:
            sys.exit("Error: one argument too much:\n"
                     f" {argv_[5]}\n"
                     f"{help_tip()}")
    else:
        sys.exit('Error: 3th argument is invalid. It\'s not mode: "--show" or "--save":\n'
                 f" {argv_[3]}\n"
                 f"{help_tip()}")

    return mode


def check_paths(argv_):
    """Check if files/dir/url paths program arguments are correct"""

    # Path args
    original_reference_path = argv_[1]
    app_reference_path = argv_[2]
    output_path = None
    # this argument position can be also width
    if len(argv_) >= 5 and not argv_[4].isnumeric():
        output_path = argv_[4]

    # Path kind args
    original_ref_is = None
    app_ref_is = None
    output_is = None

    # Checking what kind of paths are
    original_ref_is = check_path_kind(original_reference_path)
    app_ref_is = check_path_kind(app_reference_path)

    if output_path:
        output_is = check_path_kind(output_path)
        if output_is == "url":
            sys.exit("Error: output can't be url:\n"
                     f" {output_path}\n"
                     f"{help_tip()}")

    # Paths validation depending on kind
    path_validation(original_ref_is, original_reference_path,
                    "original references")
    path_validation(app_ref_is, app_reference_path, "app references")

    if output_is and not dir_exists(output_path):
        sys.exit(f"Error: Output directory does not exists:\n"
                 f" {output_path}\n"
                 f"{help_tip()}")

    # If original path and app path are dirs
    if original_ref_is == "dir" and app_ref_is == "dir":

        if original_reference_path == app_reference_path:
            sys.exit('Error: "original references" and "app references" directories are the same:\n'
                     f" {original_reference_path}\n"
                     f"{help_tip()}")

        if count_legit_images(original_reference_path) > count_legit_images(app_reference_path):
            sys.exit('Error: There are more images in "original references" dir than in "app references" dir:\n'
                     f" {original_reference_path}\n"
                     f" {app_reference_path}\n"
                     f"{help_tip()}")

    # If original path and app path are files
    if (original_ref_is == "file" and app_ref_is == "file") or (original_ref_is == "url" and app_ref_is == "url"):

        if original_reference_path == app_reference_path:
            # Checking if paths/url are not the same
            sys.exit("Error: Both files have the same path:\n"
                     f" {original_reference_path}\n"
                     f"{help_tip()}")

    # If original path is dir and app path is file
    if original_ref_is == "dir" and app_ref_is in ('file', 'url'):
        sys.exit("Error: Original reference path can't be directory, if app reference is only one file:\n"
                 f" {original_reference_path}\n"
                 f" {app_reference_path}\n"
                 f"{help_tip()}")


def check_path_kind(original_reference_path):
    """Check what kind of path is: url, file, dir"""

    # Checking paths arguments
    ext_path = os.path.splitext(original_reference_path)[1]

    # Check original path kind
    if ext_path:

        if uri_validator(original_reference_path):
            return "url"
        else:
            return "file"
    else:
        return "dir"


def path_validation(path_kind, reference_path, dir_kind):
    """Check if path exists: url, file, dir"""

    error_check_path_is_empty_string(dir_kind)

    if path_kind == "url":

        url_exists(reference_path)  # exit prompt is inside function

    elif path_kind == "file":

        if not os.path.isfile(reference_path):
            sys.exit(f"Error: File does not exists:\n"
                     f" {reference_path}\n"
                     f"{help_tip()}")

    elif path_kind == "dir":

        if not os.path.exists(reference_path):
            sys.exit(f"Error: Directory with {dir_kind} does not exist:\n"
                     f" {reference_path}\n"
                     f"{help_tip()}")

        if is_empty(reference_path):
            sys.exit(f"Error: There is no images in Directory with {dir_kind}:\n"
                     f" {reference_path}\n"
                     f"{help_tip()}")
    else:
        raise ValueError(f"Error: wrong path kind {dir_kind}:\n"
                         f" {reference_path}")


def check_if_argv_is_correct(argv_):
    """main function of module: check_if_argv_is_correct.py, used in: reference_judge.py"""

    program_name = argv_[0]

    # incorrect number of arguments
    if not (len(argv_) == 2 or (len(argv_) >= 4 and len(argv_) <= 7)):
        sys.exit(f"{help_content()}\n"
                 f"{help_tip()}")

    # invalid usage
    elif len(argv_) == 2 and not argv_[1] == "--help":
        sys.exit(f"Error: invalid 1st argument. Usage: python {program_name} --help:\n"
                 f" {argv_[1]}")

    # correct number of arguments
    elif len(argv_) >= 4 and len(argv_) <= 7:

        check_paths(argv_)

        check_mode(argv_)
