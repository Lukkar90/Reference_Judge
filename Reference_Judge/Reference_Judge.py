"""
NAME

    Reference-Judge

DESCRIPTION

    Showing visual differences between images
    ========================================

    Reference-Judge is used for developers to show visual differences
    between mobile app particular screen and reference created by mobile app designer.

    It's aims to improve workflow for programmer and also designer.

    For programmer this tool availables instant check of screen,
    if it is done according to references.

    For designer this tool relieve him/she from task of constant checking,
    if particular screen was done according to the reference.

    This program uses image recognition algorithms from https://opencv.org/
"""

# internal libs
from Reference_Judge.check_argv_correctness.check_argv_correctness import check_argv_correctness
from Reference_Judge.check_argv_correctness.helpers.check_paths import count_legit_images
from Reference_Judge.config import ARGV, IMAGES_SIZES
from Reference_Judge.create_similar_images_list.create_similar_images_list import create_similar_images_list
from Reference_Judge.help import help_detailed_usage, user_commanded_help
from Reference_Judge.modes.save import save
from Reference_Judge.modes.show import show
from Reference_Judge.utils import check_ratio_argv


def Reference_Judge(_argv):
    """Parsing sys.argv to invoke in chosen paths modes: save or show, or to get help"""

    check_argv_correctness(_argv)
    if user_commanded_help(_argv):
        return help_detailed_usage()

    # Init variables
    original_ref_path = _argv[1]
    app_ref_path = _argv[2]
    mode = _argv[3]
    messages_summary = []

    by_ratio = check_ratio_argv(_argv)

    similar_list = create_similar_images_list(
        original_ref_path, app_ref_path, by_ratio)

    references_counter = count_found_and_not_found_refs(
        original_ref_path, similar_list)
    messages_summary.append(references_counter)

    width = IMAGES_SIZES["default width"]  # Default value for mobiles apps

    if mode in ARGV["save"]:

        saving_counter = save(width, similar_list, by_ratio, _argv)
        messages_summary.append(saving_counter)

    elif mode in ARGV["show"]:

        show(width, similar_list, by_ratio, _argv)

    else:
        raise ValueError("Error: Invalid mode value\n"
                         f" {mode}")

    # Value used in UI message box
    return stringify_lists(messages_summary)


def count_found_and_not_found_refs(original_ref_path, similar_list):
    """return tuple of two integers"""

    references_counter = {
        "found matches": 0,
        "not found matches": 0
    }

    original_images_number = count_legit_images(original_ref_path)
    references_counter["found matches"] = len(similar_list)
    references_counter["not found matches"] = original_images_number - \
        references_counter["found matches"]

    return references_counter


def concat_stringified_values_and_keys(_list):
    """return list"""

    strings_list = []

    for k, v in _list.items():
        strings_list.append(f"{k}: {str(v)}")

    return strings_list


def stringify_lists(messages_summary):
    """return concated all dicts elements into one string"""

    messages_list = []
    for message in messages_summary:
        stringify = concat_stringified_values_and_keys(message)
        messages_list += stringify

    messages_string = ""
    for message in messages_list:
        messages_string += f"{message}\n"

    return messages_string
