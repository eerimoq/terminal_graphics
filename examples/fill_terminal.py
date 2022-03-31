import curses
import sys
from curses import wrapper

from PIL import Image
from PIL import ImageDraw

from terminal_graphics import write
from terminal_graphics.terminal import get_terminal_size


def main(stdscr):
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()
    image = Image.open('lenna.png')
    draw = ImageDraw.Draw(image)
    draw.text((80, 20), "Press any key to exit!")
    write(image,
          size=get_terminal_size().cells,
          fill=True,
          move_cursor=False)
    sys.stdout.buffer.flush()
    stdscr.getkey()


wrapper(main)
