"""Moho Metal Maker (ARM_T2_ECO_MohoMetalMaker) - Arm moho maker. A square light converter block with four team-capped
corner pylons; on its roof two big armoured lids hinged on the centre line stand up in a V (closed). Switched on, the
lids fold out nearly flat (team stripes up), two inner baffles drop under them and the converter column rises
39.6 elmo out of the block, turning, its glowing cyan crystal crown high above the roof.
Identity from above (on): a light square with four team corners, two flat lids with team stripes and a bright cyan
crown in the middle (the T1 Arm maker is a six-spoke star; the Core moho maker is a dark block with four fins).
Pieces (COB): groundpoly (empty root), base2, lid1/lid4 (big lids +z/-z), lid2/lid3 (inner baffles +z/-z) all
hinged at (0, 29.82, 0) and turning on x, mmakercore (move y 39.625, turn y -90 when on), glowingthing (crystal,
child of mmakercore). Preview: ON (activatescr end state).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=29, drop=['lid4'], pose={'lid1': (20, 0, 0)}),
    preview_pose={'lid1': (35.27, 0, 0), 'lid4': (-30.40, 0, 0), 'lid2': (60.81, 0, 0), 'lid3': (-74.19, 0, 0),
                  'mmakercore': {'move': (0, 39.625, 0), 'rot': (0, -90, 0)}},
)

HY = 29.82
# rest elevations (deg above the outward horizontal) chosen so the scripted turns open the lids nearly flat
EL = {'lid1': 44.0, 'lid4': 43.4, 'lid2': 64.0, 'lid3': 64.0}


def lid(k, name, side, s0, s1, hw, big):
    p = k.piece(name)
    a = math.radians(EL[name])
    d = (0.0, math.sin(a), side * math.cos(a))          # hinge -> outward edge
    n = (0.0, math.cos(a), -side * math.sin(a))          # the face that is UP once opened

    def P(s, x, h):
        return (x, HY + d[1] * s + n[1] * h, d[2] * s + n[2] * h)
    pts = lambda sa, sb, xa, xb, ha, hb: [P(s, x, h) for s in (sa, sb) for x in (xa, xb) for h in (ha, hb)]
    if big:
        p.hull(pts(s0, s1, -hw, hw, 0.0, 0.9), 'paint', bevel=0.25)
        p.hull(pts(s0 + 1.0, s1 - 1.0, -3.2, 3.2, 0.88, 1.15), 'team', bevel=0.0)
        p.hull(pts(s0 + 2.0, s1 - 2.0, hw - 4.6, hw - 1.4, 0.85, 1.1), 'dark', bevel=0.0)
        p.hull(pts(s0 + 2.0, s1 - 2.0, -hw + 1.4, -hw + 4.6, 0.85, 1.1), 'dark', bevel=0.0)
        p.hull(pts(s0, s0 + 2.4, -hw + 2.0, hw - 2.0, -1.2, 0.2), 'paint2', bevel=0.12)      # hinge knuckle side
        p.hull(pts(s1 - 1.2, s1, -hw + 1.0, hw - 1.0, 0.85, 1.12), 'hazard', bevel=0.0)
    else:
        p.hull(pts(s0, s1, -hw, hw, 0.0, 0.7), 'paint2', bevel=0.2)
        p.hull(pts(s0 + 1.5, s1 - 1.5, -hw + 1.5, hw - 1.5, 0.68, 0.9), 'dark', bevel=0.0)
    # hinge arms back to the centre line
    for x in (-hw + 1.0, hw - 3.0):
        p.hull(pts(0.0, s0 + 1.0, x, x + 2.0, -0.4, 0.6), 'dark', bevel=0.08)


def build(k):
    b = k.piece('base2')
    sq = lambda h: [(-h, -h), (h, -h), (h, h), (-h, h)]
    b.plan(0.3, 4.0, sq(31.0), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(3.9, 27.6, sq(29.0), 'paint', bevel=0.4, top_inset=2.4)
    b.cyl((0, 27.5, 0), (0, 28.0, 0), 9.8, 8, 'black', rot=math.pi / 8)
    b.box((-22.0, 27.5, -1.4), (22.0, 28.2, 1.4), 'dark', bevel=0.05)              # hinge rail
    b.box((9.6, 27.5, -1.4), (18.0, 30.4, 1.4), 'dark', bevel=0.05, mirror=True)   # bearing blocks the lid arms turn on, clear of the column
    for sx in (-1, 1):
        for sz in (-1, 1):
            lo = (min(sx * 18.0, sx * 29.4), 3.9, min(sz * 18.0, sz * 29.4))
            hi = (max(sx * 18.0, sx * 29.4), 41.6, max(sz * 18.0, sz * 29.4))
            b.box(lo, hi, 'paint', bevel=0.35)
            b.box((lo[0] + 0.8, 41.5, lo[2] + 0.8), (hi[0] - 0.8, 41.9, hi[2] - 0.8), 'team', bevel=0.0)
    # dark vents on the four faces between the pylons
    for (ox, oz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        pts = []
        for y in (8.0, 20.0):
            h = 29.0 - (y - 3.9) / 23.7 * 2.4 / math.sqrt(2)
            for v in (-10.0, 10.0):
                for dd in (0.05, 0.35):
                    pts.append((ox * (h + dd) + oz * v, y, oz * (h + dd) + ox * v))
        b.hull(pts, 'dark', bevel=0.0)
    b.box((-1.2, 0.8, 30.9), (1.2, 2.4, 31.2), 'lightr', bevel=0.0)

    lid(k, 'lid1', 1, 9.5, 32.0, 17.6, True)
    lid(k, 'lid4', -1, 9.5, 32.0, 17.6, True)
    lid(k, 'lid2', 1, 9.6, 22.0, 13.0, False)
    lid(k, 'lid3', -1, 9.6, 22.0, 13.0, False)

    # ------------------------------------------------------------------ converter column (rises 39.6)
    c = k.piece('mmakercore')
    oc = lambda r: [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4))
                    for i in range(8)]
    c.plan(-13.5, 26.0, oc(8.4), 'paint', bevel=0.3, top_inset=0.6)     # long enough to stay in the roof when raised 39.6
    for y in (0.0, 8.0, 16.0):
        c.plan(y, y + 1.6, oc(8.6), 'dark', bevel=0.06, top_inset=0.1)
    c.plan(25.9, 29.0, oc(9.4), 'paint2', bevel=0.25, top_inset=1.6)
    c.box((-6.0, 28.9, -1.0), (6.0, 29.3, 1.0), 'team', bevel=0.0)
    for a in (0, 90, 180, 270):          # crown prongs
        ar = math.radians(a)
        c.hull([(math.cos(ar) * u - math.sin(ar) * v, y, math.sin(ar) * u + math.cos(ar) * v)
                for u, y in ((4.0, 28.8), (8.0, 28.8), (6.4, 38.0), (5.4, 38.0)) for v in (-1.2, 1.2)], 'steel',
               bevel=0.12)

    # ------------------------------------------------------------------ glowingthing: the crystal crown
    g = k.piece('glowingthing')
    ring = [(4.6 * math.cos(i * math.pi / 4), 34.0, 4.6 * math.sin(i * math.pi / 4)) for i in range(8)]
    g.hull(ring + [(0, 29.0, 0), (0, 43.0, 0)], 'lightc', bevel=0.0)
