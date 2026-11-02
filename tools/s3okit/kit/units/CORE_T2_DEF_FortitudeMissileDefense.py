"""Fortitude Missile Defense (CORE_T2_DEF_FortitudeMissileDefense) - Core anti-nuke. A broad square slab carrying a squat
octagonal blockhouse with four side buttresses and a stubby launch collar on its roof, flanked by three sensor domes.
To fire, the hazard-striped hatch (wedge) slides off a roof slot, an erector rail (drawer) rises 23.5 elmo through it
and the interceptor (dummy) slides over onto the collar.
Identity from above: a dark square slab with team L-corners, a dark octagon roof with a team ring, a light steel
collar with an ochre silo-mouth ring and an ochre hatch - squat and square where the Arm Protector is a tall
petal silo.
Pieces (COB): base, collar, buttons, wedge (move x), drawer (move y), dummy (move x, hide/show: the missile).
The preview shows the OPEN state (wedge slid off, rail up, missile over the collar).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=33, drop=['wedge']),
    preview_pose={'wedge': {'move': (-5.75, 0, 0)}, 'drawer': {'move': (0, 23.5, 0)}, 'dummy': {'move': (5.25, 0, 0)}},
)

TOP = 30.0


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: slab + blockhouse
    b = k.piece('base')
    b.plan(0.0, 5.0, [(-25.0, -25.0), (25.0, -25.0), (25.0, 25.0), (-25.0, 25.0)], 'paint2', bevel=0.3, top_inset=1.2)
    # team L-corners on the slab top
    for s in (-1, 1):
        for t in (-1, 1):
            b.box((min(12.0 * s, 23.2 * s), 5.0, min(18.6 * t, 23.2 * t)), (max(12.0 * s, 23.2 * s), 5.25, max(18.6 * t, 23.2 * t)),
                  'team', bevel=0.03)
            b.box((min(18.6 * s, 23.2 * s), 5.0, min(12.0 * t, 18.6 * t)), (max(18.6 * s, 23.2 * s), 5.25, max(12.0 * t, 18.6 * t)),
                  'team', bevel=0.03)
    # octagonal blockhouse
    b.plan(4.8, TOP, octagon(13.6), 'paint', bevel=0.35, top_inset=1.0)
    # four side buttresses (the TA side blocks), sloped
    for ux, uz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        px, pz = -uz, ux
        b.hull([(ux * u + px * w, y, uz * u + pz * w) for u, y in ((11.0, 4.8), (19.4, 4.8), (11.0, 21.0), (15.4, 18.0))
                for w in (-4.4, 4.4)], 'paint2', bevel=0.3)
    # roof: dark cap with a team ring and the rail slot (x -8.7..-3, under the hatch)
    b.plan(TOP - 0.4, TOP + 0.2, octagon(12.4), 'dark', bevel=0.1)
    ring_o, ring_i = octagon(12.0), octagon(8.4)
    for i in range(8):
        a, c = ring_o[i], ring_o[(i + 1) % 8]; d, e = ring_i[i], ring_i[(i + 1) % 8]
        b.hull([(x, y, z) for x, z in (a, c, d, e) for y in (TOP + 0.2, TOP + 0.45)], 'team', bevel=0.0)
    b.box((-8.9, TOP + 0.2, -2.2), (-3.0, TOP + 0.5, 2.2), 'black', bevel=0.0)
    # door on the front face and lights
    b.box((-3.6, 4.8, 12.6), (3.6, 15.0, 13.4), 'dark', bevel=0.1)
    b.box((-1.0, 16.0, 12.7), (1.0, 17.2, 13.3), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ collar: the launch collar (light steel, ochre mouth)
    c = k.piece('collar')
    c.hull([(x, y, z) for y, r in ((TOP + 0.1, 7.0), (TOP + 6.0, 5.4)) for x, z in octagon(r)], 'steel', bevel=0.2)
    c.hull([(x, y, z) for y, r in ((TOP + 5.95, 5.45), (TOP + 8.7, 4.2)) for x, z in octagon(r)], 'hazard', bevel=0.1)
    c.hull([(x, TOP + 8.75, z) for x, z in octagon(3.0)] + [(x, TOP + 8.5, z) for x, z in octagon(3.2)], 'black', bevel=0.0)

    # ------------------------------------------------------------------ buttons: three sensor domes on the roof
    bt = k.piece('buttons')
    for x, z in ((10.0, 0.0), (0.0, 10.0), (0.0, -10.0)):
        bt.cyl((x, TOP + 0.2, z), (x, TOP + 1.2, z), 2.4, 8, 'dark', rot=math.pi / 8, bevel=0.06)
        bt.cyl((x, TOP + 1.2, z), (x, TOP + 2.4, z), 2.0, 8, 'steel', r2=1.0, rot=math.pi / 8, bevel=0.06)
        bt.box((x - 0.4, TOP + 2.35, z - 0.4), (x + 0.4, TOP + 2.75, z + 0.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ wedge: the rail-slot hatch (origin -3.75, 30, 0)
    w = k.piece('wedge'); W = w.at
    w.hull([W(x, y, z) for x, y in ((-5.4, 0.2), (0.6, 0.2), (-5.4, 2.4), (0.0, 3.6)) for z in (-3.6, 3.6)], 'hazard', bevel=0.12)

    # ------------------------------------------------------------------ drawer: erector rail (origin -7.5, 6.5, 0)
    d = k.piece('drawer'); D = d.at
    d.box(D(-1.2, 0.0, -1.8), D(1.4, 23.0, 1.8), 'dark', bevel=0.12)
    d.box(D(1.4, 6.0, -1.2), D(4.4, 21.6, 1.2), 'steel', bevel=0.08)

    # ------------------------------------------------------------------ dummy: the interceptor (origin -5.13, 17.76, 0)
    m = k.piece('dummy'); M = m.at
    m.cyl(M(0, -10.8, 0), M(0, 7.2, 0), 1.9, 10, 'steel')
    m.cyl(M(0, 7.2, 0), M(0, 11.0, 0), 1.9, 10, 'paint', r2=0.4)
    m.cyl(M(0, 5.8, 0), M(0, 7.2, 0), 1.98, 10, 'hazard')
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        m.hull([M(math.cos(a) * rr, y, math.sin(a) * rr) for rr in (1.3, 3.4) for y in (-10.8, -6.2)] +
               [M(math.cos(a) * 1.3, -3.2, math.sin(a) * 1.3)], 'dark', bevel=0.0)
