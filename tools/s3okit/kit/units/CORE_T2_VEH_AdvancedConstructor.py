"""Advanced Construction Vehicle (CORE_T2_VEH_AdvancedConstructor) - Core T2 builder. A tall armoured tower on two
long track pods with a low raked cab ahead of it: the tower is a hollow shaft (x +-9.5, z -18.7..11.3, y 5..24) closed
by two roof doors. Build sequence (COB activatescr): door1/door2 swing open ~207 deg (turn z) and fold down over the
tower sides, the telescopic `stand` rises 10.25 out of the shaft and the nano `gun` a further 1.75; `turret` (the
stand's base collar) traverses; `beam` (empty) is the nano emit point at the gun tip.
Distinct from the Arm T2 builder (wing armour, crane arm on a lift plate): a Core tower-and-mast silhouette, the doors
carry a broad team chevron, ochre hazard lips on the shaft mouth, a big nano projector with a red emitter.
Value groups from above: two team doors over a dark warm tower (closed) / a dark shaft with a light steel projector
(open), paint2 track pods, black treads, ochre hazard trims.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=83, pose={'door1': (0, 0, -60), 'turret': (0, 30, 0)}),
    preview_pose={},
    always_visible=['stand', 'gun'],
)
ZB, ZF, YT = -18.7, 11.3, 24.13      # shaft back/front, top


def build(k):
    b = k.piece('base')
    xi, xo = 11.0, 17.0
    belt = [(-21.4, 0.0), (20.4, 0.0), (23.6, 2.8), (22.6, 5.6), (-22.4, 5.6), (-24.2, 2.8)]
    b.prism(xi, xo, belt, 'tread', bevel=0.16, mirror=True)
    for z in (-16.8, -10.2, -3.6, 3.0, 9.6, 16.2):
        b.cyl((xo, 2.2, z), (xo + 0.4, 2.2, z), 1.8, 12, 'dark', mirror=True)
        b.cyl((xo + 0.4, 2.2, z), (xo + 0.65, 2.2, z), 0.7, 8, 'steel', mirror=True)
    # track pods: dark guards with Core teeth
    b.hull([(10.6, 7.4, -23.2), (17.4, 7.4, -23.2), (17.4, 7.4, 19.0), (10.6, 7.4, 19.0),
            (10.6, 5.6, 23.4), (17.0, 5.4, 22.6), (10.6, 5.4, -24.2), (17.0, 5.2, -23.8)], 'paint2', bevel=0.14, mirror=True)
    for z in (-18.0, -10.0, -2.0, 6.0, 14.0):
        b.hull([(17.3, 7.0, z - 2.6), (17.3, 7.0, z + 2.6), (17.3, 5.4, z - 1.6), (17.3, 5.4, z + 1.6), (18.2, 6.2, z)],
               'dark', bevel=0.05, mirror=True)
    # chassis deck (crosses x = 0)
    b.prism(-11.0, 11.0, [(-23.4, 2.2), (21.4, 2.2), (24.0, 4.6), (23.0, 7.4), (-23.0, 7.4), (-24.2, 4.6)], 'paint', bevel=0.16)
    # tower walls around the shaft: side walls (mirrored), back + front walls (cross x = 0)
    b.hull([(x, y, z) for x in (9.5, 12.4) for y, z in [(5.0, ZB - 2.6), (5.0, ZF + 1.6), (YT, ZB - 1.4), (YT, ZF + 0.6)]] +
           [(13.6, 5.0, ZB - 2.0), (13.6, 5.0, ZF + 1.0)], 'paint', bevel=0.18, mirror=True)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 5.0, ZB - 2.6), (9.6, YT, ZB - 1.4), (9.6, 5.0, ZB), (9.6, YT, ZB)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 5.0, ZF), (9.6, YT, ZF), (9.6, 5.0, ZF + 1.6), (9.6, YT, ZF + 0.6)]], 'paint', bevel=0.16)
    b.box((-9.5, 5.0, ZB), (9.5, 5.6, ZF), 'black', bevel=0.0)                  # shaft floor
    # ochre lips around the shaft mouth
    b.box((-9.6, YT - 0.05, ZB - 1.2), (9.6, YT + 0.15, ZB), 'hazard', bevel=0.02)
    b.box((-9.6, YT - 0.05, ZF), (9.6, YT + 0.15, ZF + 0.5), 'hazard', bevel=0.02)
    # buttress ribs on the tower sides (dark verticals: break the tall wall)
    for z in (-12.0, -2.0, 7.0):
        b.box((12.3, 7.4, z - 1.0), (13.0, 22.6, z + 1.0), 'dark', bevel=0.06, mirror=True)
    # cab: low raked block in front of the tower (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.6, 7.4, ZF + 1.4), (10.6, 7.4, 22.6), (8.6, 16.6, ZF + 1.0), (8.0, 16.6, 15.4), (7.6, 9.6, 23.6)]],
           'paint', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, 13.4, 18.4), (6.4, 16.2, 15.6), (6.8, 13.52, 18.52), (6.4, 16.32, 15.72)]], 'glass', bevel=0.03)
    b.box((-7.2, 16.6, ZF + 1.4), (7.2, 16.82, 14.8), 'team', bevel=0.04)
    b.box((5.8, 8.2, 22.8), (8.8, 9.4, 23.6), 'dark', bevel=0.05, mirror=True)
    b.box((6.0, 8.4, 23.55), (8.6, 9.2, 23.65), 'lightw', bevel=0.0, mirror=True)
    # rear: exhausts + tail lights
    b.cyl((7.6, 7.4, -22.6), (7.6, 18.0, -22.6), 1.0, 10, 'dark', bevel=0.05, mirror=True)
    b.cyl((7.6, 18.0, -22.6), (7.6, 18.15, -22.6), 0.7, 10, 'black', mirror=True)
    b.box((-6.0, 7.6, -23.6), (6.0, 12.0, -22.9), 'dark', bevel=0.05)
    b.box((4.0, 10.2, -23.7), (5.4, 11.0, -23.55), 'lightr', bevel=0.0, mirror=True)
    # amber beacons on the tower's rear corners
    for x in (-11.0, 11.0):
        b.cyl((x, YT, ZB - 1.0), (x, YT + 0.8, ZB - 1.0), 0.8, 10, 'dark', bevel=0.04)
        b.cyl((x, YT + 0.8, ZB - 1.0), (x, YT + 1.6, ZB - 1.0), 0.55, 10, 'lightw')

    # ---------------------------------------------------------------- doors (door1 hinge x -9.48; door2 mirrored)
    d = k.piece('door1'); D = d.at
    for z0, z1 in ((-13.9, -3.9), (-3.9, 6.1), (6.1, 16.1)):
        d.hull([D(x, y, z) for x, y in ((0.0, 0.0), (9.45, 2.45), (9.45, 1.9), (0.0, -0.5)) for z in (z0, z1)], 'steel', bevel=0.08)
    d.hull([D(x, y + dy, z) for x, y in ((6.2, 1.61), (9.0, 2.33)) for dy in (0.06, 0.2) for z in (-11.6, 13.8)], 'team', bevel=0.03)
    d.cyl(D(0.0, -0.1, -13.6), D(0.0, -0.1, 15.8), 0.5, 8, 'dark')
    k.clone('door2', 'door1', mirror_x=True)

    # ---------------------------------------------------------------- turret: stand collar (origin 0, 5, -8.75)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.6, 0), A(0, 3.0, 0), 4.6, 10, 'dark', rot=math.pi / 10, bevel=0.1)
    t.cyl(A(0, 3.0, 0), A(0, 5.0, 0), 3.0, 10, 'paint2', r2=2.4, rot=math.pi / 10, bevel=0.08)

    # ---------------------------------------------------------------- stand: telescopic mast (rises 10.25)
    s = k.piece('stand'); S = s.at
    s.cyl(S(0, 0.2, 0), S(0, 16.0, 0), 1.5, 10, 'steel', rot=math.pi / 10)
    for y in (4.0, 9.0, 13.6):
        s.cyl(S(0, y, 0), S(0, y + 0.7, 0), 2.0, 10, 'dark', rot=math.pi / 10, bevel=0.04)

    # ---------------------------------------------------------------- gun: nano projector (beam at z +17.5)
    g = k.piece('gun'); G = g.at
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.8, -2.4, -6.4), (3.8, 2.2, -6.4), (3.6, -3.2, 2.0), (3.6, 3.0, 2.0)]], 'paint2', bevel=0.14)
    g.box(G(-2.6, 2.95, -5.0), G(2.6, 3.2, 1.2), 'hazard', bevel=0.03)
    g.cyl(G(0, -0.1, 1.8), G(0, -0.1, 15.6), 2.0, 10, 'steel', r2=1.0, rot=math.pi / 10)
    for z in (4.6, 7.6, 10.6):
        g.cyl(G(0, -0.1, z), G(0, -0.1, z + 0.9), 2.4 - z * 0.08, 10, 'dark', rot=math.pi / 10, bevel=0.04)
    g.cyl(G(0, -0.1, 15.4), G(0, -0.1, 17.4), 1.2, 10, 'lightr', r2=0.5)
