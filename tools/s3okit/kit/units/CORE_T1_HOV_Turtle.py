"""Turtle (CORE_T1_HOV_Turtle) - Core transport hovercraft. Heavy angular barge on a deep black skirt with armoured
side sponsons (lift fans), a cargo bay amidships closed by two big doors (ldoor/rdoor swing up about their outer
edges and drop), and a TALL gantry crane at the stern (the Turtle's signature, unlike the Arm Bear's low deck crane):
`tower` (turn y) carries the `arm` (pitches x) with a `counterweight` block behind and a telescoping boom
(boom1..6 slide along z) ending in the `magnet`; `link` (empty) is the transport attach point.
`gp` (ground plate) and `botten` (TA bottom shadow plate) are kept as empty pieces.
Value groups from above: black skirt ring, dark warm hull and sponsons, darker paint2 doors with a team chevron,
light steel boom and tower (Core = light mechanics), ochre/black hazard counterweight and magnet, dark fan discs.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=2048,
    bake_res=2048,      # 4096 (and 3072) bakes were OOM-killed in the shared memory cgroup
    wreck=dict(seed=15, drop=['magnet'], pose={'tower': (0, 30, 0), 'ldoor': (0, 0, 25)}),
    preview_pose={'tower': (0, 20, 0)},
)

PLAN = [(5.6, 44.2), (24.9, 40.6), (31.4, 14.4), (31.6, -7.0), (26.4, -34.0), (12.0, -44.4), (4.0, -44.6)]
DOORY = 32.5


def ring(y, d=0.0):
    out = []
    for x, z in PLAN:
        L = math.hypot(x - 10, z) or 1
        p = (x + (x - 10) / L * d, y, z + z / L * d)
        out += [p, (-p[0], y, p[2])]
    return out


def boom(k, name, r, length, mat):
    p = k.piece(name); B = p.at
    p.box(B(-r, -r * 0.9, 0.0), B(r, r * 0.9, length), mat, bevel=0.12)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ skirt (deep: the hull floats at y 9.4)
    b.hull(ring(0.0, 0.4) + ring(4.0, 2.4) + ring(8.6, 2.0) + ring(10.2, 0.8), 'tread', bevel=0.32)
    # ------------------------------------------------------------------ hull: two tiers
    # lower deck: wide and low, the lift fans sit on its shoulders
    b.hull(ring(9.6, -1.2) + ring(17.4, -1.8), 'paint', bevel=0.24)
    b.hull(ring(9.8, 0.2) + ring(11.8, 0.0), 'steel', bevel=0.1)
    # upper block carrying the cargo bay (crosses x = 0), sloped walls
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(23.8, 17.2, -30.0), (23.8, 17.2, 28.0), (16.0, 17.2, 38.0), (5.0, 17.2, 40.6), (14.0, 17.2, -38.0),
             (22.4, 31.6, -27.8), (22.4, 31.6, 26.0), (14.6, 31.6, 34.0), (5.0, 31.6, 37.6), (13.0, 31.6, -35.8)]],
           'paint', bevel=0.24)
    # lift fans on the lower-deck shoulders (+X mirrored), fore and aft
    for x, z in ((26.6, -16.0), (26.6, 12.0)):
        b.cyl((x, 16.6, z), (x, 18.0, z), 4.0, 16, 'dark', bevel=0.12, mirror=True)
        b.cyl((x, 18.0, z), (x, 18.05, z), 3.2, 16, 'black', mirror=True)
        for i in range(3):
            a = i * 2 * math.pi / 3 + 0.2
            ca, sa = math.cos(a), math.sin(a)
            pts = []
            for d in (0.8, 3.0):
                for s in (-0.8, 0.8):
                    px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                    pts += [(px, 17.75, pz), (px, 18.05, pz)]
            b.hull(pts, 'steel', bevel=0.0, mirror=True)
        b.cyl((x, 17.7, z), (x, 18.4, z), 1.0, 10, 'steel', bevel=0.05, mirror=True)
    # ochre hazard chevrons on the lower deck bow shoulders
    b.hull([(x, y, z) for y in (17.44, 17.6) for x, z in [(17.0, 36.0), (22.0, 30.0), (24.0, 31.6), (19.4, 37.2)]],
           'hazard', bevel=0.03, mirror=True)
    # bay rim around the doors (raised coaming), bay floor
    b.box((20.2, 31.4, -25.6), (22.4, 33.4, 25.0), 'paint2', bevel=0.14, mirror=True)
    b.box((-20.2, 31.4, 24.4), (20.2, 33.4, 26.6), 'paint2', bevel=0.14)
    b.box((-20.2, 31.4, -27.6), (20.2, 33.4, -25.0), 'paint2', bevel=0.14)
    b.box((-20.0, 31.5, -25.0), (20.0, 31.62, 24.4), 'dark', bevel=0.0)
    # bow: raised bridge with windows, ochre bow plate, lights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(14.0, 31.0, 27.0), (14.0, 31.0, 34.0), (6.0, 31.0, 38.0), (11.6, 37.6, 28.4), (5.0, 37.6, 31.6)]],
           'paint', bevel=0.2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.6, 33.4, 33.8), (5.4, 34.4, 35.2), (10.6, 33.52, 33.92), (5.4, 34.52, 35.32),
             (9.8, 36.2, 30.4), (4.8, 36.8, 32.2), (9.8, 36.32, 30.52), (4.8, 36.92, 32.32)]], 'glass', bevel=0.02)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 23.0, 42.6), (4.4, 28.4, 39.2), (4.4, 23.14, 42.72), (4.4, 28.54, 39.32)]], 'hazard', bevel=0.03)
    b.box((16.0, 15.0, 40.6), (21.0, 17.4, 41.8), 'dark', bevel=0.06, mirror=True)
    b.hull([(16.3, 15.3, 41.7), (20.7, 15.3, 40.9), (16.3, 17.1, 41.7), (20.7, 17.1, 40.9),
            (16.3, 15.3, 41.82), (20.7, 15.3, 41.02), (16.3, 17.1, 41.82), (20.7, 17.1, 41.02)], 'lightw', bevel=0.0, mirror=True)
    # stern deck under the crane + exhausts
    b.box((-14.0, 31.0, -42.0), (14.0, 35.2, -27.6), 'paint2', bevel=0.16)
    b.cyl((0, 35.0, -34.1), (0, 36.7, -34.1), 8.4, 18, 'dark', bevel=0.1)
    for xx in (18.0,):
        b.cyl((xx, 24.0, -33.0), (xx, 24.0, -38.4), 2.8, 12, 'dark', bevel=0.08, mirror=True)
        b.cyl((xx, 24.0, -38.4), (xx, 24.0, -38.5), 2.0, 12, 'black', mirror=True)
    b.box((8.0, 20.0, -44.9), (11.0, 21.4, -44.5), 'lightr', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ doors (ldoor hinge x 20, rdoor x -20)
    d = k.piece('ldoor'); D = d.at
    d.box(D(-19.9, -0.9, -24.8), D(-0.1, 0.0, 24.2), 'paint2', bevel=0.18)
    # team chevron (both doors together: a forward-pointing arrow)
    d.hull([D(x, y, z) for x, y, z in
            [(-19.9, -0.04, 7.0), (-19.9, -0.04, 15.0), (-6.0, -0.04, 1.0), (-6.0, -0.04, -7.0)] +
            [(-19.9, 0.2, 7.0), (-19.9, 0.2, 15.0), (-6.0, 0.2, 1.0), (-6.0, 0.2, -7.0)]], 'team', bevel=0.04)
    for zz in (-20.0, -10.0, 18.0):
        d.box(D(-18.8, -0.05, zz), D(-1.2, 0.3, zz + 1.2), 'dark', bevel=0.05)
    k.clone('rdoor', 'ldoor', mirror_x=True)

    # ------------------------------------------------------------------ crane tower (tall lattice gantry)
    t = k.piece('tower'); T = t.at
    t.cyl(T(0, 0.0, 0), T(0, 1.6, 0), 7.0, 16, 'dark', bevel=0.1)
    for sx in (-1, 1):
        for sz in (-1, 1):
            t.box(T(4.2 * sx - 1.0, 1.4, 2.6 * sz - 1.0), T(4.2 * sx + 1.0, 42.6, 2.6 * sz + 1.0), 'steel', bevel=0.12)
    for y in (9.0, 19.0, 29.0):
        t.box(T(-5.2, y, -3.6), T(5.2, y + 1.2, 3.6), 'dark', bevel=0.08)
    t.box(T(-6.0, 39.2, -4.0), T(6.0, 42.2, 4.0), 'paint', bevel=0.16)
    t.box(T(-4.8, 1.6, 3.6), T(4.8, 6.6, 6.4), 'paint', bevel=0.14)                 # operator cab at the foot
    t.box(T(-4.0, 3.8, 6.35), T(4.0, 5.8, 6.5), 'glass', bevel=0.0)
    # ------------------------------------------------------------------ arm (jib housing) + counterweight
    a = k.piece('arm'); A = a.at
    a.cyl(A(-6.2, 0, 0), A(6.2, 0, 0), 2.6, 12, 'dark', bevel=0.08)
    a.box(A(-3.4, -3.0, -14.0), A(3.4, 3.0, 25.8), 'paint', bevel=0.2)
    a.box(A(-2.4, 2.95, -12.0), A(2.4, 3.2, 23.8), 'team', bevel=0.04)
    cw = k.piece('counterweight')
    cw.box((-13.6, 72.6, -60.6), (13.6, 81.4, -48.4), 'paint2', bevel=0.24)
    cw.box((-12.8, 81.3, -59.6), (12.8, 81.6, -49.4), 'hazard', bevel=0.05)
    for i, n in enumerate(('boom1', 'boom2', 'boom3', 'boom4', 'boom5', 'boom6')):
        boom(k, n, 2.6 - 0.15 * i, 51.0 if i < 5 else 59.6, 'steel' if i % 2 == 0 else 'dark')
    m = k.piece('magnet'); M = m.at
    m.box(M(-1.4, -4.0, -1.4), M(1.4, 1.6, 1.4), 'steel', bevel=0.1)
    m.cyl(M(0, -12.2, 0.7), M(0, -8.4, 0.7), 7.4, 18, 'dark', bevel=0.15)
    m.cyl(M(0, -8.45, 0.7), M(0, -7.9, 0.7), 6.6, 18, 'hazard', bevel=0.05)
    m.cyl(M(0, -7.9, 0.7), M(0, -4.0, 0.7), 2.2, 12, 'dark', bevel=0.05)
    m.cyl(M(0, -12.3, 0.7), M(0, -12.22, 0.7), 5.8, 18, 'black')
