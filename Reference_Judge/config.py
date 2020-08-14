"""Place to hold program's global const"""

LEGIT_EXTENSIONS = tuple(".png")

ARGV = {
    "search by ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_SIZES = {
    "highest ratio":  4,
    "lowest ratio": 0.5,
    "biggest dimmension": 1080,
}
