"""Place to hold program global const"""

legit_extensions = tuple(".png")

ARGV = {
    "search_by_ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_sizes = {
    "highest ratio":  4,
    "lowest_ratio": 0.25,
    "biggest dimmension": 1080,
}
