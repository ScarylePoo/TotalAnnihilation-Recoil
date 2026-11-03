"""Tidal Generator (CORE_T1_SEAECO_TidalGenerator) - Core tidal power. Waterline 20 (the water surface is model y = 20).
An L-shaped dark power house on piers: two tall turbine halls across the rear and a transformer yard down the left,
wrapped around a big open ring duct. In the ring a vertical-axis "eggbeater" rotor (wheel, spins on y) turns: its three
blades bow out under the surface and its team-coloured spokes run just above it, so the unit's read is a light steel
ring with a turning team star in it, next to a dark block (the Arm tidal is a light nacelle with a rotor in front).
Pieces (COB): base, wheel (spin y; origin 7.5, 17.25, 9; the geometry runs from the sea bed bearing up above the water).
The ring is built from arc segments: a convex hull of a ring would fill its hole.
Value groups from above: dark warm halls and deck, light steel ring, near-black vents and pier tops, team on hall A's
roof and the rotor spokes, warm lights on the coils.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 20.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=73, drop=['wheel']),
    preview_pose={'wheel': (0, 20, 0)},
)

CX, CZ = 7.5, 9.0     # wheel axis


def arc(b, r0, r1, a0, a1, y0, y1, mat, bevel=0.05, r_top=None):
    """one segment of a ring round the wheel axis (degrees; 0 = +x, 90 = +z). r_top narrows the top (chamfered ring)."""
    r0t, r1t = r_top or (r0, r1)
    p = []
    for a in (a0, a1):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        p += [(CX + c * r0, y0, CZ + s * r0), (CX + c * r1, y0, CZ + s * r1),
              (CX + c * r0t, y1, CZ + s * r0t), (CX + c * r1t, y1, CZ + s * r1t)]
    b.hull(p, mat, bevel=bevel)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ deck slab: L around the ring (paint2, low mass)
    b.hull([(x, y, z) for x, z in ((-24, -24), (17.5, -24), (17.5, -7.5), (-24, -7.5)) for y in (16.5, 21.0)],
           'paint2', bevel=0.2)
    b.hull([(x, y, z) for x, z in ((-24.4, -7.9), (-10.4, -7.9), (-10.4, 19.0), (-13.0, 22.5), (-24.4, 22.5))
            for y in (16.1, 20.6)], 'paint2', bevel=0.2)

    # ------------------------------------------------------------------ hall A (big, rear left): team roof
    b.hull([(x, y, z) for x, (y0, y1) in ((-23.0, (20, 28.6)), (-6.0, (20, 28.6)))
            for z, y in ((-23.0, y0), (-23.0, y1 + 2.0), (-14.0, y1 + 2.4), (-2.0, y1 - 1.6), (-2.0, y0))], 'paint', bevel=0.3)
    b.hull([(x, y, z) for x in (-21.6, -7.4) for z, y in ((-21.6, 30.82), (-14.2, 31.12), (-3.6, 27.2))]
           + [(x, y + 0.2, z) for x in (-21.6, -7.4) for z, y in ((-21.6, 30.82), (-14.2, 31.12), (-3.6, 27.2))],
           'team', bevel=0.0)
    # ------------------------------------------------------------------ hall B (lower, rear right): vents
    b.hull([(x, y, z) for x in (-3.6, 16.4) for z, y in ((-23.4, 20.4), (-23.4, 27.0), (-18.0, 28.0), (-9.6, 26.0), (-9.6, 20.4))],
           'paint', bevel=0.3)
    for x0, x1 in ((-1.4, 4.4), (7.4, 13.6)):
        b.hull([(x, y, z) for x in (x0, x1) for z, y in ((-21.6, 27.5), (-18.2, 28.1), (-11.4, 26.5))]
               + [(x, y + 0.25, z) for x in (x0, x1) for z, y in ((-21.6, 27.5), (-18.2, 28.1), (-11.4, 26.5))],
               'black', bevel=0.0)
    b.box((5.0, 28.0, -20.8), (6.8, 29.0, -15.6), 'lightr', bevel=0.0)
    # ------------------------------------------------------------------ transformer yard (front left): three coils
    b.box((-23.6, 20.5, -2.4), (-11.0, 21.6, 21.6), 'dark', bevel=0.12)
    for z, h in ((2.4, 27.0), (10.0, 28.6), (17.0, 26.0)):
        b.cyl((-17.4, 21.4, z), (-17.4, h, z), 4.1, 12, 'steel', r2=3.3, bevel=0.1, rot=math.pi / 12)
        b.cyl((-17.4, h - 0.4, z), (-17.4, h + 0.6, z), 3.5, 12, 'dark', r2=2.2, bevel=0.05, rot=math.pi / 12)
        b.cyl((-17.4, h + 0.55, z), (-17.4, h + 1.1, z), 1.8, 10, 'lightr')
    # bus duct from the coils to the ring
    b.hull([(x, y, z) for x in (-14.0, -8.2) for y in (21.2, 23.0) for z in (7.8, 11.0)], 'paint', bevel=0.12)

    # ------------------------------------------------------------------ ring duct round the rotor (segments)
    n = 16
    for i in range(n):
        a0, a1 = i * 360.0 / n, (i + 1) * 360.0 / n
        arc(b, 12.9, 16.3, a0, a1, 17.0, 23.2, 'steel', bevel=0.05, r_top=(13.4, 15.8))
        if i % 4 == 2:                          # dark clamp blocks across the steel
            arc(b, 12.5, 16.7, a0 + 7.0, a1 - 7.0, 17.0, 23.8, 'dark', bevel=0.06)
    # ------------------------------------------------------------------ piers down to the sea bed
    for x, z in ((-20.0, -20.0), (-20.0, 18.0), (13.0, -20.0)):
        b.cyl((x, 0.0, z), (x, 17.0, z), 4.6, 8, 'dark', r2=3.2, rot=math.pi / 8)
    for a in (40.0, 160.0, 280.0):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        b.cyl((CX + c * 14.6, 0.0, CZ + s * 14.6), (CX + c * 14.6, 17.4, CZ + s * 14.6), 2.2, 8, 'dark', r2=1.7, rot=math.pi / 8)
    b.cyl((CX, 0.0, CZ), (CX, 1.0, CZ), 4.0, 10, 'dark', rot=math.pi / 10)      # sea bed bearing

    # ---------------------------------------------------------------- wheel: eggbeater rotor (origin 7.5, 17.25, 9)
    w = k.piece('wheel'); W = w.at
    w.cyl(W(0, -17.0, 0), W(0, 8.2, 0), 1.7, 10, 'steel', rot=math.pi / 10)                  # axle, sea bed to hub
    w.cyl(W(0, 6.4, 0), W(0, 9.2, 0), 4.2, 12, 'dark', bevel=0.12, rot=math.pi / 12)         # top hub
    w.cyl(W(0, 9.15, 0), W(0, 9.8, 0), 2.2, 10, 'lightr')
    w.cyl(W(0, -16.0, 0), W(0, -13.6, 0), 3.2, 10, 'dark', bevel=0.08, rot=math.pi / 10)     # bottom hub
    # blade stations: (local y, radius); bowed like an eggbeater, from the bottom hub out and back to the spoke end
    st = [(-14.0, 2.0), (-8.0, 9.0), (-1.0, 11.6), (3.8, 11.8), (7.0, 11.8)]
    for i in range(3):
        a = math.radians(30 + 120 * i)
        c, s = math.cos(a), math.sin(a)
        R = lambda u, y, v: W(c * u - s * v, y, s * u + c * v)
        for (y0, r0), (y1, r1) in zip(st, st[1:]):
            w.hull([R(r + dr, y, v) for y, r in ((y0, r0), (y1, r1)) for dr in (-0.45, 0.45) for v in (-1.7, 1.7)], 'paint2', bevel=0.05)
        # spoke, hub to blade top, team on top: the wide star turning in the ring
        w.hull([R(u, y, v) for u, hw in ((2.6, 2.2), (12.3, 3.0)) for y in (6.6, 8.0) for v in (-hw, hw)], 'dark', bevel=0.08)
        w.hull([R(u, y, v) for u, hw in ((3.8, 1.9), (12.0, 2.7)) for y in (8.05, 8.25) for v in (-hw, hw)], 'team', bevel=0.0)
