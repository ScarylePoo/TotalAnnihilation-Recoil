"""Cloakable Fusion Reactor (CORE_T2_ECO_CloakableFusion) - Core cloakable fusion. A truncated-triangle dark plinth on a
ground pad, a dark containment globe held in a tripod cage of three heavy light-steel legs that rise from the plinth
corners and arch over the globe to meet above it, each arm carrying a team strip; warm glowing seams on the globe.
Identity from above: a light steel 'Y' of three team-striped arms over a dark ball on a triangle (the plain Core
fusion is a huge light globe with three free-standing leaning towers; the Arm cloakable fusion is two dark pyramids).
Pieces (COB): GP (ground pad, root), Base (plinth + cage), Shpere (globe) - all at the origin, static.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=28, drop=['Shpere']),
    preview_pose={},
)

CX, CZ = 0.0, -4.0
GY, GR = 43.0, 16.0


def radial(ang):
    a = math.radians(ang); d = (math.cos(a), math.sin(a)); p = (-d[1], d[0])
    return lambda u, v, y: (CX + d[0] * u + p[0] * v, y, CZ + d[1] * u + p[1] * v)


def build(k):
    tri = []
    for ang in (90, 210, 330):          # truncated triangle (corners cut)
        for da in (-24, 24):
            a = math.radians(ang + da)
            tri.append((CX + 36.0 * math.cos(a), CZ + 36.0 * math.sin(a)))
    g = k.piece('GP')
    g.plan(-0.2, 1.0, [(CX + (x - CX) * 1.1, CZ + (z - CZ) * 1.1) for x, z in tri], 'paint2', bevel=0.2,
           top_inset=0.6)

    b = k.piece('Base')
    b.plan(0.7, 16.0, tri, 'paint', bevel=0.4, top_inset=4.0)
    b.plan(15.9, 19.0, [(CX + (x - CX) * 0.8, CZ + (z - CZ) * 0.8) for x, z in tri], 'paint2', bevel=0.25,
           top_inset=1.0)
    b.cyl((CX, 18.9, CZ), (CX, 28.0, CZ), 9.0, 12, 'dark', r2=7.0, rot=math.pi / 12, bevel=0.15)
    # cage legs: 90 (front) built whole, 330 mirrored to 210
    for ang, m in ((90, False), (330, True)):
        P = radial(ang)
        b.hull([P(u, v, y) for (u, y) in ((25.0, 8.0), (33.0, 8.0), (33.0, 14.0), (27.6, 60.0), (22.0, 62.0),
                                          (21.0, 24.0)) for v in (-3.6, 3.6)], 'steel', bevel=0.35, mirror=m)
        b.hull([P(u, v, y) for (u, y) in ((25.0, 58.0), (28.0, 62.0), (26.0, 67.0), (4.0, 69.0), (3.0, 64.0))
                for v in (-3.2, 3.2)], 'steel', bevel=0.35, mirror=m)
        top = lambda u: 67.0 + (26.0 - u) * 2.0 / 22.0
        b.hull([P(u, v, top(u) + dy) for u in (5.0, 25.0) for v in (-2.9, 2.9) for dy in (0.1, 0.35)], 'team',
               bevel=0.0, mirror=m)
        b.hull([P(u, v, y) for (u, y) in ((31.0, 22.0), (31.4, 22.0), (29.4, 40.0), (29.8, 40.0)) for v in (-1.0, 1.0)],
               'dark', bevel=0.0, mirror=m)
        b.hull([P(u, v, y) for (u, y) in ((32.9, 9.0), (33.2, 9.0), (32.9, 12.6), (33.2, 12.6)) for v in (-3.0, 3.0)],
               'hazard', bevel=0.0, mirror=m)
    # team plates on the deck between the legs (outside the globe's shadow from above)
    for ang in (30, 150, 270):
        P = radial(ang)
        b.hull([P(u, v, y) for u in (14.0, 21.0) for v in (-8.5 + (21.0 - u) * 0.0, 8.5) for y in (18.95, 19.3)],
               'team', bevel=0.0)
    # crown hub where the arms meet
    b.cyl((CX, 64.0, CZ), (CX, 70.4, CZ), 5.6, 6, 'dark', rot=math.pi / 6, bevel=0.2)
    b.cyl((CX, 70.3, CZ), (CX, 71.0, CZ), 3.0, 6, 'lightc', rot=math.pi / 6)

    # ------------------------------------------------------------------ Shpere: the containment globe
    s = k.piece('Shpere')
    s.sphere((CX, GY, CZ), GR, 'paint2', segs=18, rings=9, scale=(1, 0.95, 1))
    for y, rr in ((GY, GR), (GY + 8.5, GR * math.cos(math.asin(8.5 / (GR * 0.95))))):
        s.cyl((CX, y - 0.6, CZ), (CX, y + 0.6, CZ), rr + 0.3, 18, 'lightc', rot=math.pi / 18)
    # team polar cap (the globe top is what the game camera sees between the cage arms)
    cap = []
    for j in range(4):
        lat = math.radians(48 + (90 - 48) * j / 4)
        for i in range(18):
            lon = 2 * math.pi * i / 18 + math.pi / 18
            rr = (GR + 0.15) * math.cos(lat)
            cap.append((CX + rr * math.cos(lon), GY + (GR + 0.15) * math.sin(lat) * 0.95, CZ + rr * math.sin(lon)))
    cap += [(CX, GY + (GR + 0.15) * 0.95, CZ), (CX, GY + (GR + 0.15) * math.sin(math.radians(48)) * 0.95 * 0.98, CZ)]
    s.hull(cap, 'team', bevel=0.0)
    s.cyl((CX, GY + GR * 0.95 - 1.0, CZ), (CX, GY + GR * 0.95 + 0.4, CZ), 5.0, 12, 'dark', rot=math.pi / 12)
