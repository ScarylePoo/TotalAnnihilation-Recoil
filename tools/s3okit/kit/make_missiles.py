#!/usr/bin/env python3
"""Vertical-launch (StarburstLauncher) missiles: the projectile matches the missile the unit raises, and the exhaust
comes out of its tail.

  python3 make_missiles.py [--check]

The engine draws a missile projectile's model with its +Z along the flight direction and puts the flame, smoke trail
and CEG at the model ORIGIN; the projectile starts at the fire point, which is vertex 0 of the piece QueryWeapon
returns (s3okit/s3o.py). So for every unit in MISSILES (a remodelled unit whose script raises a missile piece and
hides it on launch):
  * objects3d/<Unit>_Missile.s3o is written from that piece's mesh (same UVs and textures as the unit), turned so the
    nose is +Z, with the origin on the axis at the TAIL;
  * the unit S3O's missile pieces get emit vertices tail (v0) and nose (v1), so the projectile appears exactly where
    the raised missile was hidden. The same values are in each unit spec (units/<Unit>.py skeleton_opts emit) so a
    re-export keeps them; --check verifies the two agree.
Units that launch from a hidden point (no missile piece) keep their old 3DO projectile; OLD_3DO re-origins those so
the origin is at the tail of the missile body (the flare pieces some carry stay behind it).
Weapons/*.lua name the projectile models; the scripts' QueryWeapon must return the missile piece.
"""
import argparse, os, re, struct, sys
import numpy as np

KIT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(KIT, '..', '..', '..'))
OBJ = os.path.join(ROOT, 'objects3d')
sys.path.insert(0, KIT)
from s3okit import s3o  # noqa: E402

# unit -> (missile pieces (the first is the projectile's mesh), missile axis in piece space: nose toward +axis)
MISSILES = {
    'ARM_T2_VEH_Merl': (['rocket'], 'z'),
    'ARM_T2_SEA_Ranger': (['rocket1', 'rocket2'], 'z'),
    'CORE_T2_SEA_MissileFrigate': (['rocket1', 'rocket2'], 'z'),
    'CORE_T2_VEH_Diplomat': (['missle'], 'z'),
    'ARM_T2_DEF_Retaliator': (['missile'], 'z'),
    'CORE_T2_DEF_Silencer': (['nuke'], 'y'),
    'ARM_T2_DEF_Stunner': (['dummy'], 'y'),
    'CORE_T2_DEF_Neutron': (['riser'], 'y'),
    'ARM_T2_DEF_Protector': (['rocket1', 'rocket2', 'rocket3'], 'y'),
    'CORE_T2_DEF_FortitudeMissileDefense': (['dummy'], 'y'),
}
# 3DO projectiles of units without a missile piece: (model, body piece) -> origin moved to the body's tail
OLD_3DO = [('BOTA_ARM_Hover_Rocket', 'Missle'), ('cormhmsl', 'cormhmsl'), ('corkbmissl1', 'Weapon'),
           ('BOTA_Anti_Nuclear_Missile', 'rocket')]

# piece space -> projectile space (nose along +Z)
ROT = {'z': np.eye(3), 'y': np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)}   # y -> z, z -> -y


def piece_vertex_offsets(path):
    """name -> file offset of the piece's vertex array"""
    d = open(path, 'rb').read()
    root, = struct.unpack_from('<i', d, 36)
    out = {}

    def walk(o):
        nm, nch, cho, nv, vo = struct.unpack_from('<5i', d, o)
        out[d[nm:d.index(b'\0', nm)].decode()] = vo
        for i in range(nch):
            walk(struct.unpack_from('<i', d, cho + 4 * i)[0])
    walk(root)
    return out


def tail_nose(piece, axis):
    """piece-local tail and nose points on the missile's axis"""
    V = np.array([v[:3] for v in piece['verts']], float)[sorted(set(piece['idx']))]
    a = 'xyz'.index(axis)
    lo, hi = V.min(0), V.max(0)
    mid = (lo + hi) / 2
    tail, nose = mid.copy(), mid.copy()
    tail[a], nose[a] = lo[a], hi[a]
    return tail, nose


def do_unit(unit, pieces, axis, check):
    path = os.path.join(OBJ, unit + '.s3o')
    m = s3o.read(path)
    by = {p['name']: p for p in m['pieces']}
    first = by[pieces[0]]
    tail, nose = tail_nose(first, axis)
    emits = {}
    for n in pieces:
        p = by[n]
        t, s = tail_nose(p, axis)
        used = set(p['idx'])
        assert 0 not in used and 1 not in used, f'{unit}.{n}: vertices 0/1 are mesh vertices, not emit points'
        emits[n] = (t, s)
    spec = open(os.path.join(KIT, 'units', unit + '.py')).read().lower()   # spec keys use the ref model's case
    for n, (t, s) in emits.items():
        want = '%r: [%s, %s]' % (n, fmt(t), fmt(s))
        if want not in spec:
            print(f'  ! units/{unit}.py skeleton_opts emit should have  {want}')
    if check:
        return
    # unit S3O: emit vertices tail, nose (v0, v1), in place
    data = bytearray(open(path, 'rb').read())
    vofs = piece_vertex_offsets(path)
    for n, (t, s) in emits.items():
        struct.pack_into('<3f', data, vofs[n], *t)
        struct.pack_into('<3f', data, vofs[n] + 32, *s)
    open(path, 'wb').write(data)
    # projectile S3O from the first missile piece
    R = ROT[axis]
    verts = []
    for v in first['verts']:
        p = R @ (np.array(v[:3]) - tail)
        nrm = R @ np.array(v[3:6])
        verts.append(tuple(float(c) for c in (*p, *nrm, v[6], v[7])))
    out = os.path.join(OBJ, unit + '_Missile.s3o')
    r = s3o.write(out, [dict(name='missile', parent=None, off=(0.0, 0.0, 0.0), gpos=(0.0, 0.0, 0.0),
                             verts=verts, idx=list(first['idx']))], m['tex1'], m['tex2'])
    print('%-38s %s  tail %s  length %.1f  -> %s' % (unit, ','.join(pieces), fmt(tail), np.linalg.norm(nose - tail),
                                                    os.path.relpath(out, ROOT)), r['tris'], 'tris')


def fmt(p):
    return '(%s)' % ', '.join('%.2f' % (c + 0.0) for c in p)


def do_3do(model, body, check):
    """move the origin to the tail of the body piece: root offset folded in, everything shifted by -tail"""
    path = os.path.join(OBJ, model + '.3do')
    d = bytearray(open(path, 'rb').read())
    hdr = '<13i'
    ver, nv, npr, sel, x, y, z, on, _0, ov, op, osib, ochild = struct.unpack_from(hdr, d, 0)
    name = d[on:d.index(b'\0', on)].decode('latin1')
    assert name == body, f'{model}: root piece is {name}, expected {body}'
    # engine coordinates: z negated (s3okit/threedo.py)
    V = np.array([struct.unpack_from('<3i', d, ov + 12 * i) for i in range(nv)], float) / 65536 * (1, 1, -1)
    off = np.array([x, y, -z], float) / 65536
    used = set()
    for i in range(npr):
        col, ni, _, oi, ot, *_r = struct.unpack_from('<8i', d, op + 32 * i)
        if ni >= 3 and i != sel:
            used.update(struct.unpack_from('<%dh' % ni, d, oi))
    P = V[sorted(used)] + off
    lo, hi = P.min(0), P.max(0)
    tail = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]])
    shift = off - tail                              # new vertex = old vertex + shift, root offset = 0
    if np.abs(tail).max() < 0.05 and np.abs(off).max() < 0.05:
        print('%-38s origin already at the tail' % model)
        return
    print('%-38s tail was at %s (root offset %s)' % (model, fmt(tail), fmt(off)))
    if check:
        return
    enc = lambda p: [int(round(c * 65536)) for c in (p[0], p[1], -p[2])]
    for i in range(nv):
        struct.pack_into('<3i', d, ov + 12 * i, *enc(V[i] + shift))
    struct.pack_into('<3i', d, 16, 0, 0, 0)
    c = ochild
    while c:                                        # children keep their place relative to the geometry
        cx, cy, cz = struct.unpack_from('<3i', d, c + 16)
        struct.pack_into('<3i', d, c + 16, *enc(np.array([cx, cy, -cz], float) / 65536 + shift))
        c = struct.unpack_from(hdr, d, c)[11]
    open(path, 'wb').write(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='report only, write nothing')
    a = ap.parse_args()
    for unit, (pieces, axis) in MISSILES.items():
        do_unit(unit, pieces, axis, a.check)
    for model, body in OLD_3DO:
        do_3do(model, body, a.check)


if __name__ == '__main__':
    main()
