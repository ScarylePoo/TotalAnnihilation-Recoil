"""Panther (ARM_T2_VEH_Panther) - Arm lightning tank. Fast, low hull slung between two separate tall track
pontoons (TA's open "H" plan), a long faceted turret carrying a thick lightning projector ringed with dark coil
discs, and a small missile pod on a post rising out of the turret roof (Rturret/Rgun: its own traverse, child of
base, so the post must pass through the turret's roof hole).
Value groups from above: light pontoon tops + turret, darker paint2 centre hull with a team spine stripe, near-black
open gaps between hull and pontoons, dark coil-ringed gun, a team-coloured lid on the missile pod.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=11, drop=['Rgun'], pose={'Lturret': (0, 40, 0), 'Lgun': (6, 0, 0)}),
    preview_pose={'Lturret': (0, -18, 0), 'Rturret': (0, -18, 0), 'Lgun': (-4, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: two track pontoons
    b = k.piece('base')
    xi, xo = 11.8, 17.4
    belt = [(-15.0, 0.0), (14.6, 0.0), (17.6, 2.6), (16.6, 5.4), (-16.0, 5.4), (-17.8, 2.6)]
    b.prism(xi, xo, belt, 'tread', bevel=0.16, mirror=True)
    for z in (-11.4, -5.7, 0.0, 5.7, 11.4):
        b.cyl((xi, 1.9, z), (xi - 0.45, 1.9, z), 1.6, 12, 'dark', mirror=True)
        b.cyl((xi - 0.45, 1.9, z), (xi - 0.7, 1.9, z), 0.65, 8, 'steel', mirror=True)
    # pontoon armour: tall boxes over the tracks, noses raked
    b.hull([(11.4, 9.0, -15.2), (17.8, 9.0, -15.2), (17.8, 9.0, 13.0), (11.4, 9.0, 13.0),
            (11.4, 6.8, 17.6), (17.8, 6.8, 17.6), (11.4, 7.0, -17.8), (17.8, 7.0, -17.8),
            (11.4, 5.4, -16.0), (18.2, 5.4, -15.6), (18.2, 5.4, 15.2), (11.4, 5.4, 15.8)], 'paint', bevel=0.16, mirror=True)
    # dark side skirt on the outer face of each pontoon
    b.hull([(17.9, 5.6, -15.4), (18.5, 5.6, -15.0), (18.5, 5.6, 14.4), (17.9, 5.6, 14.8),
            (17.6, 2.8, -14.0), (18.2, 2.8, -13.6), (18.2, 2.8, 12.8), (17.6, 2.8, 13.2)], 'paint2', bevel=0.1, mirror=True)
    # raked hazard noses (fast-attack marking, front only)
    b.hull([(11.9, 7.05, 17.15), (17.3, 7.05, 17.15), (11.9, 8.98, 13.3), (17.3, 8.98, 13.3),
            (11.9, 7.18, 17.25), (17.3, 7.18, 17.25), (11.9, 9.12, 13.4), (17.3, 9.12, 13.4)], 'hazard', bevel=0.03, mirror=True)
    # vents on the pontoon tops, rear
    b.box((12.6, 9.0, -14.2), (16.6, 9.5, -8.6), 'dark', bevel=0.08, mirror=True)
    for z in (-13.6, -12.4, -11.2, -10.0):
        b.box((12.9, 9.5, z), (16.3, 9.6, z + 0.55), 'black', bevel=0.0, mirror=True)
    b.box((13.2, 6.0, 17.5), (16.2, 6.9, 18.0), 'dark', bevel=0.05, mirror=True)
    b.box((13.4, 6.15, 17.98), (16.0, 6.75, 18.08), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ centre hull (crosses x = 0)
    # cross struts to the pontoons, in the black gap
    for z in (-10.0, 7.0):
        b.box((-11.8, 4.0, z - 1.6), (11.8, 6.2, z + 1.6), 'dark', bevel=0.1)
    b.prism(-8.6, 8.6, [(-17.0, 2.4), (14.6, 2.4), (17.4, 5.0), (16.0, 7.6), (-16.4, 7.6), (-17.4, 5.0)], 'paint2', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.2, 7.4, -16.4), (8.2, 7.4, 14.6), (6.6, 7.0, 17.0),
             (6.8, 11.4, -15.0), (6.8, 11.4, 6.0), (4.6, 9.8, 14.0)]], 'paint2', bevel=0.18)
    # team spine stripe down the hull centre (fore of the turret and behind it)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 9.92, 13.6), (2.0, 11.42, 6.2), (2.0, 10.06, 13.66), (2.0, 11.56, 6.26)]], 'team', bevel=0.03)
    b.box((-2.0, 11.4, -15.0), (2.0, 11.56, -8.6), 'team', bevel=0.03)
    # capacitor banks either side of the rear deck (light cylinders lying fore-aft)
    for x in (4.6,):
        b.cyl((x, 12.2, -15.4), (x, 12.2, -8.4), 1.2, 10, 'steel', rot=math.pi / 10, mirror=True)
        b.cyl((x, 12.2, -8.4), (x, 12.2, -7.8), 0.8, 10, 'dark', mirror=True)
    # nose sensor and lights
    b.box((-3.0, 8.4, 15.4), (3.0, 9.4, 16.2), 'dark', bevel=0.06)
    b.box((-2.6, 8.6, 16.18), (2.6, 9.2, 16.28), 'lightc', bevel=0.0)
    b.box((-6.6, 4.6, -17.6), (6.6, 7.0, -17.1), 'dark', bevel=0.05)
    b.box((5.0, 5.6, -17.7), (6.2, 6.2, -17.55), 'lightr', bevel=0.0, mirror=True)
    # antenna, rear left pontoon
    b.cyl((-15.4, 9.0, -16.2), (-15.4, 9.7, -16.2), 0.32, 8, 'dark')
    b.cyl((-15.4, 9.7, -16.2), (-15.4, 15.0, -16.2), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-15.4, 15.0, -16.2), (-15.4, 15.2, -16.2), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- Lturret (origin 0, 13.47, -2.24; turns y)
    t = k.piece('Lturret'); A = t.at
    t.cyl(A(0, -2.1, 0), A(0, -1.6, 0), 5.0, 18, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, -1.6, -6.4), (5.6, -1.6, 1.0), (4.2, -1.6, 6.2), (2.6, -1.6, 7.4),
             (4.0, 2.2, -5.8), (4.4, 2.2, 0.8), (3.2, 2.2, 5.0), (2.0, 2.2, 6.0)]], 'paint', bevel=0.16)
    # roof: two light plates either side of the missile post hole, dark collar around the post
    t.cyl(A(0, 2.1, -0.4), A(0, 2.6, -0.4), 2.1, 14, 'dark', bevel=0.06)
    t.box(A(2.4, 2.18, -4.8), A(3.6, 2.36, 3.8), 'paint2', bevel=0.04, mirror=True)
    # emitter housing at the gun root
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, -1.2, 4.0), (2.6, 1.6, 4.0), (2.2, -0.9, 7.6), (2.2, 1.3, 7.6)]], 'paint2', bevel=0.1)
    # power conduits along the turret flanks
    t.cyl(A(4.8, -0.6, -5.2), A(4.8, -0.6, 4.2), 0.55, 8, 'dark', mirror=True)

    # ---------------------------------------------------------------- Lgun (lightning projector, turns x)
    g = k.piece('Lgun'); G = g.at
    g.cyl(G(0, 0, 0.0), G(0, 0, 11.6), 1.05, 12, 'steel')
    for z in (2.0, 4.0, 6.0, 8.0):           # coil discs: dark rings that read as "electric" from above
        g.cyl(G(0, 0, z), G(0, 0, z + 0.7), 2.0, 12, 'dark', bevel=0.06)
    g.cyl(G(0, 0, 9.6), G(0, 0, 11.4), 1.5, 10, 'dark', r2=0.8, bevel=0.05)
    g.cyl(G(0, 0, 11.4), G(0, 0, 12.0), 0.7, 10, 'lightc', r2=0.3)
    g.box(G(-0.5, 1.2, 0.4), G(0.5, 2.6, 8.8), 'dark', bevel=0.06)          # top cable spine

    # ---------------------------------------------------------------- Rturret (post, child of base)
    r = k.piece('Rturret'); R = r.at
    r.cyl(R(0, 0.4, 0), R(0, 3.2, 0), 0.95, 10, 'steel', rot=math.pi / 10)
    r.box(R(-1.4, 2.6, -1.0), R(1.4, 3.4, 1.0), 'dark', bevel=0.08)

    # ---------------------------------------------------------------- Rgun (missile pod, turns x)
    m = k.piece('Rgun'); M = m.at
    m.hull([M(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 0.0, -4.4), (3.2, 0.0, 4.6), (3.0, 2.4, -4.2), (3.0, 2.4, 4.2)]], 'paint', bevel=0.12)
    m.box(M(-2.5, 2.35, -3.6), M(2.5, 2.55, 3.4), 'team', bevel=0.04)
    m.box(M(-2.9, 0.2, 4.5), M(2.9, 2.2, 4.8), 'dark', bevel=0.04)
    for x in (-1.6, 0.0, 1.6):
        m.cyl(M(x, 1.2, 4.7), M(x, 1.2, 4.9), 0.55, 8, 'black')
    m.box(M(-2.8, 0.4, -4.75), M(2.8, 2.0, -4.35), 'black', bevel=0.0)
