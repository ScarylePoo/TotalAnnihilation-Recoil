"""Retaliator (ARM_T2_DEF_Retaliator) - Arm nuclear missile silo. A big light sloped bunker with a long silo slot down
its middle, closed by two hazard-striped nuke doors, and two sensor domes at the rear corners. To launch, the doors
swing up and sink into the walls, the elevator deck (plate) rises 20 elmo flush with the roof and the cradle (arm)
erects the huge missile to vertical.
Identity from above: closed = a big light square with a long yellow-black double door down the middle and two team
deck stripes either side of it; open = the same square with a dark lift deck, a team panel and the missile standing
up at the rear - the only hazard is on the nuke doors and the lift-deck edges.
Pieces (COB): base, plate (move y), arm (turn x, move x/z), missile (hide/show: the nuke), door1/2 (turn z, move y),
domes. The preview shows the OPEN state (doors up and sunk, deck raised, missile erected).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=29, drop=['door2'], remove=['missile']),
    preview_pose={'door1': {'move': (0, -15.25, 0), 'rot': (0, 0, 90)}, 'door2': {'move': (0, -15.25, 0), 'rot': (0, 0, -90)},
                  'plate': {'move': (0, 20.0, 0)}, 'arm': (-90, 0, 0)},
)

TOP = 20.4
SX, Z0, Z1 = 14.6, -25.7, 29.4        # silo slot half-width and z range


def build(k):
    # ------------------------------------------------------------------ base: bunker round the silo slot
    b = k.piece('base')
    b.plan(0.0, 3.0, [(-35.0, -31.0), (-31.0, -35.0), (31.0, -35.0), (35.0, -31.0), (35.0, 31.0), (31.0, 35.0),
                      (-31.0, 35.0), (-35.0, 31.0)], 'paint2', bevel=0.3, top_inset=1.0)
    for s in (-1, 1):       # side blocks: outer face sloped, inner face vertical (the slot wall)
        b.hull([(s * x, y, z) for x, y, zs in ((33.0, 2.8, 33.0), (SX, 2.8, 33.0), (28.0, TOP, 30.0), (SX, TOP, 30.0))
                for z in (-zs, zs)], 'paint', bevel=0.35)
    b.hull([(x, y, z) for x in (-SX - 0.5, SX + 0.5) for y, z in ((2.8, 33.0), (TOP, 30.0), (2.8, Z1), (TOP, Z1))], 'paint', bevel=0.3)
    b.hull([(x, y, z) for x in (-SX - 0.5, SX + 0.5) for y, z in ((2.8, -33.0), (TOP, -30.0), (2.8, Z0), (TOP, Z0))], 'paint', bevel=0.3)
    # silo pit
    b.box((-SX, 0.6, Z0), (SX, 1.2, Z1), 'black', bevel=0.0)
    for s in (-1, 1):
        b.box((s * SX - 0.4 if s > 0 else -SX, 1.0, Z0), (SX if s > 0 else -SX + 0.4, TOP - 0.2, Z1), 'dark', bevel=0.0)
    # team deck stripes either side of the slot, dark door coamings
    for s in (-1, 1):
        b.box((min(s * 17.4, s * 25.0), TOP - 0.1, -22.0), (max(s * 17.4, s * 25.0), TOP + 0.18, 16.0), 'team', bevel=0.04)
        b.box((min(s * SX, s * (SX + 1.6)), TOP - 0.1, Z0 - 1.6), (max(s * SX, s * (SX + 1.6)), TOP + 0.5, Z1 + 1.6), 'dark', bevel=0.06)
    # front face: armoured hatch and a light
    b.hull([(x, y, z) for x in (-8.0, 8.0) for y, z in ((3.0, 32.6), (14.0, 30.8), (3.0, 31.0), (14.0, 29.8))], 'paint2', bevel=0.2)
    b.box((-1.0, 15.6, 30.2), (1.0, 16.8, 30.8), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ domes: two sensor domes at the rear corners
    dm = k.piece('domes')
    for s in (-1, 1):
        c = (s * 22.0, TOP, 23.0)
        dm.cyl(c, (c[0], TOP + 1.6, c[2]), 5.6, 12, 'dark', bevel=0.08)
        dm.sphere((c[0], TOP + 1.6, c[2]), 4.8, 'steel', segs=12, rings=5, scale=(1, 0.9, 1))
        dm.cyl((c[0], TOP + 5.4, c[2]), (c[0], TOP + 5.75, c[2]), 2.2, 10, 'team')
        dm.box((c[0] - 0.5, TOP + 2.6, c[2] + 4.3), (c[0] + 0.5, TOP + 3.4, c[2] + 4.9), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ doors: the nuke doors (door1 hinge x -14.64)
    d = k.piece('door1'); D = d.at
    d.box(D(0.0, -0.4, Z0 + 0.4), D(SX - 0.2, 1.4, Z1 - 0.4), 'dark', bevel=0.15)
    d.box(D(0.8, 1.3, Z0 + 1.6), D(SX - 1.0, 1.6, Z1 - 1.6), 'hazard', bevel=0.04)
    d.cyl(D(0.0, 0.5, Z0 + 2.0), D(0.0, 0.5, Z1 - 2.0), 1.0, 8, 'steel', bevel=0.04)
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ plate: the elevator deck (origin 0, 0.18, 0)
    p = k.piece('plate')
    p.box((-SX + 0.4, -1.2, Z0 + 0.4), (SX - 0.4, 0.0, Z1 - 0.4), 'paint2', bevel=0.15)
    for s in (-1, 1):   # lift-edge hazard strips
        p.box((min(s * (SX - 0.6), s * (SX - 3.6)), -0.1, Z0 + 0.8), (max(s * (SX - 0.6), s * (SX - 3.6)), 0.12, Z1 - 0.8),
              'hazard', bevel=0.02)
    p.box((-9.0, -0.1, 3.0), (9.0, 0.14, 25.0), 'team', bevel=0.03)

    # ------------------------------------------------------------------ arm: the erector cradle (origin -7.35, 0.18, -11.02)
    a = k.piece('arm'); A = a.at
    a.box(A(-3.6, 0.0, -1.0), A(1.2, 4.0, 34.6), 'dark', bevel=0.2)               # strongback
    for z in (4.0, 16.0, 28.0):                                                  # clamps
        a.box(A(1.0, 0.6, z), A(8.6, 2.6, z + 2.4), 'steel', bevel=0.08)
    a.cyl(A(-3.8, 1.2, 0.0), A(9.0, 1.2, 0.0), 1.8, 8, 'steel', bevel=0.05)        # pivot

    # ------------------------------------------------------------------ missile: the nuke (origin 4.81, 1.36, -10.95)
    m = k.piece('missile'); M = m.at
    m.cyl(M(0, 5.0, 0.4), M(0, 5.0, 30.0), 4.6, 12, 'paint', bevel=0.06)
    m.cyl(M(0, 5.0, 30.0), M(0, 5.0, 39.4), 4.6, 12, 'steel', r2=0.8, bevel=0.05)
    m.cyl(M(0, 5.0, 26.0), M(0, 5.0, 30.0), 4.7, 12, 'hazard')
    m.cyl(M(0, 5.0, 0.0), M(0, 5.0, 1.2), 3.4, 12, 'black')
    for ang in (45, 135, 225, 315):
        aa = math.radians(ang)
        m.hull([M(math.cos(aa) * rr, 5.0 + math.sin(aa) * rr, z) for rr in (3.4, 5.9) for z in (0.6, 7.0)] +
               [M(math.cos(aa) * 3.4, 5.0 + math.sin(aa) * 3.4, 12.0)], 'dark', bevel=0.05)
