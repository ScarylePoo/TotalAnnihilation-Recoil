"""Parasite (CORE_T2_BOT_Parasite) - Core T2 spy kbot. A flat, sloped stealth wedge (the `head` piece is the whole
body) carried low between two widely set legs: a faceted dart-shaped shell with a team spine ridge, a red sensor slit
in its nose and vents at the tail. TA's 3DO has two legs with toes and heels (inspect guessed quad): standard BIPED
skeleton, heels dropped too. Script ported to scripts/CORE_T2_BOT_Parasite.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Parasite): a long flat dark-warm arrowhead with team-plated slopes and spine, straddled by two dark legs -
low and wide, with no guns at all."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=7.0, drop=['rheel', 'lheel']),
    res=1024,
    wreck=dict(seed=29, drop=[], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(thigh='paint2', shin='dark', foot='dark', width=1.45)

    # ------------------------------------------------------------------ pelvis (0, 14.25, 0): hip bar under the shell
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.2, -1.6, -2.0), (6.2, -1.6, 1.8), (6.2, 1.2, -2.0), (6.2, 1.2, 1.8), (3.0, -2.4, -2.6), (3.0, 1.0, -2.6)]],
           'dark', bevel=0.14)

    # ------------------------------------------------------------------ head (0, 14, -3.5): the stealth wedge body
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, 0.4, -10.6), (6.8, 0.4, 3.0), (5.4, 1.0, -12.4), (2.6, 0.6, 15.6), (4.6, 3.4, -10.0), (4.4, 3.6, 2.4),
             (1.6, 7.4, -6.8), (1.2, 6.2, 4.4), (0.8, 2.2, 15.8)]], 'paint', bevel=0.2)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # dark belly band
            [(6.7, 0.2, -10.4), (6.9, 0.2, 2.8), (2.7, 0.4, 15.4), (6.0, 1.4, -10.6), (6.2, 1.4, 2.8), (2.4, 1.2, 15.2)]],
           'paint2', bevel=0.08)
    h.hull([H(x, y, z) for x in (-0.6, 0.6) for y, z in [(7.3, -6.6), (8.2, -5.4), (6.9, 4.2), (6.1, 4.6)]], 'team', bevel=0.06)   # team spine
    R1, S1, R2, S2 = (1.6, 7.4, -6.8), (4.6, 3.4, -10.0), (1.2, 6.2, 4.4), (4.4, 3.6, 2.4)   # one slope face
    lerp = lambda p, q, t: tuple(p[i] + (q[i] - p[i]) * t for i in range(3))
    for sx in (-1, 1):                                                                   # team plates on the slopes
        pts = []
        for P_, Q_ in ((R1, S1), (R2, S2)):
            for t in (0.05, 0.93):
                x, y, z = lerp(P_, Q_, t)
                pts += [H(sx * x, y + 0.12, z), H(sx * x, y + 0.26, z)]
        h.hull(pts, 'team', bevel=0.03)
    h.box(H(-0.9, 0.9, 15.45), H(0.9, 1.7, 15.95), 'lightr', bevel=0.0)                # red sensor slit
    for x in (-3.0, 0.0, 3.0):                                                           # tail vents
        h.box(H(x - 0.8, 1.0, -12.0), H(x + 0.8, 2.8, -11.4), 'black', bevel=0.0)
