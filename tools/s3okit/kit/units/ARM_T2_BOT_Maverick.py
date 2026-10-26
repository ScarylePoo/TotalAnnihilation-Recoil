"""Maverick (ARM_T2_BOT_Maverick) - Arm T2 "gun-slinging" kbot. A tall, lean gunslinger: angular pauldrons, a tall
visored helmet, long arms, and two pistols carried in hip holsters. To fight it opens the holster doors, swings the
pistols out, reaches down and draws them (the hand guns appear), then aims with the arms held out; idle it holsters
them again. TA hid the pistols inside its legs; on the standard biped skeleton the old leg shells (rlegmain/llegmain)
are kept as static hip HOLSTERS hanging off the pelvis, with their doors (r/llegdoor) and holstered pistols
(r/lgunhide) inside, outside the new legs' swing. Script ported to scripts/ARM_T2_BOT_Maverick.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Maverick): narrow tall body, two square light pauldrons with team tops, two holster slabs
with team caps at the hips - a cowboy's double holster - and dark arms."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.4, keep=['rlegmain', 'llegmain', 'rlegdoor', 'llegdoor']),
    res=1024,
    always_visible=['rgunbase', 'lgunbase', 'rgunbarrel', 'lgunbarrel', 'rgunshaft', 'lgunshaft'],
    wreck=dict(seed=7, drop=['luparm'], remove=['rgunbase', 'lgunbase', 'rgunshaft', 'lgunshaft', 'rgunbarrel', 'lgunbarrel']),
    # holstered (the idle state): hand guns hidden
    preview_pose={'rgunbase': 'hide', 'lgunbase': 'hide', 'rgunshaft': 'hide', 'lgunshaft': 'hide',
                  'rgunbarrel': 'hide', 'lgunbarrel': 'hide'},
)


def build(k):
    k.standard_legs(width=1.25)

    # ------------------------------------------------------------------ pelvis (0, 19, 0): hips + waist
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -2.6, -5.0), (3.0, -2.6, 0.6), (3.6, 1.6, -5.6), (3.6, 1.6, 1.2), (2.0, -3.6, -4.0), (2.0, -3.6, 0.0)]],
           'paint2', bevel=0.18)
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 1.4, -4.6), (2.4, 1.4, 0.2), (2.8, 6.4, -5.0), (2.8, 6.4, 0.4)]], 'dark', bevel=0.14)   # waist
    for sx in (-1, 1):                                                                 # holster straps
        p.box(Q(sx * 3.2, -1.6, -3.6), Q(sx * 7.1, -0.4, -1.4), 'dark', bevel=0.06)

    # ------------------------------------------------------------------ torso (0, 27.25, -2.5)
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, -2.0, -3.6), (4.6, -2.0, 4.0), (6.6, 3.0, -5.0), (6.6, 3.0, 5.2), (5.8, 5.8, -4.6),
             (5.8, 5.8, 3.6), (3.4, 0.6, 6.0)]], 'paint', bevel=0.22)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                          # chest plate
            [(2.4, 0.6, 5.85), (3.6, 3.6, 5.1), (2.4, 0.6, 6.05), (3.6, 3.6, 5.3)]], 'paint2', bevel=0.05)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                          # back pack
            [(4.2, 0.0, -4.0), (4.2, 5.2, -4.4), (3.6, 0.6, -7.0), (3.6, 4.6, -7.0)]], 'paint2', bevel=0.16)
    for x in (-2.2, 0.0, 2.2):
        t.cyl(A(x, 4.4, -6.2), A(x, 6.8, -6.2), 0.55, 8, 'dark')                     # exhaust stubs
        t.cyl(A(x, 6.75, -6.2), A(x, 6.9, -6.2), 0.35, 8, 'black')

    # ------------------------------------------------------------------ head (0, 35, 1.25): tall visored helmet
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -3.6, -4.2), (3.0, -3.6, 2.6), (3.2, 1.2, -4.4), (3.0, 1.6, 2.8), (2.2, 3.2, -3.4), (2.0, 3.0, 1.6),
             (2.2, -1.4, 3.6)]], 'paint', bevel=0.2)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                          # visor band
            [(2.6, -0.6, 3.1), (2.8, 1.0, 2.8), (2.1, -0.6, 3.7), (2.3, 0.9, 3.35)]], 'dark', bevel=0.05)
    h.box(H(-1.8, -0.1, 3.5), H(1.8, 0.5, 3.75), 'lightc', bevel=0.0)
    h.hull([H(x, y, z) for x in (-0.6, 0.6) for y, z in                              # dark crest
            [(3.1, 1.4), (3.5, 0.4), (3.5, -3.0), (3.0, -3.8)]], 'dark', bevel=0.06)

    # ------------------------------------------------------------------ right arm (left arm = mirrored clones)
    s = k.piece('rshoulder'); S = s.at                 # (-5, 31, -2.5)
    s.cyl(S(0.4, 0, 0), S(-1.4, 0, 0), 2.0, 10, 'dark', bevel=0.06)
    s.hull([S(x, y, z) for x, y, z in                                                  # angular pauldron
            [(-1.0, -4.2, -3.8), (-1.0, -4.2, 3.6), (-7.2, -4.6, -3.6), (-7.2, -4.6, 3.4),
             (-1.4, 3.0, -3.4), (-1.4, 3.0, 3.2), (-6.4, 3.6, -3.2), (-6.4, 3.6, 3.0), (-7.6, 0.0, 0.0)]], 'paint', bevel=0.2)
    s.hull([S(x, y, z) for x, y, z in                                                  # team top plate
            [(-1.8, 3.12, -2.8), (-1.8, 3.12, 2.6), (-6.0, 3.6, -2.6), (-6.0, 3.6, 2.4),
             (-1.8, 3.28, -2.75), (-1.8, 3.28, 2.55), (-6.0, 3.76, -2.55), (-6.0, 3.76, 2.35)]], 'team', bevel=0.03)
    u = k.piece('ruparm'); U = u.at                    # (-11.25, 31.25, -2.5); elbow at (-1.88, -9, 0)
    u.hull([U(x, y, z) for x, y, z in
            [(-0.6, -3.0, -1.6), (-0.6, -3.0, 1.7), (-3.4, -3.0, -1.6), (-3.4, -3.0, 1.7),
             (-1.0, -9.0, -1.4), (-1.0, -9.0, 1.5), (-2.8, -9.0, -1.4), (-2.8, -9.0, 1.5)]], 'dark', bevel=0.12)
    a = k.piece('rarm'); R = a.at                      # (-13.12, 22.25, -2.5): forearm
    a.cyl(R(-1.6, 0, 0), R(1.6, 0, 0), 1.6, 10, 'dark', bevel=0.06)
    a.hull([R(x, y, z) for x, y, z in
            [(-1.9, -1.0, -1.9), (1.9, -1.0, -1.9), (-1.9, -1.0, 2.0), (1.9, -1.0, 2.0),
             (-2.3, -6.0, -2.2), (2.3, -6.0, -2.2), (-2.3, -6.0, 2.3), (2.3, -6.0, 2.3),
             (-1.8, -10.6, -1.7), (1.8, -10.6, -1.7), (-1.8, -10.6, 1.8), (1.8, -10.6, 1.8)]], 'paint2', bevel=0.16)
    a.hull([R(x, y, z) for x in (-1.5, 1.5) for y in (-10.4, -12.6) for z in (-1.4, 1.5)], 'dark', bevel=0.12)   # hand
    g = k.piece('rgunbase'); G = g.at                  # (-12.5, 11.5, -3): pistol frame, held at the hand
    g.hull([G(x, y, z) for x in (-1.2, 5.2) for y in (-1.4, 1.6) for z in (-1.7, 1.7)], 'paint2', bevel=0.16)
    g.hull([G(x, y, z) for x in (2.2, 5.2) for y in (-4.8, -1.2) for z in (-1.5, 1.5)], 'dark', bevel=0.12)
    g.box(G(-1.0, 1.55, -1.2), G(4.6, 1.8, 1.2), 'team', bevel=0.03)
    sh = k.piece('rgunshaft'); SH = sh.at              # (-8.75, 6.5, -3)
    sh.cyl(SH(0, 0.2, 0), SH(0, -1.7, 0), 1.0, 10, 'steel')
    b = k.piece('rgunbarrel'); B = b.at                # (-8.75, 4.7, -3): muzzle (flare1) at (0.62, -8.25, 0)
    b.cyl(B(0.3, 0.3, 0), B(0.3, -2.4, 0), 1.45, 10, 'dark', bevel=0.06)
    b.cyl(B(0.3, -2.3, 0), B(0.3, -8.0, 0), 0.9, 10, 'steel')
    b.cyl(B(0.3, -7.6, 0), B(0.3, -8.6, 0), 1.15, 10, 'dark', bevel=0.05)
    for n in ('shoulder', 'uparm', 'arm', 'gunbase', 'gunshaft', 'gunbarrel'):
        k.clone('l' + n, 'r' + n, mirror_x=True)

    # ------------------------------------------------------------------ hip holsters (static, off the pelvis)
    hl = k.piece('rlegmain'); L = hl.at                # (-2.5, 20.75, -2.5)
    hl.box(L(-5.15, -14.35, -3.9), L(-4.5, -2.15, 4.1), 'paint2', bevel=0.1)       # inner wall
    hl.box(L(-8.1, -3.35, -3.9), L(-4.5, -2.15, 4.1), 'paint', bevel=0.12)         # top cap
    hl.box(L(-7.75, -2.17, -3.4), L(-4.85, -2.0, 3.6), 'team', bevel=0.03)         # team plate on the cap
    hl.box(L(-8.1, -14.35, -3.9), L(-4.5, -13.15, 4.1), 'paint', bevel=0.12)       # bottom cap
    hl.box(L(-8.1, -13.2, -3.9), L(-4.5, -3.3, -3.3), 'paint', bevel=0.08)         # rear wall
    hl.box(L(-8.1, -13.2, 3.5), L(-4.5, -3.3, 4.1), 'paint', bevel=0.08)           # front wall
    hl.box(L(-7.9, -12.0, 4.05), L(-4.7, -11.2, 4.3), 'lightr', bevel=0.0)        # holster light
    d = k.piece('rlegdoor'); D = d.at                  # (-10.62, 12.16, -5.98): hinged at its rear edge
    d.box(D(-0.7, -5.8, 0.1), D(0.05, 5.8, 7.4), 'paint', bevel=0.1)
    d.box(D(-0.9, -3.6, 1.6), D(-0.65, 3.6, 5.8), 'hazard', bevel=0.03)
    gh = k.piece('rgunhide'); GH = gh.at               # (-7.75, 14.5, -2.5): holstered pistol, muzzle down
    gh.hull([GH(x, y, z) for x in (-1.75, -0.05) for y in (-1.6, 1.4) for z in (-1.6, 1.6)], 'paint2', bevel=0.12)
    gh.cyl(GH(-0.9, -1.4, 0), GH(-0.9, -6.4, 0), 0.75, 8, 'steel')
    gh.cyl(GH(-0.9, -5.8, 0), GH(-0.9, -6.6, 0), 0.95, 8, 'dark')
    k.clone('llegmain', 'rlegmain', mirror_x=True)
    k.clone('llegdoor', 'rlegdoor', mirror_x=True)
    k.clone('lgunhide', 'rgunhide', mirror_x=True)
