"""Place to hold program's global const"""

# https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
LEGAL_EXTENSIONS = tuple(".png")  # must be tuple to provide multiply extensions

ARGV = {
    "search by ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_SIZES = {
    "highest scale":  4.0,  # to avoid image distortions
    "lowest scale": 0.5,  # to avoid image distortions
    "biggest dimension": 1080,  # to avoid performance issues
    "smallest dimension": 1,
    "default width": 360,
}

SIMILARITY = {
    "enough": 0.95,  # SSMI value in calculating resemblance, 1 is Max
    "not enough": 0.10  # Why so low? Well... this is the lowest value in which matching makes any sense
}
