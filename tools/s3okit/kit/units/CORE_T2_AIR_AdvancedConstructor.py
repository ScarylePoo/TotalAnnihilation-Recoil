"""Advanced Construction Aircraft (CORE_T2_AIR_AdvancedConstructor) - Core T2 air builder. The T1 builder's long box
with team roof doors, grown heavier: a wider armoured hull with a stepped glazed nose, two broad side sponsons
carrying the panel hinges, belly lift jets, a tall single fin with a stabiliser, and TWIN light steel nano turrets
with ochre shrouds on the rear sponson corners (the right one aims at the build-beam origin, base's first vertex at
the rear-right as in TA). The Core tip panels (wing1/wing2) stand up when landed and fold out 90 deg in flight.
From above: a dark box with two bright team doors down the middle, flanked by sponsons and two light turrets -
the T1 is a plain box with one chin turret.
Pieces (TA layout): base, door1/door2 (roof doors; door1 = mirrored clone of door2), wing1/wing2 (tip panels;
wing1 = mirrored clone of wing2), thrusta1/thrusta2 (belly lift jets), thrustb (main nozzle) - empty emit points.
Value groups from above: dark warm armour, team doors, darker paint2 sponsons/tail, light steel nano turrets and door
hinges, ochre hazard on the turret shrouds and the panel roots.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=57, drop=['door1'], pose={'wing1': (0, 0, 40)}),
    preview_pose={'wing1': (0, 0, 90.0), 'wing2': (0, 0, -90.0)},     # flight: tip panels folded out
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ wide armoured hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 1.2, 24.4), (1.2, 3.6, 23.8), (3.8, 0.2, 18.1), (3.8, 5.8, 18.1),
             (6.6, 0.2, 15.0), (6.6, 8.4, 15.0), (6.6, 0.2, -16.9), (6.6, 8.4, -16.9),
             (4.2, 3.0, -21.0), (4.2, 7.6, -21.0)]], 'paint', bevel=0.2, seg=2)
    # stepped glazed nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 3.8, 23.0), (3.4, 5.6, 18.6), (3.0, 7.6, 16.0), (1.2, 4.6, 22.0)]] +
           [(x * sx, y + 0.12, z + 0.12) for sx in (-1, 1) for x, y, z in [(3.4, 5.6, 18.6), (3.0, 7.6, 16.0)]],
           'glass', bevel=0.05)
    b.box((-1.6, 1.6, 24.2), (1.6, 2.4, 24.5), 'lightw', bevel=0.0)
    # door hinges along the roof edges (light steel rails) + rear roof block
    b.cyl((6.2, 8.5, 15.4), (6.2, 8.5, -9.8), 0.45, 8, 'steel', mirror=True)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 8.4, -9.4), (6.4, 8.4, -16.8), (5.0, 10.0, -10.0), (4.4, 10.4, -16.6)]], 'paint2', bevel=0.12)
    for z in (-11.4, -13.4):
        b.box((-3.6, 10.1, z - 0.4), (3.6, 10.3, z + 0.4), 'black', bevel=0.0)
    # tall single fin + stabiliser
    b.hull([(x, y, z) for x in (-0.5, 0.5) for y, z in ((10.0, -12.0), (7.6, -21.4), (13.6, -17.7), (13.6, -24.2))],
           'paint2', bevel=0.07)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.5, 10.7, -20.2), (6.5, 10.7, -24.1), (0.6, 10.6, -17.0), (0.6, 10.6, -23.6),
             (6.5, 11.2, -20.2), (6.5, 11.2, -24.1), (0.6, 11.4, -17.0), (0.6, 11.4, -23.6)]], 'paint', bevel=0.06)
    b.box((-0.6, 13.5, -24.0), (0.6, 13.9, -23.0), 'lightr', bevel=0.0)
    # main nozzle (thrustb 0, 5, -20.8 .. -28)
    b.cyl((0, 5.0, -20.6), (0, 5.0, -22.8), 2.4, 12, 'dark', r2=2.0, bevel=0.05)
    b.cyl((0, 5.0, -22.75), (0, 5.0, -22.9), 1.5, 12, 'lightr')
    # belly lift jets (thrusta1/2 at x +-3.8, z 1.2)
    b.cyl((3.8, 0.4, 1.2), (3.8, 0.1, 1.2), 2.0, 12, 'dark', mirror=True)
    b.cyl((3.8, 0.12, 1.2), (3.8, 0.02, 1.2), 1.3, 12, 'lightr', mirror=True)

    # ------------------------------------------------------------------ side sponsons with the panel hinges (mirrored)
    b.hull([(6.4, 3.6, 12.0), (13.9, 4.3, 10.0), (6.4, 6.8, 12.0), (13.9, 6.3, 10.0),
            (6.4, 3.6, -17.0), (13.9, 4.3, -15.7), (6.4, 6.8, -17.0), (13.9, 6.3, -15.7)], 'paint2', bevel=0.16, mirror=True)
    b.box((7.2, 6.7, 6.0), (12.8, 6.85, 9.0), 'dark', bevel=0.0, mirror=True)               # intake grille
    b.box((13.2, 4.0, 9.6), (13.95, 5.0, 10.3), 'lightw', bevel=0.0, mirror=True)
    # twin nano turrets on the rear sponson corners (aimed back-out, toward the beam origin 23.7, 0, -24)
    b.cyl((10.4, 6.2, -12.6), (10.4, 7.6, -12.6), 2.2, 14, 'dark', bevel=0.06, mirror=True)
    b.cyl((10.4, 7.4, -12.6), (12.8, 6.8, -15.8), 1.5, 12, 'hazard', r2=1.3, bevel=0.05, mirror=True)
    b.cyl((12.8, 6.8, -15.8), (14.2, 6.4, -17.8), 1.25, 12, 'steel', r2=0.8, bevel=0.04, mirror=True)
    b.cyl((14.2, 6.4, -17.8), (14.4, 6.35, -18.1), 0.7, 10, 'lightc', mirror=True)

    # ------------------------------------------------------------------ roof doors (door2 at +x; door1 = mirror)
    d = k.piece('door2')
    d.hull([(x, y + dy, z) for x, y in ((0.15, 9.3), (6.0, 8.5)) for z in (15.0, -9.3) for dy in (0.0, 0.32)],
           'team', bevel=0.06)
    d.box((0.6, 9.2, 13.6), (5.4, 9.62, 14.4), 'dark', bevel=0.0)
    d.box((0.6, 9.0, -8.0), (5.4, 9.42, -7.2), 'dark', bevel=0.0)
    k.clone('door1', 'door2', mirror_x=True)

    # ------------------------------------------------------------------ tip panel (wing2 at +x; wing1 = mirror)
    w = k.piece('wing2'); W = w.at
    # landed: vertical; local y = span (0 at hinge, 8.9 at tip), local x 0 = inner face (top in flight)
    out = [(0.0, 13.6), (0.0, -12.0), (6.7, -8.6), (8.9, -7.5), (8.9, -0.6), (6.7, 2.9)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 1.4)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for y, z in [(0.5, 12.6), (0.5, 9.0), (2.6, 7.6), (2.6, 11.2)] for x in (-0.06, 0.1)],
           'hazard', bevel=0.0)
    w.hull([W(x, y, z) for y, z in [(0.6, -11.2), (0.6, -12.0), (8.6, -7.6), (8.6, -6.8)] for x in (-0.04, 0.1)],
           'dark', bevel=0.0)
    w.cyl(W(0.7, -0.3, -12.0), W(0.7, -0.3, 13.0), 0.75, 8, 'dark')                 # hinge barrel
    w.cyl(W(0.7, 9.1, -0.4), W(0.7, 9.1, -7.6), 0.5, 8, 'dark', r2=0.38)
    w.cyl(W(0.7, 9.1, 0.1), W(0.7, 9.1, -0.42), 0.32, 8, 'lightw', r2=0.5)
    k.clone('wing1', 'wing2', mirror_x=True)
