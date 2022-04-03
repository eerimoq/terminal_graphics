import argparse
import sys

from PIL import Image
from PIL.ImageOps import scale as scale_image
from rich.console import Console
from rich.table import Table

from . import kitty
from . import sixel
from .terminal import get_info
from .terminal import get_preferred_graphics_protocol
from .utils import pad_ratio


def _do_show(args):
    maximum_size_pixels = None

    if args.size is not None:
        size = tuple([int(v) for v in args.size.split('x')])
    else:
        size = None
        term_size = get_info().size

        if term_size.pixels is not None:
            maximum_size_pixels = (
                (term_size.cells[0] - 1) * term_size.cell_pixels[0],
                (term_size.cells[1] - 2) * term_size.cell_pixels[1])

    for file in args.files:
        image = Image.open(file)

        if maximum_size_pixels is not None:
            scale = min(maximum_size_pixels[0] / image.width,
                        maximum_size_pixels[1] / image.height)

            if scale < 1:
                image = scale_image(image, scale)

        write(image,
              sys.stdout.buffer,
              size,
              True,
              args.protocol)
        sys.stdout.buffer.write(b'\n')


def _yes_or_no(value):
    if value:
        return 'yes'
    else:
        return 'no'


def _do_info(args):
    info = get_info()
    table = Table('Name', 'Value')

    table.add_row('Rows', str(info.size.cells[1]))
    table.add_row('Columns',    str(info.size.cells[0]))

    if info.size.pixels is not None:
        table.add_row('Width',      str(info.size.pixels[0]))
        table.add_row('Height',     str(info.size.pixels[1]))

    if info.size.cell_pixels is not None:
        table.add_row('CellWidth',  str(info.size.cell_pixels[0]))
        table.add_row('CellHeight', str(info.size.cell_pixels[1]))

    sixel = info.graphics.sixel
    table.add_row('SixelSupport', _yes_or_no(sixel.is_supported))
    kitty = info.graphics.kitty
    table.add_row('KittySupport', _yes_or_no(kitty.is_supported))

    if kitty.is_supported:
        transmission_mediums = ', '.join(kitty.transmission_mediums)
        table.add_row('KittyTransmissionMediums', transmission_mediums)

    iterm = info.graphics.iterm
    table.add_row('ITermSupport', _yes_or_no(iterm.is_supported))

    Console().print(table)


def _main():
    parser = argparse.ArgumentParser()

    # Workaround to make the subparser required in Python 3.
    subparsers = parser.add_subparsers(title='subcommands',
                                       dest='subcommand')
    subparsers.required = True

    subparser = subparsers.add_parser('show')
    subparser.add_argument('--size', help='Width and height in cells.')
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
          fout=None,
          size=None,
          move_cursor=True,
          protocol=None):
    """Write given image to the terinal.

    Size is a tuple of width and height in cells.

    Fill is only used if size is given.

    Protocol is the terminal protocol to use, for example 'kitty'.

    """

    if protocol is None:
        protocol = get_preferred_graphics_protocol()

    if fout is None:
        fout = sys.stdout.buffer

    if size is not None:
        image = pad_ratio(image, size, get_info().size.cell_pixels)

    if protocol == 'kitty':
        kitty.write(image, fout, size, move_cursor)
    elif protocol == 'sixel':
        sixel.write(image, fout, size)
    else:
        raise Exception(f"Unsupported graphics protocol '{protocol}'.")


def write_file(path,
               fout=None,
               size=None,
               move_cursor=True,
               protocol=None):
    write(Image.open(path), fout, size, move_cursor, protocol)
