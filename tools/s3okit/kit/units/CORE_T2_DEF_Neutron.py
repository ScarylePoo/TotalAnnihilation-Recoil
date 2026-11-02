"""Neutron (CORE_T2_DEF_Neutron) - Core tactical nuke launcher. A star-shaped bunker: four tall dark spires on the
diagonals, four sloped buttresses on the axes and a central octagonal silo capped by a hazard-striped lid. To fire, the
four vent blocks between the spires rise, the lid flips over (~160 deg) and the missile (riser) climbs 36 elmo out of
the silo.
Identity from above: a dark four-point star of spires with team buttress tops on the axes, a light steel silo rim and
the yellow-black nuke lid in the middle (hazard only there: it is the nuke door).
Pieces (COB): base, vents (move y), fliptop (turn z), riser (move y, hide/show: the missile), emit (missile tip, empty).
The preview shows the OPEN state (vents up, lid flipped, missile raised).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=35, remove=['riser'], pose={'fliptop': (0, 0, -60)}),
    preview_pose={'vents': {'move': (0, 11.75, 0)}, 'riser': {'move': (0, 35.875, 0)}, 'fliptop': (0, 0, -160)},
)

SILO = 36.25


def octagon(r, rot=math.pi / 8, cx=0.0, cz=0.0):
    return [(cx + r * math.cos(rot + i * math.pi / 4), cz + r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base
    b = k.piece('base')
    b.plan(0.0, 3.0, octagon(26.4), 'paint2', bevel=0.3, top_inset=1.0)
    # central silo tower and its steel rim
    b.plan(2.8, SILO - 1.4, octagon(9.0), 'paint', bevel=0.3, top_inset=1.0)
    b.hull([(x, y, z) for y, r in ((SILO - 1.6, 8.2), (SILO, 7.2)) for x, z in octagon(r)], 'steel', bevel=0.15)
    b.hull([(x, SILO + 0.02, z) for x, z in octagon(5.0)] + [(x, SILO - 0.4, z) for x, z in octagon(5.0)], 'black', bevel=0.0)
    # four axis buttresses, sloping down outward; team on their sloped tops
    for ux, uz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        px, pz = -uz, ux
        prof = ((6.0, 2.8), (25.4, 2.8), (25.4, 7.0), (8.0, 27.0), (6.0, 27.0))
        b.hull([(ux * u + px * w, y, uz * u + pz * w) for u, y in prof for w in (-6.2, 6.2)], 'paint', bevel=0.3)
        tp = []
        for u in (10.4, 23.4):
            y = 27.0 - (u - 8.0) * 20.0 / 17.4
            for w in (-4.8, 4.8):
                for d in (0.1, 0.3):
                    tp.append((ux * u + px * w, y + d, uz * u + pz * w))
        b.hull(tp, 'team', bevel=0.0)
    # four diagonal spires
    for sx in (-1, 1):
        for sz in (-1, 1):
            q = [(sx * x, z * sz) for x, z in ((8.0, 14.0), (14.0, 8.0), (23.0, 15.0), (15.0, 23.0))]
            b.hull([(x, 2.8, z) for x, z in q] + [(sx * 14.6, 46.0, sz * 14.6), (sx * 12.6, 44.0, sz * 12.6)], 'paint2', bevel=0.3)
            # dark slot where the vent block rises (inner face of the spire)
            b.hull([(sx * x, y, sz * z) for x, z in ((8.6, 12.0), (12.0, 8.6)) for y in (8.0, 24.0)] +
                   [(sx * x, y, sz * z) for x, z in ((7.6, 11.0), (11.0, 7.6)) for y in (8.0, 24.0)], 'black', bevel=0.0)
            b.box((sx * 17.6 - 0.6, 6.0, sz * 17.6 - 0.6), (sx * 17.6 + 0.6, 7.4, sz * 17.6 + 0.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ vents: four louvre blocks on the diagonals
    v = k.piece('vents')
    for sx in (-1, 1):
        for sz in (-1, 1):
            q = [(sx * x, sz * z) for x, z in ((7.4, 10.6), (10.6, 7.4), (13.4, 10.2), (10.2, 13.4))]
            v.hull([(x, y, z) for x, z in q for y in (9.0, 25.4)], 'dark', bevel=0.15)
            for y in (13.0, 17.0, 21.0, 25.2):
                v.hull([(x * 1.04, yy, z * 1.04) for x, z in q for yy in (y, y + 1.0)], 'steel', bevel=0.05)

    # ------------------------------------------------------------------ fliptop: the nuke lid (origin 4.82, 36.25, 0)
    f = k.piece('fliptop'); F = f.at
    f.hull([F(-4.82 + x, y, z) for x, z in octagon(6.6) for y in (0.05, 1.0)], 'hazard', bevel=0.1)
    f.cyl(F(0.4, 0.4, -3.4), F(0.4, 0.4, 3.4), 0.9, 8, 'dark', bevel=0.04)

    # ------------------------------------------------------------------ riser: the missile (origin 0, 18.75, 0)
    r = k.piece('riser'); R = r.at
    r.cyl(R(0, -17.4, 0), R(0, 9.0, 0), 4.2, 12, 'steel', bevel=0.06)
    r.cyl(R(0, 9.0, 0), R(0, 17.2, 0), 4.2, 12, 'paint', r2=0.8, bevel=0.06)
    r.cyl(R(0, 6.4, 0), R(0, 9.0, 0), 4.3, 12, 'hazard')
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        r.hull([R(math.cos(a) * rr, y, math.sin(a) * rr) for rr in (3.0, 7.0) for y in (-17.4, -10.0)] +
               [R(math.cos(a) * 3.0, -4.0, math.sin(a) * 3.0)], 'dark', bevel=0.05)
