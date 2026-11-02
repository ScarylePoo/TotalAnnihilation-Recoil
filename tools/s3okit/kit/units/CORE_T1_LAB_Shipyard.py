"""Shipyard (CORE_T1_LAB_Shipyard) - Core T1 ship factory. A deep-set dock (waterline 32: the water surface is model
y = 32): four massive dark corner pylons stand out of the water in the yardmap's `w` corner cells - a tall control
block with warm windows and a team roof (back left, blink beacon on top), a plain buttressed pylon (front right) and
two nano gantry pylons on the diagonal (turreta front left, turretb back right: their heads rise 17.4 out of the
pylon tops, turn toward the slip and tip their nano guns down at it). Under the surface, a perimeter cradle (tops
0.6 below the water at the corners, dipping 7 at the side middles) and TA's octagonal inner ring, ochre and team
striped, read through the water; the centre stays open for the ship (built at the base origin).
Core lab family: dark warm armour, pylons with team caps, ochre hazard on the builder parts, warm lights.
Identity from above: four big dark towers round open water, an octagon showing through it (the Arm shipyard is four
small light corner towers round a square).
Pieces (COB): base, turreta/turretb (move y, turn y), guna/gunb (turn x, z), beama/beamb (empty nano emit points),
blink (beacon), explodpt1/2 (empty debris points). QueryBuildInfo uses base.
Preview: OPEN (activatescr end state; COB z turns negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    ground=False, water=32.0,
    always_visible=['guna', 'gunb', 'turreta', 'turretb'],
    wreck=dict(seed=68, drop=['turretb']),
    preview_pose={
        'turreta': {'move': (0, 17.375, 0), 'rot': (0, -33.98, 0)},
        'turretb': {'move': (0, 17.375, 0), 'rot': (0, -43.01, 0)},
        'guna': (66.9, 0, 28.67), 'gunb': (-71.68, 0, -28.67),
    },
)

W = 32.0             # water surface
C = 54.0             # corner pylon centres
YC, YM = W - 0.6, W - 7.0


def beam(b, p0, p1, w, mat_top, depth=3.5):
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    L = math.hypot(x1 - x0, z1 - z0)
    nx, nz = -(z1 - z0) / L * w / 2, (x1 - x0) / L * w / 2
    b.hull([(x + s * nx, y + yy, z + s * nz) for (x, y, z) in (p0, p1) for s in (-1, 1) for yy in (-depth, -0.4)],
           'paint2', bevel=0.2)
    b.hull([(x + s * nx * 0.8, y + yy, z + s * nz * 0.8) for (x, y, z) in (p0, p1) for s in (-1, 1)
            for yy in (-0.45, 0.1)], mat_top, bevel=0.05)


def pylon(b, cx, cz, top, r=8.0):
    """octagonal dark pylon from the sea bed to `top`, with a wider buttressed foot at the waterline"""
    b.cyl((cx, 0.0, cz), (cx, top, cz), r, 8, 'paint', rot=math.pi / 8, bevel=0.3)
    b.cyl((cx, YM - 2.0, cz), (cx, W + 4.0, cz), r + 2.4, 8, 'paint2', r2=r + 0.6, rot=math.pi / 8, bevel=0.3)
    b.cyl((cx, W + 2.0, cz), (cx, W + 3.4, cz), r + 1.6, 8, 'lightw', rot=math.pi / 8)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ underwater cradle + octagon ring
    for sx in (-1, 1):
        beam(b, (sx * C, YC, -C + 8.0), (sx * C, YM, 0.0), 6.0, 'team')
        beam(b, (sx * C, YM, 0.0), (sx * C, YC, C - 8.0), 6.0, 'hazard')
    beam(b, (-C + 8.0, YC, -C), (0.0, YM, -C), 6.0, 'hazard')
    beam(b, (0.0, YM, -C), (C - 8.0, YC, -C), 6.0, 'team')
    beam(b, (-C + 8.0, YC, C), (0.0, YM, C), 6.0, 'hazard')
    beam(b, (0.0, YM, C), (C - 8.0, YC, C), 6.0, 'hazard')
    R = 36.0
    oct_pts = [(R * math.cos(math.pi / 8 + i * math.pi / 4), R * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    for i in range(8):
        (ax, az), (bx, bz) = oct_pts[i], oct_pts[(i + 1) % 8]
        beam(b, (ax, YM - 3.0, az), (bx, YM - 3.0, bz), 4.0, 'team' if i % 4 == 0 else 'paint', depth=3.0)
    for ax, az in oct_pts[::2]:                                    # spokes from the ring to the cradle sides
        L = math.hypot(ax, az)
        beam(b, (ax, YM - 3.0, az), (ax / L * (C - 3.0) / max(abs(ax / L), abs(az / L)), YM - 1.0,
                                     az / L * (C - 3.0) / max(abs(ax / L), abs(az / L))), 3.0, 'dark', depth=2.5)
    # ------------------------------------------------------------------ corner pylons
    pylon(b, -C, C, W + 2.0)                       # front left: under turreta (gantry sleeve slides out of it)
    pylon(b, C, -C, W + 2.0)                       # back right: under turretb
    pylon(b, C, C, W + 22.0)                       # front right: plain pylon with a team cap
    b.cyl((C, W + 21.9, C), (C, W + 22.6, C), 6.8, 8, 'team', rot=math.pi / 8)
    b.box((C - 1.2, W + 22.5, C - 1.2), (C + 1.2, W + 26.0, C + 1.2), 'steel', bevel=0.1)
    # back left: control block on a pylon
    pylon(b, -C, -C, W + 9.0, r=9.0)
    b.plan(W + 8.0, W + 30.0, [(-64.0, -64.0), (-42.0, -64.0), (-42.0, -46.0), (-48.0, -42.0), (-64.0, -42.0)],
           'paint', bevel=0.4, top_inset=2.0)
    b.box((-63.2, W + 20.0, -63.2), (-42.8, W + 23.0, -42.8), 'lightw', bevel=0.1)
    b.box((-61.4, W + 29.9, -61.4), (-46.0, W + 30.6, -45.0), 'team', bevel=0.1)
    b.hull([(x, W + 30.0, z) for x, z in ((-58.0, -58.0), (-49.0, -58.0), (-49.0, -49.0), (-58.0, -49.0))]
           + [(x, W + 41.0, z) for x, z in ((-56.0, -56.0), (-51.0, -56.0), (-51.0, -51.0), (-56.0, -51.0))],
           'paint2', bevel=0.3)
    k.piece('blink').box((-54.6, W + 40.8, -54.6), (-52.4, W + 43.4, -52.4), 'lightr', bevel=0.15)

    # ------------------------------------------------------------------ gantries (turreta origin -49.26, 34.66, 58.96)
    t = k.piece('turreta'); T = t.at
    t.cyl(T(0, -21.0, 0), T(0, -2.8, 0), 5.2, 8, 'steel', rot=math.pi / 8, bevel=0.2)    # sleeve (in the pylon at rest)
    t.cyl(T(0, -3.0, 0), T(0, 2.4, 0), 6.6, 8, 'paint2', rot=math.pi / 8, bevel=0.3)
    for sx in (-1, 1):                                          # prongs; the gun swings between them
        t.box(T(sx * 3.9, 2.0, -3.4), T(sx * 6.4, 20.0, 3.4), 'paint', bevel=0.3)
    t.box(T(-6.4, 19.0, -3.4), T(6.4, 21.4, 3.4), 'paint', bevel=0.3)
    t.box(T(-5.8, 21.3, -2.8), T(5.8, 21.8, 2.8), 'hazard', bevel=0.05)
    k.clone('turretb', 'turreta')
    g = k.piece('guna'); G = g.at                               # nano gun hanging down; beama at (0, -12.26, 0)
    g.box(G(-3.4, -3.0, -2.9), G(3.4, 3.4, 2.9), 'steel', bevel=0.35)
    g.cyl(G(0, -2.8, 0), G(0, -10.8, 0), 1.7, 10, 'dark', r2=1.2)
    g.cyl(G(0, -10.7, 0), G(0, -12.26, 0), 1.25, 10, 'lightc')
    g.box(G(-3.0, 3.3, -2.5), G(3.0, 3.8, 2.5), 'hazard', bevel=0.05)
    k.clone('gunb', 'guna')
