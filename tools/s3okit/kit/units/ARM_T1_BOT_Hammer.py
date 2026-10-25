"""Hammer (ARM_T1_BOT_Hammer) - Arm artillery kbot. Narrow sensor tower for a torso, a cross-axle at shoulder height
with two big hexagonal trunnion drums, one heavy cannon in each drum. The front halves of both cannons sit in
armoured clamshells (upcase2 = upper shells, locase = lower shells) that the script swings open and slides back
when the unit deploys to fire, and closes again when it stows. Standard biped skeleton (backwards legs, shared walk);
script ported to scripts/ARM_T1_BOT_Hammer.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Hammer): two long parallel gun shells far out to the sides with team stripes, light hex
drums, a small light tower between them; dark cannons, axle and feet; paint2 lower shells and back pack."""
import math

UNIT = dict(
    skeleton='biped',
    res=1024,
    wreck=dict(seed=5, drop=['upcase2'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs()                      # thighs paint, shins paint2, feet dark; all legs share one UV set

    # ------------------------------------------------------------------ pelvis (0, 16.63, 0): hip block
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -1.6, -2.6), (3.0, -1.6, 2.2), (3.6, 1.2, -3.0), (3.6, 1.2, 2.4), (2.2, -2.8, -1.4), (2.2, -2.8, 1.0)]],
           'paint2', bevel=0.14)

    # ------------------------------------------------------------------ torso (0, 19.33, -7.34): narrow sensor tower
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -1.6, 7.3), A(0, 0.6, 7.3), 2.4, 10, 'dark', bevel=0.08)                 # waist over the pelvis
    # main tower: narrow, tall, sloped front, between the gun drums
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.4, -3.8), (3.8, 0.4, 7.6), (3.9, 5.5, -4.4), (3.9, 5.5, 6.6),
             (3.2, 9.4, -3.6), (3.2, 9.4, 3.4), (3.0, 7.6, 6.2)]], 'paint', bevel=0.2)
    # visor: dark brow with a cyan sensor strip, on the sloped front
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.5, 6.9, 6.25), (2.4, 8.8, 4.0), (2.5, 7.0, 6.45), (2.4, 8.9, 4.2)]], 'dark', bevel=0.05)
    t.box(A(-1.7, 7.55, 5.35), A(1.7, 7.95, 5.75), 'lightc', bevel=0.0)
    # team cap on the tower roof
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.5, 9.38, -2.9), (2.5, 9.38, 2.8), (2.45, 9.54, -2.85), (2.45, 9.54, 2.75)]], 'team', bevel=0.04)
    # rear ammunition pack (darker), with a feed slot
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 0.8, -3.6), (3.2, 7.4, -3.6), (2.8, 1.4, -7.0), (2.6, 6.6, -6.6)]], 'paint2', bevel=0.16)
    t.box(A(-1.9, 2.4, -7.0), A(1.9, 3.2, -6.7), 'black', bevel=0.0)
    t.box(A(-1.9, 4.0, -6.85), A(1.9, 4.8, -6.55), 'black', bevel=0.0)
    # range-finder mast (asymmetric), as on the TA model
    t.cyl(A(1.2, 9.4, -1.6), A(1.2, 10.0, -1.6), 0.45, 8, 'dark')
    t.cyl(A(1.2, 10.0, -1.6), A(1.2, 14.2, -1.6), 0.13, 6, 'steel', r2=0.07)
    t.cyl(A(1.2, 14.2, -1.6), A(1.2, 14.45, -1.6), 0.2, 6, 'lightc')

    # ------------------------------------------------------------------ canbase (0, 22.26, -10.27): axle + hex drums
    c = k.piece('canbase'); C = c.at
    c.cyl(C(-5.0, 0, 0), C(5.0, 0, 0), 1.9, 12, 'dark', bevel=0.06)                      # cross axle through the tower
    rot = math.pi / 6                                                                      # flat face on top
    c.cyl(C(4.6, 0, 0), C(11.0, 0, 0), 3.5, 6, 'paint', rot=rot, bevel=0.2, mirror=True)   # trunnion drum
    c.cyl(C(11.0, 0, 0), C(11.8, 0, 0), 2.6, 6, 'dark', rot=rot, bevel=0.08, mirror=True)  # outer hub
    c.cyl(C(11.8, 0, 0), C(12.1, 0, 0), 1.2, 10, 'steel', mirror=True)
    # dark grip band round each drum (breaks the light drum from the light shell in the top view)
    c.cyl(C(7.4, 0, 0), C(8.4, 0, 0), 3.62, 6, 'dark', rot=rot, bevel=0.05, mirror=True)

    # ------------------------------------------------------------------ cannons (built once, cloned to the right)
    g = k.piece('lcannon'); G = g.at                                                       # (7.83, 22.16, -8.27)
    g.box(G(-1.7, -1.6, -3.4), G(1.7, 1.7, 2.2), 'dark', bevel=0.16)                       # breech in the drum
    g.cyl(G(0, 0.1, 2.0), G(0, 0.1, 15.4), 1.2, 10, 'dark', r2=1.0, bevel=0.06)            # heavy barrel
    g.cyl(G(0, 0.1, 6.0), G(0, 0.1, 6.6), 1.38, 10, 'steel')                               # reinforcing ring
    g.cyl(G(0, 0.1, 15.2), G(0, 0.1, 17.4), 1.5, 8, 'dark', rot=math.pi / 8, bevel=0.06)  # muzzle brake
    g.cyl(G(0, 0.1, 17.3), G(0, 0.1, 17.45), 0.7, 8, 'black')
    for sx in (-1, 1):
        g.box(G(1.3 * sx, -0.5, 15.6), G(1.55 * sx, 0.7, 16.9), 'black', bevel=0.0)
    k.clone('rcannon', 'lcannon', mirror_x=True)

    # ------------------------------------------------------------------ clamshells over the gun fronts
    # upcase2 (0, 25.56, -0.37): hinge at the top-back; closed it covers the upper half of both barrel fronts
    u = k.piece('upcase2'); U = u.at
    gx = 7.83
    u.hull([U(x, y, z) for x, y, z in
            [(gx - 3.1, -3.4, 0.2), (gx + 3.1, -3.4, 0.2), (gx - 3.1, -3.4, 6.2), (gx + 3.1, -3.4, 6.2),
             (gx - 2.5, 0.4, 0.4), (gx + 2.5, 0.4, 0.4), (gx - 2.5, -0.4, 5.6), (gx + 2.5, -0.4, 5.6)]],
           'paint', bevel=0.18, mirror=True)
    # wide team stripe along each shell top (the big team read from above)
    u.hull([U(x, y, z) for x, y, z in
            [(gx - 1.3, 0.4, 1.0), (gx + 1.3, 0.4, 1.0), (gx - 1.3, -0.26, 5.0), (gx + 1.3, -0.26, 5.0),
             (gx - 1.25, 0.56, 1.05), (gx + 1.25, 0.56, 1.05), (gx - 1.25, -0.1, 4.95), (gx + 1.25, -0.1, 4.95)]],
           'team', bevel=0.03, mirror=True)
    # locase (0, 19.08, -0.24): hinge at the bottom-back; lower halves, darker
    l = k.piece('locase'); L = l.at
    l.hull([L(x, y, z) for x, y, z in
            [(gx - 3.1, 3.05, 0.1), (gx + 3.1, 3.05, 0.1), (gx - 3.1, 3.05, 6.1), (gx + 3.1, 3.05, 6.1),
             (gx - 2.4, 0.0, 0.3), (gx + 2.4, 0.0, 0.3), (gx - 2.4, 0.6, 5.4), (gx + 2.4, 0.6, 5.4)]],
           'paint2', bevel=0.16, mirror=True)
    # muzzle ports in the closed shells' front faces
    l.box(L(gx - 1.6, 2.2, 6.0), L(gx + 1.6, 3.0, 6.2), 'black', bevel=0.0, mirror=True)
