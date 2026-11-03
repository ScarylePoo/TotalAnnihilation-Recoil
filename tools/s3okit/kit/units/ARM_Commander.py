"""Arm Commander (ARM_Commander) - the Arm's most important unit. Commander-class biped, the tallest Arm walker, keeping the
TA proportions and what makes this model the Arm Commander: wide flared shoulder wings, two fat rounded tanks on the back,
a domed helmet (here crested), a big D-gun drum as the right forearm and the nano/laser gauntlet as the left, both hanging.
Standard biped skeleton; script ported to scripts/ARM_Commander.lua (no corpse: commanders explode). The decoy
(units/ARM_T2_BOT_DecoyCommander.py) loads this spec, so the two cannot drift apart.
Coordinates are ENGINE/global: X right, Y up, Z fwd.
Top view: very wide swept light wings with team plates, crested light dome, two light tanks with team caps, dark D-gun drum on
the right; the only hazard block sits on the left wing tip and the lathe cuff (nano side), smaller than a pure constructor's
so the commander shape leads."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=6.4),
    res=2048,
    hazard_period=2.5,                # stripes must show on the deliberately small nano-side plates
    wreck=dict(seed=19, drop=['biggun'], remove=[]),        # unused while the def has no corpse
    preview_pose={'ruparm': (-20, 0, 0), 'luparm': (-25, 0, 0)},
)


def heavy_legs(k, width=1.6):
    """standard legs + T2 extras on the source (right) leg; the clones carry them to the left leg."""
    from mathutils import Vector
    k.standard_legs(width=width)
    H = k.P['pelvis'].y
    w = 0.11 * H * width
    kn = Vector(k.T['rleg']['off']); an = Vector(k.T['rfoot']['off'])
    t = k.piece('rthigh'); A = t.at
    t.hull([A(x, kn.y + dy, kn.z + dz) for x in (-1.2 * w, 1.2 * w) for dy, dz in
            [(1.4, -0.3), (0.3, -2.4), (-1.6, -1.8), (-1.8, 0.6), (0.6, 1.4)]], 'paint2', bevel=0.16)
    l = k.piece('rleg'); B = lambda x, y, z: Vector(l.at(x, y, z))
    d = an.normalized(); L = an.length
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.18 * L, B(-1.05 * w, 0, 0) + d * 0.8 * L, 0.6, 8, 'steel')
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.12 * L, B(-1.05 * w, 0, 0) + d * 0.42 * L, 0.95, 8, 'dark', bevel=0.05)
    n = Vector((0, d.z, -d.y))
    l.hull([B(x, 0, 0) + d * s * L + n * (0.06 * H + e) for x in (-0.75 * w, 0.75 * w) for s in (0.15, 0.78) for e in (0, 0.8)],
           'paint', bevel=0.16)
    f = k.piece('rfoot'); C = f.at
    g = -k.T['rfoot']['gpos'][1]
    for x in (-0.75 * w, 0.75 * w):
        f.hull([C(x + dx, y, z) for dx in (-0.35 * w, 0.35 * w) for y, z in
                [(g, 0.36 * H), (g, 0.52 * H), (g + 0.07 * H, 0.32 * H), (g + 0.03 * H, 0.5 * H)]], 'dark', bevel=0.08)
    f.hull([C(dx, y, z) for dx in (-0.4 * w, 0.4 * w) for y, z in
            [(g, -0.26 * H), (g, -0.42 * H), (g + 0.09 * H, -0.24 * H)]], 'dark', bevel=0.08)


def build(k):
    heavy_legs(k, width=1.55)

    # ------------------------------------------------------------------ pelvis (0, 23.75, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, -1.6, -4.6), (6.6, -1.6, 4.8), (7.2, 4.6, -5.0), (7.2, 4.6, 5.4), (4.0, -3.6, -3.2), (4.0, -3.6, 3.6)]],
           'paint2', bevel=0.24)
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # codpiece
            [(2.4, -3.2, 4.4), (2.8, 3.0, 5.6), (2.4, -3.0, 4.7), (2.8, 3.0, 5.9), (1.4, -4.2, 3.8)]], 'paint', bevel=0.12)
    p.cyl(Q(0, 4.0, 0), Q(0, 7.4, 0), 4.2, 12, 'dark', bevel=0.1)                       # waist

    # ------------------------------------------------------------------ torso (0, 34.27, 0)
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # chest
            [(6.4, -6.2, -4.6), (6.4, -6.2, 4.4), (9.6, 0.6, -5.6), (9.6, 0.6, 5.8), (9.0, 6.6, -5.0), (8.2, 6.6, 4.6),
             (4.2, 8.4, -4.0), (4.2, 8.4, 3.2), (4.0, -1.0, 7.4)]], 'paint', bevel=0.3)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # chest emblem plate
            [(3.0, -2.8, 6.65), (3.6, 3.4, 5.9), (3.0, -2.8, 6.9), (3.6, 3.4, 6.15), (0.0, -4.2, 6.9), (0.0, -4.0, 7.15)]],
           'paint2', bevel=0.06)
    t.box(A(-1.2, -1.4, 7.0), A(1.2, 1.6, 7.25), 'lightc', bevel=0.0)
    for sx in (-1, 1):                                                                  # swept shoulder wings
        t.hull([A(sx * x, y, z) for x, y, z in
                [(8.6, 5.0, -5.6), (8.6, 5.0, 5.0), (17.4, 3.4, -9.4), (17.4, 3.4, 1.8), (8.8, 8.2, -5.0), (8.8, 8.2, 4.4),
                 (16.8, 5.9, -8.8), (16.8, 5.9, 1.2)]], 'paint', bevel=0.24)
    # top plates: inner x 9.4 -> outer x 15.8 follows the wing's top (y 8.2 at x 8.8, 5.9 at x 16.8)
    def wing_y(x):
        return 8.2 - (x - 8.8) * (8.2 - 5.9) / (16.8 - 8.8)
    def plate(sx, x0, x1, mat):
        pts = []
        for dy in (0.1, 0.26):
            for x in (x0, x1):
                z_shift = (x - 8.8) / 8.0
                for z in (-5.0 - 3.6 * z_shift + 0.45, 4.4 - 3.2 * z_shift - 0.45):
                    pts.append(A(sx * x, wing_y(x) + dy, z))
        t.hull(pts, mat, bevel=0.03)
    plate(-1, 9.4, 15.9, 'team')                                                        # gun side: all team
    plate(1, 9.4, 11.9, 'team')                                                         # nano side: team + hazard tip
    plate(1, 12.3, 16.3, 'hazard')
    for sx in (-1, 1):                                                                  # two back tanks
        c = A(sx * 4.6, 2.2, -8.4)
        t.cyl((c[0], c[1] - 6.2, c[2]), (c[0], c[1] + 4.8, c[2]), 3.6, 12, 'paint', bevel=0.2)
        t.sphere((c[0], c[1] + 4.8, c[2]), 3.6, 'paint', segs=12, rings=6, scale=(1, 0.6, 1))
        t.cyl((c[0], c[1] + 6.4, c[2]), (c[0], c[1] + 7.2, c[2]), 3.15, 12, 'team', bevel=0.04)
        t.cyl((c[0], c[1] - 6.0, c[2]), (c[0], c[1] - 7.0, c[2]), 2.6, 12, 'dark')
    t.box(A(-1.6, -4.0, -11.6), A(1.6, 4.6, -6.0), 'dark', bevel=0.1)                   # tank manifold

    # ------------------------------------------------------------------ head (0, 40.11, 0.71): domed helmet
    h = k.piece('head'); H = h.at
    h.cyl(H(0, -0.4, -0.2), H(0, 2.4, -0.2), 3.4, 12, 'dark', bevel=0.08)
    h.sphere(H(0, 3.0, 0.0), 3.6, 'paint', segs=14, rings=8, scale=(1, 0.95, 1.0))
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # visor
            [(2.6, 2.0, 2.4), (2.4, 3.6, 2.4), (1.6, 2.0, 3.4), (1.5, 3.4, 3.3)]], 'dark', bevel=0.05)
    h.box(H(-1.8, 2.6, 3.25), H(1.8, 3.1, 3.5), 'lightc', bevel=0.0)
    h.hull([H(x, y, z) for x in (-0.75, 0.75) for y, z in                                # commander crest
            [(6.0, 2.6), (7.6, 1.2), (9.0, -2.6), (7.2, -4.8), (4.4, -4.2)]], 'team', bevel=0.08)
    for sx in (-1, 1):
        h.cyl(H(sx * 2.8, 4.0, -1.8), H(sx * 3.5, 11.0, -3.4), 0.26, 6, 'steel', r2=0.12)   # twin antennae
        h.cyl(H(sx * 3.5, 11.0, -3.4), H(sx * 3.55, 11.4, -3.5), 0.36, 6, 'lightr')

    # ------------------------------------------------------------------ right arm: shoulder + D-gun forearm
    u = k.piece('ruparm'); U = u.at                    # (-13.06, 36.17, 0); biggun at (-1.88, -6.65, 0)
    u.cyl(U(2.4, 0, 0), U(-1.8, 0, 0), 2.6, 12, 'dark', bevel=0.08)
    u.hull([U(x, y, z) for x, y, z in
            [(-0.4, -1.0, -2.6), (-0.4, -1.0, 2.6), (-3.6, -1.0, -2.6), (-3.6, -1.0, 2.6),
             (-0.6, -6.6, -2.2), (-0.6, -6.6, 2.2), (-3.2, -6.6, -2.2), (-3.2, -6.6, 2.2)]], 'paint2', bevel=0.16)
    g = k.piece('biggun'); G = g.at                    # (-14.94, 29.52, 0): muzzle (rbigflash) at (0, -13.06, 0)
    g.cyl(G(-2.8, 0, 0), G(2.8, 0, 0), 2.4, 10, 'dark', bevel=0.06)
    g.cyl(G(0, -0.8, 0), G(0, -9.6, 0), 4.6, 12, 'paint2', rot=math.pi / 12, bevel=0.22)   # D-gun drum
    for y in (-3.0, -6.2):
        g.cyl(G(0, y, 0), G(0, y - 0.9, 0), 5.1, 12, 'dark', rot=math.pi / 12, bevel=0.06)
    g.cyl(G(0, -9.5, 0), G(0, -12.6, 0), 3.3, 12, 'dark', bevel=0.1)
    g.cyl(G(0, -12.5, 0), G(0, -13.2, 0), 2.4, 12, 'black')
    g.box(G(-1.4, -8.4, 4.4), G(1.4, -2.0, 4.85), 'lightr', bevel=0.0)                  # D-gun charge indicator
    g.box(G(-1.6, 0.0, -2.0), G(1.6, 2.0, 2.0), 'dark', bevel=0.06)

    # ------------------------------------------------------------------ left arm: shoulder + lathe gauntlet
    lu = k.piece('luparm'); V = lu.at                  # (13.06, 36.17, 0); nanolath at (1.9, -6.77, 0)
    lu.cyl(V(-2.4, 0, 0), V(1.8, 0, 0), 2.6, 12, 'dark', bevel=0.08)
    lu.hull([V(x, y, z) for x, y, z in
             [(0.4, -1.0, -2.6), (0.4, -1.0, 2.6), (3.6, -1.0, -2.6), (3.6, -1.0, 2.6),
              (0.6, -6.6, -2.2), (0.6, -6.6, 2.2), (3.2, -6.6, -2.2), (3.2, -6.6, 2.2)]], 'paint2', bevel=0.16)
    n = k.piece('nanolath'); N = n.at                  # (14.96, 29.4, 0): laser lfirept (0,-12.35,3.21), spray (0,-13.06,0)
    n.cyl(N(-2.6, 0, 0), N(2.6, 0, 0), 2.3, 10, 'dark', bevel=0.06)
    n.hull([N(x, y, z) for x, y, z in
            [(-3.6, -0.8, -3.4), (3.6, -0.8, -3.4), (-3.6, -0.8, 3.6), (3.6, -0.8, 3.6),
             (-4.0, -7.0, -3.8), (4.0, -7.0, -3.8), (-4.0, -7.0, 4.0), (4.0, -7.0, 4.0),
             (-3.0, -10.8, -3.0), (3.0, -10.8, -3.0), (-3.0, -10.8, 3.2), (3.0, -10.8, 3.2)]], 'paint', bevel=0.24)
    n.hull([N(x, y, z) for x, y, z in                                                   # lathe cuff: reads from above past the wing
            [(-4.6, -1.0, -4.6), (5.8, -1.0, -4.6), (-4.6, -1.0, 4.8), (5.8, -1.0, 4.8),
             (-4.6, -2.6, -5.0), (6.4, -2.6, -5.0), (-4.6, -2.6, 5.2), (6.4, -2.6, 5.2)]], 'paint2', bevel=0.1)
    n.hull([N(x, y, z) for dy in (0.08, 0.22) for x, y, z in
            [(1.2, -1.0 + dy, -4.1), (5.5, -1.0 + dy, -4.1), (1.2, -1.0 + dy, 4.3), (5.5, -1.0 + dy, 4.3)]], 'hazard', bevel=0.03)
    n.cyl(N(0, -10.6, 0), N(0, -12.8, 0), 1.8, 10, 'steel', r2=1.2)                    # nano lathe nozzle
    n.cyl(N(0, -12.7, 0), N(0, -13.1, 0), 1.1, 10, 'lightc')
    n.cyl(N(0, -6.0, 3.21), N(0, -12.2, 3.21), 0.55, 8, 'steel')                       # laser barrel
    n.cyl(N(0, -12.0, 3.21), N(0, -12.5, 3.21), 0.8, 8, 'dark')
