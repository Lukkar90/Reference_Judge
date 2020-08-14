"""
This module is responsible for creating list of matched images between chosen paths
Chosen paths could be single image, dir or url path
"""
# python libs
import os
import sys

# external libs
from cv2 import COLOR_BGR2GRAY, cvtColor, imread
from skimage.metrics import structural_similarity as compare_images

# internal libs
from config import LEGIT_EXTENSIONS
from utils import (
    uri_validator, url_to_image, error_check_path_is_empty_string,
    make_sizes_of_images_the_same
)

# same module
from create_similar_images_list.helpers.get_one_ref_pair import get_one_ref_pair, find_most_similar_image
from create_similar_images_list.helpers.utils import reference_pair_dictionary


def create_similar_images_list(original_reference_path, app_reference_path, by_ratio=False):
    """
    Main function of this module used in main in reference_judge.py
    It returns path or paths of similar images compared to reference
    """

    error_check_path_is_empty_string(original_reference_path)
    error_check_path_is_empty_string(app_reference_path)

    ext_original = os.path.splitext(original_reference_path)[1]
    # if original image is file, not dir
    if ext_original:

        return get_one_ref_pair(original_reference_path, app_reference_path, by_ratio)
    # if original images are dir
    else:

        return get_similar_images_list(original_reference_path, app_reference_path, by_ratio)


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
