"""common functions for helpers"""


# python libs
import os

# external libs
from cv2 import COLOR_BGR2GRAY, cvtColor, imread
from skimage.metrics import structural_similarity as compare_images

# internal libs
from Reference_Judge.config import SIMILARITY
from Reference_Judge.utils import (
    give_resized_image,
    error_check_path_is_empty_string,
    SizesSimilarityImages,
    uri_validator, url_to_image
)


# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
def find_most_similar_image(file_source_path, target_directory_path, by_ratio=False):
    """Return matched images paths of chosen file and dir"""

    error_check_path_is_empty_string(target_directory_path)

    # Init variables
    if uri_validator(file_source_path):
        source_image = url_to_image(file_source_path)
    else:
        source_image = imread(file_source_path)

    source_image = cvtColor(source_image, COLOR_BGR2GRAY)

    s_height, s_width = source_image.shape

    most_similar_image = {"file path": "", "similarity": 0}
    source_extension = os.path.splitext(file_source_path)

    # Check each file in chosen folder to find this most similar
    for file_ in os.listdir(target_directory_path):

        # Source extension and file extension should be "png"
        if file_.endswith(source_extension):

            target_path = os.path.join(target_directory_path, file_)
            target_image = imread(target_path)

            # when you want to search any image with the same ratio and similar scale
            if by_ratio:

                if SizesSimilarityImages(source_image, target_image).resizable_images:
                    target_image = give_resized_image(
                        source_image, target_image)

            t_height, t_width, _ = target_image.shape

            # NOTE: the two images must have the same dimension
            if s_height == t_height and s_width == t_width:

                # You have to change target image to gray to calculate similarity
                target_image = cvtColor(target_image, COLOR_BGR2GRAY)

                # compute the structural similarity SSMI
                similarity = compare_images(source_image, target_image)

                # filtering most similar image
                if most_similar_image["similarity"] < similarity > SIMILARITY["not enough"]:
                    most_similar_image["similarity"] = similarity
                    most_similar_image["file path"] = target_path

                # For performance, it's high propability that with this value is the same image
                if most_similar_image["similarity"] >= SIMILARITY["enough"]:
                    break

    return most_similar_image


class ReferencePair():
    """Returned pair of matched images and its attributes"""

    def __init__(self, source_name, source_path, target_path, similarity):
        self.dictionary = {
            "source_reference_name": source_name,
            "source_reference_path": source_path,
            "target_reference_path": target_path,
            "similarity": similarity
        }


def no_similar_images(similar_image):
    """return bool"""
    return similar_image["file path"] == ""
