"""Jeffy (ARM_T1_VEH_Jeffy) - Arm fast scout buggy. Narrow wedge body, four big outrigger wheels on struts
(part of `base`: the TA model never spun them), a small twin machine-gun mount on the roof (`gun`: turns x+y).
Value groups from above: light Arm body wedge, dark wheels/struts/engine (they frame the body), team stripe
down the spine + gun roof, hazard nose. The wheels are exaggerated slightly so the 4-wheel stance reads.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=7, pose={'gun': (12, 40, 0)}),
    preview_pose={'gun': (0, -20, 0)},
)

WX, WR, WW = 11.6, 4.2, 3.4       # wheel centre x, radius, width
WZ = (10.6, -10.2)                # front / rear axle z


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ wheels (static, outriggers)
    for z in WZ:
        x0, x1 = WX - WW / 2, WX + WW / 2
        b.cyl((x0, WR, z), (x1, WR, z), WR, 16, 'tread', rot=math.pi / 16, bevel=0.15, mirror=True)
        b.cyl((x1, WR, z), (x1 + 0.25, WR, z), 2.3, 12, 'dark', bevel=0.05, mirror=True)
        b.cyl((x1 + 0.25, WR, z), (x1 + 0.45, WR, z), 0.9, 8, 'steel', mirror=True)
        # strut from the body to the hub
        b.hull([(4.0, 5.2, z - 0.9), (4.0, 6.6, z - 0.9), (4.0, 5.2, z + 0.9), (4.0, 6.6, z + 0.9),
                (x0, WR - 0.5, z - 0.6), (x0, WR + 0.6, z - 0.6), (x0, WR - 0.5, z + 0.6), (x0, WR + 0.6, z + 0.6)],
               'dark', bevel=0.08, mirror=True)
        # mudguard over each wheel: light top plate, team-coloured top (reads from above)
        b.hull([(x0 - 0.3, WR + 3.3, z - 3.6), (x1 + 0.4, WR + 3.3, z - 3.6), (x0 - 0.3, WR + 3.3, z + 3.6), (x1 + 0.4, WR + 3.3, z + 3.6),
                (x0 - 0.3, WR + 4.6, z - 2.4), (x1 + 0.4, WR + 4.6, z - 2.4), (x0 - 0.3, WR + 4.6, z + 2.4), (x1 + 0.4, WR + 4.6, z + 2.4)],
               'paint', bevel=0.12, mirror=True)
        b.box((x0 + 0.2, WR + 4.6, z - 2.0), (x1 - 0.1, WR + 4.76, z + 2.0), 'team', bevel=0.04, mirror=True)

    # ------------------------------------------------------------------ body (crosses x = 0)
    # chassis pan, darker
    b.prism(-4.6, 4.6, [(-15.6, 2.6), (14.0, 2.6), (16.0, 4.4), (15.0, 5.6), (-15.4, 5.6), (-16.0, 4.0)], 'paint2', bevel=0.15)
    # main wedge: low pointed nose rising to the cabin
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.8, 5.4, -15.0), (4.8, 5.4, 12.0), (2.0, 5.0, 16.4),
             (4.4, 8.6, -14.2), (4.2, 10.4, -7.8), (4.0, 10.4, -2.0), (3.0, 7.2, 8.0), (1.4, 6.0, 14.8)]], 'paint', bevel=0.16)
    # hazard nose tip
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 5.1, 16.3), (2.6, 6.55, 13.2), (1.8, 5.23, 16.42), (2.6, 6.68, 13.32)]], 'hazard', bevel=0.03)
    # team stripe down the spine (front deck)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 7.08, 7.6), (1.0, 6.0, 13.6), (1.9, 9.75, -1.6),
             (1.6, 7.24, 7.62), (1.0, 6.16, 13.62), (1.9, 9.91, -1.58)]], 'team', bevel=0.03)
    # cabin glass, front of the gun mount
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 8.5, 3.6), (3.4, 10.45, -1.4), (3.0, 8.62, 3.7), (3.0, 10.57, -1.3)]], 'glass', bevel=0.03)
    # rear engine block: dark, with exhausts
    b.box((-3.6, 8.5, -15.2), (3.6, 9.6, -11.0), 'dark', bevel=0.1)
    for z in (-14.6, -13.7, -12.8, -11.9):
        b.box((-3.2, 9.6, z), (3.2, 9.74, z + 0.42), 'black', bevel=0.0)
    b.cyl((3.0, 6.2, -15.6), (3.0, 7.0, -16.6), 0.55, 10, 'dark', mirror=True)
    b.cyl((3.0, 7.0, -16.6), (3.0, 7.1, -16.72), 0.38, 10, 'black', mirror=True)
    # headlights
    b.box((2.4, 4.6, 14.6), (4.0, 5.5, 15.3), 'dark', bevel=0.06, mirror=True)
    b.box((2.55, 4.75, 15.28), (3.85, 5.35, 15.38), 'lightw', bevel=0.0, mirror=True)
    b.box((2.6, 6.8, -15.75), (3.8, 7.4, -15.55), 'lightr', bevel=0.0, mirror=True)
    # whip antenna, rear left (long: it is the scout's tell)
    b.cyl((-3.6, 9.4, -13.0), (-3.6, 10.1, -13.0), 0.34, 8, 'dark')
    b.cyl((-3.6, 10.1, -13.0), (-3.6, 17.5, -13.0), 0.1, 6, 'steel', r2=0.045)
    b.cyl((-3.6, 17.5, -13.0), (-3.6, 17.7, -13.0), 0.15, 6, 'lightc')

    # ---------------------------------------------------------------- gun (origin 0, 10.61, -6.57; turns x and y)
    g = k.piece('gun'); G = g.at
    g.cyl(G(0, -0.25, 0), G(0, 0.4, 0), 2.6, 14, 'dark', bevel=0.05)
    # mount housing between the two guns
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.1, 0.4, -2.2), (1.1, 0.4, 2.6), (1.0, 2.9, -1.8), (1.0, 2.9, 1.8)]], 'paint', bevel=0.1)
    g.box(G(-0.85, 2.88, -1.5), G(0.85, 3.04, 1.4), 'team', bevel=0.03)
    # twin gun bodies + barrels (bore axis at x +-1.75, y 1.97 from the flare offsets)
    for sx in (1,):
        g.box(G(1.05, 1.15, -2.0), G(2.45, 2.8, 2.6), 'paint2', bevel=0.08, mirror=True)
        g.cyl(G(1.75, 1.97, 2.5), G(1.75, 1.97, 6.6), 0.42, 8, 'dark', rot=math.pi / 8, mirror=True)
        g.cyl(G(1.75, 1.97, 3.6), G(1.75, 1.97, 5.2), 0.58, 8, 'dark', rot=math.pi / 8, bevel=0.03, mirror=True)
        g.cyl(G(1.75, 1.97, 6.55), G(1.75, 1.97, 6.9), 0.55, 8, 'steel', rot=math.pi / 8, mirror=True)
        g.cyl(G(1.75, 1.97, 6.88), G(1.75, 1.97, 6.94), 0.25, 8, 'black', mirror=True)
    g.box(G(-0.5, 1.6, 2.58), G(0.5, 2.2, 2.7), 'lightc', bevel=0.0)
