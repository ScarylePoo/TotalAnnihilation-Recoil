"""Invader (ARM_T2_BOT_Invader) - Arm T2 crawling bomb. A squat armoured warhead shell, pointed fore and aft like
TA's, scuttling on four thin splayed legs. TA's four single-piece legs -> standard QUAD skeleton (shared quad walk);
script ported to scripts/ARM_T2_BOT_Invader.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
The `base` piece (the shell) has its origin on the ground and hangs off the new pelvis.
Top view (what makes it an Invader): a light lozenge with a broad hazard-striped belt (reads "bomb"), a team cap on
the dome, red arming lights, and four dark spider legs - smaller and flatter than any other Arm walker."""
import math

UNIT = dict(
    skeleton='quad',
    skeleton_opts=dict(height=5.0, hipx=4.2, hipz=3.6),
    res=1024,
    wreck=dict(seed=3, drop=[], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(thigh='dark', shin='paint2', foot='dark', width=2.2, armour=False)

    # ------------------------------------------------------------------ pelvis (0, 5, 0): leg yoke under the shell
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, -1.4, -4.2), (4.4, -1.4, 4.2), (3.8, 0.6, -3.6), (3.8, 0.6, 3.6), (2.8, -2.2, -3.0), (2.8, -2.2, 3.0)]],
           'dark', bevel=0.12)

    # ------------------------------------------------------------------ base (origin on the ground): warhead shell
    b = k.piece('base')
    ring = lambda y, rx, rz, tip: [(rx * math.cos(a), y, rz * math.sin(a) * (tip if abs(math.cos(a)) < 0.3 else 1.0))
                                   for a in [i * math.pi / 6 for i in range(12)]]
    # lower hull, belt and dome (pointed fore/aft)
    b.hull(ring(3.0, 3.8, 5.6, 1.25) + ring(4.4, 5.0, 6.6, 1.25), 'paint2', bevel=0.12)
    b.hull(ring(4.45, 5.15, 6.75, 1.25) + ring(5.6, 5.15, 6.75, 1.25), 'hazard', bevel=0.08)
    b.hull(ring(5.65, 4.9, 6.5, 1.25) + ring(7.0, 3.9, 5.2, 1.2) + ring(8.0, 2.2, 3.0, 1.1), 'paint', bevel=0.14)
    # team cap on the dome
    b.hull(ring(7.9, 2.3, 3.1, 1.1) + ring(8.15, 1.9, 2.6, 1.1), 'team', bevel=0.04)
    # arming lights fore and aft, detonator stud on top
    for z in (-7.3, 7.3):
        b.box((-0.7, 4.7, z - 0.35), (0.7, 5.35, z + 0.35), 'lightr', bevel=0.0)
    b.cyl((0, 8.1, 0), (0, 8.9, 0), 0.7, 8, 'dark', bevel=0.04)
    b.cyl((0, 8.85, 0), (0, 9.05, 0), 0.4, 8, 'lightr')
