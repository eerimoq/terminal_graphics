import argparse
import sys
from io import BytesIO

from PIL import Image

from . import kitty


def _file_to_png_data(file):
    image = BytesIO()
    Image.open(file).save(image, 'png')

    return image.getvalue()


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help='Width and height in cells.')
    parser.add_argument('files', nargs="+")
    args = parser.parse_args()

    if args.size is not None:
        size = tuple([int(v) for v in args.size.split('x')])
    else:
        size = None

    for file in args.files:
        kitty.write_png(_file_to_png_data(file), sys.stdout.buffer, size)
        sys.stdout.buffer.write(b'\n')
        sys.stdout.buffer.flush()
