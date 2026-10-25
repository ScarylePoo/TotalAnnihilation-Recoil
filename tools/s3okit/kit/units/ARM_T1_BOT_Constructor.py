"""Construction Kbot (ARM_T1_BOT_Constructor) - Arm T1 builder. A squat wide box on short legs under a big gabled roof
made of two panels (lflap / rflap) that the script folds out sideways to raise the nano gun: arms + nanobody2 swing
it up, nozzle telescopes forward through the front hatch (guncover, swings up 126 deg), turret turns it toward the
build. Standard biped skeleton (TA's model only had sliding feet; legs are new); script ported to
scripts/ARM_T1_BOT_Constructor.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it the Arm builder): one broad light gable roof with a team ridge band and dark ridge vents,
a hazard-striped front hatch (construction equipment, it opens and the nozzle comes out there), short dark legs
barely showing at the sides. Open, the panels stand up like wings and the cyan nano emitter is exposed."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(height=9.0, hipx=6.0),
    res=1024,
    wreck=dict(seed=10, drop=['rflap'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.7)

    # ------------------------------------------------------------------ pelvis (0, 9, 0): the box body
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.6, -0.6, -11.0), (8.6, -0.6, 6.0), (9.6, 4.2, -12.0), (9.6, 4.2, 7.0),
             (9.2, 6.4, -11.6), (9.2, 6.4, 6.4), (7.6, 1.6, 8.6), (7.4, -0.2, 7.4)]], 'paint2', bevel=0.22)
    # light side skirts (the body sides that show under the roof edge)
    p.hull([Q(x, y, z) for x, y, z in
            [(9.62, 1.2, -10.4), (9.62, 1.2, 5.4), (9.62, 4.0, -11.0), (9.62, 4.0, 6.0),
             (10.2, 1.6, -10.0), (10.2, 1.6, 5.0), (10.2, 3.8, -10.6), (10.2, 3.8, 5.6)]], 'paint', bevel=0.1, mirror=True)
    # rear tool racks / tail lights
    p.box(Q(-6.4, 1.0, -12.6), Q(6.4, 4.6, -11.8), 'dark', bevel=0.08)
    for sx in (-1, 1):
        p.box(Q(5.0 * sx - 0.6, 3.6, -12.7), Q(5.0 * sx + 0.6, 4.2, -12.55), 'lightr', bevel=0.0)
    # front headlights either side of the hatch
    for sx in (-1, 1):
        p.box(Q(6.0 * sx - 0.9, 1.6, 8.0), Q(6.0 * sx + 0.9, 2.6, 8.7), 'dark', bevel=0.05)
        p.box(Q(6.0 * sx - 0.7, 1.75, 8.68), Q(6.0 * sx + 0.7, 2.45, 8.78), 'lightw', bevel=0.0)

    # ------------------------------------------------------------------ turret (0, 14, -1): ring + nano cradle
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, -0.4, 0), T(0, 0.5, 0), 6.0, 16, 'dark', bevel=0.06)
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 0.5, -6.0), (5.6, 0.5, 4.0), (5.0, 2.6, -5.6), (5.0, 2.6, 3.6)]], 'paint2', bevel=0.14)

    # ------------------------------------------------------------------ nano gun: arms -> nanobody2 -> nozzle
    a = k.piece('arms'); R = a.at                                   # (0, 16, 0.5)
    a.cyl(R(-4.6, 0, 0), R(4.6, 0, 0), 1.0, 10, 'dark', bevel=0.04)
    for sx in (-1, 1):
        a.box(R(3.4 * sx - 0.6, -0.8, -5.6), R(3.4 * sx + 0.6, 0.8, 0.6), 'dark', bevel=0.08)
    n = k.piece('nanobody2'); N = n.at                              # (0, 16, -4.5)
    n.box(N(-2.7, -1.2, -2.6), N(2.7, 3.4, 3.6), 'dark', bevel=0.16)
    n.cyl(N(0, 2.0, -2.6), N(0, 2.0, -3.2), 1.6, 10, 'dark', bevel=0.04)
    z = k.piece('nozzle'); Z = z.at                                 # (0, 18, -6.5), extends +z
    z.cyl(Z(0, 0, 0.0), Z(0, 0, 9.4), 1.15, 10, 'steel')
    z.cyl(Z(0, 0, 8.4), Z(0, 0, 9.9), 1.65, 10, 'dark', bevel=0.05)
    z.cyl(Z(0, 0, 9.85), Z(0, 0, 10.2), 1.25, 10, 'lightc', r2=0.7)   # nano emitter

    # ------------------------------------------------------------------ front hatch guncover (0, 14, 4.75)
    g = k.piece('guncover'); G = g.at
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 0.0, 0.0), (4.2, 0.0, 3.4), (4.0, 7.2, 0.0), (4.0, 6.0, 3.0)]], 'paint', bevel=0.12)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in                     # hazard face
            [(3.4, 0.8, 3.36), (3.3, 5.6, 3.09), (3.4, 0.8, 3.52), (3.3, 5.6, 3.25)]], 'hazard', bevel=0.02)

    # ------------------------------------------------------------------ roof panels (lflap built, rflap = mirror)
    f = k.piece('lflap'); F = f.at                                  # hinge (8, 22, 0)
    # gabled panel: inner edge high at the ridge (global x 0.15), outer edge low; nose and tail chamfered
    pr = [(-11.4, 0.0), (10.0, 0.0), (12.6, -1.0)]
    f.hull([F(x - 8, y, zz) for (x, ytop) in ((0.2, 5.0), (13.4, 0.6)) for y in (ytop, ytop - 1.7)
            for zz in ((-11.4, 10.6) if x < 1 else (-10.8, 9.4))] +
           [F(0.2 - 8, 4.0, 12.6), F(0.2 - 8, 2.6, 12.6), F(8.0 - 8, 2.4, 11.8), F(8.0 - 8, 1.0, 11.6)],
           'paint', bevel=0.2)
    # team band along the ridge
    f.hull([F(x - 8, y, zz) for (x, y) in ((0.8, 4.84), (3.4, 3.98)) for zz in (-9.6, 8.4)] +
           [F(x - 8, y + 0.16, zz) for (x, y) in ((0.8, 4.84), (3.4, 3.98)) for zz in (-9.5, 8.3)], 'team', bevel=0.03)
    # dark vent block near the rear outer corner, and a dark lip along the outer edge
    f.hull([F(x - 8, y, zz) for (x, y) in ((6.0, 3.24), (9.6, 2.04)) for zz in (-8.2, -3.6)] +
           [F(x - 8, y + 0.9, zz) for (x, y) in ((6.4, 3.1), (9.2, 2.2)) for zz in (-7.8, -4.0)], 'dark', bevel=0.08)
    f.hull([F(x - 8, y, zz) for x in (12.9, 13.7) for (y, zz) in ((0.5, -10.4), (0.5, 9.0), (-4.6, -9.6), (-4.6, 8.0))],
           'dark', bevel=0.1)                                              # deep side skirt: closes the gap
    k.clone('rflap', 'lflap', mirror_x=True)
