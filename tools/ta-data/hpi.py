#!/usr/bin/env python3
"""Extractor for Total Annihilation HPI-format archives (.hpi/.ufo/.ccx/.gp3).

Usage: hpi.py ARCHIVE OUTDIR [--list] [--filter SUBSTR]
"""
import os, struct, sys, zlib


class HPI:
    def __init__(self, path):
        self.f = open(path, 'rb')
        hdr = self.f.read(20)
        magic, ver, self.dirsize, hkey, self.start = struct.unpack('<4sIIII', hdr)
        if magic != b'HAPI':
            raise ValueError('not an HPI archive: %r' % magic)
        if ver != 0x00010000:
            raise ValueError('unsupported HPI version %#x (save game or HPI v2?)' % ver)
        self.key = (~((hkey * 4) | (hkey >> 6))) & 0xFF if hkey else 0
        # The directory block is addressed by absolute file offset.
        self.dir = self.read(self.start, self.dirsize - self.start)
        self.dir_base = self.start

    def read(self, pos, n):
        self.f.seek(pos)
        data = bytearray(self.f.read(n))
        if self.key:
            k = self.key
            for i in range(len(data)):
                t = ((pos + i) ^ k) & 0xFF
                data[i] = t ^ (~data[i] & 0xFF)
        return bytes(data)

    def _d(self, off, n):
        o = off - self.dir_base
        return self.dir[o:o + n]

    def _i32(self, off):
        return struct.unpack('<i', self._d(off, 4))[0]

    def _cstr(self, off):
        o = off - self.dir_base
        e = self.dir.index(b'\0', o)
        return self.dir[o:e].decode('latin-1')

    def walk(self, off=None, prefix=''):
        if off is None:
            off = self.start
        n = self._i32(off)
        lst = self._i32(off + 4)
        for i in range(n):
            e = lst + i * 9
            name_off, data_off = struct.unpack('<ii', self._d(e, 8))
            is_dir = self._d(e + 8, 1)[0]
            name = self._cstr(name_off)
            path = prefix + name
            if is_dir:
                yield from self.walk(data_off, path + '/')
            else:
                doff, size, flag = struct.unpack('<iiB', self._d(data_off, 9))
                yield path, doff, size, flag

    def extract(self, doff, size, flag):
        if flag == 0:
            return self.read(doff, size)
        nchunks = (size + 65535) // 65536
        sizes = struct.unpack('<%di' % nchunks, self.read(doff, 4 * nchunks))
        pos = doff + 4 * nchunks
        out = bytearray()
        for cs in sizes:
            chunk = self.read(pos, cs)
            pos += cs
            out += self._chunk(chunk)
        return bytes(out[:size])

    @staticmethod
    def _chunk(c):
        marker, ver, meth, enc, csize, dsize, chk = struct.unpack('<4sBBBiii', c[:19])
        if marker != b'SQSH':
            raise ValueError('bad chunk marker')
        data = bytearray(c[19:19 + csize])
        if enc:
            for x in range(len(data)):
                data[x] = ((data[x] - x) & 0xFF) ^ (x & 0xFF)
        if meth == 0:
            return bytes(data)
        if meth == 2:
            return zlib.decompress(bytes(data))
        if meth == 1:
            return lz77(data, dsize)
        raise ValueError('unknown compression %d' % meth)


def lz77(inp, dsize):
    out = bytearray()
    buf = bytearray(4096)
    w1 = 1
    ip = 0
    mask = 1
    tag = inp[ip]; ip += 1
    while True:
        if not (mask & tag):
            b = inp[ip]; ip += 1
            out.append(b); buf[w1] = b; w1 = (w1 + 1) & 0xFFF
        else:
            cnt = inp[ip] | (inp[ip + 1] << 8); ip += 2
            dp = cnt >> 4
            if dp == 0:
                break
            cnt = (cnt & 0x0F) + 2
            for _ in range(cnt):
                b = buf[dp]
                out.append(b); buf[w1] = b
                dp = (dp + 1) & 0xFFF; w1 = (w1 + 1) & 0xFFF
        mask <<= 1
        if mask & 0x100:
            mask = 1
            tag = inp[ip]; ip += 1
    return bytes(out)


def main():
    args = sys.argv[1:]
    listing = '--list' in args
    flt = None
    if '--filter' in args:
        i = args.index('--filter'); flt = args[i + 1].lower(); del args[i:i + 2]
    args = [a for a in args if a != '--list']
    h = HPI(args[0])
    outdir = args[1] if len(args) > 1 else None
    for path, doff, size, flag in h.walk():
        if flt and flt not in path.lower():
            continue
        if listing:
            print('%10d %d %s' % (size, flag, path))
            continue
        dest = os.path.join(outdir, path.lower().replace('\\', '/'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as o:
            o.write(h.extract(doff, size, flag))


if __name__ == '__main__':
    main()
