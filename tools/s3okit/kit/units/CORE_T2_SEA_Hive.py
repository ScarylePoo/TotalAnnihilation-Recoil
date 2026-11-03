"""Hive (CORE_T2_SEA_Hive) - Core light carrier: no weapons (category NOWEAPON), isairbase, builder only to repair aircraft,
QueryLandingPad alternates pad1/pad2, radar 2400 from the spinning dish. The deck is its whole job.
The tell from above: two huge square flight decks staggered fore and aft, each overhanging a different side of the
hull (a skewed S outline no other ship has), each a big team target ring around an ochre striped landing pad, with
a thin control tower and boom between them. Nothing on it points anywhere: the opposite read of the Warlord.
Pieces (TA layout): base, stall1 (fore deck, overhangs -x), stall2 (aft deck, overhangs +x), pad1/pad2 (empty, landing
points at the deck centres, y 20.94), terminal (tower, static), dish (spin y), wake1/2 (empty).
Decks stay flat and clear: the top is exactly y 20.9 and the markings only 0.06-0.2 above it, because aircraft
land at the pad heights. stall1/2 are each other's mirror plus a z shift, which clone cannot express with their shared
origin: both have their own UVs. They are by far the most visible surfaces, so that is texture well spent.
Value groups from above: mid decks (paint), darker skirts, overhang slopes and tower (paint2), black hangar doors, team rings,
ochre hazard pads and bow chevrons, bright steel dish. Builder rule: the hazard surfaces are the pads themselves.
Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=2048,
    wreck=dict(seed=47, drop=['dish'], pose={'stall1': (4, 0, -7), 'stall2': (-3, 0, 5)}),
    preview_pose={'dish': (0, 25, 0)},
)

DECK = 11.1
TOPY = 20.9
WL = [(0.0, 65.8), (2.0, 65.5), (17.6, 55.0), (24.4, 41.1), (24.4, -53.4), (15.7, -64.8)]
TOP = [(0.0, 59.6), (0.5, 59.3), (13.1, 50.4), (18.9, 38.3), (18.9, -51.7), (12.1, -59.1)]


def half(pts, y, z0, z1, sx=1.0):
    """+x half of an outline (sorted bow to stern) clipped to z0 .. z1, with centre-line points: one hull section."""
    pts = sorted(pts, key=lambda p: p[1])
    def x_at(z):
        z = max(pts[0][1], min(pts[-1][1], z))
        for (xa, za), (xb, zb) in zip(pts, pts[1:]):
            if za <= z <= zb:
                return xa + (xb - xa) * (z - za) / ((zb - za) or 1.0)
    z0, z1 = max(z0, pts[0][1]), min(z1, pts[-1][1])
    q = [(x_at(z0), z0)] + [p for p in pts if z0 < p[1] < z1] + [(x_at(z1), z1)]
    return [(x * sx, y, z) for x, z in q] + [(0.0, y, z0), (0.0, y, z1)]


def stall(k, name, s, zc):
    """One flight deck. u = outboard axis (x = s * u), zc = deck centre z, half length 18.3, pad at u = 11."""
    b = k.piece(name)
    X = lambda u: s * u
    zz = (zc - 18.3, zc + 18.3)
    # body: inboard slope, flat top, outboard slope, undercut over the water
    prof = [(22.6, 4.0), (34.2, DECK), (29.6, 20.3), (-7.6, 20.3), (-18.9, DECK), (-18.9, DECK - 1.0)]
    b.hull([(X(u), y, z) for u, y in prof for z in zz], 'paint2', bevel=0.2)
    # flight deck slab, real top = TOPY
    b.hull([(X(u), y, z) for u, y in [(29.3, 20.2), (29.3, TOPY), (-7.3, TOPY), (-7.3, 20.2)] for z in (zc - 18.6, zc + 18.6)], 'paint', bevel=0.1)
    # target ring: 12 flat trapezoids (a convex hull of a ring would fill its hole)
    n, r0, r1 = 12, 11.2, 16.8
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        pts = []
        for a in (a0, a1):
            for r in (r0, r1):
                for y in (TOPY + 0.06, TOPY + 0.2):
                    pts.append((X(11.0 + r * math.cos(a)), y, zc + r * math.sin(a)))
        b.hull(pts, 'team', bevel=0.0)
    # the pad itself: ochre stripes, dark rim
    b.cyl((X(11.0), TOPY - 0.02, zc), (X(11.0), TOPY + 0.14, zc), 8.0, 16, 'dark', bevel=0.0)
    b.cyl((X(11.0), TOPY + 0.1, zc), (X(11.0), TOPY + 0.22, zc), 7.0, 16, 'hazard', bevel=0.0)
    # runway lights at the four corners and a light bar on the outboard slope
    for u in (-6.0, 28.0):
        for dz in (-17.3, 17.3):
            b.box((X(u) - 0.6, TOPY - 0.05, zc + dz - 0.6), (X(u) + 0.6, TOPY + 0.2, zc + dz + 0.6), 'lightw', bevel=0.0)
    y0, y1 = 13.6, 15.2
    u0, u1 = 32.95 + 0.14, 32.15 + 0.14
    b.hull([(X(u), y, z) for (u, y) in [(u0, y0), (u1, y1), (u0 + 0.1, y0), (u1 + 0.1, y1)] for z in (zc - 9.0, zc + 9.0)], 'lightc', bevel=0.0)
    # hangar door on the inboard slope (slope (-18.9, 11.1) -> (-7.6, 20.3)), black, with hazard jambs
    nu, ny = -0.631, 0.775
    def door(zr, mat, d0=0.06, d1=0.2):
        return [(X(-16.9 + 8.9 * f + nu * d), 12.73 + 7.25 * f + ny * d, zc + z) for f in (0.0, 1.0) for z in zr for d in (d0, d1)]
    b.hull(door((-6.9, 6.9), 'black'), 'black', bevel=0.0)
    b.hull(door((-10.6, -7.4), 'hazard'), 'hazard', bevel=0.0)
    b.hull(door((7.4, 10.6), 'hazard'), 'hazard', bevel=0.0)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0)
    # Mirrored halves in three z sections that only touch: one hull side would be a 95-elmo island, which the packer lays
    # diagonally (first draft: 52 % UV coverage), and the mid/aft deck under the stalls can now be culled on its own.
    for z0, z1 in ((-70.0, -15.1), (-15.1, 38.3), (38.3, 70.0)):
        b.hull(half(WL, -2.4, z0, z1, 0.65) + half(WL, 0.0, z0, z1), 'paint2', bevel=0.0, mirror=True)
        b.hull(half(WL, 0.0, z0, z1) + half(TOP, DECK - 0.6, z0, z1), 'paint2', bevel=0.0, mirror=True)
        b.hull(half(TOP, DECK - 0.6, z0, z1) + half(TOP, DECK, z0, z1, 0.985), 'paint', bevel=0.0, mirror=True)
    # forecastle: raised wedge ahead of the fore deck, black vents
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(13.2, DECK - 0.2, 38.0), (8.8, DECK - 0.2, 48.4), (11.3, 14.7, 38.0), (7.6, 14.7, 47.0)]], 'paint2', bevel=0.16)
    for x in (-6.4, -2.1, 2.2):
        b.box((x, 14.66, 39.6), (x + 3.2, 14.86, 44.4), 'black', bevel=0.0)
    # approach chevrons on the bow deck (real top = DECK): hazard means "aircraft lane"
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.2) for x, z in [(0.25, 57.4), (0.25, 53.4), (8.2, 48.8), (11.6, 49.9)]], 'hazard', bevel=0.03, mirror=True)
    b.cyl((0, DECK, 58.0), (0, DECK + 0.8, 58.0), 0.45, 6, 'lightr')
    # amidships deck between the decks: team bands either side of the tower, tower foot
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.2) for x, z in [(11.8, -13.6), (18.2, -13.6), (18.2, 0.2), (11.8, 0.2)]], 'team', bevel=0.03, mirror=True)
    b.hull([(x, y, z) for x, y, z in
            [(-10.6, DECK - 0.2, -13.1), (1.8, DECK - 0.2, -13.1), (1.8, DECK - 0.2, -0.6), (-10.6, DECK - 0.2, -0.6),
             (-10.0, 17.5, -12.5), (1.2, 17.5, -12.5), (1.2, 17.5, -1.2), (-10.0, 17.5, -1.2)]], 'paint', bevel=0.16)
    # stern: vents, stern light
    for x in (-8.6, -3.0, 2.6):
        b.box((x, DECK - 0.1, -57.6), (x + 4.4, DECK + 0.2, -53.4), 'dark', bevel=0.04)
    b.box((-4.0, 6.0, -60.4), (4.0, 7.0, -59.9), 'lightr', bevel=0.0)
    b.box((23.4, 2.0, -40.0), (23.95, 3.0, -20.0), 'lightc', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ flight decks
    stall(k, 'stall1', -1, 20.0)
    stall(k, 'stall2', +1, -33.4)

    # ------------------------------------------------------------------ control tower (centre x = -4.5, z = -7), boom and strut
    t = k.piece('terminal')
    cx, cz = -4.5, -7.0
    t.hull([(cx + x * s, y, cz + z * c) for s in (-1, 1) for c in (-1, 1) for x, y, z in
            [(5.5, 17.3, 5.6), (4.6, 25.9, 4.2)]], 'paint2', bevel=0.16)
    head = lambda r, rz: [(cx + r, cz), (cx + rz * 0.72, cz + rz), (cx - rz * 0.72, cz + rz), (cx - r, cz), (cx - rz * 0.72, cz - rz), (cx + rz * 0.72, cz - rz)]
    t.hull([(x, y, z) for y, r, rz in [(25.6, 5.2, 4.4), (29.0, 8.5, 6.1), (35.1, 6.5, 4.6), (36.6, 4.9, 3.5)] for x, z in head(r, rz)], 'paint', bevel=0.18)
    t.hull([(x, y, z) for y in (36.66, 36.82) for x, z in head(4.3, 3.0)], 'team', bevel=0.03)
    # window band
    for dz, a in ((-1, 0), (1, 0)):
        t.hull([(cx + x, y, cz + dz * (z + 0.04 * d)) for x in (-4.6, 4.6) for y, z in [(31.4, 5.62), (33.8, 4.95)] for d in (1, 4)], 'lightc', bevel=0.0)
    # starboard boom (flight control), port strut down to the deck
    t.hull([(x, y, z) for x in (0.3, 11.7) for y in (22.0, 26.2) for z in (-10.0, -4.0)] + [(2.8, 24.2, -7.0)], 'dark', bevel=0.14)
    t.box((9.6, 26.1, -9.4), (11.4, 26.5, -4.6), 'lightw', bevel=0.0)
    t.hull([(x, y, z) for z in (-9.5, -4.2) for x, y in [(-17.0, 12.5), (-17.0, 23.8), (-9.1, 28.0), (-9.1, 25.9)]], 'dark', bevel=0.14)
    t.cyl((-17.0, 23.6, -6.85), (-17.0, 26.0, -6.85), 0.5, 6, 'dark')
    t.cyl((-17.0, 26.0, -6.85), (-17.0, 26.4, -6.85), 0.36, 6, 'lightr')
    # dish mount
    t.cyl((-5.72, 36.6, -8.64), (-5.72, 37.2, -8.64), 1.6, 8, 'dark', bevel=0.04)

    # ------------------------------------------------------------------ dish (spin y; 60 deg/s; radar 2400: big and bright)
    d = k.piece('dish'); D = d.at
    d.cyl(D(0, 0, 0), D(0, 9.0, 0), 0.8, 8, 'dark')
    d.hull([D(x, y, z) for x, y, z in
            [(-8.6, 3.4, 3.1), (8.6, 3.4, 3.1), (-8.6, 7.6, 3.1), (8.6, 7.6, 3.1), (-3.8, 1.8, 0.6), (3.8, 1.8, 0.6), (-3.8, 9.2, 0.6), (3.8, 9.2, 0.6),
             (-1.2, 4.4, -0.7), (1.2, 4.4, -0.7), (-1.2, 6.6, -0.7), (1.2, 6.6, -0.7)]], 'steel', bevel=0.1)
    d.cyl(D(0, 9.0, 0), D(0, 9.4, 0), 0.45, 6, 'lightr')
