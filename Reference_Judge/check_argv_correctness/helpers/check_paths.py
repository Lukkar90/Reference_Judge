# python libs
import os
import sys
from urllib import error, request

# internal libs
from config import LEGIT_EXTENSIONS, ARGV
from help import help_tip
from utils import dir_exists, uri_validator, error_check_path_is_empty_string


def check_paths(argv_):
    """Check if files/dir/url paths program arguments are correct"""

    # Path args
    original_reference_path = argv_[1]
    app_reference_path = argv_[2]
    output_path = None
    # this argument position can be also width
    if len(argv_) >= 5 and not argv_[4].isnumeric() and argv_[4] not in ARGV["search by ratio"]:
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


def is_empty(directory_path):
    """Check if there are images with LEGIT_EXTENSIONS"""

    # Init variables
    there_are_files = False

    # check if there is any legit image in directory
    for file_name in os.listdir(directory_path):

        full_path = os.path.join(directory_path, file_name)

        if os.path.isfile(full_path) and file_name.endswith(tuple(LEGIT_EXTENSIONS)):
            there_are_files = True
            break

    return not there_are_files


def count_legit_images(directory_path):
    """Count all images with LEGIT_EXTENSIONS"""

    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name)) and name.endswith(tuple(LEGIT_EXTENSIONS))])
