import argparse
import sys

from . import kitty


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size',
                        default='0x0',
                        help='Width and height in cells (default: 0x0).')
    parser.add_argument('files', nargs="+")
    args = parser.parse_args()

    for file in args.files:
        with open(file, 'rb') as fin:
            kitty.write_png(fin.read(),
                            fout=sys.stdout.buffer,
                            size=tuple([int(v) for v in args.size.split('x')]))

        sys.stdout.buffer.write(b'\n')
        sys.stdout.buffer.flush()
