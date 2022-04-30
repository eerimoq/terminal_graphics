#
# https://iterm2.com/documentation-images.html
#

from base64 import b64encode


def write(data, fout, size=None):
    arguments = f'size={len(data)};inline=1'

    if size is not None:
        arguments += f';width={size[0]};height={size[1]}'

    fout.write(f'\033]1337;File={arguments}:'.encode('utf-8'))
    fout.write(b64encode(data))
    fout.write(b'\a')
