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
from config.config import LEGIT_EXTENSIONS
from utils.utils import (
    uri_validator, url_to_image, error_check_path_is_empty_string,
    make_sizes_of_images_the_same
)


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


def path_to_image(path):
    """returning raw image"""

    if uri_validator(path):
        # original as url
        image = url_to_image(path)

    else:
        # original as file
        image = imread(path)

    return image


def reference_pair_dictionary(original_name, original_path, app_path, similarity):
    """Returned in similar_list in main in reference_judge.py"""

    dictionary = {
        "original_reference_name": original_name,
        "original_reference_path": original_path,
        "app_reference_path": app_path,
        "similarity": similarity
    }

    return dictionary


# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
def find_most_similar_image(file_source_path, target_directory_path, by_ratio=False):
    """Return matched images paths of chosen file and dir"""

    error_check_path_is_empty_string(target_directory_path)

    # Init variables
    if uri_validator(file_source_path):
        source_image = url_to_image(file_source_path)  # load image into memory
    else:
        source_image = imread(file_source_path)  # load image into memory

    source_image = cvtColor(source_image, COLOR_BGR2GRAY)

    s_height, s_width = source_image.shape

    most_similar_image = {"file_path": "", "similarity": 0}
    source_extension = os.path.splitext(file_source_path)

    # Check each file in chosen folder to find this most similar
    for file_ in os.listdir(target_directory_path):

        # Source extension and file extension should be "png"
        if file_.endswith(source_extension):

            target_path = os.path.join(target_directory_path, file_)
            target_image = imread(target_path)  # load image into memory
            # resize image target image to the same size if ratio is the same
            if by_ratio:
                target_image = make_sizes_of_images_the_same(
                    source_image, target_image)
            t_height, t_width, _ = target_image.shape

            # NOTE: the two images must have the same dimension
            if s_height == t_height and s_width == t_width:

                # You have to change target image to gray to calculate similarity
                target_image = cvtColor(target_image, COLOR_BGR2GRAY)

                # compute the structural similarity SSMI
                similarity = compare_images(source_image, target_image)

                # filtering most similar image
                if most_similar_image["similarity"] < similarity:
                    most_similar_image["similarity"] = similarity
                    most_similar_image["file_path"] = target_path

    return most_similar_image


def both_single_paths(original_reference, app_reference, original_name, by_ratio=False):
    """logic when both source and target paths are files"""

    error_check_path_is_empty_string(original_reference)
    error_check_path_is_empty_string(app_reference)
    error_check_path_is_empty_string(original_name)

    source = path_to_image(original_reference)
    target = path_to_image(app_reference)

    # resize image target image to the same size if ratio is the same
    if by_ratio:
        target = make_sizes_of_images_the_same(source, target)

    # change image to b&w to calculate similarity
    source = cvtColor(source, COLOR_BGR2GRAY)
    target = cvtColor(target, COLOR_BGR2GRAY)

    # compute the structural similarity SSMI
    try:
        similarity = compare_images(source, target)
    except ValueError as alert:
        sys.exit(alert)  # returning circa "images not he same size"

    reference_pair = reference_pair_dictionary(
        original_name, original_reference, app_reference, similarity)
    return reference_pair


def similar_images_list_generator(source_directory_path, target_directory_path, by_ratio):
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


def return_one_ref_pair(original_reference_path, app_reference_path, by_ratio):
    """return on pair of paths of matched images"""

    error_check_path_is_empty_string(original_reference_path)
    error_check_path_is_empty_string(app_reference_path)

    similar_list = list()

    original_name = os.path.basename(original_reference_path)

    # if app image and original image are single files
    ext_app = os.path.splitext(app_reference_path)[1]
    if ext_app:

        reference_pair = both_single_paths(
            original_reference_path, app_reference_path, original_name, by_ratio)

    # if only original image is single file and
    else:

        # Give results when it's only one original image and match reference image from many app references
        similar_image = find_most_similar_image(
            original_reference_path, app_reference_path, by_ratio)

        if similar_image["file_path"] == "":
            print(f"Not found reference : {original_name}")
            reference_pair = None
        else:
            reference_pair = reference_pair_dictionary(
                original_name, original_reference_path, similar_image["file_path"], similar_image["similarity"])

    # It can't be before "return", because if you have only one element in index, it wouldn't be iterable
    similar_list.append(reference_pair)
    return similar_list


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

        return return_one_ref_pair(original_reference_path, app_reference_path, by_ratio)
    # if original images are dir
    else:

        return similar_images_list_generator(original_reference_path, app_reference_path, by_ratio)
