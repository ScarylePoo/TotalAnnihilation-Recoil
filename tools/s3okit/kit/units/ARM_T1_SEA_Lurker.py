"""Lurker (ARM_T1_SEA_Lurker) - Arm submarine. A hammerhead: a slim light cigar hull with two big blunt torpedo
pods flaring out either side of the bow (the TA model's tell, wider than the hull is long at the front), a low dark
sail amidships with a team-coloured top, swept dark diving planes aft and a cruciform tail with a shrouded
propeller. Seen through 40 elmos of water, so only big value blocks: light hull + pods, dark sail/planes/tail,
team on the sail and the pod tops; no fine detail.
Pieces (TA layout): base, tail (empty: wake emit point), flare1/2 (empty: torpedo launch points in the pods).
Submarine, waterline 40 (water surface 40 above the model origin).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=4),
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ cigar hull (crosses x = 0): octagonal sections
    def sect(z, r, h, yc=7.0):
        return [(math.cos(a) * r, yc + math.sin(a) * h, z) for a in [i * math.pi / 4 + math.pi / 8 for i in range(8)]]
    b.hull(sect(-22.0, 2.6, 2.4) + sect(-14.0, 5.6, 4.6) + sect(-2.0, 6.6, 5.4), 'paint', bevel=0.2)
    b.hull(sect(-2.0, 6.6, 5.4) + sect(12.0, 6.4, 5.2) + sect(20.4, 3.4, 3.2, 6.6), 'paint', bevel=0.2)
    # dark dorsal deck strip along the spine (the hull's centre line reads as a dark stroke)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(1.6, 12.2, -14.0), (1.6, 12.3, 12.0), (1.2, 11.2, 17.4), (1.6, 11.6, -17.0),
             (1.5, 12.48, -14.0), (1.5, 12.58, 12.0)]], 'paint2', bevel=0.04)
    # ------------------------------------------------------------------ hammerhead torpedo pods (big, blunt, light)
    pod = [(7.4, 0.6, -1.6), (19.0, 0.6, 3.8), (19.0, 0.6, 16.6), (7.4, 0.6, 23.8),
           (7.4, 11.2, 4.6), (13.6, 11.2, 7.4), (13.6, 11.2, 13.8), (7.4, 11.2, 17.4),
           (17.8, 7.0, 4.8), (17.8, 7.0, 16.0), (7.4, 7.4, 22.2), (7.4, 7.4, -0.4)]
    b.hull(pod, 'paint', bevel=0.22, mirror=True)
    # pod tops: team plates
    b.hull([(x, y, z) for x, y, z in
            [(8.4, 11.15, 5.8), (12.8, 11.15, 8.2), (12.8, 11.15, 13.2), (8.4, 11.15, 16.2),
             (8.4, 11.35, 5.8), (12.8, 11.35, 8.2), (12.8, 11.35, 13.2), (8.4, 11.35, 16.2)]], 'team', bevel=0.04, mirror=True)
    # dark pod faces + black torpedo tube mouths at the front (flare1/flare2 sit in these)
    b.hull([(x, y, z) for x, y, z in
            [(9.0, 2.0, 22.4), (17.4, 2.0, 17.4), (9.0, 9.6, 19.0), (12.6, 9.6, 15.6),
             (9.0, 2.0, 23.0), (17.6, 2.0, 17.8), (9.0, 9.6, 19.5), (12.8, 9.6, 16.0)]], 'paint2', bevel=0.06, mirror=True)
    for x, y in ((11.0, 5.6), (14.4, 4.6)):
        b.cyl((x, y, 19.8 - (x - 9.0) * 0.55), (x, y, 21.6 - (x - 9.0) * 0.55), 1.1, 10, 'black', mirror=True)
    # pod-to-hull pylons (dark)
    b.box((5.6, 3.6, 3.0), (8.0, 8.6, 16.0), 'paint2', bevel=0.12, mirror=True)
    # ------------------------------------------------------------------ sail (dark, team top)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.4, 11.4, -6.8), (4.4, 11.4, 1.0), (2.8, 11.4, 7.6),
             (2.6, 16.4, -5.0), (3.4, 16.4, 0.8), (2.0, 16.4, 5.4)]], 'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.4, 16.35, -4.4), (3.0, 16.35, 0.8), (1.7, 16.35, 4.8),
             (2.3, 16.55, -4.3), (2.9, 16.55, 0.8), (1.6, 16.55, 4.7)]], 'team', bevel=0.04)
    b.cyl((0.0, 16.5, -2.6), (0.0, 19.6, -2.8), 0.4, 8, 'dark', r2=0.3)
    b.cyl((0.0, 19.6, -2.8), (0.0, 19.9, -2.8), 0.3, 6, 'lightc')
    # sail planes
    b.hull([(x, y, z) for x, y, z in
            [(3.0, 14.2, 2.6), (8.4, 14.2, 1.0), (3.0, 14.2, -1.4), (8.0, 14.2, -0.4),
             (3.0, 14.9, 2.6), (8.4, 14.6, 1.0), (3.0, 14.9, -1.4), (8.0, 14.6, -0.4)]], 'paint2', bevel=0.08, mirror=True)
    # ------------------------------------------------------------------ swept diving planes aft (dark, big)
    b.hull([(x, y, z) for x, y, z in
            [(5.0, 6.6, -5.4), (11.6, 7.4, -8.0), (11.6, 7.4, -16.6), (4.4, 6.6, -18.6),
             (5.0, 8.8, -5.4), (11.6, 9.0, -8.0), (11.6, 9.0, -16.6), (4.4, 8.6, -18.6)]], 'paint2', bevel=0.14, mirror=True)
    b.box((11.4, 7.6, -15.6), (11.75, 8.6, -9.0), 'lightc', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ cruciform tail + shrouded prop (tail emit at z -23.75)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(0.6, 8.6, -15.6), (0.6, 14.4, -19.2), (0.6, 14.4, -23.2), (0.6, 8.6, -22.0)]], 'paint2', bevel=0.12)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(0.6, 5.4, -15.6), (0.6, 0.6, -19.4), (0.6, 0.6, -23.0), (0.6, 5.4, -22.0)]], 'paint2', bevel=0.12)
    b.cyl((0, 7.0, -21.4), (0, 7.0, -24.6), 4.6, 12, 'paint2', r2=4.2, bevel=0.1)
    b.cyl((0, 7.0, -24.55), (0, 7.0, -24.7), 3.4, 12, 'black')
    for a in (0, 60, 120):
        t = math.radians(a)
        b.hull([(math.cos(t) * r + dx, 7.0 + math.sin(t) * r + dy, z)
                for r in (-3.2, 3.2) for z in (-23.2, -23.8) for dx, dy in ((-math.sin(t) * 0.45, math.cos(t) * 0.45),
                                                                              (math.sin(t) * 0.45, -math.cos(t) * 0.45))],
               'dark', bevel=0.0)
    b.cyl((0, 7.0, -22.0), (0, 7.0, -25.2), 1.0, 8, 'dark', r2=0.4)
