"""Peeper (ARM_T1_AIR_Peeper) - Arm air scout. Small, light delta: a slim dark fuselage pod, thin light wings with
up-turned outer panels, and an AWACS-style rotodome on a pylon over the fuselage (the scout's tell from above).
Pieces (TA layout, the COB drives them): base (fuselage + inner wing), wingp1/wingp2 (empty pivots at the inner trailing
corner of the outer wing panels; turn y ~51 deg to fold the panels forward on landing), wing1/wing2 (outer panels,
turn x a few degrees as flaps). wing2 = mirrored clone of wing1.
Value groups from above: light Arm wings (paint), dark paint2 fuselage spine + rotodome, near-black engine/intakes,
team-coloured wing tips and a team band across the dome.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=5, pose={'wingp1': (0, 40, 0), 'wingp2': (0, -15, 0)}),
    preview_pose={'wingp1': (0, 51.6, 0), 'wingp2': (0, -51.2, 0), 'wing1': (-8.6, 0, 0), 'wing2': (-8.1, 0, 0)},   # flight pose
)

XR = 6.92          # wing fold pivot x (wingp1 origin)
ZT = -10.27        # trailing edge z


def lead_z(x):     # wing leading edge z at span position x (straight delta edge)
    return 8.6 - (x - 2.4) * (8.6 + 6.6) / (16.0 - 2.4)


def wy(x):         # wing mid-surface height (dihedral grows outboard)
    return 3.9 if x <= XR else 3.9 + (x - XR) * 0.26


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fuselage pod (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.5, 3.6, 16.6), (1.3, 2.6, 13.0), (2.4, 2.4, 6.0), (2.5, 2.6, -8.0), (1.8, 3.0, -12.4),
             (1.1, 4.8, 15.2), (1.9, 5.8, 9.0), (2.3, 6.2, 0.0), (2.0, 5.8, -8.0), (1.4, 5.0, -12.2)]], 'paint2', bevel=0.16)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.0, 5.4, 12.8), (1.4, 6.0, 9.0), (1.4, 6.1, 5.4), (0.5, 6.9, 9.4), (0.5, 6.9, 6.2), (0.8, 6.0, 4.2)]], 'glass', bevel=0.08)
    # nose sensor tip
    b.cyl((0, 3.7, 16.4), (0, 3.7, 17.6), 0.55, 10, 'dark', r2=0.25)
    # engine: dark nacelle tail with a cool glow ring
    b.cyl((0, 4.1, -11.0), (0, 4.1, -13.4), 1.55, 12, 'dark', r2=1.35, bevel=0.05)
    b.cyl((0, 4.1, -13.35), (0, 4.1, -13.5), 1.05, 12, 'lightc')
    # side intakes
    b.hull([(x, y, z) for x, y, z in
            [(2.3, 3.0, 4.0), (3.4, 3.0, 3.2), (2.3, 5.2, 4.0), (3.2, 5.0, 3.2),
             (2.3, 3.1, -3.0), (3.4, 3.1, -3.0), (2.3, 5.0, -3.0), (3.2, 4.9, -3.0)]], 'paint2', bevel=0.1, mirror=True)
    b.box((2.5, 3.3, 3.9), (3.15, 4.8, 4.05), 'black', bevel=0.0, mirror=True)
    # inner wing (fuselage to the fold line), thin, light
    xs = (2.2, XR + 0.15)
    pts = []
    for x in xs:
        zl = lead_z(x) - (0.0 if x > 3 else 0.0)
        for z, t in ((zl, 0.15), (zl - 1.6, 0.42), (ZT + 0.6, 0.3), (ZT, 0.1)):
            pts += [(x, wy(x) + t, z), (x, wy(x) - t, z)]
    b.hull(pts, 'paint', bevel=0.06, mirror=True)
    # dark wing-root walkway strip (separates fuselage from wing at distance)
    b.hull([(x, wy(x) + dy, z) for x in (2.3, 3.6) for z in (lead_z(3.6) - 1.4, ZT + 1.0) for dy in (0.43, 0.5)],
           'dark', bevel=0.0, mirror=True)
    # twin tail fins canted out
    b.hull([(2.0, 5.2, -6.4), (2.0, 5.2, -12.0), (2.2, 4.6, -12.4), (2.2, 4.6, -6.0),
            (3.4, 9.8, -10.4), (3.4, 9.8, -12.6), (3.6, 9.8, -12.6), (3.6, 9.8, -10.4)], 'paint', bevel=0.08, mirror=True)
    b.hull([(3.37, 9.8, -10.5), (3.37, 9.8, -12.5), (3.0, 8.4, -10.1), (3.0, 8.4, -12.4),
            (3.65, 9.84, -10.5), (3.65, 9.84, -12.5), (3.3, 8.44, -10.1), (3.3, 8.44, -12.4)], 'team', bevel=0.0, mirror=True)
    b.box((3.35, 9.8, -11.9), (3.65, 10.1, -11.5), 'lightr', bevel=0.0, mirror=True)
    # rotodome on a pylon (the scout identity)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.35, 5.8, 1.4), (0.35, 5.8, -4.4), (0.3, 8.0, -0.4), (0.3, 8.0, -2.8)]], 'dark', bevel=0.05)
    b.cyl((0, 7.9, -1.6), (0, 8.5, -1.6), 4.1, 20, 'paint2', r2=4.4, bevel=0.06)
    b.cyl((0, 8.5, -1.6), (0, 9.1, -1.6), 4.4, 20, 'paint2', r2=3.6, bevel=0.06)
    b.box((-3.7, 9.08, -2.4), (3.7, 9.2, -0.8), 'team', bevel=0.02)
    b.cyl((0, 9.1, -1.6), (0, 9.3, -1.6), 0.7, 10, 'lightc')

    # ------------------------------------------------------------------ outer wing panel (wing1; wing2 = mirror clone)
    w = k.piece('wing1')
    xs = (XR - 0.1, 16.2)
    pts = []
    for x in xs:
        zl = lead_z(x)
        t0 = 0.36 if x < 10 else 0.2
        for z, t in ((zl, 0.12), (zl - 1.2, t0), (ZT + 0.5, t0 * 0.7), (ZT, 0.08)):
            pts += [(x, wy(x) + t, z), (x, wy(x) - t, z)]
    w.hull(pts, 'paint', bevel=0.05)
    # team wing tip: wide plate on the outer third
    x0, x1 = 11.6, 15.8
    w.hull([(x, wy(x) + dy, z) for x in (x0, x1) for z in (lead_z(x) - 0.5, ZT + 0.6) for dy in (0.3, 0.38)],
           'team', bevel=0.02)
    # tip pod with a nav light
    w.cyl((16.2, wy(16.2), -4.6), (16.2, wy(16.2), -11.0), 0.5, 8, 'dark', r2=0.4)
    w.cyl((16.2, wy(16.2), -4.0), (16.2, wy(16.2), -4.62), 0.3, 8, 'lightw', r2=0.5)
    k.clone('wing2', 'wing1', mirror_x=True)
