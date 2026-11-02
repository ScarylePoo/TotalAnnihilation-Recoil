"""Silencer (CORE_T2_DEF_Silencer) - Core nuclear missile silo. A huge dark stepped bunker with a recessed hexagonal silo
hatch in its roof - two hazard-striped sliding nuke doors - and three coolant hoses running out of its back wall. To
launch, the doors slide apart, the hexagonal launch collar (tube) rises 16 elmo through the roof and the gantry (tower)
lifts the nuke 68 elmo until it stands far above the bunker.
Identity from above: a big dark rectangle with two long team strips flanking a yellow-black hexagonal hatch (the nuke
doors - the meaningful hazard); open, a light steel nuke standing in a hazard-ringed collar.
Built on the third-party S3O's piece layout (the COB drives it): base, hoses, doorl/doorr (move x), tube (move y),
tower (move y), nuke (move, hide/show), point (launch point, empty). All origins are at 0 in the S3O except point.
The preview shows the OPEN state (doors apart, collar and gantry up).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=67, drop=['doorr'], remove=['nuke', 'tower']),
    preview_pose={'doorl': {'move': (-20.0, 0, 0)}, 'doorr': {'move': (20.0, 0, 0)}, 'tube': {'move': (0, 16.25, 0)},
                  'tower': {'move': (0, 68.0, 0)}, 'nuke': {'move': (0.25, 0, 0.25)}},
)

RIM = 30.0                 # roof rim top
HEX = [(0.0, 34.6), (22.6, 17.2), (22.6, -17.2), (0.0, -34.6), (-22.6, -17.2), (-22.6, 17.2)]
RX, RZ = 37.0, 43.0        # roof outer half-size


def build(k):
    # ------------------------------------------------------------------ base: footing, body, roof rim round the hatch
    b = k.piece('base')
    b.plan(0.0, 4.0, [(-47.0, -50.0), (-44.0, -54.0), (44.0, -54.0), (47.0, -50.0), (47.0, 50.0), (44.0, 54.0),
                      (-44.0, 54.0), (-47.0, 50.0)], 'paint2', bevel=0.35, top_inset=1.2)
    b.hull([(x * sx, y, z * sz) for sx in (-1, 1) for sz in (-1, 1) for x, y, z in
            [(44.0, 3.8, 50.0), (RX, 20.4, RZ)]], 'paint', bevel=0.45)
    b.hull([(x, 20.2, z) for x, z in HEX] + [(x, 20.6, z) for x, z in HEX], 'black', bevel=0.0)       # silo floor
    # roof rim: four corner blocks and two side strips round the hexagonal opening
    for sz in (-1, 1):
        for sx in (-1, 1):
            poly = [(sx * 0.0, sz * RZ), (sx * RX, sz * RZ), (sx * RX, sz * 17.2), (sx * 22.6, sz * 17.2), (sx * 0.0, sz * 34.6)]
            b.hull([(x, y, z) for x, z in poly for y in (20.0, RIM)], 'paint', bevel=0.3)
    for sx in (-1, 1):
        b.hull([(x, y, z) for x in (sx * 22.6, sx * RX) for z in (-17.2, 17.2) for y in (20.0, RIM)], 'paint', bevel=0.3)
        # team strips along both long sides of the roof
        b.box((min(sx * 23.4, sx * 35.8), RIM - 0.1, -40.0), (max(sx * 23.4, sx * 35.8), RIM + 0.25, 40.0), 'team', bevel=0.04)
    # dark coaming round the hatch
    for i in range(6):
        (x0, z0), (x1, z1) = HEX[i], HEX[(i + 1) % 6]
        nx, nz = (z1 - z0), -(x1 - x0); n = math.hypot(nx, nz); nx, nz = nx / n, nz / n
        b.hull([(x + nx * d, y, z + nz * d) for x, z in ((x0, z0), (x1, z1)) for d in (0.0, 2.2) for y in (RIM - 0.1, RIM + 0.5)],
               'dark', bevel=0.05)
    # side vents and lights
    for sx in (-1, 1):
        b.hull([(sx * x, y, z) for x, y in ((41.2, 7.0), (39.0, 16.0), (41.6, 7.0), (39.4, 16.0)) for z in (-24.0, 24.0)], 'dark', bevel=0.06)
    b.box((-1.4, 22.0, 42.6), (1.4, 23.8, 43.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ hoses: three coolant pipes out of the back wall
    h = k.piece('hoses')
    for x in (-4.0, 12.0, 28.0):
        h.cyl((x, 13.0, 44.0), (x, 13.0, 58.0), 3.0, 8, 'dark', bevel=0.05)
        h.cyl((x, 13.0, 58.0), (x, 10.0, 64.0), 3.0, 8, 'dark', r2=3.0, bevel=0.05)
        h.cyl((x, 10.0, 64.0), (x, 0.0, 66.0), 3.0, 8, 'dark', bevel=0.05)
        h.cyl((x, -0.5, 66.0), (x, 2.0, 66.0), 4.4, 8, 'paint2', bevel=0.08)
        for z in (48.0, 54.0):
            h.cyl((x, 13.0, z), (x, 13.0, z + 1.2), 3.5, 8, 'steel')

    # ------------------------------------------------------------------ doors: the nuke doors (slide out along x)
    dl = k.piece('doorl')
    dl.hull([(x, y, z) for x, z in [(0.2, 34.4), (-22.4, 17.1), (-22.4, -17.1), (0.2, -34.4)] for y in (20.6, 21.9)], 'dark', bevel=0.15)
    dl.hull([(x, y, z) for x, z in [(-0.8, 31.6), (-20.8, 16.2), (-20.8, -16.2), (-0.8, -31.6)] for y in (21.85, 22.1)], 'hazard', bevel=0.03)
    k.clone('doorr', 'doorl', mirror_x=True)

    # ------------------------------------------------------------------ tube: hexagonal launch collar (rises 16.25)
    t = k.piece('tube')
    inner = [(x * 0.94, z * 0.94) for x, z in HEX]
    t.hull([(x, y, z) for x, z in inner for y in (-12.6, 17.6)], 'paint2', bevel=0.3)
    t.hull([(x * 0.9, y, z * 0.9) for x, z in HEX for y in (17.5, 20.3)], 'hazard', bevel=0.15)
    t.cyl((0, 20.25, 0), (0, 20.5, 0), 10.4, 12, 'black')

    # ------------------------------------------------------------------ tower: launch gantry behind the nuke
    g = k.piece('tower')
    for x in (-4.4, 4.4):
        g.box((x - 1.0, -51.4, 9.6), (x + 1.0, 4.6, 11.6), 'dark', bevel=0.08)
    for y in range(-46, 4, 8):
        g.box((-4.4, y, 10.0), (4.4, y + 1.4, 11.2), 'dark', bevel=0.05)
    for y in (-30.0, -6.0):
        g.box((-1.4, y, 6.6), (1.4, y + 2.0, 10.0), 'steel', bevel=0.05)    # clamps to the missile

    # ------------------------------------------------------------------ nuke (stands on the gantry)
    n = k.piece('nuke')
    n.cyl((0, -54.0, 0), (0, 4.0, 0), 6.4, 12, 'steel', bevel=0.08)
    n.cyl((0, 4.0, 0), (0, 20.6, 0), 6.4, 12, 'steel', r2=1.2, bevel=0.08)
    n.cyl((0, -2.0, 0), (0, 4.0, 0), 6.55, 12, 'hazard')
    n.cyl((0, -40.0, 0), (0, -37.0, 0), 6.55, 12, 'dark')
    n.box((-0.9, 20.2, -0.9), (0.9, 21.6, 0.9), 'lightr', bevel=0.0)
    for ang in (0, 90, 180, 270):
        a = math.radians(ang + 45)
        n.hull([(math.cos(a) * rr, y, math.sin(a) * rr) for rr in (5.0, 9.6) for y in (-54.0, -44.0)] +
               [(math.cos(a) * 5.0, -34.0, math.sin(a) * 5.0)], 'paint2', bevel=0.1)
