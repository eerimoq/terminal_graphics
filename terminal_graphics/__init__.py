import argparse
import sys
from io import BytesIO

from PIL import Image

from . import kitty


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size',
                        default='0x0',
                        help='Width and height in cells (default: 0x0).')
    parser.add_argument('files', nargs="+")
    args = parser.parse_args()

    for file in args.files:
        image = BytesIO()
        Image.open(file).save(image, 'png')
        kitty.write_png(image.getvalue(),
                        fout=sys.stdout.buffer,
                        size=tuple([int(v) for v in args.size.split('x')]))

        sys.stdout.buffer.write(b'\n')
        sys.stdout.buffer.flush()
