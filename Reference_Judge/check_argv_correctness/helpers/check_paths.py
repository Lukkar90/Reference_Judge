"""validate all paths"""

# python libs
import os
import sys
from urllib import error, request

# internal libs
from Reference_Judge.config import LEGAL_EXTENSIONS, ARGV
from Reference_Judge.help import help_tip
from Reference_Judge.utils import dir_exists, error_check_path_is_empty_string, uri_validator

# same lib
from Reference_Judge.check_argv_correctness.helpers.errors import (
    ERRORS_MESSAGES,
    get_error_directory_does_not_exists,
    get_error_no_images_in_dir,
    get_error_wrong_web_path
)


def check_paths(_argv):
    """Check if files/dir/url paths program arguments are correct"""

    source_reference_path = _argv[1]
    app_reference_path = _argv[2]

    output_path, output_kind_legal = get_output_path_if_exists_and_legal(_argv)

    source_ref_kind = get_path_kind(source_reference_path)
    app_ref_kind = get_path_kind(app_reference_path)

    check_if_many_paths_exists(
        source_reference_path,
        app_reference_path,
        output_path,
        source_ref_kind,
        app_ref_kind,
        output_kind_legal,
        _argv
    )

    check_paths_legal_combinations(
        source_ref_kind,
        app_ref_kind,
        source_reference_path,
        app_reference_path,
        output_path
    )


def get_output_path_if_exists_and_legal(argv_):
    """if output_path exists return output_path and his output_kind_legal"""

    output_path = None
    output_kind_legal = None

    if len(argv_) >= 5 and is_output_path_argv(argv_):
        output_path = argv_[4]

    if output_path:
        output_kind_legal = get_path_kind(output_path)
        if output_kind_legal == "url":
            sys.exit(f'{ERRORS_MESSAGES["cant be url"]}\n'
                     f" {output_path}\n"
                     f"{help_tip()}")

    return output_path, output_kind_legal


def check_output_path_exists(output_path, output_kind_legal):
    """if wrong, it exits program"""

    if output_kind_legal and not dir_exists(output_path):
        sys.exit(f"{ERRORS_MESSAGES['output does not exists']}\n"
                 f" {output_path}\n"
                 f"{help_tip()}")


def check_if_many_paths_exists(
    source_reference_path,
    app_reference_path,
    output_path,
    source_ref_kind,
    app_ref_kind,
    output_kind_legal,
    _argv
):
    """if wrong, it exits program"""

    path_exists(
        source_ref_kind,
        source_reference_path,
        "source references"
    )

    path_exists(
        app_ref_kind,
        app_reference_path,
        "target references"
    )

    if len(_argv) >= 4 and _argv[3] in ARGV["save"]:
        check_output_path_exists(
            output_path,
            output_kind_legal
        )


def check_paths_legal_combinations(
    source_ref_kind,
        app_ref_kind,
        source_reference_path,
        app_reference_path,
        output_path
):
    """if wrong, it exits program"""

    check_source_and_reference_if_dirs(
        source_ref_kind,
        app_ref_kind,
        source_reference_path,
        app_reference_path
    )

    check_source_and_reference_if_files(
        source_ref_kind,
        app_ref_kind,
        source_reference_path,
        app_reference_path
    )

    check_if_source_dir_and_reference_file_or_url(
        source_ref_kind,
        app_ref_kind,
        source_reference_path,
        app_reference_path
    )

    # check if source ref and app ref are the same as output
    if output_path:

        check_if_app_or_source_paths_are_same_as_output(
            output_path,
            source_reference_path,
            app_reference_path
        )


def check_source_and_reference_if_dirs(
    source_ref_kind,
    app_ref_kind,
    source_reference_path,
    app_reference_path
):
    """if wrong, it exits program"""

    if source_ref_kind == "dir" and app_ref_kind == "dir":

        if source_reference_path == app_reference_path:
            sys.exit(f'{ERRORS_MESSAGES["Original App same"]}\n'
                     f" {source_reference_path}\n"
                     f"{help_tip()}")

        if count_legal_images(source_reference_path) > count_legal_images(app_reference_path):
            sys.exit(f'{ERRORS_MESSAGES["Original > App"]}\n'
                     f" {source_reference_path}\n"
                     f" {app_reference_path}\n"
                     f"{help_tip()}")


def check_source_and_reference_if_files(
    source_ref_kind,
    app_ref_kind,
    source_reference_path,
    app_reference_path
):
    """if wrong, it exits program"""

    if (source_ref_kind == "file" and app_ref_kind == "file") or (source_ref_kind == "url" and app_ref_kind == "url"):

        if source_reference_path == app_reference_path:
            sys.exit(f"{ERRORS_MESSAGES['Original App same files']}\n"
                     f" {source_reference_path}\n"
                     f"{help_tip()}")


def check_if_source_dir_and_reference_file_or_url(
    source_ref_kind,
    app_ref_kind,
    source_reference_path,
    app_reference_path
):
    """if wrong, it exits program"""

    if source_ref_kind == "dir" and app_ref_kind in ('file', 'url'):
        sys.exit(f"{ERRORS_MESSAGES['Original dir App file']}\n"
                 f" {source_reference_path}\n"
                 f" {app_reference_path}\n"
                 f"{help_tip()}")


def check_if_app_or_source_paths_are_same_as_output(output_path, source_reference_path, app_reference_path):
    """if wrong, it exits program"""

    # make sure that output path wil be always dir to compare
    if os.path.isfile(output_path):
        output_path = os.path.dirname(output_path)

    if output_path == source_reference_path:
        sys.exit(f'{ERRORS_MESSAGES["output same as original"]}\n'
                 f" {source_reference_path}\n"
                 f"{help_tip()}")

    if output_path == app_reference_path:
        sys.exit(f'{ERRORS_MESSAGES["output same as app"]}\n'
                 f" {app_reference_path}\n"
                 f"{help_tip()}")


def is_output_path_argv(argv_):
    """return bool"""
    return not argv_[4].isnumeric() and isinstance(argv_[4], str) and argv_[4] not in ARGV["search by ratio"]


def get_path_kind(source_reference_path):
    """Check what kind of path is: url, file, dir"""

    # Checking paths arguments
    ext_path = os.path.splitext(source_reference_path)[1]

    # Check source path kind
    if ext_path:

        if uri_validator(source_reference_path):
            return "url"
        else:
            return "file"
    else:
        return "dir"


def path_exists(path_kind, reference_path, dir_kind):
    """Check if path exists: url, file, dir"""

    error_check_path_is_empty_string(dir_kind)

    if path_kind == "url":

        url_exists(reference_path)  # exit prompt is inside function

    elif path_kind == "file":

        if not os.path.isfile(reference_path):
            sys.exit(f"{ERRORS_MESSAGES['no file']}\n"
                     f" {reference_path}\n"
                     f"{help_tip()}")

    elif path_kind == "dir":

        if not os.path.exists(reference_path):
            sys.exit(f"{get_error_directory_does_not_exists(dir_kind)}\n"
                     f" {reference_path}\n"
                     f"{help_tip()}")

        if is_empty(reference_path):
            sys.exit(f"{get_error_no_images_in_dir(dir_kind)}\n"
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
        sys.exit(f"{get_error_wrong_web_path('http', alert)}\n"  # can't be  exported reasonably to general function
                 f" {url}")
    except error.URLError as alert:
        sys.exit(f"{get_error_wrong_web_path('url', alert)}\n"  # can't be  exported reasonably to general function
                 f" {url}")

    return True


def is_empty(directory_path):
    """Check if there are images with LEGAL_EXTENSIONS"""

    # Init variables
    there_are_files = False

    # check if there is any legal image in directory
    for file_name in os.listdir(directory_path):

        full_path = os.path.join(directory_path, file_name)

        if os.path.isfile(full_path) and file_name.endswith(LEGAL_EXTENSIONS):
            there_are_files = True
            break

    return not there_are_files


def count_legal_images(directory_path):
    """Count all images with LEGAL_EXTENSIONS"""

    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name)) and name.endswith(LEGAL_EXTENSIONS)])
