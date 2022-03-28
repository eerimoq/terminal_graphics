import argparse
import sys

from PIL import Image
from PIL.ImageOps import scale as scale_image

from . import kitty
from .utils import pad_ratio


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale',
                        type=float,
                        help='Image size scale factor.')
    parser.add_argument('--size', help='Width and height in cells.')
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
        write_file(file, sys.stdout.buffer, args.scale, size, args.fill)
        sys.stdout.buffer.write(b'\n')


def write(image, fout, scale=None, size=None, fill=None, protocol=None):
    if scale is not None:
        image = scale_image(image, scale)

    if size is not None and not fill:
        image = pad_ratio(image, size)

    kitty.write(image, fout, size)


def write_file(path, fout, scale=None, size=None, fill=None, protocol=None):
    write(Image.open(path), fout, scale, size, fill, protocol)
