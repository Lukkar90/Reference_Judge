# python libs
import os
import sys

# external libs
from cv2 import imread

# internal libs
from config import LEGIT_EXTENSIONS
from utils import error_check_path_is_empty_string

# same module
from create_similar_images_list.helpers.utils import reference_pair_dictionary, find_most_similar_image


def get_similar_images_list(source_directory_path, target_directory_path, by_ratio):
    """return list of paths of matched images"""

    error_check_path_is_empty_string(source_directory_path)
    error_check_path_is_empty_string(target_directory_path)

    # Init variables
    sources_paths = files_paths(source_directory_path)
    reference_pairs = list()

    # add all similar images pairs to list
    for source_path in sources_paths:

        source_name = os.path.basename(source_path)

        similar_image = find_most_similar_image(
            source_path, target_directory_path, by_ratio)

        if similar_image["file_path"] == "":
            print(f"Not found reference : {source_name}")
            reference_pair = None
        else:
            reference_pair = reference_pair_dictionary(
                source_name, source_path, similar_image["file_path"], similar_image["similarity"])
            # Notice User with searching progress
            print(
                f"Found reference : {source_name}, similarity: {similar_image['similarity']}")
            reference_pairs.append(reference_pair)

    return reference_pairs


def files_paths(directory):
    """returning legit list paths of files in chosen directory"""

    error_check_path_is_empty_string(directory)

    # Init variables
    paths = list()

    # add all images paths to list
    # check all instances in this directory, but not sub-directories
    for file_ in os.listdir(directory):

        full_path = os.path.join(directory, file_)

        # (tuple(LEGIT_EXTENSIONS) to use multiply arguments
        if os.path.isfile(full_path) and file_.endswith(tuple(LEGIT_EXTENSIONS)):
            paths.append(full_path)

    return paths
