import argparse
import sys
from io import BytesIO

from PIL import Image

from . import kitty
from .utils import pad_ratio


def _file_to_png_data(file, size, fill):
    image = Image.open(file)

    if size is not None:
        if not fill:
            image = pad_ratio(image, size)

    output = BytesIO()
    image.save(output, 'png', compress_level=1)

    return output.getvalue()


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
        kitty.write_png(_file_to_png_data(file, size, args.fill),
                        sys.stdout.buffer,
                        size)
        sys.stdout.buffer.write(b'\n')
        sys.stdout.buffer.flush()
