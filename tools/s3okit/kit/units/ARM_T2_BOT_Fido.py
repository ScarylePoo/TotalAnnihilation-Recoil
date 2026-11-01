"""Fido (ARM_T2_BOT_Fido) - Arm T2 gauss kbot, a four-legged "dog": a long low body (high rear hump = pelvis, lower
front chest with a sensor snout = torso) carrying a gauss cannon turret on the hump with a long twin-rail barrel
reaching past the snout. TA's 3DO walks on its "arms" as front legs, so it gets the standard QUAD skeleton (the old
arm pieces become rf/lf legs, the old legs rb/lb); script ported to scripts/ARM_T2_BOT_Fido.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Fido): the only Arm T2 quad - a long light lozenge on four heavy dark legs, a dark turret
puck with twin team plates either side, and a long steel rail gun running the whole length of the body."""
import math

UNIT = dict(
    skeleton='quad',
    skeleton_opts=dict(hipx=7.6, hipz=8.0, drop=['ruparm', 'rloarm', 'rhand', 'luparm', 'lloarm', 'lhand']),
    res=1024,
    wreck=dict(seed=6, drop=[], remove=[]),
    preview_pose={'turret': (0, -20, 0)},
)


def heavy_legs(k, width=1.6):
    """standard legs + T2 extras on the source leg; the clones carry them to the other legs."""
    from mathutils import Vector
    from s3okit.skeleton import LEGS
    s = LEGS[k.skeleton][0]
    k.standard_legs(width=width)
    H = k.P['pelvis'].y
    w = 0.11 * H * width
    kn = Vector(k.T[s + 'leg']['off']); an = Vector(k.T[s + 'foot']['off'])
    t = k.piece(s + 'thigh'); A = t.at
    t.hull([A(x, kn.y + dy, kn.z + dz) for x in (-1.2 * w, 1.2 * w) for dy, dz in
            [(0.9, -0.2), (0.2, -1.6), (-1.0, -1.2), (-1.2, 0.4), (0.4, 0.9)]], 'paint2', bevel=0.12)
    l = k.piece(s + 'leg'); B = lambda x, y, z: Vector(l.at(x, y, z))
    d = an.normalized(); L = an.length
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.18 * L, B(-1.05 * w, 0, 0) + d * 0.8 * L, 0.42, 8, 'steel')
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.12 * L, B(-1.05 * w, 0, 0) + d * 0.42 * L, 0.65, 8, 'dark', bevel=0.04)
    n = Vector((0, d.z, -d.y))
    l.hull([B(x, 0, 0) + d * s_ * L + n * (0.06 * H + e) for x in (-0.7 * w, 0.7 * w) for s_ in (0.2, 0.75) for e in (0, 0.5)],
           'paint', bevel=0.1)
    f = k.piece(s + 'foot'); C = f.at
    g = -k.T[s + 'foot']['gpos'][1]
    for x in (-0.75 * w, 0.75 * w):
        f.hull([C(x + dx, y, z) for dx in (-0.35 * w, 0.35 * w) for y, z in
                [(g, 0.36 * H), (g, 0.52 * H), (g + 0.07 * H, 0.32 * H), (g + 0.03 * H, 0.5 * H)]], 'dark', bevel=0.06)
    f.hull([C(dx, y, z) for dx in (-0.4 * w, 0.4 * w) for y, z in
            [(g, -0.26 * H), (g, -0.42 * H), (g + 0.09 * H, -0.24 * H)]], 'dark', bevel=0.05)


def build(k):
    heavy_legs(k, width=1.5)

    # ------------------------------------------------------------------ pelvis (0, 15.59, 0): rear hump
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, -3.6, -12.4), (6.2, -3.6, 3.0), (6.0, 5.6, -12.0), (6.0, 6.4, 3.0), (4.4, 7.3, -11.0),
             (4.6, 7.4, 2.2), (4.2, 1.0, -14.0), (4.0, -2.4, -13.6)]], 'paint', bevel=0.24)
    # dark belly / leg yoke between the hips
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.0, -2.0, -10.0), (7.0, -2.0, 10.0), (7.0, 2.2, -10.0), (7.0, 2.2, 10.0), (5.0, -4.6, -8.0), (5.0, -4.6, 8.0)]],
           'paint2', bevel=0.2)
    # team plates on the deck either side of the turret
    p.hull([Q(x, y, z) for x, y, z in
            [(3.7, 7.42, -10.8), (5.6, 6.8, -10.8), (3.7, 7.42, 1.6), (5.6, 6.6, 1.6),
             (3.7, 7.58, -10.75), (5.55, 6.96, -10.75), (3.7, 7.58, 1.55), (5.55, 6.76, 1.55)]], 'team', bevel=0.03, mirror=True)
    # rear engine block with vents and a red tail light
    p.box(Q(-3.4, 0.6, -14.6), Q(3.4, 5.0, -12.6), 'dark', bevel=0.12)
    for y in (1.4, 2.6, 3.8):
        p.box(Q(-2.8, y, -14.85), Q(2.8, y + 0.5, -14.5), 'black', bevel=0.0)
    p.cyl(Q(-3.2, 7.0, -9.8), Q(-3.2, 9.0, -9.8), 0.3, 6, 'dark')                  # antenna base, left rear
    p.cyl(Q(-3.2, 9.0, -9.8), Q(-3.2, 14.0, -9.8), 0.1, 6, 'steel', r2=0.05)
    p.cyl(Q(-3.2, 14.0, -9.8), Q(-3.2, 14.25, -9.8), 0.16, 6, 'lightr')

    # ------------------------------------------------------------------ torso (0, 15.59, 2.33): front chest + snout
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.8, -4.4, 0.4), (5.8, 4.6, 0.4), (5.4, -4.6, 9.0), (5.0, 3.4, 9.0), (3.6, -3.4, 13.6), (3.4, 1.6, 13.8)]],
           'paint', bevel=0.24)
    # dark lower jaw / chest band
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.9, -4.8, 1.0), (5.5, -4.9, 9.4), (3.7, -3.6, 14.0), (5.9, -2.6, 1.0), (5.5, -2.8, 9.6), (3.7, -1.8, 14.1)]],
           'paint2', bevel=0.12)
    # sensor snout: dark brow with two cyan eyes
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 0.2, 13.6), (3.0, 1.9, 13.4), (2.6, 0.3, 15.2), (2.4, 1.6, 15.0)]], 'dark', bevel=0.08)
    for sx in (-1.3, 1.3):
        t.cyl(A(sx, 1.0, 15.0), A(sx, 1.0, 15.35), 0.6, 8, 'lightc')
    # team chevron on the chest top (in front of the turret, not under the barrel's middle)
    for sx in (-1, 1):
        t.hull([A(x * sx, y, z) for x, y, z in
                [(1.9, 4.62, 1.0), (5.0, 4.0, 1.0), (1.9, 3.95, 7.0), (4.0, 3.4, 8.0),
                 (1.9, 4.78, 1.05), (4.95, 4.16, 1.05), (1.9, 4.11, 6.95), (3.95, 3.56, 7.95)]], 'team', bevel=0.03)

    # ------------------------------------------------------------------ turret (0, 23.04, -5.8)
    r = k.piece('turret'); R = r.at
    r.cyl(R(0, -0.6, 0), R(0, 1.9, 0), 3.9, 14, 'dark', bevel=0.1)
    r.cyl(R(0, 1.85, 0), R(0, 2.0, 0), 2.6, 14, 'paint2')

    # ------------------------------------------------------------------ gauss (0, 24.9, -5.8): breech + rail barrel
    g = k.piece('gauss'); G = g.at
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 0.0, -4.6), (3.4, 0.0, 5.4), (3.0, 4.6, -4.0), (3.0, 4.6, 4.6), (2.2, 2.8, 7.2), (2.4, 0.2, 7.0)]],
           'paint', bevel=0.2)
    g.box(G(-2.2, 4.55, -3.2), G(2.2, 4.75, 3.4), 'team', bevel=0.04)               # turret roof plate
    g.box(G(-3.5, 1.0, -4.8), G(3.5, 3.4, -4.4), 'dark', bevel=0.06)                # breech cap
    Y = 1.86
    g.cyl(G(0, Y, 6.0), G(0, Y, 18.4), 0.7, 10, 'dark')                             # core barrel
    for sx in (-1, 1):                                                                # twin steel rails
        g.box(G(sx * 0.35 if sx > 0 else -1.5, Y - 1.2, 6.4), G(1.5 if sx > 0 else -0.35, Y + 1.2, 18.8), 'steel', bevel=0.1)
    for z in (9.0, 12.0, 15.0):                                                       # coil collars, cyan strip on top
        g.box(G(-1.9, Y - 1.6, z), G(1.9, Y + 1.6, z + 0.7), 'dark', bevel=0.06)
        g.box(G(-1.0, Y + 1.58, z + 0.1), G(1.0, Y + 1.74, z + 0.6), 'lightc', bevel=0.0)
    g.box(G(-1.8, Y - 1.8, 17.8), G(1.8, Y + 1.8, 18.6), 'dark', bevel=0.08)        # muzzle frame
