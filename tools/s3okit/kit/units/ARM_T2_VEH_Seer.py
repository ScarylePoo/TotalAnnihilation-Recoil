"""Seer (ARM_T2_VEH_Seer) - Arm mobile radar. Compact tracked carrier with a stepped central superstructure and a
big orange-peel radar reflector on top (dish spins y when active): wider than the hull, it is the unit's identity
from above - a wide light curved band with a team top rim, dark back lattice and a feed horn on a boom.
Value groups from above: the dish (largest light block, team rim), darker paint2 carrier deck, light track guards,
black tracks.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=37, drop=['dish']),
    preview_pose={'dish': (0, -25, 0)},
)


def build(k):
    b = k.piece('base')
    xi, xo = 8.4, 12.6
    belt = [(-13.6, 0.0), (13.0, 0.0), (15.8, 2.6), (15.0, 4.8), (-14.8, 4.8), (-16.2, 2.4)]
    b.prism(xi, xo, belt, 'tread', bevel=0.15, mirror=True)
    for z in (-9.6, -3.2, 3.2, 9.6):
        b.cyl((xo, 1.8, z), (xo + 0.4, 1.8, z), 1.5, 12, 'dark', mirror=True)
        b.cyl((xo + 0.4, 1.8, z), (xo + 0.65, 1.8, z), 0.6, 8, 'steel', mirror=True)
    # track guards (flat, light) with angled front cheeks
    b.hull([(8.0, 6.2, -14.4), (12.8, 6.2, -14.4), (8.0, 6.2, 11.4), (12.8, 6.2, 11.4),
            (8.0, 4.8, 15.8), (12.6, 4.8, 15.4), (8.0, 4.8, -16.0), (12.6, 4.8, -15.6)], 'paint', bevel=0.14, mirror=True)
    b.box((9.0, 6.2, -12.8), (12.0, 6.4, 9.6), 'paint2', bevel=0.04, mirror=True)
    # hull (crosses x = 0)
    b.prism(-8.2, 8.2, [(-15.4, 2.2), (13.8, 2.2), (16.2, 4.6), (15.0, 7.0), (-15.6, 7.0), (-16.2, 4.6)], 'paint2', bevel=0.14)
    # stepped superstructure: lower deck box, upper pedestal
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.0, 7.0, -15.4), (8.0, 7.0, 14.0), (6.4, 9.4, 15.2), (7.0, 10.6, -14.4), (7.0, 10.6, 8.6)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 10.6, -9.4), (5.4, 10.6, 5.4), (4.0, 12.2, -7.6), (4.0, 12.2, 3.8)]], 'paint2', bevel=0.12)
    b.cyl((0, 11.8, -1.5), (0, 12.3, -1.5), 3.0, 16, 'dark', bevel=0.05)
    # instrument racks / generator on the rear deck
    b.box((-6.2, 10.6, -14.6), (-1.0, 12.0, -10.4), 'dark', bevel=0.08)
    for z in (-14.0, -13.0, -12.0, -11.0):
        b.box((-5.8, 12.0, z), (-1.4, 12.12, z + 0.5), 'black', bevel=0.0)
    b.box((1.0, 10.6, -14.6), (6.2, 11.4, -10.4), 'team', bevel=0.05)
    # glacis team chevron (small: the dish rim carries most of the team colour)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 9.5, 14.4), (4.6, 10.62, 9.4), (4.6, 9.64, 14.5), (4.6, 10.76, 9.5)]], 'team', bevel=0.03)
    b.box((-5.0, 5.2, 15.4), (5.0, 6.4, 16.1), 'dark', bevel=0.05)
    b.box((-4.6, 5.4, 16.08), (4.6, 6.2, 16.18), 'lightw', bevel=0.0)
    b.box((-6.0, 7.6, -16.0), (6.0, 10.0, -15.5), 'dark', bevel=0.05)
    b.box((4.4, 8.6, -16.1), (5.6, 9.4, -15.95), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- dish (origin 0, 12.12, -1.5; spins y)
    d = k.piece('dish'); D = d.at
    # mast
    d.cyl(D(0, 0.0, 0), D(0, 3.4, 0), 1.3, 12, 'steel', rot=math.pi / 12)
    d.box(D(-2.0, 2.8, -1.8), D(2.0, 4.4, 1.8), 'dark', bevel=0.08)
    # orange-peel reflector: curved band of panels facing +Z (concave toward the feed)
    R, segs, half = 14.0, 8, math.radians(58)
    y0, y1 = 3.2, 9.8
    zc = 10.0                      # curve centre in front: the band bows back toward the mast
    for i in range(segs):
        a0 = -half + 2 * half * i / segs
        a1 = -half + 2 * half * (i + 1) / segs
        pts = []
        for a in (a0, a1):
            x, z = R * math.sin(a), zc - R * math.cos(a)
            for dz, yy in ((0.0, y0), (0.0, y1), (-0.9, y0 + 0.4), (-0.9, y1 - 0.4)):
                nx, nz = math.sin(a), -math.cos(a)
                pts.append(D(x + nx * (-dz), yy, z + nz * (-dz)))
        d.hull(pts, 'paint', bevel=0.08)
        # team rim along the top edge of each panel
        rim = []
        for a in (a0, a1):
            x, z = R * math.sin(a), zc - R * math.cos(a)
            nx, nz = math.sin(a), -math.cos(a)
            for off in (0.15, 0.75):
                for yy in (y1 - 0.05, y1 + 0.25):
                    rim.append(D(x + nx * off, yy, z + nz * off))
        d.hull(rim, 'team', bevel=0.02)
    # back lattice: dark spars from the mast to the reflector
    for a in (-0.75, 0.0, 0.75):
        x, z = R * math.sin(a), zc - R * math.cos(a)
        d.hull([D(px, py, pz) for px, pz in ((0.0, -0.6), (x * 0.96, z - 0.9)) for py in (4.4, 5.2)] +
               [D(px + 0.4, py, pz) for px, pz in ((0.0, -0.6), (x * 0.96, z - 0.9)) for py in (4.4, 5.2)], 'dark', bevel=0.04)
    # feed horn on a boom in front of the reflector
    d.cyl(D(0, 4.8, -2.0), D(0, 6.4, 6.2), 0.45, 8, 'steel')
    d.cyl(D(0, 6.4, 6.2), D(0, 6.5, 7.6), 0.9, 10, 'dark', r2=0.5, bevel=0.03)
    d.cyl(D(0, 6.5, 7.6), D(0, 6.5, 7.7), 0.4, 8, 'lightc')
