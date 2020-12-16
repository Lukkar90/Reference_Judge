"""calculate values need in function cv2.putText"""

# python libs
from math import floor

# external libs
import cv2

# internal libs
from Show_Images_Differences.add_text_to_image.helpers.utils import give_pad_value


def calculate_text_values(
        img_h,
        img_w,
        text_description,
        font, thickness,
        percent_of_img,
        fontScale
):
    """return all needed values to render text in cv2.putText"""

    # calculate ratio to resize all values
    resize = get_scale_value(img_w)

    # rescale values
    fontScale, thickness = rescale_values(resize, fontScale, thickness)

    # get values of co-ordinates of text
    coord_w, coord_h = get_middle_coords_of_pad(
        img_h, img_w, text_description, font, thickness, percent_of_img, fontScale)

    # pass co-ordinates
    middle_of_padding = (
        coord_w, coord_h)

    return middle_of_padding, fontScale, thickness


def get_scale_value(img_w):
    """Get multiplier value for text properties"""

    default_size = 512
    resize = img_w/default_size
    return resize


def rescale_values(resize, fontScale, thickness):
    """Resize text properties by multiplier value"""

    fontScale *= resize
    thickness = floor((thickness * 3) * resize)
    return fontScale, thickness


def get_middle_coords_of_pad(
        img_h,
        img_w,
        text_description,
        font, thickness,
        percent_of_img,
        fontScale
):
    """Get coords for relative center of white padding"""

    text_width = cv2.getTextSize(
        text_description, font, fontScale, thickness)[0][0]

    pad_value = give_pad_value(img_h, percent_of_img)

    coord_w = int(img_w/2) - int(text_width/2)
    coord_h = img_h + int(pad_value/2)

    return coord_w, coord_h
