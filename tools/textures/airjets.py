#!/usr/bin/env python3
"""Thruster flames for TA:Recoil aircraft (Airjets GL4 / LUPS AirJet entries), from the models' exhaust vectors.

  airjets.py [--report]

TA models mark exhausts with "vector" pieces: two vertices and no faces, named like an exhaust (thrust, jet, exhaust,
engine, burner, nozzle; "flare" pieces are gun muzzles, "wake" pieces are water wakes). The piece origin is usually the
model centre; the two vertices carry the real position and direction, in either order. So for each vector:
  * direction: a mostly vertical vector blows down, a mostly lengthwise one blows backward (-z);
  * nozzle: where the vector leaves the hull, found by casting from its outer end back along it against the model's
    faces (rest pose), else its inner end;
  * the jet gets `pos` = nozzle in the piece's space (S3O pieces carry no rest rotation), so it moves with the piece
    when the script turns it (Atlas/Valkyrie nacelles).
Models without usable vectors get hand placement in MANUAL (Thunder: its four engine pods, which stand upright when
landed and swing back in flight). MIRROR adds the missing twin of a one-sided vector (Arm Constructor).
Nozzles the model has no vectors for get NOZZLES: a hand-read nozzle centre, cast onto the hull from behind (or from
below) to find the nozzle face and the piece it belongs to, so the jet follows that piece (wings that slide out).
Arm jets are blue-white, Core jets orange (matching the unit lights); size from the model. Jets only show while the
aircraft is active (flying).
Writes luaui/configs/lupsunitfxs_ta.lua, merged into effectUnitDefs by lupsunitfxs.lua.
"""
import argparse, glob, os, re, struct
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'luaui', 'configs', 'lupsunitfxs_ta.lua')
EXHAUST = re.compile(r'thrust|jet|exhaust|engine|burner|nozzle', re.I)
COLORS = {'arm': (0.55, 0.75, 1.0, 0.8), 'core': (1.0, 0.55, 0.15, 0.8)}

# unit -> [(piece, pos in piece space, emit vector, width or None)]; replaces the vectors found in the model
MANUAL = {
    # engine pods on the 'jets' piece (piece space): exhausts at their lower ends; the piece turns 90 deg about x in
    # flight, which swings the pods' downward axis to point backward
    'arm_t1_air_thunder': [('jets', (x, -7.7, 0.1), (0, -1, 0), 2.6) for x in (-17.6, -10.0, 10.0, 18.0)],
}
# unit -> nozzles read off the model (rear/bottom views): ('rear', x, y) blows backward from the hull face behind
# (x, y); ('down', x, z) blows down from the hull face under (x, z). Entries with x != 0 are mirrored to -x.
NOZZLES = {
    'arm_t1_air_peeper': [('rear', 0, 4.5)],
    'arm_t2_air_eagle': [('rear', 0, 3.3), ('rear', 14.5, 3.5)],
    'arm_t2_air_seahawk': [('rear', 7.5, 7.8)],
    'arm_t2_air_advancedconstructor': [('rear', 2.8, 6.8), ('down', 11.9, 14.5), ('down', 11.9, -14.5)],
    'core_t2_air_hunter': [('rear', 3.4, 3.6)],
    'core_t2_air_vulture': [('rear', 7.0, 3.0)],
    'core_t2_air_hurricane': [('rear', 0, 3.5), ('rear', 10.0, 6.6)],   # its vectors only cover the belly jets
    'arm_t1_seapl_albatross': [('rear', 6.7, 3.2)],
    'arm_t1_seapl_constructor': [('rear', 4.5, 13.0)],
    'arm_t1_seapl_tornado': [('rear', 6.5, 3.3)],
    'core_t1_seapl_constructor': [('rear', 0, 6.2)],
    'core_t1_seapl_typhoon': [('rear', 6.8, 3.3)],
    'core_t1_seapl_voodoo': [('rear', 4.8, 3.9)],
}
# unit -> vector pieces whose jet is copied to the other side (x mirrored): the model has two nozzles, one vector
MIRROR = {
    'arm_t1_air_constructor': ['rearthrust'],
}


def flag(s, k):
    return bool(re.search(r'\b%s\s*=\s*(true|1)\b' % k, s, re.I))


def num(s, k):
    m = re.search(r'\b%s\s*=\s*([\d.]+)' % k, s, re.I)
    return float(m.group(1)) if m else 0.0


def read_s3o(path):
    """-> pieces: name, origin (model space, rest pose), local verts (n,3), model-space triangles (t,3,3)."""
    d = open(path, 'rb').read()
    assert d.startswith(b'Spring unit')
    root, = struct.unpack_from('<i', d, 36)
    rd = lambda o: d[o:d.index(b'\0', o)].decode('latin-1') if o else ''
    pieces = []

    def piece(off, base):
        name_o, nch, ch_o, nv, v_o, vtype, prim, nidx, idx_o, coll, ox, oy, oz = struct.unpack_from('<iiiiiiiiiifff', d, off)
        origin = base + np.array([ox, oy, oz])
        v = np.frombuffer(d, np.float32, nv * 8, v_o).reshape(nv, 8)[:, 0:3].astype(float) if nv else np.zeros((0, 3))
        idx = np.frombuffer(d, np.int32, nidx, idx_o) if nidx else np.zeros(0, np.int32)
        if prim == 0:
            tris = idx[: len(idx) // 3 * 3].reshape(-1, 3)
        elif prim == 2:  # quads
            q = idx[: len(idx) // 4 * 4].reshape(-1, 4)
            tris = np.concatenate([q[:, [0, 1, 2]], q[:, [0, 2, 3]]])
        else:            # triangle strips
            tris = np.array([(idx[i], idx[i + 1], idx[i + 2]) for i in range(len(idx) - 2)
                             if len({idx[i], idx[i + 1], idx[i + 2]}) == 3], np.int32).reshape(-1, 3)
        pieces.append(dict(name=rd(name_o), origin=origin, verts=v, tris=(v + origin)[tris] if len(tris) else None))
        for c in struct.unpack_from('<%di' % nch, d, ch_o) if nch else ():
            piece(c, origin)
    piece(root, np.zeros(3))
    return pieces


def first_hit(o, e, tris, index=False):
    """Smallest t in (0, 1] where segment o->e crosses a triangle (Moller-Trumbore), or None; index: (t, triangle)."""
    dvec = e - o
    v0, e1, e2 = tris[:, 0], tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    p = np.cross(dvec, e2)
    det = np.einsum('ij,ij->i', e1, p)
    ok = np.abs(det) > 1e-9
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    s = o - v0
    u = np.einsum('ij,ij->i', s, p) * inv
    q = np.cross(s, e1)
    v = (q @ dvec) * inv
    t = np.einsum('ij,ij->i', e2, q) * inv
    hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-4) & (t <= 1)
    if not hit.any():
        return (None, None) if index else None
    i = int(np.where(hit, t, np.inf).argmin())
    return (float(t[i]), i) if index else float(t[i])


def cast_nozzles(uname, pieces, hull, owner, width):
    """-> [(piece, pos in piece space, emit, width)] for the hand-read NOZZLES of a unit."""
    out = []
    for kind, a, b in NOZZLES[uname]:
        for x in ((a, -a) if a else (a,)):
            if kind == 'rear':
                o, e, emit, w = np.array([x, b, -500.0]), np.array([x, b, 500.0]), (0, 0, -1), width * 0.85
            else:
                o, e, emit, w = np.array([x, -500.0, b]), np.array([x, 500.0, b]), (0, -1, 0), width
            t, i = first_hit(o, e, hull, index=True)
            if t is None:
                raise SystemExit('%s: no hull behind/under nozzle %s %s,%s' % (uname, kind, x, b))
            p = pieces[owner[i]]
            out.append((p['name'], o + t * (e - o) - p['origin'], emit, w))
    return out


def exhaust_jets(pieces, hull):
    """-> [(piece, model-space nozzle, emit vector)] from the model's exhaust vectors."""
    out = []
    for p in pieces:
        n = p['name']
        if len(p['verts']) != 2 or p['tris'] is not None or not EXHAUST.search(n) or re.search('flare|wake', n, re.I):
            continue
        a, b = p['verts'] + p['origin']
        axis = int(np.argmax(np.abs(b - a)))
        if axis == 0:        # sideways: not an exhaust
            continue
        emit = (0, -1, 0) if axis == 1 else (0, 0, -1)
        outer, inner = (a, b) if a[axis] < b[axis] else (b, a)   # both blow toward -y / -z
        t = first_hit(outer, inner, hull)
        nozzle = inner if t is None else outer + t * (inner - outer)
        out.append((n, nozzle, emit))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'units', '*.lua'))):
        s = open(f).read()
        if not flag(s, 'canfly'):
            continue
        uname = os.path.splitext(os.path.basename(f))[0].lower()
        obj = re.search(r'objectname\s*=\s*"([^"]+)"', s, re.I).group(1).split('/')[-1]
        pieces = read_s3o(os.path.join(ROOT, 'objects3d', obj))
        byname = {p['name']: p for p in pieces}
        meshes = [p['tris'] for p in pieces if p['tris'] is not None]
        if not meshes:
            continue
        hull = np.concatenate(meshes)
        owner = np.concatenate([np.full(len(p['tris']), k) for k, p in enumerate(pieces) if p['tris'] is not None])
        allv = hull.reshape(-1, 3)
        size = float(np.linalg.norm(allv.max(0) - allv.min(0)))       # model diagonal, elmos
        width = float(np.clip(size * 0.06, 2.5, 6))
        length = round(float(np.clip(size * 0.45, 14, 45)))

        entries = []   # (piece, pos in piece space, emit, width)
        if uname in MANUAL:
            for piece, pos, emit, w in MANUAL[uname]:
                entries.append((piece, np.array(pos, float), emit, w or width))
        else:
            for piece, nozzle, emit in exhaust_jets(pieces, hull):
                w = width * (1.0 if emit[1] else 0.85)
                origin = byname[piece]['origin']
                entries.append((piece, nozzle - origin, emit, w))
                if piece in MIRROR.get(uname, ()):
                    entries.append((piece, nozzle * (-1, 1, 1) - origin, emit, w))
            if uname in NOZZLES:
                entries += cast_nozzles(uname, pieces, hull, owner, width)
        if not entries:
            continue
        col = COLORS['arm' if uname.startswith('arm') else 'core']
        out[uname] = (col, length, entries)
        if a.report:
            print('%-34s %s' % (uname, ', '.join('%s@(%.1f,%.1f,%.1f)%s' % (pc, *(pos + byname[pc]['origin']), 'v' if e[1] else '')
                                                for pc, pos, e, _ in entries)))
    with open(OUT, 'w', newline='\n') as f:
        f.write('-- GENERATED by tools/textures/airjets.py: thruster flames on the exhaust vectors of TA:Recoil aircraft.\n'
                '-- pos = nozzle in piece space (vector pieces sit at the model centre; their vertices mark the exhaust).\n'
                '-- Merged into effectUnitDefs by lupsunitfxs.lua; hand-made entries there win.\n'
                'return {\n')
        for uname in sorted(out):
            col, length, entries = out[uname]
            f.write('\t%s = {\n' % uname)
            for piece, pos, v, w in entries:
                pos = [round(float(c), 1) + 0.0 for c in pos]
                f.write("\t\t{class='AirJet', options={color={%s,%s,%s,%s}, width=%s, length=%d, piece=\"%s\", "
                        "pos={%s, %s, %s}, onActive=true, emitVector={%d, %d, %d}}},\n"
                        % (col[0], col[1], col[2], col[3], round(w, 1), length, piece, pos[0], pos[1], pos[2], v[0], v[1], v[2]))
            f.write('\t},\n')
        f.write('}\n')
    print('%d aircraft with jets -> %s' % (len(out), os.path.relpath(OUT, ROOT)))


if __name__ == '__main__':
    main()
