import argparse
import sys

from PIL import Image
from PIL.ImageOps import scale as scale_image

from . import kitty
from . import sixel
from .terminal import get_preferred_graphics_protocol
from .terminal import get_terminal_graphics_protocol_info
from .terminal import get_terminal_size
from .utils import pad_ratio


def _do_show(args):
    if args.size is not None:
        size = (args.columns, args.rows)
    else:
        size = None

    for file in args.files:
        write_file(file,
                   sys.stdout.buffer,
                   args.scale,
                   size,
                   args.fill,
                   True,
                   args.protocol)
        sys.stdout.buffer.write(b'\n')


def _yes_or_no(value):
    if value:
        return 'yes'
    else:
        return 'no'


def _do_info(args):
    size = get_terminal_size()
    print(f'Rows:       {size.cells[1]}')
    print(f'Columns:    {size.cells[0]}')

    if size.pixels is not None:
        print(f'Width:      {size.pixels[0]}')
        print(f'Height:     {size.pixels[1]}')

    if size.cell_pixels is not None:
        print(f'CellWidth:  {size.cell_pixels[0]}')
        print(f'CellHeight: {size.cell_pixels[1]}')

    graphics_protocol_info = get_terminal_graphics_protocol_info()
    sixel = graphics_protocol_info.sixel
    print(f'SixelSupport: {_yes_or_no(sixel.is_supported)}')
    kitty = graphics_protocol_info.kitty
    print(f'KittySupport: {_yes_or_no(kitty.is_supported)}')

    if kitty.is_supported:
        transmission_mediums = ', '.join(kitty.transmission_mediums)
        print(f'KittyTransmissionMediums: {transmission_mediums}')

    iterm = graphics_protocol_info.iterm
    print(f'ITermSupport: {_yes_or_no(iterm.is_supported)}')


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
          fout=None,
          scale=None,
          size=None,
          fill=None,
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

    if scale is not None:
        image = scale_image(image, scale)

    if size is not None and not fill:
        terminal_size = get_terminal_size()
        image = pad_ratio(image, size, terminal_size.cell_pixels)

    if protocol == 'kitty':
        kitty.write(image, fout, size, move_cursor)
    elif protocol == 'sixel':
        sixel.write(image, fout, size)
    else:
        raise Exception(f"Unsupported protocol '{protocol}'.")


def write_file(path,
               fout=None,
               scale=None,
               size=None,
               fill=None,
               move_cursor=True,
               protocol=None):
    write(Image.open(path), fout, scale, size, fill, move_cursor, protocol)
