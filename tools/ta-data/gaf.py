#!/usr/bin/env python3
"""TA GAF animations -> sprite sheet grids (for CEG animated textures).

  gaf.py FILE.gaf PALETTE.pal OUTDIR [--filter substr] [--black]

One PNG per sequence: every frame in a cell of the same size, aligned on the frame's origin (TA's x/y offset) so
the animation does not wobble, left to right, top to bottom. Transparent pixels get alpha 0 (or black with --black,
for additive blending). Writes OUTDIR/index.json: per sequence the grid (cols x rows), cell size, frame count and
the origin inside the cell.
"""
import json, math, os, struct, sys
from PIL import Image


def read_palette(path):
    d = open(path, 'rb').read()
    return [tuple(d[i * 4:i * 4 + 3]) for i in range(256)]


class GAF:
    def __init__(self, path):
        self.d = open(path, 'rb').read()
        ver, n, _ = struct.unpack_from('<iii', self.d, 0)
        if ver != 0x00010100:
            raise ValueError('not a GAF file')
        self.entries = struct.unpack_from('<%di' % n, self.d, 12)

    def sequences(self):
        for p in self.entries:
            frames, _u1, _u2 = struct.unpack_from('<hhi', self.d, p)
            name = self.d[p + 8:p + 40].split(b'\0')[0].decode('latin-1')
            out = []
            for i in range(frames):
                fp, dur = struct.unpack_from('<ii', self.d, p + 40 + i * 8)
                out.append((self.frame(fp), dur))
            yield name, out

    def frame(self, p):
        """-> (w, h, ox, oy, pixels dict or list of layers). pixels: bytearray w*h of palette index, None = transparent."""
        w, h, ox, oy, trans, comp, nsub, _u, ptr, _u3 = struct.unpack_from('<hhhhBBhiii', self.d, p)
        if nsub > 0:
            subs = [self.frame(q) for q in struct.unpack_from('<%di' % nsub, self.d, ptr)]
            # composite: every subframe placed by its own origin, relative to the parent origin
            img = [None] * (w * h)
            for sw, sh, sox, soy, spx in subs:
                for y in range(sh):
                    for x in range(sw):
                        v = spx[y * sw + x]
                        tx, ty = x - sox + ox, y - soy + oy
                        if v is not None and 0 <= tx < w and 0 <= ty < h:
                            img[ty * w + tx] = v
            return w, h, ox, oy, img
        px = [None] * (w * h)
        if comp:
            q = ptr
            for y in range(h):
                n = struct.unpack_from('<H', self.d, q)[0]
                q += 2
                end, x = q + n, 0
                while q < end and x < w:
                    m = self.d[q]; q += 1
                    if m & 1:
                        x += m >> 1
                    elif m & 2:
                        c = (m >> 2) + 1
                        v = self.d[q]; q += 1
                        for _ in range(c):
                            if x < w:
                                px[y * w + x] = v if v != trans else None
                            x += 1
                    else:
                        c = (m >> 2) + 1
                        for k in range(c):
                            if x < w:
                                v = self.d[q + k]
                                px[y * w + x] = v if v != trans else None
                            x += 1
                        q += c
                q = end
        else:
            raw = self.d[ptr:ptr + w * h]
            px = [None if v == trans else v for v in raw]
        return w, h, ox, oy, px


def main():
    args = sys.argv[1:]
    black = '--black' in args
    flt = None
    if '--filter' in args:
        i = args.index('--filter'); flt = args[i + 1].lower(); del args[i:i + 2]
    args = [a for a in args if a != '--black']
    gaf, pal, out = args[0], read_palette(args[1]), args[2]
    os.makedirs(out, exist_ok=True)
    index = {}
    for name, frames in GAF(gaf).sequences():
        if flt and flt not in name.lower():
            continue
        if not frames:
            continue
        # common cell: union of all frames around their origins
        left = max(f[2] for f, _ in frames); top = max(f[3] for f, _ in frames)
        right = max(f[0] - f[2] for f, _ in frames); bottom = max(f[1] - f[3] for f, _ in frames)
        cw, ch = left + right, top + bottom
        n = len(frames)
        cols = math.ceil(math.sqrt(n)); rows = math.ceil(n / cols)
        sheet = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 255 if black else 0))
        for i, ((w, h, ox, oy, px), _dur) in enumerate(frames):
            cell = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            cell.putdata([(0, 0, 0, 0) if v is None else pal[v] + (255,) for v in px])
            sheet.alpha_composite(cell, ((i % cols) * cw + left - ox, (i // cols) * ch + top - oy))
        safe = ''.join(c if c.isalnum() or c in '-_' else '_' for c in name)
        sheet.save(os.path.join(out, safe + '.png'))
        index[name] = dict(file=safe + '.png', frames=n, cols=cols, rows=rows, cell=[cw, ch], origin=[left, top],
                           ta_frame_durations=[d for _, d in frames])
    json.dump(index, open(os.path.join(out, 'index.json'), 'w'), indent=1)
    print(len(index), 'sequences ->', out)


if __name__ == '__main__':
    main()
