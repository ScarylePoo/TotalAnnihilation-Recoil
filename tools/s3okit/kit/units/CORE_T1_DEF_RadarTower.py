"""Radar Tower (CORE_T1_DEF_RadarTower) - Core radar. A tall narrow stepped mast with a side ladder spine and a huge
hexagonal dish on a short yoke at the top (the whole dish spins on y).
The TA dish stood almost vertical, which reads as a thin bar from the game camera; here it is tilted back 40 degrees
so its big light steel face (team rim, dark feed horn with a red tip) shows from above.
Identity from above: one big light hexagon with a team rim - the Arm radar is a dark 'T' of two paddles instead.
Pieces (COB): base, dish (spin y).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=43, drop=['dish']),
    preview_pose={'dish': (0, -30, 0)},
)

TILT = math.radians(40)       # dish face normal elevation above horizontal


def build(k):
    from mathutils import Vector      # bpy-only module: compose/preview load specs without it
    # ------------------------------------------------------------------ base: stepped mast
    b = k.piece('base')
    b.plan(0.0, 2.2, [(-14, -10), (-10, -14), (10, -14), (14, -10), (14, 10), (10, 14), (-10, 14), (-14, 10)],
           'paint2', bevel=0.2, top_inset=0.5)
    b.box((-11.0, 2.0, -11.0), (11.0, 9.6, 11.0), 'paint', bevel=0.3)
    for sx in (-1, 1):
        for sz in (-1, 1):   # team corner caps on the foot block
            b.box((min(6.0 * sx, 10.6 * sx), 9.5, min(6.0 * sz, 10.6 * sz)),
                  (max(6.0 * sx, 10.6 * sx), 9.75, max(6.0 * sz, 10.6 * sz)), 'team', bevel=0.03)
    b.plan(9.4, 30.0, [(-7.6, -7.6), (7.6, -7.6), (7.6, 7.6), (-7.6, 7.6)], 'paint2', bevel=0.25, top_inset=2.6)
    b.box((-5.2, 29.6, -5.2), (5.2, 56.6, 5.2), 'paint', bevel=0.25)
    for y in (36.0, 46.0):
        b.box((-5.6, y, -5.6), (5.6, y + 1.2, 5.6), 'dark', bevel=0.06)
    b.box((-2.0, 12.0, -7.4), (2.0, 54.0, -5.0), 'dark', bevel=0.1)          # ladder spine at the back
    b.cyl((0, 56.4, -2.29), (0, 58.6, -2.29), 4.8, 12, 'dark', bevel=0.1)
    b.box((-1.0, 50.0, 5.15), (1.0, 51.2, 5.45), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- dish (origin 0, 58.43, -2.29)
    d = k.piece('dish'); D = d.at
    d.cyl(D(0, 0, 0), D(0, 6.0, 0), 3.4, 10, 'dark', bevel=0.08)
    # yoke arms up to the dish pivot
    pv = (0.0, 20.0, 2.0)
    d.hull([D(x, y, z) for x in (-2.0, 2.0) for (y, z) in ((5.0, -2.4), (5.0, 2.4), (pv[1], pv[2] - 2.4), (pv[1], pv[2] + 1.0))],
           'paint2', bevel=0.15)
    n = Vector((0, math.sin(TILT), math.cos(TILT)))
    u = Vector((1, 0, 0))
    v = n.cross(u).normalized() * -1          # up along the dish face
    c = Vector(D(*pv)) + n * 1.6
    hexa = [(math.cos(math.pi / 6 + i * math.pi / 3), math.sin(math.pi / 6 + i * math.pi / 3)) for i in range(6)]

    def ring(r, dn, sx=1.0):
        return [tuple(c + u * (r * a * sx) + v * (r * bb) + n * dn) for a, bb in hexa]
    # back shell (dark), front face (steel), team rim, dark centre
    d.hull(ring(21.0, -0.6) + ring(12.0, -3.8), 'paint2', bevel=0.25)
    d.hull(ring(21.0, -0.6) + ring(21.0, 0.6), 'team', bevel=0.12)
    d.hull(ring(18.6, 0.55) + ring(18.6, 0.85), 'steel', bevel=0.0)
    d.hull(ring(5.4, 0.8) + ring(5.4, 1.1), 'dark', bevel=0.05)
    # feed horn on struts
    tip = c + n * 11.0
    d.cyl(tuple(c + n * 1.0), tuple(tip), 0.9, 8, 'dark')
    d.cyl(tuple(tip), tuple(tip + n * 2.2), 1.8, 8, 'dark', bevel=0.05)
    d.cyl(tuple(tip + n * 2.2), tuple(tip + n * 2.5), 1.0, 8, 'lightr')
    for a in (90, 210, 330):
        r = math.radians(a)
        p0 = c + (u * math.cos(r) + v * math.sin(r)) * 15.0 + n * 0.8
        d.cyl(tuple(p0), tuple(tip + n * 0.4), 0.35, 6, 'dark')
