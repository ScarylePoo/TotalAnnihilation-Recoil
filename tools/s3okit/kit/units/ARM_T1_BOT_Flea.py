"""Flea (ARM_T1_BOT_Flea) - Arm fast light scout kbot, the smallest Arm walker. A low rounded carapace on four splayed
legs, a sensor head hanging off the front, and a tiny laser turret on top. Standard QUAD skeleton (TA's 4 legs ->
rf/lf/rb/lb thigh/leg/foot, shared quad walk); script ported to scripts/ARM_T1_BOT_Flea.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Flea): a short wide light egg with team plates on both shoulders, a dark turret dot with a
single needle barrel forward, four dark legs sticking out at the corners like an insect. Nothing else in the Arm
roster is a quad, so the splayed-leg X silhouette is the read; legs are widened so they survive at distance."""
import math

UNIT = dict(
    skeleton='quad',
    skeleton_opts=dict(height=5.6, hipx=3.4, hipz=3.0),
    res=1024,
    wreck=dict(seed=9, drop=[], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(thigh='dark', shin='paint2', foot='dark', width=2.3, armour=False)

    # ------------------------------------------------------------------ pelvis (0, 5.6, 0): leg yoke under the body
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -0.6, -3.6), (3.0, -0.6, 3.6), (2.4, 1.2, -3.0), (2.4, 1.2, 3.0), (1.6, -1.4, -2.4), (1.6, -1.4, 2.4)]],
           'dark', bevel=0.12)

    # ------------------------------------------------------------------ body (0, 7.25, 1.88): domed carapace
    b = k.piece('body'); B = b.at
    # egg-shaped shell: wide, low, longer than wide, rear rounded (several hull rings)
    ring = lambda y, rx, rz, z0: [B(rx * math.cos(a), y, z0 + rz * math.sin(a)) for a in [i * math.pi / 6 for i in range(12)]]
    b.hull(ring(-1.0, 4.4, 5.0, -2.4) + ring(1.0, 4.9, 5.6, -2.4) + ring(2.8, 4.0, 4.6, -2.6) + ring(4.0, 2.2, 2.8, -2.8),
           'paint', bevel=0.12)
    # team plates on the carapace shoulders either side of the turret (visible from above, not hidden by it)
    b.hull([B(x, y, z) for x, y, z in
            [(2.0, 3.7, -5.6), (3.6, 2.9, -5.0), (2.0, 3.7, 0.4), (3.6, 2.9, 0.0),
             (2.0, 3.86, -5.55), (3.55, 3.06, -4.95), (2.0, 3.86, 0.35), (3.55, 3.06, -0.05)]], 'team', bevel=0.03, mirror=True)
    # dark belly rim (separates carapace from legs in every view)
    b.hull(ring(-1.6, 4.0, 4.6, -2.4) + ring(-0.6, 4.5, 5.1, -2.4), 'paint2', bevel=0.08)
    # two exhaust ports at the rear
    for sx in (-1, 1):
        b.cyl(B(1.6 * sx, 1.0, -7.4), B(1.6 * sx, 1.2, -8.3), 0.7, 8, 'dark', bevel=0.04)
        b.cyl(B(1.6 * sx, 1.2, -8.25), B(1.6 * sx, 1.22, -8.35), 0.4, 8, 'black')

    # ------------------------------------------------------------------ head (0, 10.67, 3.3): sensor head at the front
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, -4.6, 0.6), (2.6, -2.4, 0.4), (1.8, -4.4, 4.6), (2.0, -2.6, 4.2), (1.0, -3.4, 5.8)]], 'paint2', bevel=0.15)
    for sx in (-1, 1):                                       # two cyan eyes
        h.cyl(H(1.1 * sx, -3.4, 4.6), H(1.15 * sx, -3.4, 5.3), 0.55, 8, 'dark')
        h.cyl(H(1.15 * sx, -3.4, 5.25), H(1.16 * sx, -3.4, 5.4), 0.38, 8, 'lightc')
    h.box(H(-1.2, -4.9, 2.0), H(1.2, -4.5, 4.0), 'dark', bevel=0.04)                         # mandible plate

    # ------------------------------------------------------------------ turret (0, 11.87, -0.37)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, -0.9, 0), T(0, 0.2, 0), 2.2, 10, 'dark', bevel=0.06)
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.9, 0.2, -1.9), (1.9, 0.2, 1.6), (1.4, 1.7, -1.4), (1.4, 1.7, 1.3), (1.0, 0.9, 2.6)]], 'dark', bevel=0.12)
    t.box(T(-0.9, 1.68, -1.0), T(0.9, 1.82, 0.9), 'team', bevel=0.03)
    t.box(T(-1.1, -0.5, 1.6), T(1.1, 1.0, 3.4), 'dark', bevel=0.08)                          # mantlet

    # ------------------------------------------------------------------ barrel (0, 12, 3.5): needle laser
    r = k.piece('barrel'); R = r.at
    r.cyl(R(0, 0, -1.6), R(0, 0, 6.6), 0.5, 8, 'steel')
    r.cyl(R(0, 0, 0.0), R(0, 0, 1.4), 0.75, 8, 'dark', bevel=0.04)
    r.cyl(R(0, 0, 6.4), R(0, 0, 7.2), 0.62, 8, 'dark', bevel=0.03)
    r.cyl(R(0, 0, 7.15), R(0, 0, 7.3), 0.32, 8, 'lightr')
