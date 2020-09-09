"""
This module is responsible for creating list of matched images between chosen paths
Chosen paths could be single image, dir or url path
"""


# python libs
import os

# internal libs
from Reference_Judge.utils import error_check_path_is_empty_string

# same module
from Reference_Judge.create_similar_images_list.helpers.get_similar_images_list import get_similar_images_list
from Reference_Judge.create_similar_images_list.helpers.get_one_ref_pair import get_one_ref_pair


def create_similar_images_list(source_reference_path, target_reference_path, script_run_date, output_path, by_ratio=False):
    """
    It returns path or paths of similar images compared to image reference with additional attributes
    """

    error_check_path_is_empty_string(source_reference_path)
    error_check_path_is_empty_string(target_reference_path)

    ext_source = os.path.splitext(source_reference_path)[1]
    # if source image is file
    if ext_source:

        return get_one_ref_pair(source_reference_path, target_reference_path, by_ratio, script_run_date, output_path)

    # if source images are dir
    else:

        return get_similar_images_list(source_reference_path, target_reference_path, by_ratio, script_run_date, output_path)
