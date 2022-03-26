import sys

from . import kitty


def _main():
    kitty.write_png(open(sys.argv[1], 'rb').read())

