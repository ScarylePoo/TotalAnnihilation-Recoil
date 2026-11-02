"""Buzzsaw (CORE_T2_DEF_Buzzsaw) - Core rapid-fire plasma cannon. A massive clawed pedestal, a tall two-cheeked tower and
between the cheeks a big vertical wheel (spindle) with six heavy barrels radiating from it like saw teeth; the wheel
turns to bring the next barrel to bear (spindle turn x), each barrel recoils along its own axis.
Identity from above: a long light steel line (the wheel's front and rear barrels and hub) splitting two dark tower
cheeks with team tops, over a dark claw-footed square - nothing else is a six-barrel wheel.
Pieces (COB): GP, Base, Turret (turn y), rotate (empty), spindle (turn x), sleeve1..6, barrel1..6 (move y/z),
Flare1..6 (emit, empty). Barrels point radially at 60 deg steps in the spindle's yz plane (barrel1 forward, +z).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    wreck=dict(seed=47, drop=['barrel2', 'barrel5'], pose={'Turret': (0, 35, 0), 'spindle': (20, 0, 0)}),
    preview_pose={'Turret': (0, -25, 0)},
)

ANG = {1: 0, 2: 60, 3: 120, 4: 180, 5: 240, 6: 300}     # barrel direction from +z toward +y, degrees


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ Base: clawed pedestal
    b = k.piece('Base')
    b.plan(0.0, 3.0, octagon(25.6), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.8, 21.7, octagon(19.6), 'paint', bevel=0.35, top_inset=3.6)
    b.cyl((0, 21.2, 0), (0, 22.0, 0), 15.4, 16, 'dark', bevel=0.08)
    for sx in (-1, 1):
        for sz in (-1, 1):   # four claws on the diagonals
            c = lambda u, w: ((u - w) * 0.7071 * sx, (u + w) * 0.7071 * sz)
            pts = []
            for u, y, hw in ((12.0, 0.0, 5.4), (28.0, 0.0, 3.6), (27.0, 4.6, 2.6), (14.0, 16.0, 4.4)):
                for w in (-hw, hw):
                    x, z = c(u, w); pts.append((x, y, z))
            b.hull(pts, 'paint2', bevel=0.3)
            tp = []
            for u in (16.4, 24.2):
                y = 16.0 - (u - 14.0) * 11.4 / 13.0
                for w in (-2.4, 2.4):
                    for d in (0.1, 0.28):
                        x, z = c(u, w); tp.append((x, y + d, z))
            b.hull(tp, 'team', bevel=0.0)
    b.box((-1.0, 9.0, 17.6), (1.0, 10.4, 18.2), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ Turret: twin-cheek tower (origin 0, 21.76, 0)
    t = k.piece('Turret'); T = t.at
    t.cyl(T(0, 0, 0), T(0, 2.0, 0), 15.0, 16, 'dark', bevel=0.1)
    for sx in (-1, 1):
        t.hull([T(sx * x, y, z) for x, y, z in
                [(5.6, 1.6, -14.0), (17.4, 1.6, -14.0), (5.6, 1.6, 14.0), (17.4, 1.6, 14.0),
                 (5.6, 58.0, -12.4), (15.4, 54.0, -11.4), (5.6, 58.0, 12.4), (15.4, 54.0, 11.4),
                 (5.6, 64.6, -6.4), (13.0, 62.0, -6.0), (5.6, 64.6, 6.4), (13.0, 62.0, 6.0)]], 'paint', bevel=0.4)
        # team on the cheek's top: the flat crown and the sloped shoulder, lifted off the surface
        top = [(6.4, 64.6, -5.6), (12.2, 62.2, -5.2), (6.4, 64.6, 5.6), (12.2, 62.2, 5.2)]
        sho = [(6.4, 58.2, -11.0), (14.4, 54.6, -10.2), (6.4, 58.2, 11.0), (14.4, 54.6, 10.2)]
        for d0, d1 in ((0.12, 0.3),):
            t.hull([T(sx * (x + 0.1), y + d, z) for x, y, z in top for d in (d0, d1)], 'team', bevel=0.0)
            t.hull([T(sx * (x + d * 0.6), y + d * 0.8, z) for x, y, z in top[1::2] + sho[1::2] + [top[0], top[2], sho[0], sho[2]]
                    for d in (d0, d1)], 'team', bevel=0.0)
        # dark armour bands down the cheek
        for y in (14.0, 30.0):
            t.hull([T(sx * x, yy, z) for x in (16.6, 17.8) for yy in (y, y + 3.0) for z in (-13.8, 13.8)], 'dark', bevel=0.08)
        t.cyl(T(sx * 5.4, 49.7, 0), T(sx * 7.4, 49.7, 0), 7.0, 12, 'dark', bevel=0.08)     # axle bosses
    t.box(T(-5.6, 1.8, -12.0), T(5.6, 6.0, 12.0), 'dark', bevel=0.1)

    # ------------------------------------------------------------------ spindle: the wheel hub (origin 0, 71.48, 0)
    sp = k.piece('spindle'); P = sp.at
    sp.cyl(P(-4.6, 0, 0), P(4.6, 0, 0), 14.6, 12, 'steel', rot=0.0, bevel=0.15)
    sp.cyl(P(-5.2, 0, 0), P(5.2, 0, 0), 6.0, 12, 'dark', bevel=0.08)
    sp.cyl(P(-5.3, 0, 0), P(5.3, 0, 0), 2.4, 8, 'lightr')

    # ------------------------------------------------------------------ sleeves and barrels, radial
    for i in range(1, 7):
        a = math.radians(ANG[i]); uy, uz = math.sin(a), math.cos(a)
        s = k.piece(f'sleeve{i}'); S = s.at          # sleeves share the spindle origin
        s.cyl(S(0, uy * 13.0, uz * 13.0), S(0, uy * 31.6, uz * 31.6), 4.4, 8, 'paint2', rot=math.pi / 8, bevel=0.12)
        s.cyl(S(0, uy * 25.0, uz * 25.0), S(0, uy * 31.8, uz * 31.8), 4.9, 8, 'team', rot=math.pi / 8, bevel=0.08)   # team sleeve collars
        br = k.piece(f'barrel{i}'); B = br.at
        L = 18.4
        br.cyl(B(0, -uy * 0.6, -uz * 0.6), B(0, uy * (L - 3.4), uz * (L - 3.4)), 3.0, 10, 'steel', rot=math.pi / 10)
        br.cyl(B(0, uy * (L - 3.6), uz * (L - 3.6)), B(0, uy * L, uz * L), 3.6, 8, 'steel', r2=3.3, rot=math.pi / 8, bevel=0.06)
        br.cyl(B(0, uy * 6.0, uz * 6.0), B(0, uy * 7.2, uz * 7.2), 3.4, 10, 'dark', rot=math.pi / 10)
        br.cyl(B(0, uy * (L - 0.02), uz * (L - 0.02)), B(0, uy * (L + 0.1), uz * (L + 0.1)), 1.6, 10, 'black')
