"""Envoy (CORE_T1_SEA_Envoy) - Core naval transport. A very wide, rounded-octagon dark barge with flared sides, a
raised forecastle at the bow, a deep cargo hold amidships closed by three transverse deck panels that slide aft and
stack (door1 > door2 > door3, each moves 15 back along z on its parent), and aft a hexagonal crane base with a tall
column; on top a heavy boom (counterweight behind, team top) with five telescoping sections and a hexagonal magnet.
Distinct from the Arm Hulk (side-hinged hatch halves + two-pillar gantry): here the hold reads as three light
cross-bands with team stripes, and the crane is one central column.
Value groups from above: dark Core hull, darker paint2 flare/skirt, light steel deck panels and crane column, team on
the panels and counterweight, ochre hazard magnet rim.
Pieces (TA layout): base, turret (turn y), boom (turn x), arm1..arm5 (move z, nested), magnet (turn x), link (empty,
cargo point), door1/door2/door3 (move z, nested), wake1/2 (empty). Floater, no waterline (water at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=2048,
    bake_res=2048,
    always_visible=['arm2', 'arm3', 'arm4', 'arm5'],
    wreck=dict(seed=8, drop=['magnet'], pose={'turret': (0, -30, 0), 'boom': (10, 0, 0)}),
    preview_pose={},
)

DECK = 12.6
WATER = [(0.0, 59.0), (9.4, 58.6), (26.6, 45.5), (33.3, 30.4), (33.3, -45.8), (16.6, -58.6)]
DECKO = [(0.0, 49.6), (8.5, 49.3), (18.4, 41.4), (23.4, 31.3), (23.4, -39.8), (9.6, -50.6)]


def cut(pts, z0, z1):
    P = sorted({z: x for x, z in pts}.items())
    zs = [z for z, _ in P]; xs = [x for _, x in P]

    def xat(z):
        for i in range(len(zs) - 1):
            if zs[i] <= z <= zs[i + 1]:
                t = (z - zs[i]) / (zs[i + 1] - zs[i]); return xs[i] + t * (xs[i + 1] - xs[i])
        return xs[0] if z < zs[0] else xs[-1]
    lo, hi = max(z0, zs[0]), min(z1, zs[-1])
    return [(xat(z), z) for z in sorted({lo, hi} | {z for z in zs if lo < z < hi})]


def ring(pts, y, sx=1.0):
    return [(x * sx * s, y, z) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull segments: keel, flared skirt, deck rim
    segs = ((31.3, 60.0), (-17.4, 31.3), (-60.0, -17.4))
    for z0, z1 in segs:
        w, d = cut(WATER, z0, z1), cut(DECKO, z0, z1)
        kk = [(x * 0.62, max(min(z, 52.0), -52.0)) for x, z in w]
        b.hull(ring(kk, -3.0) + ring(w, 0.0), 'paint2', bevel=0.25)
        b.hull(ring(w, 0.0) + ring(w, 2.2, 0.985) + ring(d, DECK), 'paint2', bevel=0.25)
    # deck rim around the hold (dark Core paint), the hold itself is open below the panels
    b.hull(ring(cut(DECKO, 31.3, 60.0), DECK - 0.6) + ring(cut(DECKO, 31.3, 60.0), DECK + 0.2, 0.98), 'paint', bevel=0.15)
    b.hull(ring(cut(DECKO, -60.0, -17.4), DECK - 0.6) + ring(cut(DECKO, -60.0, -17.4), DECK + 0.2, 0.98), 'paint', bevel=0.15)
    for x0, x1 in ((23.4, 30.0),):
        b.hull([(x, y, z) for x in (23.4, 29.6) for y in (DECK - 0.6, DECK + 0.2) for z in (-17.4, 31.3)] +
               [(31.0, 8.0, z) for z in (-17.4, 31.3)], 'paint', bevel=0.15, mirror=True)
    # hold: black floor and dark inner walls just under the panels
    b.box((-23.4, 4.0, -17.4), (23.4, 4.4, 31.3), 'black', bevel=0.0)
    # rubbing strake on the flare
    b.hull([(x, y, z) for x in (31.8, 32.4) for y in (5.6, 6.6) for z in (-40.0, 26.0)], 'dark', bevel=0.05, mirror=True)
    # ------------------------------------------------------------------ forecastle (raised, light steel top)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(12.5, DECK, 33.8), (12.5, DECK, 45.0), (8.8, 18.8, 36.2), (8.8, 18.8, 40.0)]], 'paint', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.2, 18.75, 36.6), (8.2, 18.75, 39.6), (8.1, 18.95, 36.7), (8.1, 18.95, 39.5)]], 'steel', bevel=0.03)
    b.box((11.6, 14.2, 44.6), (12.0, 15.2, 45.4), 'lightw', bevel=0.0, mirror=True)
    for x in (6.0,):
        b.cyl((x, DECK, 47.0), (x, DECK + 1.4, 47.0), 1.0, 10, 'dark', mirror=True)
    # vents between hold and crane base
    b.hull([(x, y, z) for x, y, z in
            [(5.0, DECK, -17.5), (16.2, DECK, -17.5), (5.0, DECK, -22.5), (16.2, DECK, -22.5),
             (7.5, 18.8, -21.2), (13.8, 18.8, -21.2), (7.5, 18.8, -24.1), (13.8, 18.8, -24.1)]], 'paint', bevel=0.15, mirror=True)
    b.box((8.2, 18.75, -23.6), (13.1, 18.95, -21.7), 'black', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ aft superstructure the crane stands on
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(21.2, DECK, -22.5), (21.2, DECK, -40.0), (15.0, DECK, -40.0), (8.8, DECK, -50.0),
             (21.2, 22.5, -25.0), (21.2, 22.5, -40.0), (15.0, 22.5, -40.0), (8.8, 22.5, -50.0)]], 'paint', bevel=0.25)
    b.box((-20.6, 18.0, -22.95), (20.6, 20.6, -22.65), 'black', bevel=0.0)        # the panels stack into this slot
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(20.6, 22.45, -25.6), (20.6, 22.45, -27.6), (20.5, 22.65, -25.6), (20.5, 22.65, -27.6)]], 'hazard', bevel=0.0)
    b.box((21.15, 17.0, -38.0), (21.4, 18.0, -28.0), 'lightc', bevel=0.0, mirror=True)
    b.box((-2.0, 9.6, -58.0), (2.0, 10.4, -57.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ sliding deck panels (light steel, team stripe)
    def panel(name, z0, z1, y0, ox):
        p = k.piece(name)
        p.box((-23.2 + ox, y0 - 0.5, z0), (23.2 + ox, y0, z1), 'steel', bevel=0.12)
        p.box((-18.0 + ox, y0 - 0.05, z0 + 4.4), (18.0 + ox, y0 + 0.2, z1 - 4.4), 'team', bevel=0.03)
        for x in (-21.2, 21.2):
            p.box((x - 0.8 + ox, y0 - 0.05, z0 + 0.8), (x + 0.8 + ox, y0 + 0.25, z1 - 0.8), 'dark', bevel=0.03)
    panel('door1', -17.4, -1.3, 12.6, -0.16)
    panel('door2', -1.21, 15.1, 13.1, 0.0)
    panel('door3', 15.16, 31.3, 13.6, -0.16)

    # ------------------------------------------------------------------ crane base + column (turret origin 0, 23, -37.5)
    t = k.piece('turret'); T = t.at
    hexo = [(14.1, 0.0), (8.2, -10.8), (-8.2, -10.8), (-14.1, 0.0), (-8.2, 10.8), (8.2, 10.8)]
    t.hull([T(x, y, z) for x, z in hexo for y in (-0.5, 8.7)], 'paint', bevel=0.25)
    t.hull([T(x * 0.95, 8.7, z * 0.95) for x, z in hexo] + [T(x * 0.58, 18.1, z * 0.5) for x, z in hexo], 'paint2', bevel=0.2)
    t.hull([T(x, y, z) for x, z in ((8.1, 0.0), (5.2, -5.3), (-5.2, -5.3), (-8.1, 0.0), (-5.2, 5.3), (5.2, 5.3))
            for y in (18.0, 45.1)], 'steel', bevel=0.2)
    t.box(T(-1.4, 30.0, 5.2), T(1.4, 42.0, 5.5), 'lightc', bevel=0.0)
    # control cab on the base, front
    t.hull([T(x, y, z) for x, y, z in
            [(-5.0, 8.0, 8.6), (5.0, 8.0, 8.6), (-4.4, 8.0, 14.0), (4.4, 8.0, 14.0),
             (-4.6, 13.2, 8.6), (4.6, 13.2, 8.6), (-4.0, 12.0, 12.6), (4.0, 12.0, 12.6)]], 'paint', bevel=0.15)
    t.hull([T(x, y, z) for x, y, z in
            [(-3.9, 9.4, 13.95), (3.9, 9.4, 13.95), (-3.8, 11.7, 12.85), (3.8, 11.7, 12.85),
             (-3.9, 9.4, 14.25), (3.9, 9.4, 14.25), (-3.8, 11.7, 13.15), (3.8, 11.7, 13.15)]], 'glass', bevel=0.0)

    # ------------------------------------------------------------------ boom (origin 0, 62.5, -37.5): counterweight aft
    bm = k.piece('boom'); B = bm.at
    bm.cyl(B(-6.0, 0, 0), B(6.0, 0, 0), 3.2, 12, 'dark')
    bm.box(B(-4.2, -3.8, -20.0), B(4.2, 3.8, 35.0), 'paint2', bevel=0.2)
    bm.box(B(-2.4, 3.75, 2.0), B(2.4, 4.05, 32.0), 'hazard', bevel=0.03)
    bm.hull([B(x * s, y, z) for s in (-1, 1) for x, y, z in
             [(18.8, -6.3, -18.7), (18.8, 6.2, -18.7), (13.8, -3.8, -36.2), (13.8, 3.7, -36.2)]], 'paint', bevel=0.3)
    bm.hull([B(x * s, y, z) for s in (-1, 1) for x, y, z in
             [(16.4, 5.8, -20.4), (12.4, 3.6, -34.4), (16.3, 6.0, -20.4), (12.3, 3.8, -34.4)]], 'team', bevel=0.04)
    # telescoping sections (arm1..arm5 share origin z -67.5; tips stepped)
    for name, w, tip in (('arm1', 3.3, 69.5), ('arm2', 2.95, 70.1), ('arm3', 2.6, 70.7), ('arm4', 2.3, 71.3),
                         ('arm5', 2.0, 81.2)):
        p = k.piece(name); o = p.at(0, 0, 0)
        p.box((o[0] - w, o[1] - w, o[2] + 33.0), (o[0] + w, o[1] + w, o[2] + tip),
              'steel' if name in ('arm2', 'arm4') else 'dark', bevel=0.1)
    # magnet (origin 0, 62.5, 6.75): stem + hexagonal plate with a team top and hazard rim
    m = k.piece('magnet'); M = m.at
    m.box(M(-2.5, -13.3, -4.25), M(2.5, 2.5, 4.25), 'dark', bevel=0.15)
    m.box(M(-5.0, -13.3, -4.25), M(5.0, -5.5, 4.25), 'paint2', bevel=0.15)
    hexm = [(14.5, 0.0), (7.2, -12.6), (-7.2, -12.6), (-14.5, 0.0), (-7.2, 12.6), (7.2, 12.6)]
    m.hull([M(x, -20.0, z) for x, z in hexm] + [M(x, -17.1, z) for x, z in hexm] +
           [M(x * 0.55, -13.2, z * 0.55) for x, z in hexm], 'paint2', bevel=0.2)
    m.hull([M(x * 1.02, -19.0, z * 1.02) for x, z in hexm] + [M(x * 1.02, -17.6, z * 1.02) for x, z in hexm], 'hazard', bevel=0.05)
    m.hull([M(x * 0.5, -13.25, z * 0.5) for x, z in hexm] + [M(x * 0.5, -13.05, z * 0.5) for x, z in hexm], 'team', bevel=0.03)
    m.hull([M(x * 0.9, -20.2, z * 0.9) for x, z in hexm] + [M(x * 0.9, -20.05, z * 0.9) for x, z in hexm], 'lightc', bevel=0.0)
