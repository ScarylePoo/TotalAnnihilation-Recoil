"""Advanced Torpedo Launcher (CORE_T2_SEADEF_AdvancedTorpedoLauncher) - Core T2 torpedo launcher. Waterline 15 (the
water surface is model y = 15): it lies submerged, as in TA. A dark octagonal sea-bed pad with a bearing ring; on it a
long swivelling platform (launcher) carrying, on its LEFT, a coilgun: a dark guide rail with three light steel
accelerator coils (coil1..3, each kicks back on firing) and a steel barrel; on its RIGHT a heavy power block with a team
roof. A fixed mast rises through the platform hub to a small dark marker float on the surface (team top, warm beacon).
Identity from above: a dark bar with a team block at one end and three light rings in a row at the other, under the
water, a team dot on the surface (the Core T1 launcher is a dark X with corner pods; the Arm T2 launcher is a light float
over a hanging twin tube).
Pieces (COB): base, launcher (turn y; origin -0.04, 3.28, 0.02), barrel, coil1..3 (move z recoil; coils identical:
clones), bubbles/flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 15.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=211, drop=['coil2'], pose={'launcher': (0, 40, 0)}),
    preview_pose={'launcher': (0, -30, 0)},
)

GX = -15.8       # coilgun axis x (global)
GY = 3.88


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    b.plan(-1.0, 1.2, octagon(23.5), 'paint2', bevel=0.3, top_inset=1.2)
    b.cyl((0, 1.0, 0), (0, 2.4, 0), 10.0, 16, 'dark', bevel=0.1)
    for sz in (-1, 1):                                     # four team corner plates on the pad (diagonals)
        pts = []
        for ang in (30.0, 60.0):
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for r in (14.0, 20.4):
                pts += [(r * c, y, r * s_ * sz) for y in (1.1, 1.38)]
        b.hull(pts, 'team', bevel=0.0, mirror=True)
    b.cyl((0, 2.0, 0), (0, 13.0, 0), 1.8, 8, 'steel')     # marker mast through the hub
    b.cyl((0, 12.4, 0), (0, 17.4, 0), 4.2, 8, 'paint', r2=3.6, rot=math.pi / 8, bevel=0.25)
    b.cyl((0, 14.4, 0), (0, 15.6, 0), 4.45, 8, 'dark', rot=math.pi / 8)
    b.cyl((0, 17.3, 0), (0, 17.6, 0), 3.0, 8, 'team', rot=math.pi / 8)
    b.cyl((0, 17.5, 0), (0, 18.7, 0), 0.9, 8, 'lightr')

    # ---------------------------------------------------------------- launcher: swivel platform
    l = k.piece('launcher')
    l.cyl((0, 2.4, 0), (0, 6.6, 0), 5.2, 12, 'paint2', bevel=0.2)                   # hub ring
    l.hull([(x, y, z) for x in (-21.0, 21.0) for y in (2.4, 5.6) for z in (-4.0, 4.0)], 'paint', bevel=0.3)
    # right power block, team roof
    l.hull([(x, y, z) for x in (8.0, 21.6) for y in (2.4, 9.0) for z in (-9.0, 9.0)]
           + [(x, 10.4, z) for x in (9.6, 20.0) for z in (-7.4, 7.4)], 'paint', bevel=0.4)
    l.hull([(x, y, z) for x in (9.9, 19.7) for y in (10.35, 10.6) for z in (-7.1, 7.1)], 'team', bevel=0.0)
    for z in (-6.0, -2.0, 2.0):
        l.box((21.5, 4.0, z), (21.9, 8.0, z + 2.4), 'black', bevel=0.0)
    # left coilgun cradle and rail
    l.hull([(x, y, z) for x in (GX - 5.6, GX + 5.6) for y in (1.0, 2.6) for z in (-15.6, 10.0)], 'paint', bevel=0.25)
    l.cyl((GX, GY, -15.0), (GX, GY, 8.0), 2.0, 8, 'dark', rot=math.pi / 8)
    l.hull([(x, y, z) for x in (GX - 5.2, GX + 5.2) for y in (2.5, 2.8) for z in (-14.6, -9.0)], 'team', bevel=0.0)
    for z in (-12.0, 6.6):
        l.hull([(x, y, z0) for x in (GX - 4.4, GX + 4.4) for y in (2.4, 8.4) for z0 in (z, z + 1.6)], 'paint2',
               bevel=0.15)
    l.box((-6.0, 5.5, -1.0), (-4.0, 6.0, 1.0), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- barrel + coils
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -2.0), B(0, 0, 7.3), 2.4, 10, 'steel', bevel=0.06)
    br.cyl(B(0, 0, 7.1), B(0, 0, 7.4), 1.7, 10, 'black')
    br.cyl(B(0, 0, 4.0), B(0, 0, 5.0), 2.9, 10, 'dark')
    c = k.piece('coil1'); C = c.at
    c.cyl(C(0, 0, -0.9), C(0, 0, 0.9), 3.9, 12, 'steel', bevel=0.15)
    c.cyl(C(0, 0, -1.2), C(0, 0, 1.2), 2.6, 12, 'lightc')
    k.clone('coil2', 'coil1')
    k.clone('coil3', 'coil1')
