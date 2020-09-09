"""
get_one_pair_of_similar images by comparing another one or iterating among many in selected dir
"""


# python libs
import os
import sys

# external libs
from cv2 import COLOR_BGR2GRAY, cvtColor, imread
from Reference_Judge.config.logger import Logger, write_in_log
from skimage.metrics import structural_similarity as compare_images

# internal libs
from Reference_Judge.create_similar_images_list.helpers.utils import (
    find_most_similar_image,
    no_similar_images,
    ReferencePair
)
from Reference_Judge.utils import (
    give_resized_image,
    error_check_path_is_empty_string,
    SizesSimilarityImages,
    uri_validator,
    url_to_image
)


def get_one_ref_pair(source_reference_path, target_reference_path, by_ratio, script_run_date, output_path):
    """return on pair of paths of matched images"""

    error_check_path_is_empty_string(source_reference_path)
    error_check_path_is_empty_string(target_reference_path)

    similar_list = list()

    source_name = os.path.basename(source_reference_path)

    # if target image and source image are single files
    ext_target = os.path.splitext(target_reference_path)[1]
    if ext_target:

        reference_pair = both_single_paths(
            source_reference_path,
            target_reference_path,
            source_name,
            by_ratio
        )

    # if only source image is single file
    else:
        reference_pair = find_similar_one_source_image_among_targets(
            source_reference_path,
            source_name,
            target_reference_path,
            by_ratio,
            script_run_date,
            output_path
        )

    # It can't be before "return", because if you have only one element in index
    # it wouldn't be iterable
    similar_list.append(reference_pair)

    return similar_list


def both_single_paths(source_reference, target_reference, source_name, by_ratio=False):
    """logic when both source and target paths are files"""

    error_check_path_is_empty_string(source_reference)
    error_check_path_is_empty_string(target_reference)
    error_check_path_is_empty_string(source_name)

    source = path_to_image(source_reference)
    target = path_to_image(target_reference)

    # resize image target image to the same size if ratio is the same
    if by_ratio:

        if SizesSimilarityImages(source, target).resizable_images:
            target = give_resized_image(source, target)

        else:

            SizesSimilarityImages(
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
        source_name, source_reference, target_reference, similarity).dictionary
    return reference_pair


def path_to_image(path):
    """returning raw image"""

    if uri_validator(path):
        # source as url
        image = url_to_image(path)

    else:
        # source as file
        image = imread(path)

    return image


def find_similar_one_source_image_among_targets(
    source_reference_path,
    source_name,
    target_reference_path,
    by_ratio,
    script_run_date,
    output_path
):
    """return no pair or only one"""

    similar_image = find_most_similar_image(
        source_reference_path, target_reference_path, by_ratio)

    if no_similar_images(similar_image):
        print(f"Not found reference:\n  {source_name}")
        if output_path:
            save_log = Logger().load_saving_bool()
            if save_log:
                write_in_log(
                    "[NOT FOUND]",
                    os.path.join(output_path, similar_image["source name"]),
                    script_run_date
                )
                reference_pair = None
    else:
        reference_pair = ReferencePair(
            source_name,
            source_reference_path,
            similar_image["target path"],
            similar_image["similarity"]).dictionary

    return reference_pair
