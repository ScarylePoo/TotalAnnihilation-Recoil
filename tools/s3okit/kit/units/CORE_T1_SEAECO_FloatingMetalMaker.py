"""Floating Metal Maker (CORE_T1_SEAECO_FloatingMetalMaker) - Core sea metal maker. Waterline 33 (the water surface is
model y = 33; the TA model's top lay 1.4 under it). A dark octagonal rim deck riding 2.5 elmo above the water on four
diagonal struts round a sunken well; in the well a four-blade iris (door1..4) over the glowing orange converter crystal
(glow) on a dark core column; six dark ballast floats hang round the column (they push out 5 elmo when working). A light
steel arch spans the well diagonally - the land Core maker's arch over its crystal.
Switched on, the iris blades turn 90 deg on their radial axes and stand up as four dark blades round the glow.
Identity from above (on): a dark octagon with four team corner segments, a light steel arch across it and an orange
glow cut into four by dark blades (the Arm sea maker is a light three-armed star with a cyan dome).
Pieces (COB): base (move y: 0 on, -12.5 off), float1..6 (move x/z out 5 on; identical drums: clones), glow (crystal),
door1/door2 (turn x), door3/door4 (turn z) - iris blades; door2 = door1 mirrored (clone).
Preview: ON (floats out, iris open).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 33.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    flipped=['door1', 'door2', 'door3', 'door4'],
    wreck=dict(seed=181, drop=['door2']),
    preview_pose={'float1': {'move': (0, 0, -5.375)}, 'float2': {'move': (4.5, 0, -2.625)},
                  'float3': {'move': (4.375, 0, 2.5)}, 'float4': {'move': (0, 0, 5.375)},
                  'float5': {'move': (-4.625, 0, 2.75)}, 'float6': {'move': (-4.625, 0, -2.625)},
                  'door1': (-90, 0, 0), 'door2': (90, 0, 0), 'door3': (0, 0, -90), 'door4': (0, 0, 90)},
)

DY = 31.62
RI, RO = 14.6, 22.0       # rim inner / outer radius


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    # rim deck: eight segments (team on the four diagonal ones)
    O, I = octagon(RO, 0.0), octagon(RI, 0.0)
    for i in range(8):
        j = (i + 1) % 8
        b.hull([(x, y, z) for (x, z) in (O[i], O[j]) for y in (26.0, 35.5)]
               + [(x, y, z) for (x, z) in (I[i], I[j]) for y in (28.0, 35.5)], 'paint', bevel=0.3)
        if i % 2 == 0:
            q = [(O[i][0] * 0.9 + I[i][0] * 0.1, O[i][1] * 0.9 + I[i][1] * 0.1),
                 (O[j][0] * 0.9 + I[j][0] * 0.1, O[j][1] * 0.9 + I[j][1] * 0.1),
                 (O[i][0] * 0.2 + I[i][0] * 0.8, O[i][1] * 0.2 + I[i][1] * 0.8),
                 (O[j][0] * 0.2 + I[j][0] * 0.8, O[j][1] * 0.2 + I[j][1] * 0.8)]
            b.hull([(x, y, z) for x, z in q for y in (35.45, 35.7)], 'team', bevel=0.0)
    for i in range(8):            # waterline band (segments: a hull of the whole ring would cap the well)
        p, q = O[i], O[(i + 1) % 8]
        b.hull([(x * s, y, z * s) for (x, z) in (p, q) for s in (0.97, 1.025) for y in (32.2, 33.8)], 'dark',
               bevel=0.0)
    for a in (22.5, 112.5, 202.5, 292.5):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        b.box((c * (RO + 0.4) - 0.8, 30.0, s * (RO + 0.4) - 0.8), (c * (RO + 0.4) + 0.8, 31.0, s * (RO + 0.4) + 0.8),
              'lightc', bevel=0.0)
    # well floor ring under the iris, core column, diagonal struts
    b.cyl((0, 2.0, 0), (0, 26.2, 0), 6.4, 8, 'paint2', r2=5.6, rot=math.pi / 8, bevel=0.2)
    b.cyl((0, 0.0, 0), (0, 2.2, 0), 4.0, 8, 'dark', r2=6.4, rot=math.pi / 8)
    for sz in (-1, 1):
        b.hull([(x, y, x * sz + w * sz) for x in (3.0, 12.6) for y in (25.4, 28.6) for w in (-1.4, 1.4)], 'dark',
               bevel=0.15, mirror=True)
        b.hull([(x, y, x * sz + w * sz) for x in (2.0, 14.0) for y in (3.0, 5.0) for w in (-1.2, 1.2)], 'dark',
               bevel=0.1, mirror=True)
    # light steel arch over the well, on the diagonal (x = -z)
    arch = [(13.8, 36.8), (11.0, 42.0), (7.0, 45.0), (2.5, 46.2)]
    for sg in (1, -1):        # the arch crosses x = 0: both halves built (no mirror)
        b.hull([(sg * x + w, y, -sg * x + w) for x in (12.0, 15.6) for y in (35.4, 37.0) for w in (-1.0, 1.0)],
               'steel', bevel=0.15)
        for (r0, y0), (r1, y1) in zip(arch, arch[1:]):
            b.hull([(sg * r + w, y + dy, -sg * r + w) for r, y in ((r0, y0), (r1, y1)) for dy in (-1.2, 1.2)
                    for w in (-0.9, 0.9)], 'steel', bevel=0.12)
    b.hull([(x, y, -x + w) for x in (-2.6, 2.6) for y in (45.0, 47.4) for w in (-1.3, 1.3)], 'steel', bevel=0.12)
    b.box((-0.8, 47.3, -0.8), (0.8, 47.7, 0.8), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- glow: converter crystal
    g = k.piece('glow')
    g.hull([(x, 27.8, z) for x, z in octagon(4.2)] + [(0, 25.6, 0), (0, 31.0, 0)], 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- floats: ballast drums (identical)
    f = k.piece('float1'); F = f.at
    f.cyl(F(0, -4.4, 0), F(0, 5.6, 0), 3.4, 8, 'paint', rot=math.pi / 8, bevel=0.25)
    f.cyl(F(0, 0.4, 0), F(0, 1.4, 0), 3.6, 8, 'dark', rot=math.pi / 8)
    for n in ('float2', 'float3', 'float4', 'float5', 'float6'):
        k.clone(n, 'float1')

    # ---------------------------------------------------------------- iris blades
    def blade(name, axis):
        d = k.piece(name); D = d.at
        if axis == 'x':     # door1: hinge at x = -9.75, blade covers the -x quadrant triangle
            tri = [(0.0, -9.6), (0.0, 9.6), (9.6, 0.0)]
            pts = [D(u, y, w) for u, w in tri for y in (-0.6, 0.6)]
        else:               # door3: hinge at z = -9.75, blade covers the -z quadrant triangle
            tri = [(0.0, -9.6), (0.0, 9.6), (9.6, 0.0)]
            pts = [D(w, y, u) for u, w in tri for y in (-0.6, 0.6)]
        d.hull(pts, 'paint2', bevel=0.12)
    blade('door1', 'x')
    k.clone('door2', 'door1', mirror_x=True)
    blade('door3', 'z')
    d4 = k.piece('door4'); D4 = d4.at            # +z side: mirrored in z, built (clones only mirror x)
    d4.hull([D4(w, y, -u) for u, w in [(0.0, -9.6), (0.0, 9.6), (9.6, 0.0)] for y in (-0.6, 0.6)], 'paint2',
            bevel=0.12)
