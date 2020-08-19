"""App integration test"""


import os
from Reference_Judge.Reference_Judge import Reference_Judge


def _get_app_absolute_dir_path():
    """It works only in tests dir"""

    file_dir = os.getcwd()
    parent_dir = os.path.dirname(file_dir)
    return parent_dir


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

print(test_paths)
print(Reference_Judge.__doc__)
