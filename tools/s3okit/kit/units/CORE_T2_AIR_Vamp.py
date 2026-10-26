"""Vamp (CORE_T2_AIR_Vamp) - Core T2 stealth fighter. The Avenger's big brother as a bat: a broad, faceted diamond
body (wider and heavier than the Avenger's arrowhead) with a raised armoured spine, twin light steel intake humps
and two missile tubes slung beside the belly. Core's tip panels (winga/wingb) are bat wings here: three finger
spars fanning out from the hinge with scalloped membranes between them. They stand up when landed and fold out
111.7 deg in flight (COB turn z) - past horizontal, so the flying Vamp has drooping bat wings with a saw-toothed
trailing edge, unlike any other Core plane.
Pieces (TA layout): base, winga/wingb (bat wings; winga = mirrored clone of wingb), jet (tail nozzle block),
thrustb (empty, child of jet), missilea/missileb (empty launch points), thrusta1/thrusta2 (empty lift-jet emits).
Value groups from above: dark warm armour, darker paint2 spine and wing spars, light steel intake humps + missile
tubes (the light bars), team on the membranes' inner face (= top in flight).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=33, drop=['winga'], pose={'wingb': (0, 0, -60)}),
    preview_pose={'winga': (0, 0, 111.67), 'wingb': (0, 0, -111.67)},    # flight: bat wings folded out and down
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ faceted diamond body (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 3.0, 17.0), (0.3, 2.2, 16.4),
             (3.4, 1.4, 9.0), (3.0, 5.6, 8.4),
             (8.2, 2.6, 2.0), (7.0, 6.6, 1.0), (3.4, 8.2, 0.0),
             (8.2, 2.6, -12.0), (6.6, 6.8, -11.0), (3.4, 8.0, -11.0),
             (4.6, 2.2, -15.0), (3.0, 6.2, -14.4)]], 'paint', bevel=0.18)
    # belly keel
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 0.4, 6.0), (3.4, 2.0, 8.0), (3.0, 0.4, -10.0), (3.6, 2.0, -12.0), (5.0, 2.0, -4.0)]], 'paint2', bevel=0.12)
    # raised armoured spine (dark paint2 block down the middle)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 8.0, 1.4), (2.2, 8.6, -2.0), (2.2, 8.6, -12.0), (1.6, 8.0, -14.8), (2.8, 7.6, -12.0), (2.8, 7.6, -2.0)]],
           'paint2', bevel=0.1)
    # cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 4.4, 12.6), (2.4, 6.0, 7.6), (2.2, 7.6, 2.4), (0.9, 8.5, 5.8), (0.9, 8.6, 2.6), (1.4, 5.4, 10.6)]],
           'glass', bevel=0.08)
    b.cyl((0, 2.6, 16.8), (0, 2.6, 19.0), 0.42, 8, 'dark', r2=0.15)
    # twin light steel intake humps beside the spine (the Vamp's two light bars from above)
    b.hull([(2.8, 6.4, 6.2), (5.6, 5.6, 5.0), (2.8, 8.2, 3.0), (5.8, 7.4, 2.0), (4.2, 8.4, 2.0),
            (2.8, 7.6, -10.0), (6.0, 6.6, -10.0), (4.2, 8.6, -8.0), (2.8, 7.0, -13.4), (5.4, 6.0, -13.0)],
           'steel', bevel=0.16, mirror=True)
    b.hull([(3.1, 6.55, 6.25), (5.4, 5.8, 5.1), (3.1, 7.9, 3.3), (5.5, 7.2, 2.4),
            (3.1, 6.55, 5.95), (5.4, 5.8, 4.8), (3.1, 7.9, 3.0), (5.5, 7.2, 2.1)], 'black', bevel=0.0, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(3.4, 8.36, -1.0), (5.0, 8.1, -1.0), (3.4, 8.44, -6.0), (5.0, 8.24, -6.0)]] +
           [(x, y + 0.12, z) for x, y, z in [(3.4, 8.36, -1.0), (5.0, 8.1, -1.0), (3.4, 8.44, -6.0), (5.0, 8.24, -6.0)]],
           'dark', bevel=0.0, mirror=True)                  # dark vent grille on each hump
    # wing hinge blocks (winga/wingb pivot at x +-8.65, y 5.1)
    b.box((7.4, 3.0, -13.6), (8.7, 5.7, 3.4), 'paint2', bevel=0.12, mirror=True)
    # missile tubes beside the belly (launch points missilea/b at +-6.25, 2.59, 3.74)
    b.box((5.6, 2.2, -6.0), (6.9, 3.2, 2.0), 'dark', bevel=0.06, mirror=True)
    b.cyl((6.25, 1.7, -8.0), (6.25, 1.7, 3.4), 1.05, 8, 'steel', rot=math.pi / 8, mirror=True)
    b.cyl((6.25, 1.7, 3.4), (6.25, 1.7, 4.4), 1.1, 8, 'dark', rot=math.pi / 8, mirror=True)
    b.cyl((6.25, 1.7, 4.36), (6.25, 1.7, 4.46), 0.7, 8, 'lightr', mirror=True)
    # belly lift-jet grilles (thrusta1/2 emit at x +-4.2, z -3.8)
    b.cyl((4.2, 0.9, -3.8), (4.2, 0.5, -3.8), 1.5, 12, 'dark', mirror=True)
    b.cyl((4.2, 0.52, -3.8), (4.2, 0.42, -3.8), 1.0, 12, 'lightr', mirror=True)
    # canted ventral fins
    b.hull([(3.0, 2.0, -6.0), (3.4, 1.8, -14.0), (5.6, -2.2, -11.0), (5.8, -2.2, -14.6),
            (3.6, 2.0, -6.0), (4.0, 1.8, -14.0), (6.1, -2.2, -11.0), (6.3, -2.2, -14.6)], 'paint2', bevel=0.06, mirror=True)
    b.box((-1.2, 8.7, -6.0), (1.2, 9.0, -4.6), 'lightr', bevel=0.0)        # dorsal beacon

    # ------------------------------------------------------------------ tail nozzle block (jet, origin 0, 4, -11.12)
    j = k.piece('jet'); J = j.at
    j.cyl(J(0, 0, 0.6), J(0, 0, -1.6), 2.3, 12, 'dark', r2=2.0, bevel=0.06)
    j.cyl(J(0, 0, -1.55), J(0, 0, -1.7), 1.4, 12, 'lightr')

    # ------------------------------------------------------------------ bat wing (wingb at +x; winga = mirror)
    w = k.piece('wingb'); W = w.at
    # landed: vertical, local y = span (0 at hinge, 13.8 at tip), local z = chord; local x 0 = inner face (top in
    # flight). Membranes are convex sectors fanning from the root O between three finger spars; the trailing edge
    # is scalloped between the finger tips (notches N1, N2).
    O, LR, LM, F3, F2, N2, F1, N1, TR = ((0.6, -1.0), (0.0, 6.0), (7.6, 3.0), (13.8, -1.0), (13.8, -12.8),
                                         (10.4, -7.6), (7.6, -10.6), (4.2, -6.0), (0.0, -8.6))
    secs = [((O, LR, LM, F3), 'paint2'), ((O, F3, F2), 'team'), ((O, F2, N2), 'team'), ((O, N2, F1), 'team'),
            ((O, F1, N1), 'paint2'), ((O, N1, TR), 'paint2')]
    for sec, m in secs:
        w.hull([W(x, y, z) for y, z in sec for x in (0.1, 0.75)], 'paint2', bevel=0.04)
        if m == 'team':
            cy = sum(p[0] for p in sec) / len(sec); cz = sum(p[1] for p in sec) / len(sec)
            ins = [(cy + (y - cy) * 0.86, cz + (z - cz) * 0.86) for y, z in sec]
            w.hull([W(x, y, z) for y, z in ins for x in (-0.06, 0.12)], 'team', bevel=0.02)
    # team on the leading sector's outer part too
    w.hull([W(x, y, z) for y, z in ((6.4, 2.4), (12.4, -0.9), (5.0, -0.6)) for x in (-0.06, 0.12)], 'team', bevel=0.02)
    # finger spars (dark ribs on the inner face fanning from the root to the finger tips) + leading-edge spar
    for (y1, z1) in (F1, F2, F3):
        w.cyl(W(-0.1, O[0], O[1]), W(-0.1, y1, z1), 0.42, 6, 'dark', r2=0.24)
    w.cyl(W(-0.1, 0.0, 6.0), W(-0.1, 7.6, 3.0), 0.4, 6, 'dark', r2=0.32)
    w.cyl(W(-0.1, 7.6, 3.0), W(-0.1, 13.8, -1.0), 0.32, 6, 'dark', r2=0.22)
    w.cyl(W(0.4, 0.0, -9.0), W(0.4, 0.0, 6.4), 0.75, 8, 'dark')                 # hinge barrel
    w.box(W(-0.2, 13.4, -2.0), W(0.9, 14.2, -0.6), 'lightw', bevel=0.0)          # tip light
    k.clone('winga', 'wingb', mirror_x=True)
