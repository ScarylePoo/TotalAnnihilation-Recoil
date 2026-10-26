"""Hawk (ARM_T2_AIR_Hawk) - Arm T2 stealth fighter. Where the T1 Freedom Fighter is a needle between two pods, the
Hawk is a flat, faceted lifting body: a broad diamond-chined hull with a sharp beak, a long low canopy, two dorsal
intakes, flat slot nozzles and a canted V-tail (fins splayed 35 deg). The wings (wing1/wing2) slide OUT of the body
on take-off (COB move x 5.0/5.6, z -1.4/-1.5) into a wide cranked delta with saw-tooth trailing edges, carrying a
missile under each tip (flare1/flare2 launch points).
Pieces (TA layout): base, wing1/wing2 (sliding wings; wing1 = mirrored clone of wing2), flare1/flare2 (empty
launch points, children of the wings), rearthrust (empty, main nozzle).
Value groups from above: light Arm body and wings, dark paint2 intake deck + V-tail, near-black slot nozzles and
intake mouths, team as a big dorsal chevron behind the canopy + the outer wing panels (wide flat team in flight).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=31, remove=['wing1'], drop=[]),
    always_visible=['wing1', 'wing2'],       # inner wing hides in the body at rest, shows in flight
    # flight pose: the COB slides the wings out on take-off (engine x = -COB x)
    preview_pose={'wing1': {'move': (-5.0, 0, -1.375)}, 'wing2': {'move': (5.625, 0, -1.5)}},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ faceted lifting body (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.25, 2.6, 20.4), (0.25, 2.1, 19.8),
             (2.6, 1.6, 13.0), (2.4, 4.6, 12.0),
             (7.4, 2.2, 1.0), (4.6, 5.8, 1.0), (2.6, 6.8, 0.0),
             (8.6, 2.2, -10.0), (5.2, 5.6, -10.0), (2.8, 6.4, -10.0),
             (8.8, 2.3, -15.0), (4.6, 1.4, -15.0), (4.6, 5.0, -16.0),
             (3.0, 1.6, -19.4), (3.0, 4.4, -19.4)]], 'paint', bevel=0.16)
    # chine skirt: thin sharp edge round the body (catches the rim light from above)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 2.2, 21.0), (3.0, 2.0, 12.4), (8.0, 2.0, 1.0), (9.4, 2.0, -10.0), (9.6, 2.0, -15.6),
             (0.3, 2.6, 21.0), (3.0, 2.5, 12.4), (8.0, 2.5, 1.0), (9.4, 2.5, -10.0), (9.6, 2.5, -15.6),
             (5.0, 2.2, -14.0), (5.0, 2.5, -14.0)]], 'paint', bevel=0.06)
    # long low canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.0, 3.8, 14.6), (1.9, 5.2, 9.0), (1.9, 6.5, 2.4), (0.8, 7.4, 6.4), (0.8, 7.5, 2.8), (1.0, 6.5, 0.6)]],
           'glass', bevel=0.08)
    b.cyl((0, 2.35, 20.6), (0, 2.35, 22.8), 0.32, 8, 'dark', r2=0.1)            # pitot
    # dorsal intakes either side of the canopy (dark paint2 deck: separates canopy/body from above)
    b.hull([(1.9, 5.6, 3.6), (4.8, 5.0, 3.0), (2.0, 7.0, 0.4), (4.6, 6.3, 0.0),
            (2.0, 6.6, -9.0), (5.0, 5.7, -9.0)], 'paint2', bevel=0.1, mirror=True)
    b.hull([(2.3, 5.75, 3.5), (4.5, 5.2, 3.0), (2.3, 6.8, 0.8), (4.4, 6.15, 0.5),
            (2.3, 5.75, 3.3), (4.5, 5.2, 2.8), (2.3, 6.8, 0.6), (4.4, 6.15, 0.3)], 'black', bevel=0.0, mirror=True)
    # team chevron on the spine behind the canopy (the body's colour block, wide and flat)
    b.hull([(x, y, z) for x, y, z in
            [(0.0, 6.62, -1.6), (0.0, 6.5, -6.6), (2.4, 6.55, -5.4), (2.4, 6.45, -10.0),
             (0.0, 6.78, -1.6), (0.0, 6.66, -6.6), (2.4, 6.71, -5.4), (2.4, 6.61, -10.0)]], 'team', bevel=0.02, mirror=True)
    b.hull([(x, 2.55 + d, z) for x, z in ((5.4, -1.0), (8.0, 0.6), (9.1, -10.0), (6.2, -10.0)) for d in (0.0, 0.08)],
           'team', bevel=0.02, mirror=True)                                     # chine team strakes
    # flat slot nozzles at the tail (rearthrust 0.12, 2.87, -18)
    b.hull([(x, y, z) for x in (0.6, 4.2) for y in (1.9, 4.0) for z in (-16.0, -19.6)], 'dark', bevel=0.08, mirror=True)
    b.box((0.9, 2.3, -19.75), (3.9, 3.6, -19.55), 'black', bevel=0.0, mirror=True)
    b.box((1.1, 2.5, -19.8), (3.7, 3.4, -19.7), 'lightc', bevel=0.0, mirror=True)
    # canted V-tail
    b.hull([(3.2, 4.6, -9.4), (3.6, 4.2, -16.4), (7.6, 11.0, -14.4), (8.0, 10.8, -18.6),
            (3.8, 4.4, -9.4), (4.2, 4.0, -16.4), (8.2, 10.8, -14.4), (8.6, 10.6, -18.6)], 'paint2', bevel=0.07, mirror=True)
    b.box((7.7, 10.7, -18.4), (8.6, 11.1, -17.4), 'lightr', bevel=0.0, mirror=True)
    # belly weapon-bay seam, nose landing light
    b.box((-1.6, 1.25, -8.0), (1.6, 1.5, 6.0), 'dark', bevel=0.04)
    b.box((-0.8, 1.7, 15.0), (0.8, 2.0, 15.4), 'lightw', bevel=0.0)

    # ------------------------------------------------------------------ wing2 (origin 2.38, 2.95, -4.4; +x side)
    w = k.piece('wing2'); W = w.at
    # cranked delta: root inside the body (slides out 5.6), sharp swept leading edge, saw-tooth trailing edge
    pl = [(1.0, 12.0), (1.0, -9.0), (6.0, -9.0), (9.0, -6.4), (13.6, -7.2), (13.6, -5.0), (8.0, 4.0)]
    w.hull([W(x, y, z) for x, z in pl for y in ((0.42, -0.42) if x < 9 else (0.26, -0.26))], 'paint', bevel=0.06)
    # outer wing team panel (the fighter's colour read in flight)
    w.hull([W(x, y, z) for x, z, t in ((3.6, 7.6, 0.43), (7.6, 3.0, 0.43), (12.8, -4.9, 0.27), (12.8, -6.6, 0.27),
                                        (9.4, -5.9, 0.36), (5.8, -6.0, 0.43), (3.6, -6.0, 0.43)) for y in (t, t + 0.1)], 'team', bevel=0.02)
    # dark flap strip along the inner trailing edge
    w.hull([W(x, y, z) for x, z in ((1.2, -7.4), (5.6, -7.4), (5.8, -8.8), (1.2, -8.8)) for y in (0.42, 0.52)],
           'paint2', bevel=0.0)
    # tip missile on a pylon (flare2 launch point at local 8.27, -1.2, 3.76)
    mx, my = 8.27, -1.35
    w.box(W(mx - 0.25, my + 0.3, -1.6), W(mx + 0.25, -0.3, 3.0), 'dark', bevel=0.0)
    w.cyl(W(mx, my, -3.0), W(mx, my, 3.6), 0.62, 8, 'steel', rot=math.pi / 8)
    w.cyl(W(mx, my, 3.6), W(mx, my, 5.6), 0.62, 8, 'lightr', r2=0.12, rot=math.pi / 8)
    w.box(W(mx - 1.3, my - 0.06, -3.0), W(mx + 1.3, my + 0.06, -1.6), 'dark', bevel=0.0)
    # wing-tip nav light
    w.box(W(13.0, -0.2, -6.9), W(13.7, 0.25, -5.4), 'lightw', bevel=0.0)
    k.clone('wing1', 'wing2', mirror_x=True)
