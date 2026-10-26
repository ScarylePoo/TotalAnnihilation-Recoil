"""Eagle (ARM_T2_AIR_Eagle) - Arm T2 radar plane (AWACS). The identity is the huge rotodome: a 21-elmo disc on a
pylon over the fuselage, spun by the COB in flight (spin y), dark with a broad light radar bar across it and a team
rim - from above a spinning dark disc with a light bar, unlike any other plane. Underneath: a slim fuselage with a long
nose, a long straight wing with two engine nacelles, outer wing panels (Lwing/Rwing) that slide out 11 elmo on
take-off (move x) for a 52-elmo glider span, and a twin tail.
Pieces (TA layout): base, Lwing (+x side, sliding outer panel) / Rwing (-x; mirrored clone of Lwing), radar
(rotodome on its pylon; spins y).
Value groups from above: light Arm wings and fuselage, the dark paint2 rotodome with its light bar, dark paint2
nacelles, team on the dome rim + outer wing panels + fin tips.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=47, drop=['radar'], remove=['Rwing']),
    always_visible=['Lwing', 'Rwing'],
    # flight pose: outer panels out (engine x = -COB x); the dome spins
    preview_pose={'Lwing': {'move': (11.125, 0, 0)}, 'Rwing': {'move': (-11.125, 0, 0)}, 'radar': (0, 30, 0)},
)

WY = 1.3


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ slim fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.6, 1.4, 25.4), (0.6, 2.4, 25.2), (3.0, 0.5, 20.0), (3.0, 3.6, 19.0),
             (4.6, 0.4, 12.0), (4.0, 6.0, 11.0), (4.8, 0.4, -10.0), (3.8, 6.2, -12.0),
             (3.2, 0.8, -24.0), (2.6, 5.6, -24.6), (1.6, 2.0, -27.0), (1.4, 4.6, -27.0)]], 'paint', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 3.0, 22.6), (3.0, 4.4, 18.0), (2.6, 6.2, 12.6), (1.2, 6.8, 14.4), (1.2, 6.6, 11.8), (2.0, 3.8, 21.0)]],
           'glass', bevel=0.07)
    b.cyl((0, 1.9, 25.2), (0, 1.9, 27.4), 0.4, 8, 'dark', r2=0.14)
    # dome pylon fairing on the spine
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 6.0, 2.0), (1.8, 6.2, -12.0), (1.0, 7.2, -2.0), (1.0, 7.2, -9.0)]], 'paint2', bevel=0.12)

    # ------------------------------------------------------------------ long straight fixed wing (mirrored)
    b.hull([(x, WY + t, z) for x, z0, z1, tt in ((4.0, 13.0, -16.0, 0.85), (18.4, 2.6, -16.0, 0.55))
            for z, t in ((z0, 0.0), (z0 - 1.6, tt), (z0 - 1.6, -tt), (z1 + 1.0, tt * 0.8), (z1 + 1.0, -tt * 0.8), (z1, 0.0))],
           'paint', bevel=0.08, mirror=True)
    b.hull([(x, WY + d, z) for x in (5.0, 17.6) for z in (-13.2, -15.6) for d in (0.66, 0.76)], 'paint2', bevel=0.0, mirror=True)
    b.hull([(x, WY + 0.55 + 0.3 * (18.4 - x) / 14.4 + d, z) for x, zs in ((16.0, (2.6, -12.8)), (18.0, (1.6, -12.8)))
            for z in zs for d in (0.08, 0.18)], 'team', bevel=0.02, mirror=True)     # team band at the fixed-wing tips
    # engine nacelles out on the wing (outside the dome's shadow)
    b.cyl((13.4, 2.8, 4.6), (13.4, 2.8, -10.4), 2.0, 12, 'paint2', r2=1.7, rot=math.pi / 12, bevel=0.08, mirror=True)
    b.cyl((13.4, 2.8, 4.8), (13.4, 2.8, 4.5), 1.4, 12, 'black', mirror=True)
    b.cyl((13.4, 2.8, -10.35), (13.4, 2.8, -10.55), 1.1, 12, 'lightc', mirror=True)
    b.box((12.9, 1.6, -6.0), (13.9, 2.2, 2.0), 'dark', bevel=0.0, mirror=True)
    # twin tail + stabiliser
    b.hull([(x, WY + t, z) for x, z0, z1 in ((2.6, -17.0, -26.0), (10.8, -22.6, -27.2)) for z in (z0, z1)
            for t in (0.4, -0.4)], 'paint', bevel=0.06, mirror=True)
    b.hull([(5.8, 2.0, -18.0), (5.8, 2.0, -25.6), (6.7, 11.7, -21.5), (6.7, 11.7, -27.0),
            (6.6, 2.0, -18.0), (6.6, 2.0, -25.6), (7.5, 11.7, -21.5), (7.5, 11.7, -27.0)], 'paint', bevel=0.07, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(6.5, 10.2, -20.6), (6.7, 11.7, -21.5), (6.7, 11.7, -27.0), (6.5, 10.2, -26.6)]] +
           [(x + 0.85, y, z) for x, y, z in [(6.5, 10.2, -20.6), (6.7, 11.7, -21.5), (6.7, 11.7, -27.0), (6.5, 10.2, -26.6)]],
           'team', bevel=0.0, mirror=True)
    b.box((6.6, 11.6, -26.8), (7.6, 12.0, -25.8), 'lightr', bevel=0.0, mirror=True)
    b.cyl((0, 3.2, -26.6), (0, 3.2, -28.2), 1.4, 10, 'dark', r2=1.1, bevel=0.03)
    b.box((17.8, 0.9, 1.8), (18.6, 1.8, 2.8), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ rotodome (radar, origin 0, 8.5, -5; spins y)
    r = k.piece('radar'); R = r.at
    r.cyl(R(0, -2.6, 0), R(0, -0.6, 0), 1.1, 10, 'dark', bevel=0.04)                  # pylon
    r.cyl(R(0, -0.8, 0), R(0, 0.2, 0), 10.6, 32, 'paint2', r2=10.6, bevel=0.0)
    r.cyl(R(0, 0.2, 0), R(0, 1.3, 0), 10.6, 32, 'paint2', r2=9.6, bevel=0.1)            # domed top
    r.cyl(R(0, -0.8, 0), R(0, -1.5, 0), 10.6, 32, 'paint2', r2=9.4, bevel=0.06)          # domed bottom
    # team rim on the dome's shoulder
    r.cyl(R(0, 0.25, 0), R(0, 1.05, 0), 10.75, 32, 'team', r2=9.95, bevel=0.0)
    # broad light radar bar across the dome (reads as a spinning bar from above)
    r.hull([R(x, y, z) for x in (-8.9, 8.9) for z in (-2.2, 2.2) for y in (1.25, 1.55)] +
           [R(x, 1.0, z) for x in (-9.5, 9.5) for z in (-2.4, 2.4)], 'paint', bevel=0.06)
    r.cyl(R(0, 1.3, 0), R(0, 1.9, 0), 1.4, 12, 'dark', r2=1.0, bevel=0.03)
    r.cyl(R(0, 1.9, 0), R(0, 2.2, 0), 0.5, 8, 'lightr')

    # ------------------------------------------------------------------ Lwing (origin 5, 0.5, -7.5; slides +11.1)
    w = k.piece('Lwing'); W = w.at
    pl = [(-1.5, 9.4), (-1.5, -8.4), (12.8, -4.6), (12.8, -1.4)]
    pts = []
    for x, z in pl:
        t = 0.6 - 0.25 * (x + 1.5) / 14.3
        pts += [W(x, WY - 0.5 + t, z), W(x, WY - 0.5 - t, z)]
    w.hull(pts, 'paint', bevel=0.06)
    tp = [(1.2, 7.4), (12.2, -1.5), (12.2, -4.4), (1.2, -7.6)]
    w.hull([W(x, WY - 0.5 + 0.6 - 0.25 * (x + 1.5) / 14.3 + d, z) for x, z in tp for d in (0.04, 0.14)], 'team', bevel=0.02)
    w.box(W(12.6, WY - 0.9, -4.4), W(13.2, WY - 0.1, -3.2), 'lightw', bevel=0.0)
    k.clone('Rwing', 'Lwing', mirror_x=True)
