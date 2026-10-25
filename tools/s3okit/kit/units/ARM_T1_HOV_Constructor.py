"""Construction Hovercraft (ARM_T1_HOV_Constructor) - Arm hover builder. Two long lens-shaped side hulls with a
big lift fan each, joined by a raised central bay housing with a pointed glazed bow; the bay roof is two sloped
doors (door1/door2 turn z ~67 deg about their outer edges and drop 5). When building, `plate` (the bay floor) rises
10 to deck level, `turret` turns y, `post` swings up 90 deg (turn x) and the `nanogun` lathe stays level on top of
it (turn x -90); `beam` (empty) is the nano emit point at the lathe tip.
Value groups from above: black skirt ring, light Arm side hulls with team plates on their bows, dark fan discs,
dark paint2 bay doors with yellow hazard edges along the ridge (construction gear), dark stern engine block.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=3, pose={'door2': (0, 0, 40), 'turret': (0, 30, 0)}),
    preview_pose={},
)


def fan(b, x, z, y0, y1, r, blades=4):
    b.cyl((x, y0, z), (x, y1, z), r + 0.9, 16, 'dark', bevel=0.12, mirror=True)
    b.cyl((x, y1, z), (x, y1 + 0.05, z), r, 16, 'black', mirror=True)
    for i in range(blades):
        a = i * 2 * math.pi / blades + 0.5
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.9, r - 0.25):
            for s in (-0.6, 0.6):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, y1 - 0.25, pz), (px, y1 + 0.05, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    b.cyl((x, y1 - 0.2, z), (x, y1 + 0.35, z), 1.1, 10, 'paint', bevel=0.06, mirror=True)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ skirt
    def ring(y, rx, rz, c):
        return [(rx, y, rz - c * 1.6), (rx - c, y, rz), (-rx + c, y, rz), (-rx, y, rz - c * 1.6),
                (-rx, y, -rz + c * 1.6), (-rx + c, y, -rz), (rx - c, y, -rz), (rx, y, -rz + c * 1.6)]
    b.hull(ring(0.0, 17.2, 23.6, 7.0) + ring(2.6, 18.6, 25.0, 7.4) + ring(5.0, 18.0, 24.4, 7.2) +
           ring(6.6, 16.6, 23.0, 6.8), 'tread', bevel=0.3)
    # ------------------------------------------------------------------ side hulls (lens plan, +X; mirrored)
    lens = [(6.8, -23.2), (11.5, -21.4), (15.8, -11.8), (17.2, 0.0), (15.8, 11.9), (11.5, 21.4), (6.8, 23.2)]
    b.plan(6.0, 13.0, lens, 'paint', bevel=0.2, mirror=True, top_inset=1.2)
    # dark blue strake along the hull side
    b.plan(6.2, 8.0, [(6.8, -23.6), (11.7, -21.8), (16.2, -12.0), (17.6, 0.0), (16.2, 12.1), (11.7, 21.8), (6.8, 23.6)],
           'paint2', bevel=0.1, mirror=True)
    # big lift fan in each side hull
    fan(b, 11.6, -7.4, 12.2, 13.5, 4.1)
    # team plate on each side-hull bow (the unit's team read: two forward-pointing plates)
    b.hull([(x, y, z) for x, y, z in [(8.0, 13.05, 2.4), (14.6, 13.05, 2.4), (13.6, 13.05, 12.0), (9.4, 13.05, 17.4),
                                       (8.0, 13.05, 17.4)]] +
           [(x, 13.22, z) for x, z in [(8.0, 2.4), (14.6, 2.4), (13.6, 12.0), (9.4, 17.4), (8.0, 17.4)]],
           'team', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ central bay housing (walls, +X mirrored)
    b.box((4.6, 6.4, -16.6), (6.9, 17.5, 13.1), 'paint', bevel=0.14, mirror=True)
    b.box((4.7, 17.3, -16.4), (6.6, 17.6, 12.9), 'dark', bevel=0.05, mirror=True)       # door sill
    # bow (crosses x = 0): glazed wedge in front of the bay
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, 6.2, 13.0), (6.8, 6.2, 23.0), (2.0, 6.4, 24.4), (6.8, 13.0, 13.0), (6.4, 17.4, 13.1),
             (4.0, 11.0, 22.0), (1.0, 11.0, 22.6), (2.6, 15.6, 14.4)]], 'paint', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 13.0, 18.3), (2.2, 15.1, 15.3), (4.6, 13.12, 18.42), (2.2, 15.22, 15.42)]], 'glass', bevel=0.03)
    b.box((2.6, 7.8, 22.6), (4.6, 9.2, 23.4), 'dark', bevel=0.05, mirror=True)
    b.box((2.8, 8.0, 23.36), (4.4, 9.0, 23.46), 'lightw', bevel=0.0, mirror=True)
    # stern (crosses x = 0): dark engine block behind the bay, exhaust grille, two vents
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, 6.2, -16.6), (6.8, 6.2, -23.2), (6.8, 15.0, -16.6), (6.4, 14.4, -22.4)]], 'paint2', bevel=0.16)
    b.box((-4.8, 8.4, -23.4), (4.8, 13.0, -22.9), 'black', bevel=0.0)
    for y in (9.0, 10.4, 11.8):
        b.box((-4.6, y, -23.55), (4.6, y + 0.5, -23.1), 'dark', bevel=0.03)
    b.cyl((3.2, 14.6, -19.6), (3.2, 16.6, -19.6), 0.8, 10, 'dark', bevel=0.04, mirror=True)
    b.cyl((3.2, 16.6, -19.6), (3.2, 16.7, -19.6), 0.55, 10, 'black', mirror=True)
    b.box((13.6, 9.0, -22.0), (15.0, 10.0, -21.4), 'lightr', bevel=0.0, mirror=True)
    # bay floor walls inside (seen when the doors are open)
    b.box((-4.6, 6.4, -16.6), (4.6, 6.9, 13.1), 'dark', bevel=0.0)
    # beacon on the stern block, left
    b.cyl((-4.2, 15.0, -21.0), (-4.2, 15.8, -21.0), 0.6, 10, 'dark')
    b.cyl((-4.2, 15.8, -21.0), (-4.2, 16.5, -21.0), 0.45, 10, 'lightw')

    # ------------------------------------------------------------------ doors (gable halves, hinge on outer edge)
    for name, sx in (('door2', 1),):
        d = k.piece(name); D = d.at
        ox = 4.6 * sx
        pts = []
        for z in (-14.9 - (d.org.z), 13.1 - d.org.z):
            for (x, y) in ((0.0, 0.0), (-4.55 * sx, 1.95), (-4.55 * sx, 1.35), (0.0, -0.6)):
                pts.append(D(x, y, z))
        d.hull(pts, 'paint2', bevel=0.12)
        # hazard strip along the ridge edge (yellow stripes from above when closed, meaningful: builder)
        pts = []
        for z in (-14.5 - d.org.z, 12.7 - d.org.z):
            for (x, y) in ((-3.0 * sx, 1.36), (-4.5 * sx, 2.0)):
                for dy in (0.06, 0.18):
                    pts.append(D(x, y + dy, z))
        d.hull(pts, 'hazard', bevel=0.02)
    k.clone('door1', 'door2', mirror_x=True)

    # ------------------------------------------------------------------ plate (bay floor; rises 10)
    p = k.piece('plate')
    p.box((-4.4, 6.9, -14.7), (4.4, 7.5, 12.9), 'paint2', bevel=0.1)
    p.box((-4.0, 7.48, -14.3), (-3.2, 7.6, 12.5), 'hazard', bevel=0.02)
    p.box((3.2, 7.48, -14.3), (4.0, 7.6, 12.5), 'hazard', bevel=0.02)

    # ------------------------------------------------------------------ turret / post / nanogun
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.0, 0), A(0, 1.4, 0), 2.9, 14, 'dark', bevel=0.08)
    t.box(A(-1.8, 1.3, -1.6), A(1.8, 3.0, 1.8), 'paint', bevel=0.12)
    po = k.piece('post'); O = po.at
    po.cyl(O(-1.6, 0, 0), O(1.6, 0, 0), 1.4, 12, 'dark', bevel=0.06)
    po.box(O(-1.1, -1.0, -12.4), O(1.1, 1.2, 0.4), 'steel', bevel=0.1)
    po.box(O(-0.6, 1.15, -11.0), O(0.6, 1.5, -1.0), 'hazard', bevel=0.03)
    ng = k.piece('nanogun'); N = ng.at
    ng.cyl(N(-1.7, 0, 0), N(1.7, 0, 0), 1.2, 12, 'dark', bevel=0.05)
    ng.hull([N(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(2.6, 0.6, -4.6), (2.6, 0.6, 4.4), (2.6, 5.6, -3.8), (2.2, 5.6, 4.4)]], 'paint', bevel=0.16)
    ng.box(N(-1.9, 5.55, -2.8), N(1.9, 5.75, 3.4), 'team', bevel=0.04)
    ng.cyl(N(0, 4.65, 4.2), N(0, 4.65, 11.4), 1.25, 12, 'steel', bevel=0.04)
    ng.cyl(N(0, 4.65, 11.4), N(0, 4.65, 13.6), 1.8, 12, 'dark', r2=1.2, bevel=0.06)
    ng.cyl(N(0, 4.65, 13.6), N(0, 4.65, 14.0), 0.9, 12, 'lightc')
