"""Zipper (ARM_T2_BOT_Zipper) - Arm T2 fast attack kbot. A lean sprinter: a small wedge chest with a low sensor
head, two hexagonal shoulder pods (TA's), a slim left arm and a long right arm-cannon carried forward like a lance.
Long light legs. Standard biped skeleton; script ported to scripts/ARM_T2_BOT_Zipper.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Zipper): the narrowest Arm T2 body - two hex team-topped pods either side of a small light
wedge, and one long dark cannon reaching out ahead on the right (asymmetric, unlike the twin-gunned Arm kbots)."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.3),
    res=1024,
    wreck=dict(seed=12, drop=['rloarm'], remove=[]),
    preview_pose={'rloarm': (-80.16, 0, 0)},       # carry pose (the COB walk's)
)


def hexpod(b, sx):
    """hexagonal shoulder pod on an upper-arm piece, centred over the shoulder joint; sx = -1 right, +1 left."""
    P = lambda x, y, z: b.at(sx * x, y, z)
    cx = 3.9
    ring = lambda y, r: [P(cx + r * math.cos(a), y, r * math.sin(a)) for a in [i * math.pi / 3 + math.pi / 6 for i in range(6)]]
    b.hull(ring(-1.6, 3.6) + ring(1.6, 4.0) + ring(3.0, 3.4), 'paint', bevel=0.16)
    b.hull(ring(3.0, 2.6) + ring(3.2, 2.5), 'team', bevel=0.04)
    b.cyl(P(0.6, 0, 0), P(-0.6, 0, 0), 1.7, 10, 'dark', bevel=0.05)


def build(k):
    k.standard_legs(width=1.25)

    # ------------------------------------------------------------------ pelvis (0, 18.15, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, -2.4, -2.4), (2.6, -2.4, 2.6), (3.2, 1.2, -3.0), (3.2, 1.2, 3.0), (1.6, -3.2, -1.6), (1.6, -3.2, 1.8)]],
           'paint2', bevel=0.16)

    # ------------------------------------------------------------------ torso (0, 19.24, 0): wedge chest
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -0.4, 0), A(0, 2.0, 0), 2.2, 10, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 1.6, -2.8), (2.6, 1.6, 3.2), (4.6, 6.4, -3.4), (4.6, 6.4, 4.4), (4.2, 10.2, -3.0), (3.2, 10.6, 2.8),
             (2.0, 4.2, 5.4)]], 'paint', bevel=0.2)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                          # sternum plate
            [(1.6, 2.4, 4.4), (2.8, 6.6, 4.65), (1.6, 2.4, 4.6), (2.8, 6.6, 4.85)]], 'paint2', bevel=0.04)
    # low sensor head pushed forward, cyan slit
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 9.6, -0.6), (1.8, 9.6, 4.8), (1.4, 12.0, -0.2), (1.2, 11.6, 4.2), (1.0, 10.2, 6.0)]], 'paint2', bevel=0.12)
    t.box(A(-1.0, 10.5, 5.35), A(1.0, 10.95, 5.6), 'lightc', bevel=0.0)
    # dorsal fin/radiator, dark
    t.hull([A(x, y, z) for x in (-0.5, 0.5) for y, z in [(10.4, -2.6), (12.6, -2.0), (12.4, -0.6), (10.6, 0.4)]], 'dark', bevel=0.06)
    t.box(A(-2.4, 4.0, -3.7), A(2.4, 8.6, -3.2), 'dark', bevel=0.06)                 # back vent
    for y in (4.8, 6.0, 7.2):
        t.box(A(-2.0, y, -3.9), A(2.0, y + 0.45, -3.6), 'black', bevel=0.0)

    # ------------------------------------------------------------------ right arm: pod + cannon forearm
    u = k.piece('ruparm'); U = u.at                    # (-4.9, 26.81, 0); elbow at (-3.44, -7.98, 0)
    hexpod(u, -1)
    u.hull([U(x, y, z) for x, y, z in
            [(-2.6, -1.6, -1.3), (-2.6, -1.6, 1.4), (-4.4, -1.6, -1.3), (-4.4, -1.6, 1.4),
             (-2.7, -8.0, -1.1), (-2.7, -8.0, 1.2), (-4.2, -8.0, -1.1), (-4.2, -8.0, 1.2)]], 'dark', bevel=0.1)
    r = k.piece('rloarm'); R = r.at                    # (-8.34, 18.83, 0): muzzle rfirept at (0, -19.25, 3.44)
    r.cyl(R(-1.6, 0, 0), R(1.6, 0, 0), 1.5, 10, 'dark', bevel=0.05)
    r.hull([R(x, y, z) for x, y, z in                                                  # cannon housing
            [(-1.7, -0.8, -1.8), (1.7, -0.8, -1.8), (-1.7, -0.8, 2.6), (1.7, -0.8, 2.6),
             (-1.9, -9.0, -2.2), (1.9, -9.0, -2.2), (-1.9, -9.0, 4.6), (1.9, -9.0, 4.6),
             (-1.5, -12.0, 0.6), (1.5, -12.0, 0.6), (-1.5, -12.0, 4.6), (1.5, -12.0, 4.6)]], 'paint2', bevel=0.14)
    r.box(R(-1.3, -2.0, 4.5), R(1.3, -8.0, 4.8), 'team', bevel=0.03)                 # team strip along the top
    r.cyl(R(0, -9.0, 3.44), R(0, -18.2, 3.44), 0.85, 10, 'steel')                     # barrel
    r.cyl(R(0, -11.8, 3.44), R(0, -12.8, 3.44), 1.2, 10, 'dark')
    r.cyl(R(0, -18.0, 3.44), R(0, -19.3, 3.44), 1.15, 8, 'dark', rot=math.pi / 8, bevel=0.04)
    r.cyl(R(0, -19.25, 3.44), R(0, -19.4, 3.44), 0.55, 8, 'black')

    # ------------------------------------------------------------------ left arm: pod, slim forearm, fist
    lu = k.piece('luparm'); V = lu.at                  # (4.9, 26.81, 0); elbow at (3.44, -7.98, 0)
    hexpod(lu, 1)
    lu.hull([V(x, y, z) for x, y, z in
             [(2.6, -1.6, -1.3), (2.6, -1.6, 1.4), (4.4, -1.6, -1.3), (4.4, -1.6, 1.4),
              (2.7, -8.0, -1.1), (2.7, -8.0, 1.2), (4.2, -8.0, -1.1), (4.2, -8.0, 1.2)]], 'dark', bevel=0.1)
    la = k.piece('lloarm'); W = la.at                  # (8.34, 18.83, 0); hand at (-0.54, -9.26, -0.54)
    la.cyl(W(-1.4, 0, 0), W(1.4, 0, 0), 1.3, 10, 'dark', bevel=0.05)
    la.hull([W(x, y, z) for x, y, z in
             [(-1.5, -0.8, -1.5), (1.5, -0.8, -1.5), (-1.5, -0.8, 1.6), (1.5, -0.8, 1.6),
              (-1.7, -5.0, -1.7), (1.7, -5.0, -1.7), (-1.7, -5.0, 1.8), (1.7, -5.0, 1.8),
              (-1.3, -8.8, -1.3), (1.3, -8.8, -1.3), (-1.3, -8.8, 1.4), (1.3, -8.8, 1.4)]], 'paint2', bevel=0.12)
    hd = k.piece('lhand'); HD = hd.at
    hd.hull([HD(x, y, z) for x in (-1.2, 1.3) for y in (0.2, -2.6) for z in (-1.1, 1.6)], 'dark', bevel=0.12)
