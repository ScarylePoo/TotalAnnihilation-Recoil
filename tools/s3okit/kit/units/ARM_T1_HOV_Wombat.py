"""Wombat (ARM_T1_HOV_Wombat) - Arm hover rocket artillery. Blunt rectangular barge on a black skirt; a long rocket
`Box` (2x3 big tube mouths at its front end) lies in a trough on the left half of the deck, hinged at its rear
bottom edge: on activation it swings up 90 deg (COB turn x) to stand vertical at the stern, like a VLS. The right
half carries a raised armoured deckhouse; the bow is a flat ramp.
Pieces (TA 3DO): GP (empty), Base (rocks x/z), Box (turn x), Flare (empty emit), Wake1..8 (empty).
Value groups from above: black skirt ring, light Arm deck + deckhouse, the launcher box as a long dark-blue
paint2 slab with a team stripe along its spine (team + dark = the artillery mark), hazard tube rims at its mouth,
big dark fan on the right rear, team plate on the deckhouse roof.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=4, pose={'Box': (-30, 0, 0)}),
    preview_pose={'Box': (-55, 0, 0)},
)


def rect(y, x, zr, zf, c):
    return [(x, y, zf - c), (x - c, y, zf), (-x + c, y, zf), (-x, y, zf - c),
            (-x, y, zr + c), (-x + c, y, zr), (x - c, y, zr), (x, y, zr + c)]


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ skirt
    b.hull(rect(0.0, 21.2, -23.0, 23.0, 5.0) + rect(2.8, 22.8, -24.4, 24.6, 5.4) + rect(5.6, 22.4, -24.0, 24.2, 5.2) +
           rect(7.2, 21.0, -22.8, 23.0, 4.8), 'tread', bevel=0.3)
    # ------------------------------------------------------------------ hull
    b.hull(rect(6.8, 20.4, -22.4, 18.4, 4.6) + rect(12.7, 19.3, -21.6, 14.0, 4.2) +
           [(x, 12.7, 20.1) for x in (-8.8, 8.8)] + [(x, 7.0, 22.6) for x in (-8.8, 8.8)], 'paint', bevel=0.2)
    b.hull(rect(7.0, 20.8, -22.8, 18.8, 4.7) + rect(8.8, 20.6, -22.6, 18.6, 4.7), 'paint2', bevel=0.08)
    # bow ramp hazard band (meaningful: a loading ramp)
    b.hull([(x, y, z) for x in (-7.6, 7.6) for y, z in ((12.76, 19.6), (8.6, 21.9), (12.9, 19.64), (8.74, 21.94))],
           'hazard', bevel=0.02)
    # trough for the launcher (left half): dark floor + raised rails either side
    b.box((-10.6, 12.6, -21.8), (-9.0, 15.0, 4.6), 'paint', bevel=0.12)
    b.box((0.4, 12.6, -21.8), (1.6, 15.0, 4.6), 'paint', bevel=0.12)
    # hinge block at the stern of the trough
    b.cyl((-9.2, 7.51, -22.36), (0.4, 7.51, -22.36), 2.2, 12, 'dark', bevel=0.08)
    # right half: raised deckhouse with team roof and slit windows
    b.hull([(1.8, 12.6, -3.6), (11.2, 12.6, -3.6), (1.8, 12.6, 9.0), (11.2, 12.6, 9.0),
            (2.4, 17.1, -3.0), (10.4, 17.1, -3.0), (2.4, 17.1, 7.8), (10.4, 17.1, 7.8)], 'paint', bevel=0.2)
    b.box((3.4, 17.05, -2.0), (9.4, 17.25, 6.8), 'team', bevel=0.04)
    b.hull([(2.5, 15.0, 8.2), (10.3, 15.0, 8.2), (2.6, 16.4, 7.85), (10.2, 16.4, 7.85),
            (2.5, 15.0, 8.34), (10.3, 15.0, 8.34), (2.6, 16.4, 7.99), (10.2, 16.4, 7.99)], 'glass', bevel=0.0)
    b.cyl((8.6, 17.2, 0.0), (8.6, 18.8, 0.0), 0.5, 8, 'dark')
    b.cyl((8.6, 18.8, 0.0), (8.6, 25.0, 0.0), 0.1, 6, 'steel', r2=0.05)
    b.cyl((8.6, 25.0, 0.0), (8.6, 25.2, 0.0), 0.16, 6, 'lightc')
    # right rear: one big lift fan
    x, z = 9.8, -13.2
    b.cyl((x, 12.2, z), (x, 13.8, z), 6.4, 18, 'dark', bevel=0.14)
    b.cyl((x, 13.8, z), (x, 13.85, z), 5.4, 18, 'black')
    for i in range(6):
        a = i * math.pi / 3 + 0.25
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (1.0, 5.1):
            for s in (-0.6, 0.6):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, 13.55, pz), (px, 13.85, pz)]
        b.hull(pts, 'steel', bevel=0.0)
    b.cyl((x, 13.5, z), (x, 14.2, z), 1.4, 12, 'paint', bevel=0.06)
    # left front deck: team plate ahead of the trough
    b.box((-15.6, 12.65, 6.6), (-3.0, 12.85, 13.6), 'team', bevel=0.04)
    # left outer deck between trough and edge: vents
    for zz in (-18.0, -13.0, -8.0, -3.0):
        b.box((-17.6, 12.65, zz), (-12.4, 12.95, zz + 2.6), 'dark', bevel=0.05)
    # lights
    b.box((3.4, 8.2, 21.4), (7.4, 9.8, 22.3), 'dark', bevel=0.05, mirror=True)
    b.box((3.7, 8.5, 22.26), (7.1, 9.5, 22.36), 'lightw', bevel=0.0, mirror=True)
    b.box((15.0, 9.4, -23.0), (17.6, 10.4, -22.6), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- Box (origin -4.39, 7.51, -22.36; turns x)
    bx = k.piece('Box'); B = bx.at
    top = 9.8
    bx.box(B(-4.6, 1.0, 0.8), B(4.6, top, 26.4), 'paint2', bevel=0.22)
    bx.box(B(-2.4, top - 0.05, 2.0), B(2.4, top + 0.22, 24.6), 'team', bevel=0.05)
    for sx in (-1, 1):   # dark side rails (origin is off-centre: no mirror)
        a, c = sorted((4.5 * sx, 5.1 * sx))
        bx.box(B(a, 5.4, 2.0), B(c, top - 1.0, 25.0), 'dark', bevel=0.06)
    # front face with 2x3 tube mouths
    bx.box(B(-4.2, 1.4, 26.3), B(4.2, top - 0.4, 26.6), 'dark', bevel=0.05)
    for x in (-2.6, 0.0, 2.6):
        for y in (3.3, 7.0):
            bx.cyl(B(x, y, 26.5), B(x, y, 27.1), 1.25, 10, 'hazard', bevel=0.03)
            bx.cyl(B(x, y, 27.1), B(x, y, 27.16), 0.85, 10, 'black')
    # hinge arms down to the pivot
    for sx in (-1, 1):
        a, c = sorted((3.4 * sx, 4.4 * sx))
        bx.box(B(a, -1.6, -1.2), B(c, 2.0, 3.6), 'dark', bevel=0.08)
