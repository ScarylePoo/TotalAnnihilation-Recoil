"""Eraser (ARM_T2_BOT_Eraser) - Arm T2 radar jammer kbot. A slim walker carrying a wide hexagonal jammer beam across
its shoulders; when active the two jammer tongs drop out of the beam, swing forward into a fork on the chest hub
(tongpivot) and the hub spins them. Standard biped skeleton; script ported to scripts/ARM_T2_BOT_Eraser.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward. The torso piece's origin is at the ground (TA model).
Top view (what makes it an Eraser): a long light bar wider than any other Arm kbot, team plates on both bar ends, a
dark central mast, and (active) the spinning light fork with cyan emitter tips in front."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=4.2),
    res=1024,
    wreck=dict(seed=8, drop=['ltong'], remove=[]),
    # jammer active (the normal state in game): tongs down and swung forward
    preview_pose={'tongend': {'move': (0, -7.5, 0)}, 'ltong': {'move': (0, -7.5, 0), 'rot': (0, -119.17, 0)},
                  'rtong': {'move': (0, -7.5, 0), 'rot': (0, 116.72, 0)}, 'tongpivot': (0, 0, 30)},
)


def build(k):
    k.standard_legs(width=1.45)

    # ------------------------------------------------------------------ pelvis (0, 17, 0): hip block
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -2.6, -2.8), (3.0, -2.6, 2.6), (3.6, 1.6, -3.4), (3.6, 1.6, 3.0), (2.0, -3.6, -1.6), (2.0, -3.6, 1.6)]],
           'paint2', bevel=0.18)

    # ------------------------------------------------------------------ torso (origin 0,0,0): mast + jammer beam
    t = k.piece('torso')
    # central mast from the hips up to the beam, slim so the tongs sweep past it
    t.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 17.8, -3.6), (2.2, 17.8, 0.6), (2.0, 24.6, -9.6), (2.0, 24.6, -3.2), (2.2, 20.6, -7.0)]], 'dark', bevel=0.14)
    # chest plate in front of the mast, behind the hub
    t.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 17.6, -4.6), (3.4, 17.6, -3.0), (3.0, 23.0, -5.0), (3.0, 23.0, -3.4)]], 'paint', bevel=0.14)
    # the beam: hex section along X
    sec = [(-12.4, 28.2), (-9.8, 32.6), (-4.2, 32.6), (-1.6, 28.2), (-4.2, 23.8), (-9.8, 23.8)]
    t.prism(-13.4, 13.4, sec, 'paint', bevel=0.22)
    # end caps (darker) with cyan emitter lenses
    for sx in (-1, 1):
        x0, x1 = (13.3, 14.6) if sx > 0 else (-14.6, -13.3)
        t.prism(x0, x1, [(z, y) for z, y in [(-11.6, 28.2), (-9.4, 31.8), (-4.6, 31.8), (-2.4, 28.2), (-4.6, 24.6), (-9.4, 24.6)]],
                'paint2', bevel=0.14)
        t.cyl((sx * 14.5, 28.2, -7.0), (sx * 14.8, 28.2, -7.0), 1.4, 10, 'lightc')
    # team plates on the beam top, both ends; dark slot down the middle (where the tongs live)
    t.hull([(x, y, z) for x, y, z in
            [(4.6, 32.62, -9.4), (12.6, 32.62, -9.4), (4.6, 32.62, -4.6), (12.6, 32.62, -4.6),
             (4.6, 32.78, -9.35), (12.55, 32.78, -9.35), (4.6, 32.78, -4.65), (12.55, 32.78, -4.65)]], 'team', bevel=0.04, mirror=True)
    t.box((-3.6, 32.55, -9.0), (3.6, 32.8, -5.0), 'dark', bevel=0.05)
    # underside slot lips (dark) the tongs drop out of
    t.box((-12.6, 23.65, -11.0), (12.6, 23.9, -3.0), 'black', bevel=0.0)
    # beam front sensor strip
    t.box((-11.0, 27.4, -1.75), (11.0, 28.9, -1.45), 'dark', bevel=0.04)

    # ------------------------------------------------------------------ hub (0, 19.5, -3), spins about Z
    h = k.piece('tongpivot'); H = h.at
    h.cyl(H(0, 0, -0.8), H(0, 0, 3.6), 2.7, 8, 'dark', bevel=0.12)
    h.cyl(H(0, 0, 3.5), H(0, 0, 4.9), 1.9, 8, 'paint', r2=1.2, bevel=0.06)
    h.cyl(H(0, 0, 4.85), H(0, 0, 5.05), 0.9, 8, 'lightc')

    # ------------------------------------------------------------------ tong mount (0, 27, -6)
    e = k.piece('tongend'); E = e.at
    e.box(E(-2.3, -1.4, -2.4), E(2.3, 1.4, 2.8), 'paint2', bevel=0.14)
    e.box(E(-1.2, -1.6, -1.0), E(1.2, -1.35, 2.0), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ tongs: left built, right mirrored clone
    g = k.piece('ltong'); G = g.at
    # stowed: the arm runs out along +x and sweeps back to z -8; deployed (turned) it points forward
    g.hull([G(x, y, z) for y in (-1.3, 1.3) for x, z in [(0.0, -0.6), (0.0, 0.6), (3.0, 0.4), (3.0, -1.6)]], 'dark', bevel=0.1)
    g.hull([G(x, y, z) for y in (-1.5, 1.5) for x, z in [(2.6, 0.3), (2.6, -1.7), (8.4, -5.4), (9.6, -4.6), (10.0, -7.6), (8.8, -7.9)]],
           'paint', bevel=0.16)
    g.hull([G(x, y, z) for y in (1.48, 1.64) for x, z in [(3.6, -0.6), (3.6, -1.6), (8.2, -4.6), (8.8, -4.2)]], 'team', bevel=0.02)
    g.cyl(G(9.4, 0, -7.75), G(9.4, 0, -8.15), 1.05, 8, 'lightc')
    k.clone('rtong', 'ltong', mirror_x=True)
