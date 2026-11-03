"""Torpedo Launcher (ARM_T1_SEADEF_TorpedoLauncher) - Arm T1 torpedo launcher. Waterline 23 (the water surface is
model y = 23): the launcher itself lies submerged, as in TA. A light octagonal ring frame on four splayed anchor legs,
three spokes to a central yaw bearing from which the torpedo tube hangs (gun: turns y and x); a slim mast rises from the
bearing to a light marker float that breaks the surface (team top, cyan beacon), so the launcher is findable from above.
Identity from above: a small team disc on the water over a light ring with a long light tube across it (the Core
torpedo launcher is a dark X with corner pods; the Arm advanced launcher hangs a twin tube under a wide yoke).
Pieces (Lua script): base, gun (turn y, turn x; origin -0.25, 5, 0), flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 23.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=41, pose={'gun': (8, 40, 0)}),
    preview_pose={'gun': (0, -30, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    # ring frame: eight light segments with team tops on the four diagonal ones
    O, I = octagon(17.0), octagon(12.6)
    for i in range(8):
        j = (i + 1) % 8
        pts = [(x, y, z) for (x, z) in (O[i], O[j], I[i], I[j]) for y in (12.0, 16.0)]
        b.hull(pts, 'paint', bevel=0.25)
        if i % 2 == 0:
            mid = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
            a0, a1, c0, c1 = mid(O[i], O[j], 0.15), mid(O[i], O[j], 0.85), mid(I[i], I[j], 0.15), mid(I[i], I[j], 0.85)
            q = [(x * 0.97, z * 0.97) for x, z in (a0, a1)] + [(x * 1.02, z * 1.02) for x, z in (c0, c1)]
            b.hull([(x, y, z) for (x, z) in q for y in (15.95, 16.2)], 'team', bevel=0.0)
    # four anchor legs from the ring corners (+-x, +-z axis segments) down to the sea bed
    for a in (0, 90, 180, 270):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        R = lambda r, w: (c * r - s * w, s * r + c * w)
        top = [R(r, w) for r in (13.5, 16.4) for w in (-2.0, 2.0)]
        bot = [R(r, w) for r in (17.0, 21.0) for w in (-2.6, 2.6)]
        b.hull([(x, 12.2, z) for x, z in top] + [(x, 2.0, z) for x, z in bot], 'paint2', bevel=0.2)
        b.hull([(x, y, z) for x, z in [R(r, w) for r in (16.0, 22.0) for w in (-3.6, 3.6)] for y in (0.0, 2.2)],
               'dark', bevel=0.15)
    # three spokes to the yaw bearing (hub) over the tube
    for a in (90, 210, 330):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        b.hull([(c * r - s * w, y, s * r + c * w) for r in (5.0, 13.4) for w in (-1.4, 1.4) for y in (12.8, 15.2)],
               'paint2', bevel=0.15)
    b.cyl((-0.25, 7.6, 0), (-0.25, 15.6, 0), 5.6, 12, 'dark', r2=4.6, bevel=0.15)
    # marker mast and float
    b.cyl((-0.25, 15.4, 0), (-0.25, 21.0, 0), 1.6, 8, 'steel')
    b.cyl((-0.25, 20.6, 0), (-0.25, 25.2, 0), 5.6, 12, 'paint', r2=4.8, bevel=0.3)
    b.cyl((-0.25, 25.1, 0), (-0.25, 25.45, 0), 4.2, 12, 'team')
    b.cyl((-0.25, 22.4, 0), (-0.25, 23.4, 0), 5.85, 12, 'dark')
    b.cyl((-0.25, 25.4, 0), (-0.25, 27.0, 0), 0.9, 8, 'lightc')

    # ---------------------------------------------------------------- gun: torpedo tube (origin -0.25, 5, 0)
    g = k.piece('gun'); G = g.at
    g.cyl(G(0, 0.6, 0), G(0, 2.7, 0), 3.2, 10, 'dark', bevel=0.08)                  # swivel
    g.hull([G(x, y, z) for x in (-4.6, 4.6) for y in (-4.4, 0.8) for z in (-12.0, 9.0)]
           + [G(x, y, 12.5) for x in (-3.6, 3.6) for y in (-3.8, 0.0)], 'paint', bevel=0.3)
    g.hull([G(x, y, z) for x in (-2.6, 2.6) for y in (0.75, 1.05) for z in (-10.0, 7.0)], 'team', bevel=0.0)
    g.cyl(G(0, -2.25, 9.0), G(0, -2.25, 16.4), 2.7, 12, 'steel', bevel=0.05)
    g.cyl(G(0, -2.25, 16.2), G(0, -2.25, 16.55), 2.0, 12, 'black')
    g.cyl(G(0, -2.25, -15.0), G(0, -2.25, -11.8), 3.0, 12, 'dark', r2=3.6, bevel=0.06)
    for z in (-6.0, 2.0):
        g.box(G(-4.75, -3.2, z), G(4.75, 0.2, z + 1.4), 'dark', bevel=0.04)
