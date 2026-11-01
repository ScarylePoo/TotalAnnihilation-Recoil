"""Cloakable Fusion Reactor (ARM_T2_ECO_CloakableFusion) - Arm cloakable fusion. Two dark stepped reactor pyramids
side by side (dark / light / dark tiers, team ledges, a small glowing cyan dome on top), a dark coupling beam between
them, a cluster of three tall dark cloak-emitter masts with cyan tips at the front left and a row of capacitor
boxes along the front.
Identity from above: two dark concentric squares with team rings and cyan dots plus three emitter dots - darker and
squarer than the plain Arm fusion's two big light domes with team rings.
Pieces (Lua script): base (pyramids), pieces (capacitor boxes), cloakdoodads2 (masts + beam) - all at the origin.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=26, drop=['CloakDoodads2']),
    preview_pose={},
)

PX, PZ = 20.0, -6.0


def build(k):
    b = k.piece('base')
    b.plan(0.0, 2.6, [(-40.0, -28.0), (40.0, -28.0), (40.0, 26.0), (-40.0, 26.0)], 'paint2', bevel=0.3, top_inset=1.0)
    sq = lambda h: [(-PX - h, PZ - h), (-PX + h, PZ - h), (-PX + h, PZ + h), (-PX - h, PZ + h)]
    b.plan(2.5, 12.0, sq(18.0), 'paint2', bevel=0.35, top_inset=2.4, mirror=True)
    b.plan(11.9, 12.3, sq(15.4), 'team', bevel=0.0, mirror=True)
    b.plan(12.2, 26.0, sq(12.8), 'paint', bevel=0.35, top_inset=3.6, mirror=True)
    b.plan(25.9, 35.0, sq(8.4), 'paint2', bevel=0.3, top_inset=1.8, mirror=True)
    b.plan(34.9, 35.3, sq(6.2), 'team', bevel=0.0, mirror=True)
    b.sphere((-PX, 35.2, PZ), 3.8, 'lightc', segs=12, rings=6, scale=(1, 0.8, 1), mirror=True)
    # vent slots on the light tier (all four faces)
    for (ox, oz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        pts = []
        for y in (15.0, 20.0):
            h = 12.8 - (y - 12.2) / 13.8 * 3.6 / math.sqrt(2)
            for v in (-3.0, 3.0):
                for d in (0.05, 0.35):
                    pts.append((-PX + ox * (h + d) + oz * v, y, PZ + oz * (h + d) + ox * v))
        b.hull(pts, 'black', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ cloakdoodads2: emitter masts + coupling beam
    c = k.piece('CloakDoodads2')
    c.box((-PX + 8.0, 22.0, PZ - 3.0), (PX - 8.0, 27.0, PZ + 3.0), 'dark', bevel=0.3)
    c.box((-4.0, 26.9, PZ - 2.0), (4.0, 27.3, PZ + 2.0), 'hazard', bevel=0.0)
    for (mx, mz, h) in ((-33.0, 20.0, 52.0), (-26.0, 21.0, 46.0), (-32.0, 13.0, 40.0)):
        c.cyl((mx, 2.4, mz), (mx, h, mz), 2.8, 6, 'paint2', r2=2.2, rot=math.pi / 6, bevel=0.1)
        for y in (h * 0.5, h * 0.75):
            c.cyl((mx, y, mz), (mx, y + 1.4, mz), 3.0, 6, 'dark', rot=math.pi / 6)
        c.sphere((mx, h + 1.2, mz), 2.6, 'lightc', segs=8, rings=5)
    c.box((-35.6, 30.0, 12.0), (-24.0, 31.6, 22.0), 'dark', bevel=0.15)

    # ------------------------------------------------------------------ pieces: capacitor boxes along the front
    p = k.piece('pieces')
    for x0 in (-18.0, -9.0, 0.0, 9.0, 18.0, 27.0):
        p.box((x0, 2.5, 14.0), (x0 + 7.0, 9.0, 23.0), 'paint', bevel=0.3)
        p.box((x0 + 1.4, 8.9, 15.4), (x0 + 5.6, 9.3, 21.6), 'dark', bevel=0.0)
    p.cyl((-18.0, 6.0, 18.5), (34.0, 6.0, 18.5), 1.2, 8, 'steel')
