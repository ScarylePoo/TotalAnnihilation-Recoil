"""Underwater Fusion Powerplant (CORE_T2_SEAECO_UWFusionPowerplant) - Core seabed fusion (no waterline: sits on the sea
bed under at least 15 elmo of water). The land Core fusion's huge light steel containment globe, half sunk into a
massive dark stepped square caisson on its right half, a glowing warm seam where it meets the deck and a team polar cap;
on the left two tall dark pentagonal field towers (vertical, not leaning: they must stand the water pressure) with
team caps and lit tips, steel conduits from the towers to the globe, team edge bands along the caisson front and back,
and the coolant exhaust (emit1) at the left end.
Identity from above (through the water): a big light disc with a team centre on the right of a dark square, two team-
capped tower heads on the left (the land Core fusion is a full globe ringed by three leaning towers; the Arm UW fusion
is two light cones side by side).
Pieces (COB): newcorfus (root), emit1 (exhaust point, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    preview_water=15.0,
    hazard_period=5.0,
    wreck=dict(seed=251),
)

GX, GZ, GR = 13.0, 0.0, 22.0      # globe centre x/z and radius (centre at deck height)
DECK = 12.0


def build(k):
    b = k.piece('newcorfus')
    b.plan(0.0, 5.0, [(-39.0, -38.0), (39.0, -38.0), (41.0, -35.0), (41.0, 35.0), (39.0, 38.0), (-39.0, 38.0),
                      (-41.0, 35.0), (-41.0, -35.0)], 'paint2', bevel=0.4, top_inset=1.4)
    b.plan(4.8, DECK, [(-36.0, -34.0), (37.0, -34.0), (37.0, 34.0), (-36.0, 34.0)], 'paint', bevel=0.4,
           top_inset=2.4)
    for sz in (-1, 1):                                     # team edge bands (front / back)
        b.hull([(x, y, z * sz) for x in (-30.0, 33.0) for z in (25.0, 31.2) for y in (DECK - 0.05, DECK + 0.2)],
               'team', bevel=0.0)
    # half-sunk globe: upper hemisphere above the deck, glowing seam ring
    ring = [(math.cos(i * math.pi / 12), math.sin(i * math.pi / 12)) for i in range(24)]
    pts = []
    for ang in (0, 15, 30, 45, 60, 75):
        a = math.radians(ang); r = GR * math.cos(a); y = DECK + 0.6 + GR * 0.8 * math.sin(a)
        pts += [(GX + x * r, y, GZ + z * r) for x, z in ring]
    pts.append((GX, DECK + 0.6 + GR * 0.8, GZ))
    b.hull(pts, 'steel', bevel=0.0)
    b.hull([(GX + x * r, y, GZ + z * r) for x, z in ring for r, y in ((GR + 1.2, DECK - 0.1), (GR + 0.4, DECK + 1.4))]
           , 'lightc', bevel=0.0)
    cap = []
    for ang in (54, 66, 78, 90):
        a = math.radians(ang); r = GR * math.cos(a) + 0.35; y = DECK + 0.6 + GR * 0.8 * math.sin(a) + 0.35
        cap += [(GX + x * r, y, GZ + z * r) for x, z in ring] if r > 0.5 else [(GX, y, GZ)]
    b.hull(cap, 'team', bevel=0.0)
    for ang in (0, 90, 180, 270):                          # dark meridian straps
        a = math.radians(ang); c, s = math.cos(a), math.sin(a)
        strap = []
        for e in (5, 20, 35, 50, 62):
            ee = math.radians(e); r = GR * math.cos(ee) + 0.25; y = DECK + 0.6 + GR * 0.8 * math.sin(ee) + 0.2
            for w in (-1.0, 1.0):
                strap += [(GX + c * r - s * w, y, GZ + s * r + c * w)]
        b.hull(strap, 'dark', bevel=0.0)
    # two field towers on the left (pentagonal, tapering), team caps, lit tips
    for tz in (-18.0, 18.0):
        P = [(-26.0 + 7.5 * math.cos(math.pi / 2 + i * 2 * math.pi / 5), tz + 7.5 * math.sin(math.pi / 2 + i * 2 * math.pi / 5))
             for i in range(5)]
        b.hull([(x, DECK - 0.5, z) for x, z in P] + [(-26.0 + (x + 26.0) * 0.6, 46.0, tz + (z - tz) * 0.6) for x, z in P],
               'paint2', bevel=0.35)
        b.hull([(-26.0 + (x + 26.0) * 0.62, y, tz + (z - tz) * 0.62) for x, z in P for y in (45.8, 46.2)], 'team',
               bevel=0.0)
        b.cyl((-26.0, 46.0, tz), (-26.0, 50.0, tz), 1.4, 6, 'steel')
        b.cyl((-26.0, 49.8, tz), (-26.0, 51.2, tz), 1.9, 6, 'lightc')
        for y in (20.0, 32.0):
            b.cyl((-26.0, y, tz), (-26.0, y + 1.6, tz), 7.6 - (y - DECK) * 0.088, 5, 'dark', rot=math.pi / 2)
        b.cyl((-20.0, 22.0, tz), (GX - GR * 0.8, 22.0, tz * 0.55), 2.0, 8, 'steel')       # conduit to the globe
    # exhaust at emit1 (left end)
    b.box((-41.6, 0.6, -22.0), (-36.0, 5.0, -13.5), 'dark', bevel=0.2)
    for z in (-21.0, -18.6, -16.2):
        b.box((-41.8, 1.2, z), (-41.5, 4.4, z + 1.4), 'black', bevel=0.0)
    b.box((-33.0, DECK, -6.0), (-19.0, DECK + 5.0, 6.0), 'paint2', bevel=0.3)              # pump block between towers
    b.hull([(x, y, z) for x in (-31.0, -21.0) for y in (DECK + 4.95, DECK + 5.2) for z in (-4.0, 4.0)], 'hazard',
           bevel=0.0)
