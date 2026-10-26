"""Hedgehog (CORE_T2_VEH_Hedgehog) - Core mobile anti-missile defence. A four-wheeled armoured carrier (LF/LR/RF/RR
wheels: hex road wheels on outriggers, the COB slides them 5 elmo when deploying) carrying one very long launcher Box
lying along the spine; when it deploys the Box swings up 90 deg (turn x) to stand vertical with its cell face up, and
the four triangular armour fins (Guard1..4) slide out and down 7.6/8.4 as stabilisers. `Fire` is the empty emit point
at the cell face; GP the empty ground piece.
Value groups from above: the long Box is the read - a light steel launcher spine running the full length with a team
stripe and an ochre cell face - over a dark warm carrier; four dark fins standing either side of it (the "hedgehog"
spines), black hex wheels at the corners, paint2 wheel arches.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=71, drop=['Guard1'], pose={'Box': (-20, 0, 0)}),
    preview_pose={},
)


def build(k):
    # ------------------------------------------------------------------ wheels: LFwheel built, others cloned
    w = k.piece('LFwheel'); W = w.at
    w.cyl(W(0.4, 0, 0), W(5.6, 0, 0), 3.9, 6, 'tread', rot=math.pi / 6, bevel=0.14)
    w.cyl(W(5.6, 0, 0), W(6.0, 0, 0), 2.2, 6, 'dark', rot=math.pi / 6, bevel=0.05)
    w.cyl(W(6.0, 0, 0), W(6.25, 0, 0), 0.9, 6, 'steel', rot=math.pi / 6)
    k.clone('LRwheel', 'LFwheel')
    k.clone('RFwheel', 'LFwheel', mirror_x=True)
    k.clone('RRwheel', 'LFwheel', mirror_x=True)

    # ------------------------------------------------------------------ Base: carrier hull
    b = k.piece('Base')
    b.prism(-10.4, 10.4, [(-19.2, 1.6), (16.6, 1.6), (19.0, 4.0), (18.0, 7.2), (-18.6, 7.2), (-19.8, 4.2)], 'paint', bevel=0.18)
    # wheel arches over each wheel (paint2), outrigger arms
    for z in (4.52, -10.48):
        b.hull([(9.6, 7.6, z - 5.2), (16.6, 7.6, z - 5.2), (9.6, 7.6, z + 5.2), (16.6, 7.6, z + 5.2),
                (9.6, 6.0, z - 6.0), (16.6, 6.0, z - 6.0), (9.6, 6.0, z + 6.0), (16.6, 6.0, z + 6.0)], 'paint2', bevel=0.14, mirror=True)
        b.box((8.8, 2.4, z - 1.4), (10.6, 4.2, z + 1.4), 'dark', bevel=0.08, mirror=True)
    # raised deck strips beside the Box (where the fins stand), dark
    b.box((3.8, 7.2, -16.4), (9.6, 8.4, 10.6), 'dark', bevel=0.1, mirror=True)
    # Box cradle under its front and rear
    b.box((-4.2, 7.2, 14.6), (4.2, 8.6, 18.2), 'dark', bevel=0.08)
    b.box((-4.2, 7.2, -19.6), (4.2, 8.6, -16.8), 'dark', bevel=0.08)
    b.cyl((-4.6, 4.8, -15.6), (4.6, 4.8, -15.6), 1.6, 12, 'steel')               # Box hinge
    # ochre nose bumper + lights
    b.box((-9.6, 2.6, 18.6), (9.6, 4.6, 19.6), 'hazard', bevel=0.08)
    b.box((5.6, 5.0, 18.2), (8.6, 6.2, 18.9), 'dark', bevel=0.05, mirror=True)
    b.box((5.8, 5.2, 18.85), (8.4, 6.0, 18.95), 'lightw', bevel=0.0, mirror=True)
    b.box((-8.0, 2.6, -20.1), (8.0, 6.4, -19.5), 'dark', bevel=0.05)
    b.box((6.2, 4.6, -20.2), (7.4, 5.4, -20.05), 'lightr', bevel=0.0, mirror=True)
    b.cyl((-8.6, 8.4, -18.2), (-8.6, 9.1, -18.2), 0.34, 8, 'dark')
    b.cyl((-8.6, 9.1, -18.2), (-8.6, 15.0, -18.2), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-8.6, 15.0, -18.2), (-8.6, 15.2, -18.2), 0.15, 6, 'lightr')

    # ------------------------------------------------------------------ Guards: triangular fins (Guard1 built)
    g = k.piece('Guard1'); G = g.at
    g.hull([G(x, y, z) for x in (0.0, 1.0) for y, z in [(0.0, -4.6), (0.0, 4.4), (8.4, -4.6), (8.4, -2.6)]], 'dark', bevel=0.1)
    g.hull([G(x, y, z) for x in (1.0, 7.4) for y, z in [(0.0, -4.4), (0.0, 4.2)]] +
           [G(1.0, 8.0, -4.4), G(1.0, 8.0, -2.8)], 'paint2', bevel=0.1)
    g.box(G(1.0, 0.4, -4.3), G(1.2, 6.8, -3.2), 'hazard', bevel=0.02)
    k.clone('Guard2', 'Guard1')
    k.clone('Guard3', 'Guard1', mirror_x=True)
    k.clone('Guard4', 'Guard1', mirror_x=True)

    # ------------------------------------------------------------------ Box: the launcher (origin 0, 4.8, -15.6)
    x = k.piece('Box'); X = x.at
    for z0, z1 in ((-5.4, 9.6), (9.6, 24.0), (24.0, 36.0)):
        x.box(X(-3.6, -1.4, z0), X(3.6, 5.4, z1), 'steel', bevel=0.16)
    x.hull([X(xx, y, z) for xx in (-3.6, 3.6) for y, z in [(-1.4, 36.0), (5.4, 36.0), (-1.0, 38.6), (5.4, 39.0)]], 'steel', bevel=0.14)
    x.box(X(-1.6, 5.4, -3.6), X(1.6, 5.62, 33.6), 'team', bevel=0.04)
    # side reinforcement ribs (dark), break the long box
    for z in (2.0, 14.0, 26.0):
        x.box(X(-3.9, -1.0, z), X(3.9, 5.0, z + 1.6), 'dark', bevel=0.06)
    # cell face: ochre frame with a 2x3 grid of black missile cells
    x.hull([X(xx, y, z) for xx in (-3.4, 3.4) for y, z in [(-0.8, 38.7), (5.2, 39.05), (-0.8, 38.85), (5.2, 39.2)]], 'hazard', bevel=0.03)
    for cx in (-1.7, 1.7):
        for cy in (0.6, 2.4, 4.2):
            x.cyl(X(cx, cy, 38.95 + (cy + 0.8) * 0.058), X(cx, cy, 39.3 + (cy + 0.8) * 0.058), 0.7, 8, 'black')
    # base block below the hinge (the part that goes down when the Box stands up)
    x.box(X(-3.4, -4.8, -5.4), X(3.4, -1.4, 0.0), 'dark', bevel=0.12)
