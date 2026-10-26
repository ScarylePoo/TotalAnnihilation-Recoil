"""Dragon's Teeth (CORE_T1_DEF_DragonsTeeth) - Core wall piece. Kept bold and cheap: a square stepped plinth with a
tangle of fat crossed blades (a 'hedgehog' anti-tank obstacle) - two crossed diagonal pairs, four low spikes along
the axes and a team-capped post, the TA spiky-cross silhouette.
Identity from above: an X-and-cross starburst of light steel blades over a dark square plate with ochre hazard
corners and a team cap - the Arm teeth are a four-point star on an octagon instead.
One piece (base); the feature `_dead` reuses this same model, so there is no separate wreck.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def blade(b, p0, p1, w, t, mat):
    """flat-ish tapered blade from p0 (wide, w x t) to the point p1"""
    import mathutils
    a, c = mathutils.Vector(p0), mathutils.Vector(p1)
    d = (c - a).normalized()
    side = d.cross(mathutils.Vector((0, 1, 0)))
    if side.length < 1e-3:
        side = mathutils.Vector((1, 0, 0))
    side.normalize()
    up = side.cross(d).normalized()
    pts = [tuple(a + side * sx * w + up * sy * t) for sx in (-1, 1) for sy in (-1, 1)] + [tuple(c)]
    b.hull(pts, mat, bevel=0.15)


def build(k):
    b = k.piece('base')
    b.box((-11.6, 0.0, -11.6), (11.6, 2.0, 11.6), 'paint2', bevel=0.3)
    b.plan(1.8, 4.2, [(-8.6, -8.6), (8.6, -8.6), (8.6, 8.6), (-8.6, 8.6)], 'paint2', bevel=0.25, top_inset=1.6)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.hull([(x * sx, y, z * sz) for x, y, z in
                    [(8.6, 2.0, 11.4), (11.4, 2.0, 8.6), (11.4, 2.0, 11.4),
                     (8.6, 2.16, 11.4), (11.4, 2.16, 8.6), (11.4, 2.16, 11.4)]], 'hazard', bevel=0.0)
    # three crossed blade pairs: diagonals and the X axis, each a long blade from one low corner to the opposite top
    for ang in (45, 135):
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a)
        blade(b, (-cx * 5.0, 3.0, -cz * 5.0), (cx * 16.0, 16.4, cz * 16.0), 3.2, 1.6, 'steel')
        blade(b, (cx * 5.0, 3.0, cz * 5.0), (-cx * 16.0, 16.4, -cz * 16.0), 3.2, 1.6, 'steel')
    # front/back spikes along Z
    for s in (-1, 1):
        blade(b, (0, 3.5, -s * 2.0), (0, 9.0, s * 16.4), 3.0, 1.6, 'steel')
        blade(b, (-s * 2.0, 3.5, 0), (s * 16.4, 9.0, 0), 3.0, 1.6, 'steel')
    # crowned post
    b.cyl((0, 3.5, 0), (0, 18.0, 0), 3.4, 6, 'dark', r2=2.2, bevel=0.1)
    b.cyl((0, 17.95, 0), (0, 20.2, 0), 2.3, 6, 'team', r2=1.2)
