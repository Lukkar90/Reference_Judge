"""
Place to store all generic data for user about program help
"""
# python libs
import sys

# internal libs
from config import ARGV


def help_command_line():
    """Explaining user general usage of program"""

    # https://stackoverflow.com/a/35514032/12490791
    program_name = sys.argv[0]

    # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
    return (f"Usage: python {program_name} <original_reference_path> <app_reference_path> <--mode> [directory_differences_output]"
            f" [width] [{ARGV['search by ratio'][0]}]")


def help_tip():
    """String to use when user write wrong input, showing him how to invoke help function"""

    # https://stackoverflow.com/a/35514032/12490791
    program_name = sys.argv[0]

    return f"For more information:\n Usage: python {program_name} {ARGV['help'][0]}"


def help_detailed_usage():
    """showing user "usage" of program"""
    sys.exit(DetailedUsage().string)


def user_commanded_help(argv_):
    """return bool"""
    return len(argv_) == 2 and argv_[1] in ARGV["help"]


class DetailedUsage():
    """create complete usage instructions for client"""

    program_name = sys.argv[0]

    def __init__(self, program_name=program_name):
        self.string = (
            "\n"
            f"{help_command_line()}\n"
            "\n"
            "On desktop:\n"
            " save:\n"
            f"  python {program_name} path_dir path_dir {ARGV['save'][0]} path_dir [px] [r]\n"
            f"  python {program_name} path_dir path_dir {ARGV['save'][0]} path_file [px] [r]\n"
            f"  python {program_name} path_file path_dir {ARGV['save'][0]} path_dir [px] [r]\n"
            f"  python {program_name} path_file path_file {ARGV['save'][0]} path_dir [px] [r] *\n"
            f"  python {program_name} path_file path_file {ARGV['save'][0]} path_file [px] [r] *\n"
            "\n"
            " show:\n"
            f"  python {program_name} path_dir path_dir {ARGV['show'][0]} [px] [r]\n"
            f"  python {program_name} path_file path_dir {ARGV['show'][0]} [px] [r]\n"
            f"  python {program_name} path_file path_file {ARGV['show'][0]} [px] [r] *\n"
            "\n"
            "HTTPS:\n"
            " save:\n"
            f"  python {program_name} https/address.com/image.img https/address.com/image.img {ARGV['save'][0]} path_dir [px] [r] *\n"
            f"  python {program_name} https/address.com/image.img https/address.com/image.img {ARGV['save'][0]} path_file [px] [r] *\n"
            f"  python {program_name} https/address.com/image.img path_dir {ARGV['save'][0]} path_dir [px] [r]\n"
            f"  python {program_name} https/address.com/image.img path_dir {ARGV['save'][0]} path_file [px] [r]\n"
            f"  python {program_name} path_file https/address.com/image.img {ARGV['save'][0]} path_dir [px] [r] *\n"
            f"  python {program_name} path_file https/address.com/image.img {ARGV['save'][0]} path_file [px] [r] *\n"
            "\n"
            " show:\n"
            f"  python {program_name} https/address.com/image.img https/address.com/image.img {ARGV['show'][0]} [px] [r] *\n"
            f"  python {program_name} path_file https/address.com/image.img {ARGV['show'][0]} [px] [r] *\n"
            f"  python {program_name} https/address.com/image.img path_file {ARGV['show'][0]} [px] [r] *\n"
            f"  python {program_name} https/address.com/image.img path_dir {ARGV['show'][0]} [px] [r]\n"
            "\n"
            " * images have to be the same size\n"
            " [px] is optional value of width of each image\n"
            f" abbr of {ARGV['save'][0]} is {ARGV['save'][1]}\n"
            f" abbr of {ARGV['show'][0]} is {ARGV['show'][1]}\n"
            f" [r] {ARGV['search by ratio'][0]} or {ARGV['search by ratio'][1]} -> images could be different sizes but they have to be the same ratio"
        )
