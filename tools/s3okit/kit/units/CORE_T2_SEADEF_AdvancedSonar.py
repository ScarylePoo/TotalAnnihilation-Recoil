"""Advanced Sonar Station (CORE_T2_SEADEF_AdvancedSonar) - Core T2 sonar. Waterline 0 (the water surface is model
y = 0). A dark trefoil of three hexagonal float pods (6 elmo freeboard) round a hub with a short steel mast; under the
hub a stalk carries the Sonar: a huge light steel hexagonal plate with a team rim and dark radial ribs, lying flat
8 elmo under the water (raised up its spin axis from the TA depth) and slowly turning - the land Core radar's big hexagonal dish, laid down in the sea.
Identity from above: a big light hexagon with a team rim under the water, three dark hex pods with team caps and warm lights over
it (the Arm T2 sonar is a light cross of petals with four float drums).
Pieces (COB): base, sonar (spin y; origin 0.01, -14.21, 3.38).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 0.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=201, drop=['Sonar']),
    preview_pose={'Sonar': (0, 15, 0)},
)

CZ = 3.38
LIFT = 5.6


def hexagon(r, cx=0.0, cz=0.0, rot=0.0):
    return [(cx + r * math.cos(rot + i * math.pi / 3), cz + r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def build(k):
    b = k.piece('Base')
    # hub, mast, stalk
    b.plan(-6.0, 6.0, hexagon(7.4, 0.0, CZ, math.pi / 6), 'paint', bevel=0.3, top_inset=1.2)
    b.cyl((0, 5.8, CZ), (0, 13.0, CZ), 1.4, 8, 'steel')
    b.cyl((0, 9.0, CZ), (0, 9.8, CZ), 3.6, 8, 'steel')
    b.cyl((0, 12.9, CZ), (0, 14.0, CZ), 1.8, 8, 'lightc')
    b.cyl((0, -8.0, CZ), (0, -5.8, CZ), 2.6, 8, 'paint2', r2=4.4, rot=math.pi / 8)
    # three pods and their arms (front pod whole, back pair mirrored)
    def pod(ang, mirror):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        px, pz = c * 15.0, CZ + s * 15.0
        b.hull([(c * r - s * w, y, CZ + s * r + c * w) for r in (5.0, 10.0) for w in (-2.6, 2.6) for y in (-1.0, 4.0)],
               'paint2', bevel=0.2, mirror=mirror)
        b.hull([(x, -7.0, z) for x, z in hexagon(6.4, px, pz)] + [(x, 2.0, z) for x, z in hexagon(8.4, px, pz)]
               + [(x, 6.6, z) for x, z in hexagon(7.4, px, pz)], 'paint', bevel=0.35, mirror=mirror)
        b.hull([(x, y, z) for x, z in hexagon(8.65, px, pz) for y in (-0.6, 0.8)], 'dark', bevel=0.0, mirror=mirror)
        b.plan(6.5, 7.1, hexagon(4.6, px, pz), 'team', bevel=0.1, mirror=mirror)
        b.box((px - 0.9, 7.0, pz - 0.9), (px + 0.9, 7.6, pz + 0.9), 'lightc', bevel=0.0, mirror=mirror)
    pod(90, False)
    pod(330, True)

    # ---------------------------------------------------------------- sonar: the big hex plate (spins)
    so = k.piece('Sonar'); S0 = so.at
    S = lambda x, y, z: S0(x, y + LIFT, z)      # the plate rides LIFT up its spin axis, closer to the surface
    so.hull([S(x, y, z) for x, z in hexagon(18.4) for y in (-2.4, -0.6)] + [S(x, -3.6, z) for x, z in hexagon(14.0)],
            'steel', bevel=0.3)
    ring = hexagon(18.0); inner = hexagon(15.0)
    for i in range(6):
        j = (i + 1) % 6
        so.hull([S(x, y, z) for x, z in (ring[i], ring[j], inner[i], inner[j]) for y in (-0.65, -0.4)], 'team',
                bevel=0.0)
    for i in range(6):
        a = i * math.pi / 3 + math.pi / 6
        c, s = math.cos(a), math.sin(a)
        so.hull([S(c * r - s * w, y, s * r + c * w) for r in (4.0, 14.2) for w in (-0.8, 0.8) for y in (-0.7, 0.4)],
                'dark', bevel=0.05)
    so.cyl(S(0, -0.7, 0), S(0, 1.0, 0), 4.6, 6, 'dark', bevel=0.1)
