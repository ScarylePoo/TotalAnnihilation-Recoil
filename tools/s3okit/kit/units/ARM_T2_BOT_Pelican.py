"""Pelican (ARM_T2_BOT_Pelican) - Arm T2 amphibious kbot (hover movement class: it walks on land and rides the water
surface). A boat hull on two legs: pointed bow, flared sides with a dark lower hull band, a laser turret amidships
and a twin missile pod on a pylon at the stern. TA's 3DO has two legs on hip pivots (inspect guessed quad): standard
BIPED skeleton. In water it folds its legs out to the sides like outriggers and drops onto the surface; script ported
to scripts/ARM_T2_BOT_Pelican.lua. The pontoons piece is never shown by the COB: kept empty, as are the wake emitters.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Pelican): a long light pointed boat hull with team side stripes, a dark turret dot and a
light missile block at the stern - the only Arm kbot that reads as a vessel."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=8.4, drop=['lhippivot', 'rhippivot']),
    res=1024,
    wreck=dict(seed=15, drop=['misturret'], remove=[]),
    preview_pose={'lasturret': (0, -20, 0)},
)


def build(k):
    k.standard_legs(width=1.45)

    # ------------------------------------------------------------------ pelvis (0, 19, 0): hip bar across the hull
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, -2.2, -1.5), (7.6, -2.2, 1.3), (7.6, 0.2, -1.5), (7.6, 0.2, 1.3), (5.0, -2.6, -1.2), (5.0, -2.6, 1.0)]],
           'paint2', bevel=0.12)

    # ------------------------------------------------------------------ body (0, 12.5, -2): boat hull
    b = k.piece('body'); B = b.at
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # lower hull (dark band)
            [(1.0, -2.0, -12.0), (1.0, -2.0, 9.0), (0.2, -1.4, 14.0), (5.8, 2.6, -13.4), (6.2, 2.6, 7.4), (2.0, 2.6, 15.4)]],
           'paint2', bevel=0.18)
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # upper hull
            [(5.8, 2.6, -13.4), (6.2, 2.6, 7.4), (2.0, 2.6, 15.4), (5.6, 6.4, -13.8), (5.4, 6.4, 6.8), (1.6, 5.4, 15.0),
             (0.4, 4.6, 16.4)]], 'paint', bevel=0.2)
    b.hull([B(x, y, z) for x, y, z in                                                    # team side stripes on the deck
            [(3.4, 6.42, -12.6), (5.1, 6.42, -12.6), (3.4, 6.42, 5.8), (4.9, 6.42, 5.6),
             (3.4, 6.58, -12.55), (5.05, 6.58, -12.55), (3.4, 6.58, 5.75), (4.85, 6.58, 5.55)]], 'team', bevel=0.03, mirror=True)
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # dark bow plate
            [(1.4, 5.5, 13.6), (3.0, 6.36, 9.0), (1.4, 5.66, 13.55), (3.0, 6.52, 8.95), (0.3, 4.7, 16.2), (0.3, 4.85, 16.15)]],
           'dark', bevel=0.04)
    for sx in (-1, 1):
        b.box(B(sx * 2.0 - 0.5, 5.0, 14.3), B(sx * 2.0 + 0.5, 5.5, 14.7), 'lightw', bevel=0.0)   # bow lights
    # stern: two water jets
    for sx in (-2.6, 2.6):
        b.cyl(B(sx, 1.0, -13.4), B(sx, 1.0, -15.2), 1.5, 10, 'dark', bevel=0.06)
        b.cyl(B(sx, 1.0, -15.15), B(sx, 1.0, -15.3), 1.0, 10, 'black')
    # missile pylon at the stern
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 6.3, -13.0), (1.6, 6.3, -8.6), (1.2, 11.3, -12.4), (1.2, 11.3, -9.6)]], 'dark', bevel=0.1)

    # ------------------------------------------------------------------ laser turret (0, 19, -2.5)
    t = k.piece('lasturret'); T = t.at
    t.cyl(T(0, -0.4, 0), T(0, 1.6, 0), 3.2, 12, 'dark', bevel=0.08)
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 1.5, -2.4), (2.6, 1.5, 2.2), (1.8, 3.8, -1.8), (1.8, 3.8, 1.4), (1.4, 2.4, 3.4)]], 'paint', bevel=0.14)
    t.box(T(-1.2, 3.75, -1.4), T(1.2, 3.92, 1.0), 'team', bevel=0.03)
    l = k.piece('lasbarrel'); L = l.at                 # (0, 21, -1): muzzle (flare) at (0, 0.25, 9.25)
    l.box(L(-1.4, -1.0, -0.4), L(1.4, 1.4, 2.6), 'dark', bevel=0.08)
    l.cyl(L(0, 0.25, 2.4), L(0, 0.25, 9.0), 0.65, 10, 'steel')
    l.cyl(L(0, 0.25, 8.6), L(0, 0.25, 9.3), 0.9, 10, 'dark')

    # ------------------------------------------------------------------ missile pod (0, 24.1, -12.29)
    m = k.piece('misturret'); M = m.at
    m.hull([M(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -0.4, -6.8), (5.4, -0.4, 1.0), (5.2, 3.0, -6.6), (5.2, 3.0, 0.8), (4.4, 1.4, -7.4)]], 'paint', bevel=0.18)
    m.box(M(-1.0, -0.42, -5.6), M(1.0, 3.1, 0.6), 'paint2', bevel=0.06)                 # centre spine
    for sx in (-4.25, 4.25):                                                          # launch tubes
        m.cyl(M(sx, 2.03 - 0.6, 0.0), M(sx, 2.03 - 0.6, 1.2), 1.2, 10, 'dark', bevel=0.04)
        m.cyl(M(sx, 1.43, 1.15), M(sx, 1.43, 1.3), 0.8, 10, 'black')
    m.box(M(-4.6, 3.0, -5.6), M(-2.0, 3.15, -0.6), 'hazard', bevel=0.02)
    m.box(M(2.0, 3.0, -5.6), M(4.6, 3.15, -0.6), 'hazard', bevel=0.02)
