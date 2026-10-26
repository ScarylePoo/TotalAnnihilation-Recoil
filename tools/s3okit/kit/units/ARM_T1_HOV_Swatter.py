"""Swatter (ARM_T1_HOV_Swatter) - Arm anti-air hovercraft. Wide catamaran: two broad pentagonal pontoons on black
skirts, each with a lift fan, and an open launch well between them. The missile `Box` (three big tubes side by side,
team lid) sits low in the well and, on activation, rises ~8, slides forward and tilts up (COB move y/z, turn x),
then turns y to aim. A radar dish on the left pontoon and a sensor mast on the right mark it as the AA unit.
Pieces (TA 3DO): GP (ground plate; its 3DO quad is a shadow plate, dropped), Base (rocks x/z), Box, Flare1..3
(empty emit points at the three tube mouths), Wake1..8 (empty).
Value groups from above: black skirt rails, light Arm pontoons, dark fan discs, dark paint2 well floor, a big
team-coloured lid on the launcher box framed by dark side rails, three black tube mouths.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=6, pose={'Box': (0, 25, 0)}),
    preview_pose={'Box': (-15, -20, 0)},
)

PENT = [(7.5, -24.0), (20.1, -14.4), (23.5, 0.0), (19.9, 13.5), (7.5, 24.0)]


def pent(y, d=0.0):
    out = []
    for x, z in PENT:
        dx, dz = x - 14.0, z
        L = math.hypot(dx, dz) or 1
        out.append((x + dx / L * d, y, z + dz / L * d))
    return out


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ pontoons (+X built, mirrored)
    b.hull(pent(0.6, 0.4) + pent(3.4, 1.8) + pent(6.4, 1.4) + pent(7.6, 0.4), 'tread', bevel=0.28, mirror=True)
    b.hull(pent(7.2, -0.4) + pent(11.6, -0.2) + pent(13.7, -2.0), 'paint', bevel=0.22, mirror=True)
    b.hull(pent(7.4, 0.1) + pent(9.0, 0.2), 'paint2', bevel=0.08, mirror=True)
    # lift fan, aft
    x, z = 14.4, -8.6
    b.cyl((x, 12.8, z), (x, 14.2, z), 4.6, 16, 'dark', bevel=0.12, mirror=True)
    b.cyl((x, 14.2, z), (x, 14.25, z), 3.7, 16, 'black', mirror=True)
    for i in range(5):
        a = i * 2 * math.pi / 5
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for dd in (0.9, 3.5):
            for s in (-0.55, 0.55):
                px, pz = x + ca * dd - sa * s, z + sa * dd + ca * s
                pts += [(px, 13.95, pz), (px, 14.25, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    b.cyl((x, 13.9, z), (x, 14.5, z), 1.0, 10, 'paint', bevel=0.05, mirror=True)
    # team plate on each pontoon bow
    b.hull([(9.2, y, 9.6) for y in (13.72, 13.86)] + [(18.2, y, 9.6) for y in (13.72, 13.86)] +
           [(16.6, y, 13.8) for y in (13.72, 13.86)] + [(9.2, y, 19.8) for y in (13.72, 13.86)], 'team', bevel=0.03, mirror=True)
    # headlights on the pontoon noses
    b.box((10.0, 9.0, 21.4), (12.6, 10.2, 22.2), 'dark', bevel=0.05, mirror=True)
    b.hull([(10.2, 9.2, 22.14), (12.4, 9.2, 21.6), (10.2, 10.0, 22.14), (12.4, 10.0, 21.6),
            (10.2, 9.2, 22.26), (12.4, 9.2, 21.72), (10.2, 10.0, 22.26), (12.4, 10.0, 21.72)], 'lightw', bevel=0.0, mirror=True)
    # inner walls of the launch well (light), bridged fore and aft
    b.box((7.2, 6.8, -21.0), (8.4, 13.7, 21.0), 'paint', bevel=0.12, mirror=True)
    b.box((-7.6, 6.6, -22.0), (7.6, 8.4, 22.4), 'paint2', bevel=0.12)              # well floor / keel
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, 8.4, 13.0), (7.6, 8.4, 22.4), (7.6, 12.6, 14.0), (7.0, 12.6, 19.0), (5.0, 9.4, 23.4)]], 'paint', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, 8.4, -22.0), (7.6, 8.4, -14.0), (7.6, 13.2, -21.4), (7.6, 13.2, -14.6)]], 'paint', bevel=0.16)
    # hazard edge on the forward bridge (launch blast zone)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, 12.62, 14.4), (6.6, 12.62, 16.2), (6.6, 12.74, 14.4), (6.6, 12.74, 16.2)]], 'hazard', bevel=0.02)
    # ------------------------------------------------------------------ AA sensors (asymmetric)
    # radar dish, left pontoon aft
    b.cyl((-17.0, 13.6, 0.0), (-17.0, 17.6, 0.0), 0.8, 10, 'dark', bevel=0.04)
    b.cyl((-17.0, 17.4, 0.0), (-17.0, 18.6, 0.0), 1.6, 12, 'dark', bevel=0.05)
    b.cyl((-17.0, 20.6, -1.2), (-17.0, 20.9, 0.6), 4.2, 18, 'paint', r2=3.2, bevel=0.06)
    b.cyl((-17.0, 20.88, 0.55), (-17.0, 20.93, 0.62), 2.6, 16, 'team')
    b.cyl((-17.0, 18.6, -0.3), (-17.0, 20.7, -0.6), 0.5, 8, 'dark')
    # sensor mast, right pontoon
    b.box((16.4, 13.6, -1.0), (19.0, 15.8, 1.6), 'dark', bevel=0.08)
    b.cyl((17.7, 15.8, 0.3), (17.7, 22.6, 0.3), 0.32, 8, 'steel', r2=0.18)
    b.box((16.2, 21.4, -0.2), (19.2, 21.8, 0.8), 'dark', bevel=0.04)
    b.cyl((17.7, 22.6, 0.3), (17.7, 22.9, 0.3), 0.28, 8, 'lightr')
    # tail lights
    b.box((17.0, 9.8, -19.6), (18.6, 10.6, -19.0), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- Box (origin 0, 13.5, -10.45): launcher
    bx = k.piece('Box'); B = bx.at
    bx.box(B(-6.6, 0.2, -10.2), B(6.6, 6.4, 10.0), 'paint', bevel=0.22)
    bx.box(B(-5.6, 6.35, -9.0), B(5.6, 6.6, 8.0), 'team', bevel=0.05)
    for sx in (-1, 1):
        bx.box(B(min(6.4 * sx, 7.2 * sx), 1.2, -9.4), B(max(6.4 * sx, 7.2 * sx), 5.8, 9.4), 'dark', bevel=0.08)
    # front face: three tube mouths at the flare positions (x -3.5/0/3.5, y 3.0)
    bx.box(B(-6.2, 0.6, 9.9), B(6.2, 5.6, 10.3), 'dark', bevel=0.06)
    for x in (-3.5, 0.0, 3.5):
        bx.cyl(B(x, 3.0, 10.2), B(x, 3.0, 11.2), 1.55, 12, 'steel', bevel=0.04)
        bx.cyl(B(x, 3.0, 11.2), B(x, 3.0, 11.28), 1.1, 12, 'black')
    # rear blast vents
    bx.box(B(-5.6, 1.2, -10.5), B(5.6, 5.2, -10.1), 'black', bevel=0.0)
