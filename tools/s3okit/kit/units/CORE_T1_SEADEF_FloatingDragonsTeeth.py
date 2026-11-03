"""Floating Dragon's Teeth (CORE_T1_SEADEF_FloatingDragonsTeeth) - Core naval wall piece. Waterline 16 (the water
surface is model y = 16; the TA model lay entirely under it, so this one is built up to break the surface). Kept bold and
cheap like the land teeth: a dark square float set diagonally (a diamond, 3 elmo freeboard) with ochre hazard tips and
the land teeth's 'hedgehog' of fat light steel blades - two crossed diagonal pairs and a team-capped post - rising out of
it; a plain ballast block hangs underneath.
Identity from above: a steel X-and-cross starburst on a dark diamond with ochre tips - low team colour on purpose (wall
piece). The land Core teeth sit on a square plate; the Arm sea teeth are a light star on an octagonal float.
Pieces: ground (empty root), base. The feature reuses this same model, so there is no separate wreck.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 16.0
UNIT = dict(res=1024, ground=False, water=WL)


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
    dia = [(15.0, 0.0), (0.0, 15.0), (-15.0, 0.0), (0.0, -15.0)]
    b.hull([(x * 0.8, 6.0, z * 0.8) for x, z in dia] + [(x, 12.0, z) for x, z in dia]
           + [(x * 0.92, 19.0, z * 0.92) for x, z in dia], 'paint', bevel=0.35)
    b.hull([(x * s, y, z * s) for x, z in dia for s in (0.99, 1.03) for y in (14.8, 16.6)], 'dark', bevel=0.0)
    for sx, sz in ((1, 0), (-1, 0), (0, 1), (0, -1)):         # ochre tips (top-facing)
        b.hull([(sx * u + sz * w, y, sz * u + sx * w) for u, w in ((13.6, 0.0), (9.4, 3.6), (9.4, -3.6))
                for y in (18.9, 19.15)], 'hazard', bevel=0.0)
    # hedgehog: crossed blades rising out of the deck
    for ang in (45, 135):
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a)
        blade(b, (-cx * 4.0, 18.0, -cz * 4.0), (cx * 12.5, 30.0, cz * 12.5), 3.0, 1.5, 'steel')
        blade(b, (cx * 4.0, 18.0, cz * 4.0), (-cx * 12.5, 30.0, -cz * 12.5), 3.0, 1.5, 'steel')
    for s in (-1, 1):
        blade(b, (0, 18.6, -s * 2.0), (0, 24.0, s * 15.0), 2.8, 1.5, 'steel')
        blade(b, (-s * 2.0, 18.6, 0), (s * 15.0, 24.0, 0), 2.8, 1.5, 'steel')
    b.cyl((0, 18.5, 0), (0, 31.0, 0), 3.2, 6, 'dark', r2=2.0, bevel=0.1)
    b.cyl((0, 30.95, 0), (0, 33.0, 0), 2.1, 6, 'team', r2=1.1)
    b.box((-5.0, -1.0, -5.0), (5.0, 6.2, 5.0), 'dark', bevel=0.2)                 # ballast block
