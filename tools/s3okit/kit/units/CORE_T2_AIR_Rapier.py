"""Rapier (CORE_T2_AIR_Rapier) - Core T2 gunship. A low armoured hover wedge (20 elmo wide) with a long beak, a raised
cockpit block, twin engine nacelles along the rear flanks with tall fins on top, and two big three-barrel rotary
cannons (gun1/gun2, spun 120 deg per shot by the COB, turn z) jutting forward from the front corners like mandibles -
light steel on dark armour, the gunship read from above. Core tip panels (winga/wingb) stand up when landed and fold
out 90 deg in flight (COB turn z): broad swept blades that make the flying Rapier a manta/arrowhead, where the Arm
Brawler is an H with hanging pods.
Pieces (TA layout): base, winga/wingb (tip panels; winga = mirrored clone of wingb), gun1/gun2 (rotary cannons,
gun1 = mirrored clone), flare1/flare2 (empty muzzle points, flash polygons dropped), thrusta (belly lift jet),
thrustb1/thrustb2 (nacelle nozzles) - all empty emit points.
Value groups from above: dark warm armour, darker paint2 nacelles/fins/cockpit block, light steel rotary cannons and
nacelle intake rings, team on the outer half of the panels' inner face (= top in flight) + a spine plate.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=41, drop=['winga'], pose={'wingb': (0, 0, -45)}),
    preview_pose={'winga': (0, 0, 90.0), 'wingb': (0, 0, -90.0)},     # flight: panels folded out
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ armoured wedge hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.4, 1.2, 26.0), (0.4, 2.4, 25.6), (3.6, 0.6, 17.0), (3.4, 5.0, 16.0),
             (6.0, 0.4, 9.0), (5.6, 6.2, 8.4), (9.6, 0.8, 4.0), (9.4, 4.8, 3.0),
             (9.8, 0.8, -15.0), (9.4, 4.2, -15.0), (5.0, 0.8, -18.6), (5.0, 4.4, -18.4)]], 'paint', bevel=0.18)
    # raised cockpit block + spine (paint2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 5.0, 16.0), (4.0, 6.4, 10.0), (3.6, 7.6, 6.0), (3.6, 7.0, -12.0), (2.4, 5.6, -17.6), (4.6, 5.2, -12.0)]],
           'paint2', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 6.2, 15.2), (2.8, 7.4, 10.4), (2.4, 8.6, 6.6), (1.0, 9.0, 8.4), (1.0, 8.9, 6.0), (2.2, 6.0, 14.0)]],
           'glass', bevel=0.07)
    # team plate on the spine
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 7.62, 3.0), (2.6, 7.08, -10.0), (2.6, 7.78, 3.0), (2.6, 7.24, -10.0)]], 'team', bevel=0.02)
    b.box((-0.9, 7.3, -12.6), (0.9, 7.7, -11.6), 'lightr', bevel=0.0)
    # gun mounts at the front corners (gun1/2 spin about z at x +-7.5, y 2.5)
    b.hull([(5.0, 0.2, 11.4), (9.8, 0.2, 10.2), (5.0, 5.2, 11.4), (9.6, 4.8, 10.2),
            (5.0, 0.4, 4.0), (10.0, 0.6, 4.0), (5.0, 5.8, 4.0), (9.6, 5.0, 4.0)], 'paint2', bevel=0.16, mirror=True)
    # rear engine nacelles (thrustb1/2 nozzles at x +-7.5, y 2.8, z -14.9)
    b.hull([(x, y, z) for x in (5.0, 10.4) for y, z in ((0.4, -1.0), (5.4, -2.0), (0.4, -18.6), (5.4, -18.0))] +
           [(7.7, 6.4, -4.0), (7.7, 6.4, -17.0)], 'paint2', bevel=0.2, mirror=True)
    b.cyl((7.7, 3.0, -18.4), (7.7, 3.0, -20.6), 2.3, 12, 'dark', r2=2.0, bevel=0.04, mirror=True)
    b.cyl((7.7, 3.0, -20.55), (7.7, 3.0, -20.7), 1.5, 12, 'lightr', mirror=True)
    b.cyl((7.7, 6.5, -2.4), (7.7, 6.5, -4.8), 1.7, 12, 'steel', bevel=0.05, mirror=True)       # dorsal intake ring
    b.cyl((7.7, 6.5, -2.35), (7.7, 6.5, -2.5), 1.15, 12, 'black', mirror=True)
    # tall fins on the nacelles
    b.hull([(7.3, 5.6, -10.0), (7.3, 5.4, -18.0), (7.3, 10.9, -16.5), (7.3, 10.9, -23.0),
            (8.1, 5.6, -10.0), (8.1, 5.4, -18.0), (8.1, 10.9, -16.5), (8.1, 10.9, -23.0)], 'paint2', bevel=0.07, mirror=True)
    b.box((7.2, 10.8, -22.8), (8.2, 11.2, -21.8), 'lightr', bevel=0.0, mirror=True)
    # belly lift jet (thrusta at 0, 0.1, 1)
    b.cyl((0, 0.6, 1.0), (0, 0.2, 1.0), 2.6, 14, 'dark')
    b.cyl((0, 0.22, 1.0), (0, 0.12, 1.0), 1.8, 14, 'lightr')
    # panel hinge rails (winga/wingb pivot at x +-10, y 3.31)
    b.box((9.2, 2.2, -20.0), (10.0, 4.4, 10.6), 'dark', bevel=0.08, mirror=True)
    b.cyl((0, 1.8, 25.8), (0, 1.8, 28.0), 0.45, 8, 'dark', r2=0.15)

    # ------------------------------------------------------------------ rotary cannon (gun2 at +x; gun1 = mirror)
    g = k.piece('gun2'); G = g.at
    g.cyl(G(0, 0, -0.4), G(0, 0, 3.6), 2.5, 12, 'steel', r2=2.2, bevel=0.1)
    g.cyl(G(0, 0, 3.6), G(0, 0, 4.4), 1.6, 12, 'dark')
    for a in range(3):
        t = math.radians(90 + a * 120)
        bx, by = math.cos(t) * 1.15, math.sin(t) * 1.15
        g.cyl(G(bx, by, 4.0), G(bx, by, 10.6), 0.55, 8, 'steel')
        g.cyl(G(bx, by, 10.55), G(bx, by, 10.7), 0.3, 6, 'black')
    g.cyl(G(0, 0, 7.6), G(0, 0, 8.4), 2.0, 12, 'dark', bevel=0.03)          # barrel clamp
    k.clone('gun1', 'gun2', mirror_x=True)

    # ------------------------------------------------------------------ tip panel (wingb at +x; winga = mirror)
    w = k.piece('wingb'); W = w.at
    # landed: vertical; local y = span (0 at hinge, 14 at tip); local x 0 = inner face (top in flight)
    out = [(0.0, 18.0), (0.0, -12.8), (14.0, -17.7), (14.0, -8.5), (9.7, -4.0)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 1.6)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for y, z in [(5.2, 6.6), (5.2, -12.6), (13.3, -16.6), (13.3, -9.0), (9.4, -5.0)]
            for x in (-0.08, 0.1)], 'team', bevel=0.03)
    w.hull([W(x, y, z) for y, z in [(0.6, 17.0), (0.6, 15.0), (4.4, 7.6), (4.4, 10.4)] for x in (-0.04, 0.1)],
           'steel', bevel=0.0)                                   # light leading-edge cuff near the root
    w.hull([W(x, y, z) for y, z in [(0.6, -12.6), (0.6, -11.6), (13.6, -16.6), (13.6, -17.5)] for x in (-0.04, 0.1)],
           'dark', bevel=0.0)
    w.cyl(W(0.8, 14.2, -8.0), W(0.8, 14.2, -17.8), 0.55, 8, 'dark', r2=0.4)
    w.cyl(W(0.8, 14.2, -7.5), W(0.8, 14.2, -8.02), 0.35, 8, 'lightw', r2=0.55)
    w.cyl(W(0.8, -0.3, -12.6), W(0.8, -0.3, 17.4), 0.75, 8, 'dark')                # hinge barrel
    k.clone('winga', 'wingb', mirror_x=True)
