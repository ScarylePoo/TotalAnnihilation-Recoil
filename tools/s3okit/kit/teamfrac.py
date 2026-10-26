"""Top-view team-colour fraction of an exported unit in its preview pose (readability rule: 15-25 %).
usage: python3 teamfrac.py <stem> [<work dir>]      (from the kit dir; after `export`)
Rasterises the posed S3O from straight above, keeps the top-most surface per cell, samples tex1 alpha there."""
import sys, os, math, importlib.util
import numpy as np
from PIL import Image
sys.path.insert(0, '.')
from s3okit import s3o as S3O

stem = sys.argv[1]
WD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.environ.get('S3OKIT_WORK', 'work'), stem)
spec = importlib.util.spec_from_file_location('spec', f'units/{stem}.py'); mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
pose = {n.lower(): v for n, v in mod.UNIT.get('preview_pose', {}).items()}
m = S3O.read(os.path.join(WD, 'out', stem + '.s3o'))
tex = np.asarray(Image.open(os.path.join(WD, 'out', stem + '_1.png')).convert('RGBA')).astype(np.float32) / 255
H, W = tex.shape[:2]


def rot(deg):
    a, b, c = [math.radians(d) for d in deg]
    X = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Y = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Z = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Z @ Y @ X


mats = {}
for p in m['pieces']:
    M = np.eye(4); off = np.array(p['off'], float); R = np.eye(3)
    q = pose.get(p['name'])
    if q == 'hide':
        mats[p['name']] = None; continue
    if isinstance(q, dict):
        off = off + np.array(q.get('move', (0, 0, 0))); R = rot(q.get('rot', (0, 0, 0)))
    elif q:
        R = rot(q)
    M[:3, :3] = R; M[:3, 3] = off
    par = mats.get(p['parent']) if p['parent'] else np.eye(4)
    mats[p['name']] = None if (p['parent'] and par is None) else par @ M
tris = []
for p in m['pieces']:
    M = mats[p['name']]
    if M is None or not p['idx']:
        continue
    V = np.array([v[:3] for v in p['verts']]); UV = np.array([(v[6], v[7]) for v in p['verts']])
    Vw = (M[:3, :3] @ V.T).T + M[:3, 3]
    I = np.array(p['idx']).reshape(-1, 3)
    for t in I:
        tris.append((Vw[t], UV[t]))
allv = np.concatenate([t[0] for t in tris])
x0, x1 = allv[:, 0].min(), allv[:, 0].max(); z0, z1 = allv[:, 2].min(), allv[:, 2].max()
res = 0.15
nx, nz = int((x1 - x0) / res) + 1, int((z1 - z0) / res) + 1
depth = np.full((nz, nx), -1e9); team = np.zeros((nz, nx)); cov = np.zeros((nz, nx), bool)
gx = x0 + np.arange(nx) * res; gz = z0 + np.arange(nz) * res
for P, UV in tris:
    a, b, c = P[:, [0, 2]]
    den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    if abs(den) < 1e-9:
        continue
    lo = np.floor((P[:, [0, 2]].min(0) - [x0, z0]) / res).astype(int); hi = np.ceil((P[:, [0, 2]].max(0) - [x0, z0]) / res).astype(int)
    lo = np.maximum(lo, 0); hi = np.minimum(hi, [nx - 1, nz - 1])
    if (hi < lo).any():
        continue
    X, Z = np.meshgrid(gx[lo[0]:hi[0] + 1], gz[lo[1]:hi[1] + 1])
    w0 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Z - c[1])) / den
    w1 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Z - c[1])) / den
    w2 = 1 - w0 - w1
    ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
    if not ins.any():
        continue
    y = w0 * P[0, 1] + w1 * P[1, 1] + w2 * P[2, 1]
    u = w0 * UV[0, 0] + w1 * UV[1, 0] + w2 * UV[2, 0]; v = w0 * UV[0, 1] + w1 * UV[1, 1] + w2 * UV[2, 1]
    sl = (slice(lo[1], hi[1] + 1), slice(lo[0], hi[0] + 1))
    d = depth[sl]; upd = ins & (y > d)
    px = np.clip((u * W).astype(int), 0, W - 1); py = np.clip(((1 - v) * H).astype(int), 0, H - 1)
    al = tex[py, px, 3]
    d[upd] = y[upd]; team[sl][upd] = al[upd]; cov[sl][upd] = True
print(f'{stem}: top-view team fraction {team[cov].mean() * 100:.1f} %  (span x {x1 - x0:.1f}, z {z1 - z0:.1f})')
