"""Advanced Kbot Lab (ARM_T2_LAB_AdvancedKbotLab) - Arm T2 kbot factory. Closed: a tall light hall over the pad
whose roof rises to a central peak - four quarter shells (quarter1..4) with team upper roof slopes, standing on two
inner gantry frames (centerbar1/2) between four leaning corner pylons and two hazard-striped slide rails. On
activation the gantries slide 22.5 apart (move x) carrying their two quarters each, the quarters part again along z,
so the hall opens into four team-roofed corner towers, and the long nano rails (nano1/nano2) slide in 10 toward the
pad between them.
Arm lab family (T2 = taller, more parts): light chamfered blocks, team roofs, dark lane with hazard edges, light round
pad, cyan lights. Identity from above (open): four peaked team-roofed towers round a dark lane and a light disc, two
long hazard rails with cyan emitters along the lane edges (the T1 kbot lab is a flat cross with two tilted lids).
Pieces (COB): base, centerbar1/2 (move x), quarter1..4 (move z), nano1/2 (move x), beam1/2 (empty nano emit
points), pad (spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['centerbar1', 'centerbar2', 'nano1', 'nano2'],
    wreck=dict(seed=73, drop=['quarter3']),
    preview_pose={
        'centerbar1': {'move': (-22.5, 0, 0)}, 'centerbar2': {'move': (22.5, 0, 0)},
        'quarter1': {'move': (0, 0, -14.625)}, 'quarter2': {'move': (0, 0, 16.125)},
        'quarter3': {'move': (0, 0, 16.0)}, 'quarter4': {'move': (0, 0, -14.875)},
        'nano1': {'move': (10.0, 0, 0)}, 'nano2': {'move': (-10.125, 0, 0)},
    },
)

WY, RY = 19.0, 34.0  # hall wall top, roof peak


def quarter(k, name, sx, sz):
    """one hall quadrant in global rest coords: x from 0 to sx*21.1, z from ~0 to sz*24.6, peaked roof toward (0, 0)"""
    q = k.piece(name)
    X, Z = sx * 21.1, sz * 24.6
    xi, zi = sx * 0.15, sz * 0.15
    q.box((min(xi, X), 0.35, min(zi, Z)), (max(xi, X), WY, max(zi, Z)), 'paint', bevel=0.35)
    q.box((min(X - sx * 0.3, X + sx * 0.2), 4.0, min(zi + sz * 3.0, Z - sz * 3.0)),
          (max(X - sx * 0.3, X + sx * 0.2), 12.0, max(zi + sz * 3.0, Z - sz * 3.0)), 'paint2', bevel=0.1)
    q.box((min(X, X + sx * 0.3), 14.0, min(zi + sz * 5.0, Z - sz * 5.0)),
          (max(X, X + sx * 0.3), 15.2, max(zi + sz * 5.0, Z - sz * 5.0)), 'lightc', bevel=0.0)
    f = lambda t: (sx * (21.1 * (1 - t) + 0.15 * t), sz * (24.6 * (1 - t) + 0.15 * t))   # roof edge shrink
    mid = 0.12
    xm, zm = f(mid)
    q.hull([(x, WY - 0.2, z) for x in (xi, X) for z in (zi, Z)]
           + [(x, WY + (RY - WY) * mid, z) for x in (xi, xm) for z in (zi, zm)], 'paint', bevel=0.3)
    q.hull([(x, WY + (RY - WY) * mid - 0.1, z) for x in (xi, xm) for z in (zi, zm)]
           + [(x, RY, z) for x in (xi, sx * 1.6) for z in (zi, sz * 1.6)], 'team', bevel=0.25)


def build(k):
    # ------------------------------------------------------------------ base: lane, rails, corner pylons
    b = k.piece('base')
    b.box((-24.0, 0.0, -48.0), (24.0, 0.3, 48.0), 'paint2', bevel=0.05)
    b.box((-24.0, 0.0, -48.0), (-21.0, 0.45, 48.0), 'hazard', bevel=0.04, mirror=True)
    for z0, z1 in ((-42.0, -14.0), (14.0, 42.0)):                              # slide beds under the towers
        b.box((-45.0, 0.0, z0), (-24.0, 0.35, z1), 'dark', bevel=0.05, mirror=True)
    for x in (-40.0, -28.0):                                                  # slide rails (hazard tops)
        b.box((x - 1.2, 0.0, -44.0), (x + 1.2, 1.4, 44.0), 'paint2', bevel=0.15, mirror=True)
        b.box((x - 1.0, 1.35, -43.0), (x + 1.0, 1.7, 43.0), 'hazard', bevel=0.04, mirror=True)
    for zs in (1, -1):                                                        # leaning corner pylons
        z0, z1 = sorted((zs * 43.0, zs * 48.0))
        za, zb = sorted((zs * 41.0, zs * 47.0))
        b.hull([(x, 0.0, z) for x in (-40.0, -31.0) for z in (za, zb)]
               + [(x, 16.0, z) for x in (-38.5, -33.0) for z in (zs * 43.5 - 1.5, zs * 43.5 + 1.5)], 'paint',
               bevel=0.3, mirror=True)
        b.box((-38.2, 15.9, zs * 43.5 - 1.3), (-33.3, 16.4, zs * 43.5 + 1.3), 'team', bevel=0.06, mirror=True)
        b.box((-32.3, 8.0, zs * 44.5 - 0.6), (-31.85, 9.4, zs * 44.5 + 0.6), 'lightc', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ gantry frames (centerbar origin 0)
    c = k.piece('centerbar1')
    for z in (-17.0, 15.0):
        c.box((-13.4, 0.35, z - 1.6), (-4.2, 15.0, z + 1.6), 'dark', bevel=0.25)
    c.box((-13.4, 13.0, -18.6), (-4.2, 15.0, 16.6), 'dark', bevel=0.25)
    c.box((-12.8, 14.9, -18.0), (-4.8, 15.4, 16.0), 'hazard', bevel=0.05)
    k.clone('centerbar2', 'centerbar1', mirror_x=True)
    # nano rails (nano1 origin -13.75, 7, -1.11): rail along z, emitter at beam1 (10, -0.62, -1.12)
    n = k.piece('nano1'); N = n.at
    n.box(N(0.2, -2.0, -19.6), N(3.4, 3.0, 19.4), 'paint', bevel=0.25)
    n.box(N(0.6, 2.9, -19.0), N(3.0, 3.4, 18.8), 'hazard', bevel=0.04)
    for z in (-12.0, -1.12, 10.0):
        n.cyl(N(3.2, -0.62, z), N(9.0, -0.62, z), 1.5, 10, 'dark', r2=1.0)
        n.cyl(N(8.9, -0.62, z), N(10.0, -0.62, z), 1.05, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ hall quarters
    quarter(k, 'quarter1', -1, -1)
    quarter(k, 'quarter2', -1, 1)
    quarter(k, 'quarter3', 1, 1)
    quarter(k, 'quarter4', 1, -1)

    # ------------------------------------------------------------------ pad (origin 0.5, 0.4, -1): spinning disc
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, -0.1, 0), Pp(0, 0.4, 0), 18.0, 36, 'dark', bevel=0.12)
    p.cyl(Pp(0, 0.4, 0), Pp(0, 0.52, 0), 16.2, 36, 'paint')
    p.cyl(Pp(0, 0.5, 0), Pp(0, 0.6, 0), 3.2, 16, 'paint2')
