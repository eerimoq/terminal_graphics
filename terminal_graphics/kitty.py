#
# https://sw.kovidgoyal.net/kitty/graphics-protocol/
#

import sys
from base64 import b64encode
from io import BytesIO

from PIL import Image
import numpy


def _serialize_gr_command(payload, **cmd):
    cmd = ','.join(f'{k}={v}' for k, v in cmd.items())
    ans = []
    ans.append(b'\033_G')
    ans.append(cmd.encode('ascii'))

    if payload:
        ans.append(b';')
        ans.append(payload)

    ans.append(b'\033\\')

    return b''.join(ans)


def _write_chunked(fout, data, **cmd):
    data = b64encode(data)
    reader = BytesIO(data)
    more = True

    while more:
        chunk = reader.read(4096)
        more = (reader.tell() < len(data))
        m = 1 if more else 0
        fout.write(_serialize_gr_command(chunk, m=m, **cmd))
        cmd.clear()


def _write_rgb_rgba(data, fout, width, height, f, size):
    cmd = {}

    if size is not None:
        cmd['c'] = size[0]
        cmd['r'] = size[1]

    _write_chunked(fout, data, a='T', f=f, s=width, v=height, **cmd)


def write_rgb(data, fout, width, height, size=None):
    _write_rgb_rgba(data, fout, width, height, 24, size)


def write_rgba(data, fout, width, height, size=None):
    _write_rgb_rgba(data, fout, width, height, 32, size)


def write_png(data, fout, size=None):
    cmd = {}

    if size is not None:
        cmd['c'] = size[0]
        cmd['r'] = size[1]

    _write_chunked(fout, data, a='T', f=100, **cmd)


def write(image, fout, size=None):
    image = image.convert('RGBA')
    write_rgba(numpy.array(image), fout, image.width, image.height, size)
