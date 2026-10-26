"""Construction Hovercraft (CORE_T1_HOV_Constructor) - Core hover builder. Low arrowhead hull on a black skirt: a
long pointed bow, broad angular side sponsons with lift fans and two swept tail fins at the stern (Core spikiness).
A raised bay on the spine is closed by two flat doors that flip ~210 deg outwards about the centre-line edges
(door1/door2 turn z) to lie on the sponsons; the `boom` then pitches up 43 deg about its front pivot, the `neck`
counter-rotates to keep the `gun` (nano projector) level and the gun turns y; `beam` (empty) is the emit point.
Value groups from above: black skirt, dark warm sponsons/bow (paint), darker paint2 spine bay, team plates on the
doors (wide, the spine read), light steel nano gear, ochre hazard on the tail fins and bay sills.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=8, pose={'door2': (0, 0, 120), 'gun': (0, 30, 0)}),
    preview_pose={},
)

OUT = [(2.0, 28.6), (8.6, 25.8), (18.4, 8.6), (18.8, -7.0), (12.2, -28.0), (3.0, -29.0)]


def outline(y, d=0.0):
    pts = []
    for x, z in OUT:
        L = math.hypot(x - 6, z) or 1
        p = (x + (x - 6) / L * d, y, z + z / L * d)
        pts += [p, (-p[0], y, p[2])]
    return pts


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ skirt
    b.hull(outline(0.0, 0.0) + outline(2.6, 1.6) + outline(4.6, 1.2) + outline(5.8, 0.2), 'tread', bevel=0.3)
    # ------------------------------------------------------------------ hull: low arrowhead, sloped sides
    b.hull(outline(5.4, -0.6) + [(x * sx, 9.8, z) for sx in (-1, 1) for x, z in
                                  [(1.4, 25.0), (7.4, 21.6), (15.2, 7.0), (15.4, -6.2), (10.2, -25.6), (2.6, -26.6)]],
           'paint', bevel=0.22)
    # dark band at the skirt join
    b.hull(outline(5.2, 0.0) + outline(6.4, -0.1), 'steel', bevel=0.08)
    # lift fans in the sponsons
    for x, z in ((11.4, -0.4),):
        b.cyl((x, 9.2, z), (x, 10.4, z), 4.6, 16, 'dark', bevel=0.12, mirror=True)
        b.cyl((x, 10.4, z), (x, 10.45, z), 3.7, 16, 'black', mirror=True)
        for i in range(3):
            a = i * 2 * math.pi / 3 + 0.9
            ca, sa = math.cos(a), math.sin(a)
            pts = []
            for d in (0.9, 3.5):
                for s in (-0.8, 0.8):
                    px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                    pts += [(px, 10.15, pz), (px, 10.45, pz)]
            b.hull(pts, 'steel', bevel=0.0, mirror=True)
        b.cyl((x, 10.1, z), (x, 10.8, z), 1.1, 10, 'steel', bevel=0.05, mirror=True)
    # spine bay walls (raised housing the doors close over), darker
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.8, 9.6, -15.6), (7.8, 9.6, 12.6), (5.6, 13.6, -12.0), (5.6, 13.6, 10.6), (3.0, 9.6, 16.4), (2.4, 12.4, 13.6)]],
           'paint2', bevel=0.2)
    # bay floor (visible when open)
    b.box((-4.8, 13.5, -11.4), (4.8, 13.62, 10.2), 'dark', bevel=0.0)
    # hazard sills along the bay edges
    b.box((5.0, 13.4, -12.0), (5.9, 13.75, 10.6), 'hazard', bevel=0.03, mirror=True)
    # bow: windows + lights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 11.2, 15.6), (1.2, 10.4, 19.4), (2.2, 11.32, 15.72), (1.2, 10.52, 19.52)]], 'glass', bevel=0.03)
    b.box((5.6, 6.2, 22.6), (7.8, 7.6, 23.6), 'dark', bevel=0.05, mirror=True)
    b.hull([(5.8, 6.4, 23.55), (7.6, 6.4, 23.1), (5.8, 7.4, 23.55), (7.6, 7.4, 23.1),
            (5.8, 6.4, 23.67), (7.6, 6.4, 23.22), (5.8, 7.4, 23.67), (7.6, 7.4, 23.22)], 'lightw', bevel=0.0, mirror=True)
    # stern: two swept tail fins with ochre hazard tips (Core spikes), exhaust block
    b.hull([(4.4, 9.6, -26.0), (4.4, 9.6, -16.4), (5.2, 9.6, -16.0), (5.6, 16.7, -26.2), (5.6, 16.3, -19.6),
            (4.4, 11.0, -28.4)], 'paint', bevel=0.1, mirror=True)
    b.hull([(4.3, 14.6, -25.8), (6.0, 14.6, -25.8), (4.3, 14.4, -22.0), (6.0, 14.4, -22.0),
            (5.4, 16.8, -26.4), (5.9, 16.8, -26.4), (5.4, 16.4, -19.4), (5.9, 16.4, -19.4)], 'hazard', bevel=0.03, mirror=True)
    b.box((-3.6, 6.4, -29.0), (3.6, 10.6, -26.8), 'dark', bevel=0.1)
    b.box((-2.4, 9.4, -29.1), (-1.2, 10.2, -28.9), 'lightr', bevel=0.0)
    b.box((1.2, 9.4, -29.1), (2.4, 10.2, -28.9), 'lightr', bevel=0.0)
    # antenna
    b.cyl((-13.0, 9.6, -12.0), (-13.0, 10.4, -12.0), 0.35, 8, 'dark')
    b.cyl((-13.0, 10.4, -12.0), (-13.0, 17.0, -12.0), 0.09, 6, 'steel', r2=0.04)
    b.cyl((-13.0, 17.0, -12.0), (-13.0, 17.2, -12.0), 0.14, 6, 'lightr')

    # ------------------------------------------------------------------ doors: flat plates, hinge on the centre line
    d = k.piece('door2'); D = d.at          # origin (5.52, 13.68, 0), plate spans x -5.5..0 (towards the centre)
    d.box(D(-5.45, -0.05, -11.6), D(-0.1, 0.75, 10.3), 'paint', bevel=0.14)
    d.box(D(-4.6, 0.7, -9.8), D(-0.9, 0.92, 8.6), 'team', bevel=0.04)
    d.box(D(-5.4, -0.25, -11.0), D(-0.2, 0.0, 9.8), 'dark', bevel=0.04)    # underside ribbing (seen when open)
    k.clone('door1', 'door2', mirror_x=True)

    # ------------------------------------------------------------------ boom / neck / gun (nano gear: light steel)
    bm = k.piece('boom'); B = bm.at                  # pivot at the front, arm runs back 12.9
    bm.cyl(B(-1.8, 0, 0), B(1.8, 0, 0), 1.3, 12, 'dark', bevel=0.05)
    bm.box(B(-1.2, -0.8, -12.6), B(1.2, 1.0, 0.4), 'steel', bevel=0.12)
    n = k.piece('neck'); N = n.at
    n.cyl(N(-1.6, 0, 0), N(1.6, 0, 0), 1.2, 12, 'dark', bevel=0.05)
    n.box(N(-1.1, 0.0, -1.0), N(1.1, 2.4, 1.0), 'steel', bevel=0.1)
    g = k.piece('gun'); G = g.at
    g.cyl(G(0, -0.6, 0), G(0, 0.2, 0), 2.0, 12, 'dark', bevel=0.05)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 0.0, -7.6), (3.2, 0.0, 2.4), (2.4, 2.6, -6.6), (2.0, 2.6, 2.2), (1.8, 0.4, 5.0)]], 'steel', bevel=0.16)
    g.cyl(G(0, 1.0, 3.8), G(0, 1.0, 10.6), 1.0, 10, 'steel', bevel=0.04)
    g.cyl(G(0, 1.0, 10.4), G(0, 1.0, 11.9), 1.6, 10, 'dark', r2=1.1, bevel=0.05)
    g.cyl(G(0, 1.0, 11.9), G(0, 1.0, 12.2), 0.8, 10, 'lightc')
    g.box(G(-1.4, 2.55, -5.6), G(1.4, 2.75, 1.4), 'hazard', bevel=0.03)
