# python libs
import math

# external libs
import cv2
import numpy as np


def add_text(img, text_description="None", font=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.25, fontColor=(0, 0, 0), lineType=1):

    # check if canvas is to small to add text
    if image_is_bigger_than(100, img):

        # init value
        img_w, img_h = img.shape[:2]

        # add 10% white padding
        percent = 10
        img = add_white_space(img, pad_bot=percent)

        # calculate proportional text values
        bottomLeftCornerOfText, fontScale, lineType = calculate_text_values(
            img_w,
            lineType,
            text_description,
            font,
            img_h,
            percent,
            fontScale
        )

        # add text to image
        cv2.putText(
            img,
            text_description,
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType
        )

    return img


def image_is_bigger_than(value, img):
    w_img = img.shape[1]
    big_enough = w_img >= value

    return big_enough


def add_white_space(img, pad_top=0, pad_bot=0, pad_left=0, pad_right=0, color=(255, 255, 255)):

    pad_top, pad_bot, pad_left, pad_right = calculate_pads_values(
        img, pad_top, pad_bot, pad_left, pad_right)

    return cv2.copyMakeBorder(img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))


def calculate_pads_values(img, pad_top=0, pad_bot=0, pad_left=0, pad_right=0):

    h, w = img.shape[:2]

    if pad_top > 0:
        pad_top = give_pad_value(h, pad_top)

    if pad_bot > 0:
        pad_bot = give_pad_value(h, pad_bot)

    if pad_left > 0:
        pad_left = give_pad_value(w, pad_left)

    if pad_right > 0:
        pad_left = give_pad_value(w, pad_right)

    return (pad_top, pad_bot, pad_left, pad_right)


def calculate_text_values(img_w, lineType, text_description, font, img_h, percent, fontScale):

    # calculate ratio to resize all values
    resize = get_scale_value(img_w)

    # rescale values
    fontScale, lineType = rescale_values(resize, fontScale, lineType)

    # get values of co-ordinates of text
    coord_w, coord_h = get_middle_coords_of_pad(
        text_description, font, fontScale, lineType, img_h, percent, img_w)

    # pass co-ordinates
    middle_of_padding = (
        coord_w, coord_h)

    return middle_of_padding, fontScale, lineType


def get_scale_value(img_w):

    default_size = 512
    resize = default_size/img_w
    return resize


def rescale_values(resize, fontScale, lineType):

    fontScale *= resize
    lineType = math.ceil(lineType * resize)
    return fontScale, lineType


def get_middle_coords_of_pad(text_description, font, fontScale, lineType, img_h, percent, img_w):
    text_width, text_height = cv2.getTextSize(
        text_description, font, fontScale, lineType)[0]

    pad_value = give_pad_value(img_h, percent)

    coord_w = int(img_w/2) - int(text_width/2)
    coord_h = img_h + int(pad_value/1.5)

    return coord_w, coord_h


def give_pad_value(img_edge, percent=0):

    if percent > 0:
        fraction = percent/100
        pad = img_edge*fraction
        pad = int(pad)

    return pad
