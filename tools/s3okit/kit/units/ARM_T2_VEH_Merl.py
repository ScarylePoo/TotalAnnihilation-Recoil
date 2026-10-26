"""Merl (ARM_T2_VEH_Merl) - Arm mobile (long-range) rocket launcher. Six... no: four huge wheels in armoured fender
pods at the corners, a driver's cab and spine on the left, and a long launch bay right of centre closed by two lids.
When it deploys (COB activate) the lids (door1/door2) flip 90 deg on their outer hinges and sink 6.4 into the bay
walls, the plate (bay floor) rises 7.75 and the arm swings the one big rocket upright (arm turn x -90).
The base is built AROUND the bay (x -2.4..9.8, y 6.2..14.5, z -23.3..12.2): the rocket lies inside when stowed.
Value groups from above: light fender pods + cab spine, two long team-coloured lids (the read: a big team slab
offset right, with a dark seam), dark bay liners/chassis, black tyres; the rocket is light with a hazard warhead
and stands as a tall white column when deployed.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=19, remove=['rocket'], drop=['door2']),
    preview_pose={},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ wheels + fender pods (symmetric)
    for z in (13.6, -13.6):
        b.cyl((15.2, 6.6, z), (22.4, 6.6, z), 6.6, 16, 'tread', rot=math.pi / 16, bevel=0.18, mirror=True)
        b.cyl((22.4, 6.6, z), (22.9, 6.6, z), 3.8, 12, 'dark', bevel=0.06, mirror=True)
        b.cyl((22.9, 6.6, z), (23.2, 6.6, z), 1.4, 8, 'steel', mirror=True)
        # faceted fender arching over the wheel
        b.hull([(14.4, 13.6, z - 5.0), (23.6, 13.6, z - 5.0), (14.4, 13.6, z + 5.0), (23.6, 13.6, z + 5.0),
                (14.4, 10.4, z - 8.6), (23.6, 10.4, z - 8.6), (14.4, 10.4, z + 8.6), (23.6, 10.4, z + 8.6),
                (14.4, 11.6, z - 8.2), (23.6, 11.6, z - 8.2), (14.4, 11.6, z + 8.2), (23.6, 11.6, z + 8.2)],
               'paint', bevel=0.18, mirror=True)
        b.box((15.6, 13.6, z - 3.6), (22.4, 13.82, z + 3.6), 'team' if z > 0 else 'paint2', bevel=0.05, mirror=True)
    # dark axle/suspension block between the pods (reads as the gap)
    b.box((12.6, 3.2, -18.0), (15.2, 9.4, 18.0), 'dark', bevel=0.12, mirror=True)
    # chassis tub (crosses x = 0)
    b.prism(-13.2, 13.2, [(-24.0, 3.0), (22.6, 3.0), (25.0, 5.4), (24.2, 7.0), (-24.4, 7.0), (-25.0, 5.0)], 'paint2', bevel=0.16)

    # ------------------------------------------------------------------ left: driver's spine + cab
    b.hull([(-13.6, 7.0, -24.6), (-2.6, 7.0, -24.6), (-13.6, 7.0, 22.0), (-2.6, 7.0, 22.0),
            (-12.8, 15.2, -23.6), (-2.6, 15.2, -23.6), (-12.8, 15.2, 4.0), (-2.6, 15.2, 4.0)], 'paint', bevel=0.18)
    # cab block at the front left, rising highest, raked windscreen
    b.hull([(-13.6, 7.0, 4.0), (-2.6, 7.0, 4.0), (-13.6, 7.0, 24.4), (-2.6, 7.0, 24.4),
            (-12.6, 18.6, 4.4), (-3.4, 18.6, 4.4), (-12.6, 18.6, 13.0), (-3.4, 18.6, 13.0),
            (-12.8, 12.6, 22.6), (-3.2, 12.6, 22.6)], 'paint', bevel=0.18)
    b.hull([(-11.8, 18.0, 13.8), (-4.2, 18.0, 13.8), (-11.8, 13.4, 21.6), (-4.2, 13.4, 21.6),
            (-11.8, 18.12, 13.9), (-4.2, 18.12, 13.9), (-11.8, 13.52, 21.7), (-4.2, 13.52, 21.7)], 'glass', bevel=0.03)
    b.box((-11.6, 18.6, 5.4), (-4.4, 18.82, 11.8), 'dark', bevel=0.04)         # cab roof hatch
    # equipment boxes along the spine top
    b.box((-12.0, 15.2, -21.6), (-4.0, 16.4, -15.0), 'dark', bevel=0.1)
    for z in (-21.0, -19.6, -18.2, -16.8):
        b.box((-11.6, 16.4, z), (-4.4, 16.52, z + 0.6), 'black', bevel=0.0)
    b.box((-12.0, 15.2, -11.6), (-4.0, 15.42, 2.4), 'paint2', bevel=0.05)
    # antenna on the spine
    b.cyl((-11.0, 16.4, -13.0), (-11.0, 17.0, -13.0), 0.38, 8, 'dark')
    b.cyl((-11.0, 17.0, -13.0), (-11.0, 23.6, -13.0), 0.1, 6, 'steel', r2=0.05)
    b.cyl((-11.0, 23.6, -13.0), (-11.0, 23.8, -13.0), 0.16, 6, 'lightc')

    # ------------------------------------------------------------------ right of the bay + its ends
    b.hull([(9.8, 7.0, -24.6), (14.4, 7.0, -24.6), (9.8, 7.0, 22.0), (14.4, 7.0, 22.0),
            (9.8, 14.4, -23.6), (14.0, 14.4, -23.6), (9.8, 14.4, 12.2), (14.0, 14.4, 12.2)], 'paint', bevel=0.16)
    # bay front block (hood): x -2.6..9.8, z 12.2..24
    b.hull([(-2.6, 7.0, 12.2), (14.4, 7.0, 12.2), (-2.6, 7.0, 24.6), (14.4, 7.0, 24.6),
            (-2.6, 14.6, 12.2), (14.0, 14.6, 12.2), (-2.6, 12.0, 23.0), (14.0, 12.0, 23.0)], 'paint', bevel=0.18)
    b.hull([(x, y, z) for x in (-1.6, 12.6) for y, z in [(12.14, 22.6), (12.6, 20.75), (12.28, 22.7), (12.74, 20.85)]],
           'hazard', bevel=0.03)
    b.box((1.0, 8.6, 24.3), (11.0, 11.0, 24.9), 'dark', bevel=0.06)
    b.box((1.6, 9.0, 24.88), (10.4, 10.6, 24.98), 'lightw', bevel=0.0)
    # bay rear wall
    b.box((-2.6, 7.0, -24.6), (9.8, 14.4, -23.3), 'paint', bevel=0.12)
    # rear plate + lights
    b.box((-12.0, 8.0, -25.2), (13.0, 12.6, -24.6), 'dark', bevel=0.06)
    for x in (-10.8, 10.4):
        b.box((x, 10.8, -25.3), (x + 1.4, 11.6, -25.15), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- plate (bay floor; rises 7.75)
    p = k.piece('plate')
    p.box((-2.2, 5.0, -23.0), (9.4, 6.2, 11.8), 'paint2', bevel=0.1)
    for z0 in (-22.6, 8.6):
        p.box((-1.8, 6.2, z0), (9.0, 6.36, z0 + 2.8), 'hazard', bevel=0.02)

    # ---------------------------------------------------------------- arm (launch rail, pivot at the rear)
    a = k.piece('arm'); A = a.at
    for z0, z1 in ((-0.8, 9.6), (9.6, 20.0), (20.0, 30.4)):
        a.box(A(-3.0, -0.2, z0), A(0.6, 1.4, z1), 'dark', bevel=0.1)
    a.cyl(A(-3.2, 0.6, 0.0), A(0.8, 0.6, 0.0), 1.2, 12, 'steel')
    for z in (5.0, 15.0, 25.0):
        a.box(A(-4.2, 0.4, z - 0.8), A(-2.9, 3.4, z + 0.8), 'paint2', bevel=0.06)

    # ---------------------------------------------------------------- rocket (centre 1.35, 7.47, -4.66)
    r = k.piece('rocket'); R = r.at
    yc = 1.4
    r.cyl(R(0, yc, -14.2), R(0, yc, 10.0), 1.85, 12, 'paint')
    r.cyl(R(0, yc, 10.0), R(0, yc, 14.6), 1.85, 12, 'hazard', r2=0.35)
    r.cyl(R(0, yc, 1.6), R(0, yc, 4.4), 1.9, 12, 'team')
    r.cyl(R(0, yc, -14.9), R(0, yc, -14.2), 1.2, 10, 'dark', r2=1.6)
    for ang in (math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4):
        dx, dy = math.cos(ang), math.sin(ang)
        r.hull([R(dx * rr, yc + dy * rr, z) for rr in (1.6, 2.6) for z in (-13.8, -10.2)] +
               [R(dx * rr - dy * 0.15, yc + dy * rr + dx * 0.15, z) for rr in (1.6, 2.6) for z in (-13.8, -10.2)],
               'dark', bevel=0.0)

    # ---------------------------------------------------------------- lids (hinged on their outer edges)
    # each lid in three segments: one 35-elmo strip packs badly (it ended up diagonal across the UV sheet)
    segs = ((-17.7, -5.9), (-5.9, 5.9), (5.9, 17.7))
    d = k.piece('door1'); D = d.at
    for z0, z1 in segs:
        d.hull([D(x, y, z) for x, y, z in
                [(0.0, 0.0, z0), (6.0, 0.0, z0), (0.0, 0.0, z1), (6.0, 0.0, z1),
                 (0.2, 1.8, z0 + 0.25), (6.0, 2.1, z0 + 0.25), (0.2, 1.8, z1 - 0.25), (6.0, 2.1, z1 - 0.25)]], 'paint2', bevel=0.1)
        d.box(D(0.0, -0.4, z0 + 0.3), D(0.6, 0.2, z1 - 0.3), 'dark', bevel=0.04)
    d.hull([D(x, y + dy, z) for x, y in ((3.2, 2.06), (5.6, 2.16)) for dy in (0.06, 0.2) for z in (-15.6, 15.6)], 'team', bevel=0.03)
    e = k.piece('door2'); E = e.at
    for z0, z1 in segs:
        e.hull([E(x, y, z) for x, y, z in
                [(-6.0, 0.0, z0), (0.0, 0.0, z0), (-6.0, 0.0, z1), (0.0, 0.0, z1),
                 (-6.0, 2.1, z0 + 0.25), (-0.2, 1.8, z0 + 0.25), (-6.0, 2.1, z1 - 0.25), (-0.2, 1.8, z1 - 0.25)]], 'paint2', bevel=0.1)
        e.box(E(-0.6, -0.4, z0 + 0.3), E(0.0, 0.2, z1 - 0.3), 'dark', bevel=0.04)
    e.hull([E(x, y + dy, z) for x, y in ((-3.2, 2.06), (-5.6, 2.16)) for dy in (0.06, 0.2) for z in (-15.6, 15.6)], 'team', bevel=0.03)
