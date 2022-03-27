import unittest
from terminal_graphics import kitty
from io import BytesIO


class KittyTest(unittest.TestCase):

    def test_write_png(self):
        output = BytesIO()

        with open('tests/files/box.png', 'rb') as fin:
            kitty.write_png(fin.read(), output)

        self.assertEqual(
            output.getvalue(),
            b'\x1b_Gm=0,a=T,f=100;'
            b'iVBORw0KGgoAAAANSUhEUgAAAD4AAAA6CAYAAADoUOpSAAAACXBIWXMAAAPYAA'
            b'AD2AFuR2M1AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAA'
            b'AF5JREFUaIHtz0EBACAQgDC1f5sLqDF8jCWAPTN3gc7vgF8a1zSuaVzTuKZxTe'
            b'OaxjWNaxrXNK5pXNO4pnFN45rGNY1rGtc0rmlc07imcU3jmsY1jWsa1zSuaVzTu'
            b'OYBiyUDjLZLEGgAAAAASUVORK5CYII='
            b'\x1b\\')
