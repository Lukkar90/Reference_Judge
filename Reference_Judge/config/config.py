"""Place to hold program's global const"""

legit_extensions = tuple(".png")

ARGV = {
    "search by ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_sizes = {
    "highest ratio":  4,
    "lowest ratio": 0.5,
    "biggest dimmension": 1080,
}
