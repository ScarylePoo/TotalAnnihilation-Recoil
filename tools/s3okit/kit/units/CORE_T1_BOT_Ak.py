"""A.K. (CORE_T1_BOT_Ak) - Core light infantry kbot. Modelled to the third-party conscript S3O's piece layout (its
COB drives those pieces; the original is preserved in tools/s3okit/ref/ on install): a stocky hunched torso with a
crested head, two angular shoulder pods (lshoulder / rshoulder pitch to aim) each with a light laser gun slung under
it (lgun / rgun, fire points lfire / rfire at the muzzles). Standard biped skeleton; script ported to
scripts/CORE_T1_BOT_Ak.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it an A.K.): a compact dark warm body whose read is the crest - an ochre/team stripe running
front to back over the head and back - flanked by two angular dark pods with LIGHT steel guns poking out ahead of
them. Smaller and simpler than the Storm/Thud; team colour on the pod tops, not the chest (the Peewee's layout)."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.2),
    res=1024,
    wreck=dict(seed=13, drop=['rgun'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.5)

    # ------------------------------------------------------------------ torso (-0.07, 13.46, 0.94)
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -2.0, -0.6), A(0, 0.8, -0.6), 2.4, 10, 'dark', bevel=0.08)                   # waist
    # stocky hunched chest: wide shoulders, deep, leaning forward
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 0.4, -3.6), (3.0, 0.4, 3.6), (4.4, 4.6, -5.0), (4.4, 4.6, 4.8),
             (3.8, 8.0, -4.4), (3.4, 8.0, 3.0), (2.6, 6.4, 6.2)]], 'paint', bevel=0.2)
    # darker belly / groin armour
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 0.6, 3.5), (3.4, 3.8, 5.0), (2.4, 0.8, 3.8), (3.2, 3.8, 5.3)]], 'paint2', bevel=0.08)
    # head: low wedge, sunk between the shoulders, with a crest
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 7.6, -1.6), (2.0, 7.6, 4.0), (1.6, 10.4, -1.0), (1.4, 10.0, 2.8), (1.0, 8.6, 5.4)]], 'paint', bevel=0.14)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                                    # visor (warm)
            [(1.5, 8.6, 4.5), (1.2, 9.4, 3.6), (1.5, 8.75, 4.7), (1.2, 9.55, 3.8)]], 'dark', bevel=0.03)
    t.box(A(-1.1, 8.95, 4.25), A(1.1, 9.25, 4.45), 'lightr', bevel=0.0)
    # crest: team-coloured ridge over the head and down the back (the A.K. read from above)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.7, 10.3, -1.0), (0.7, 10.0, 2.8), (0.5, 11.4, -0.4), (0.5, 11.0, 2.0),
             (0.7, 8.2, -4.6), (0.5, 9.0, -4.2)]], 'team', bevel=0.06)
    # back pack (dark) with an antenna
    t.box(A(-2.8, 1.6, -6.6), A(2.8, 6.8, -4.2), 'dark', bevel=0.14)
    t.cyl(A(-1.8, 6.8, -5.6), A(-1.8, 7.3, -5.6), 0.32, 8, 'dark')
    t.cyl(A(-1.8, 7.3, -5.6), A(-1.8, 11.2, -5.8), 0.1, 6, 'steel', r2=0.05)
    t.cyl(A(-1.8, 11.2, -5.8), A(-1.8, 11.4, -5.8), 0.16, 6, 'lightr')

    # ------------------------------------------------------------------ left shoulder pod (cloned to the right)
    s = k.piece('lshoulder'); S = s.at                  # (4.33, 18.25, 0); gun mount at local (3.57, -2.32, 0)
    s.cyl(S(-0.6, 0, 0), S(1.2, 0, 0), 1.8, 10, 'dark', bevel=0.06)                           # joint
    s.hull([S(x, y, z) for x, y, z in                                                          # angular pod
            [(0.8, -1.6, -4.6), (0.8, -1.6, 4.6), (6.8, -1.8, -4.2), (6.8, -1.8, 4.2),
             (1.2, 2.2, -3.8), (1.2, 2.2, 3.4), (6.0, 2.6, -3.4), (6.0, 2.6, 3.0),
             (4.0, 1.2, 5.6)]], 'paint2', bevel=0.18)
    s.hull([S(x, y, z) for x, y, z in                                                          # team plate on top
            [(1.5, 2.26, -3.3), (5.7, 2.62, -2.9), (1.5, 2.26, 3.0), (5.7, 2.62, 2.7),
             (1.5, 2.44, -3.25), (5.7, 2.8, -2.85), (1.5, 2.44, 2.95), (5.7, 2.8, 2.65)]], 'team', bevel=0.03)
    g = k.piece('lgun'); G = g.at                       # (7.9, 15.93, 0); muzzle lfire at local (0, -3, 13)
    g.box(G(-1.6, -4.4, -3.6), G(1.6, -0.2, 5.0), 'steel', bevel=0.14)                        # LIGHT receiver
    g.cyl(G(0, -3.0, 4.6), G(0, -3.0, 12.6), 0.95, 10, 'steel')                                # LIGHT barrel
    g.cyl(G(0, -3.0, 7.0), G(0, -3.0, 7.6), 1.05, 10, 'dark', bevel=0.03)
    g.cyl(G(0, -3.0, 12.4), G(0, -3.0, 13.2), 1.0, 8, 'dark', rot=math.pi / 8, bevel=0.04)
    g.cyl(G(0, -3.0, 13.15), G(0, -3.0, 13.3), 0.5, 8, 'lightr')
    g.box(G(-0.5, -0.4, 0.0), G(0.5, 0.2, 3.0), 'steel', bevel=0.04)                         # cooling rail
    k.clone('rshoulder', 'lshoulder', mirror_x=True)
    k.clone('rgun', 'lgun', mirror_x=True)
