"""Zeus (ARM_T2_BOT_Zeus) - Arm T2 assault kbot with a lightning gun. A broad barrel-chested walker with a domed
head, two huge rounded pauldrons, a heavy left fist, and a long forked lightning cannon that rides stowed on its back
(backgun) until the right arm reaches over the shoulder and draws it (gun, along the right forearm).
Standard biped skeleton with heavy T2 legs (knee guards, shin pistons, clawed feet); script ported to
scripts/ARM_T2_BOT_Zeus.lua (draw/holster keyframes kept, the old walk replaced by the shared one).
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Zeus): the widest Arm kbot silhouette - two big light pauldrons with team tops either side
of a light dome head, a dark generator backpack with cyan coils, and the dark gun with cyan coil rings on the right."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=5.0),
    res=1024,
    wreck=dict(seed=5, drop=['backgun'], remove=['gun']),
    # in game it walks with the gun holstered and the arms carried forward (COB holster end pose)
    preview_pose={'ruparm': (-17.93, 0, 0), 'luparm': (-36.56, 0, 0), 'lloarm': (0, 0, -22.15),
                  'lhand': (0, -43.94, 0), 'rloarm': (-67.85, 0, 0), 'gun': 'hide'},
)


def heavy_legs(k, width=1.6):
    """standard legs + T2 extras on the source (right) leg; the clones carry them to the left leg."""
    from mathutils import Vector
    k.standard_legs(width=width)
    H = k.P['pelvis'].y
    w = 0.11 * H * width
    kn = Vector(k.T['rleg']['off']); an = Vector(k.T['rfoot']['off'])
    t = k.piece('rthigh'); A = t.at
    # knee guard: a rounded cap behind the (backwards) knee
    t.hull([A(x, kn.y + dy, kn.z + dz) for x in (-1.2 * w, 1.2 * w) for dy, dz in
            [(0.9, -0.2), (0.2, -1.6), (-1.0, -1.2), (-1.2, 0.4), (0.4, 0.9)]], 'paint2', bevel=0.12)
    l = k.piece('rleg'); B = lambda x, y, z: Vector(l.at(x, y, z))
    # shin piston on the outside of the shin
    d = an.normalized(); L = an.length
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.18 * L, B(-1.05 * w, 0, 0) + d * 0.8 * L, 0.42, 8, 'steel')
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.12 * L, B(-1.05 * w, 0, 0) + d * 0.42 * L, 0.65, 8, 'dark', bevel=0.04)
    # front shin plate
    n = Vector((0, d.z, -d.y))   # perpendicular to the shin in the side view, pointing up/forward
    l.hull([B(x, 0, 0) + d * s * L + n * (0.06 * H + e) for x in (-0.7 * w, 0.7 * w) for s in (0.2, 0.75) for e in (0, 0.5)],
           'paint', bevel=0.1)
    f = k.piece('rfoot'); C = f.at
    g = -k.T['rfoot']['gpos'][1]
    # two front toe claws and a heel spur
    for x in (-0.75 * w, 0.75 * w):
        f.hull([C(x + dx, y, z) for dx in (-0.35 * w, 0.35 * w) for y, z in
                [(g, 0.36 * H), (g, 0.52 * H), (g + 0.07 * H, 0.32 * H), (g + 0.03 * H, 0.5 * H)]], 'dark', bevel=0.06)
    f.hull([C(dx, y, z) for dx in (-0.4 * w, 0.4 * w) for y, z in
            [(g, -0.26 * H), (g, -0.42 * H), (g + 0.09 * H, -0.24 * H)]], 'dark', bevel=0.05)


def lightning_gun(b, dy=0.0, dz=0.0):
    """the forked lightning cannon in gun-local coordinates (muzzle toward -y); shifted by (0, dy, dz) for backgun."""
    G = lambda x, y, z: b.at(x, y + dy, z + dz)
    X, Z = -9.8, 1.8                                                                  # barrel axis
    b.cyl(G(X, -6.6, Z), G(X, 9.4, Z), 2.0, 10, 'dark', rot=math.pi / 10, bevel=0.1)
    b.cyl(G(X, 9.3, Z), G(X, 10.8, Z), 1.6, 10, 'paint2', bevel=0.08)                # rear cap
    for y in (-5.4, -3.6, -1.8):                                                      # cyan coil rings
        b.cyl(G(X, y, Z), G(X, y + 0.7, Z), 2.3, 10, 'lightc', rot=math.pi / 10)
    b.hull([G(X + sx, y, z) for sx in (-1.9, 1.9) for y, z in                        # underslung capacitor
            [(-1.0, -0.3), (9.0, -0.3), (-0.2, -5.4), (8.4, -5.4)]], 'paint2', bevel=0.14)
    b.box(G(X - 1.2, 1.6, -5.6), G(X + 1.2, 7.6, -5.3), 'lightc', bevel=0.0)        # charge window
    for sx in (-1.25, 1.25):                                                           # forked prongs
        b.hull([G(X + sx + dx, y, Z + dzz) for dx in (-0.5, 0.5) for dzz in (-0.6, 0.6) for y in (-6.0,)] +
               [G(X + sx * 1.3 + dx, -11.0, Z + dzz) for dx in (-0.35, 0.35) for dzz in (-0.4, 0.4)], 'steel', bevel=0.06)
        b.cyl(G(X + sx * 1.3, -10.6, Z), G(X + sx * 1.3, -11.2, Z), 0.45, 8, 'lightc')


def pauldron(b, sx):
    """big rounded shoulder pad on an upper-arm piece; sx = -1 right arm, +1 left arm."""
    U = lambda x, y, z: b.at(sx * x, y, z)
    b.cyl(U(0, 0, 0), U(1.8, 0, 0), 2.2, 12, 'dark', bevel=0.08)                     # shoulder ball
    ring = lambda y, rx, rz, cx: [U(cx + rx * math.cos(a), y, rz * math.sin(a)) for a in [i * math.pi / 5 for i in range(10)]]
    b.hull(ring(-2.6, 3.7, 4.8, 5.2) + ring(1.6, 4.4, 5.3, 5.0) + ring(3.9, 3.7, 4.5, 4.7), 'paint', bevel=0.16)
    b.hull(ring(3.9, 3.7, 4.5, 4.7) + ring(5.5, 1.8, 2.6, 4.4), 'team', bevel=0.1)       # team cap on the pad top
    b.hull([U(x, y, z) for x, y, z in                                                  # dark rim under the pad
            [(1.8, -2.4, -4.4), (1.8, -2.4, 4.4), (9.0, -2.4, -3.6), (9.0, -2.4, 3.6),
             (1.8, -3.3, -4.0), (1.8, -3.3, 4.0), (8.6, -3.3, -3.2), (8.6, -3.3, 3.2)]], 'paint2', bevel=0.1)


def build(k):
    heavy_legs(k, width=1.65)

    # ------------------------------------------------------------------ pelvis (0, 14.96, -2.33)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, -3.0, -3.0), (3.4, -3.0, 3.2), (4.2, 2.4, -3.6), (4.2, 2.4, 4.0), (2.4, -4.2, -2.0), (2.4, -4.2, 2.4)]],
           'paint2', bevel=0.2)
    p.box(Q(-2.2, -2.6, 3.4), Q(2.2, 1.6, 4.6), 'dark', bevel=0.1)                     # crotch plate

    # ------------------------------------------------------------------ torso (0, 18.52, -1.14)
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -2.4, 0), A(0, 0.8, 0), 3.0, 12, 'dark', bevel=0.08)                  # waist
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                         # barrel chest
            [(3.6, 0.6, -3.8), (3.6, 0.6, 4.0), (5.4, 5.0, -4.6), (5.4, 5.0, 5.6), (5.0, 9.4, -4.4),
             (5.0, 9.4, 4.4), (4.0, 10.6, -3.6), (4.0, 10.6, 3.2), (2.8, 3.0, 6.4)]], 'paint', bevel=0.25)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                         # abdomen plate (darker front band)
            [(2.9, 0.9, 4.25), (3.6, 4.4, 5.75), (2.9, 0.9, 4.45), (3.6, 4.4, 5.95)]], 'paint2', bevel=0.06)
    for y in (6.2, 7.4):                                                              # chest vents
        t.box(A(-3.2, y, 5.25), A(3.2, y + 0.55, 5.5), 'black', bevel=0.0)
    # domed head, set forward, cyan visor and a team crest
    t.sphere(A(0, 11.0, 1.2), 3.1, 'paint', segs=14, rings=8, scale=(1, 0.85, 1.05))
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.3, 10.5, 3.2), (2.0, 11.9, 3.0), (1.6, 10.5, 4.3), (1.4, 11.7, 4.1)]], 'dark', bevel=0.05)
    t.box(A(-1.5, 10.9, 4.15), A(1.5, 11.4, 4.35), 'lightc', bevel=0.0)
    t.hull([A(x, y, z) for x in (-0.7, 0.7) for y, z in
            [(13.2, 3.0), (13.7, -1.6), (13.75, 1.2), (14.3, 0.6), (14.2, -1.2), (12.7, -3.0)]], 'team', bevel=0.06)
    # generator backpack (dark) with two cyan coil columns
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 2.0, -4.0), (3.6, 9.4, -4.0), (3.2, 2.6, -8.0), (3.2, 8.8, -8.0)]], 'paint2', bevel=0.22)
    for sx in (-1.6, 1.6):
        t.cyl(A(sx, 2.2, -8.4), A(sx, 9.0, -8.4), 0.9, 8, 'dark')
        for y in (3.4, 5.0, 6.6):
            t.cyl(A(sx, y, -8.4), A(sx, y + 0.5, -8.4), 1.1, 8, 'lightc')
    t.box(A(-0.8, 9.0, -7.0), A(0.8, 10.4, -5.0), 'dark', bevel=0.08)               # vent stack

    # ------------------------------------------------------------------ right arm: pad, upper arm, gun forearm
    u = k.piece('ruparm'); U = u.at                    # shoulder (-4.75, 22.56, -1.85); elbow at (-5.82, -8.19, 0.26)
    pauldron(u, -1)
    u.hull([U(x, y, z) for x, y, z in
            [(-4.6, -2.4, -1.5), (-4.6, -2.4, 1.6), (-7.0, -2.4, -1.5), (-7.0, -2.4, 1.6),
             (-4.9, -8.2, -1.3), (-4.9, -8.2, 1.5), (-6.8, -8.2, -1.3), (-6.8, -8.2, 1.5)]], 'dark', bevel=0.1)
    r = k.piece('rloarm'); R = r.at                    # elbow (-10.57, 14.37, -1.59)
    r.cyl(R(-1.6, 0, 0), R(1.6, 0, 0), 1.8, 10, 'dark', bevel=0.06)
    r.hull([R(x, y, z) for x, y, z in
            [(-2.2, -1.2, -2.2), (2.2, -1.2, -2.2), (-2.2, -1.2, 2.0), (2.2, -1.2, 2.0),
             (-2.5, -7.0, -2.5), (2.5, -7.0, -2.5), (-2.5, -7.0, 2.4), (2.5, -7.0, 2.4),
             (-2.0, -13.4, -2.0), (2.0, -13.4, -2.0), (-2.0, -13.4, 1.8), (2.0, -13.4, 1.8)]], 'paint', bevel=0.16)
    r.box(R(-2.6, -9.0, -2.6), R(2.6, -10.2, 2.5), 'dark', bevel=0.06)             # wrist band
    g = k.piece('gun')
    lightning_gun(g)
    bg = k.piece('backgun')                            # same cannon, stowed on the back (origin offset from gun's)
    lightning_gun(bg, dy=22.35, dz=-11.6)

    # ------------------------------------------------------------------ left arm: pad, elbow, gauntlet, fist
    lu = k.piece('luparm'); V = lu.at                  # (4.75, 22.56, -1.85); lelbow at (5.82, -3.44, 0.24)
    pauldron(lu, 1)
    lu.hull([V(x, y, z) for x, y, z in
            [(4.6, -2.4, -1.5), (4.6, -2.4, 1.6), (7.0, -2.4, -1.5), (7.0, -2.4, 1.6),
             (4.9, -3.6, -1.3), (4.9, -3.6, 1.5), (6.8, -3.6, -1.3), (6.8, -3.6, 1.5)]], 'dark', bevel=0.1)
    e = k.piece('lelbow'); E = e.at
    e.hull([E(x, y, z) for x in (-1.3, 1.3) for y in (0.0, -4.8) for z in (-1.3, 1.5)], 'dark', bevel=0.1)
    e.cyl(E(-1.7, -4.75, 0), E(1.7, -4.75, 0), 1.8, 10, 'dark', bevel=0.06)
    la = k.piece('lloarm'); W = la.at
    la.hull([W(x, y, z) for x, y, z in
             [(-2.2, -1.0, -2.2), (2.2, -1.0, -2.2), (-2.2, -1.0, 2.0), (2.2, -1.0, 2.0),
              (-2.6, -4.4, -2.6), (2.6, -4.4, -2.6), (-2.6, -4.4, 2.5), (2.6, -4.4, 2.5),
              (-2.2, -7.6, -2.2), (2.2, -7.6, -2.2), (-2.2, -7.6, 2.0), (2.2, -7.6, 2.0)]], 'paint', bevel=0.16)
    la.box(W(-1.2, -2.0, 2.4), W(1.2, -6.0, 2.75), 'paint2', bevel=0.05)
    h = k.piece('lhand'); Hh = h.at
    h.hull([Hh(x, y, z) for x, y, z in
            [(-2.0, 0.2, -2.0), (2.0, 0.2, -2.0), (-2.0, 0.2, 1.9), (2.0, 0.2, 1.9),
             (-2.4, -3.0, -2.3), (2.4, -3.0, -2.3), (-2.4, -3.0, 2.4), (2.4, -3.0, 2.4),
             (-1.9, -5.0, -1.8), (1.9, -5.0, -1.8), (-1.9, -5.0, 2.0), (1.9, -5.0, 2.0)]], 'dark', bevel=0.2)
    h.box(Hh(-2.1, -4.6, 2.0), Hh(2.1, -2.2, 2.75), 'steel', bevel=0.08)            # knuckle plate
