"""Gaat Gun (CORE_T1_DEF_GaatGun) - Core anti-air gatling tower. A tall slim pylon on a squat octagonal foot, a short
swivel stand and a big pentagonal armoured gun house (TA's 'house' shape) with a spinning three-barrel gatling
cluster out front (spindle spins on z).
Identity from above: a broad dark pentagon-roofed box with an ochre-striped ridge and team roof flanks, the long light
steel gatling barrels pointing out of it, on a dark pole - the only Core tower that is a big box on a stick.
Pieces (COB): base, stand (turn y), turret (turn x), spindle (spin z), gun1..3 (static on the spindle), flare (emit).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=19, drop=['spindle'], pose={'stand': (0, 40, 0), 'turret': (20, 0, 0)}),
    preview_pose={'stand': (0, -25, 0), 'turret': (-15, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: foot + pylon
    b = k.piece('base')
    oct8 = lambda r: [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    b.plan(0.0, 2.4, oct8(17.0), 'paint2', bevel=0.2, top_inset=0.6)
    b.plan(2.3, 9.0, oct8(12.0), 'paint', bevel=0.22, top_inset=3.0)
    # team plates on four faces of the foot (top-facing)
    for i in (0, 2, 4, 6):
        a = math.pi / 8 + i * math.pi / 4 + math.pi / 8
        cx, cz = math.cos(a), math.sin(a); px, pz = -cz, cx
        b.hull([(cx * r + px * t, 2.4 + d, cz * r + pz * t) for r in (12.6, 15.6) for t in (-3.0, 3.0) for d in (0.0, 0.16)],
               'team', bevel=0.0)
    # pylon: square tapering column with dark corner ribs
    b.cyl((0, 8.0, 0), (0, 40.6, 0), 7.2, 4, 'paint2', r2=5.6, rot=math.pi / 4, bevel=0.2)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.hull([(x * sx, y, z * sz) for x, y, z in
                    [(3.4, 8.0, 3.4), (5.4, 8.0, 3.4), (3.4, 8.0, 5.4), (5.4, 8.0, 5.4),
                     (2.6, 40.6, 2.6), (4.2, 40.6, 2.6), (2.6, 40.6, 4.2), (4.2, 40.6, 4.2)]], 'dark', bevel=0.1)
    for y in (20.0, 31.0):
        b.box((-5.6, y, 4.95), (5.6, y + 1.0, 5.25), 'dark', bevel=0.0)
    b.box((-1.0, 36.0, 4.4), (1.0, 37.2, 4.75), 'lightr', bevel=0.0)
    b.cyl((0, 39.8, 0), (0, 41.0, 0), 6.4, 8, 'dark', rot=math.pi / 8, bevel=0.1)

    # ---------------------------------------------------------------- stand: swivel (origin 0, 40.78, 0.27)
    s = k.piece('stand'); S = s.at
    s.cyl(S(0, 0, 0), S(0, 6.0, 0), 4.6, 10, 'dark', bevel=0.1)
    s.cyl(S(0, 2.0, 0), S(0, 3.6, 0), 5.4, 10, 'paint2', bevel=0.08)
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 6.0, -4.0), (4.4, 6.0, 4.0), (6.4, 10.4, -3.0), (6.4, 10.4, 3.0)]], 'paint2', bevel=0.15)

    # ---------------------------------------------------------------- turret: pentagonal gun house (origin 0, 51.25, 0.39)
    t = k.piece('turret'); A = t.at
    house = [(15.0, -3.0), (15.6, 8.0), (0.0, 18.0)]          # (x, y) half pentagon; ridge at x=0
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for (x, y) in house for z in (-11.6, 4.4)] +
           [A(x * sx, y, 5.8) for sx in (-1, 1) for (x, y) in ((13.4, -2.0), (13.8, 7.6))] + [A(0, 16.4, 5.8)],
           'paint', bevel=0.3)
    # team roof flanks (top-facing slopes of the 'house')
    for sx in (-1, 1):
        pts = []
        for (x, y) in ((12.2, 10.0), (3.2, 15.9)):
            for z in (-9.6, 2.6):
                for d in (0.1, 0.3):
                    pts.append(A(sx * (x + d * 0.55), y + d * 0.84, z))
        t.hull(pts, 'team', bevel=0.0)
    # ochre ridge stripe
    t.hull([A(x, y, z) for x in (-1.6, 1.6) for z in (-10.8, 3.6) for y in (17.9, 18.15)] , 'hazard', bevel=0.0)
    # dark side ammo drums and rear vent
    t.cyl(A(15.4, 2.0, -6.0), A(17.6, 2.0, -6.0), 4.2, 10, 'paint2', bevel=0.1, mirror=True)
    t.cyl(A(17.5, 2.0, -6.0), A(17.8, 2.0, -6.0), 2.2, 10, 'dark', mirror=True)
    t.box(A(-9.0, 0.0, -12.4), A(9.0, 8.0, -11.4), 'black', bevel=0.0)
    for y in (1.6, 3.6, 5.6):
        t.box(A(-9.4, y, -12.6), A(9.4, y + 0.6, -11.6), 'dark', bevel=0.0)
    # front mantlet round the spindle
    t.cyl(A(0, 6.13, 4.0), A(0, 6.13, 6.4), 10.4, 12, 'dark', bevel=0.15)
    t.box(A(-11.0, 13.0, 4.6), A(-8.6, 14.2, 6.0), 'lightw', bevel=0.0)
    t.box(A(8.6, 13.0, 4.6), A(11.0, 14.2, 6.0), 'lightw', bevel=0.0)

    # ---------------------------------------------------------------- spindle: gatling drum (origin 0, 57.37, 6.52)
    sp = k.piece('spindle'); P = sp.at
    sp.cyl(P(0, 0, 0), P(0, 0, 13.4), 7.8, 9, 'steel', bevel=0.15)
    sp.cyl(P(0, 0, 13.4), P(0, 0, 14.4), 8.6, 9, 'dark', bevel=0.08)
    sp.cyl(P(0, 0, 4.0), P(0, 0, 6.0), 8.2, 9, 'hazard', bevel=0.0)
    sp.cyl(P(0, 0, 14.4), P(0, 0, 15.4), 2.6, 9, 'dark')

    # ---------------------------------------------------------------- guns: barrels (gun1 at top; gun2/3 lower left/right)
    g = k.piece('gun1'); G = g.at
    if True:
        g.cyl(G(0, 0, -0.6), G(0, 0, 18.4), 1.7, 8, 'steel', rot=math.pi / 8)
        g.cyl(G(0, 0, 8.0), G(0, 0, 9.4), 2.2, 8, 'dark', rot=math.pi / 8)
        g.cyl(G(0, 0, 17.0), G(0, 0, 19.2), 2.1, 8, 'dark', rot=math.pi / 8, bevel=0.05)
        g.cyl(G(0, 0, 19.18), G(0, 0, 19.28), 1.1, 8, 'black')
    k.clone('gun2', 'gun1')
    k.clone('gun3', 'gun1')
