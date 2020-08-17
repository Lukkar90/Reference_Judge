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
