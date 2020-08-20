# external libs
import cv2

# internal libs
from Reference_Judge.compute_image_differences import compute_image_differences

# same module
from Reference_Judge.modes.utils import (
    check_width_argv_exists,
    check_correctness_optional_argvs,
    retrieve_argv_width, resize_all
)


def show(width, similar_list, by_ratio, _argv):
    """show matched images"""

    # Optional args
    if len(_argv) >= 5:
        check_correctness_optional_argvs(_argv, 6)
        if check_width_argv_exists(_argv, 6):
            width = retrieve_argv_width(_argv, 6, width)

    # Process all images, show user each sequence one by one
    for similar_pair in similar_list:

        if not similar_pair is None:

            images = compute_image_differences(similar_pair, by_ratio)

            show_images(width, images)

            print('NOTE: Press the "0" key, to close opened windows')
            cv2.waitKey(0)


def show_images(width, images):
    """show user differences between app image and reference"""

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Difference_RGB"]
    diff = images["Difference_Structure"]
    thresh = images["Thresh"]

    # Show images
    cv2.imshow("Original", original)
    cv2.imshow("Modified", modified)
    cv2.imshow("Difference_RGB", diff_BGR)
    cv2.imshow("Difference_Structure", diff)
    cv2.imshow("Thresh", thresh)
