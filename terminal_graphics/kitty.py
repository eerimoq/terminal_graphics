#
# https://sw.kovidgoyal.net/kitty/graphics-protocol/
#

import sys
from base64 import b64encode


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

    while data:
        chunk, data = data[:4096], data[4096:]
        m = 1 if data else 0
        fout.write(_serialize_gr_command(chunk, m=m, **cmd))
        cmd.clear()


def write_png(data, fout, size=None):
    cmd = {}

    if size is not None:
        cmd['c'] = size[0]
        cmd['r'] = size[1]

    _write_chunked(fout, data, a='T', f=100, **cmd)
