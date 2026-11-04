#!/usr/bin/env python3
"""Find geometry floating inside one piece at rest: islands of a mesh that touch nothing on the unit. piece_gaps.py cannot see these, it treats a piece as one solid.
Islands are triangles joined by shared vertex positions. Islands join into groups within TOL across the whole model, and every group but the largest is reported.
Moving pieces are judged in their rest pose only. Wrecks and heaps are skipped.
  python3 piece_islands.py [--tol 0.6] [--file path.s3o] [--view DIR] [stem ...]    (no stems = every objects3d/*.s3o)
--view writes DIR/<stem>.png: top, side and front views of the unit in grey with each loose group in its own colour, numbered as in the printed list."""
import argparse, glob, multiprocessing, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s3okit import s3o
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def samples(tri, step=0.5):
    out = []
    for a, b, c in tri:
        n = max(1, int(max(np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)) / step))
        for i in range(n + 1):
            for j in range(n + 1 - i):
                out.append(a + (b - a) * i / n + (c - a) * j / n)
    return np.array(out)


def islands_of(p, off):
    V = np.array([v[:3] for v in p['verts']], dtype=float) + off; I = np.array(p['idx']).reshape(-1, 3)
    keys = {}; parent = list(range(len(I)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for t, tri in enumerate(I):
        for i in tri:
            k = tuple(np.round(V[i], 3))
            if k in keys:
                parent[find(t)] = find(keys[k])
            else:
                keys[k] = t
    groups = {}
    for t in range(len(I)):
        groups.setdefault(find(t), []).append(t)
    return [samples(V[I[g]]) for g in groups.values()]


def audit(f, tol, view=None):
    try:
        m = s3o.read(f)
    except Exception:
        return []
    G = {}; isl = []
    for p in m['pieces']:
        G[p['name']] = np.array(p['off'], float) + (G[p['parent']] if p['parent'] else 0)
        if p['idx']:
            isl += [(p['name'], x) for x in islands_of(p, G[p['name']])]
    if len(isl) < 2:
        return []
    comp = list(range(len(isl)))
    def cf(x):
        while comp[x] != x:
            comp[x] = comp[comp[x]]; x = comp[x]
        return x
    lo = np.array([x[1].min(0) for x in isl]) - tol; hi = np.array([x[1].max(0) for x in isl]) + tol
    trees = [cKDTree(x[1]) for x in isl]
    for i in range(len(isl)):
        for j in np.nonzero(np.all(lo[i] <= hi, 1) & np.all(lo <= hi[i], 1))[0]:
            if j > i and cf(i) != cf(j) and trees[i].query(isl[j][1], k=1, distance_upper_bound=tol)[0].min() <= tol:
                comp[cf(i)] = cf(j)
    by = {}
    for i in range(len(isl)):
        by.setdefault(cf(i), []).append(i)
    if len(by) < 2:
        return []
    main = max(by.values(), key=lambda g: sum(len(isl[i][1]) for i in g))
    mt = cKDTree(np.vstack([isl[i][1] for i in main]))
    out = []; loose = []
    for g in by.values():
        if g is main:
            continue
        pts = np.vstack([isl[i][1] for i in g])
        loose.append(pts)
        out.append(f"{os.path.basename(f)[:-4]} {'+'.join(sorted({isl[i][0] for i in g}))} gap {float(mt.query(pts)[0].min()):.2f} at {np.round((pts.min(0) + pts.max(0)) / 2, 1).tolist()} size {np.round(pts.max(0) - pts.min(0), 1).tolist()}")
    if view and loose:
        draw(view, os.path.basename(f)[:-4], np.vstack([x[1] for x in isl]), loose)
    return out


def draw(view, stem, allp, loose):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    idx = np.random.default_rng(0).permutation(len(allp))[:30000]
    for a, (i, j, name) in zip(ax, ((0, 2, 'top: x, z'), (2, 1, 'side: z, y'), (0, 1, 'front: x, y'))):
        a.scatter(allp[idx, i], allp[idx, j], s=1, c='0.75')
        for n, g in enumerate(loose):
            a.scatter(g[:, i], g[:, j], s=4, c=[plt.cm.tab10(n % 10)])
            a.annotate(str(n + 1), (g[:, i].mean(), g[:, j].mean()), color='k', weight='bold')
        a.set_aspect('equal'); a.set_title(name)
    fig.suptitle(stem); fig.tight_layout(); fig.savefig(os.path.join(view, stem + '.png'), dpi=70); plt.close(fig)


def _job(a):
    return audit(*a)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--tol', type=float, default=0.6); a.add_argument('--file'); a.add_argument('--view'); a.add_argument('stems', nargs='*'); o = a.parse_args()
    fs = [o.file] if o.file else [os.path.join(REPO, 'objects3d', s + '.s3o') for s in o.stems] or sorted(glob.glob(os.path.join(REPO, 'objects3d', '*.s3o')))
    fs = [f for f in fs if not os.path.basename(f)[:-4].endswith(('_dead', '_dead1', '_dead2')) and not (os.path.basename(f)[:1].isdigit() and 'x' in os.path.basename(f)[:3])]
    if o.view:
        os.makedirs(o.view, exist_ok=True)
    with multiprocessing.Pool(16) as pool:
        rows = [r for rs in pool.imap(_job, [(f, o.tol, o.view) for f in fs]) for r in rs]
    print('\n'.join(rows))
    print('loose groups', len(rows))
