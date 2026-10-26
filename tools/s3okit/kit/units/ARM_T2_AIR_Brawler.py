"""Brawler (ARM_T2_AIR_Brawler) - Arm T2 gunship. A fat, round armoured hover body (15 elmo wide, 45 long) with a
bubble cockpit, a dorsal intake, twin tall tail fins and stubby wings carrying vertical-lift engine nacelles at the
tips. Under each wing hangs a heavy rotary-cannon pod (weapon1/weapon2). On take-off the COB slides the wings out
7.25 elmo and the gun pods 7.1-7.4 elmo with them (move x), so the flying Brawler is a broad H: a pale fuselage
between two dark gun pods with long barrels poking forward - the gunship read from above.
Pieces (TA layout): base, wing1/wing2 (sliding wings; wing1 = mirrored clone of wing2), weapon1/weapon2 (gun pods;
weapon2 = mirrored clone), flare1A/1B/2A/2B (empty gun emit points; the COB fires from flare1B's emit vertex),
wing1thrust/wing2thrust (empty, children of the opposite wings as in TA), tail1/tail2 (empty, the COB turns them),
rearthrust (empty).
Value groups from above: light Arm fuselage and wings, dark paint2 gun pods + engine nacelles, near-black barrels
and intakes, team on the outer wing panels and the pod tops.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=39, drop=['weapon2'], remove=['wing1']),
    always_visible=['wing1', 'wing2'],
    # flight pose (engine x = -COB x)
    preview_pose={'wing1': {'move': (-7.25, 0, 0)}, 'wing2': {'move': (7.25, 0, 0)},
                  'weapon1': {'move': (7.125, 0, 0)}, 'weapon2': {'move': (-7.375, 0, 0)}},
)


def ring(z, rx, y0, y1, k=0.42):
    """octagon-ish section at z: half width rx, from y0 to y1 (k = corner cut)."""
    ym = (y0 + y1) / 2; ry = (y1 - y0) / 2
    return [(rx, ym + ry * k, z), (rx, ym - ry * k, z), (rx * k, y0, z), (rx * k, y1, z),
            (-rx, ym + ry * k, z), (-rx, ym - ry * k, z), (-rx * k, y0, z), (-rx * k, y1, z)]


def top_y(pts, x, z):
    """height of the convex hull of pts above (x, z) (for decals that must sit just above a hull's top)."""
    from scipy.spatial import ConvexHull
    h = ConvexHull(pts)
    return min(-(a * x + c * z + d) / b for a, b, c, d in h.equations if b > 1e-6)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ round armoured fuselage (crosses x = 0)
    FUS = ring(22.8, 1.6, 8.2, 10.6) + ring(15.4, 6.6, 5.6, 13.8) + ring(10.0, 7.7, 5.4, 14.6) + ring(-12.7, 7.7, 5.5, 13.6)
    b.hull(FUS, 'paint', bevel=0.2, seg=2)
    # team shoulder plates on the fuselage flanks beside the intake (the body's colour read from above)
    b.hull([(x, top_y(FUS, x, z) + d, z) for x in (4.7, 7.0) for z in (8.0, -11.0) for d in (0.08, 0.2)],
           'team', bevel=0.02, mirror=True)
    b.hull(ring(-12.6, 7.4, 5.6, 13.4) + ring(-21.2, 2.6, 7.9, 10.4), 'paint', bevel=0.16)
    # bubble cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 10.2, 20.6), (3.6, 13.0, 15.0), (3.0, 14.6, 8.6), (1.4, 15.6, 11.6), (1.2, 15.4, 7.0), (2.6, 13.8, 5.0)]],
           'glass', bevel=0.08)
    # dorsal intake / rotor housing (dark paint2 block on the spine)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.8, 14.0, 3.0), (4.4, 14.0, -11.0), (3.0, 15.8, 1.4), (3.2, 15.8, -10.0), (2.6, 13.4, -14.4)]],
           'paint2', bevel=0.14)
    b.box((-2.6, 15.7, 0.4), (2.6, 15.95, -8.0), 'black', bevel=0.0)
    for z in (-1.4, -3.6, -5.8):
        b.box((-2.8, 15.9, z - 0.35), (2.8, 16.1, z + 0.35), 'dark', bevel=0.0)
    # team spine stripe from the intake to the tail
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.5, 13.62, -14.0), (1.2, 10.5, -21.0), (1.5, 13.78, -14.0), (1.2, 10.66, -21.0)]], 'team', bevel=0.02)
    # chin sensor + nose light
    b.cyl((0, 7.4, 17.0), (0, 6.2, 17.0), 1.4, 10, 'dark', bevel=0.04)
    b.cyl((0, 6.2, 17.0), (0, 5.9, 17.0), 0.9, 10, 'lightw')
    # wing roots (the sliding wings run through here)
    b.box((6.8, 7.6, -10.4), (8.4, 10.4, 10.0), 'paint2', bevel=0.14, mirror=True)
    # twin tall canted fins
    b.hull([(2.8, 12.2, -12.0), (2.8, 11.0, -21.0), (7.3, 17.8, -19.5), (7.7, 17.6, -23.0),
            (3.6, 12.2, -12.0), (3.6, 11.0, -21.0), (8.0, 17.8, -19.5), (8.4, 17.6, -23.0)], 'paint', bevel=0.08, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(6.6, 16.4, -18.6), (7.3, 17.8, -19.5), (7.7, 17.6, -23.0), (7.0, 16.3, -22.6)]] +
           [(x + 0.75, y, z) for x, y, z in [(6.6, 16.4, -18.6), (7.3, 17.8, -19.5), (7.7, 17.6, -23.0), (7.0, 16.3, -22.6)]],
           'team', bevel=0.0, mirror=True)
    b.box((7.5, 17.7, -22.8), (8.4, 18.1, -21.8), 'lightr', bevel=0.0, mirror=True)
    # rear lift nozzle (rearthrust 0, 4.7, -18.8)
    b.cyl((0, 6.0, -18.8), (0, 4.6, -18.8), 2.0, 12, 'dark', r2=1.7, bevel=0.04)
    b.cyl((0, 4.62, -18.8), (0, 4.5, -18.8), 1.2, 12, 'lightc')

    # ------------------------------------------------------------------ wing2 (origin 4.75, 8.38, 0; slides +7.25)
    w = k.piece('wing2'); W = w.at
    pl = [(-4.0, 10.5), (-4.0, -10.5), (16.8, -10.5), (16.8, -4.6), (6.0, 4.0), (1.0, 6.0)]
    w.hull([W(x, y, z) for x, z in pl for y in (0.0, 1.5)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for x, z in ((3.6, 4.6), (6.0, 3.0), (15.6, -4.6), (15.6, -9.6), (3.6, -9.6)) for y in (1.52, 1.62)],
           'team', bevel=0.02)
    # tip lift-engine nacelle (wing1thrust emit at local 12.5, z -8.5)
    w.cyl(W(12.5, 0.6, 3.0), W(12.5, 0.6, -13.2), 2.0, 12, 'paint2', r2=1.8, rot=math.pi / 12, bevel=0.08)
    w.cyl(W(12.5, 0.6, 3.2), W(12.5, 0.6, 2.9), 1.3, 12, 'black')
    w.cyl(W(12.5, 0.6, -13.15), W(12.5, 0.6, -13.35), 1.2, 12, 'lightc')
    w.cyl(W(12.5, -1.6, -8.5), W(12.5, -2.2, -8.5), 1.4, 12, 'dark')       # lift-jet grille under the nacelle
    w.box(W(16.6, 0.2, -10.4), W(17.2, 1.3, -9.4), 'lightw', bevel=0.0)
    k.clone('wing1', 'wing2', mirror_x=True)

    # ------------------------------------------------------------------ gun pod (weapon1, origin 0, 7.5, 0; geometry +x)
    g = k.piece('weapon1'); G = g.at
    # pylon up to the wing underside
    g.box(G(11.0, -2.6, -1.0), G(13.0, 0.9, 5.0), 'dark', bevel=0.1)
    # pod body
    g.hull([G(x, y, z) for x in (9.4, 14.6) for y in (-7.4, -2.6) for z in (-2.0, 7.4)] +
           [G(12.0, -2.0, 6.0), G(12.0, -2.0, -1.0)], 'paint2', bevel=0.2)
    g.hull([G(x, y, z) for x in (10.2, 13.8) for z in (-1.0, 6.4) for y in (-2.38, -2.26)], 'team', bevel=0.02)
    # rotary barrel cluster
    g.cyl(G(12.0, -5.0, 7.3), G(12.0, -5.0, 8.6), 2.0, 12, 'dark', bevel=0.04)
    for a in range(5):
        t = math.radians(a * 72 + 18)
        g.cyl(G(12.0 + math.cos(t) * 1.2, -5.0 + math.sin(t) * 1.2, 8.4), G(12.0 + math.cos(t) * 1.2, -5.0 + math.sin(t) * 1.2, 12.6),
              0.42, 6, 'steel')
    g.cyl(G(12.0, -5.0, 11.6), G(12.0, -5.0, 12.2), 1.9, 12, 'dark')
    g.cyl(G(12.0, -5.0, -2.0), G(12.0, -5.0, -3.0), 1.6, 10, 'dark', r2=1.2)        # ammo drum cap
    k.clone('weapon2', 'weapon1', mirror_x=True)
