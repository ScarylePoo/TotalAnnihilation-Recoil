"""Advanced Kbot Lab (CORE_T2_LAB_AdvancedKbotLab) - Core T2 kbot factory. Two massive dark towers (maina/mainb,
57.5 tall, team roofs, red beacons) stand side by side at the back of the lane with a staircase of ochre-edged steps
(stepa1..3 on the left half, stepb1..3 on the right) descending from them toward the pad. On activation the towers
slide 24.4 apart (move x), the steps sink (move y) and the nano guns (guna/gunb) swing forward and down out of slots
in the tower fronts to aim at the pad, which sits on a fixed track (fork) between two glowing gate posts (glow).
Core lab family (T2 = taller, more parts): dark warm armour, team caps, near-black lane with ochre hazard edges, light
steel pad, warm lights. Identity from above (open): two big dark team-roofed blocks either side of the lane's back
end, ochre stair edges in front of them, a light disc on a track (the T1 kbot lab is two low split blocks).
Pieces (COB): base, maina/mainb (move x), stepa1..3/stepb1..3 (move y; stepa1 fixed), guna/gunb (turn x), beama/beamb
(empty nano emit points), blinka/blinkb (beacons), fork + glow (static track and gate lights), pad (spin y;
QueryBuildInfo).
Preview: OPEN (activatescr end state; COB x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['guna', 'gunb'],
    wreck=dict(seed=74, drop=['stepb3']),
    preview_pose={
        'maina': {'move': (-24.375, 0, 0)}, 'mainb': {'move': (24.375, 0, 0)},
        'stepa2': {'move': (0, -5.625, 0)}, 'stepa3': {'move': (0, -11.25, 0)},
        'stepb1': {'move': (0, -5.75, 0)}, 'stepb2': {'move': (0, -11.5, 0)}, 'stepb3': {'move': (0, -17.0, 0)},
        'guna': (121.62, 0, 0), 'gunb': (121.01, 0, 0),
    },
)

MY = 57.5            # tower height
Z0, Z1 = -37.5, -11.3  # tower depth (a slot x -13.5..-4.4, y 33..55 runs through it: gun + hanger)


def step(k, name, x0, x1, y0, y1, depth):
    s = k.piece(name)
    s.box((x0, y0, -11.25), (x1, y1, -11.25 + depth), 'paint', bevel=0.3)
    xa, xb = (x0 + 0.6, x1 - 0.6)
    s.box((xa, y1 - 0.05, -11.25 + depth - 2.4), (xb, y1 + 0.35, -11.25 + depth - 0.4), 'hazard', bevel=0.04)


def build(k):
    # ------------------------------------------------------------------ base: lane, rails, back wall, front pylons
    b = k.piece('base')
    b.box((-40.0, 0.0, -14.0), (40.0, 0.3, 32.0), 'paint2', bevel=0.05)
    b.box((-24.0, 0.0, 32.0), (24.0, 0.3, 48.0), 'paint2', bevel=0.05)
    b.box((-40.0, 0.0, -14.0), (-36.4, 0.45, 32.0), 'hazard', bevel=0.04, mirror=True)
    b.box((-24.0, 0.0, 32.0), (-20.4, 0.45, 48.0), 'hazard', bevel=0.04, mirror=True)
    b.box((-55.0, 0.0, -39.0), (55.0, 0.4, -14.0), 'dark', bevel=0.05)                         # slide bed
    for z in (-33.0, -16.0):
        b.box((-54.0, 0.3, z - 1.0), (54.0, 0.9, z + 1.0), 'steel', bevel=0.1)
    b.plan(0.0, 14.0, [(-56.0, -48.0), (56.0, -48.0), (56.0, -39.4), (-56.0, -39.4)], 'paint', bevel=0.35,
           top_inset=1.4)
    b.box((-52.0, 13.9, -46.0), (52.0, 14.4, -42.0), 'team', bevel=0.08)
    b.box((-40.0, 5.0, -39.5), (40.0, 6.2, -39.2), 'lightw', bevel=0.0)
    for sx in (-1, 1):                                                         # front corner pylons
        x0, x1 = sorted((sx * 27.0, sx * 50.0))
        b.plan(0.0, 10.0, [(x0, 34.0), (x1, 34.0), (x1, 48.0), (x0, 48.0)], 'paint', bevel=0.3, top_inset=1.6)
        xc = sx * 40.0
        b.hull([(x, 9.5, z) for x in (xc - 6.0, xc + 6.0) for z in (36.5, 45.5)]
               + [(x, 22.0, z) for x in (xc - 3.5, xc + 3.5) for z in (39.0, 43.0)], 'paint', bevel=0.3)
        b.box((xc - 3.3, 21.9, 39.2), (xc + 3.3, 22.5, 42.8), 'team', bevel=0.06)

    # gun hangers: masts behind the towers, arms through the tower slots to the gun pivots (the guns are children of
    # base and stay over the lane when the towers part)
    b.box((-7.4, 13.9, -45.0), (-3.6, 46.0, -41.0), 'paint2', bevel=0.3, mirror=True)
    b.box((-7.2, 41.6, -44.0), (-4.8, 44.6, -23.5), 'dark', bevel=0.2, mirror=True)
    b.box((-7.0, 44.5, -43.0), (-5.0, 44.9, -25.0), 'hazard', bevel=0.04, mirror=True)

    # ------------------------------------------------------------------ towers (maina origin -12.5, 0, -22.5)
    m = k.piece('maina')
    m.box((-25.0, 0.0, Z0), (-13.5, MY, Z1), 'paint', bevel=0.45)
    m.box((-4.4, 0.0, Z0), (0.0, MY, Z1), 'paint', bevel=0.35)
    m.box((-13.5, 0.0, Z0), (-4.4, 33.0, Z1), 'paint', bevel=0.3)                             # under the slot
    m.box((-13.5, 55.0, Z0), (-4.4, MY, Z1), 'paint', bevel=0.3)                              # over the slot
    m.box((-13.4, 33.0, Z0 + 0.5), (-4.5, 33.4, Z1 - 0.5), 'black', bevel=0.0)                # slot floor
    m.box((-24.0, MY - 0.05, Z0 + 1.0), (-1.0, MY + 0.45, Z1 - 1.0), 'team', bevel=0.12)       # roof
    m.box((-24.0, 6.0, Z1 - 0.1), (-15.0, 30.0, Z1 + 0.3), 'paint2', bevel=0.1)                # front armour
    m.box((-22.0, 36.0, Z1 - 0.1), (-16.0, 38.0, Z1 + 0.25), 'lightw', bevel=0.0)
    m.box((-25.4, 10.0, Z0 + 4.0), (-24.8, 46.0, Z1 - 4.0), 'paint2', bevel=0.1)               # outer flank rib
    m.box((-13.9, 30.0, Z1 - 0.2), (-4.0, 33.2, Z1 + 0.3), 'hazard', bevel=0.05)               # slot sill
    k.clone('mainb', 'maina', mirror_x=True)
    bl = k.piece('blinka')
    bl.cyl((-6.25, MY, -20.0), (-6.25, 62.0, -20.0), 0.8, 8, 'steel')
    bl.box((-7.6, 61.6, -21.4), (-4.9, 64.4, -18.6), 'lightr', bevel=0.15)
    k.clone('blinkb', 'blinka', mirror_x=True)
    # nano guns (guna origin -5.5, 40, -23.5), upright at rest, beama at (-0.75, 13.97, 0)
    g = k.piece('guna'); G = g.at
    g.cyl(G(-6.2, 0, 0), G(0.4, 0, 0), 3.0, 10, 'dark', rot=math.pi / 10)
    g.box(G(-5.6, -2.8, -3.2), G(0.0, 6.0, 3.2), 'steel', bevel=0.35)
    g.cyl(G(-0.75, 5.8, 0), G(-0.75, 12.6, 0), 1.6, 10, 'dark', r2=1.15)
    g.cyl(G(-0.75, 12.5, 0), G(-0.75, 13.97, 0), 1.2, 10, 'lightc')
    g.box(G(-5.2, 0.0, 3.1), G(-0.4, 5.6, 3.5), 'hazard', bevel=0.03)
    k.clone('gunb', 'guna', mirror_x=True)

    # ------------------------------------------------------------------ steps (origin 0, 2.5, -11.25)
    step(k, 'stepa1', -20.0, -0.1, 0.0, 5.8, 13.8)
    step(k, 'stepa2', -15.0, -0.1, 2.5, 17.5, 10.0)
    step(k, 'stepa3', -10.0, -0.1, 2.5, 29.2, 6.5)
    step(k, 'stepb1', 0.1, 20.0, 2.5, 11.7, 13.8)
    step(k, 'stepb2', 0.1, 15.0, 2.5, 23.3, 10.0)
    step(k, 'stepb3', 0.1, 10.0, 2.5, 35.0, 6.5)

    # ------------------------------------------------------------------ track, gate lights, pad
    f = k.piece('fork')
    f.box((-10.0, 0.25, -6.0), (10.0, 0.42, 40.0), 'dark', bevel=0.04)
    for x in (-11.5, 11.5):
        f.box((x - 1.0, 0.25, -6.0), (x + 1.0, 0.75, 41.0), 'steel', bevel=0.1)
    gl = k.piece('glow')
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 17.0, sx * 20.0))
        gl.box((x0, 0.3, 38.0), (x1, 7.6, 42.0), 'paint2', bevel=0.2)
        gl.box((x0 + 0.3, 7.5, 38.3), (x1 - 0.3, 8.9, 41.7), 'lightw', bevel=0.1)
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, -0.2, 0), Pp(0, 0.3, 0), 14.2, 32, 'dark', bevel=0.1)
    p.cyl(Pp(0, 0.3, 0), Pp(0, 0.42, 0), 12.6, 32, 'steel')
    for a in range(4):
        t = math.radians(a * 90 + 45)
        p.hull([Pp(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r in (12.7, 14.0) for dt in (-0.22, 0.22)
                for yy in (0.25, 0.4)], 'hazard', bevel=0.0)
