"""Storm (CORE_T1_BOT_Storm) - Core rocket kbot. Modelled to the third-party S3O's piece layout (its COB drives those
pieces; the original is preserved in tools/s3okit/ref/ on install): a small torso carrying two big slab rocket
launchers on its shoulders (lgun on -X, rgun on +X, as the original names them), each with two fat launch tubes
(?barrel1 / ?barrel2) running through it. The whole torso turns and pitches to aim. Standard biped skeleton;
script ported to scripts/CORE_T1_BOT_Storm.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Storm): two broad dark warm slabs side by side covering the unit, each with a team plate
and a row of two LIGHT steel tube mouths poking out front AND back; the tiny torso between them is dark. Reads as a
flat 2x2 tube battery - unlike the Thud (two long barrels) or the A.K. (crest + small pods)."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=4.2),
    res=1024,
    wreck=dict(seed=15, drop=['rgun'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.5)

    # ------------------------------------------------------------------ pelvis (0, 12.47, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, -2.2, -4.0), (3.2, -2.2, 3.4), (3.8, 2.8, -4.6), (3.8, 2.8, 4.2), (2.0, -3.6, -2.4), (2.0, -3.6, 2.2)]],
           'paint2', bevel=0.16)

    # ------------------------------------------------------------------ torso (0, 17.39, 0): small core, dark
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -2.4, 0), A(0, 0.4, 0), 2.6, 10, 'dark', bevel=0.08)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 0.2, -3.4), (2.6, 0.2, 3.2), (2.6, 5.4, -3.0), (2.2, 5.4, 2.6), (1.8, 2.6, 4.6)]], 'paint', bevel=0.16)
    t.box(A(-1.4, 2.6, 4.2), A(1.4, 3.2, 4.65), 'lightr', bevel=0.0)                           # eye slit
    t.cyl(A(-2.6, 3.0, 0.4), A(2.6, 3.0, 0.4), 1.4, 10, 'dark', bevel=0.05)                    # launcher axle
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                                    # ochre spine on top
            [(0.8, 5.38, -2.6), (0.8, 5.38, 2.2), (0.75, 5.54, -2.55), (0.75, 5.54, 2.15)]], 'hazard', bevel=0.02)

    # ------------------------------------------------------------------ launcher slab lgun (-2.55, 20.14, 0.37)
    g = k.piece('lgun'); G = g.at                        # spans local x -8.7..0, y -2.7..4.6, z -7.1..6.9
    g.hull([G(x, y, z) for x, y, z in
            [(-0.4, -2.6, -4.4), (-0.4, -2.6, 4.6), (-8.8, -2.6, -4.4), (-8.8, -2.6, 4.6),
             (-0.6, 3.6, -3.8), (-0.6, 3.2, 4.0), (-8.4, 3.6, -3.8), (-8.4, 3.2, 4.0)]], 'paint', bevel=0.22)
    g.hull([G(x, y, z) for x, y, z in                                                            # team plate on top
            [(-1.6, 3.62, -2.8), (-7.4, 3.62, -2.8), (-1.6, 3.28, 3.0), (-7.4, 3.28, 3.0),
             (-1.6, 3.78, -2.75), (-7.4, 3.78, -2.75), (-1.6, 3.44, 2.95), (-7.4, 3.44, 2.95)]], 'team', bevel=0.03)
    g.hull([G(x, y, z) for x, y, z in                                                            # paint2 underside band
            [(-0.5, -2.62, -4.2), (-8.7, -2.62, -4.2), (-0.5, -2.62, 4.4), (-8.7, -2.62, 4.4),
             (-0.5, -1.2, -4.45), (-8.7, -1.2, -4.45), (-0.5, -1.2, 4.65), (-8.7, -1.2, 4.65)]], 'paint2', bevel=0.06)
    g.box(G(-9.0, -1.0, -2.6), G(-8.6, 1.6, 2.6), 'dark', bevel=0.06)                           # side hatch

    # ------------------------------------------------------------------ launch tube (built on lbarrel1, cloned x4)
    b = k.piece('lbarrel1'); B = b.at                   # local z -2..14.5 (front at +14)
    b.cyl(B(0, 0.05, -2.4), B(0, 0.05, 14.4), 1.5, 10, 'steel', bevel=0.06)                   # LIGHT tube
    b.cyl(B(0, 0.05, 13.4), B(0, 0.05, 14.6), 1.75, 10, 'dark', bevel=0.05)                   # muzzle ring
    b.cyl(B(0, 0.05, 14.55), B(0, 0.05, 14.7), 1.05, 10, 'black')
    b.cyl(B(0, 0.05, -2.6), B(0, 0.05, -1.6), 1.75, 10, 'dark', bevel=0.05)                   # rear vent ring
    b.cyl(B(0, 0.05, -2.75), B(0, 0.05, -2.6), 1.05, 10, 'black')
    b.cyl(B(0, 0.05, 9.0), B(0, 0.05, 9.6), 1.62, 10, 'dark', bevel=0.03)                    # clamp ring
    k.clone('lbarrel2', 'lbarrel1')
    k.clone('rgun', 'lgun', mirror_x=True)
    k.clone('rbarrel1', 'lbarrel1', mirror_x=True)
    k.clone('rbarrel2', 'lbarrel1', mirror_x=True)
