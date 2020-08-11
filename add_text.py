"""
MODULE

    Add text

DESCRIPTION

    Add text description to the image
"""

# python libs
import math

# external libs
import cv2


def add_text(
        img,
        text_description="None",
        font=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        fontColor=(0, 0, 0),
        thickness=1
):
    """Main function, it adds white padding and text at the bottom of provided image"""

    # check if canvas is to small to add text
    if is_bigger_than(100, img):

        # init value
        img_h, img_w = img.shape[:2]

        # add 10% white padding
        percent_of_img = 10
        img = add_white_space(img, pad_bot=percent_of_img)

        # calculate proportional text values
        bottom_left_origin, fontScale, thickness = calculate_text_values(
            img_h,
            img_w,
            text_description,
            font,
            thickness,
            percent_of_img,
            fontScale
        )

        # add text to image
        cv2.putText(
            img,
            text_description,
            bottom_left_origin,
            font,
            fontScale,
            fontColor,
            thickness,
        )

    return img


def is_bigger_than(value, img):
    """Return bool value if provided image is bigger than provided value"""

    w_img = img.shape[1]
    big_enough = w_img >= value

    return big_enough


def add_white_space(
        img,
        pad_top=0,
        pad_bot=0,
        pad_left=0,
        pad_right=0,
        color=(255, 255, 255)
):
    """
    Add white padding to the image in chosen direction\n
    :param int pad_top: percent of added canvas to image\n
    :param int pad_bot: percent of added canvas to image\n
    :param int pad_left: percent of added canvas to image\n
    :param int pad_right: percent of added canvas to image\n
    :param tulpe(int red, int green, int blue) pad_right: color of added background
    """

    pad_top, pad_bot, pad_left, pad_right = calculate_pads_values(
        img, pad_top, pad_bot, pad_left, pad_right)

    return cv2.copyMakeBorder(
        img,
        pad_top,
        pad_bot,
        pad_left,
        pad_right,
        borderType=cv2.BORDER_CONSTANT,
        value=color
    )


def calculate_pads_values(img, pad_top=0, pad_bot=0, pad_left=0, pad_right=0):
    """Return value of height of padding in px"""

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
    thickness = math.floor((thickness * 3) * resize)
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


def give_pad_value(img_edge, percent_of_img=0):
    """Create height value for padding"""

    if percent_of_img > 0:
        fraction = percent_of_img/100
        pad = img_edge*fraction
        pad = int(pad)

        # avoid too small pad
        if pad < 20:
            pad = 20

    return pad
