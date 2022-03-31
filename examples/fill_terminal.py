import curses
import sys
from curses import wrapper

from terminal_graphics import write_file
from terminal_graphics.terminal import get_terminal_size


def main(stdscr):
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()
    write_file('lenna.png',
               size=get_terminal_size().cells,
               fill=True,
               move_cursor=False)
    sys.stdout.buffer.flush()
    stdscr.getkey()


wrapper(main)
