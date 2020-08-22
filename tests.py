"""App integration test"""


import os
import shutil
import unittest
import sys
from io import StringIO

import cv2

from Reference_Judge.help import help_tip, help_command_line
from Reference_Judge.config import ARGV, LEGIT_EXTENSIONS, IMAGES_SIZES
from Reference_Judge.check_argv_correctness.helpers.check_paths import count_legit_images
from Reference_Judge.Reference_Judge import Reference_Judge


def _get_app_absolute_dir_path(path=""):
    """It works only in tests dir"""

    file_dir = os.getcwd()
    return os.path.join(file_dir, path)


def get_program_name():
    program_name = sys.argv[0]

    return program_name


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
    "custom name": "new name.png",
    "source dir": images_path + "\\original",
    "target dir": images_path + "\\modified",
    "output dir": images_path + "\\output",
    "source file": "modified.png",
    "target file": "modified.png",
    "target file size": "Android-Login 01.png",
    "target file size err": "Android-Login 01.png",
    "target file ratio err": "Android-Login 01.png",
    "http source": "https://pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png",
    "http target": "https://3.bp.blogspot.com/-idDNlSH6Sas/U8_gCraGJZI/AAAAAAAAAt4/6xAk4-AuE68/s1600/opencv_logo_with_text.png",
    "source file http": "opencv_logo.png",
    "target file http": "opencv_logo.png",
    "by ratio": ARGV["search by ratio"][0],
    "random": "pizza time!"
}


class TestReferenceJudge(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestReferenceJudge, self).__init__(*args, **kwargs)

        self.source_dir = _get_app_absolute_dir_path(test_paths["source dir"])
        self.target_dir = _get_app_absolute_dir_path(test_paths["target dir"])
        self.output_dir = _get_app_absolute_dir_path(test_paths["output dir"])

        self.source_single = os.path.join(
            self.source_dir, test_paths["source file"])
        self.target_single = os.path.join(
            self.target_dir,  test_paths["target file"])
        self.output_single = os.path.join(
            self.output_dir, test_paths["custom name"])

        self.http_source = test_paths["http source"]
        self.http_target = test_paths["http target"]

        self.source_file_http = os.path.join(
            self.source_dir, test_paths["source file http"])
        self.target_file_http = os.path.join(
            self.target_dir, test_paths["target file http"])

        self.save = ARGV["save"][0]
        self.show = ARGV["show"][0]

        self.width = "200"
        self.width_DEFAULT = IMAGES_SIZES["default width"]

        self.by_ratio = test_paths["by ratio"]

        self.refresh_folder = True

        self.target_fail = os.path.join(
            self.target_dir, test_paths["custom name"])

        self.source_dir_fail = self.source_dir + "Null"
        self.target_dir_fail = self.target_dir + "Nana"
        self.output_dir_fail = self.output_dir + "Zero"
        self.http_source_fail = self.http_source + "Void"

        self.random = test_paths["random"]

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
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 2, "Should be 2")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_folder_by_folder_to_single_save(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_single]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 2, "Should be 2")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

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

    def test_http_by_folder_to_folder_save(self):

        _argv = [program_name, self.http_source,
                 self.target_dir, self.save, self.output_dir]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_single_by_single_to_single_save(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_single]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_single_by_single_to_single_save_width(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_single, self.width]

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
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_single_by_single_to_folder_save(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_dir]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_single_by_single_to_folder_save_width(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_dir, self.width]

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
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_http_by_single_to_folder_save(self):

        _argv = [program_name, self.http_source,
                 self.target_file_http, self.save, self.output_dir]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_http_by_single_to_folder_save_width(self):

        _argv = [program_name, self.http_source,
                 self.target_file_http, self.save, self.output_dir, self.width]

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
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_http_by_single_to_single_save(self):

        _argv = [program_name, self.http_source,
                 self.target_file_http, self.save, self.output_single]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_http_by_http_to_folder_save(self):

        _argv = [program_name, self.http_source,
                 self.http_target, self.save, self.output_dir]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_single_by_http_to_folder_save(self):

        _argv = [program_name, self.source_file_http,
                 self.http_target, self.save, self.output_dir]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_http_by_http_to_single_save(self):

        _argv = [program_name, self.http_source,
                 self.http_target, self.save, self.output_single]

        # make sure that folder is empty
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        # run module
        Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 1, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_single_by_single_show(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.show]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 1, "Should be 1")

    def test_single_by_single_show_width(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.show, self.width]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 1, "Should be 1")

    def test_folder_by_folder_show(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 2, "Should be 1")

    def test_single_by_folder_show(self):

        _argv = [program_name, self.source_single,
                 self.target_dir, self.show]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 1, "Should be 1")

    def test_http_by_folder_show(self):

        _argv = [program_name, self.http_source,
                 self.target_dir, self.show]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 1, "Should be 1")

    def test_folder_by_folder_save_by_ratio(self):  # todo

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.by_ratio]

        with Capturing() as output:

            Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width_DEFAULT, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 3, "Should be 3")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_folder_by_folder_save_width_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width, self.by_ratio]

        with Capturing() as output:

            Reference_Judge(_argv)

        # check conditions
        number_of_created_files = count_legit_images(self.output_dir)
        legit_5_times_widths = check_if_width_is_correct(
            self.width, self.output_dir)

        # refresh folder
        if self.refresh_folder:
            make_folder_empty(self.output_dir)

        with self.subTest():
            self.assertEqual(number_of_created_files, 3, "Should be 1")

        with self.subTest():
            self.assertTrue(legit_5_times_widths,
                            "Should be 5 more than width input")

    def test_folder_by_folder_show_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.by_ratio]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 3, "Should be 3")

    def test_folder_by_folder_show_width_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width, self.by_ratio]

        with Capturing() as output:

            Reference_Judge(_argv)

        output_occurrence = output.count(
            'NOTE: Press the "0" key, to close opened windows')

        self.assertEqual(output_occurrence, 3, "Should be 1")

    def test_FAIL_file_does_not_exists(self):

        _argv = [program_name, self.source_dir,
                 self.target_fail, self.save, self.output_dir]

        error_message = (f"Error: File does not exists:\n"
                         f" {self.target_fail}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_too_small_number_of_args(self):

        _argv = [program_name, self.source_dir, self.show]

        error_message = (f"{help_command_line()}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_no_output_file(self):

        _argv = [program_name, self.source_dir, self.target_dir, self.save]

        error_message = ("Error: No output path\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_4th_last_argument_should_numeric_or_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.random]

        error_message = (f'Error: 4th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                         f" {self.random}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_5th_last_argument_should_numeric_or_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.random]

        error_message = (f'Error: 5th, last argument should be numeric or be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                         f" {self.random}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_6th_last_argument_should_numeric_or_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width, self.random]

        error_message = (f'Error: 6th, last argument should be {ARGV["search by ratio"][0]} or {ARGV["search by ratio"][1]}:\n'
                         f" {self.random}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_directory_with_app_references_does_not_exists(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir_fail, self.show]

        error_message = (f"Error: Directory with app references does not exist:\n"  # todo {dir_kind}
                         f" {self.target_dir_fail}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_directory_with_original_references_does_not_exists(self):

        _argv = [program_name, self.source_dir_fail,
                 self.target_dir, self.show]

        error_message = (f"Error: Directory with original references does not exist:\n"  # todo {dir_kind}
                         f" {self.source_dir_fail}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_output_directory_does_not_exists(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir_fail]

        error_message = (f"Error: Output directory does not exists:\n"  # todo {dir_kind}
                         f" {self.output_dir_fail}\n"
                         f"{help_tip()}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)

    def test_FAIL_http_Error_404(self):

        _argv = [program_name, self.http_source_fail,
                 self.target_dir, self.save, self.output_dir]

        error_message = (f"Error: path http: HTTP Error 404: Not Found:\n"  # todo {dir_kind}
                         f" {self.http_source_fail}")

        with self.assertRaises(SystemExit) as cm:
            # run module
            Reference_Judge(_argv)

        self.assertEqual(cm.exception.code, error_message)


if __name__ == '__main__':
    unittest.main()
