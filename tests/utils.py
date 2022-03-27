import difflib
import os
import shutil
import unittest


class TestCase(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        os.makedirs('tests/build', exist_ok=True)

    def assert_in(self, needle, haystack):
        try:
            self.assertIn(needle, haystack)
        except AssertionError:
            differ = difflib.Differ()
            diff = differ.compare(needle.splitlines(), haystack.splitlines())

            raise AssertionError(
                '\n' + '\n'.join([diffline.rstrip('\n') for diffline in diff]))

    def assert_not_in(self, needle, haystack):
        self.assertNotIn(needle, haystack)

    def assert_exception_string(self, cm, expected):
        self.assertEqual(expected, remove_ansi(str(cm.exception)))

    def assert_file_exists(self, path):
        self.assertTrue(os.path.exists(path))

    def assert_file_not_exists(self, path):
        self.assertFalse(os.path.exists(path))

    def assert_files_equal(self, actual, expected):
        # os.makedirs(os.path.dirname(expected), exist_ok=True)
        # open(expected, 'wb').write(open(actual, 'rb').read())
        self.assertEqual(read_file(actual), read_file(expected))

    def assert_in_file(self, needle, haystack):
        self.assert_in(needle, read_file(haystack))

    def assert_not_in_file(self, needle, haystack):
        self.assertNotIn(needle, read_file(haystack))


def read_file(filename):
    with open(filename, 'rb') as fin:
        return fin.read()


def remove_directory(name):
    if os.path.exists(name):
        shutil.rmtree(name)


def remove_build_directory(name):
    remove_directory('tests/build/' + name)


class Path:

    def __init__(self, new_dir):
        self.new_dir = new_dir
        self.old_dir = None

    def __enter__(self):
        self.old_dir = os.getcwd()
        os.chdir(self.new_dir)

        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self.old_dir)

        return False
