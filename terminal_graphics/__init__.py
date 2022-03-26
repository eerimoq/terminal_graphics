import argparse
import sys

from . import kitty


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size',
                        default='0x0',
                        help='Width and height in cells (default: 0x0).')
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'rb') as fin:
        kitty.write_png(fin.read(),
                        size=tuple([int(v) for v in args.size.split('x')]))

    print()
