import fcntl
import struct
import termios
from dataclasses import dataclass
from typing import Tuple


@dataclass
class TerminalSize:
    cells: Tuple[int, int]
    pixels: Tuple[int, int]
    cell_pixels: Tuple[int, int]


def get_terminal_size():
    rows, columns, width, height = struct.unpack(
        'HHHH',
        fcntl.ioctl(0,
                    termios.TIOCGWINSZ,
                    struct.pack('HHHH', 0, 0, 0, 0)))

    return TerminalSize((columns, rows),
                        (width, height),
                        (width // columns, height // rows))
