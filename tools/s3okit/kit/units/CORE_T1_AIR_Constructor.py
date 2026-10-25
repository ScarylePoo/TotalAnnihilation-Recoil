"""Construction Aircraft (CORE_T1_AIR_Constructor) - Core T1 air builder. A slab-sided box fuselage whose roof is a
pair of armoured bay doors (doora/doorb, hinged at the outer edges, meeting on the centre line) over the nano bay,
short stub wings to the hinges at x +-14.5 and Core's fold-out tip panels (winga/wingb) that stand up when landed and
fold out 90 deg in flight. A heavy nano projector sits in a chin turret under the nose (the build beam starts at the
base's first vertex, at the front-right as in TA); a single tall fin on a short tail boom.
From above: a long dark box with two bright team doors down the middle - unlike the arrow fighters, the
straight-winged Fink or the broad Shadow.
Pieces (TA layout): base, doora/doorb (roof doors; doora = mirrored clone of doorb), winga/wingb (tip panels; winga =
mirrored clone of wingb), thrusta1/thrusta2/thrustb (empty emit points: two belly lift jets + main nozzle).
Value groups from above: dark warm armour, team doors (plus a thin trailing stripe on the tip panels), darker paint2 wing panels/tail, light steel nano projector and
door hinges, ochre hazard on the projector shroud and wing roots.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=29, drop=['doora'], pose={'winga': (0, 0, 40)}),
    preview_pose={'winga': (0, 0, 90.1), 'wingb': (0, 0, -90.1)},   # flight: tip panels folded out
)

WY = 4.0


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ box fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 2.6, 24.4), (1.4, 6.0, 24.2), (3.8, 1.2, 18.0), (4.2, 8.2, 16.0),
             (6.0, 0.4, 12.0), (6.0, 8.9, 12.0), (6.0, 0.4, -12.0), (6.0, 8.9, -12.0),
             (3.6, 2.8, -20.0), (3.4, 9.0, -21.6)]], 'paint', bevel=0.2, seg=2)
    # door coaming: dark rim around the bay
    b.box((-5.6, 8.85, -11.6), (5.6, 9.2, 12.4), 'paint2', bevel=0.1)
    b.box((-4.7, 9.15, -10.9), (4.7, 9.3, 11.8), 'black', bevel=0.0)
    # cockpit glazing on the nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 6.2, 24.0), (3.6, 7.6, 18.0), (3.0, 9.0, 15.0), (1.3, 6.4, 23.9)]] +
           [(x * sx, y + 0.12, z + 0.1) for sx in (-1, 1) for x, y, z in [(3.6, 7.6, 18.0), (3.0, 9.0, 15.0)]], 'glass', bevel=0.05)
    # tail boom + single tall fin
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 7.2, -18.0), (2.0, 9.6, -18.0), (1.2, 7.8, -25.0), (1.2, 9.6, -25.0)]], 'paint2', bevel=0.1)
    b.hull([(x, y, z) for x in (-0.6, 0.6) for y, z in ((9.4, -16.6), (9.4, -24.8), (16.7, -21.0), (16.7, -25.4))],
           'paint2', bevel=0.08)
    b.box((-0.65, 16.2, -25.2), (0.65, 16.9, -24.2), 'lightr', bevel=0.0)
    b.cyl((0, 8.4, -24.4), (0, 8.4, -26.2), 1.3, 10, 'dark', r2=1.0, bevel=0.03)        # main nozzle (thrustb)
    b.cyl((0, 8.4, -26.15), (0, 8.4, -26.3), 0.8, 10, 'lightr')
    # belly lift jets (thrusta1/2 at x +-2.9, z 8.4)
    b.cyl((2.9, 0.9, 8.4), (2.9, 0.2, 8.4), 1.6, 12, 'dark', r2=1.4, bevel=0.03, mirror=True)
    b.cyl((2.9, 0.2, 8.4), (2.9, 0.1, 8.4), 1.0, 12, 'lightr', mirror=True)

    # ------------------------------------------------------------------ stub wings to the tip hinges (mirrored)
    pts = []
    for x, zl, zt, t in ((5.6, 14.0, -15.6, 0.9), (14.5, 6.4, -17.1, 0.6)):
        for z, tt in ((zl, 0.12), (zl - 2.0, t), (zt + 1.2, t * 0.8), (zt, 0.1)):
            pts += [(x, WY + tt, z), (x, WY - tt, z)]
    b.hull(pts, 'paint', bevel=0.08, mirror=True)
    b.hull([(x, WY + t + 0.05, z) for x, t in ((6.6, 0.9), (13.6, 0.62)) for z in (11.6, 4.6)] +
           [(x, WY + t + 0.16, z) for x, t in ((6.6, 0.9), (13.6, 0.62)) for z in (11.6, 4.6)], 'hazard', bevel=0.02, mirror=True)
    b.box((13.6, 3.2, -16.6), (14.5, 4.8, 6.0), 'paint2', bevel=0.1, mirror=True)       # hinge block

    # ------------------------------------------------------------------ chin nano turret (beam origin = base vert 0, front right)
    b.cyl((0, 1.2, 15.0), (0, -0.4, 15.0), 3.0, 14, 'dark', bevel=0.06)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, -0.4, 12.8), (2.4, -2.6, 13.4), (1.8, -0.6, 18.4), (1.8, -2.2, 18.2)]], 'hazard', bevel=0.08)
    b.cyl((0, -1.4, 17.6), (0, -1.4, 22.6), 1.0, 10, 'steel', r2=0.8, rot=math.pi / 10)
    for z in (19.0, 20.6):
        b.cyl((0, -1.4, z), (0, -1.4, z + 0.5), 1.25, 10, 'dark', rot=math.pi / 10)
    b.cyl((0, -1.4, 22.6), (0, -1.4, 23.0), 0.7, 10, 'lightc')

    # ------------------------------------------------------------------ roof doors (doorb at +x hinges on its edge; doora = mirror)
    d = k.piece('doorb'); D = d.at
    d.hull([D(x, y, z) for x in (-4.8, 0.2) for z in (-10.9, 10.7) for y in ((0.05, 0.75) if x > -1 else (0.95, 1.55))],
           'paint2', bevel=0.08)
    d.hull([D(x, y, z) for x in (-4.0, -0.6) for z in (-9.4, 9.2) for y in
            ((0.75 + (0.2 - x) * 0.16 + 0.05, 0.75 + (0.2 - x) * 0.16 + 0.17))], 'team', bevel=0.02)
    d.cyl(D(0.3, 0.2, -10.6), D(0.3, 0.2, 10.4), 0.45, 8, 'steel')                 # hinge
    k.clone('doora', 'doorb', mirror_x=True)

    # ------------------------------------------------------------------ tip panel (wingb at +x; winga = mirror)
    w = k.piece('wingb'); W = w.at
    out = [(0.0, 12.4), (0.0, -11.1), (14.2, -16.0), (13.8, -5.3)]
    w.hull([W(x, y, z) for y, z in out for x in (-1.0, -0.1)], 'paint2', bevel=0.08)   # outer face = underside in flight
    w.hull([W(x, y, z) for y, z in [(1.4, -6.8), (1.4, -9.6), (12.6, -13.8), (12.6, -11.8)] for x in (-1.1, -0.95)], 'team', bevel=0.02)
    w.cyl(W(-0.55, 14.0, -5.0), W(-0.55, 14.0, -16.2), 0.55, 8, 'dark', r2=0.42)
    w.cyl(W(-0.55, 14.0, -4.6), W(-0.55, 14.0, -5.02), 0.34, 8, 'lightw', r2=0.55)
    w.cyl(W(-0.55, -0.4, -10.8), W(-0.55, -0.4, 12.0), 0.65, 8, 'dark')             # hinge barrel
    k.clone('winga', 'wingb', mirror_x=True)
