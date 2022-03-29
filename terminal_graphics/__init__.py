import argparse
import sys

from PIL import Image
from PIL.ImageOps import scale as scale_image

from . import kitty
from . import sixel
from .terminal import get_terminal_size
from .utils import Size
from .utils import pad_ratio


def _do_show(args):
    if args.size is not None:
        size = Size(args.columns, args.rows)
    else:
        size = None

    for file in args.files:
        write_file(file,
                   sys.stdout.buffer,
                   args.scale,
                   size,
                   args.fill,
                   args.protocol)


def _do_info(args):
    size = get_terminal_size()
    print(f'Rows:       {size.cells.height}')
    print(f'Columns:    {size.cells.width}')
    print(f'Width:      {size.pixels.width}')
    print(f'Height:     {size.pixels.height}')
    print(f'CellWidth:  {size.cell_pixels.width}')
    print(f'CellHeight: {size.cell_pixels.height}')


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
    subparser.add_argument('--protocol',
                           help='Protocol to use.')
    subparser.add_argument('files', nargs="+")
    subparser.set_defaults(func=_do_show)

    subparser = subparsers.add_parser('info')
    subparser.set_defaults(func=_do_info)

    args = parser.parse_args()

    try:
        args.func(args)
    except BaseException as e:
        sys.exit('error: ' + str(e))


def write(image,
          fout,
          scale=None,
          size=None,
          fill=None,
          protocol=None):
    """Write given image to the terinal.

    Size is a tuple of width and height in cells.

    Fill is only used if size is given.

    Protocol is the terminal protocol to use, for example 'kitty'.

    """

    # Remove later.
    if protocol is None:
        protocol = 'kitty'

    if scale is not None:
        image = scale_image(image, scale)

    if size is not None and not fill:
        terminal_size = get_terminal_size()
        image = pad_ratio(image, size, terminal_size.cell_pixels)

    if protocol == 'kitty':
        kitty.write(image, fout, size)
        sys.stdout.buffer.write(b'\n')
    elif protocol == 'sixel':
        sixel.write(image, fout, size)
    else:
        raise Exception(f"Bad protocol '{protocol}.'")


def write_file(path,
               fout,
               scale=None,
               size=None,
               fill=None,
               protocol=None):
    write(Image.open(path), fout, scale, size, fill, protocol)
