"""Spider (ARM_T2_VEH_Spider) - Arm T2 all-terrain paralyzer spider (ARM_PARALYZER, alternating twin emitters).
TA's model: a long hull, six thin legs from the sides, a small turret on the REAR with two long barrels reaching forward
over the body. Remodelled on the shared six-leg skeleton (skeleton='hexa', walk.Hexa in scripts/headers/walk.lua);
script ported to scripts/ARM_T2_VEH_Spider.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it the Spider): a real spider - dark leg hub and six dark splayed legs around a light body in two
segments (wedge head with four cyan eyes, raised round abdomen behind), the turret on the abdomen with two dark
emitter rods ringed in cyan coils (paralyzer) reaching forward over the head. Team colour: abdomen back plates, turret
roof and a head plate."""
import math

SPLAY = 30   # walk.Hexa's default base splay (deg): previews show the legs as they stand in game

UNIT = dict(
    skeleton='hexa',
    skeleton_opts=dict(height=10.0, hipx=6.5, hipz=7.0),
    res=1024,
    wreck=dict(seed=41, drop=['barrel2'], remove=[]),
    preview_pose={'rfthigh': (0, SPLAY, 0), 'lfthigh': (0, -SPLAY, 0), 'rbthigh': (0, -SPLAY, 0), 'lbthigh': (0, SPLAY, 0)},
)


def ring(y, pts):
    return [(x * s, y, z) for s in (-1, 1) for x, z in pts]


def build(k):
    k.hexa_legs(thigh='paint2', shin='dark', foot='dark', joint='dark', armour='paint2', width=1.25, thick=1.15)

    b = k.piece('base'); A = b.at                         # origin (0, 0, 0)
    # ------------------------------------------------------------------ leg hub: dark octagon the hips sit in
    b.hull([A(*p) for p in ring(7.6, [(4.4, -7.6), (6.2, -5.2), (6.2, 5.6), (4.4, 8.4)]) +
            ring(12.4, [(4.0, -7.0), (5.8, -4.8), (5.8, 5.2), (4.0, 7.8)])], 'paint2', bevel=0.25)
    # ------------------------------------------------------------------ head: light wedge between the front legs
    b.hull([A(*p) for p in ring(8.4, [(3.6, 5.0), (3.2, 14.0), (1.8, 18.2)]) +
            ring(13.4, [(4.0, 4.6), (3.0, 11.6)]) + ring(11.6, [(1.6, 16.6)])], 'paint', bevel=0.22)
    b.hull([A(*p) for p in ring(13.48, [(3.5, 4.9), (2.7, 10.9)]) + ring(13.68, [(3.4, 5.0), (2.6, 10.8)])],
           'team', bevel=0.04)                            # head plate
    b.hull([A(*p) for p in ring(12.46, [(3.4, -3.2), (3.4, 4.2)]) + ring(12.66, [(3.3, -3.1), (3.3, 4.1)])],
           'team', bevel=0.04)                            # saddle over the leg hub
    for x, y, z, r in ((1.0, 12.95, 12.6, 0.7), (2.15, 13.15, 11.8, 0.5)):   # four spider eyes
        b.sphere(A(x, y, z), r, 'lightc', segs=8, rings=4, mirror=True)
    b.hull([A(*p) for p in ring(9.0, [(1.4, 17.4), (0.9, 19.6)]) + ring(10.6, [(1.2, 16.8), (0.6, 19.0)])],
           'dark', bevel=0.08)                            # mandibles
    # ------------------------------------------------------------------ abdomen: raised round body behind the hub
    b.hull([A(*p) for p in ring(9.4, [(3.6, -4.6), (5.6, -9.0), (4.8, -17.0), (2.2, -20.4)]) +
            ring(14.2, [(6.8, -4.0), (7.8, -10.0), (6.8, -17.4), (3.2, -21.6)]) +
            ring(19.4, [(4.8, -5.4), (5.4, -10.0), (4.4, -16.2), (2.0, -18.8)])], 'paint', bevel=0.3)
    # team plates on the abdomen back, either side of the turret pedestal and behind it
    b.hull([A(*p) for p in ring(19.46, [(4.6, -6.0), (5.2, -10.0), (4.2, -16.0), (1.9, -18.4)]) +
            ring(19.66, [(4.4, -6.2), (5.0, -10.0), (4.0, -15.8), (1.8, -18.2)])], 'team', bevel=0.04)
    for z in (-7.2, -12.8):                                # dark segment bands across the abdomen sides
        b.hull([A(*p) for p in ring(10.0, [(5.9, z - 0.45), (5.9, z + 0.45)]) + ring(14.4, [(7.95, z - 0.5), (7.95, z + 0.5)]) +
                ring(18.8, [(5.6, z - 0.4), (5.6, z + 0.4)])], 'dark', bevel=0.05)
    b.cyl(A(0, 13.0, -21.0), A(0, 13.0, -21.9), 0.85, 8, 'lightc')    # spinneret glow (rear)

    # ------------------------------------------------------------------ turret (0, 22.9, -12.89): emitter mount
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, -3.6, 0), T(0, -0.4, 0), 2.6, 10, 'dark', bevel=0.12)                 # pedestal
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.6, -0.5, -4.4), (3.8, -0.5, 0.2), (1.9, -0.5, 3.4), (3.2, 2.3, -4.0), (3.3, 2.3, 0.0), (1.5, 2.1, 2.6)]],
           'paint', bevel=0.2)
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.7, 2.36, -3.5), (2.8, 2.36, -0.1), (1.2, 2.2, 2.0), (2.6, 2.56, -3.4), (2.7, 2.56, -0.2), (1.1, 2.4, 1.9)]],
           'team', bevel=0.03)
    t.cyl(T(0, 0.9, -4.3), T(0, 0.9, -5.3), 1.0, 8, 'dark')

    # ------------------------------------------------------------------ emitters: built once, cloned (barrel2 = mirror)
    g = k.piece('barrel1'); G = g.at                      # muzzle (flare1) at local z 9.81
    g.cyl(G(0, 0, -3.4), G(0, 0, 8.6), 0.72, 10, 'dark', bevel=0.05)
    for z in (2.2, 4.4, 6.6):                             # cyan coil rings
        g.cyl(G(0, 0, z), G(0, 0, z + 0.7), 0.98, 10, 'lightc')
    g.cyl(G(0, 0, 8.5), G(0, 0, 9.7), 0.55, 8, 'steel', r2=0.3)
    g.sphere(G(0, 0, 9.75), 0.42, 'lightc', segs=8, rings=4)
    k.clone('barrel2', 'barrel1', mirror_x=True)
