"""Advanced Shipyard (ARM_T2_LAB_AdvancedShipyard) - Arm T2 ship factory: the T1 Arm floating dock grown bigger.
Waterline 1 (the water surface is model y = 1). A double square cradle under water (outer pontoon beams 0.6 under the
surface at the corners dipping 7 at the side middles where ships cross, plus an inner team/hazard ring) and four light
corner towers in the yardmap's `w` corner cells: two tall control towers with cyan cabs and team caps (back corners)
and two nano gantries (front corners: piling1/piling2 turn to face the slip, the nano heads rise 19 between their
prongs and tip down toward it). Everything between the corners stays under water (the yardmap is open `C` there):
ships are built at `slip` (centre, y -8.75) and sail out over the beams.
Arm lab family (T2 = taller, more parts): light chamfered blocks, team caps, hazard on the builder parts, cyan lights.
Identity from above: four light corner towers - two tall ones at the back - round a double square seen through the
water (the T1 shipyard has one tall house; the Core yards are dark and massive).
Pieces (COB): base, piling1/2 (turn y), nano1/2 (move y, turn x), beam1/2 (empty nano emit points), slip (empty;
QueryBuildInfo), explode1/explode2 (empty debris points).
Preview: OPEN (activatescr end state).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    ground=False, water=1.0,
    always_visible=['nano1', 'nano2'],
    wreck=dict(seed=79, drop=['piling2']),
    preview_pose={
        'nano1': {'move': (0, 19.125, 0), 'rot': (58.05, 0, 0)},
        'nano2': {'move': (0, 19.5, 0), 'rot': (58.05, 0, 0)},
        'piling1': (0, -52.65, 0), 'piling2': (0, 47.7, 0),
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
    Ci = 40.0                                                                 # inner ring, deeper
    for i, ((ax, az), (bx, bz)) in enumerate((((-Ci, -Ci), (Ci, -Ci)), ((Ci, -Ci), (Ci, Ci)), ((Ci, Ci), (-Ci, Ci)),
                                              ((-Ci, Ci), (-Ci, -Ci)))):
        beam(b, (ax, YM - 4.0, az), (bx, YM - 4.0, bz), 4.0, 'team' if i == 0 else 'paint')
    for sx in (-1, 1):                                                        # cross ties ring -> cradle corners
        for sz in (-1, 1):
            beam(b, (sx * Ci, YM - 4.0, sz * Ci), (sx * (C - 5.0), YC - 2.0, sz * (C - 5.0)), 3.0, 'dark')
    # corner caissons (footings from the cradle down to the sea bed side)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.cyl((sx * C, -30.0, sz * C), (sx * C, YC - 0.2, sz * C), 7.4, 16, 'paint2', rot=math.pi / 16, bevel=0.2)
    # front corners: low light drums at the waterline under the gantries
    for sx in (-1, 1):
        b.cyl((sx * 51.0, -6.0, 51.25), (sx * 51.0, 3.2, 51.25), 8.0, 16, 'paint', rot=math.pi / 16, bevel=0.3)
        b.cyl((sx * 51.0, 3.1, 51.25), (sx * 51.0, 3.6, 51.25), 6.6, 16, 'team', rot=math.pi / 16)
        b.box((sx * 51.0 - 1.2, 1.6, 59.6), (sx * 51.0 + 1.2, 2.6, 59.9), 'lightc', bevel=0.0)
    # back corners: two tall control towers (mirrored)
    b.plan(-6.0, 14.0, [(-61.0, -61.0), (-43.0, -61.0), (-43.0, -43.0), (-61.0, -43.0)], 'paint', bevel=0.4,
           top_inset=1.4, mirror=True)
    b.box((-59.4, 13.9, -59.4), (-44.6, 14.4, -44.6), 'hazard', bevel=0.05, mirror=True)
    b.hull([(x, 13.5, z) for x, z in ((-58.0, -58.0), (-46.0, -58.0), (-46.0, -46.0), (-58.0, -46.0))]
           + [(x, 34.0, z) for x, z in ((-56.0, -56.0), (-48.0, -56.0), (-48.0, -48.0), (-56.0, -48.0))], 'paint',
           bevel=0.35, mirror=True)
    b.hull([(x, 33.5, z) for x, z in ((-57.0, -57.0), (-47.0, -57.0), (-47.0, -47.0), (-57.0, -47.0))]
           + [(x, 40.0, z) for x, z in ((-58.0, -58.0), (-46.0, -58.0), (-46.0, -46.0), (-58.0, -46.0))], 'paint2',
           bevel=0.3, mirror=True)
    b.box((-58.3, 36.0, -58.3), (-45.7, 38.4, -45.7), 'lightc', bevel=0.1, mirror=True)
    b.hull([(x, 39.9, z) for x, z in ((-58.0, -58.0), (-46.0, -58.0), (-46.0, -46.0), (-58.0, -46.0))]
           + [(x, 44.0, z) for x, z in ((-55.0, -55.0), (-49.0, -55.0), (-49.0, -49.0), (-55.0, -49.0))], 'team',
           bevel=0.25, mirror=True)
    b.box((-52.8, 43.9, -52.8), (-51.2, 46.0, -51.2), 'lightr', bevel=0.1, mirror=True)

    # ------------------------------------------------------------------ nano gantries (piling1 origin -51, -8.75, 51.25)
    t = k.piece('piling1'); T = t.at
    t.cyl(T(0, 12.0, 0), T(0, 14.5, 0), 5.6, 16, 'dark', rot=math.pi / 16, bevel=0.15)
    for sx in (-1, 1):                                                         # prongs the head rides between
        t.box(T(sx * 3.3 - 1.2, 14.0, -2.8), T(sx * 3.3 + 1.2, 40.5, 2.8), 'paint', bevel=0.3)
        t.box(T(sx * 3.3 - 1.0, 40.4, -2.4), T(sx * 3.3 + 1.0, 40.9, 2.4), 'hazard', bevel=0.05)
    t.box(T(-3.6, 34.0, 1.8), T(3.6, 36.0, 2.8), 'paint2', bevel=0.15)
    k.clone('piling2', 'piling1')
    n = k.piece('nano1'); N = n.at                                             # head; beam1 at (0, -11.12, 0)
    n.box(N(-2.2, -2.6, -2.8), N(2.2, 4.4, 2.8), 'steel', bevel=0.3)
    n.box(N(-2.0, 4.3, -2.4), N(2.0, 4.8, 2.4), 'hazard', bevel=0.05)
    n.cyl(N(0, -2.4, 0), N(0, -9.8, 0), 1.5, 10, 'dark', r2=1.1)
    n.cyl(N(0, -9.7, 0), N(0, -11.1, 0), 1.15, 10, 'lightc')
    k.clone('nano2', 'nano1')
