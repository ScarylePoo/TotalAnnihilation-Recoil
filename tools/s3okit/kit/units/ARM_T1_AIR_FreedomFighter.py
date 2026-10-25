"""Freedom Fighter (ARM_T1_AIR_FreedomFighter) - Arm T1 fighter. Slim needle fuselage between two dark intake pods
carrying the twin guns, a single tall fin, and narrow, sharply swept (42 deg) wings with engine pods on the tips.
The wings are separate pieces that the COB slides OUT of the body on take-off (move x 6, z -1.25) and back in on
landing: at rest they tuck under the light wing gloves, in flight the span grows from 36 to 48 elmo - the swept,
narrow, wide-span arrow is the fighter's read from above.
Pieces (TA layout): base, wing1/wing2 (sliding wings; wing2 = mirrored clone), flare1/flare2 + wing1thrust/wing2thrust
(empty emit points at the wing-pod nozzles), rearthrust (empty, main nozzle), mgun1/mgun2 (empty gun emit points at the
pod muzzles).
Value groups from above: light Arm fuselage, gloves and wings; dark paint2 intake pods; near-black nozzles; team
wedges on the glove tops + a spine band; cyan engine glows.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=7, remove=['wing2'], drop=[]),
    # flight pose: the COB moves the wings out on take-off (engine x = -COB x)
    preview_pose={'wing1': {'move': (6.0, 0, -1.25)}, 'wing2': {'move': (-6.1, 0, -1.37)}},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 3.7, 17.6), (0.3, 3.2, 17.2),
             (1.6, 2.6, 13.0), (1.6, 5.0, 13.0),
             (3.0, 1.6, 6.0), (3.0, 6.6, 6.0),
             (3.2, 1.6, -8.0), (3.2, 6.6, -8.0),
             (2.4, 2.2, -17.0), (2.4, 5.6, -17.0)]], 'paint', bevel=0.16)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 5.2, 12.4), (1.9, 6.5, 8.0), (1.9, 6.6, 3.6), (0.7, 7.7, 7.4), (0.7, 7.7, 4.2), (1.2, 6.6, 1.8)]], 'glass', bevel=0.08)
    # pitot / radar tip
    b.cyl((0, 3.55, 17.4), (0, 3.55, 19.4), 0.34, 8, 'dark', r2=0.12)
    # team spine band behind the canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 6.6, 0.8), (1.4, 6.6, -9.0), (1.4, 6.74, 0.8), (1.4, 6.74, -9.0)]], 'team', bevel=0.03)

    # ------------------------------------------------------------------ intake pods with the guns (mirrored)
    b.hull([(3.0, 2.2, 8.6), (6.6, 2.2, 8.6), (3.0, 5.6, 9.8), (6.4, 5.6, 9.8), (3.0, 6.0, 4.0), (7.0, 6.0, 4.0),
            (3.0, 1.6, -15.6), (7.6, 1.6, -15.0), (3.0, 6.0, -15.6), (7.4, 6.0, -15.0)], 'paint2', bevel=0.14, mirror=True)
    b.hull([(3.4, 2.3, 9.0), (6.8, 2.3, 9.0), (3.4, 5.4, 9.95), (6.6, 5.4, 9.95),
            (3.4, 2.3, 8.7), (6.8, 2.3, 8.7), (3.4, 5.4, 9.65), (6.6, 5.4, 9.65)], 'black', bevel=0.0, mirror=True)
    # gun housing + barrel on the pod top (muzzle = mgun1 at 6.9, 5.88, 10.1)
    b.box((5.9, 5.9, -1.0), (7.9, 6.9, 6.0), 'dark', bevel=0.1, mirror=True)
    b.cyl((6.9, 6.0, 5.8), (6.9, 6.0, 10.2), 0.45, 8, 'steel', rot=math.pi / 8, mirror=True)
    b.cyl((6.9, 6.0, 9.6), (6.9, 6.0, 10.3), 0.62, 8, 'dark', rot=math.pi / 8, mirror=True)
    b.cyl((6.9, 6.0, 10.28), (6.9, 6.0, 10.36), 0.3, 8, 'black', mirror=True)
    # pod exhaust ring
    b.cyl((5.2, 3.8, -15.0), (5.2, 3.8, -16.2), 1.6, 12, 'dark', r2=1.4, bevel=0.04, mirror=True)
    b.cyl((5.2, 3.8, -16.15), (5.2, 3.8, -16.3), 1.0, 12, 'lightc', mirror=True)

    # ------------------------------------------------------------------ wing gloves (the wings retract under them)
    b.hull([(7.2, 4.1, 3.0), (12.8, 4.1, -5.0), (12.8, 4.1, -15.0), (7.2, 4.1, -15.0),
            (7.2, 4.8, 3.0), (12.6, 4.6, -5.2), (12.6, 4.6, -14.8), (7.2, 4.8, -14.8)], 'paint', bevel=0.1, mirror=True)
    b.hull([(7.6, 4.8, 0.6), (11.8, 4.62, -5.4), (11.8, 4.62, -13.6), (7.6, 4.8, -13.6),
            (7.6, 4.92, 0.6), (11.8, 4.74, -5.4), (11.8, 4.74, -13.6), (7.6, 4.92, -13.6)], 'team', bevel=0.03, mirror=True)

    # ------------------------------------------------------------------ tail: single tall fin + stabilisers
    b.hull([(0.3, 6.0, -9.0), (0.3, 5.4, -18.6), (0.3, 11.6, -15.4), (0.3, 11.6, -19.4)], 'paint', bevel=0.06, mirror=True)
    b.hull([(0.32, 10.4, -14.6), (0.32, 11.6, -15.4), (0.32, 11.6, -19.4), (0.32, 10.4, -19.1),
            (0.52, 10.4, -14.6), (0.52, 11.6, -15.4), (0.52, 11.6, -19.4), (0.52, 10.4, -19.1)], 'team', bevel=0.0, mirror=True)
    b.box((-0.3, 11.6, -19.2), (0.3, 11.95, -18.4), 'lightr', bevel=0.0)
    b.hull([(2.4, 4.4, -13.0), (2.4, 4.4, -19.0), (9.6, 4.4, -18.0), (9.6, 4.4, -20.0),
            (2.4, 4.85, -13.0), (2.4, 4.85, -19.0), (9.6, 4.65, -18.0), (9.6, 4.65, -20.0)], 'paint', bevel=0.06, mirror=True)
    # main nozzle (rearthrust at 0, 3.12, -17)
    b.cyl((0, 3.9, -15.4), (0, 3.9, -18.6), 2.1, 14, 'dark', r2=1.8, bevel=0.05)
    b.cyl((0, 3.9, -18.55), (0, 3.9, -18.7), 1.35, 14, 'lightc')

    # ------------------------------------------------------------------ wing1 (origin 7, 3.12, -8); wing2 = mirror clone
    w = k.piece('wing1'); W = w.at
    pts = []
    for x, zl, zt, t in ((0.0, 7.5, -4.5, 0.42), (11.0, -4.4, -8.0, 0.18)):
        for z, tt in ((zl, 0.1), (zl - 1.4, t), (zt + 0.8, t * 0.8), (zt, 0.06)):
            pts += [W(x, tt, z), W(x, -tt, z)]
    w.hull(pts, 'paint', bevel=0.05)
    # dark trailing-edge flap strip (separates the wing from the glove/fuselage at distance)
    w.hull([W(1.0, 0.36, -3.2), W(1.0, 0.32, -4.4), W(9.6, 0.18, -6.6), W(9.6, 0.15, -7.6),
            W(1.0, 0.46, -3.2), W(1.0, 0.42, -4.4), W(9.6, 0.28, -6.6), W(9.6, 0.25, -7.6)], 'paint2', bevel=0.0)
    # tip engine pod (wing1thrust / flare1 emit at 9.34, -0.93, -1.45)
    w.cyl(W(9.34, -0.93, 4.4), W(9.34, -0.93, -1.25), 0.95, 10, 'dark', r2=0.85, rot=math.pi / 10, bevel=0.04)
    w.cyl(W(9.34, -0.93, 4.6), W(9.34, -0.93, 4.38), 0.55, 10, 'black')
    w.cyl(W(9.34, -0.93, -1.22), W(9.34, -0.93, -1.42), 0.62, 10, 'lightc')
    w.box(W(8.9, -0.15, -0.2), W(9.8, 0.05, 3.4), 'dark', bevel=0.0)     # pylon
    k.clone('wing2', 'wing1', mirror_x=True)
