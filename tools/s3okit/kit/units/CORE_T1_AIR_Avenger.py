"""Avenger (CORE_T1_AIR_Avenger) - Core T1 fighter. Sharp arrowhead: a pointed nose, a short swept wing to the
fold line at x +-13.5 and Core's signature tip panels (winga/wingb) that stand vertical when landed and fold OUT
91 deg in flight (COB turn z), doubling the span to a narrow, swept 49-elmo arrow. Two tall canted tail fins and two
light steel missile rails slung beside the fuselage, their noses ahead of the wing (light-on-dark read of a gunship).
Pieces (TA layout): base, winga/wingb (tip panels; winga = mirrored clone of wingb), missle1/missle2 (empty launch
points), thrusta1/thrusta2/thrustb (empty engine emit points).
The tip panel's inner face becomes its top in flight, so team colour sits on that face (the fighter's team read is
two long swept stripes out at the tips) and the outer face is dark.
Value groups from above: dark warm armour (paint), darker paint2 spine/fins/flaps, light steel missiles and intake
rims, ochre hazard nose chevron, team on the tip panels.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=21, drop=['winga'], pose={'wingb': (0, 0, -40)}),
    preview_pose={'winga': (0, 0, 91.2), 'wingb': (0, 0, -91.2)},    # flight: tip panels folded out
)

WY = 2.7       # wing mid-plane


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 2.2, 17.2), (0.3, 1.6, 16.6),
             (2.2, 0.8, 9.0), (2.6, 4.4, 8.4),
             (4.0, 0.4, 0.0), (3.6, 6.2, 0.0),
             (3.8, 0.4, -12.0), (2.8, 6.8, -11.0),
             (3.4, 0.6, -15.6), (2.0, 5.6, -15.4)]], 'paint', bevel=0.16)
    # dark spine from the canopy to the tail
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 6.3, -1.0), (1.4, 6.85, -11.2), (1.4, 6.5, -1.0), (1.4, 7.05, -11.2), (0.8, 6.0, 1.2), (0.8, 6.2, 1.2)]],
           'paint2', bevel=0.04)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 4.0, 10.8), (2.2, 5.4, 6.4), (2.0, 6.0, 1.8), (0.8, 6.9, 5.0), (0.8, 6.9, 2.4), (0.8, 5.2, 9.2)]], 'glass', bevel=0.08)
    # ochre hazard chevron on the nose (Core accent)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.4, 2.36, 16.4), (1.9, 3.5, 11.4), (0.4, 2.48, 16.5), (1.9, 3.62, 11.5), (0.6, 3.9, 11.0), (0.6, 4.02, 11.1)]],
           'hazard', bevel=0.02)

    # ------------------------------------------------------------------ swept main wing (mirrored)
    pts = []
    for x, zl, zt, t in ((3.6, 8.6, -12.6, 0.55), (13.5, 0.9, -12.9, 0.4)):
        for z, tt in ((zl, 0.1), (zl - 1.6, t), (zt + 1.0, t * 0.8), (zt, 0.08)):
            pts += [(x, WY + tt, z), (x, WY - tt, z)]
    b.hull(pts, 'paint', bevel=0.06, mirror=True)
    # trailing-edge flap strip
    b.hull([(x, WY + d, z) for x in (5.0, 13.0) for z in (-10.2, -12.6) for d in (0.36, 0.46)], 'paint2', bevel=0.0, mirror=True)
    # light steel leading-edge strip (catches light, outlines the arrow from above)
    b.hull([(x, WY + d, z) for x, z in ((4.8, 7.6), (13.3, 1.0), (13.3, -0.6), (4.8, 5.6)) for d in (0.4, 0.5)], 'steel', bevel=0.0, mirror=True)
    # tip hinge block (winga/wingb pivot at x 13.5, y 3.12)
    b.box((12.6, 1.9, -12.4), (13.5, 3.5, 1.0), 'paint2', bevel=0.1, mirror=True)

    # ------------------------------------------------------------------ intakes + missile rails (missle points 6.75, 1.38, 4)
    b.hull([(4.0, 0.6, 6.0), (6.4, 0.6, 5.0), (4.0, 3.8, 6.0), (6.0, 3.4, 5.0),
            (3.8, 0.6, -8.0), (6.4, 0.8, -8.0), (3.6, 4.4, -8.0), (6.0, 3.6, -8.0)], 'paint2', bevel=0.12, mirror=True)
    b.hull([(4.2, 0.9, 6.1), (6.2, 0.9, 5.1), (4.2, 3.5, 6.1), (5.8, 3.2, 5.1),
            (4.2, 0.9, 5.8), (6.2, 0.9, 4.8), (4.2, 3.5, 5.8), (5.8, 3.2, 4.8)], 'black', bevel=0.0, mirror=True)
    b.cyl((4.0, 2.2, 6.1), (6.5, 2.2, 5.1), 0.25, 6, 'steel', mirror=True)
    # over-wing missile rails (light steel on the dark wing: the gunship read from above; launch points stay at the
    # TA missle1/2 emit positions under them)
    my = WY + 1.65
    b.box((6.0, WY + 0.4, -7.0), (7.5, my - 0.5, 4.0), 'dark', bevel=0.06, mirror=True)          # pylon
    b.cyl((6.75, my, -8.4), (6.75, my, 6.0), 0.95, 8, 'steel', rot=math.pi / 8, mirror=True)
    b.cyl((6.75, my, 6.0), (6.75, my, 9.0), 0.95, 8, 'steel', r2=0.15, rot=math.pi / 8, mirror=True)
    b.cyl((6.75, my, 6.4), (6.75, my, 6.9), 1.0, 8, 'lightr', rot=math.pi / 8, mirror=True)
    b.box((4.95, my - 0.08, -8.4), (8.55, my + 0.08, -6.0), 'dark', bevel=0.0, mirror=True)       # tail fins
    b.box((6.67, my - 1.8, -8.4), (6.83, my + 1.8, -6.0), 'dark', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ twin canted tail fins + engines
    b.hull([(1.6, 5.4, -8.0), (2.0, 5.0, -15.4), (5.8, 13.5, -13.4), (5.8, 13.5, -17.9),
            (2.2, 5.0, -8.0), (2.6, 4.6, -15.4), (6.3, 13.4, -13.4), (6.3, 13.4, -17.9)], 'paint2', bevel=0.07, mirror=True)
    b.box((5.6, 13.3, -17.7), (6.5, 13.8, -16.8), 'lightr', bevel=0.0, mirror=True)
    for x in (2.3,):
        b.cyl((x, 1.6, -13.4), (x, 1.6, -16.0), 1.35, 12, 'steel', r2=1.15, bevel=0.04, mirror=True)
        b.cyl((x, 1.6, -15.95), (x, 1.6, -16.1), 0.85, 12, 'lightr', mirror=True)
    b.cyl((0, 3.0, -14.2), (0, 3.0, -16.0), 1.0, 10, 'dark', r2=0.8, bevel=0.03)
    b.cyl((0, 3.0, -15.95), (0, 3.0, -16.1), 0.6, 10, 'lightr')

    # ------------------------------------------------------------------ tip panel (wingb at +x; winga = mirror clone)
    w = k.piece('wingb'); W = w.at
    # landed: vertical, standing up from the hinge; local x 0 = inner face (top in flight)
    out = [(0.0, 6.7), (0.0, -9.3), (11.0, -9.3), (11.0, -3.9)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 0.8)], 'paint', bevel=0.06)
    w.hull([W(x, y, z) for y, z in [(1.0, 4.4), (1.0, -7.6), (10.2, -8.0), (10.2, -4.6)] for x in (-0.08, 0.06)], 'team', bevel=0.02)
    w.hull([W(x, y, z) for y, z in [(0.6, -7.8), (0.6, -9.2), (10.8, -9.2), (10.8, -8.3)] for x in (-0.04, 0.06)], 'paint2', bevel=0.0)
    w.cyl(W(0.4, 11.0, -3.6), W(0.4, 11.0, -9.6), 0.45, 8, 'dark', r2=0.35)
    w.cyl(W(0.4, 11.0, -3.2), W(0.4, 11.0, -3.62), 0.28, 8, 'lightw', r2=0.45)
    w.cyl(W(0.4, -0.4, -9.0), W(0.4, -0.4, 6.0), 0.55, 8, 'dark')                     # hinge barrel
    k.clone('winga', 'wingb', mirror_x=True)
