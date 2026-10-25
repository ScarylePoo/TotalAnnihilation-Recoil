"""Crasher (CORE_T1_BOT_Crasher) - Core missile (anti-air) kbot. Modelled to the third-party S3O's piece layout (its COB
drives those pieces; the original is preserved in tools/s3okit/ref/ on install): a squat walker whose upper body
(turret) is a heavy horseshoe yoke, open at the front, cradling a big round missile drum (gunbase pitches to aim)
with two short launch tubes (gun1 / gun2 recoil) poking out of its face. Standard biped skeleton (short legs: the
pelvis sits at 7.4 like the original); script ported to scripts/CORE_T1_BOT_Crasher.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Crasher): a dark warm U with team plates on its two arms, and a LIGHT steel ball sitting
in the U - the only round silhouette among the Core kbots, with two dark tube mouths at the open end."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=5.4),
    res=1024,
    wreck=dict(seed=14, drop=['gunbase'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.9)

    # ------------------------------------------------------------------ pelvis (0, 7.38, 0.11): hip box
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, -2.2, -3.6), (4.4, -2.2, 3.4), (5.6, 1.8, -4.4), (5.6, 1.8, 4.0), (2.8, -3.4, -2.0), (2.8, -3.4, 2.0)]],
           'paint2', bevel=0.16)

    # ------------------------------------------------------------------ turret (0, 10.38, -0.19): horseshoe yoke
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.0, 0), A(0, 1.2, 0), 4.6, 14, 'dark', bevel=0.08)                           # turret ring
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                                    # base plate
            [(6.0, 1.2, -6.6), (6.0, 1.2, 3.2), (5.2, 3.2, -6.0), (5.2, 3.2, 2.6)]], 'paint', bevel=0.18)
    # rear arch of the U (behind the drum)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 3.0, -10.6), (6.4, 3.0, -7.0), (5.6, 14.6, -9.6), (5.6, 14.6, -6.8), (2.0, 16.0, -9.0), (2.0, 16.0, -6.8)]],
           'paint', bevel=0.2)
    # the two arms of the U, sweeping forward either side of the drum (built once, mirrored)
    t.hull([A(x, y, z) for x, y, z in
            [(6.4, 3.0, -9.0), (10.8, 3.0, -6.0), (6.4, 3.0, 3.0), (10.8, 3.0, 2.8),
             (6.6, 14.0, -7.4), (9.8, 14.0, -5.0), (6.6, 13.0, 2.6), (9.8, 13.0, 2.0),
             (8.8, 8.0, 4.2), (11.0, 8.0, -1.6)]], 'paint', bevel=0.22, mirror=True)
    t.hull([A(x, y, z) for x, y, z in                                                           # team plate on the arm top
            [(7.2, 13.98, -5.8), (9.2, 13.98, -4.4), (7.2, 13.16, 1.8), (9.2, 13.16, 1.4),
             (7.2, 14.14, -5.75), (9.2, 14.14, -4.35), (7.2, 13.32, 1.75), (9.2, 13.32, 1.35)]], 'team', bevel=0.03, mirror=True)
    t.hull([A(x, y, z) for x, y, z in                                                           # ochre hazard arm tips
            [(8.9, 8.1, 4.12), (10.9, 8.1, -1.5), (6.7, 12.9, 2.62), (9.7, 12.9, 2.08),
             (9.05, 8.1, 4.3), (11.05, 8.1, -1.35), (6.8, 12.9, 2.8), (9.8, 12.9, 2.25)]], 'hazard', bevel=0.02, mirror=True)
    # trunnion bosses holding the drum
    t.cyl(A(6.6, 8.6, 0.2), A(5.0, 8.6, 0.2), 2.0, 10, 'dark', bevel=0.06, mirror=True)
    # back pack: exhaust vents on the rear arch
    for y in (5.0, 7.0, 9.0):
        t.box(A(-4.0, y, -10.9), A(4.0, y + 0.8, -10.5), 'black', bevel=0.0)

    # ------------------------------------------------------------------ gunbase (0, 18.98, 0.01): LIGHT missile drum
    g = k.piece('gunbase'); G = g.at
    g.sphere(G(0, 0, 0), 6.0, 'steel', segs=14, rings=9, scale=(1.0, 1.0, 1.05))
    g.cyl(G(5.2, 0, 0), G(6.0, 0, 0), 2.6, 12, 'dark', bevel=0.04, mirror=True)               # side hubs
    g.cyl(G(0, 0, 4.6), G(0, 0, 6.6), 4.6, 12, 'dark', bevel=0.08)                            # face plate
    g.box(G(-0.5, 5.6, -3.0), G(0.5, 6.4, 3.0), 'dark', bevel=0.05)                           # top seam rib

    # ------------------------------------------------------------------ launch tubes (gun2 cloned mirrored)
    a = k.piece('gun1'); B = a.at                       # (3.86, 18.78, 7.39), firept1 at z +4
    a.cyl(B(0, 0, -1.0), B(0, 0, 3.9), 1.7, 10, 'dark', bevel=0.06)
    a.cyl(B(0, 0, 3.8), B(0, 0, 4.1), 1.95, 10, 'dark', bevel=0.03)
    a.cyl(B(0, 0, 4.05), B(0, 0, 4.15), 1.1, 10, 'black')
    a.cyl(B(0, 0, 3.4), B(0, 0, 4.0), 0.75, 8, 'steel', r2=0.2)                               # missile nose
    k.clone('gun2', 'gun1', mirror_x=True)
