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


def write_png(image, fout=None, size=(0, 0)):
    if fout is None:
        fout = sys.stdout.buffer

    _write_chunked(fout, image, a='T', f=100, c=size[0], r=size[1])
