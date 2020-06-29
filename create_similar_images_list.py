# python libs
import os
from sys import exit

# external libs
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as compare_images
from cv2 import imread, cvtColor, COLOR_BGR2GRAY

# internal libs
from app_data import legit_extensions
from utlis import url_to_image, uri_validator


def files_paths(directory):

    # Init variables
    paths = list()

    # add all images paths to list
    for file_ in os.listdir(directory):  # check all instances in this directory, but not sub-directories

        full_path = os.path.join(directory, file_)

        if os.path.isfile(full_path) and file_.endswith(tuple(legit_extensions)):  # file_.endswith(tuple(legit_extensions) -> https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
            paths.append(full_path)

    return paths


def count_legit_images(directory_path):

    # count all legit images
    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name)) and name.endswith(tuple(legit_extensions))])


def is_empty(directory_path):

    # Init variables
    there_are_files = False

    # check if there is any legit image in directory
    for file_name in os.listdir(directory_path):

        full_path = os.path.join(directory_path, file_name)

        if os.path.isfile(full_path) and file_name.endswith(tuple(legit_extensions)):
            there_are_files = True
            break

    return not there_are_files


def is_file_validation(file_path):

    if not os.path.isfile(file_path):
        exit(f"Error: This file is does not exists: {file_path}")
    return


def path_to_image(path, reference_name_kind):

    if uri_validator(path):
        # original as url
        image = url_to_image(path)

    else:
        # original as file
        is_file_validation(path)
        image = imread(path)

    return image


class Reference_pair:
    def __init__(self, original_name, original_path, app_path, similarity):
        self.dictonary = {
            "original_reference_name": original_name,
            "original_reference_path": original_path,
            "app_reference_path": app_path,
            "similarity": similarity
        }


def find_most_similar_image(source_path, target_directory_path):  # https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

    # Init variables
    if uri_validator(source_path):
        source_image = url_to_image(source_path)  # load image into memory
    else:
        source_image = imread(source_path)  # load image into memory
    source_image = cvtColor(source_image, COLOR_BGR2GRAY)

    s_height, s_width = source_image.shape

    most_similar_image = {"file_path": "", "similarity": 0}
    source_extension = os.path.splitext(source_path)

    # Check each file in choosed folder to find this most similar
    for file_ in os.listdir(target_directory_path):

        # Source extension and file extension should be "png"
        if file_.endswith(source_extension):

            target_path = os.path.join(target_directory_path, file_)
            target_image = imread(target_path)  # load image into memory
            t_height, t_width, _ = target_image.shape

            # NOTE: the two images must have the same dimension
            if s_height == t_height and s_width == t_width:

                target_image = cvtColor(target_image, COLOR_BGR2GRAY)  # You have to change target image to gray to calculate similarity
                similitarity = compare_images(source_image, target_image)  # compute the structural similarity SSMI

                # filtering most similar image
                if most_similar_image["similarity"] < similitarity:
                    most_similar_image["similarity"] = similitarity
                    most_similar_image["file_path"] = target_path

    return most_similar_image


def both_single_paths(original_reference, app_reference, original_name):

    source = path_to_image(original_reference, "Original reference")
    target = path_to_image(app_reference, "App reference")

    # change image to b&w to calculate similarity
    source = cvtColor(source, COLOR_BGR2GRAY)
    target = cvtColor(target, COLOR_BGR2GRAY)

    # compute the structural similarity SSMI
    similitarity = compare_images(source, target)

    reference_pair = Reference_pair(original_name, original_reference, app_reference, similitarity).dictonary
    return reference_pair


def similar_images_list_generator(source_directory_path, target_directory_path):

    # Init variables
    sources_paths = files_paths(source_directory_path)
    reference_pairs = list()

    # add all similar images pairs to list
    for source_path in sources_paths:

        source_name = os.path.basename(source_path)

        similar_image = find_most_similar_image(source_path, target_directory_path)

        reference_pair = Reference_pair(source_name, source_path, similar_image["file_path"], similar_image["similarity"]).dictonary

        print(f"Found reference : {source_name}, similarity: {similar_image['similarity']}")  # Notice User with searching progress
        reference_pairs.append(reference_pair)

    return reference_pairs


def directories_validation(original_reference_directory_path, app_reference_directory_path):

    if app_reference_directory_path == original_reference_directory_path:
        exit('Error: "original references" and "app references" directories are the same')

    if not os.path.exists(original_reference_directory_path):
        exit("Error: Directory with original references does not exist")

    if is_empty(original_reference_directory_path):
        exit("Error: There is no images in Directory with original references")

    if not os.path.exists(app_reference_directory_path):
        exit("Error: Directory with app references does not exist")

    if is_empty(app_reference_directory_path):
        exit("Error: There is no images in Directory with app references")

    if count_legit_images(app_reference_directory_path) < count_legit_images(original_reference_directory_path):
        exit('Error: There are more images in "original references" dir than in "app references" dir')


def return_one_ref_pair(original_reference_path, app_reference_path):

    similar_list = list()

    original_name = os.path.basename(original_reference_path)

    ext_app = os.path.splitext(app_reference_path)[1]
    # if app image and orginal image are single file
    if ext_app:

        reference_pair = both_single_paths(original_reference_path, app_reference_path, original_name)

    # if orginal image is single file
    else:

        # Give results when it's only one original image and match reference image from many app references
        similar_image = find_most_similar_image(original_reference_path, app_reference_path)

        reference_pair = Reference_pair(original_name, original_reference_path, similar_image["file_path"], similar_image["similarity"]).dictonary


    similar_list.append(reference_pair)  # It can't be before "return", becouse if you have only one element in index, it wouldn't be iterable 
    return similar_list

def create_similar_images_list(original_reference_path, app_reference_path):

    # Checking if paths/url are not the same
    if original_reference_path == app_reference_path:
        exit("Error: Both files have the same path")

    # Checking if many files will be compared to one
    if os.path.isdir(original_reference_path) and os.path.isfile(app_reference_path):
        exit("Error: Original reference path can't be directory, if app reference is only one file")

    ext_original = os.path.splitext(original_reference_path)[1]
    # if orginal image is file, not dir
    if ext_original:

        return return_one_ref_pair(original_reference_path, app_reference_path)
    # if original images are dir
    else:

        directories_validation(original_reference_path, app_reference_path)

        return similar_images_list_generator(original_reference_path, app_reference_path)