"""Hulk (ARM_T1_SEA_Hulk) - Arm naval transport. A big, wide, flat-decked hull riding low (waterline 15: only ~2
elmo of freeboard) with a ram bow; the middle is one huge cargo hold closed by two dark hatch doors (door1/door2
swing up 90 deg about the outer coaming edges). Aft stands a tall gantry: a light tower block with a forward cab,
two dark pillars up to y 80 holding the crane axle; the crane (arm1) is a long boom with a big counterweight at the
back, six telescoping sections (arm2..arm7) and a magnet that hangs over the hold (link = cargo attach point).
From above: wide light hull, dark hatch doors with two team stripes and light ribs, light tower with a team roof,
the dark boom running forward over the hold to a yellow/black hazard magnet, team-topped counterweight at the stern.
Pieces (TA layout): base, door1/door2, turret (turn y), arm1 (turn x), arm2/arm4/arm3/arm5/arm6/arm7 (move z, nested
in that order), magnet (turn x), link (empty, move y), wake1/2 (empty). The 3DO is centred on x = -1.25 (hinges at
-25 and 22.5): built around that line without mirror; door2 = mirrored clone of door1.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    bake_res=2048,      # 4096 bakes are OOM-killed in the shared memory cgroup (see Bear)
    always_visible=['arm2', 'arm3', 'arm4', 'arm5', 'arm6', 'arm7'],    # nested at rest, extended when loading
    wreck=dict(seed=6, drop=['magnet'], pose={'turret': (0, 25, 0), 'arm1': (12, 0, 0), 'door1': (0, 0, -60)}),
    preview_pose={},
)

C = -1.25          # hull centre line
XB, YB = -1.75, 73.75   # telescoping boom axis (global), as the 3DO sections
DECK = 17.1
HOLD = (-25.0, 22.5, -19.5, 31.5)       # coaming x0, x1, z0, z1
# half outline at deck level (half-width, z), bow to stern
OUT = [(9.4, 56.4), (14.1, 51.5), (22.6, 41.9), (25.8, 38.7), (28.4, 31.5), (28.4, -19.6), (26.4, -52.0), (17.2, -62.6)]


def cut(pts, z0, z1):
    P = sorted({z: x for x, z in pts}.items())
    zs = [z for z, _ in P]; xs = [x for _, x in P]

    def xat(z):
        for i in range(len(zs) - 1):
            if zs[i] <= z <= zs[i + 1]:
                t = (z - zs[i]) / (zs[i + 1] - zs[i]); return xs[i] + t * (xs[i + 1] - xs[i])
        return xs[0] if z < zs[0] else xs[-1]
    lo, hi = max(z0, zs[0]), min(z1, zs[-1])
    return [(xat(z), z) for z in sorted({lo, hi} | {z for z in zs if lo < z < hi})]


def ringc(pts, y, sx=1.0, dz=0.0):
    return [(C + x * sx * s, y, z + dz) for x, z in pts for s in (-1, 1)]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull in segments (no long UV strips)
    for z0, z1 in ((31.5, 57.0), (5.0, 31.5), (-19.6, 5.0), (-63.0, -19.6)):
        o = cut(OUT, z0, z1)
        lo = [(x * 0.8, min(max(z, -58.0), 53.5)) for x, z in o]
        b.hull(ringc(lo, 0.2) + ringc(o, 12.0, 0.99), 'paint2', bevel=0.25)                 # below water
        b.hull(ringc(o, 12.0, 0.99) + ringc(o, DECK), 'paint', bevel=0.25)                  # freeboard band
    # ram bow (sloping forward below the deck)
    b.hull([(C + x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.0, DECK, 56.0), (13.6, DECK, 51.6), (5.6, 7.8, 59.6), (9.6, 7.8, 56.4)]], 'paint', bevel=0.25)
    # deck plating: dark walkway strip along the gunwale
    for s in (-1, 1):
        b.box((C + s * 26.6 - 0.6, DECK - 0.05, -48.0), (C + s * 26.6 + 0.6, DECK + 0.25, 30.0), 'dark', bevel=0.04)
    # ------------------------------------------------------------------ cargo hold: coaming walls + black floor
    x0, x1, z0, z1 = HOLD
    yt = 21.38 - 0.6
    b.box((x0 - 1.4, DECK - 0.2, z0 - 1.4), (x0, yt, z1 + 1.4), 'paint', bevel=0.15)
    b.box((x1, DECK - 0.2, z0 - 1.4), (x1 + 1.4, yt, z1 + 1.4), 'paint', bevel=0.15)
    b.box((x0, DECK - 0.2, z0 - 1.4), (x1, yt, z0), 'paint', bevel=0.15)
    b.box((x0, DECK - 0.2, z1), (x1, yt, z1 + 1.4), 'paint', bevel=0.15)
    b.box((x0, DECK - 0.4, z0), (x1, DECK - 0.1, z1), 'black', bevel=0.0)
    # forecastle: bollards, a dark winch house and twin running lights
    b.box((C - 6.0, DECK, 38.0), (C + 6.0, DECK + 3.4, 45.0), 'paint2', bevel=0.2)
    b.box((C - 4.6, DECK + 3.35, 39.0), (C + 4.6, DECK + 3.6, 44.0), 'dark', bevel=0.04)
    for s in (-1, 1):
        b.cyl((C + s * 11.0, DECK, 47.0), (C + s * 11.0, DECK + 1.6, 47.0), 1.1, 10, 'dark')
        b.box((C + s * 28.4 - 0.2, 15.2, 30.0), (C + s * 28.4 + 0.2, 16.2, 32.0), 'lightw' if s > 0 else 'lightr', bevel=0.0)
    # aft deck: two dark engine vents either side of the tower and the stern light
    for s in (-1, 1):
        b.box((C + s * 22.0 - 2.4, DECK, -50.0), (C + s * 22.0 + 2.4, DECK + 2.2, -30.0), 'dark', bevel=0.15)
        for z in (-48.0, -44.0, -40.0, -36.0):
            b.box((C + s * 22.0 - 1.8, DECK + 2.15, z), (C + s * 22.0 + 1.8, DECK + 2.3, z + 1.6), 'black', bevel=0.0)
    b.box((C - 2.0, 14.6, -62.9), (C + 2.0, 15.6, -62.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ hatch doors (door1 origin -25, 21.38, 5)
    d = k.piece('door1'); D = d.at
    W = 23.75                                   # meets door2 (mirrored clone) on the centre line x = -1.25
    d.box(D(0.0, -0.7, -24.5), D(W, 0.2, 26.5), 'paint2', bevel=0.15)
    d.box(D(4.0, 0.15, -22.6), D(10.0, 0.42, 24.6), 'team', bevel=0.04)
    for z in (-16.0, 0.0, 16.0):
        d.box(D(11.2, 0.15, z - 1.0), D(W - 0.4, 0.5, z + 1.0), 'paint', bevel=0.06)
    d.box(D(0.6, 0.15, -23.6), D(2.4, 0.5, 25.6), 'dark', bevel=0.05)          # hinge beam
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ gantry tower (turret origin -2, 17.5, -42)
    t = k.piece('turret'); T = t.at
    oc = [(-19.2, -13.1), (-19.2, 10.0), (0.0, 19.5), (19.3, 10.0), (19.3, -13.1), (0.0, -20.5)]
    t.hull([T(x, y, z) for x, z in oc for y in (0.0, 10.1)], 'paint', bevel=0.25)
    t.hull([T(x, y, z) for x, z in ((-13.0, -15.5), (14.5, -15.5), (14.5, 12.0), (-13.0, 12.0)) for y in (10.0, 21.7)] +
           [T(x, 33.0, z) for x, z in ((-8.0, -10.5), (9.5, -10.5), (9.5, 2.0), (-8.0, 2.0))], 'paint', bevel=0.25)
    t.box(T(-7.4, 32.95, -9.9), T(8.9, 33.25, 1.4), 'team', bevel=0.05)
    # forward cab with a wide glass band
    t.hull([T(x, y, z) for x, y, z in
            [(-8.0, 12.5, 12.0), (9.5, 12.5, 12.0), (-6.0, 12.5, 22.0), (5.0, 12.5, 22.0),
             (-8.0, 20.0, 12.0), (9.5, 20.0, 12.0), (-6.0, 20.0, 16.0), (7.7, 20.0, 16.0)]], 'paint', bevel=0.2)
    t.hull([T(x, y, z) for x, y, z in
            [(-6.1, 15.0, 21.7), (5.1, 15.0, 21.7), (-6.4, 18.6, 18.4), (6.4, 18.6, 18.4),
             (-6.1, 15.0, 22.1), (5.1, 15.0, 22.1), (-6.4, 18.6, 18.8), (6.4, 18.6, 18.8)]], 'glass', bevel=0.0)
    # two dark pillars to the crane axle
    for xa, xb in ((-19.2, -16.0), (16.1, 19.3)):
        t.hull([T(x, y, z) for x in (xa, xb) for y, z in ((10.0, 11.4), (10.0, -14.1), (63.2, 5.1), (63.2, -7.8))],
               'paint2', bevel=0.2)
        t.box(T(xa - 0.1, 63.1, -4.6), T(xb + 0.1, 63.6, 1.8), 'lightr', bevel=0.0)
    t.box(T(16.0, 22.0, 2.0), T(16.2, 24.0, 6.0), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ crane boom (arm1 origin -2, 74, -44; turns x)
    a = k.piece('arm1'); A = a.at
    a.cyl(A(-15.8, 0, 0), A(12.1, 0, 0), 2.2, 12, 'dark')                                    # axle between the pillars
    a.box((XB - 2.7, YB - 3.1, A(0, 0, -4.0)[2]), (XB + 2.7, YB + 3.4, A(0, 0, 48.6)[2]), 'paint2', bevel=0.2)   # boom sleeve
    a.box((XB - 1.6, YB + 3.35, A(0, 0, 2.0)[2]), (XB + 1.6, YB + 3.6, A(0, 0, 46.0)[2]), 'hazard', bevel=0.03)
    a.box((XB - 2.9, YB - 3.1, A(0, 0, -18.6)[2]), (XB + 2.9, YB + 3.4, A(0, 0, -3.8)[2]), 'paint2', bevel=0.2)   # tail
    a.hull([A(x, y, z) for x in (-13.0, 10.5) for y, z in ((-9.0, -36.0), (8.5, -28.5), (8.5, -18.5), (-9.0, -18.5))],
           'paint', bevel=0.3)                                                               # counterweight
    a.box(A(-11.6, 8.45, -27.2), A(9.1, 8.75, -19.8), 'team', bevel=0.05)
    # telescoping sections (local z 0 .. tip): nested, shrinking, tips stepped so the ends never coincide
    for name, w, tip in (('arm2', 2.3, 48.5), ('arm4', 2.05, 48.9), ('arm3', 1.8, 49.3),
                         ('arm5', 1.55, 55.0), ('arm6', 1.3, 55.4), ('arm7', 1.05, 55.8)):
        p = k.piece(name); B = p.at
        o = B(0, 0, 0)
        p.box((XB - w, YB - w * 1.15, o[2]), (XB + w, YB + w * 1.15, o[2] + tip), 'steel' if name in ('arm2', 'arm3', 'arm6') else 'dark',
              bevel=0.08)
    # magnet (origin -1.75, 73.5, 13.25): stem + wide yellow/black hazard plate with a dark rim, cyan coil glow
    m = k.piece('magnet'); M = m.at
    m.box(M(-2.3, -9.4, -2.8), M(2.3, 2.2, 4.8), 'dark', bevel=0.15)
    m.hull([M(x, y, z) for x in (-9.6, 9.6) for y, z in ((-14.4, -10.2), (-14.4, 12.2), (-10.6, -8.6), (-10.6, 10.6))],
           'paint2', bevel=0.2)
    m.box(M(-7.8, -10.75, -7.0), M(7.8, -10.45, 9.0), 'hazard', bevel=0.04)
    m.box(M(-8.6, -14.6, -9.2), M(8.6, -14.35, 11.2), 'lightc', bevel=0.0)
