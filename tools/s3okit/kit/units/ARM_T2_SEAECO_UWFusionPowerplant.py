"""Underwater Fusion Powerplant (ARM_T2_SEAECO_UWFusionPowerplant) - Arm seabed fusion (no waterline: sits on the sea bed
under at least 15 elmo of water). The land Arm fusion's twin light reactors, rebuilt as two tall stepped light cones
(pressure-proof) on a broad dark foundation, each girdled near the top by a wide team containment collar and crowned
by a glowing cyan dome (dome1/dome2); a dark conduit bridge joins them and a low pump annex with a team roof and steel
pipes sits in front, its exhaust vent at emit1.
Identity from above (through the water): two light circles with team rings and cyan centres side by side (twin eyes,
like the land fusion) but on tall cones over a dark slab, a team block in front (the Core UW fusion is a single dark
caisson with a half-sunk steel globe and two towers).
Pieces (Lua script): base, dome1/dome2 (origin 0,0,0; crowns at x -/+17.35, z -6.25), emit1 (empty vent point).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    preview_water=15.0,
    wreck=dict(seed=111, drop=['dome2']),
)

TX, TZ = 17.35, -6.25


def octagon(r, cx=0.0, cz=0.0, rot=math.pi / 8):
    return [(cx + r * math.cos(rot + i * math.pi / 4), cz + r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 4.0, [(-38.0, -30.0), (38.0, -30.0), (41.0, -26.0), (41.0, 26.0), (38.0, 30.0), (-38.0, 30.0),
                      (-41.0, 26.0), (-41.0, -26.0)], 'paint2', bevel=0.4, top_inset=1.4)
    # twin towers (+x built, mirrored)
    b.plan(3.6, 9.0, octagon(17.0, TX, TZ), 'paint', bevel=0.35, top_inset=2.0, mirror=True)
    b.plan(8.8, 10.0, octagon(15.2, TX, TZ), 'dark', bevel=0.1, mirror=True)
    b.hull([(x, 9.8, z) for x, z in octagon(13.6, TX, TZ)] + [(x, 27.0, z) for x, z in octagon(9.6, TX, TZ)],
           'paint', bevel=0.4, mirror=True)
    for y in (14.0, 19.5):
        b.hull([(x, yy, z) for x, z in octagon(13.6 - (y - 9.8) * 4.0 / 17.2 + 0.25, TX, TZ) for yy in (y, y + 1.4)],
               'dark', bevel=0.0, mirror=True)
    b.plan(26.8, 29.4, octagon(12.6, TX, TZ), 'team', bevel=0.25, top_inset=1.6, mirror=True)       # collar
    b.hull([(x, 29.2, z) for x, z in octagon(9.4, TX, TZ)] + [(x, 36.0, z) for x, z in octagon(6.8, TX, TZ)],
           'paint', bevel=0.3, mirror=True)
    b.cyl((TX, 35.8, TZ), (TX, 37.6, TZ), 6.8, 16, 'dark', bevel=0.1, mirror=True)
    b.box((TX - 1.0, 31.0, TZ + 8.6), (TX + 1.0, 32.2, TZ + 8.95), 'lightc', bevel=0.0, mirror=True)
    # conduit bridge between the towers (crosses x = 0)
    b.hull([(x, y, z) for x in (-8.0, 8.0) for y in (17.0, 22.0) for z in (TZ - 3.0, TZ + 3.0)], 'paint2', bevel=0.25)
    b.cyl((-7.0, 19.5, TZ), (7.0, 19.5, TZ), 1.2, 8, 'lightc')
    # pump annex in front (asymmetric: towards +x, vent at emit1)
    b.plan(3.8, 11.0, [(-24.0, 12.0), (30.0, 12.0), (30.0, 25.0), (-24.0, 25.0)], 'paint', bevel=0.3, top_inset=1.0)
    b.box((-22.0, 10.95, 13.8), (27.4, 11.2, 23.2), 'team', bevel=0.0)
    b.box((17.5, 3.8, 18.0), (25.5, 9.6, 26.8), 'dark', bevel=0.2)
    for x in (18.5, 20.5, 22.5, 24.5):
        b.box((x, 4.4, 26.7), (x + 1.0, 9.0, 26.95), 'black', bevel=0.0)
    for x in (-14.0, 6.0):
        b.cyl((x, 7.5, 12.0), (x, 7.5, 2.0), 1.8, 8, 'steel', mirror=False)
    b.cyl((-14.0, 7.5, 2.0), (-TX + 4.0, 7.5, 2.0), 1.8, 8, 'steel')
    b.cyl((6.0, 7.5, 2.0), (TX - 4.0, 7.5, 2.0), 1.8, 8, 'steel')

    # ---------------------------------------------------------------- domes: cyan reactor crowns
    d = k.piece('dome1')
    d.sphere((-TX, 37.4, TZ), 5.6, 'lightc', segs=16, rings=8, scale=(1, 0.85, 1))
    d.cyl((-TX, 41.6, TZ), (-TX, 42.8, TZ), 1.6, 8, 'steel')
    k.clone('dome2', 'dome1', mirror_x=True)
