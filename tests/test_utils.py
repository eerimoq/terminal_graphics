import os
import unittest

from PIL import Image

from terminal_graphics import utils

from .utils import TestCase


class KittyTest(TestCase):

    def test_split_image_horizontally(self):
        image = Image.open('tests/files/test_split_image_horizontally/diagonal.png')
        images = list(utils.split_image_horizontally(image, 3))
        self.assertEqual(len(images), 3)
        os.makedirs('tests/build/test_split_image_horizontally', exist_ok=True)

        for i in range(3):
            actual = f'tests/build/test_split_image_horizontally/{i}.png'
            expected = f'tests/files/test_split_image_horizontally/{i}.png'
            images[i].save(actual)
            self.assert_files_equal(actual, expected)
