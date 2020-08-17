"""
This module is responsible for creating list of matched images between chosen paths
Chosen paths could be single image, dir or url path
"""


# python libs
import os

# internal libs
from utils import error_check_path_is_empty_string

# same module
from create_similar_images_list.helpers.get_one_ref_pair import get_one_ref_pair
from create_similar_images_list.helpers.get_similar_images_list import get_similar_images_list


def create_similar_images_list(original_reference_path, app_reference_path, by_ratio=False):
    """
    It returns path or paths of similar images compared to image reference with additional attributes
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
