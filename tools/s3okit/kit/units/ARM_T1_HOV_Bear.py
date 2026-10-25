"""Bear (ARM_T1_HOV_Bear) - Arm transport hovercraft. Big flat cargo hull with a pointed bow on a black skirt, the
whole top is two cargo doors (door3/door4 swing up about their outer edges and drop into the hull), a telescoping
crane on the stern (turret1 turns y, turret2 lifts the mast 12.5, boom1 pitches, boom2..9 telescope along z,
magnet2222 hangs from the tip; link2222 empty = transport attach point) and two big ducted stern propellers.
Value groups from above: black skirt ring, light Arm doors + hull with a wide team band across both doors, dark
crane spine (team stripe on top), yellow/black hazard magnet disc, dark propeller ducts at the stern.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=2048,
    bake_res=2048,      # 4096 (and 3072) bakes were OOM-killed in the shared memory cgroup
    wreck=dict(seed=7, drop=['magnet2222'], pose={'turret1': (0, 35, 0), 'door4': (0, 0, 20)}),
    preview_pose={'turret1': (0, -20, 0)},
)

TOPY = 30.2      # hull deck under the doors
DOORY = 31.25    # door piece origin height


def skirt_ring(b, y, grow):
    pts = [(29.8, -44.6), (31.6, -39.0), (31.6, 27.6), (17.4, 39.6), (0.0, 43.2)]
    return [(x * sx + (grow if x > 0 else 0) * sx, y, z + (grow if z > 0 else -grow)) for sx in (-1, 1) for x, z in pts]


def door(k, name, sx):
    d = k.piece(name)
    y0, y1 = DOORY - 0.95, DOORY
    xa, xb = 0.2 * sx, 22.1 * sx
    lo, hi = min(xa, xb), max(xa, xb)
    d.box((lo, y0, -25.9), (hi, y1, 21.2), 'paint', bevel=0.18)
    # longitudinal stiffening ribs (dark lines from above), split around the team band
    for xr in (7.0, 15.4):
        for z0, z1 in ((-24.0, 4.2), (16.0, 19.6)):
            a, c = sorted((xr * sx - 0.7, xr * sx + 0.7))
            d.box((a, y1 - 0.05, z0), (c, y1 + 0.45, z1), 'paint2', bevel=0.08)
    # wide team band across the door (with the other door: one band across the whole hull)
    a, c = sorted((1.6 * sx, 21.0 * sx))
    d.box((a, y1 - 0.02, 5.0), (c, y1 + 0.22, 15.0), 'team', bevel=0.05)
    # hazard strip on the inner (meeting) edge
    a, c = sorted((0.25 * sx, 1.35 * sx))
    d.box((a, y1 - 0.02, -25.4), (c, y1 + 0.12, 20.8), 'hazard', bevel=0.03)


def boom(k, name, r, length, mat):
    p = k.piece(name); B = p.at
    p.box(B(-r, -r * 0.85, 0.0), B(r, r * 0.85, length), mat, bevel=0.12)


def build(k):
    b = k.piece('base2')
    # ------------------------------------------------------------------ skirt
    b.hull(skirt_ring(b, 0.0, -1.2) + skirt_ring(b, 3.2, 0.4) + skirt_ring(b, 6.8, -0.4), 'tread', bevel=0.3)
    # ------------------------------------------------------------------ main hull (bow forward)
    pts = []
    for y, xw, zr, zf, xb, zb, zn in ((6.4, 24.8, -27.2, 26.0, 14.0, 34.0, 37.0),
                                       (15.0, 26.8, -27.2, 28.0, 13.4, 36.4, 39.0),
                                       (23.8, 26.4, -27.2, 23.9, 13.6, 32.5, 35.2),
                                       (TOPY, 22.4, -26.6, 21.5, 13.8, 26.3, 29.0)):
        for sx in (-1, 1):
            pts += [(xw * sx, y, zr), (xw * sx, y, zf), (xb * sx, y, zb), (0.0, y, zn)]
    b.hull(pts, 'paint', bevel=0.22)
    # dark-blue rub strake at the widest point
    pts = []
    for y in (13.8, 16.4):
        for sx in (-1, 1):
            pts += [(27.3 * sx, y, -27.6), (27.3 * sx, y, 28.3), (13.7 * sx, y, 36.9), (0.0, y, 39.6)]
    b.hull(pts, 'paint2', bevel=0.1)
    # bay floor seen when the doors are open
    b.box((-21.6, TOPY - 0.1, -25.4), (21.6, TOPY + 0.12, 20.6), 'paint2', bevel=0.05)
    # bow: bridge windows on the forward slope + headlights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.5, 27.0, 31.0), (10.5, 29.6, 27.0), (10.5, 27.12, 31.12), (10.5, 29.72, 27.12),
             (3.0, 27.6, 33.6), (3.0, 30.0, 29.2), (3.0, 27.72, 33.72), (3.0, 30.12, 29.32)]], 'glass', bevel=0.03)
    b.box((9.0, 17.2, 35.2), (13.0, 19.4, 36.6), 'dark', bevel=0.06, mirror=True)
    b.hull([(9.3, 17.5, 36.5), (12.7, 17.5, 35.9), (9.3, 19.1, 36.5), (12.7, 19.1, 35.9),
            (9.3, 17.5, 36.62), (12.7, 17.5, 36.02), (9.3, 19.1, 36.62), (12.7, 19.1, 36.02)], 'lightw', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ stern deck (crane + propellers)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(25.6, 6.4, -42.4), (25.6, 6.4, -26.0), (26.4, 15.0, -42.8), (26.4, 15.0, -26.0),
             (24.0, 25.0, -41.6), (24.0, 25.0, -26.0)]], 'paint', bevel=0.2)
    b.box((-24.2, 25.0, -41.4), (24.2, 25.4, -27.0), 'paint2', bevel=0.06)
    # crane base ring
    b.cyl((0, 25.2, -33.73), (0, 26.0, -33.73), 9.4, 18, 'dark', bevel=0.1)
    # propeller pylons + ducted props (vertical discs, axis along z)
    for x in (17.6,):
        b.box((x - 1.6, 25.2, -38.6), (x + 1.6, 28.0, -35.4), 'dark', bevel=0.12, mirror=True)
        b.cyl((x, 33.4, -39.4), (x, 33.4, -34.4), 7.4, 18, 'paint2', bevel=0.16, mirror=True)
        b.cyl((x, 33.4, -39.5), (x, 33.4, -39.45), 6.2, 18, 'black', mirror=True)
        b.cyl((x, 33.4, -34.35), (x, 33.4, -34.3), 6.2, 18, 'black', mirror=True)
        for i in range(3):
            a = i * 2 * math.pi / 3 + 0.4
            ca, sa = math.cos(a), math.sin(a)
            pts = []
            for dd in (1.0, 5.8):
                for s in (-0.7, 0.7):
                    px, py = x + ca * dd - sa * s, 33.4 + sa * dd + ca * s
                    pts += [(px, py, -39.9), (px, py, -39.5)]
            b.hull(pts, 'steel', bevel=0.0, mirror=True)
        b.cyl((x, 33.4, -40.4), (x, 33.4, -39.4), 1.3, 10, 'dark', r2=0.7, mirror=True)
        # team fin on top of each duct
        b.box((x - 0.5, 40.6, -39.0), (x + 0.5, 42.6, -34.8), 'team', bevel=0.06, mirror=True)
    b.box((20.6, 12.0, -43.3), (23.6, 13.0, -42.7), 'lightr', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ doors
    door(k, 'door4', 1)
    door(k, 'door3', -1)

    # ------------------------------------------------------------------ crane
    t1 = k.piece('turret1'); A = t1.at
    t1.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(7.4, 0.6, -3.2), (7.4, 0.6, 3.2), (3.2, 0.6, 7.4), (3.2, 0.6, -7.4),
              (6.2, 14.4, -2.8), (6.2, 14.4, 2.8), (2.8, 14.4, 6.2), (2.8, 14.4, -6.2)]], 'paint', bevel=0.2)
    t1.box(A(-5.8, 4.0, 5.9), A(5.8, 6.2, 7.1), 'hazard', bevel=0.04)
    t2 = k.piece('turret2')
    t2.cyl((0, 37.0, -33.75), (0, 46.2, -33.75), 3.9, 14, 'steel', bevel=0.06)
    t2.cyl((0, 37.0, -33.75), (0, 39.2, -33.75), 4.6, 14, 'dark', bevel=0.06)
    bm = k.piece('boom1'); C = bm.at
    # boom housing (outer sleeve the sections slide out of) with a team stripe on top
    bm.box(C(-4.4, -3.6, -14.2), C(4.4, 3.6, 19.2), 'paint', bevel=0.2)
    bm.box(C(-3.2, 3.55, -12.0), C(3.2, 3.85, 17.0), 'team', bevel=0.05)
    bm.cyl(C(-4.6, 0, 0), C(4.6, 0, 0), 2.6, 12, 'dark', bevel=0.06)
    # counterweight at the back of the boom
    bm.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(9.6, -8.6, -8.8), (9.6, -8.6, -16.2), (9.6, 7.6, -8.8), (9.6, 7.6, -16.2), (4.4, -3.0, -6.0), (4.4, 3.0, -6.0)]],
            'paint2', bevel=0.22)
    bm.box(C(-9.0, 7.5, -15.6), C(9.0, 7.8, -9.4), 'hazard', bevel=0.04)
    # telescoping sections, strictly shrinking so they nest
    for i, n in enumerate(('boom2', 'boom3', 'boom4', 'boom5', 'boom6', 'boom7', 'boom8', 'boom9')):
        boom(k, n, 3.25 - 0.13 * i, 28.0 if i < 6 else 35.0, 'dark' if i % 2 else 'steel')
    # magnet
    m = k.piece('magnet2222'); M = m.at
    m.box(M(-1.4, -3.0, -1.4), M(1.4, 1.4, 1.4), 'steel', bevel=0.1)
    m.cyl(M(0, -7.4, 0), M(0, -4.4, 0), 7.2, 18, 'dark', bevel=0.15)
    m.cyl(M(0, -4.45, 0), M(0, -3.95, 0), 6.4, 18, 'hazard', bevel=0.05)
    m.cyl(M(0, -3.95, 0), M(0, -3.0, 0), 2.2, 12, 'dark', bevel=0.05)
    m.cyl(M(0, -7.5, 0), M(0, -7.42, 0), 5.6, 18, 'black')
