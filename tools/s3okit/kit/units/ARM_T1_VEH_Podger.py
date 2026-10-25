"""Podger (ARM_T1_VEH_Podger) - Arm mine layer. Narrow armoured body on four big balloon wheels (Tire1..4 spin x),
low cab in front, tall mine bay at the rear closed by two doors (turn z ~91 deg + drop). When activated the `plate`
lift rises 7.4 elmo through the open bay carrying `post` and the mine `gun` (turn y); `beam` (empty) is the emit
point at the dispenser muzzle.
Value groups from above: light Arm cab/bonnet + bay walls, darker paint2 doors with team stripes, dark wheels
(exaggerated 6.5 radius - they are the unit's silhouette), team plates on the bonnet and mudguard tops,
hazard/black mine-chute markings on the dispenser.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=6, drop=['Tire3'], pose={'door1': (0, 0, -40)}),
    preview_pose={},
)


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ chassis (crosses x = 0)
    b.prism(-5.2, 5.2, [(-25.4, 4.0), (24.0, 4.0), (25.6, 6.4), (25.0, 9.0), (-25.4, 9.0), (-26.0, 6.4)], 'paint2', bevel=0.15)
    # axle beams to the wheels
    for z in (17.6, -18.2):
        b.cyl((-1.0, 6.52, z), (1.0, 6.52, z), 1.3, 10, 'dark')
        b.hull([(4.6, 5.4, z - 1.3), (4.6, 7.6, z - 1.3), (4.6, 5.4, z + 1.3), (4.6, 7.6, z + 1.3),
                (7.9, 5.8, z - 0.9), (7.9, 7.2, z - 0.9), (7.9, 5.8, z + 0.9), (7.9, 7.2, z + 0.9)], 'dark', bevel=0.08, mirror=True)
        # mudguard over the wheel: light shell with a team top
        b.hull([(7.6, 13.6, z - 7.0), (15.2, 13.6, z - 7.0), (7.6, 13.6, z + 7.0), (15.2, 13.6, z + 7.0),
                (7.6, 14.6, z - 4.6), (15.2, 14.6, z - 4.6), (7.6, 14.6, z + 4.6), (15.2, 14.6, z + 4.6)],
               'paint2', bevel=0.12, mirror=True)
        b.hull([(7.6, 9.0, z - 1.0), (8.8, 9.0, z - 1.0), (7.6, 13.6, z - 3.0), (8.8, 13.6, z - 3.0),
                (7.6, 9.0, z + 1.0), (8.8, 9.0, z + 1.0), (7.6, 13.6, z + 3.0), (8.8, 13.6, z + 3.0)], 'dark', bevel=0.06, mirror=True)
    # ------------------------------------------------------------------ cab + bonnet (front)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, 8.8, -1.0), (6.6, 8.8, 23.6), (5.6, 8.6, 25.6),
             (5.6, 12.0, 24.4), (6.0, 12.6, 12.0), (5.6, 16.0, 8.2), (6.0, 16.0, -1.0)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.8, 13.08, 11.6), (4.6, 15.78, 8.6), (4.8, 13.22, 11.66), (4.6, 15.92, 8.66)]], 'glass', bevel=0.03)
    def slope(z):      # bonnet top: the hull runs straight from the nose (y 12, z 24.4) to the cab roof (y 16, z 8.2)
        return 12.0 + 4.0 * (24.4 - z) / 16.2
    # team plate on the bonnet slope, dark bumper
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, slope(22.6) + 0.08, 22.6), (4.6, slope(12.6) + 0.08, 12.6),
             (4.6, slope(22.6) + 0.24, 22.6), (4.6, slope(12.6) + 0.24, 12.6)]], 'team', bevel=0.03)
    b.box((-5.8, 6.6, 25.4), (5.8, 8.4, 26.2), 'dark', bevel=0.05)
    b.box((3.4, 9.4, 24.8), (5.0, 10.6, 25.4), 'dark', bevel=0.05, mirror=True)
    b.box((3.55, 9.55, 25.38), (4.85, 10.45, 25.48), 'lightw', bevel=0.0, mirror=True)
    b.box((-5.4, 16.0, 1.0), (5.4, 16.2, 6.4), 'paint2', bevel=0.04)
    # ------------------------------------------------------------------ mine bay (rear, open-topped under the doors)
    # side walls; inner face at x 4.15 = door hinge line
    b.hull([(4.15, 8.8, -18.6), (6.8, 8.8, -18.6), (4.15, 8.8, -1.8), (6.8, 8.8, -1.8),
            (4.15, 17.6, -18.4), (6.0, 17.6, -18.4), (4.15, 17.6, -2.0), (6.0, 17.6, -2.0)], 'paint', bevel=0.14, mirror=True)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, 8.8, -18.4), (6.6, 8.8, -25.0), (6.0, 17.6, -18.4), (5.6, 16.4, -21.0), (5.6, 10.0, -25.6)]], 'paint', bevel=0.14)
    b.box((-4.2, 8.8, -1.8), (4.2, 16.4, -0.6), 'paint', bevel=0.1)
    b.box((-4.15, 9.0, -18.4), (4.15, 11.0, -2.0), 'dark', bevel=0.0)     # bay floor under the lift
    # rear: mine chute (dark slot with hazard frame) and tail lights
    b.box((-3.6, 9.4, -25.8), (3.6, 13.4, -25.3), 'hazard', bevel=0.05)
    b.box((-2.6, 10.0, -25.95), (2.6, 12.8, -25.7), 'black', bevel=0.0)
    b.box((4.2, 14.0, -24.0), (5.2, 15.0, -23.8), 'lightr', bevel=0.0, mirror=True)
    # amber beacon on the cab roof (mine layer warning light)
    b.cyl((-3.4, 16.0, 4.0), (-3.4, 16.7, 4.0), 0.85, 10, 'dark')
    b.cyl((-3.4, 16.7, 4.0), (-3.4, 17.5, 4.0), 0.6, 10, 'lightw')
    b.cyl((3.4, 16.0, 3.0), (3.4, 16.6, 3.0), 0.34, 8, 'dark')
    b.cyl((3.4, 16.6, 3.0), (3.4, 22.0, 3.0), 0.09, 6, 'steel', r2=0.045)
    b.cyl((3.4, 22.0, 3.0), (3.4, 22.2, 3.0), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- tyres (Tire2 built, the rest cloned)
    t = k.piece('Tire2'); T = t.at
    t.cyl(T(0.2, 0, 0), T(6.4, 0, 0), 6.5, 16, 'tread', rot=math.pi / 16, bevel=0.3)
    t.cyl(T(6.4, 0, 0), T(6.7, 0, 0), 3.6, 12, 'dark', bevel=0.06)
    t.cyl(T(6.7, 0, 0), T(6.95, 0, 0), 1.5, 8, 'steel')
    for i in range(5):     # hub bolts
        a = 2 * math.pi * i / 5
        t.cyl(T(6.7, 2.5 * math.cos(a), 2.5 * math.sin(a)), T(6.95, 2.5 * math.cos(a), 2.5 * math.sin(a)), 0.42, 6, 'black')
    k.clone('Tire4', 'Tire2')
    k.clone('Tire1', 'Tire2', mirror_x=True)
    k.clone('Tire3', 'Tire2', mirror_x=True)

    # ---------------------------------------------------------------- doors (door1 hinge at x -4.05; door2 = mirror)
    d = k.piece('door1'); D = d.at
    d.box(D(0.05, -0.5, -7.9), D(4.1, 0.6, 8.0), 'paint2', bevel=0.1)
    d.box(D(0.6, 0.6, -7.2), D(3.7, 0.76, 7.2), 'team', bevel=0.03)
    d.cyl(D(0.0, 0.0, -7.6), D(0.0, 0.0, 7.6), 0.42, 8, 'dark')
    k.clone('door2', 'door1', mirror_x=True)

    # ---------------------------------------------------------------- plate (lift) + post + mine dispenser gun
    p = k.piece('plate'); Pp = p.at
    p.box(Pp(-4.0, -1.0, -7.8), Pp(4.0, 0.0, 7.8), 'paint2', bevel=0.08)
    for z0 in (-7.6, 6.0):
        p.box(Pp(-3.8, 0.0, z0), Pp(3.8, 0.14, z0 + 1.6), 'hazard', bevel=0.02)
    # three mines racked on the plate (front), dark discs with a red light
    for x in (-2.4, 0.0, 2.4):
        p.cyl(Pp(x, 0.0, 3.6), Pp(x, 0.9, 3.6), 1.05, 10, 'dark', bevel=0.05)
        p.cyl(Pp(x, 0.9, 3.6), Pp(x, 1.05, 3.6), 0.35, 8, 'lightr')
    po = k.piece('post'); O = po.at
    po.cyl(O(0, 0.0, 0), O(0, 0.6, 0), 1.6, 12, 'dark', bevel=0.05)
    po.cyl(O(0, 0.6, 0), O(0, 4.3, 0), 0.9, 10, 'steel', rot=math.pi / 10)
    g = k.piece('gun'); G = g.at
    g.cyl(G(0, -0.4, 0), G(0, 0.2, 0), 1.6, 12, 'dark')
    # dispenser: drum magazine + forward chute ending at the beam point (z 9.68)
    g.cyl(G(0, 0.2, -1.2), G(0, 2.2, -1.2), 2.4, 12, 'paint', rot=math.pi / 12, bevel=0.1)
    g.cyl(G(0, 2.2, -1.2), G(0, 2.36, -1.2), 1.7, 12, 'team')
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.3, -0.6, 0.6), (1.3, 1.6, 0.6), (1.0, -0.6, 9.0), (1.0, 1.0, 9.0)]], 'paint2', bevel=0.08)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 1.56, 2.0), (0.95, 1.06, 8.4), (1.2, 1.7, 2.0), (0.95, 1.2, 8.4)]], 'hazard', bevel=0.02)
    g.box(G(-0.8, -0.4, 9.0), G(0.8, 0.8, 9.6), 'black', bevel=0.0)
