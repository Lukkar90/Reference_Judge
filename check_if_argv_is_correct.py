# python lib
import os

#internal lib
from app_data import legit_extensions
from utlis import uri_validator, get_rid_end_slashes



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


def directories_validation(original_reference_directory_path, app_reference_directory_path):

    if app_reference_directory_path == original_reference_directory_path:
        exit('Error: "original references" and "app references" directories are the same')

    if not os.path.exists(original_reference_directory_path):
        exit("Error: Directory with original references does not exist")

    if is_empty(original_reference_directory_path):
        exit("Error: There is no images in Directory with original references")

    if not os.path.exists(app_reference_directory_path):
        exit("Error: Directory with app references does not exist")

    if is_empty(app_reference_directory_path):
        exit("Error: There is no images in Directory with app references")

    if count_legit_images(app_reference_directory_path) < count_legit_images(original_reference_directory_path):
        exit('Error: There are more images in "original references" dir than in "app references" dir')


def check_if_argv_is_correct(argv):

    program_name = argv[0]
    
    # incorrect number of arguments
    if not (len(argv) == 2 or (len(argv) >= 4 and len(argv) <= 6)):
        exit(f"Usage: python {program_name} <orignal_reference_path> <app_reference_path> <--mode> [directory_diffrences_output] [width]\n"  # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
            "For more information:\n"
            f"python {program_name} --help")

    elif len(argv) == 2:
        exit(f"Error: invalid 1st argument. Avaible usage: python {program_name} --help")
        
    # correct number of arguments
    elif len(argv) >= 4 and len(argv) <= 6:

        original_reference_path = argv[1]
        app_reference_path = argv[2]

        # check if mode is correct
        if not (argv[3] == "--save" or argv[3] == "--show"):
            exit('Error: 3th argument is invalid. It\'s not mode: "--show" or "--save"')
        mode = argv[3]

        # check modes arguments
        if mode == "--save":
            if len(argv) < 5:
                exit("Error: No output path")

            elif len(argv) == 6 and not argv[5].isnumeric():
                exit("Error: 5th, last argument should be numeric")

        elif mode == "--show":
            if len(argv) == 5 and not argv[4].isnumeric():
                exit("Error: 4th, last argument should be numeric")

            elif len(argv) == 6:
                exit("Error: one argument too much")
        else:
            exit("Error: Invalid mode argument")

        # Checking paths arguments
        ext_original = os.path.splitext(original_reference_path)[1]
        # original ref arg is a file
        if ext_original:

            ext_app = os.path.splitext(app_reference_path)[1]
            if ext_app and original_reference_path == app_reference_path:
                # Checking if paths/url are not the same
                exit("Error: Both files have the same path")

        # if orginal images are dir
        else:

            # Checking if many files will be compared to one
            if os.path.isdir(original_reference_path) and (os.path.isfile(app_reference_path) or uri_validator(app_reference_path)):
                exit("Error: Original reference path can't be directory, if app reference is only one file")

            directories_validation(original_reference_path, app_reference_path)