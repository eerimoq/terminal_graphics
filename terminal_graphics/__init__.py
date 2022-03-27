import argparse
import sys

from PIL import Image
from PIL.ImageOps import scale as scale_image

from . import kitty


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scale',
                        type=float,
                        help='Image size scale factor.')
    parser.add_argument('files', nargs="+")
    args = parser.parse_args()

    for file in args.files:
        write_file(file, sys.stdout.buffer, args.scale)
        sys.stdout.buffer.write(b'\n')


def write(image, fout, scale=None, protocol=None):
    if scale is not None:
        image = scale_image(image, scale)

    kitty.write(image, fout)


def write_file(path, fout, scale=None, protocol=None):
    write(Image.open(path), fout, scale, protocol)
