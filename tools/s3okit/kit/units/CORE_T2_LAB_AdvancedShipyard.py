"""Advanced Shipyard (CORE_T2_LAB_AdvancedShipyard) - Core T2 ship factory: the T1 Core deep dock grown bigger.
Waterline 32 (the water surface is model y = 32). Four massive dark pylons stand out of the water in the yardmap's
`w` corner cells - two tall control blocks with warm windows and team roofs at the back, two buttressed pylons with
red beacons (blinks) at the front - round an underwater cradle (tops 0.6 below the surface at the corners, dipping
7 at the side middles) with TA's octagonal inner ring. Mid-side under water lie two crane housings: on activation
their long nano arms (gun1/gun2, turn z ~90) swing up out of the water to stand beside the slip with their emitters
facing it. The centre stays open for the ship (built at the base origin).
Core lab family (T2 = taller, more parts): dark warm armour, team caps, ochre hazard on the builder parts, warm
lights. Identity from above: four big dark towers round open water, an octagon showing through it, two ochre crane
arms standing at the side middles (the T1 Core yard has gantry pylons on one diagonal).
Pieces (COB): base, gun1/gun2 (turn z), beam1/beam2 (empty nano emit points), blinks (beacons), explodpt1..4 (empty
debris points). QueryBuildInfo uses base.
Preview: OPEN (activatescr end state; COB z turns negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    ground=False, water=32.0,
    always_visible=['gun1', 'gun2'],
    wreck=dict(seed=80, drop=['gun2']),
    preview_pose={'gun1': (0, 0, 89.73), 'gun2': (0, 0, -89.73)},
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
    beam(b, (0.0, YM, -C), (C - 8.0, YC, -C), 6.0, 'hazard')
    beam(b, (-C + 8.0, YC, C), (0.0, YM, C), 6.0, 'hazard')
    beam(b, (0.0, YM, C), (C - 8.0, YC, C), 6.0, 'hazard')
    R = 36.0
    oct_pts = [(R * math.cos(math.pi / 8 + i * math.pi / 4), R * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    for i in range(8):
        (ax, az), (bx, bz) = oct_pts[i], oct_pts[(i + 1) % 8]
        beam(b, (ax, YM - 3.0, az), (bx, YM - 3.0, bz), 4.0, 'paint', depth=3.0)
    for ax, az in oct_pts[::2]:                                    # spokes from the ring to the cradle sides
        L = math.hypot(ax, az)
        beam(b, (ax, YM - 3.0, az), (ax / L * (C - 3.0) / max(abs(ax / L), abs(az / L)), YM - 1.0,
                                     az / L * (C - 3.0) / max(abs(ax / L), abs(az / L))), 3.0, 'dark', depth=2.5)
    # ------------------------------------------------------------------ corner pylons
    for sx in (-1, 1):
        pylon(b, sx * C, C, W + 14.0)                                  # front: buttressed pylons, beacons on top
        b.cyl((sx * C, W + 13.9, C), (sx * C, W + 14.6, C), 6.8, 8, 'team', rot=math.pi / 8)
        pylon(b, sx * C, -C, W + 9.0, r=9.0)                           # back: control blocks
        x0, x1 = sorted((sx * 64.0, sx * 42.0))
        b.plan(W + 8.0, W + 27.0, [(x0, -64.0), (x1, -64.0), (x1, -42.0), (x0, -42.0)], 'paint', bevel=0.4,
               top_inset=2.0)
        b.box((x0 + 0.8, W + 18.0, -63.2), (x1 - 0.8, W + 21.0, -42.8), 'lightw', bevel=0.1)
        b.box((x0 + 2.6, W + 26.9, -61.4), (x1 - 2.6, W + 27.6, -44.6), 'team', bevel=0.1)
        xc = sx * 53.0
        b.hull([(x, W + 27.0, z) for x in (xc - 4.5, xc + 4.5) for z in (-57.5, -48.5)]
               + [(x, W + 36.0, z) for x in (xc - 2.5, xc + 2.5) for z in (-55.5, -50.5)], 'paint2', bevel=0.3)
    bl = k.piece('blinks')
    for x0 in (-54.5, 50.0):
        bl.box((x0, W + 14.2, 48.8), (x0 + 3.5, W + 17.7, 53.0), 'lightr', bevel=0.15)
    # crane housings (under water, mid sides)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 63.0, sx * 50.0))
        b.box((x0, 0.0, -8.0), (x1, 21.0, 14.0), 'paint2', bevel=0.4)
        b.box((x0 + 0.6, 20.9, -7.4), (x1 - 0.6, 21.4, 13.4), 'hazard', bevel=0.05)

    # ------------------------------------------------------------------ crane arms (gun1 origin -55.3, 16.45, 4.28)
    g = k.piece('gun1'); G = g.at                       # lies along +x at rest; beam1 at (21.05, -11.0, -1.78)
    g.cyl(G(0, 0, -6.4), G(0, 0, 3.0), 4.4, 10, 'dark', rot=math.pi / 10, bevel=0.15)
    g.box(G(0.0, -2.6, -4.4), G(24.0, 3.2, 1.2), 'paint', bevel=0.35)
    g.box(G(0.6, 3.1, -3.8), G(23.4, 3.6, 0.6), 'hazard', bevel=0.05)
    g.box(G(18.0, -9.0, -4.0), G(24.6, -2.4, 0.4), 'steel', bevel=0.3)
    g.cyl(G(21.05, -8.8, -1.78), G(21.05, -11.0, -1.78), 1.3, 10, 'lightc')
    k.clone('gun2', 'gun1', mirror_x=True)
