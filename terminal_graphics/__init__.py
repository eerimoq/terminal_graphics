import argparse
import sys

from PIL import Image
from PIL.ImageOps import scale as scale_image

from . import kitty
from .utils import pad_ratio


def _do_show(args):
    if args.size is not None:
        size = tuple([int(v) for v in args.size.split('x')])
    else:
        size = None

    for file in args.files:
        write_file(file, sys.stdout.buffer, args.scale, size, args.fill)
        sys.stdout.buffer.write(b'\n')


def _do_info(args):
    print(get_terminal_info())


def _main():
    parser = argparse.ArgumentParser()

    # Workaround to make the subparser required in Python 3.
    subparsers = parser.add_subparsers(title='subcommands',
                                       dest='subcommand')
    subparsers.required = True

    subparser = subparsers.add_parser('show')
    subparser.add_argument('--scale',
                           type=float,
                           help='Image size scale factor.')
    subparser.add_argument('--size', help='Width and height in cells.')
    subparser.add_argument('--fill',
                           action='store_true',
                           help='Stretch or squish to fill given size.')
    subparser.add_argument('files', nargs="+")
    subparser.set_defaults(func=_do_show)

    subparser = subparsers.add_parser('info')
    subparser.set_defaults(func=_do_info)

    args = parser.parse_args()

    try:
        args.func(args)
    except BaseException as e:
        sys.exit('error: ' + str(e))


def write(image, fout, scale=None, size=None, fill=None, protocol=None):
    if scale is not None:
        image = scale_image(image, scale)

    if size is not None and not fill:
        image = pad_ratio(image, size)

    kitty.write(image, fout, size)


def write_file(path, fout, scale=None, size=None, fill=None, protocol=None):
    write(Image.open(path), fout, scale, size, fill, protocol)
