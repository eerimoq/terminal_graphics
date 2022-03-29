import termios
import fcntl
import struct
from dataclasses import dataclass
from .utils import Size


@dataclass
class TerminalSize:
    cells: Size
    pixels: Size
    cell_pixels: Size


def get_terminal_size():
    rows, columns, width, height = struct.unpack(
        'HHHH',
        fcntl.ioctl(0,
                    termios.TIOCGWINSZ,
                    struct.pack('HHHH', 0, 0, 0, 0)))

    return TerminalSize(Size(rows, columns),
                        Size(width, height),
                        Size(width // columns, height // rows))
