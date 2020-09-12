"""return true if success, else false"""


# Python
from os import path

# Internal libs
from Reference_Judge.utils import uri_validator
from Reference_Judge.create_similar_images_list.helpers.get_similar_images_list import files_paths
from UI.widgets import ScrolledTextBox


def window_displaying_not_found_images(source_ref_path, similar_list):
    """It creates box with listed all path files which does not have match"""

    if is_single_file(source_ref_path):

        source_path = source_ref_path

        source_path_match = list_all_source_matched(similar_list)

        if len(source_path_match) != 1:
            ScrolledTextBox("List of not found matches",
                            source_path)
            return True

    else:

        source_paths = files_paths(source_ref_path)

        if source_paths:

            source_paths_matches = list_all_source_matched(similar_list)

            source_paths_no_matches = list_not_matched_source(
                source_paths, source_paths_matches)

            if source_paths_no_matches:
                ScrolledTextBox("List of not found matches",
                                source_paths_no_matches)
                return True

    return False


def is_single_file(source_ref_path):
    """return bool"""

    return path.isfile(source_ref_path) or uri_validator(source_ref_path)


def list_not_matched_source(source_paths, source_paths_matches):
    """return set"""

    return set(source_paths).symmetric_difference(set(source_paths_matches))


def list_all_source_matched(similar_list):
    """return a list"""

    source_paths_matches = []

    for item in similar_list:
        source_paths_matches.append(item["source reference path"])
    return source_paths_matches
