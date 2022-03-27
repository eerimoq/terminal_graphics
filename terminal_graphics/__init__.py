import argparse
import sys
from io import BytesIO

from PIL import Image
import numpy

from . import kitty
from .utils import pad_ratio


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help='Width and height in cells.')
    parser.add_argument('--fill',
                        action='store_true',
                        help='Stretch or squish to fill given size.')
    parser.add_argument('files', nargs="+")
    args = parser.parse_args()

    if args.size is not None:
        size = tuple([int(v) for v in args.size.split('x')])
    else:
        size = None

    for file in args.files:
        write_file(file, sys.stdout.buffer, size, args.fill)
        sys.stdout.buffer.write(b'\n')


def write(image, fout, size=None, fill=False, protocol=None):
    if size is not None and not fill:
        image = pad_ratio(image, size)

    kitty.write(image, fout, size)


def write_file(path, fout, size=None, fill=False, protocol=None):
    write(Image.open(path), fout, size, fill, protocol)
