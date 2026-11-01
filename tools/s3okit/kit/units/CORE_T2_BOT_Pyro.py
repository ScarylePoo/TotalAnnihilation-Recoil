"""Pyro (CORE_T2_BOT_Pyro) - Core T2 flamethrower kbot. A hunched walker carrying two big fuel cylinders crosswise on
its back (TA's hex tanks, ochre hazard bands), an exhaust stack, a flamethrower arm reaching far forward on the right
and a slanted shield plate on the left arm. TA's pilot-light flame polygons (flame1..3) are flare geometry: the pieces
stay empty. Standard biped skeleton; script ported to scripts/CORE_T2_BOT_Pyro.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Pyro): two fat light-ochre-banded tanks across the back (the widest part), a dark hunched
body with a team plate and a team cradle lid between the tanks, a long light steel nozzle reaching out on the right and the dark shield slab on the left."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.8),
    res=1024,
    wreck=dict(seed=23, drop=['lloarm'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.5)

    # ------------------------------------------------------------------ pelvis (0, 13.16, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, -2.2, -3.4), (3.2, -2.2, 2.2), (3.6, 1.6, -4.4), (3.6, 1.6, 2.6), (1.8, -3.0, -2.4), (1.8, -3.0, 1.6)]],
           'paint2', bevel=0.16)

    # ------------------------------------------------------------------ torso (0, 17.67, -4.05)
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -2.6, 0.6), A(0, 0.6, 0.6), 2.8, 10, 'dark', bevel=0.06)                # waist
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # hunched chest
            [(4.4, 0.2, -4.4), (4.4, 0.2, 5.6), (5.8, 4.6, -5.0), (5.8, 4.6, 7.4), (5.0, 8.6, -6.0), (4.2, 8.0, 5.4),
             (2.4, 2.4, 9.4), (2.4, 6.6, 8.8)]], 'paint', bevel=0.22)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # team plate on the hump
            [(3.2, 8.62, -4.6), (2.8, 8.18, 3.6), (3.2, 8.78, -4.55), (2.8, 8.34, 3.55)]], 'team', bevel=0.03)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # dark face slot
            [(2.0, 3.4, 9.0), (2.0, 5.6, 8.7), (1.6, 3.6, 9.4), (1.6, 5.4, 9.15)]], 'dark', bevel=0.04)
    t.box(A(-1.4, 4.2, 9.25), A(1.4, 4.8, 9.45), 'lightw', bevel=0.0)
    # tank cradle and the two fuel cylinders lying across the back
    t.box(A(-3.6, 0.2, -11.4), A(3.6, 9.2, -5.2), 'paint2', bevel=0.14)
    t.box(A(-3.3, 9.18, -11.1), A(3.3, 9.34, -5.5), 'team', bevel=0.03)                # team lid on the cradle
    for y, z in ((0.0, -8.6), (6.2, -9.4)):
        t.cyl(A(-9.4, y, z), A(9.4, y, z), 3.3, 6, 'paint', rot=math.pi / 6, bevel=0.16)
        for x in (-6.4, 6.4):
            t.cyl(A(x - 1.0, y, z), A(x + 1.0, y, z), 3.45, 6, 'hazard', rot=math.pi / 6, bevel=0.04)
        if y > 0:                                                                       # team band on the top tank
            t.cyl(A(-3.2, y, z), A(3.2, y, z), 3.42, 6, 'team', rot=math.pi / 6, bevel=0.04)
        for sx in (-1, 1):
            t.cyl(A(sx * 9.35, y, z), A(sx * 9.8, y, z), 2.2, 6, 'dark', rot=math.pi / 6)
    t.cyl(A(1.6, 9.0, -6.4), A(1.6, 18.6, -6.4), 0.7, 8, 'dark', bevel=0.04)          # exhaust stack
    t.cyl(A(1.6, 18.4, -6.4), A(1.6, 19.4, -6.4), 1.0, 8, 'dark', bevel=0.04)
    t.cyl(A(1.6, 19.35, -6.4), A(1.6, 19.5, -6.4), 0.6, 8, 'black')

    # ------------------------------------------------------------------ flamethrower arm (-3.24, 18.91, -3.74)
    u = k.piece('ruparm'); U = u.at                    # nozzle (firept) at (-4.26, -4.16, 17.99)
    u.cyl(U(0.4, 0, 0), U(-2.4, 0, 0), 2.4, 10, 'dark', bevel=0.06)                   # shoulder
    u.hull([U(x, y, z) for x, y, z in                                                  # arm housing with fuel feed
            [(-2.4, -2.6, -3.0), (-6.6, -2.6, -3.0), (-2.4, 2.4, -2.4), (-6.6, 2.4, -2.4),
             (-2.8, -5.6, 7.0), (-6.4, -5.6, 7.0), (-2.8, -2.4, 7.6), (-6.4, -2.4, 7.6)]], 'paint2', bevel=0.2)
    u.hull([U(x, y, z) for x, y, z in                                                  # ochre fuel canister on top
            [(-3.2, 2.3, -1.6), (-5.8, 2.3, -1.6), (-3.2, 2.3, 4.0), (-5.8, 2.3, 4.0),
             (-3.4, 3.8, -1.2), (-5.6, 3.8, -1.2), (-3.4, 3.4, 3.6), (-5.6, 3.4, 3.6)]], 'hazard', bevel=0.1)
    u.cyl(U(-4.26, -4.16, 7.0), U(-4.26, -4.16, 16.6), 1.0, 10, 'steel')               # nozzle tube
    for z in (9.0, 12.0):
        u.cyl(U(-4.26, -4.16, z), U(-4.26, -4.16, z + 0.8), 1.4, 10, 'dark')
    u.cyl(U(-4.26, -4.16, 16.4), U(-4.26, -4.16, 18.0), 1.25, 10, 'steel', r2=1.6)    # flared tip
    u.cyl(U(-4.26, -4.16, 17.95), U(-4.26, -4.16, 18.1), 1.0, 10, 'black')
    u.cyl(U(-4.26, -2.6, 15.2), U(-4.26, -2.6, 17.4), 0.35, 6, 'dark')                # igniter
    u.cyl(U(-4.26, -2.6, 17.35), U(-4.26, -2.6, 17.6), 0.3, 6, 'lightr')

    # ------------------------------------------------------------------ shield arm (3.24, 17.41, -3.24)
    lu = k.piece('luparm'); V = lu.at
    lu.cyl(V(-0.4, 0, 0), V(2.6, 0, 0), 2.4, 10, 'dark', bevel=0.06)
    lu.hull([V(x, y, z) for x in (1.4, 4.8) for y, z in [(-2.2, -2.8), (2.2, -2.8), (2.0, 6.6), (-2.2, 6.6)]], 'paint2', bevel=0.16)
    sh = k.piece('lloarm')                             # origin (0, 0, -2.5); the shield slab in global coords
    sh.hull([(x, y, z) for x, y, z in
             [(5.0, 15.4, 1.0), (5.0, 15.4, 7.8), (3.8, 28.8, 1.0), (3.8, 28.8, 6.6),
              (6.6, 15.4, 1.0), (6.6, 15.4, 7.8), (5.4, 28.8, 1.0), (5.4, 28.8, 6.6),
              (12.8, 18.0, 4.0), (12.0, 26.0, 4.0)]], 'paint', bevel=0.2)
    sh.hull([(x, y, z) for x, y, z in                                                  # dark armour ribs
             [(6.7, 17.0, 2.0), (6.7, 17.0, 6.8), (6.7, 18.4, 2.0), (6.7, 18.4, 6.8),
              (7.2, 17.0, 2.2), (7.2, 17.0, 6.6), (7.2, 18.4, 2.2), (7.2, 18.4, 6.6)]], 'dark', bevel=0.04)
    sh.hull([(x, y, z) for x, y, z in                                                  # team stripe on the shield top
             [(4.1, 28.85, 1.6), (4.1, 28.85, 6.0), (5.1, 28.85, 1.6), (5.1, 28.85, 6.0),
              (4.1, 29.0, 1.65), (4.1, 29.0, 5.95), (5.1, 29.0, 1.65), (5.1, 29.0, 5.95)]], 'team', bevel=0.02)
