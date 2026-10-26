"""Snake (CORE_T1_SEA_Snake) - Core submarine. A broad, flat manta-like body: a wide humped aft hull with the sail
fused into a high sloping spine, a tapering snout forward, and two forward-swept glazed torpedo blisters on the
shoulders (tube1/tube2 fire from them); small swept fins under the snout. The opposite read of the Arm Lurker:
wide at the BACK, pointed at the front, dark overall with light (steel) blisters.
Pieces (TA layout): base, tube1/tube2 (empty torpedo points), wake (empty emit point at the stern).
Value groups from above (seen through 30 elmos of water): dark Core hull, darker paint2 spine/aft deck, light steel
shoulder blisters + snout plate, team on the spine top and blister tops. Submarine, waterline 30.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=7),
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ aft hull: wide, flat, humped (crosses x = 0)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.4, 1.4, -2.0), (9.4, 1.4, -20.0), (7.6, 1.6, -24.6),
             (12.6, 6.2, -1.6), (12.4, 6.2, -19.2), (7.8, 6.2, -25.0),
             (9.4, 10.6, -2.0), (8.4, 10.6, -22.8), (4.0, 13.4, -6.0), (3.8, 13.0, -18.0)]], 'paint', bevel=0.22)
    # forebody: tapering snout to the bow
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.4, 1.6, -2.0), (5.2, 1.6, 14.0), (4.4, 1.6, 21.2), (0.4, 1.6, 24.6),
             (9.0, 8.4, -2.0), (3.6, 6.2, 13.4), (3.6, 4.2, 20.0), (0.4, 3.2, 23.6), (5.0, 10.2, -2.0)]], 'paint', bevel=0.22)
    # high sloping spine (fused sail): dark, team top stripe
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.4, 10.4, 6.0), (5.4, 12.0, -6.0), (5.0, 11.0, -20.4),
             (1.8, 15.8, -9.0), (1.8, 15.4, -14.6), (1.6, 11.4, 5.0), (2.4, 12.4, -20.6)]], 'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(1.35, 15.62, -8.6), (1.35, 15.3, -14.2), (1.2, 13.4, -1.0),
             (1.3, 15.8, -8.6), (1.3, 15.48, -14.2), (1.15, 13.58, -1.0)]], 'team', bevel=0.03)
    b.cyl((0, 15.6, -10.6), (0, 18.4, -11.0), 0.36, 8, 'dark', r2=0.26)
    b.cyl((0, 18.4, -11.0), (0, 18.7, -11.0), 0.26, 6, 'lightr')
    # light snout plate (pointed, reads as the head of the snake)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.0, 6.1, 13.6), (2.6, 4.2, 19.6), (0.2, 3.3, 23.0), (2.4, 7.2, 8.0),
             (3.0, 6.3, 13.6), (2.6, 4.4, 19.6), (0.2, 3.5, 23.0), (2.4, 7.4, 8.0)]], 'steel', bevel=0.05)
    b.box((-0.9, 3.9, 21.5), (0.9, 4.4, 22.2), 'lightc', bevel=0.0)
    # ------------------------------------------------------------------ shoulder torpedo blisters (steel, glazed)
    bl = [(7.0, 3.0, -16.8), (12.4, 4.0, -18.6), (15.2, 5.8, -2.0), (14.0, 6.2, 3.4), (9.0, 4.2, 3.6),
          (7.4, 9.2, -16.0), (11.8, 9.4, -17.8), (14.8, 9.4, -2.0), (13.0, 8.8, 3.0), (9.4, 11.4, -2.4), (8.4, 8.6, 2.8)]
    b.hull(bl, 'steel', bevel=0.2, mirror=True)
    b.hull([(x, y, z) for x, y, z in
            [(9.4, 9.9, -14.6), (12.0, 9.8, -15.8), (13.6, 9.6, -3.4), (9.8, 11.2, -3.4),
             (9.4, 10.08, -14.6), (12.0, 9.98, -15.8), (13.6, 9.78, -3.4), (9.8, 11.38, -3.4)]], 'team', bevel=0.03, mirror=True)
    # dark glazed launch faces at the front of the blisters (tube1/tube2 at x 10.62, y 7.94, z 2.64)
    b.hull([(x, y, z) for x, y, z in
            [(8.8, 5.0, 3.0), (13.8, 6.6, 3.0), (9.6, 10.2, 2.4), (13.2, 8.8, 2.4),
             (8.8, 5.0, 3.5), (13.8, 6.6, 3.6), (9.6, 10.2, 2.9), (13.2, 8.8, 2.9)]], 'glass', bevel=0.04, mirror=True)
    b.cyl((10.62, 7.94, 2.8), (10.62, 7.94, 3.9), 1.25, 10, 'black', mirror=True)
    # ------------------------------------------------------------------ swept fins under the snout (dark)
    b.hull([(x, y, z) for x, y, z in
            [(5.0, 1.6, 5.0), (11.6, 0.4, 11.0), (12.8, 0.4, 16.6), (4.6, 1.8, 13.0),
             (5.0, 2.4, 5.0), (11.6, 0.9, 11.0), (12.8, 0.9, 16.6), (4.6, 2.6, 13.0)]], 'paint2', bevel=0.1, mirror=True)
    # ------------------------------------------------------------------ stern: twin dark jet nozzles around the wake point
    for x in (4.2,):
        b.cyl((x, 4.0, -23.0), (x, 4.0, -26.2), 2.0, 10, 'dark', r2=1.6, bevel=0.06, mirror=True)
        b.cyl((x, 4.0, -26.15), (x, 4.0, -26.3), 1.2, 10, 'lightr', mirror=True)
    # aft fins
    b.hull([(x, y, z) for x, y, z in
            [(8.0, 6.0, -18.0), (14.6, 6.4, -23.4), (14.6, 6.4, -26.2), (7.6, 6.0, -24.4),
             (8.0, 7.4, -18.0), (14.6, 7.2, -23.4), (14.6, 7.2, -26.2), (7.6, 7.4, -24.4)]], 'paint2', bevel=0.1, mirror=True)
