"""adding white (default) padding to image"""

# external libs
import cv2

# internal libs
from add_text_to_image.helpers.utils import give_pad_value


def add_padding(
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
        :param tuples(int G, int B, int R) color: color of added background
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
        pad_right = give_pad_value(w, pad_right)

    return (pad_top, pad_bot, pad_left, pad_right)
