import fcntl
import os
import struct
import termios
from dataclasses import dataclass
from typing import List
from typing import Tuple


@dataclass
class Size:
    cells: Tuple[int, int]
    pixels: Tuple[int, int] = None
    cell_pixels: Tuple[int, int] = None


@dataclass
class KittyGraphicsInfo:
    is_supported: bool
    transmission_mediums: List[str]


@dataclass
class SixelGraphicsInfo:
    is_supported: bool


@dataclass
class ITermGraphicsInfo:
    is_supported: bool


@dataclass
class GraphicsInfo:
    has_true_color: bool
    sixel: SixelGraphicsInfo
    kitty: KittyGraphicsInfo
    iterm: ITermGraphicsInfo


@dataclass
class Info:
    size: Size
    graphics: GraphicsInfo


def get_size():
    rows, columns, width, height = struct.unpack(
        'HHHH',
        fcntl.ioctl(0,
                    termios.TIOCGWINSZ,
                    struct.pack('HHHH', 0, 0, 0, 0)))

    size = Size((columns, rows))

    if width > 0 and height > 0:
        size.pixels = (width, height)
        size.cell_pixels = (width // columns, height // rows)

    return size


def get_graphics_info():
    return GraphicsInfo(os.environ.get('COLORTERM') == 'truecolor',
                        get_sixel_graphics_info(),
                        get_kitty_graphics_info(),
                        get_iterm_graphics_info())


def get_sixel_graphics_info():
    return SixelGraphicsInfo(False)


def get_kitty_graphics_info():
    term = os.environ.get('TERM')
    is_supported = term is not None and 'kitty' in term
    transmission_mediums = []

    if is_supported:
        transmission_mediums.append('direct')

    return KittyGraphicsInfo(is_supported, transmission_mediums)


def get_iterm_graphics_info():
    program = os.environ.get('TERM_PROGRAM')
    is_supported = False

    if program is not None:
        if 'iTerm' in program or 'WezTerm' in program or 'mintty' in program:
            is_supported = True

    return ITermGraphicsInfo(is_supported)


def get_info():
    return Info(get_size(), get_graphics_info())


def get_preferred_graphics_protocol():
    graphics_info = get_graphics_info()

    if graphics_info.kitty.is_supported:
        return 'kitty'
    elif graphics_info.iterm.is_supported:
        return 'iterm'
    elif graphics_info.sixel.is_supported:
        return 'sixel'
    else:
        return 'text'
