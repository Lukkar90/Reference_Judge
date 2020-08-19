""" Add text description to the image"""


# external libs
import cv2

# internal libs
from add_text_to_image.helpers.add_padding import add_padding
from add_text_to_image.helpers.calculate_text_values import calculate_text_values


def add_text_to_image(
        img,
        text_description="None",
        font=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        fontColor=(0, 0, 0),
        thickness=1
):
    """
    Main function, it adds white padding and text at the bottom of provided image
        :param 3d list int img: GBR image
        :param str text_description: percent of added canvas to image, max len of str = 25
        :param cv2.FONT font: https://docs.opencv.org/3.1.0/d0/de1/group__core.html#ga0f9314ea6e35f99bb23f29567fc16e11
        :param int fontScale:
        :param tuples(int R, int G, int B) fontColor:
        :param int thickness:
    """
    # check max length of description
    check_max_str_len(text_description)

    if is_bigger_than(100, img):

        # init value
        img_h, img_w = img.shape[:2]

        # add 10% white padding
        percent_of_img = 10
        img = add_padding(img, pad_bot=percent_of_img)

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


def check_max_str_len(text_description, max_str_len=25):
    """To assure developer that string is not too long to display in image"""
    if len(text_description) > max_str_len:
        raise ValueError(f"Too long description: {max_str_len}\n"
                         f" {text_description}")


def is_bigger_than(value, img):
    """Return bool value if provided image is bigger than provided value"""

    w_img = img.shape[1]
    big_enough = w_img >= value

    return big_enough
