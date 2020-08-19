"""Place to hold program's global const"""


LEGIT_EXTENSIONS = tuple(".png")

ARGV = {
    "search by ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_SIZES = {
    "highest scale":  4.0,  # to avoid image distortions
    "lowest scale": 0.5,  # to avoid image distortions
    "biggest dimmension": 1080,  # to avoid performance issues
    "default width": 360,
}

ENOUGH_SIMILARITY = 0.95  # SSMI value in calculating resemblance
