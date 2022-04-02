import fcntl
import os
import struct
import termios
from dataclasses import dataclass
from typing import List
from typing import Tuple


@dataclass
class TerminalSize:
    cells: Tuple[int, int]
    pixels: Tuple[int, int] = None
    cell_pixels: Tuple[int, int] = None


def get_terminal_size():
    rows, columns, width, height = struct.unpack(
        'HHHH',
        fcntl.ioctl(0,
                    termios.TIOCGWINSZ,
                    struct.pack('HHHH', 0, 0, 0, 0)))

    terminal_size = TerminalSize((columns, rows))

    if width > 0 and height > 0:
        terminal_size.pixels = (width, height)
        terminal_size.cell_pixels = (width // columns, height // rows)

    return terminal_size


@dataclass
class TerminalGraphicsKittyInfo:
    is_supported: bool
    transmission_mediums: List[str]


@dataclass
class TerminalGraphicsSixelInfo:
    is_supported: bool


@dataclass
class TerminalGraphicsITermInfo:
    is_supported: bool


@dataclass
class TerminalGraphicsInfo:
    has_true_color: bool
    sixel: TerminalGraphicsSixelInfo
    kitty: TerminalGraphicsKittyInfo
    iterm: TerminalGraphicsITermInfo

def get_terminal_graphics_info():
    return TerminalGraphicsInfo(
        os.environ.get('COLORTERM') == 'truecolor',
        get_terminal_graphics_sixel_info(),
        get_terminal_graphics_kitty_info(),
        get_terminal_graphics_iterm_info())


def get_terminal_graphics_sixel_info():
    return TerminalGraphicsSixelInfo(False)


def get_terminal_graphics_kitty_info():
    term = os.environ.get('TERM')
    is_supported = term is not None and 'kitty' in term
    transmission_mediums = []

    if is_supported:
        transmission_mediums.append('direct')

    return TerminalGraphicsKittyInfo(is_supported,
                                             transmission_mediums)


def get_terminal_graphics_iterm_info():
    program = os.environ.get('TERM_PROGRAM')
    is_supported = False

    if program is not None:
        if 'iTerm' in program or 'WezTerm' in program or 'mintty' in program:
            is_supported = True

    return TerminalGraphicsITermInfo(is_supported)


def get_preferred_graphics_protocol():
    graphics_info = get_terminal_graphics_info()

    if graphics_info.kitty.is_supported:
        return 'kitty'
    elif graphics_info.iterm.is_supported:
        return 'iterm'
    elif graphics_info.sixel.is_supported:
        return 'sixel'
    else:
        return 'text'
