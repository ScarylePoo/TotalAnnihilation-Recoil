"""Immolator (CORE_T1_DEF_Immolator) - Core plasma tower. A flared three-footed trunk (TA tripod root) carrying a
wide flat hexagonal turret drum with two short tapered plasma guns side by side (each recoils on z).
Identity from above: a big flat dark hexagon with a team ring and a hot glowing core vent in the middle, twin light
steel guns out front, over three dark feet - a mushroom where the other Core towers are boxes on poles.
Pieces (COB): plasground (empty), plasbase, plasturret (turn y + x), plasgunL/R (move z), emitplasL/R (emit, empty).
plasgunR is plasgunL mirrored (clone); the COB-era origins are 0.01 off symmetric, the guns are the same shape.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=23, drop=['plasgunR'], pose={'plasturret': (10, 30, 0)}),
    preview_pose={'plasturret': (-8, -25, 0)},
)


def build(k):
    # ------------------------------------------------------------------ plasbase: tripod root + trunk
    b = k.piece('plasbase')
    b.cyl((0, 0, 0), (0, 2.4, 0), 14.0, 12, 'paint2', r2=13.0, bevel=0.2)
    for ang in (90, 210, 330):            # three feet: front, rear-left, rear-right
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a); px, pz = -cz, cx
        b.hull([(cx * u + px * w, y, cz * u + pz * w) for (u, y, w0) in
                ((4.0, 0.0, 6.4), (20.0, 0.0, 6.0), (20.0, 4.6, 5.0), (4.0, 20.0, 4.2)) for w in (-w0, w0)], 'paint', bevel=0.3)
        b.hull([(cx * u + px * w, y, cz * u + pz * w) for (u, y) in ((15.0, 5.1), (19.6, 4.75)) for w in (-4.2, 4.2) for _ in (0,)]
               + [(cx * u + px * w, y + 0.18, cz * u + pz * w) for (u, y) in ((15.0, 5.1), (19.6, 4.75)) for w in (-4.2, 4.2)],
               'hazard', bevel=0.0)
        b.box((cx * 20.2 - 0.6, 1.2, cz * 20.2 - 0.6), (cx * 20.2 + 0.6, 2.4, cz * 20.2 + 0.6), 'dark', bevel=0.0)
    # trunk, flaring to the top
    b.cyl((0, 2.0, 0), (0, 30.0, 0), 8.6, 6, 'paint', r2=5.6, bevel=0.25)
    b.cyl((0, 29.0, 0), (0, 37.0, 0), 5.8, 6, 'paint2', r2=8.4, bevel=0.2)
    b.cyl((0, 36.6, 0), (0, 37.6, 0), 9.4, 12, 'dark', bevel=0.1)
    for y in (12.0, 20.0):
        b.cyl((0, y, 0), (0, y + 1.2, 0), 8.2 - (y - 2) * 0.1, 6, 'dark', bevel=0.05)
    b.box((-0.9, 24.0, 6.1), (0.9, 25.2, 6.5), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- plasturret: flat hex drum (origin 0, 40.77, 0.07)
    t = k.piece('plasturret'); A = t.at
    hexa = lambda r: [(r * math.cos(i * math.pi / 3), r * math.sin(i * math.pi / 3)) for i in range(6)]
    t.hull([A(x, -3.4, z) for x, z in hexa(12.4)] + [A(x, 5.0, z) for x, z in hexa(13.4)] +
           [A(x, 8.0, z) for x, z in hexa(10.0)], 'paint', bevel=0.3)
    # team ring on the top slope (six trapezoids)
    for i in range(6):
        a0, a1 = i * math.pi / 3, (i + 1) * math.pi / 3
        pts = []
        for (r, y) in ((12.7, 5.65), (10.6, 7.75)):
            for a in (a0 + 0.06, a1 - 0.06):
                for d in (0.1, 0.28):
                    pts.append(A((r + d * 0.7) * math.cos(a), y + d * 0.7, (r + d * 0.7) * math.sin(a)))
        t.hull(pts, 'team', bevel=0.0)
    # central glowing vent with a dark collar
    t.cyl(A(0, 7.6, -1.0), A(0, 9.4, -1.0), 5.4, 12, 'dark', bevel=0.1)
    t.cyl(A(0, 9.3, -1.0), A(0, 9.55, -1.0), 3.6, 12, 'lightr')
    for z in (-3.4, -1.0, 1.4):
        t.box(A(-3.8, 9.5, z - 0.3), A(3.8, 9.75, z + 0.3), 'black', bevel=0.0)
    # dark lower skirt band and gun mantlets
    t.hull([A(x, -3.6, z) for x, z in hexa(12.8)] + [A(x, -1.6, z) for x, z in hexa(13.2)], 'paint2', bevel=0.15)
    for sx in (-1, 1):      # plasturret origin x is -0.004: no mirror=True on this piece
        t.box(A(3.8 * sx, -2.6, 9.6), A(9.6 * sx, 4.4, 16.6), 'paint2', bevel=0.2)
    t.box(A(-0.9, 1.0, 12.2), A(0.9, 2.6, 13.0), 'lightw', bevel=0.0)

    # ---------------------------------------------------------------- guns (plasgunL origin 6.70, 40.77, 18.41)
    g = k.piece('plasgunL'); G = g.at
    g.cyl(G(0, 0.6, -2.4), G(0, 0.6, 3.0), 2.9, 8, 'dark', rot=math.pi / 8, bevel=0.08)
    g.cyl(G(0, 0.6, 3.0), G(0, 0.6, 16.4), 2.0, 8, 'steel', r2=1.25, rot=math.pi / 8)
    g.cyl(G(0, 0.6, 7.0), G(0, 0.6, 8.2), 2.25, 8, 'dark', rot=math.pi / 8)
    g.cyl(G(0, 0.6, 16.2), G(0, 0.6, 18.8), 1.9, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl(G(0, 0.6, 18.78), G(0, 0.6, 18.9), 1.0, 8, 'lightr')
    k.clone('plasgunR', 'plasgunL', mirror_x=True)
