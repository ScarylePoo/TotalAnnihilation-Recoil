"""Moho Metal Maker (CORE_T2_ECO_MohoMetalMaker) - Core moho maker. A dark stepped square converter block with team
corner blocks and a central octagonal cap; four thick radial blades lie over the cap like roof ribs (closed). Switched
on, the cap sinks, flips over and returns with its glowing underside (an orange crystal cluster in a team ring) on
top, and the four blades swing up to stand at the edge centres like a crown.
Identity from above (on): dark square, four team corners, four light steel blade stubs at the edge centres and a
bright warm core in a team ring (the Arm moho maker is a light block with two flat lids and a cyan crown).
Pieces (COB): groundplane (empty root), base, flap1 (+z) / flap4 (-z) turn x, flap2 (+x) / flap3 (-x) turn z,
topcap (origin 0, 36.07, 0; on = move y -1.75, turn y 45, flipped 180 on z), glowingthing (child of topcap, under it
at rest). Preview: ON (activatescr end state; COB z turns negated).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=30, drop=['flap2'], pose={'flap1': (40, 0, 0)}),
    preview_pose={'flap1': (89.39, 0, 0), 'flap4': (-86.35, 0, 0), 'flap2': (-4.86, 0, -69.32), 'flap3': (0, 0, 69.32),
                  'topcap': {'move': (0, -1.75, 0), 'rot': (0, 45, 180)}},
)

TY = 36.07
BLADE = [(0.0, -4.0), (3.0, -4.8), (21.0, 11.6), (19.6, 15.2), (0.0, 3.0)]   # (inward distance, height) at rest


def blade(k, name, axis, side):
    """axis 'z': blade in the y-z plane on the +-z edge; 'x': in the x-y plane on the +-x edge. side = +-1."""
    p = k.piece(name); O = k.P[name]

    def P(r, h, w):
        if axis == 'z':
            return (O[0] + w, O[1] + h, O[2] - side * r)
        return (O[0] - side * r, O[1] + h, O[2] + w)
    p.hull([P(r, h, w) for r, h in BLADE for w in (-2.8, 2.8)], 'steel', bevel=0.3)
    # team tip (faces up once the blade stands) and dark ribs on the flanks
    p.hull([P(r, h, w) for r, h in ((18.0, 9.4), (21.2, 11.8), (19.8, 15.4), (17.0, 14.6)) for w in (-2.95, 2.95)],
           'team', bevel=0.0)
    for r0 in (6.0, 11.0):
        p.hull([P(r, h, w) for r, h in ((r0, -1.0 + r0 * 0.75), (r0 + 1.4, -1.0 + (r0 + 1.4) * 0.75),
                                         (r0 + 1.4, 4.0 + (r0 + 1.4) * 0.6), (r0, 4.0 + r0 * 0.6)) for w in (-2.95, 2.95)],
               'dark', bevel=0.0)
    p.hull([P(r, h, w) for r, h in ((-0.6, -5.4), (3.0, -5.4), (3.0, 3.6), (-0.6, 3.6)) for w in (-3.6, 3.6)], 'dark',
           bevel=0.15)


def build(k):
    b = k.piece('base')
    sq = lambda h: [(-h, -h), (h, -h), (h, h), (-h, h)]
    b.plan(0.0, 4.0, sq(32.0), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(3.9, 20.0, sq(30.0), 'paint', bevel=0.4, top_inset=3.0)
    b.plan(19.9, 30.0, sq(26.4), 'paint', bevel=0.35, top_inset=2.0)
    b.plan(29.9, 31.0, sq(24.0), 'paint2', bevel=0.15, top_inset=0.5)
    # corner team blocks on the lower step
    for sx in (-1, 1):
        for sz in (-1, 1):
            lo = (min(sx * 20.0, sx * 28.4), 19.9, min(sz * 20.0, sz * 28.4))
            hi = (max(sx * 20.0, sx * 28.4), 23.4, max(sz * 20.0, sz * 28.4))
            b.box(lo, hi, 'paint2', bevel=0.25)
            b.box((lo[0] + 0.6, 23.3, lo[2] + 0.6), (hi[0] - 0.6, 23.65, hi[2] - 0.6), 'team', bevel=0.0)
    # team corner squares on the top deck (the lower-step corner blocks hide under the upper step from above)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.box((min(sx * 14.6, sx * 23.2), 30.95, min(sz * 14.6, sz * 23.2)),
                  (max(sx * 14.6, sx * 23.2), 31.3, max(sz * 14.6, sz * 23.2)), 'team', bevel=0.0)
    # cap well ring and black slots for the blades
    b.cyl((0, 30.9, 0), (0, 31.4, 0), 15.4, 8, 'dark', rot=math.pi / 8)
    for (ox, oz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        x0, x1 = (min(ox * 15.0, ox * 24.0), max(ox * 15.0, ox * 24.0)) if ox else (-3.2, 3.2)
        z0, z1 = (min(oz * 15.0, oz * 24.0), max(oz * 15.0, oz * 24.0)) if oz else (-3.2, 3.2)
        b.box((x0, 30.95, z0), (x1, 31.2, z1), 'black', bevel=0.0)
    # vents on the sides
    for (ox, oz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for y0 in (7.0, 12.0):
            h = lambda y: 30.0 - (y - 3.9) / 16.1 * 3.0 / math.sqrt(2)
            b.hull([(ox * (h(y) + dd) + oz * v, y, oz * (h(y) + dd) + ox * v) for y in (y0, y0 + 2.4)
                    for v in (-12.0, 12.0) for dd in (0.05, 0.35)], 'black', bevel=0.0)
    b.box((-1.2, 1.0, 31.9), (1.2, 2.6, 32.2), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ blades
    blade(k, 'flap1', 'z', 1)
    blade(k, 'flap4', 'z', -1)
    blade(k, 'flap2', 'x', 1)
    blade(k, 'flap3', 'x', -1)

    # ------------------------------------------------------------------ topcap: dome on top, glowing cradle beneath
    t = k.piece('topcap')
    oc = lambda r: [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4))
                    for i in range(8)]
    t.plan(TY - 1.2, TY + 1.2, oc(13.9), 'paint2', bevel=0.25, top_inset=0.4)
    t.hull([(x, TY + 1.1, z) for x, z in oc(12.6)] + [(x, TY + 5.6, z) for x, z in oc(6.0)] + [(0, TY + 6.8, 0)],
           'paint', bevel=0.2)
    # underside (on top once flipped): team ring, dark cradle round the crystals
    t.plan(TY - 1.55, TY - 1.15, [(x, z) for x, z in oc(13.2)], 'team', bevel=0.0)
    t.hull([(x, TY - 1.5, z) for x, z in oc(9.6)] + [(x, TY - 5.4, z) for x, z in oc(8.0)], 'dark', bevel=0.15)

    # ------------------------------------------------------------------ glowingthing: crystal cluster (below the cap)
    g = k.piece('glowingthing')
    for (cx, cz, h, r) in ((0.0, 0.0, 14.0, 3.4), (4.4, 2.4, 9.0, 2.0), (-4.0, 3.0, 10.0, 2.2), (0.4, -4.8, 8.6, 2.0)):
        y0 = TY - 5.0
        g.hull([(cx + r * math.cos(i * math.pi / 3), y0 - h * 0.55, cz + r * math.sin(i * math.pi / 3)) for i in range(6)]
               + [(cx, y0, cz), (cx, y0 - h, cz)], 'lightc', bevel=0.0)
