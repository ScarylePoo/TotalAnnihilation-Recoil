"""Construction Seaplane (CORE_T1_SEAPL_Constructor) - Core T1 sea builder, the biggest of the seaplanes. A wide
shark-nosed hull on two long float booms that reach far aft, with a pair of armoured striped bay doors on its back. The
two tall side panels stand up like sails on the water and fold out 90 deg in flight (COB turn z), turning into a huge
pair of swept wings at the very rear: from above a long dark dart with a big striped deck and team-coloured rear wings
(the Core T1 air builder is a box with stubby wings).
Pieces (TA layout): base, leftwing (+x; rightwing = mirrored clone), nanopoint (empty, emit point at the origin).
Value groups from above: dark warm hull, darker paint2 booms and fins, striped deck, team on the wing panels, light steel
hinges and nano ring, warm lights.
The panel's inner face (local -x) becomes the top in flight, so team sits on it and the outer face stays plain.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=39, drop=['rightwing'], pose={'leftwing': (0, 0, -35)}),
    preview_pose={'leftwing': (0, 0, -90), 'rightwing': (0, 0, 90)},     # flight (COB z values negated in the engine)
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ shark hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.5, 3.4, 27.0), (0.5, 4.6, 26.4), (4.0, 0.8, 17.0), (4.2, 7.4, 15.0),
             (8.6, 0.4, 5.0), (7.6, 10.6, 5.0), (10.0, 0.4, -12.0), (7.6, 10.6, -14.0),
             (6.0, 1.6, -22.0), (5.4, 8.8, -22.0)]], 'paint', bevel=0.2, seg=2)
    # cockpit glazing
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.0, 5.2, 25.0), (3.6, 7.6, 15.6), (4.2, 10.7, 7.0), (2.0, 11.2, 7.0), (0.9, 5.34, 25.1), (3.5, 7.74, 15.7)]],
           'glass', bevel=0.05)
    # ------------------------------------------------------------------ armoured bay doors in construction stripes
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.5, 10.5, 4.6), (7.5, 10.5, -14.4), (7.0, 11.8, 4.2), (7.0, 11.8, -14.0), (0.4, 12.6, 4.2), (0.4, 12.6, -14.0)]],
           'hazard', bevel=0.1)
    b.box((-0.45, 12.5, -14.1), (0.45, 12.85, 4.3), 'black', bevel=0.0)
    # rear deck, vents, nozzles
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 8.7, -21.8), (7.4, 10.5, -14.6), (5.2, 9.0, -21.8), (7.2, 10.8, -14.6)]], 'paint2', bevel=0.04)
    for z in (-16.4, -18.6):
        b.box((-4.6, 10.0 + (z + 16.4) * 0.26, z - 0.7), (4.6, 10.9 + (z + 16.4) * 0.26, z + 0.7), 'black', bevel=0.0)
    b.cyl((0, 5.2, -21.8), (0, 5.2, -24.0), 2.6, 12, 'dark', r2=2.2, bevel=0.04)
    b.cyl((0, 5.2, -23.95), (0, 5.2, -24.1), 1.6, 12, 'lightr')
    # ------------------------------------------------------------------ float booms (reach far aft; panel hinges on them)
    b.hull([(x, y, z) for x, y, z in
            [(7.6, 2.2, 3.0), (10.4, 2.6, 3.0), (7.6, 5.0, 1.0), (11.0, 5.0, 1.0),
             (7.2, 0.2, -12.0), (13.0, 0.6, -12.0), (7.2, 8.2, -12.0), (13.0, 8.2, -12.0),
             (7.8, 1.4, -35.0), (12.4, 1.8, -35.0), (8.2, 6.6, -35.0), (12.0, 6.6, -35.0)]], 'paint2', bevel=0.16, mirror=True)
    b.hull([(8.0, 8.26, -13.0), (12.6, 8.26, -13.0), (8.4, 6.8, -33.6), (11.8, 6.8, -33.6),
            (8.0, 8.5, -13.0), (12.6, 8.5, -13.0), (8.4, 7.04, -33.6), (11.8, 7.04, -33.6)], 'black', bevel=0.0, mirror=True)
    b.box((13.0, 2.4, -32.8), (13.5, 3.8, -4.4), 'steel', bevel=0.05, mirror=True)      # panel hinge rail
    b.box((9.0, 2.0, -36.0), (11.2, 5.0, -34.8), 'dark', bevel=0.05, mirror=True)
    b.box((9.4, 2.5, -36.15), (10.8, 4.5, -35.95), 'lightr', bevel=0.0, mirror=True)
    # twin tail fins
    b.hull([(4.0, 8.4, -11.0), (4.2, 7.8, -22.0), (4.8, 8.2, -11.0), (5.0, 7.6, -22.0),
            (6.4, 15.2, -20.0), (6.4, 15.2, -25.0), (7.0, 15.0, -20.0), (7.0, 15.0, -25.0)], 'paint2', bevel=0.07, mirror=True)
    b.box((6.2, 14.9, -25.0), (7.2, 15.5, -24.0), 'lightr', bevel=0.0, mirror=True)
    # nano ring around the origin on the belly (light steel, seen when it banks and from the side)
    b.cyl((0, 0.6, 0.0), (0, -0.5, 0.0), 3.4, 12, 'steel', r2=2.6, rot=math.pi / 12)
    b.cyl((0, -0.45, 0.0), (0, -0.7, 0.0), 1.8, 10, 'lightr')

    # ------------------------------------------------------------------ side panel (leftwing at +x; rightwing = mirror)
    w = k.piece('leftwing'); W = w.at
    out = [(0.0, 17.5), (0.0, -17.0), (14.2, -18.3), (14.2, -5.0)]
    w.hull([W(x, y, z) for y, z in out for x in (-1.1, -0.15)], 'paint2', bevel=0.08)
    w.hull([W(x, y, z) for y, z in ((2.2, 10.8), (2.2, -13.4), (12.4, -15.4), (12.4, -7.8)) for x in (-1.3, -1.12)], 'team', bevel=0.0)
    w.cyl(W(-0.6, 14.2, -4.6), W(-0.6, 14.2, -18.6), 0.7, 8, 'dark', r2=0.55, rot=math.pi / 8)
    w.cyl(W(-0.6, 14.2, -4.2), W(-0.6, 14.2, -4.62), 0.4, 8, 'lightr', r2=0.7)
    k.clone('rightwing', 'leftwing', mirror_x=True)
