"""Advanced Sonar Station (ARM_T2_SEADEF_AdvancedSonar) - Arm T2 sonar. Waterline 34 (the water surface is model
y = 34). A tall light column on a four-legged sea-bed anchor; four light float drums on diagonal arms hold its top
4 elmo above the water, with the beacon (light) on the column head. Round the column, on a spinning collar (wheel) at
y 22.5, four tall hydrophone petals (dish1..4 on hinge1..4): closed they stand up round the column like a bud, open
(activated) they fold out and down under the water like a flower, while the whole station rises 10 elmo.
The float arms sit on the diagonals, so the petals (on the axes) swing between them without clipping.
Identity from above (open): a light cross of four broad petals with team centre stripes seen under the water, four
light drums on the diagonals, a cyan beacon in the middle (the T1 Arm sonar is a single float disc with a paddle rotor).
Pieces (Lua script): base (move y: -10 off, 0 on), light, wheel (spin y), hinge1/2 (turn x), hinge3/4 (turn z),
dish1..4 (turn y 180 on). Petals are symmetric front/back: dish2 = dish1, dish4 = dish3 (clones, shared UVs).
Preview: OPEN (hinges +-120.3 deg, dishes 180 deg, base at 0).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 34.0
A = 120.32       # 2.1 rad
UNIT = dict(
    res=1024,                  # 4x4, but 1024 like the land T1 defences (shared 2-core machine: 4096 bakes too slow)
    ground=False, water=WL,
    always_visible=['dish1', 'dish2', 'dish3', 'dish4'],
    wreck=dict(seed=121, drop=['dish3']),
    preview_pose={'hinge1': (A, 0, 0), 'hinge2': (-A, 0, 0), 'hinge3': (0, 0, -A), 'hinge4': (0, 0, A),
                  'dish1': (0, 180, 0), 'dish2': (0, 180, 0), 'dish3': (0, 180, 0), 'dish4': (0, 180, 0)},
)

PW, PT, PL = 6.0, 1.1, 28.5      # petal half width, half thickness, length


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    # anchor: four legs on the diagonals (deep: plain)
    for sz in (-1, 1):
        b.hull([(x, y, x * sz) for x, y in ((3.0, 16.0), (4.6, 16.0), (19.0, 0.0), (22.0, 0.0))]
               + [(x + 1.6, y, x * sz - 1.6 * sz) for x, y in ((3.0, 16.0), (19.0, 0.0))]
               + [(x - 1.6, y, x * sz + 1.6 * sz) for x, y in ((4.6, 16.0), (22.0, 0.0))], 'paint2', bevel=0.15,
               mirror=True)
        b.cyl((20.5, 0.0, 20.5 * sz), (20.5, 2.0, 20.5 * sz), 4.0, 8, 'dark', mirror=True)
    b.cyl((0, 0.0, 0), (0, 54.0, 0), 5.0, 8, 'paint2', r2=4.2, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 14.0, 0), (0, 20.4, 0), 7.0, 8, 'dark', r2=6.0, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 26.4, 0), (0, 28.0, 0), 5.6, 8, 'dark', rot=math.pi / 8)
    b.cyl((0, 44.0, 0), (0, 54.0, 0), 5.6, 8, 'paint', r2=4.6, rot=math.pi / 8, bevel=0.25)
    b.cyl((0, 53.8, 0), (0, 54.3, 0), 3.4, 8, 'dark', rot=math.pi / 8)
    # diagonal arms and float drums (team tops)
    for sz in (-1, 1):
        b.hull([(x, y, x * sz + w * sz) for x in (3.4, 15.0) for y in (33.0, 35.6) for w in (-1.0, 1.0)],
               'dark', bevel=0.12, mirror=True)
        c = 15.6
        b.cyl((c, 28.0, c * sz), (c, 38.6, c * sz), 5.8, 16, 'paint', rot=math.pi / 16, bevel=0.3, mirror=True)
        b.cyl((c, 38.5, c * sz), (c, 38.9, c * sz), 3.8, 16, 'team', rot=math.pi / 16, mirror=True)
        b.cyl((c, 33.4, c * sz), (c, 34.6, c * sz), 6.05, 16, 'dark', rot=math.pi / 16, mirror=True)
        b.cyl((c, 24.6, c * sz), (c, 28.1, c * sz), 3.0, 8, 'paint2', r2=5.4, rot=math.pi / 8, mirror=True)

    # ---------------------------------------------------------------- light: beacon
    l = k.piece('light')
    l.cyl((0, 54.2, 0), (0, 55.6, 0), 1.8, 8, 'steel')
    l.cyl((0, 55.5, 0), (0, 57.0, 0), 2.1, 8, 'lightc')

    # ---------------------------------------------------------------- wheel: spinning collar (origin 0, 22.5, 0)
    w = k.piece('wheel')
    w.cyl((0, 20.6, 0), (0, 25.4, 0), 8.6, 8, 'paint', r2=7.6, rot=math.pi / 8, bevel=0.25)
    w.cyl((0, 25.3, 0), (0, 25.8, 0), 6.4, 8, 'dark', rot=math.pi / 8)

    # ---------------------------------------------------------------- hinges: knuckles on the collar rim
    def knuckle(name, along_x):
        h = k.piece(name); H = h.at
        if along_x:
            h.cyl(H(-2.6, 0.2, 0), H(2.6, 0.2, 0), 1.3, 8, 'dark')
        else:
            h.cyl(H(0, 0.2, -2.6), H(0, 0.2, 2.6), 1.3, 8, 'dark')
    knuckle('hinge1', True)
    k.clone('hinge2', 'hinge1')
    knuckle('hinge3', False)
    k.clone('hinge4', 'hinge3')

    # ---------------------------------------------------------------- dishes: hydrophone petals (symmetric)
    def petal(name, along_x):
        d = k.piece(name); D = d.at
        P = (lambda u, y, t: D(u, y, t)) if along_x else (lambda u, y, t: D(t, y, u))
        prof = [(-PW * 0.55, 0.4), (PW * 0.55, 0.4), (-PW, 6.0), (PW, 6.0), (-PW, PL - 6.0), (PW, PL - 6.0),
                (-PW * 0.45, PL), (PW * 0.45, PL)]
        d.hull([P(u, y, t) for u, y in prof for t in (-PT, PT)]
               + [P(u, y, t) for u, y in ((-PW * 0.7, 9.0), (PW * 0.7, 9.0), (-PW * 0.7, PL - 8.0),
                                          (PW * 0.7, PL - 8.0)) for t in (-PT - 0.7, PT + 0.7)], 'paint', bevel=0.2)
        for t in (-1, 1):
            d.hull([P(u, y, t * tt) for u in (-1.6, 1.6) for y in (8.0, PL - 6.0) for tt in (PT + 0.65, PT + 0.9)],
                   'team', bevel=0.0)
            for y in (4.0, PL - 3.5):
                d.hull([P(u, yy, t * tt) for u in (-PW * 0.5, PW * 0.5) for yy in (y, y + 1.2)
                        for tt in (PT - 0.1, PT + 0.15)], 'dark', bevel=0.0)
        d.box(D(-0.6, PL - 0.4, -0.6), D(0.6, PL + 0.4, 0.6), 'lightc', bevel=0.0)
    petal('dish1', True)
    k.clone('dish2', 'dish1')
    petal('dish3', False)
    k.clone('dish4', 'dish3')
