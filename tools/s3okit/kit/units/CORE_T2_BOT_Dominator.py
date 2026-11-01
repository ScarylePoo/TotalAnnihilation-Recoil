"""Dominator (CORE_T2_BOT_Dominator) - Core T2 heavy rocket kbot. A short heavy walker carrying a huge flat missile
box (Launcher) on its back; to fire, the box tips up 90 degrees so its tube face points at the sky (vertical launch).
Under the box: a sensor head with a jutting nose and the torso block. The missiles themselves are always hidden by the
script (Missile1/2 stay empty emit points inside the box). Standard biped skeleton, wide-set legs; script ported to
scripts/CORE_T2_BOT_Dominator.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Dominator): one big dark-warm square slab with a pair of wide team plates, ochre hazard
edges and a grid of black tube hatches on its front - a roof on legs, unlike any other Core kbot."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=7.4),
    res=1024,
    wreck=dict(seed=27, drop=[], remove=[], pose={'Launcher': (-20, 0, 0)}),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.75)

    # ------------------------------------------------------------------ pelvis (0, 14.61, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, -2.0, -3.0), (6.6, -2.0, 2.6), (6.6, 1.8, -3.4), (6.6, 1.8, 3.0), (3.6, -3.0, -2.4), (3.6, -3.0, 2.0)]],
           'paint2', bevel=0.18)

    # ------------------------------------------------------------------ torso (origin 0,0,0): block under the box
    t = k.piece('Torso')
    t.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 13.0, -7.0), (4.4, 13.0, 6.0), (4.6, 18.8, -8.2), (4.6, 18.8, 8.6), (3.0, 11.2, -5.0), (3.0, 11.2, 4.4),
             (3.0, 15.6, 9.6)]], 'paint', bevel=0.22)
    t.box((-2.6, 13.4, 8.4), (2.6, 16.6, 9.2), 'dark', bevel=0.08)
    for y in (14.0, 15.2):
        t.box((-2.2, y, 9.15), (2.2, y + 0.5, 9.35), 'black', bevel=0.0)

    # ------------------------------------------------------------------ head (origin 0,0,0): sensor nose
    h = k.piece('Head')
    h.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 18.8, -11.0), (4.4, 18.8, 10.0), (4.2, 20.6, -11.0), (4.2, 20.6, 10.0), (2.8, 19.0, 15.6),
             (2.4, 22.2, 14.8), (3.2, 22.6, 10.0)]], 'paint2', bevel=0.2)
    h.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in                             # dark visor wrap
            [(2.6, 20.0, 15.2), (2.2, 21.8, 14.6), (2.7, 19.8, 15.45), (2.3, 21.7, 14.85)]], 'dark', bevel=0.04)
    for sx in (-1.4, 1.4):
        h.cyl((sx, 20.8, 15.1), (sx, 20.8, 15.6), 0.5, 8, 'lightw')

    # ------------------------------------------------------------------ launcher (0, 22.99, -10.01): the missile box
    l = k.piece('Launcher'); L = l.at
    l.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(13.0, -3.6, -5.6), (13.0, -3.6, 19.4), (13.0, 4.6, -5.6), (13.0, 4.6, 19.4), (11.8, 5.4, -4.6),
             (11.8, 5.4, 18.4), (11.8, -4.3, -4.6), (11.8, -4.3, 18.4)]], 'paint', bevel=0.3)
    for sx in (-1, 1):                                                                  # team plates on the roof
        l.hull([L(sx * x, y, z) for x, y, z in
                [(3.6, 5.42, 0.0), (3.6, 5.42, 12.0), (10.0, 5.42, 0.0), (10.0, 5.42, 12.0),
                 (3.6, 5.58, 0.05), (3.6, 5.58, 11.95), (10.0, 5.58, 0.05), (10.0, 5.58, 11.95)]], 'team', bevel=0.03)
    l.box(L(-1.4, 5.3, -4.0), L(1.4, 5.9, 17.4), 'dark', bevel=0.06)                   # roof spine
    l.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # hazard frame on the tube face
            [(12.6, -3.4, 19.42), (12.6, 4.4, 19.42), (12.6, -3.4, 19.6), (12.6, 4.4, 19.6)]], 'hazard', bevel=0.04)
    for x in (-9.0, -4.5, 4.5, 9.0):                                                    # tube hatches
        for y in (-1.2, 2.6):
            l.cyl(L(x, y, 19.55), L(x, y, 19.9), 1.4, 10, 'dark')
            l.cyl(L(x, y, 19.85), L(x, y, 19.95), 0.9, 10, 'black')
    l.box(L(-12.0, -3.0, -5.9), L(12.0, 4.0, -5.4), 'paint2', bevel=0.08)              # rear plate
    for sx in (-1, 1):                                                                  # hinge lugs at the back
        l.cyl(L(sx * 6.0, 0, -0.6), L(sx * 4.2, 0, -0.6), 2.0, 10, 'dark', bevel=0.06)
