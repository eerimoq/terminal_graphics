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
class TerminalGraphicsKittyProtocolInfo:
    is_supported: bool
    transmission_mediums: List[str]


@dataclass
class TerminalGraphicsSixelProtocolInfo:
    is_supported: bool


@dataclass
class TerminalGraphicsITermProtocolInfo:
    is_supported: bool


@dataclass
class TerminalGraphicsProtocolInfo:
    sixel: TerminalGraphicsSixelProtocolInfo
    kitty: TerminalGraphicsKittyProtocolInfo
    iterm: TerminalGraphicsITermProtocolInfo

def get_terminal_graphics_protocol_info():
    return TerminalGraphicsProtocolInfo(
        get_terminal_graphics_sixel_protocol_info(),
        get_terminal_graphics_kitty_protocol_info(),
        get_terminal_graphics_iterm_protocol_info())


def get_terminal_graphics_sixel_protocol_info():
    return TerminalGraphicsSixelProtocolInfo(False)


def get_terminal_graphics_kitty_protocol_info():
    term = os.environ.get('TERM')
    is_supported = term is not None and 'kitty' in term
    transmission_mediums = []

    if is_supported:
        transmission_mediums.append('direct')

    return TerminalGraphicsKittyProtocolInfo(is_supported,
                                             transmission_mediums)


def get_terminal_graphics_iterm_protocol_info():
    program = os.environ.get('TERM_PROGRAM')
    is_supported = False

    if program is not None:
        if 'iTerm' in program or 'WezTerm' in program or 'mintty' in program:
            is_supported = True

    return TerminalGraphicsITermProtocolInfo(is_supported)
