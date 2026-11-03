#!/usr/bin/env python3
"""Find pieces that float off the unit while it animates, from a `GAP=1 tools/headless-test/run.sh` run.

    python3 piece_gaps.py /tmp/tmp.XXX/gapdata.txt [--units REGEX] [--min-gap 1.0] [--json out.json] [-j 8] [-v]

The probe (zz_piece_gap_probe) logs model-space piece matrices of every unit def in action. For each logged pose this poses the real S3O geometry:
triangle surface samples per piece (spacing scales with the unit, see spacing()), KD-tree distance between pieces, and a generalised winding number test so
a small piece buried inside a bigger hull counts as touching it (a joint inside a torso has no surface near the torso's surface). Pieces closer than the
tolerance are one component; the component with the most surface area is the unit, every other one floats. A set floating at rest too is reported as REST
(the model, not the script; ANIM only if the animation makes it worse), a set floating only in action as ANIM, with its gap (nearest surface of the unit, elmos),
when, and the Move/Turn/Spin lines that drive it.
Hidden pieces are left out, both as floaters and as bridges: LUS units report Hide/Show exactly (the probe wraps them), COB ones are read statically
from the bytecode (a COB floater that the script hides somewhere is marked `maybe-hidden`).
Limits: only what the probe exercises gets seen (no transports, no landing pads, no damage reactions); poses are every 4 frames; a gap under the tolerance is not seen.
"""
import argparse, json, multiprocessing, os, re, sys
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s3okit import s3o, cob

REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OBJ, SCR = os.path.join(REPO, 'objects3d'), os.path.join(REPO, 'scripts')


def parse(path):
    units, phases = {}, []
    cur = None
    for raw in open(path):
        for rec in raw.rstrip('\n').split(';'):
            f = rec.split()
            if not f:
                continue
            t = f[0]
            if t == 'M' and cur is not None:
                cur[1][int(f[1])] = (int(f[2]), [float(x) for x in f[3:]])
            elif t == 'S':
                cur = (int(f[2]), {})
                units[f[1]]['samples'].append(cur)
            elif t == 'U':
                units[f[1]] = dict(name=f[2], model=f[3], pieces={}, parents={}, samples=[], died=None)
            elif t == 'P':
                units[f[1]]['pieces'][int(f[2])] = f[3]
                units[f[1]]['parents'][int(f[2])] = f[4]
            elif t == 'F':
                phases.append((int(f[1]), f[2]))
            elif t == 'D':
                units[f[1]]['died'] = int(f[2])
    return units, phases


def phase_at(phases, frame):
    name = phases[0][1] if phases else '?'
    for fr, ph in phases:
        if frame >= fr:
            name = ph
    return name


def spacing(total_area):
    return float(np.clip((total_area / 25000.0) ** 0.5, 0.35, 3.0))


class Piece:
    def __init__(self, name, parent, off, verts, idx):
        self.name, self.parent, self.off = name, parent, np.array(off, float)
        self.has = len(idx) >= 3
        if not self.has:
            return
        v = np.array([x[:3] for x in verts], float)
        t = v[np.array(idx).reshape(-1, 3)]
        self.tris = t
        a = np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1) / 2
        keep = a > 1e-9
        self.tris, self.area = t[keep], a[keep]
        self.has = len(self.tris) > 0
        if not self.has:
            return
        self.total = float(self.area.sum())

    def sample(self, s, rng):
        t, a = self.tris, self.area
        n = np.minimum(np.ceil(a / (s * s)).astype(int), 4000)
        pts = [np.vstack([t[:, 0], t[:, 1], t[:, 2]])]
        i = np.repeat(np.arange(len(t)), n)
        u, w = rng.random(len(i)), rng.random(len(i))
        fl = u + w > 1
        u[fl], w[fl] = 1 - u[fl], 1 - w[fl]
        pts.append(t[i, 0] + u[:, None] * (t[i, 1] - t[i, 0]) + w[:, None] * (t[i, 2] - t[i, 0]))
        self.pts = np.unique(np.round(np.vstack(pts), 3), axis=0)
        self.tree = cKDTree(self.pts)
        self.c = (self.pts.max(0) + self.pts.min(0)) / 2
        self.r = float(np.linalg.norm(self.pts - self.c, axis=1).max())
        self.size = (self.pts.max(0) - self.pts.min(0)).round(1).tolist()


def winding(q, tris):
    """generalised winding number of points q (n,3) against triangles (m,3,3) (van Oosterom & Strackee)"""
    a, b, c = (tris[:, i][None] - q[:, None] for i in range(3))
    la, lb, lc = (np.linalg.norm(x, axis=2) for x in (a, b, c))
    det = np.einsum('ijk,ijk->ij', a, np.cross(b, c))
    den = la * lb * lc + np.einsum('ijk,ijk->ij', a, b) * lc + np.einsum('ijk,ijk->ij', b, c) * la + np.einsum('ijk,ijk->ij', c, a) * lb
    return np.abs(np.arctan2(det, den).sum(1)) / (2 * np.pi)


def lua_lines(stem):
    p = os.path.join(SCR, stem + '.lua')
    return open(p, errors='replace').read().split('\n') if os.path.exists(p) else None


NUM = r'(-?\d+(?:\.\d+)?)'
def drivers(lines, name, kind_axis_val):
    """script lines that Move/Turn/Spin this piece, those nearest the measured value first"""
    out = []
    for n, l in enumerate(lines, 1):
        code = l.split('--')[0]
        for m in re.finditer(r'\b(Move|Turn|Spin)\(\s*%s\s*,\s*(x|y|z)_axis\s*,\s*([^;]*)' % re.escape(name), code):
            k, ax, rest = m.group(1), m.group(2), m.group(3)
            v = re.search(NUM, rest)
            val = float(v.group(1)) if v else None
            score = 1e9
            if val is not None and k in ('Move', 'Turn') and k in kind_axis_val:
                score = abs(val - kind_axis_val[k]['xyz'.index(ax)])
                if k == 'Move' and abs(kind_axis_val[k]['xyz'.index(ax)]) < 0.05:
                    score = 1e8
                if k == 'Turn' and abs(kind_axis_val[k]['xyz'.index(ax)]) < 0.5:
                    score = 1e8
            elif k == 'Spin':
                score = 1e7
            out.append((score, n, l.strip()[:90]))
    out.sort(key=lambda x: (x[0], x[1]))
    return out[:3]


def euler(R):
    return np.degrees([np.arctan2(R[2, 1], R[2, 2]), np.arcsin(np.clip(-R[2, 0], -1, 1)), np.arctan2(R[1, 0], R[0, 0])])


def analyse(args):
    u, phases, opts = args
    stem = os.path.splitext(os.path.basename(u['model']))[0]
    res = dict(name=u['name'], stem=stem, lang='?', events=[], samples=len(u['samples']), died=u['died'])
    path = os.path.join(OBJ, u['model'])
    if not u['model'].lower().endswith('.s3o') or not os.path.exists(path):
        res['skip'] = 'no s3o'
        return res
    m = s3o.read(path)
    P = {p['name'].lower(): Piece(p['name'].lower(), p['parent'].lower() if p['parent'] else None, p['off'], p['verts'], p['idx']) for p in m['pieces']}
    geo = [p for p in P.values() if p.has]
    if len(geo) < 2:
        res['skip'] = 'one piece'
        return res
    s = spacing(sum(p.total for p in geo))
    tol = max(s * 1.6, 0.6)
    res['spacing'], res['tol'] = round(s, 2), round(tol, 2)
    rng = np.random.default_rng(0)
    for p in geo:
        p.sample(s, rng)
    lua = lua_lines(stem)
    res['lang'] = 'lua' if lua is not None else 'cob'
    maybe_hidden = set()
    if lua is None:
        for ext in ('.COB', '.cob'):
            cp = os.path.join(SCR, stem + ext)
            if os.path.exists(cp):
                c = cob.read(cp)
                for ins in c['scripts'].values():
                    for nm, ops in ins:
                        if nm == 'hide' and ops and 0 <= ops[0] < len(c['pieces']):
                            maybe_hidden.add(c['pieces'][ops[0]].lower())
                break
    # rest pose from the file
    def rest_world():
        out = {}
        for n, p in P.items():
            t, q = np.zeros(3), p
            while q is not None:
                t = t + q.off
                q = P.get(q.parent) if q.parent else None
            out[n] = (np.eye(3), t)
        return out
    cache = {}
    def rel(a, b, ma, mb):
        Ra, ta = ma; Rb, tb = mb
        R = Ra.T @ Rb
        t = Ra.T @ (tb - ta)
        return R, t
    def pair(a, b, ma, mb, need_dist=False):
        """(touching, distance or None); a and b Piece"""
        if a.name > b.name:
            a, b, ma, mb = b, a, mb, ma
        R, t = rel(a, b, ma, mb)
        key = (a.name, b.name, tuple(np.round(R.ravel(), 2)), tuple(np.round(t, 1)))
        e = cache.get(key)
        if e is None:
            e = {}
            cache[key] = e
        if 'touch' not in e:
            cb = R @ b.c + t
            d0 = np.linalg.norm(cb - a.c)
            if d0 - a.r - b.r > tol:
                e['touch'] = False
                e['far'] = float(d0 - a.r - b.r)
            else:
                # transform the smaller cloud into the frame of the bigger one
                if len(a.pts) >= len(b.pts):
                    d, _ = a.tree.query(b.pts @ R.T + t, k=1)
                    e['dist'] = float(d.min())
                else:
                    d, _ = b.tree.query((a.pts - t) @ R, k=1)
                    e['dist'] = float(d.min())
                e['touch'] = e['dist'] <= tol
                if not e['touch']:
                    rngw = np.random.default_rng(1)
                    pa = b.pts @ R.T + t
                    sa = pa if len(pa) < 48 else pa[rngw.choice(len(pa), 48, replace=False)]
                    pb = a.pts
                    sb = pb if len(pb) < 48 else pb[rngw.choice(len(pb), 48, replace=False)]
                    sb2 = (sb - t) @ R
                    inside = False
                    if len(a.tris) < 6000 and (winding(sa, a.tris) > 0.5).any():
                        inside = True
                    if not inside and len(b.tris) < 6000 and (winding(sb2, b.tris) > 0.5).any():
                        inside = True
                    e['touch'] = inside
        if need_dist and 'dist' not in e:
            if len(a.pts) >= len(b.pts):
                d, _ = a.tree.query(b.pts @ R.T + t, k=1)
            else:
                d, _ = b.tree.query((a.pts - t) @ R, k=1)
            e['dist'] = float(d.min())
        return e['touch'], e.get('dist')

    def components(world, visible):
        nodes = [p for p in geo if p.name in visible]
        idx = {p.name: i for i, p in enumerate(nodes)}
        par = list(range(len(nodes)))
        def find(i):
            while par[i] != i:
                par[i] = par[par[i]]; i = par[i]
            return i
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                ia, ib = find(i), find(idx[b.name])
                if ia == ib:
                    continue
                if pair(a, b, world[a.name], world[b.name])[0]:
                    par[ia] = ib
        comps = {}
        for i, p in enumerate(nodes):
            comps.setdefault(find(i), []).append(p)
        comps = sorted(comps.values(), key=lambda c: -sum(p.total for p in c))
        return comps

    def gap_of(comp, main, world):
        best, wa, wb = 1e9, None, None
        for a in comp:
            for b in main:
                _, d = pair(a, b, world[a.name], world[b.name], need_dist=True)
                if d < best:
                    best, wa, wb = d, a.name, b.name
        return best, wa, wb

    rest = rest_world()
    allvis = {p.name for p in geo}
    rest_comps = components(rest, allvis)
    rest_float = {}
    for c in rest_comps[1:]:
        k = frozenset(p.name for p in c)
        rest_float[k] = gap_of(c, rest_comps[0], rest)[0]
    res['rest_floaters'] = [dict(pieces=sorted(k), gap=round(v, 2)) for k, v in rest_float.items()]

    # replay
    world = dict(rest)
    vis = dict.fromkeys(P, True)
    seen = {}
    n2i = {v: k for k, v in u['pieces'].items()}
    keyf = None
    for frame, changes in u['samples']:
        for i, (v, a) in changes.items():
            name = u['pieces'].get(i, '').lower()
            if name in P:
                R = np.array([a[0:3], a[3:6], a[6:9]]).T
                world[name] = (R, np.array(a[9:12]))
                vis[name] = bool(v)
        visible = {p.name for p in geo if vis[p.name]}
        k2 = tuple(sorted((n, tuple(np.round(world[n][0].ravel(), 2)), tuple(np.round(world[n][1], 1))) for n in visible))
        if k2 == keyf:
            continue
        keyf = k2
        comps = components(world, visible)
        if len(comps) < 2:
            continue
        for c in comps[1:]:
            k = frozenset(p.name for p in c)
            g, wa, wb = gap_of(c, comps[0], world)
            e = seen.get(k)
            if e is None:
                e = seen[k] = dict(k=k, first=frame, last=frame, count=0, gap=-1, frame=frame, near=None, phases=set(), world=None)
            e['last'] = frame; e['count'] += 1; e['phases'].add(phase_at(phases, frame))
            if g > e['gap']:
                e.update(gap=g, frame=frame, near=(wa, wb), world=dict(world))
    for k, e in seen.items():
        cls = 'ANIM'
        if k in rest_float:
            if e['gap'] <= rest_float[k] + tol:
                cls = 'REST'
        if e['gap'] < opts['min_gap']:
            continue
        # the chain from the floating piece's root up to the unit's root that moved at the worst moment
        drv, seen_c = [], set()
        for n in sorted(k):
            q = P[n]
            while q is not None and q.name not in seen_c:
                seen_c.add(q.name)
                par = P.get(q.parent) if q.parent else None
                Rw, tw = e['world'][q.name]
                if par is not None:
                    Rp, tp = e['world'][par.name]
                    Rl = Rp.T @ Rw
                    dl = Rp.T @ (tw - tp) - q.off
                else:
                    Rl = Rw; dl = tw - q.off
                ang = euler(Rl)
                if np.abs(dl).max() > 0.05 or np.abs(ang).max() > 0.5:
                    # engine model-space matrices: compare to script values (rad) in degrees; move in elmos
                    d = dict(piece=q.name, move=[round(float(x), 2) for x in dl], turn=[round(float(x), 1) for x in ang])
                    if lua is not None:
                        d['lines'] = [dict(line=x[1], code=x[2]) for x in drivers(lua, q.name, {'Move': d['move'], 'Turn': d['turn']})]
                    drv.append(d)
                q = par
        res['events'].append(dict(cls=cls, pieces=sorted(k), gap=round(e['gap'], 2), gap_rest=round(rest_float.get(k, 0), 2), frame=e['frame'], first=e['first'], last=e['last'],
                                  samples=e['count'], phases=sorted(e['phases'], key=lambda p: [x[1] for x in phases].index(p) if p in [x[1] for x in phases] else 99),
                                  nearest=e['near'], size=[P[n].size for n in sorted(k)], maybe_hidden=sorted(k & maybe_hidden), drivers=drv))
    res['events'].sort(key=lambda e: -e['gap'])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data')
    ap.add_argument('--units', default='')
    ap.add_argument('--min-gap', type=float, default=1.0, help='report floaters whose gap exceeds this many elmos')
    ap.add_argument('--json')
    ap.add_argument('-j', type=int, default=8)
    ap.add_argument('-v', action='store_true', help='also list the driving script lines')
    a = ap.parse_args()
    units, phases = parse(a.data)
    rx = re.compile(a.units, re.I)
    work = [(u, phases, dict(min_gap=a.min_gap)) for u in units.values() if rx.search(u['name'])]
    if a.j > 1:
        with multiprocessing.Pool(a.j) as pool:
            out = pool.map(analyse, work, chunksize=1)
    else:
        out = [analyse(w) for w in work]
    out.sort(key=lambda r: -(r['events'][0]['gap'] if r['events'] else 0))
    nb = 0
    for r in out:
        if not r['events']:
            continue
        nb += 1
        print(f"{r['stem']} [{r['lang']}] tol {r.get('tol')} samples {r['samples']}")
        for e in r['events']:
            mh = ' maybe-hidden:' + ','.join(e['maybe_hidden']) if e['maybe_hidden'] else ''
            print(f"  {e['cls']} gap {e['gap']} (rest {e['gap_rest']}) {'+'.join(e['pieces'])} size {e['size'][0]} near {e['nearest'][1]} @f{e['frame']} ({','.join(e['phases'])}, {e['samples']} poses f{e['first']}-{e['last']}){mh}")
            if a.v:
                for d in e['drivers']:
                    print(f"      {d['piece']} move {d['move']} turn {d['turn']}")
                    for l in d.get('lines', []):
                        print(f"        L{l['line']}: {l['code']}")
    print(f"--- {nb} of {len(out)} units float (gap > {a.min_gap}); skipped: {[r['stem'] for r in out if r.get('skip')]}")
    if a.json:
        json.dump(out, open(a.json, 'w'), indent=1)


if __name__ == '__main__':
    main()
