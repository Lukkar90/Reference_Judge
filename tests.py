"""App integration test"""


import os
import unittest
from Reference_Judge.config import ARGV
from Reference_Judge.check_argv_correctness.helpers.check_paths import count_legit_images
from Reference_Judge.Reference_Judge import Reference_Judge


def _get_app_absolute_dir_path(path=""):
    """It works only in tests dir"""

    file_dir = os.getcwd()
    return os.path.join(file_dir, path)


images_path = "data\\images_test"
test_paths = {
    "source dir": images_path + "\\original",
    "target dir": images_path + "\\modified",
    "output dir": images_path + "\\output",
    "source file": "Android-Login.png",
    "target file": "Android-Login.png",
    "target file size": "Android-Login 01.png",
    "target file size err": "Android-Login 01.png",
    "target file ratio err": "Android-Login 01.png",
    "http": "https://pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png"
}


class TestReferenceJudge(unittest.TestCase):

    def __init__(self):
        self.source_dir = _get_app_absolute_dir_path(test_paths["source dir"])
        self.target_dir = _get_app_absolute_dir_path(test_paths["target_dir"])
        self.output_dir = _get_app_absolute_dir_path(test_paths["output dir"])
        self.save = ARGV["save"][0]

    def test_folder_to_folder(self):

        self.assertEqual(os.system(), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()
