"""Advanced Construction Kbot (CORE_T2_BOT_AdvancedConstructor) - Core T2 builder. TA's model walks on four spike
legs (fore/hind pairs; inspect guessed biped): standard QUAD skeleton. A low leg platform carries a squat front column
(torso) and, behind it, two long hexagonal nano cases stacked one above the other; to build, the cases slide out
sideways, swing round 90 deg, their end doors flap open and the nano guns telescope out. Script ported to
scripts/CORE_T2_BOT_AdvancedConstructor.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes the Core T2 builder): a dark-warm four-legged crab with a long case across its back in
construction stripes (hazard, with dark clamp bands and a team plate; the builder read from the game camera) - a quad, so it never reads like the Arm T2 builder's double crate."""
import math

UNIT = dict(
    skeleton='quad',
    skeleton_opts=dict(hipx=7.0, hipz=5.0),
    res=1024,
    always_visible=['lnanogun', 'rnanogun'],
    wreck=dict(seed=32, drop=['rnanocase'], remove=[]),
    preview_pose={},
)


def nanocase(k, case, door, gun, sx):
    """hex case along x on piece `case`; the open end (door) faces sx (+1 = +x end); gun telescopes from inside."""
    c = k.piece(case); C = c.at
    o = k.P[case]                                      # prism() takes GLOBAL x and (z, y)
    G_ = lambda prof: [(o.z + z, o.y + y) for z, y in prof]
    x0, x1 = (-3.5, 9.4) if sx > 0 else (-9.4, 3.5)
    hexa = [(-4.8 + 4.6 * math.cos(a), 4.2 * math.sin(a)) for a in [i * math.pi / 3 for i in range(6)]]
    c.prism(o.x + x0, o.x + x1, G_(hexa), 'hazard', bevel=0.2)                     # construction stripes
    c.prism(o.x + x0 + 1.6, o.x + x1 - 1.6, G_([(z, y + 0.08) for z, y in [(-7.2, 3.66), (-2.4, 3.66), (-2.4, 3.86), (-7.2, 3.86)]]),
            'team', bevel=0.03)
    for xb in ((x0 + 3.0, x0 + 3.8), (x1 - 3.8, x1 - 3.0)):                             # dark clamp bands
        c.prism(o.x + xb[0], o.x + xb[1], G_([(-4.8 + 4.8 * math.cos(a), 4.4 * math.sin(a)) for a in [i * math.pi / 3 for i in range(6)]]),
                'dark', bevel=0.04)
    d = k.piece(door); D = d.at                        # flat plate hinged at its top edge
    d.box(D(-0.15 if sx > 0 else -0.45, -9.0, -4.4), D(0.45 if sx > 0 else 0.15, -0.2, 4.4), 'paint2', bevel=0.08)
    g = k.piece(gun); G = g.at                         # along sx from the joint
    s = sx
    g.cyl(G(0, 0.15, 0), G(s * 7.6, 0.15, 0), 1.5, 10, 'steel')
    g.cyl(G(s * 2.0, 0.15, 0), G(s * 2.8, 0.15, 0), 1.85, 10, 'dark')
    g.cyl(G(s * 7.4, 0.15, 0), G(s * 8.8, 0.15, 0), 1.2, 10, 'steel', r2=0.7)
    g.cyl(G(s * 8.75, 0.15, 0), G(s * 9.1, 0.15, 0), 0.75, 10, 'lightc')


def build(k):
    k.standard_legs(thigh='paint2', shin='dark', foot='dark', width=1.7, armour=True)

    # ------------------------------------------------------------------ pelvis (0, 10.5, 0): leg platform
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, -2.2, -7.0), (6.6, -2.2, 6.4), (6.6, 2.0, -7.4), (6.6, 2.0, 6.8), (4.0, -3.0, -5.0), (4.0, -3.0, 4.6)]],
           'paint2', bevel=0.2)
    p.box(Q(-1.4, 1.9, -7.0), Q(1.4, 2.4, 5.0), 'hazard', bevel=0.04)

    # ------------------------------------------------------------------ torso (0, 22.5, -5): front column
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, -9.6, -1.2), (4.4, -9.6, 6.6), (5.0, -2.0, -1.4), (5.0, -2.0, 7.4), (4.2, 5.4, -1.0), (4.0, 5.4, 5.6),
             (2.6, 1.0, 8.6)]], 'paint', bevel=0.22)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # dark visor
            [(3.4, 0.0, 7.7), (3.2, 2.6, 7.2), (3.4, 0.0, 7.95), (3.2, 2.6, 7.45)]], 'dark', bevel=0.04)
    for x in (-2.0, 0.0, 2.0):
        t.box(A(x - 0.5, 1.0, 7.9), A(x + 0.5, 1.6, 8.05), 'lightw', bevel=0.0)
    t.box(A(-2.6, 5.35, 0.0), A(2.6, 5.55, 4.6), 'team', bevel=0.03)
    t.box(A(-1.2, -8.0, -2.6), A(1.2, 5.0, -1.0), 'dark', bevel=0.08)                  # spine holding the cases

    # ------------------------------------------------------------------ the two stacked nano cases
    nanocase(k, 'lnanocase', 'lcasedoor', 'lnanogun', +1)    # lower case, opens at +x
    nanocase(k, 'rnanocase', 'rcasedoor', 'rnanogun', -1)    # upper case, opens at -x
