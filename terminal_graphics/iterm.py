#
# https://iterm2.com/documentation-images.html
#

from base64 import b64encode


def write(data, fout):
    fout.write(f'\033]1337;File=size={len(data)};inline=1:'.encode('utf-8'))
    fout.write(b64encode(data))
    fout.write(b'\a')
