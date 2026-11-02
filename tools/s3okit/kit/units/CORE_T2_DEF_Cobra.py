"""Cobra (CORE_T2_DEF_Cobra) - Core flak gun. A tall stepped pillar with buttressed feet carrying a wide hooded gun
housing (the 'cobra hood') with two long flak cannons on its flanks.
Identity from above: a wide dark hood with a team crown along its ridge, two long light steel guns well
apart on its flanks, over a small dark footing with team corner pads - a tall pillar where the Arm Flakker is a squat
bunker with ear shields.
Pieces (COB): ground, base, turret (turn y), turret2 (turn x), gun1/gun2 (move z recoil), flare1/2 (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=39, drop=['gun2'], pose={'turret': (0, 40, 0), 'turret2': (12, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'turret2': (-20, 0, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: footing + stepped pillar
    b = k.piece('base')
    b.plan(0.0, 2.2, [(-14.0, -14.0), (14.0, -14.0), (14.0, 14.0), (-14.0, 14.0)], 'paint2', bevel=0.25, top_inset=0.8)
    for s in (-1, 1):
        for t in (-1, 1):
            b.box((min(s * 9.0, s * 13.2), 2.0, min(t * 9.0, t * 13.2)), (max(s * 9.0, s * 13.2), 3.0, max(t * 9.0, t * 13.2)),
                  'team', bevel=0.06)
    # four buttress feet on the diagonals
    for s in (-1, 1):
        for t in (-1, 1):
            b.hull([(s * x, y, t * z) for x, y, z in
                    ((4.0, 2.0, 9.6), (9.6, 2.0, 4.0), (10.6, 2.0, 10.6), (4.0, 9.0, 6.0), (6.0, 9.0, 4.0))], 'paint', bevel=0.2)
    b.plan(2.0, 13.0, octagon(8.2), 'paint', bevel=0.25, top_inset=0.8)
    b.plan(12.6, 14.2, octagon(8.0), 'dark', bevel=0.1)
    b.plan(14.0, 26.4, octagon(6.6), 'paint', bevel=0.25, top_inset=0.6)
    b.plan(26.0, 27.4, octagon(7.4), 'dark', bevel=0.1)
    b.box((-1.0, 19.0, 6.0), (1.0, 20.4, 6.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret: swivel (origin 0, 30.6, 0)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, -3.4, 0), T(0, -1.0, 0), 6.8, 12, 'dark', bevel=0.08)
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, -1.2, -4.4), (4.6, -1.2, 5.8), (4.0, 3.6, -3.6), (4.0, 3.0, 5.0)]], 'paint2', bevel=0.25)

    # ------------------------------------------------------------------ turret2: the hood (origin 0, 27.03, -4.27)
    h = k.piece('turret2'); H = h.at
    h.cyl(H(-10.6, 0, 0), H(10.6, 0, 0), 2.4, 10, 'steel', bevel=0.05)
    # wide hood: flat-topped, chamfered front, overhanging the trunnion
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, -0.6, -12.4), (10.4, -0.4, -10.0), (10.4, -0.4, 6.0), (5.6, -0.6, 10.4),
             (4.6, 6.8, -12.0), (8.6, 5.4, -9.0), (8.6, 5.4, 3.0), (4.6, 6.0, 8.4)]], 'paint', bevel=0.35)
    # team crown along the hood ridge
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.8, 6.7, -10.6), (3.8, 6.1, 6.0), (3.8, 6.95, -10.6), (3.8, 6.35, 6.0)]], 'team', bevel=0.0)
    # gun pods on the flanks (the guns ride in them)
    for sx in (-1, 1):
        h.hull([H(sx * x, y, z) for x, y, z in
                [(4.6, -0.6, -2.0), (9.4, -0.6, -2.0), (4.6, 3.6, -2.0), (9.4, 3.6, -2.0),
                 (4.6, -0.2, 6.4), (9.4, -0.2, 6.4), (4.6, 3.2, 6.4), (9.4, 3.2, 6.4)]], 'dark', bevel=0.2)
    h.box(H(-2.6, 0.6, 10.2), H(2.6, 3.6, 10.8), 'black', bevel=0.0)
    h.box(H(-0.8, 4.0, 9.4), H(0.8, 5.0, 9.9), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ guns (gun1 origin -6.9, 28.47, -1.96)
    g = k.piece('gun1'); G = g.at
    g.cyl(G(0, 0, -1.0), G(0, 0, 20.6), 1.35, 8, 'steel', rot=math.pi / 8)
    g.cyl(G(0, 0, 4.0), G(0, 0, 9.0), 1.75, 8, 'steel', rot=math.pi / 8, bevel=0.04)
    g.cyl(G(0, 0, 17.6), G(0, 0, 20.9), 1.8, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl(G(0, 0, 20.88), G(0, 0, 21.0), 0.8, 8, 'black')
    k.clone('gun2', 'gun1', mirror_x=True)
