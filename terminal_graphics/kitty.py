#
# https://sw.kovidgoyal.net/kitty/graphics-protocol/
#

import sys
from base64 import b64encode
from io import BytesIO

import numpy
from PIL import Image


def _serialize_gr_command(payload, **cmd):
    cmd = ','.join(f'{k}={v}' for k, v in cmd.items())
    data = []
    data.append(b'\033_G')
    data.append(cmd.encode('ascii'))

    if payload:
        data.append(b';')
        data.append(payload)

    data.append(b'\033\\')

    return b''.join(data)


def _write_chunked(fout, data, **cmd):
    data = b64encode(data)
    reader = BytesIO(data)
    more = 1

    while more == 1:
        chunk = reader.read(4096)
        more = 1 if reader.tell() < len(data) else 0
        fout.write(_serialize_gr_command(chunk, m=more, **cmd))
        cmd.clear()


def _write_rgb_rgba(data, width, height, fout, f, size):
    cmd = {}

    if size is not None:
        cmd['c'] = size.width
        cmd['r'] = size.height

    _write_chunked(fout, data, a='T', f=f, s=width, v=height, **cmd)


def write_rgb(data, width, height, fout, size=None):
    _write_rgb_rgba(data, width, height, fout, 24, size)


def write_rgba(data, width, height, fout, size=None):
    _write_rgb_rgba(data, width, height, fout, 32, size)


def write_png(data, fout, size=None):
    cmd = {}

    if size is not None:
        cmd['c'] = size.width
        cmd['r'] = size.height

    _write_chunked(fout, data, a='T', f=100, **cmd)


def write(image, fout, size=None):
    image = image.convert('RGBA')
    write_rgba(numpy.array(image), image.width, image.height, fout, size)
