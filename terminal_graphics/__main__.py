import sys

from . import kitty


kitty.write_png(open(sys.argv[1], 'rb').read())
