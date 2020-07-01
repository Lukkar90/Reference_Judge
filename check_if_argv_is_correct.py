# python lib
import os
from sys import exit, argv
import __main__

# external libs
from urllib import error, request

#internal libs
from app_data import legit_extensions
from utlis import dir_exists, dir_from_path, uri_validator, Error_check_variable_is_empty_string


def url_exists(url):

    try:
        request.urlopen(url)
    except error.HTTPError as e:
        exit(f"Error: path http: {e}:\n"
            f" {url}")
    except error.URLError as e:
        exit(f"Error: path url: {e}:\n"
            f" {url}")

    return True

def count_legit_images(directory_path):

    # count all legit images
    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name)) and name.endswith(tuple(legit_extensions))])


def is_empty(directory_path):

    # Init variables
    there_are_files = False

    # check if there is any legit image in directory
    for file_name in os.listdir(directory_path):

        full_path = os.path.join(directory_path, file_name)

        if os.path.isfile(full_path) and file_name.endswith(tuple(legit_extensions)):
            there_are_files = True
            break

    return not there_are_files


class Help_tip:
    """String to use when user write wrong input, showing him how to invoke help function"""

    def __init__(self):
        program_name = __main__.__file__  # https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
        self.string = f"For more information:\n Usage: python {program_name} --help"


class Help_content:
    """Explaining user general usage of program"""

    def __init__(self):
        program_name = __main__.__file__  # https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
        self.string = f"Usage: python {program_name} <orignal_reference_path> <app_reference_path> <--mode> [directory_diffrences_output] [width]"


def check_if_argv_is_correct(argv):

    program_name = argv[0]
    
    # incorrect number of arguments
    if not (len(argv) == 2 or (len(argv) >= 4 and len(argv) <= 6)):
        exit(f"{Help_content().string}\n"  # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
            f"{Help_tip().string}")

    # arg for def program_help(argv) in reference-judge.py
    elif len(argv) == 2 and not argv[1] == "--help":
        exit(f"Error: invalid 1st argument. Usage: python {program_name} --help:\n"
            f" {argv[1]}")
        
    # correct number of arguments
    elif len(argv) >= 4 and len(argv) <= 6:

        check_paths(argv)

        check_mode(argv)


def check_mode(argv):

    if not (argv[3] == "--save" or argv[3] == "--show"):
        exit('Error: 3th argument is invalid. It\'s not mode: "--show" or "--save":\n'
            f" {argv[3]}\n"
            f"{Help_tip().string}")
    mode = argv[3]

    # check modes arguments
    if mode == "--save":
        if len(argv) < 5:
            exit("Error: No output path\n"
                f"{Help_tip().string}")

        elif len(argv) == 6 and not argv[5].isnumeric():
            exit("Error: 5th, last argument should be numeric:\n"
                f" {argv[5]}\n"
                f"{Help_tip().string}")

    elif mode == "--show":
        if len(argv) == 5 and not argv[4].isnumeric():
            exit("Error: 4th, last argument should be numeric:\n"
                f" {argv[4]}\n"
                f"{Help_tip().string}")

        elif len(argv) == 6:
            exit("Error: one argument too much:\n"
                f" {argv[5]}\n"
                f"{Help_tip().string}")
    else:
        raise ValueError(f"Error: wrong mode kind:\n" 
                        f"{mode}")

    return mode


def check_paths(argv):

    # Path args
    original_reference_path = argv[1]
    app_reference_path = argv[2]
    output_path = None
    if len(argv) >= 5 and not argv[4].isnumeric():  # this argument position can be also width
        output_path = argv[4]

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
            exit("Error: output can't be url:\n"
                f" {output_path}\n"
                f"{Help_tip().string}")
        
    # Paths validation depending on kind
    path_validation(original_ref_is, original_reference_path, "original references")
    path_validation(app_ref_is, app_reference_path, "app references")

    if output_is and not dir_exists(output_path):
        exit(f"Error: Output directory does not exists:\n"
            f" {output_path}\n"
            f"{Help_tip().string}")


    # If original path and app path are dirs
    if original_ref_is == "dir" and app_ref_is == "dir":

        if original_reference_path == app_reference_path:
            exit('Error: "original references" and "app references" directories are the same:\n'
                f" {original_reference_path}\n"
                f"{Help_tip().string}")

        if count_legit_images(original_reference_path) > count_legit_images(app_reference_path):
            exit('Error: There are more images in "original references" dir than in "app references" dir:\n'
                f" {original_reference_path}\n"
                f" {app_reference_path}\n"
                f"{Help_tip().string}")


    # If original path and app path are files
    if (original_ref_is == "file" and app_ref_is == "file") or (original_ref_is == "url" and app_ref_is == "url"):

        if original_reference_path == app_reference_path:
            # Checking if paths/url are not the same
            exit("Error: Both files have the same path:\n"
                f" {original_reference_path}\n"
                f"{Help_tip().string}")

    # If original path is dir and app path is file
    if original_ref_is == "dir" and (app_ref_is == "file" or app_ref_is == "url"):
        exit("Error: Original reference path can't be directory, if app reference is only one file:\n"
            f" {original_reference_path}\n"
            f" {app_reference_path}\n"
            f"{Help_tip().string}")


def check_path_kind(original_reference_path):
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

    Error_check_variable_is_empty_string(dir_kind)

    if path_kind == "url":
        
        url_exists(reference_path)  # exit prompt is inside function

    elif path_kind == "file":

        if not os.path.isfile(reference_path):
            exit(f"Error: File does not exists:\n"
                f" {reference_path}\n"
                f"{Help_tip().string}")

    elif path_kind == "dir":

        if not os.path.exists(reference_path):
            exit(f"Error: Directory with {dir_kind} does not exist:\n"
                f" {reference_path}\n"
                f"{Help_tip().string}")

        if is_empty(reference_path):
            exit(f"Error: There is no images in Directory with {dir_kind}:\n"
                f" {reference_path}\n"
                f"{Help_tip().string}")
    else:
        raise ValueError(f"Error: wrong path kind {dir_kind}:\n"
                        f" {reference_path}")