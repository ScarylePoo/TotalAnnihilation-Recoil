"""Advanced Construction Kbot (ARM_T2_BOT_AdvancedConstructor) - Arm T2 builder. A walker carrying two big equipment
pods on its shoulders under one hinged roof (guncase); to build, the roof swings up and back, and a folding frame
(nanoarm + nanojoint) lifts two nano emitters out of the pods and flips them forward. Standard biped skeleton with
wide-set legs; script ported to scripts/ARM_T2_BOT_AdvancedConstructor.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it the Arm T2 builder): two large light roof panels with team plates and yellow hazard front
edges side by side, split by a dark hinge - a wide square "double crate", bigger than the T1 builder's single dome."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=6.6),
    res=1024,
    always_visible=['nanoarm', 'nanojoint', 'lnanogun', 'rnanogun'],
    wreck=dict(seed=18, drop=['guncase'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.75)

    # ------------------------------------------------------------------ pelvis (0, 13.75, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -2.2, -3.0), (5.4, -2.2, 2.6), (5.8, 1.2, -3.4), (5.8, 1.2, 3.0), (3.0, -3.0, -2.2), (3.0, -3.0, 2.0)]],
           'paint2', bevel=0.18)

    # ------------------------------------------------------------------ torso (0, 14.5, -2.25): spine + two pods
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                              # central spine
            [(4.2, 0.0, -6.0), (4.2, 0.0, 6.0), (4.4, 7.6, -6.6), (4.4, 7.6, 6.2), (2.0, 2.0, 9.4), (2.4, 7.0, 8.4)]],
           'paint2', bevel=0.2)
    t.box(A(-1.6, 4.4, 8.6), A(1.6, 5.4, 8.95), 'lightc', bevel=0.0)                     # sensor strip
    for sx in (-1, 1):
        t.hull([A(sx * x, y, z) for x, y, z in                                            # equipment pod
                [(4.4, 0.6, -8.4), (4.4, 0.6, 7.0), (13.2, 1.6, -8.2), (13.2, 1.6, 6.8), (4.4, 8.9, -9.0), (4.4, 8.9, 7.0),
                 (13.8, 8.9, -8.8), (13.8, 8.9, 6.8), (13.4, 4.4, 7.6), (4.6, 4.4, 8.4)]], 'paint', bevel=0.22)
        t.box(A(sx * 13.7 - 0.25, 2.8, -6.4), A(sx * 13.7 + 0.25, 6.8, 4.6), 'paint2', bevel=0.06)   # side panel
        t.box(A(sx * 9.0 - 1.6, 1.0, -9.15), A(sx * 9.0 + 1.6, 6.4, -8.6), 'dark', bevel=0.06)      # rear vents
        for y in (2.0, 3.4, 4.8):
            t.box(A(sx * 9.0 - 1.2, y, -9.3), A(sx * 9.0 + 1.2, y + 0.5, -9.05), 'black', bevel=0.0)

    # ------------------------------------------------------------------ roof (guncase, 0, 23.5, -6.5): hinged at the back
    g = k.piece('guncase'); G = g.at
    for sx in (-1, 1):
        g.hull([G(sx * x, y, z) for x, y, z in
                [(4.6, 0.0, 0.2), (4.6, 0.0, 13.6), (13.8, 0.0, 0.2), (13.8, 0.0, 13.6), (5.6, 3.6, 1.0), (5.6, 3.6, 12.6),
                 (12.8, 3.6, 1.0), (12.8, 3.6, 12.6)]], 'paint', bevel=0.2)
        g.hull([G(sx * x, y, z) for x, y, z in                                            # team plate
                [(6.6, 3.62, 2.4), (6.6, 3.62, 9.6), (11.8, 3.62, 2.4), (11.8, 3.62, 9.6),
                 (6.6, 3.78, 2.45), (6.6, 3.78, 9.55), (11.8, 3.78, 2.45), (11.8, 3.78, 9.55)]], 'team', bevel=0.03)
        g.hull([G(sx * x, y, z) for x, y, z in                                            # hazard front edge
                [(5.8, 3.0, 12.7), (12.6, 3.0, 12.7), (5.8, 0.6, 13.7), (12.6, 0.6, 13.7),
                 (5.8, 3.12, 12.85), (12.6, 3.12, 12.85), (5.8, 0.7, 13.85), (12.6, 0.7, 13.85)]], 'hazard', bevel=0.02)
    g.cyl(G(-4.8, 0.8, 0.8), G(4.8, 0.8, 0.8), 1.0, 10, 'dark', bevel=0.04)              # hinge bar
    g.box(G(-4.8, 0.0, 0.6), G(4.8, 1.2, 4.0), 'dark', bevel=0.08)

    # ------------------------------------------------------------------ folding frame + nano emitters
    a = k.piece('nanoarm'); N = a.at                    # (0, 26, 3.75): frame lying along -z
    for sx in (-1, 1):
        a.box(N(sx * 7.6 - 0.6, -0.9, -9.2), N(sx * 7.6 + 0.6, 0.7, 1.8), 'dark', bevel=0.06)
    a.box(N(-8.3, -0.6, 0.4), N(8.3, 0.6, 1.8), 'paint2', bevel=0.06)
    j = k.piece('nanojoint'); J = j.at                  # (0, 25, -5.5): cross bar carrying the emitters
    j.cyl(J(-10.0, -1.6, 1.0), J(10.0, -1.6, 1.0), 1.2, 10, 'steel')
    j.box(J(-2.4, -3.2, 0.0), J(2.4, -0.2, 2.2), 'dark', bevel=0.08)
    n = k.piece('lnanogun'); L = n.at                   # (8.25, 22, -3.25): emitter along +z, spray at (-0.25, 0, 9.75)
    n.box(L(-2.6, -2.4, 0.0), L(2.6, 2.4, 3.6), 'paint2', bevel=0.12)
    n.cyl(L(-0.25, 0, 3.4), L(-0.25, 0, 8.4), 1.3, 10, 'steel')
    for z in (4.6, 6.4):
        n.cyl(L(-0.25, 0, z), L(-0.25, 0, z + 0.6), 1.7, 10, 'dark')
    n.cyl(L(-0.25, 0, 8.3), L(-0.25, 0, 9.4), 1.0, 10, 'steel', r2=0.6)
    n.cyl(L(-0.25, 0, 9.35), L(-0.25, 0, 9.7), 0.6, 10, 'lightc')
    k.clone('rnanogun', 'lnanogun', mirror_x=True)
