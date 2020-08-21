"""App integration test"""


import os
import shutil
import unittest
import sys
from io import StringIO

import cv2

from Reference_Judge.config import ARGV, LEGIT_EXTENSIONS
from Reference_Judge.check_argv_correctness.helpers.check_paths import count_legit_images
from Reference_Judge.Reference_Judge import Reference_Judge


def _get_app_absolute_dir_path(path=""):
    """It works only in tests dir"""

    file_dir = os.getcwd()
    return os.path.join(file_dir, path)


def get_program_name():
    file_dir = os.getcwd()
    parent_dir = os.path.dirname(file_dir)

    return parent_dir


def make_folder_empty(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def check_if_width_is_correct(width, output_folder):
    are_correct = True

    for filename in os.listdir(output_folder):

        file_path = os.path.join(output_folder, filename)

        if os.path.isfile(file_path) and file_path.endswith(LEGIT_EXTENSIONS):

            img = cv2.imread(file_path, 0)
            width_image = img.shape[1]

            if int(width_image / 5) != int(width):
                are_correct = False
                break

    return are_correct


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


program_name = get_program_name()

images_path = "data\\images"
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

    def __init__(self, *args, **kwargs):
        super(TestReferenceJudge, self).__init__(*args, **kwargs)
        self.source_dir = _get_app_absolute_dir_path(test_paths["source dir"])
        self.target_dir = _get_app_absolute_dir_path(test_paths["target dir"])
        self.output_dir = _get_app_absolute_dir_path(test_paths["output dir"])
        self.save = ARGV["save"][0]
        self.show = ARGV["show"][0]
        self.width = "200"
        self.refresh_folder = True

    def test_folder_by_folder_to_folder_save(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        self.assertEqual(number_of_created_files, 2, "Should be 2")

    def test_folder_by_folder_to_folder_save_width(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 2, "Should be 2")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_folder_by_folder_to_folder_show(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width]

        number_of_found = 2

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertTrue(
            number_of_found == output_occurrence,
            f"output: {output}"
        )


if __name__ == '__main__':
    unittest.main()
