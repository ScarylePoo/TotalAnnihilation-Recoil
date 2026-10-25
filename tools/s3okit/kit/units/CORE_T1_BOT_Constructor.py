"""Construction Kbot (CORE_T1_BOT_Constructor) - Core T1 builder. Lopsided like the TA original: a hunched armoured
hump on the right shoulder (torso, sloped forward, the main mass), a clamp bracket on the left (gunclamp) holding a
long nano cannon (nanogun) laid ACROSS the back of the unit, with its end cap (guncover) on the right. To build, the
cap slides off, the cannon swings up and round to point forward and the nozzle telescopes out; torso turns to the
build. Standard biped skeleton; script ported to scripts/CORE_T1_BOT_Constructor.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it the Core builder): dark warm hump with a team plate on one side, a long LIGHT steel cannon
bar across the rear with an ochre hazard end cap - an L / T outline unlike any Core combat kbot."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=4.6),
    res=1024,
    wreck=dict(seed=11, drop=['nanogun'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.6)

    # ------------------------------------------------------------------ pelvis (0, 12.5, 0): hip box
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.0, -2.0, -3.6), (4.0, -2.0, 3.8), (5.2, 2.8, -4.6), (5.2, 2.8, 5.0), (3.0, -3.0, -2.4), (3.0, -3.0, 2.6)]],
           'paint2', bevel=0.18)
    p.box(Q(-2.6, -1.2, 4.8), Q(2.6, 1.8, 5.6), 'dark', bevel=0.08)                           # crotch plate

    # ------------------------------------------------------------------ torso (0, 16.5, -0.5): hump on the right
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -1.6, 0.5), A(0, 0.6, 0.5), 3.4, 12, 'dark', bevel=0.08)                        # waist
    # main hump: rises toward +x and back, sloped glacis toward the front (TA's wedge)
    t.hull([A(x, y, z) for x, y, z in
            [(-4.6, 0.4, -2.6), (-4.6, 0.4, 6.0), (10.0, 0.4, -2.6), (10.0, 0.4, 7.4),
             (-3.8, 5.2, -1.8), (-3.8, 4.0, 5.6), (9.4, 12.8, -1.4), (9.4, 9.0, 4.6),
             (2.0, 12.4, -1.4), (2.0, 9.4, 3.4), (10.6, 4.0, 9.4), (-3.0, 2.4, 8.6)]], 'paint', bevel=0.24)
    # team plate on the hump's sloped top
    t.hull([A(x, y, z) for x, y, z in
            [(3.2, 12.22, -0.6), (8.4, 12.42, -0.6), (3.2, 9.6, 2.6), (8.4, 9.4, 3.6),
             (3.2, 12.38, -0.65), (8.4, 12.58, -0.65), (3.2, 9.76, 2.55), (8.4, 9.56, 3.55)]], 'team', bevel=0.03)
    # cannon saddle behind the hump (paint2): the nano cannon rests on it
    t.hull([A(x, y, z) for x, y, z in
            [(-4.0, 0.4, -6.2), (9.0, 0.4, -6.2), (-4.0, 0.4, -2.0), (9.0, 0.4, -2.0),
             (-3.4, 4.6, -5.6), (8.4, 4.6, -5.6), (-3.4, 5.4, -2.2), (8.4, 5.4, -2.2)]], 'paint2', bevel=0.16)
    # dark visor slot on the glacis, warm lights
    t.hull([A(x, y, z) for x, y, z in
            [(-1.8, 3.6, 7.9), (8.6, 4.2, 8.6), (-1.6, 5.0, 6.8), (8.4, 5.8, 7.6),
             (-1.8, 3.6, 8.15), (8.6, 4.2, 8.85), (-1.6, 5.0, 7.05), (8.4, 5.8, 7.85)]], 'dark', bevel=0.05)
    for x in (0.4, 4.0, 7.2):
        t.box(A(x, 4.3, 8.0), A(x + 1.1, 4.8, 8.5), 'lightc', bevel=0.0)
    # rear exhaust block (paint2) with ribs
    t.box(A(1.4, 0.6, -8.2), A(9.0, 4.4, -6.0), 'dark', bevel=0.14)
    for y in (1.4, 2.6):
        t.box(A(2.0, y, -8.45), A(8.4, y + 0.5, -8.1), 'black', bevel=0.0)

    # ------------------------------------------------------------------ gun clamp (-7.5, 16, -7.5): U bracket
    c = k.piece('gunclamp'); C = c.at
    c.cyl(C(0, -0.6, 0), C(0, 0.6, 0), 2.8, 10, 'dark', bevel=0.06)                           # swivel
    for sz in (-1, 1):
        c.hull([C(x, y, z * sz) for x, y, z in
                [(-2.6, 0.4, 2.2), (2.6, 0.4, 2.2), (-2.6, 0.4, 3.4), (2.6, 0.4, 3.4),
                 (-2.0, 9.6, 2.4), (2.0, 9.6, 2.4), (-2.0, 9.6, 3.4), (2.0, 9.6, 3.4)]], 'paint', bevel=0.14)
    c.box(C(-2.6, 0.4, -3.4), C(2.6, 2.2, 3.4), 'paint', bevel=0.14)
    c.hull([C(x, y, z) for x, y, z in                                                            # hazard bands on top
            [(-1.9, 9.58, 2.5), (1.9, 9.58, 2.5), (-1.9, 9.58, 3.3), (1.9, 9.58, 3.3),
             (-1.85, 9.74, 2.55), (1.85, 9.74, 2.55), (-1.85, 9.74, 3.25), (1.85, 9.74, 3.25)]], 'paint2', bevel=0.02)

    # ------------------------------------------------------------------ nano cannon (-7.5, 24.5, -7.5) along +x
    n = k.piece('nanogun'); N = n.at
    n.cyl(N(-2.2, 0, 0), N(14.2, 0, 0), 2.3, 10, 'steel', rot=math.pi / 10, bevel=0.08)         # LIGHT barrel (Core)
    n.cyl(N(-2.6, 0, 0), N(-1.8, 0, 0), 2.6, 10, 'dark', rot=math.pi / 10, bevel=0.06)
    for x in (1.0, 6.0, 11.0):
        n.cyl(N(x, 0, 0), N(x + 0.9, 0, 0), 2.55, 10, 'dark', rot=math.pi / 10, bevel=0.04)    # clamp rings
    n.box(N(2.4, 2.1, -1.0), N(9.6, 2.7, 1.0), 'team', bevel=0.04)                              # team strip on top
    z = k.piece('nozzle'); Z = z.at                                                              # (-2.5, 24.5, -7.5)
    z.cyl(Z(0.0, 0, 0), Z(8.6, 0, 0), 1.3, 10, 'dark', bevel=0.04)
    z.cyl(Z(8.4, 0, 0), Z(9.0, 0, 0), 1.6, 10, 'dark', bevel=0.04)
    z.cyl(Z(8.95, 0, 0), Z(9.15, 0, 0), 1.2, 10, 'lightc', r2=0.6)                              # nano emitter

    # ------------------------------------------------------------------ end cap (7, 24.5, -7.5): ochre hazard
    g = k.piece('guncover'); G = g.at
    g.cyl(G(0.0, 0, 0), G(2.0, 0, 0), 3.0, 10, 'hazard', r2=2.6, rot=math.pi / 10, bevel=0.12)
    g.cyl(G(1.95, 0, 0), G(2.25, 0, 0), 2.0, 10, 'dark', rot=math.pi / 10)
