"""Moho Mine (CORE_T2_ECO_MohoMine) - Core moho mine. A broad dark stepped hexagonal mound over the metal spot whose top
is a hexagonal hatch (the 'shell') on an axle between two steel stands. Closed it is an armoured hex pyramid lid;
switched on, the stands lift the lid, it rolls over 180 deg on its axle and settles back, so its underside - a team
ring round a dark centre - faces up and the extractor that hung beneath it (a rotary arm with a steel drill bit and
a team-capped motor at its tip) now stands on top and spins.
Identity from above (on): dark hexagon, a team hex ring with a steel rotor arm sweeping over it (the Arm moho is a
light octagon under a three-armed frame; the T1 Core mex is a small hex pyramid with a claw).
Pieces (COB): base, stands (move y), shell (turn x -180 to open; origin -22.2, 27.06, 0), rotary (spin y), dingle1
(drill), dingle2 (motor) - rotary/dingles hang under the shell at rest and are hidden by the script when closed.
Preview: ON (shell rolled over).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=32, drop=['dingle2'], pose={'shell': (-140, 0, 0)}),
    preview_pose={'shell': (-180, 0, 0), 'rotary': (0, 30, 0)},
)

SY = 27.06
RL = 22.2       # lid hex radius (vertices on +-x, on the axle)


def hexa(r, rot=0.0):
    return [(r * math.cos(rot + i * math.pi / 3), r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 4.0, hexa(42.9), 'paint2', bevel=0.35, top_inset=1.2)
    b.plan(3.9, 17.0, hexa(40.0), 'paint', bevel=0.4, top_inset=4.0)
    b.plan(16.9, 26.6, hexa(35.0), 'paint', bevel=0.35, top_inset=5.4)
    b.plan(26.5, 27.0, hexa(28.6), 'paint2', bevel=0.1, top_inset=0.4)
    b.plan(26.9, 27.1, hexa(RL + 1.0), 'black', bevel=0.0)
    # ochre-striped bands and dark vents on the lower step faces
    for i in range(6):
        a = math.pi / 6 + i * math.pi / 3; ox, oz = math.cos(a), math.sin(a); px, pz = -oz, ox
        ap = lambda y: (40.0 - (y - 3.9) / 13.1 * 4.0) * math.cos(math.pi / 6)
        mat = 'hazard' if i % 3 == 1 else 'black'
        b.hull([(ox * (ap(y) + d) + px * v, y, oz * (ap(y) + d) + pz * v) for y in (7.0, 11.0)
                for v in (-9.0, 9.0) for d in (0.05, 0.35)], mat, bevel=0.0)
    b.box((-1.4, 1.0, 37.0), (1.4, 2.6, 37.3), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ stands: axle posts at the lid's +-x vertices
    s = k.piece('stands')
    for sx in (-1, 1):
        x0, x1 = sorted((sx * (RL + 0.4), sx * (RL + 4.6)))
        s.box((x0, 14.0, -3.4), (x1, 28.4, 3.4), 'steel', bevel=0.3)
        s.cyl((sx * (RL - 0.6), SY, 0), (sx * (RL + 4.9), SY, 0), 2.4, 8, 'dark', rot=math.pi / 8)

    # ------------------------------------------------------------------ shell: the lid (pyramid up, team ring down)
    sh = k.piece('shell')
    sh.plan(SY - 0.6, SY + 0.8, hexa(RL), 'paint2', bevel=0.25, top_inset=0.4)
    sh.hull([(x, SY + 0.7, z) for x, z in hexa(RL - 1.2)] + [(x, SY + 7.6, z) for x, z in hexa(6.0)], 'paint',
            bevel=0.3)
    sh.cyl((0, SY + 7.5, 0), (0, SY + 9.2, 0), 4.6, 6, 'dark', bevel=0.1)
    sh.plan(SY - 0.95, SY - 0.55, hexa(RL - 1.0), 'team', bevel=0.0)
    sh.plan(SY - 1.3, SY - 0.9, hexa(10.0), 'dark', bevel=0.05)
    for i in range(6):           # dark ribs over the team ring (underside)
        a = i * math.pi / 3 + math.pi / 6; ox, oz = math.cos(a), math.sin(a); px, pz = -oz, ox
        sh.hull([(ox * u + px * v, y, oz * u + pz * v) for u in (10.0, RL - 2.0) for v in (-0.9, 0.9)
                 for y in (SY - 1.25, SY - 0.9)], 'dark', bevel=0.0)

    # ------------------------------------------------------------------ rotary: hub + arm, hanging under the lid
    r = k.piece('rotary')
    ry = k.P['rotary'][1]
    r.cyl((0, ry - 9.4, 0), (0, ry - 1.2, 0), 5.0, 8, 'dark', rot=math.pi / 8, bevel=0.15)
    r.hull([(x, y, z) for x in (2.0, 21.0) for y in (ry - 9.6, ry - 5.6) for z in (-3.6, 3.6)], 'steel', bevel=0.3)
    r.box((4.0, ry - 9.95, -2.4), (16.0, ry - 9.55, 2.4), 'hazard', bevel=0.0)
    r.cyl((0, ry - 10.2, 0), (0, ry - 9.3, 0), 2.6, 8, 'lightc', rot=math.pi / 8)

    # ------------------------------------------------------------------ dingle1: drill bit (points down once flipped)
    d1 = k.piece('dingle1'); D = d1.at
    d1.cyl(D(0, 0.0, 0), D(0, 1.6, 0), 4.0, 8, 'dark', rot=math.pi / 8, bevel=0.1)
    d1.cyl(D(0, 1.5, 0), D(0, 6.8, 0), 3.0, 8, 'steel', r2=0.6, rot=math.pi / 8)
    for yy in (2.6, 4.4):
        d1.cyl(D(0, yy, 0), D(0, yy + 0.6, 0), 3.0 - (yy - 1.5) * 0.45 + 0.35, 8, 'dark', rot=math.pi / 8)
    # ------------------------------------------------------------------ dingle2: motor (on top once flipped)
    d2 = k.piece('dingle2'); D2 = d2.at
    d2.hull([D2(x, y, z) for x in (-4.4, 4.4) for y in (-0.2, -6.4) for z in (-4.4, 4.4)], 'paint', bevel=0.35)
    d2.box(D2(-3.4, -6.75, -3.4), D2(3.4, -6.35, 3.4), 'team', bevel=0.0)
    d2.box(D2(4.3, -5.0, -2.0), D2(4.6, -1.4, 2.0), 'black', bevel=0.0)
