"""Freaker (CORE_T2_BOT_Freaker) - Core T2 fast attack kbot. The tallest, thinnest Core walker: very long legs, a
small sloped torso with a long thruster tail behind (Thrust emit point at its end), a little sensor head, angular
shoulder wedges, a long gun-arm on the left (LLArm, muzzle at Flare) and a shorter claw arm on the right. Standard
biped skeleton; script ported to scripts/CORE_T2_BOT_Freaker.lua. Coordinates are ENGINE/global: X right, Y up, Z fwd.
Top view (what makes it a Freaker): a narrow dark-warm dart with a team tail boom, two team-topped shoulder wedges and a
long light steel gun arm on one side - a small cross on stilts, nothing like the bulky Core kbots."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.2),
    res=1024,
    wreck=dict(seed=26, drop=['LLArm'], remove=[]),
    preview_pose={'luarm': (-17.23, 0, 0), 'llarm': (-68.2, 0, 0)},      # aiming pose (activatescr end)
)


def build(k):
    k.standard_legs(width=1.2)

    # ------------------------------------------------------------------ pelvis (0, 23.59, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, -2.2, -2.2), (2.4, -2.2, 2.4), (2.8, 1.2, -2.6), (2.8, 1.2, 2.8), (1.4, -3.0, -1.4), (1.4, -3.0, 1.6)]],
           'paint2', bevel=0.14)

    # ------------------------------------------------------------------ torso (0, 25.11, 0.6): sloped body + tail
    t = k.piece('Torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 0.2, -3.4), (2.6, 0.2, 3.8), (3.8, 4.2, -4.0), (3.8, 4.2, 4.6), (3.0, 8.0, -3.2), (2.6, 8.0, 2.4),
             (1.8, 2.4, 5.6)]], 'paint', bevel=0.2)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # thruster tail (team boom)
            [(2.4, 2.4, -3.6), (2.4, 6.8, -3.6), (1.2, 3.2, -12.4), (1.2, 4.8, -12.6)]], 'team', bevel=0.12)
    t.cyl(A(0, 3.93, -12.0), A(0, 3.93, -13.0), 1.1, 8, 'dark')
    t.cyl(A(0, 3.93, -12.95), A(0, 3.93, -13.1), 0.7, 8, 'lightr')
    t.hull([A(x, y, z) for x in (-0.5, 0.5) for y, z in [(6.6, -3.8), (9.4, -8.6), (8.6, -10.6), (5.6, -8.0)]],
           'hazard', bevel=0.06)                                                         # tail fin
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # team plate on the back
            [(2.2, 8.02, -2.6), (2.0, 8.02, 1.8), (2.2, 8.18, -2.55), (2.0, 8.18, 1.75)]], 'team', bevel=0.03)

    # ------------------------------------------------------------------ head (0, 33.27, 0)
    h = k.piece('Head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, -0.4, -1.4), (1.4, -0.4, 3.6), (1.1, 3.4, -1.0), (1.0, 3.0, 3.4), (0.8, 1.0, 5.0)]], 'paint2', bevel=0.12)
    h.box(H(-0.9, 1.2, 4.55), H(0.9, 1.7, 4.85), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ shoulder wedges (left built, right = clone)
    lu = k.piece('LUArm'); V = lu.at                   # (4.07, 30.85, -1.36); LLArm at (3.97, -3.2, 0)
    lu.cyl(V(-0.4, 0, 0), V(2.0, 0, 0), 1.6, 10, 'dark', bevel=0.05)
    lu.hull([V(x, y, z) for x, y, z in
             [(0.6, 4.2, -3.2), (0.6, 4.2, 3.8), (6.6, 2.0, -2.6), (6.6, 2.0, 3.0), (1.6, -2.2, -2.8), (1.6, -2.2, 3.2),
              (5.4, -3.4, -2.0), (5.4, -3.4, 2.4)]], 'paint', bevel=0.16)
    lu.hull([V(x, y, z) for x, y, z in
             [(1.4, 4.1, -2.4), (1.4, 4.1, 3.0), (5.8, 2.2, -2.0), (5.8, 2.2, 2.4),
              (1.4, 4.26, -2.35), (1.4, 4.26, 2.95), (5.8, 2.36, -1.95), (5.8, 2.36, 2.35)]], 'team', bevel=0.03)
    k.clone('RUArm', 'LUArm', mirror_x=True)

    # ------------------------------------------------------------------ long gun arm (8.04, 27.65, -1.36)
    g = k.piece('LLArm'); G = g.at                     # muzzle (Flare) at (1.74, -19.55, 0.67)
    g.cyl(G(-1.4, 0, 0), G(1.4, 0, 0), 1.4, 10, 'dark', bevel=0.05)
    g.hull([G(x, y, z) for x, y, z in
            [(-1.6, -0.6, -1.8), (2.6, -0.6, -1.8), (-1.6, -0.6, 2.0), (2.6, -0.6, 2.0),
             (-1.8, -9.6, -2.2), (3.2, -9.6, -2.2), (-1.8, -9.6, 2.4), (3.2, -9.6, 2.4),
             (0.2, -12.8, -1.2), (3.0, -12.8, -1.2), (0.2, -12.8, 2.0), (3.0, -12.8, 2.0)]], 'paint2', bevel=0.16)
    g.cyl(G(1.74, -12.4, 0.67), G(1.74, -19.0, 0.67), 0.75, 10, 'steel')
    g.cyl(G(1.74, -18.6, 0.67), G(1.74, -19.6, 0.67), 1.0, 8, 'dark', rot=math.pi / 8, bevel=0.03)
    g.box(G(-1.7, -8.0, 2.35), G(1.0, -2.0, 2.6), 'hazard', bevel=0.03)

    # ------------------------------------------------------------------ claw arm (-8.04, 27.65, -1.36)
    r = k.piece('RLArm'); R = r.at
    r.cyl(R(-1.4, 0, 0), R(1.4, 0, 0), 1.4, 10, 'dark', bevel=0.05)
    r.hull([R(x, y, z) for x, y, z in
            [(-1.8, -0.6, -1.6), (1.6, -0.6, -1.6), (-1.8, -0.6, 1.6), (1.6, -0.6, 1.6),
             (-2.2, -7.4, -1.8), (1.8, -7.4, -1.8), (-2.2, -7.4, 1.8), (1.8, -7.4, 1.8)]], 'paint2', bevel=0.14)
    for dz in (-1.0, 1.0):
        r.hull([R(x, y, z + dz) for x, y, z in
                [(-0.5, -7.2, -0.4), (0.5, -7.2, -0.4), (-0.5, -7.2, 0.4), (0.5, -7.2, 0.4), (0.0, -11.0, 0.9 * dz)]],
               'dark', bevel=0.05)
