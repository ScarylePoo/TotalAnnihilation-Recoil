"""Jammer (ARM_T2_VEH_Jammer) - Arm mobile radar jammer. Small high-backed tracked carrier (2x2) with a raised cab at the
rear and a long forward boom carrying the jammer rotor: the `fork` spins about Z (the forward axis) when active, so it
is built as a four-armed cross of emitter vanes (always shows a wide bar from above, whatever its spin angle) instead
of TA's thin two-prong fork. `peices` holds the side equipment pods (static).
Value groups from above: light cab and track guards, dark boom, the rotor as the biggest shape: four light vanes with
team-coloured faces and cyan emitter tips around a dark hub; darker paint2 side pods.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=31, drop=['fork']),
    preview_pose={'fork': (0, 0, 45)},
)


def build(k):
    b = k.piece('base')
    xi, xo = 7.6, 12.6
    # belt in two halves: one 30-elmo strip packs diagonally across the UV sheet
    b.prism(xi, xo, [(-0.2, 0.0), (12.6, 0.0), (15.4, 2.6), (14.6, 5.0), (-0.2, 5.0)], 'tread', bevel=0.15, mirror=True)
    b.prism(xi, xo, [(-13.6, 0.0), (0.2, 0.0), (0.2, 5.0), (-14.6, 5.0), (-16.0, 2.4)], 'tread', bevel=0.15, mirror=True)
    for z in (-9.0, -3.0, 3.0, 9.0):
        b.cyl((xi, 1.8, z), (xi - 0.4, 1.8, z), 1.5, 12, 'dark', mirror=True)
        b.cyl((xi - 0.4, 1.8, z), (xi - 0.65, 1.8, z), 0.6, 8, 'steel', mirror=True)
    # track guards: slanted plates (TA's angled side fins)
    b.hull([(7.2, 7.4, -13.6), (13.2, 6.0, -13.6), (7.2, 7.4, -1.0), (13.2, 6.0, -1.0), (7.2, 5.8, -16.0), (12.6, 4.8, -15.6),
            (7.2, 4.8, -13.6), (13.4, 4.8, -13.6), (13.4, 4.8, -1.0), (7.2, 4.8, -1.0)], 'paint', bevel=0.14, mirror=True)
    b.hull([(7.2, 7.4, -1.0), (13.2, 6.0, -1.0), (7.2, 7.4, 12.4), (13.2, 6.0, 12.4), (7.2, 5.6, 16.2), (12.6, 4.6, 15.6),
            (7.2, 4.8, -1.0), (13.4, 4.8, -1.0), (13.4, 4.8, 12.4), (7.2, 4.8, 12.4)], 'paint', bevel=0.14, mirror=True)
    for z0, z1 in ((-12.6, -0.8), (0.8, 11.4)):
        b.hull([(x, y, z) for x, y in ((13.2, 6.0), (13.36, 6.12), (11.8, 6.6), (11.9, 6.74)) for z in (z0, z1)],
               'paint2', bevel=0.03, mirror=True)
    # hull (crosses x = 0): low nose, high box cab at the rear
    b.prism(-7.4, 7.4, [(-15.4, 2.2), (13.6, 2.2), (16.0, 4.6), (15.0, 7.0), (-15.6, 7.0), (-16.2, 4.6)], 'paint2', bevel=0.14)
    # cab block at the rear only: the front deck stays low (y 7) as a well the spinning rotor clears
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 7.0, -15.6), (5.6, 7.0, -1.0), (5.2, 14.6, -2.0), (5.2, 14.6, -12.6), (5.6, 12.0, -15.6)]], 'paint', bevel=0.18)
    # team plate on the cab roof
    b.box((-3.8, 14.6, -11.6), (3.8, 14.82, -5.4), 'team', bevel=0.04)
    # cab visor across the cab front (glass)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.0, 11.6, -1.55), (4.0, 13.8, -1.84), (4.0, 11.6, -1.42), (4.0, 13.8, -1.71)]], 'glass', bevel=0.03)
    # boom mount on the cab front
    b.box((-1.8, 11.8, -2.4), (1.8, 15.0, -0.4), 'dark', bevel=0.1)
    # nose: team chevron on the low glacis, dark rotor-well floor plates
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 5.62, 15.1), (4.2, 6.96, 13.9), (4.2, 5.76, 15.2), (4.2, 7.1, 14.0)]], 'team', bevel=0.03)
    b.box((-6.0, 7.0, 0.0), (6.0, 7.2, 11.6), 'dark', bevel=0.04)
    # headlights, tail
    b.box((-4.4, 5.0, 15.2), (4.4, 6.2, 15.9), 'dark', bevel=0.05)
    b.box((-4.0, 5.2, 15.88), (4.0, 6.0, 15.98), 'lightw', bevel=0.0)
    b.box((-5.0, 8.0, -15.95), (5.0, 12.0, -15.5), 'dark', bevel=0.05)
    b.box((3.4, 10.6, -16.05), (4.6, 11.4, -15.9), 'lightr', bevel=0.0, mirror=True)
    # whip aerials on the cab corners
    for x in (-4.4, 4.4):
        b.cyl((x, 14.6, -14.0), (x, 15.2, -14.0), 0.3, 8, 'dark')
        b.cyl((x, 15.2, -14.0), (x, 20.0, -14.0), 0.09, 6, 'steel', r2=0.045)
        b.cyl((x, 20.0, -14.0), (x, 20.2, -14.0), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- peices: side equipment pods (static)
    p = k.piece('peices')
    p.hull([(x, y, z) for x in (5.4, 7.6) for y, z in
            [(4.6, -12.0), (8.8, -11.0), (4.6, -2.0), (8.4, -2.0)]], 'paint2', bevel=0.1, mirror=True)
    p.box((7.5, 5.6, -10.4), (7.8, 7.6, -3.4), 'dark', bevel=0.02, mirror=True)
    p.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.0, 7.0, 13.4), (4.0, 7.0, 15.6), (3.0, 9.4, 13.0), (3.0, 8.4, 15.0)]], 'paint2', bevel=0.08)

    # ---------------------------------------------------------------- fork: jammer rotor (spins z)
    f = k.piece('fork'); F = f.at
    f.cyl(F(0, 0, -0.6), F(0, 0, 16.0), 0.8, 10, 'dark', bevel=0.04)           # boom shaft
    f.cyl(F(0, 0, 6.2), F(0, 0, 11.0), 2.2, 12, 'dark', bevel=0.08)            # rotor hub
    f.cyl(F(0, 0, 15.4), F(0, 0, 17.0), 1.3, 10, 'paint2', r2=0.6, bevel=0.04)
    f.cyl(F(0, 0, 17.0), F(0, 0, 17.2), 0.5, 8, 'lightc')
    for a in range(4):
        ang = a * math.pi / 2 + math.pi / 4
        c, s = math.cos(ang), math.sin(ang)
        def P(r, t, z):     # r along the arm, t across it (perpendicular, in the XY plane)
            return F(c * r - s * t, s * r + c * t, z)
        # strut
        f.hull([P(r, t, z) for r in (1.6, 2.6) for t in (-0.45, 0.45) for z in (7.0, 10.2)], 'dark', bevel=0.05)
        # emitter vane: wide flat blade, light, with a team face (max radius 6.2: clears the deck at y 7 when spinning)
        f.hull([P(r, t, z) for r in (2.4, 5.8) for t in (-0.55, 0.55) for z in (3.0, 15.0)], 'paint', bevel=0.1)
        f.hull([P(r, t, z) for r in (2.9, 5.4) for t in (0.55, 0.71) for z in (4.4, 13.6)], 'team', bevel=0.02)
        f.hull([P(r, t, z) for r in (5.8, 6.15) for t in (-0.35, 0.35) for z in (4.0, 14.0)], 'lightc', bevel=0.0)
