#!/usr/bin/env python3
"""Find holes in installed models: sight lines from outside and above whose first hit is the inside of a surface. Rays come from 12 directions at 25-65 degrees elevation
(undersides are culled on purpose, so nothing looks from below), on a 0.5 elmo grid at most. Per model: the largest connected patch seen in any view, in square elmos, and where.
Pieces are judged in the rest pose. Only patches at least 3 grid cells across count.
  python3 model_holes.py [--min 1.0] [--file path.s3o] [--view DIR] [-j 16] [stem ...]     (no stems = every unit; prints worst first)"""
import argparse, glob, math, multiprocessing, os, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # provides mathutils
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from s3okit import s3o
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DIRS = [(az, el) for el in (25, 45, 65) for az in (0, 90, 180, 270)]


def scan(f, view=None):
    m = s3o.read(f)
    verts, tris, owner = [], [], []; G = {}
    for p in m['pieces']:
        G[p['name']] = np.array(p['off'], float) + (G[p['parent']] if p['parent'] else 0)
        if p['idx']:
            o = len(verts)
            verts += [tuple(np.array(v[:3]) + G[p['name']]) for v in p['verts']]
            I = p['idx']; tris += [(I[k] + o, I[k + 1] + o, I[k + 2] + o) for k in range(0, len(I), 3)]
            owner += [p['name']] * (len(I) // 3)
    V = np.array(verts); ctr = (V.min(0) + V.max(0)) / 2; R = np.linalg.norm(V - ctr, axis=1).max()
    step = max(0.25, R * 2 / 300)
    bvh = BVHTree.FromPolygons(verts, tris, all_triangles=True, epsilon=0.0)
    best = (0.0, None, None, None); total = 0.0; imgs = []
    for az, el in DIRS:
        a, e = math.radians(az), math.radians(el)
        d = Vector((-math.cos(e) * math.sin(a), -math.sin(e), -math.cos(e) * math.cos(a)))    # travel direction
        u = d.cross(Vector((0, 1, 0))).normalized(); w = u.cross(d).normalized()
        n = int(2 * R / step) + 1
        back = np.zeros((n, n), bool); hit = np.zeros((n, n), bool); who = {}
        c0 = Vector(ctr) - d * (R + 5)
        for i in range(n):
            for j in range(n):
                o = c0 + u * (-R + i * step) + w * (-R + j * step)
                loc, nor, idx, _ = bvh.ray_cast(o, d)
                if loc is None:
                    continue
                hit[i, j] = True
                if nor.dot(d) > 0.02:
                    back[i, j] = True; who[(i, j)] = (idx, tuple(loc))
        # a real hole is an open area: this drops the one-cell outlines from sight lines grazing where plates meet a hull
        back = ndimage.binary_opening(back, structure=np.ones((3, 3), bool))
        lab, k = ndimage.label(back)
        if k:
            sizes = ndimage.sum(back, lab, range(1, k + 1)) * step * step
            total = max(total, float(back.sum() * step * step))
            b = int(np.argmax(sizes))
            if sizes[b] > best[0]:
                ii, jj = np.nonzero(lab == b + 1); mi = len(ii) // 2
                idx, loc = who[(int(ii[mi]), int(jj[mi]))]
                best = (float(sizes[b]), owner[idx], [round(x, 1) for x in loc], (az, el))
                imgs = [(hit, back, lab == b + 1, az, el)]
    if view and imgs and best[0] >= 1:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        hit, back, big, az, el = imgs[0]
        im = np.zeros(hit.shape + (3,), float) + 0.15; im[hit] = 0.7; im[back] = (1, 0.6, 0); im[big] = (1, 0, 0)
        plt.imsave(os.path.join(view, os.path.basename(f)[:-4] + '.png'), np.rot90(im))
    return os.path.basename(f)[:-4], best, total


def _job(a):
    try:
        return scan(*a)
    except Exception as e:
        return os.path.basename(a[0])[:-4], (-1, repr(e)[:60], None, None), 0


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--min', type=float, default=1.0); a.add_argument('--file'); a.add_argument('--view'); a.add_argument('-j', type=int, default=16); a.add_argument('stems', nargs='*')
    o = a.parse_args()
    if o.file:
        fs = [o.file]
    else:
        st = o.stems or [os.path.basename(f)[:-4] for f in glob.glob(os.path.join(REPO, 'units', '*.lua'))]
        fs = [os.path.join(REPO, 'objects3d', s + '.s3o') for s in st]
    if o.view:
        os.makedirs(o.view, exist_ok=True)
    with multiprocessing.Pool(o.j) as pool:
        rows = pool.map(_job, [(f, o.view) for f in fs], 1)
    rows.sort(key=lambda r: -r[1][0])
    for s, (sz, piece, loc, dr), total in rows:
        if sz >= o.min or sz < 0:
            print(f'{s} hole {sz:.1f} elmo2 (all in that view {total:.0f}) piece {piece} at {loc} view az,el {dr}')
    print('models over', o.min, sum(1 for r in rows if r[1][0] >= o.min), 'of', len(rows))
