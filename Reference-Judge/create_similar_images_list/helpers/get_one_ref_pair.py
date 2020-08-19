"""
get_one_pair_of_similar images by comparing another one or iterating among many in selected dir
"""


# python libs
import os
import sys

# external libs
from cv2 import COLOR_BGR2GRAY, cvtColor, imread
from skimage.metrics import structural_similarity as compare_images

# internal libs
from create_similar_images_list.helpers.utils import (
    find_most_similar_image,
    no_similar_images,
    ReferencePair
)
from utils import (
    error_check_path_is_empty_string,
    MakeSizesOfImagesTheSame,
    uri_validator,
    url_to_image
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
            original_reference_path,
            app_reference_path,
            original_name,
            by_ratio
        )

    # if only original image is single file
    else:
        reference_pair = find_similar_one_original_image_among_references(
            original_reference_path,
            original_name,
            app_reference_path,
            by_ratio
        )

    # It can't be before "return", because if you have only one element in index
    # it wouldn't be iterable
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
        if MakeSizesOfImagesTheSame(source, target).check_if_scale_not_too_big():
            target = MakeSizesOfImagesTheSame(
                source,
                target
            ).give_resized_image(target)
        else:
            MakeSizesOfImagesTheSame(
                source, target).notify_user_about_wrong_scale()  # For UX, user has to be informed

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


def find_similar_one_original_image_among_references(
    original_reference_path,
    original_name,
    app_reference_path,
    by_ratio
):
    """return no pair or only one"""

    similar_image = find_most_similar_image(
        original_reference_path, app_reference_path, by_ratio)

    if no_similar_images(similar_image):
        print(f"Not found reference : {original_name}")
        reference_pair = None
    else:
        reference_pair = ReferencePair(
            original_name,
            original_reference_path,
            similar_image["file_path"],
            similar_image["similarity"]).dictionary

    return reference_pair
