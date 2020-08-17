# python libs
import os
import sys

# external libs
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from skimage.metrics import structural_similarity as compare_images

# internal libs
from utils import (
    error_check_path_is_empty_string,
    uri_validator,
    MakeSizesOfImagesTheSame,
    url_to_image
)
from create_similar_images_list.helpers.utils import (
    find_most_similar_image,
    ReferencePair
)


def get_one_ref_pair(original_reference_path, app_reference_path, by_ratio):
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
            reference_pair = ReferencePair(
                original_name, original_reference_path, similar_image["file_path"], similar_image["similarity"]).dictionary

    # It can't be before "return", because if you have only one element in index, it wouldn't be iterable
    similar_list.append(reference_pair)
    return similar_list


def both_single_paths(original_reference, app_reference, original_name, by_ratio=False):
    """logic when both source and target paths are files"""

    error_check_path_is_empty_string(original_reference)
    error_check_path_is_empty_string(app_reference)
    error_check_path_is_empty_string(original_name)

    source = path_to_image(original_reference)
    target = path_to_image(app_reference)

    # resize image target image to the same size if ratio is the same
    if by_ratio:
        target = MakeSizesOfImagesTheSame(source, target).target

    # change image to b&w to calculate similarity
    source = cvtColor(source, COLOR_BGR2GRAY)
    target = cvtColor(target, COLOR_BGR2GRAY)

    # compute the structural similarity SSMI
    try:
        similarity = compare_images(source, target)
    except ValueError as alert:
        sys.exit(alert)  # returning circa "images not he same size"

    reference_pair = ReferencePair(
        original_name, original_reference, app_reference, similarity).dictionary
    return reference_pair


def path_to_image(path):
    """returning raw image"""

    if uri_validator(path):
        # original as url
        image = url_to_image(path)

    else:
        # original as file
        image = imread(path)

    return image