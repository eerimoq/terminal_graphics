import fcntl
import struct
import termios
from dataclasses import dataclass
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
