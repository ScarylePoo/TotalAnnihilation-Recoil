"""Air Repair Pad (ARM_T2_DEF_AirRepairPad) - Arm aircraft repair pad. A wide sloped plinth with a raised square landing
deck and two nano repair arms on brackets at the left and right edges. No moving parts.
Identity from above: a big light square with a team landing frame and team-capped nano arms either side, yellow-black
corner chevrons marking the landing zone (the meaningful hazard: it is a pad aircraft land on).
Pieces (COB): base, nano1/nano2 (repair arms), beam1/beam2 (nano emit points, empty), landpad (landing point, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=59, drop=['nano2']),
)

TOP = 20.0


def build(k):
    # ------------------------------------------------------------------ base: plinth + landing deck
    b = k.piece('base')
    b.plan(0.0, 2.6, [(-32.0, -29.0), (-29.0, -32.0), (29.0, -32.0), (32.0, -29.0), (32.0, 29.0), (29.0, 32.0),
                      (-29.0, 32.0), (-32.0, 29.0)], 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.4, 12.4, [(-30.0, -30.0), (30.0, -30.0), (30.0, 30.0), (-30.0, 30.0)], 'paint', bevel=0.35, top_inset=4.6)
    b.box((-26.4, 12.0, -26.4), (26.4, TOP, 26.4), 'paint', bevel=0.4)
    # dark deck border, team landing frame, central light
    for lo, hi in (((-26.0, -26.0), (26.0, -23.4)), ((-26.0, 23.4), (26.0, 26.0)), ((-26.0, -23.4), (-23.4, 23.4)), ((23.4, -23.4), (26.0, 23.4))):
        b.box((lo[0], TOP - 0.1, lo[1]), (hi[0], TOP + 0.3, hi[1]), 'dark', bevel=0.04)
    for lo, hi in (((-18.6, -18.6), (18.6, -12.2)), ((-18.6, 12.2), (18.6, 18.6)), ((-18.6, -12.2), (-12.2, 12.2)), ((12.2, -12.2), (18.6, 12.2))):
        b.box((lo[0], TOP - 0.1, lo[1]), (hi[0], TOP + 0.22, hi[1]), 'team', bevel=0.03)
    b.cyl((0, TOP - 0.1, 0), (0, TOP + 0.3, 0), 2.6, 12, 'lightw')
    # hazard corner chevrons (landing zone)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.hull([(sx * x, y, sz * z) for x, z in ((22.8, 22.8), (14.0, 22.8), (22.8, 14.0), (19.4, 19.4), (14.0, 19.4), (19.4, 14.0))
                    for y in (TOP - 0.1, TOP + 0.26)], 'hazard', bevel=0.02)
    # side hatches on the deck flanks and edge lights
    for sz in (-1, 1):
        b.box((-8.0, 13.6, sz * 26.4 - 0.4 if sz > 0 else -26.8), (8.0, 18.4, 26.8 if sz > 0 else -26.4 + 0.4), 'dark', bevel=0.08)
        for x in (-24.0, 24.0):
            b.box((x - 0.7, TOP + 0.2, sz * 25.3 - 0.4), (x + 0.7, TOP + 0.7, sz * 25.3 + 0.4), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ nano arms on the left/right edges (origin 0, 0, 0)
    n = k.piece('nano1')
    n.hull([(x, y, z) for x, y in ((-33.4, 2.0), (-27.0, 2.0), (-31.6, 13.0), (-27.0, 13.0)) for z in (-4.6, 4.6)], 'paint2', bevel=0.25)
    n.hull([(x, y, z) for x, y in ((-31.8, 12.6), (-26.6, 12.6), (-31.8, 25.4), (-28.0, 26.4)) for z in (-3.8, 3.8)], 'paint', bevel=0.25)
    n.cyl((-28.6, 23.2, 0), (-24.2, 23.2, 0), 2.2, 8, 'dark', r2=1.4, bevel=0.05)          # nozzle toward the deck
    n.box((-24.4, 22.6, -0.6), (-23.9, 23.8, 0.6), 'lightc', bevel=0.0)
    n.hull([(x, y, z) for x, y in ((-31.4, 25.35), (-28.4, 26.3), (-31.4, 25.6), (-28.4, 26.55)) for z in (-3.0, 3.0)], 'team', bevel=0.0)
    k.clone('nano2', 'nano1', mirror_x=True)
