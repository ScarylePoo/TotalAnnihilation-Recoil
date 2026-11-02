"""Shipyard (ARM_T1_LAB_Shipyard) - Arm T1 ship factory. A floating dock (waterline 1: the water surface is model
y = 1): a square cradle of pontoon beams under water (tops 0.6 under the surface at the corners, so they read through
the water, dipping to 7 down at the side middles where ships cross) with diamond braces, and four light corner caissons standing out of the water in the
yardmap's `w` corner cells: a control house (back left), a beacon pylon (back right) and two nano gantries (front
corners: turret1/turret2 turn to face the slip, the nano heads rise 19.4 between their prongs and tip down toward it).
Everything between the corners stays under water (the yardmap is open `C` there): ships are built at `slip` (centre,
y -8.75) and sail out over the beams.
Arm lab family: light chamfered blocks, team caps, hazard on the builder parts, cyan lights. Identity from above: four
light corner towers round open water with a team/hazard-striped square seen through it (the Core shipyard is a
massive dark half-sunk dock with two gantry towers).
Pieces (COB): base, turret1/2 (turn y), nano1/2 (move y, turn x), beam1/2 (empty nano emit points), slip (empty;
QueryBuildInfo), light (beacon), exlpode1/explode2/explode3 (empty debris points).
Preview: OPEN (activatescr end state).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    ground=False, water=1.0,
    always_visible=['nano1', 'nano2'],
    wreck=dict(seed=67, drop=['turret2']),
    preview_pose={
        'nano1': {'move': (0, 19.375, 0), 'rot': (47.7, 0, 0)},
        'nano2': {'move': (0, 19.5, 0), 'rot': (48.15, 0, 0)},
        'turret1': (0, -45.0, 0), 'turret2': (0, 45.44, 0),
    },
)

C = 52.0             # corner caisson centres (+-C, +-C)
YC, YM = 0.4, -6.0    # beam top at the corners (0.6 under the surface) / at the side middles


def beam(b, p0, p1, w, mat_top):
    """pontoon beam segment between two top-centre points (x, y, z): paint2 body 3 deep and a 0.5 top strip"""
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    dx, dz = x1 - x0, z1 - z0
    L = math.hypot(dx, dz)
    nx, nz = -dz / L * w / 2, dx / L * w / 2
    body = [(x + sx * nx, y + yy, z + sx * nz) for (x, y, z) in (p0, p1) for sx in (-1, 1) for yy in (-3.0, -0.4)]
    b.hull(body, 'paint2', bevel=0.2)
    top = [(x + sx * nx * 0.8, y + yy, z + sx * nz * 0.8) for (x, y, z) in (p0, p1) for sx in (-1, 1)
           for yy in (-0.45, 0.1)]
    b.hull(top, mat_top, bevel=0.05)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ underwater cradle
    for sx in (-1, 1):                                                        # side beams (x = +-C), team tops
        beam(b, (sx * C, YC, -C + 6.0), (sx * C, YM, 0.0), 6.0, 'team')
        beam(b, (sx * C, YM, 0.0), (sx * C, YC, C - 6.0), 6.0, 'hazard')
    beam(b, (-C + 6.0, YC, -C), (0.0, YM, -C), 6.0, 'team')                  # back beam
    beam(b, (0.0, YM, -C), (C - 6.0, YC, -C), 6.0, 'hazard')
    beam(b, (-C + 6.0, YC, C), (0.0, YM, C), 6.0, 'hazard')                  # front sill
    beam(b, (0.0, YM, C), (C - 6.0, YC, C), 6.0, 'hazard')
    for (ax, az), (bx, bz) in (((-C, 0.0), (0.0, -C)), ((0.0, -C), (C, 0.0)), ((C, 0.0), (0.0, C)), ((0.0, C), (-C, 0.0))):
        b.hull([(x + dx, y, z + dz) for x, z in ((ax, az), (bx, bz)) for dx, dz in ((-1.2, -1.2), (1.2, 1.2))
                for y in (YM - 4.0, YM - 1.6)], 'dark', bevel=0.15)            # diamond braces
    # corner caissons (footings from the cradle down to the sea bed side)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.cyl((sx * C, -30.0, sz * C), (sx * C, YC - 0.2, sz * C), 7.4, 16, 'paint2', rot=math.pi / 16, bevel=0.2)
    # front corners: low light drums at the waterline under the gantries
    for sx in (-1, 1):
        b.cyl((sx * 51.0, -6.0, 51.75), (sx * 51.0, 3.2, 51.75), 8.0, 16, 'paint', rot=math.pi / 16, bevel=0.3)
        b.cyl((sx * 51.0, 3.1, 51.75), (sx * 51.0, 3.6, 51.75), 6.6, 16, 'team', rot=math.pi / 16)
        b.box((sx * 51.0 - 1.2, 1.6, 59.6), (sx * 51.0 + 1.2, 2.6, 59.9), 'lightc', bevel=0.0)
    # back left: control house
    b.plan(-6.0, 12.0, [(-61.0, -61.0), (-43.0, -61.0), (-43.0, -43.0), (-61.0, -43.0)], 'paint', bevel=0.4,
           top_inset=1.4)
    b.hull([(x, 11.5, z) for x, z in ((-58.0, -58.0), (-46.0, -58.0), (-46.0, -46.0), (-58.0, -46.0))]
           + [(x, 21.0, z) for x, z in ((-57.0, -57.0), (-47.0, -57.0), (-47.0, -47.0), (-57.0, -47.0))], 'paint2',
           bevel=0.3)
    b.box((-57.3, 15.0, -57.3), (-46.7, 18.0, -46.7), 'lightc', bevel=0.1)
    b.box((-56.4, 20.9, -56.4), (-47.6, 21.6, -47.6), 'team', bevel=0.1)
    b.box((-59.4, 11.9, -59.4), (-44.6, 12.4, -44.6), 'hazard', bevel=0.05)
    b.cyl((-49.0, 21.5, -49.0), (-49.0, 31.0, -49.0), 0.6, 8, 'steel')
    # back right: beacon pylon (light piece on top)
    b.plan(-6.0, 8.6, [(45.0, -55.5), (55.0, -55.5), (55.0, -45.5), (45.0, -45.5)], 'paint', bevel=0.35,
           top_inset=1.2)
    b.box((46.4, 8.5, -54.1), (53.6, 9.0, -46.9), 'team', bevel=0.08)
    k.piece('light').box((48.2, 8.9, -52.0), (51.8, 12.4, -48.8), 'lightr', bevel=0.2)

    # ------------------------------------------------------------------ nano gantries (turret1 origin -51, -8.75, 51.75)
    t = k.piece('turret1'); T = t.at
    t.cyl(T(0, 12.0, 0), T(0, 14.5, 0), 5.6, 16, 'dark', rot=math.pi / 16, bevel=0.15)
    for sx in (-1, 1):                                                         # prongs the head rides between
        t.box(T(sx * 3.3 - 1.0, 14.0, -2.6), T(sx * 3.3 + 1.0, 37.5, 2.6), 'paint', bevel=0.3)
        t.box(T(sx * 3.3 - 0.8, 37.4, -2.2), T(sx * 3.3 + 0.8, 37.9, 2.2), 'hazard', bevel=0.05)
    t.box(T(-3.6, 34.0, 1.8), T(3.6, 36.0, 2.8), 'paint2', bevel=0.15)
    k.clone('turret2', 'turret1')
    n = k.piece('nano1'); N = n.at                                             # head; beam1 at (0, -11.12, 0)
    n.box(N(-2.2, -2.6, -2.8), N(2.2, 4.4, 2.8), 'steel', bevel=0.3)
    n.box(N(-2.0, 4.3, -2.4), N(2.0, 4.8, 2.4), 'hazard', bevel=0.05)
    n.cyl(N(0, -2.4, 0), N(0, -9.8, 0), 1.5, 10, 'dark', r2=1.1)
    n.cyl(N(0, -9.7, 0), N(0, -11.1, 0), 1.15, 10, 'lightc')
    k.clone('nano2', 'nano1')
