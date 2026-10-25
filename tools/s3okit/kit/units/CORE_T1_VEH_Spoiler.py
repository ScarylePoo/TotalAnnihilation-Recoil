"""Spoiler (CORE_T1_VEH_Spoiler) - Core mine layer. Two big front wheels (Wheel1/2 spin x) under a low cab, a tall
armoured mine magazine at the rear riding on short tracks (part of Base: the TA model has no rear wheel pieces).
The magazine is a hollow walled box closed by two roof doors (Door1/2 turn + slide); when activated the `Turret`
pylon rises out of it carrying `Stand` and the mine `Gun` (turns y); `Beam` (empty) is the emit point.
Value groups from above: dark warm cab, darker paint2 magazine walls framed by light steel rails around team-coloured roof doors, steel wheel arches, black
tyres/tracks, light steel dispenser gun + pylon, ochre hazard bumper and mine-chute frame.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=12, drop=['Wheel2'], pose={'Door2': (0, 0, 30)}),
    preview_pose={},
)


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ rear tracks under the magazine
    belt = [(-21.6, 0.0), (-7.4, 0.0), (-5.4, 2.4), (-6.0, 4.6), (-22.6, 4.6), (-24.0, 2.4)]
    b.prism(9.4, 14.2, belt, 'tread', bevel=0.15, mirror=True)
    for z in (-19.6, -14.6, -9.6):
        b.cyl((14.2, 2.2, z), (14.6, 2.2, z), 1.6, 12, 'dark', mirror=True)
        b.cyl((14.6, 2.2, z), (14.8, 2.2, z), 0.65, 8, 'steel', mirror=True)
    # chassis spine (crosses x = 0)
    b.prism(-9.6, 9.6, [(-23.6, 2.6), (21.6, 2.6), (23.6, 4.8), (23.0, 6.6), (-23.8, 6.6), (-24.4, 4.4)], 'paint2', bevel=0.15)
    # ------------------------------------------------------------------ magazine (hollow: walls around the bay)
    # side walls (inner face x 11.5 = door hinge), sloped outer face
    b.hull([(11.5, 4.6, -23.6), (14.4, 4.6, -23.6), (11.5, 4.6, -4.6), (14.4, 4.6, -4.6),
            (11.5, 16.9, -21.4), (12.6, 16.9, -21.4), (11.5, 16.9, -6.6), (12.6, 16.9, -6.6)], 'paint2', bevel=0.16, mirror=True)
    # rear wall with mine chute, front wall
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(11.6, 4.6, -23.8), (11.6, 4.6, -19.8), (11.6, 16.9, -21.4), (11.6, 16.9, -19.8)]], 'paint2', bevel=0.14)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(11.6, 4.6, -7.8), (11.6, 4.6, -4.4), (11.6, 16.9, -7.8), (11.6, 16.9, -6.6)]], 'paint2', bevel=0.14)
    b.box((-11.5, 4.6, -19.8), (11.5, 6.4, -7.8), 'dark', bevel=0.0)          # bay floor
    # light steel rails framing the roof doors (Core: light metal on dark armour)
    b.box((11.6, 16.9, -21.2), (12.7, 17.5, -6.8), 'steel', bevel=0.08, mirror=True)
    for z0, z1 in ((-21.4, -19.9), (-7.7, -6.6)):
        b.box((-11.6, 16.9, z0), (11.6, 17.5, z1), 'steel', bevel=0.08)
    # team bands along the wall tops (beside the doors)
    # mine chute at the back: hazard frame, black slot
    b.box((-5.0, 4.8, -24.2), (5.0, 9.6, -23.6), 'hazard', bevel=0.05)
    b.box((-3.8, 5.4, -24.35), (3.8, 9.0, -24.1), 'black', bevel=0.0)
    b.box((8.4, 12.6, -23.2), (10.0, 13.6, -22.9), 'lightr', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ cab + bonnet (front)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.4, 6.4, -4.4), (9.4, 6.4, 22.4), (8.2, 6.2, 24.2),
             (8.6, 10.6, 23.2), (8.8, 11.4, 10.0), (8.0, 14.6, 5.8), (8.6, 14.6, -4.4)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, 11.7, 9.4), (6.4, 14.2, 6.4), (6.8, 11.82, 9.52), (6.4, 14.32, 6.52)]], 'glass', bevel=0.03)
    b.box((-6.6, 14.6, -3.6), (6.6, 14.78, 4.4), 'paint2', bevel=0.04)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.0, 10.65, 22.0), (6.0, 11.36, 13.0), (6.0, 10.8, 22.04), (6.0, 11.5, 13.04)]], 'paint2', bevel=0.03)
    # wheel arches (front wheels sit at x 5.5..13.9), team tops
    b.hull([(9.2, 10.4, 11.4), (14.6, 10.4, 11.4), (9.2, 10.4, 24.4), (14.6, 10.4, 24.4),
            (9.2, 11.6, 13.2), (14.6, 11.6, 13.2), (9.2, 11.6, 22.6), (14.6, 11.6, 22.6)], 'steel', bevel=0.12, mirror=True)
    # hazard bumper, headlights
    b.box((-9.0, 4.8, 23.8), (9.0, 6.8, 24.8), 'dark', bevel=0.05)
    b.box((5.8, 7.6, 23.6), (7.6, 8.8, 24.3), 'dark', bevel=0.05, mirror=True)
    b.box((5.95, 7.75, 24.28), (7.45, 8.65, 24.38), 'lightw', bevel=0.0, mirror=True)
    # beacon on the cab roof
    b.cyl((0.0, 14.6, 5.4), (0.0, 15.3, 5.4), 0.9, 10, 'dark')
    b.cyl((0.0, 15.3, 5.4), (0.0, 16.1, 5.4), 0.62, 10, 'lightr')

    # ---------------------------------------------------------------- front wheels (Wheel1 built, Wheel2 mirror clone)
    w = k.piece('Wheel1'); W = w.at
    w.cyl(W(0.4, 0, 0), W(8.2, 0, 0), 5.6, 16, 'tread', rot=math.pi / 16, bevel=0.3)
    w.cyl(W(8.2, 0, 0), W(8.5, 0, 0), 3.0, 12, 'dark', bevel=0.06)
    w.cyl(W(8.5, 0, 0), W(8.75, 0, 0), 1.3, 8, 'steel')
    k.clone('Wheel2', 'Wheel1', mirror_x=True)

    # ---------------------------------------------------------------- doors (Door1 hinge x -11.48; Door2 mirror clone)
    d = k.piece('Door1'); D = d.at
    d.box(D(0.05, -0.6, -5.9), D(11.45, 0.3, 5.9), 'paint2', bevel=0.1)
    d.box(D(1.0, 0.3, -5.2), D(10.0, 0.46, 5.2), 'team', bevel=0.03)
    d.box(D(10.2, 0.3, -5.4), D(11.3, 0.42, 5.4), 'hazard', bevel=0.02)
    d.cyl(D(0.0, -0.1, -5.6), D(0.0, -0.1, 5.6), 0.45, 8, 'dark')
    k.clone('Door2', 'Door1', mirror_x=True)

    # ---------------------------------------------------------------- turret pylon / stand / gun (rise from the bay)
    t = k.piece('Turret'); A = t.at
    t.hull([A(x * sx, y, z * sz) for sx in (-1, 1) for sz in (-1, 1) for x, y, z in
            [(4.6, 0.0, 4.6), (1.4, 8.6, 1.4)]], 'paint2', bevel=0.12)
    t.box(A(-1.6, 7.2, -1.6), A(1.6, 8.8, 1.6), 'dark', bevel=0.06)
    s = k.piece('Stand'); St = s.at
    s.cyl(St(0, 0.0, 0), St(0, 11.4, 0), 0.95, 10, 'steel', rot=math.pi / 10)
    s.cyl(St(0, 9.8, 0), St(0, 10.6, 0), 1.3, 10, 'dark')
    g = k.piece('Gun'); G = g.at
    # drum magazine + flared dispenser chute to the beam point (z 15.5)
    g.cyl(G(0, -2.4, -1.6), G(0, 2.4, -1.6), 2.6, 12, 'steel', rot=math.pi / 12, bevel=0.1)
    g.cyl(G(0, 2.4, -1.6), G(0, 2.56, -1.6), 1.9, 12, 'team')
    g.hull([G(x * sx, y * sy, z) for sx in (-1, 1) for sy in (-1, 1) for x, y, z in
            [(1.7, 1.7, 0.4), (1.1, 1.1, 13.0), (1.5, 1.5, 15.2)]], 'steel', bevel=0.08)
    g.box(G(-1.3, -1.3, 15.2), G(1.3, 1.3, 15.45), 'black', bevel=0.0)
    g.box(G(-1.25, 1.2, 3.0), G(1.25, 1.42, 11.0), 'hazard', bevel=0.02)
