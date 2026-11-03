"""Advanced Construction Sub (ARM_T2_SEA_AdvancedConstructor) - Arm T2 underwater builder. The TA model's hammer: a wide
swept arrowhead bow far wider than the hull, two dark side pods, and a long gabled hangar down the spine whose roof
halves (door1/door2) swing up and slide into the walls while a lift (plate) raises the nano post (post > gun) above them.
From above (through 40 elmos of water): the longest striped block of any sub (construction stripes on the roof and
the lift), team on the arrowhead wings, dark pods and stern. Largest silhouette of the Arm subs.
Pieces (TA layout): GP (empty root), base, door1/door2 (turn z 67 deg, move y -7.9: door2 = mirrored clone), plate (move
y +14.1), post (turn y), gun, beam (empty nano point), wake1/2 (empty, at the pods' sterns).
Submarine: def has waterline 40 and SHIP_SUBMARINE, no floater; run.py resolves water=40 from the movement class. ground
stays at its default so undersides get less texture; no underside is culled because water is set.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    always_visible=['plate', 'post', 'gun'],       # inside the closed hangar at rest, raised by the build script
    wreck=dict(seed=21, drop=['door2'], pose={'door1': (0, 0, 40)}),
    preview_pose={},
)

HZ0, HZ1 = -27.6, 14.1          # hangar ends = the doors' z extent in the 3DO
WALL = 6.5                      # inner wall face, just outside the door hinge x (6.29)
WTOP = 15.1                     # wall top, just below the hinge height (15.19)
WING = 9.6                      # flat top of the arrowhead


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ keel and hangar walls (open-topped bay)
    # three lengthwise segments: full-length chamfer strips pack as long diagonal UV slivers
    for z0, z1 in ((HZ0, -13.8), (-13.8, 0.0), (0.0, HZ1)):
        b.hull(sym([(9.0, 0.6, z0), (9.0, 0.6, z1), (10.2, 2.2, z0), (10.2, 2.2, z1)]), 'paint2', bevel=0.2)
        b.hull([(x, y, z) for z in (z0, z1) for x, y in
                ((WALL, 2.0), (10.2, 2.0), (10.8, 8.6), (8.6, WTOP), (WALL, WTOP))], 'paint', bevel=0.2, mirror=True)
    # end walls of the bay
    b.hull(sym([(WALL, 2.0, HZ1), (WALL, WTOP, HZ1), (0.0, 17.6, HZ1), (WALL, 2.0, HZ1 + 1.0), (WALL, WTOP, HZ1 + 1.0), (0.0, 17.6, HZ1 + 1.0)]),
           'paint', bevel=0.1)
    # ------------------------------------------------------------------ dark gabled wedge forward of the hangar
    b.hull(sym([(10.2, 2.2, HZ1 + 0.6), (9.0, 13.6, HZ1 + 0.6), (0.0, 17.5, HZ1 + 0.6), (2.6, 7.6, 31.0), (0.0, 9.8, 32.0), (2.6, 3.8, 30.0)]),
           'paint2', bevel=0.18)
    # ------------------------------------------------------------------ arrowhead bow: wide, flat, light, team wings
    A = [(0.0, 36.0), (9.5, 32.6), (24.5, 16.8), (24.5, 14.8), (9.5, 14.8)]
    b.hull(sym([(x, WING, z) for x, z in A] + [(x * 0.96, 6.8, z - 0.3 if z > 15 else z) for x, z in A]), 'paint', bevel=0.2)
    b.hull([(x, y, z) for y in (WING - 0.05, WING + 0.2) for x, z in
            [(8.2, 15.6), (23.4, 15.6), (23.4, 16.6), (9.8, 31.0), (8.2, 32.4)]], 'team', bevel=0.04, mirror=True)
    b.box((24.45, 7.4, 15.0), (24.75, 9.2, 16.6), 'lightc', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ side pods (dark): pointed forward, wake at the stern
    pod = [(x, y, z) for z in (-4.2, 18.0) for x, y in ((11.8, 2.8), (15.2, 2.8), (17.0, 6.0), (17.0, 9.8), (15.2, 13.0), (11.8, 13.0), (10.4, 9.8), (10.4, 6.0))]
    pod += [(13.5, 6.4, 27.0), (13.5, 8.6, 27.0)]
    b.hull(pod, 'paint2', bevel=0.2, mirror=True)
    b.hull([(x, y, z) for y in (12.95, 13.2) for x, z in [(12.0, -2.6), (15.0, -2.6), (15.0, 13.0), (12.0, 13.0)]], 'team', bevel=0.04, mirror=True)
    b.box((10.2, 5.0, -2.0), (11.0, 10.0, 12.0), 'dark', bevel=0.08, mirror=True)        # pod pylon
    b.cyl((13.5, 8.0, -4.0), (13.5, 8.0, -4.5), 2.7, 12, 'black', mirror=True)
    # ------------------------------------------------------------------ stern: dark tapered tail, fins
    b.hull(sym([(10.2, 2.2, HZ0), (8.6, WTOP, HZ0), (0.0, 17.6, HZ0), (3.2, 6.4, -35.2), (2.4, 11.6, -35.2), (4.4, 2.6, -33.0)]), 'paint2', bevel=0.2)
    b.cyl((0, 9.0, -35.0), (0, 9.0, -35.4), 2.3, 10, 'black')
    b.hull([(x, y, z) for x, y, z in [(0.3, 17.66, -28.0), (8.0, 15.1, -28.0), (2.4, 11.8, -34.6), (0.3, 12.4, -34.6),
                                      (0.3, 17.9, -28.0), (8.0, 15.34, -28.0), (2.4, 12.04, -34.6), (0.3, 12.64, -34.6)]], 'team', bevel=0.03, mirror=True)
    b.hull([(x, y, z) for y in (6.6, 8.2) for x, z in [(9.4, -14.6), (10.0, -26.0), (17.6, -35.2), (17.6, -31.6)]], 'dark', bevel=0.12, mirror=True)
    # ------------------------------------------------------------------ roof halves: the builder's striped block
    d = k.piece('door1')
    for z0, z1 in ((HZ0 + 0.05, -13.8), (-13.8, 0.0), (0.0, HZ1 - 0.05)):      # segments: see the walls
        d.hull([(x, y + dy, z) for z in (z0, z1) for dy in (0.0, -0.45) for x, y in ((-6.29, 15.19), (-0.02, 17.8))], 'hazard', bevel=0.0)
    k.clone('door2', 'door1', mirror_x=True)
    # ------------------------------------------------------------------ lift plate (rises to y 16.7, then the top of the sub)
    p = k.piece('plate')
    for z0, z1 in ((HZ0 + 0.15, -13.8), (-13.8, 0.0), (0.0, HZ1 - 0.15)):
        p.box((-6.2, 2.1, z0), (6.2, 2.61, z1), 'hazard', bevel=0.0)
    # post and nano gun (gun origin x = 0.12: no mirrors)
    q = k.piece('post'); Q = q.at
    q.cyl(Q(0, -0.02, 0), Q(0, 9.7, 0), 1.7, 10, 'dark', bevel=0.06)
    g = k.piece('gun'); G = g.at
    g.hull([G(x, y, z) for x, y, z in [(-3.6, -0.5, -8.0), (3.6, -0.5, -8.0), (-3.6, -0.5, 6.0), (3.6, -0.5, 6.0),
                                       (-2.8, 3.2, -6.8), (2.8, 3.2, -6.8), (-2.2, 2.6, 5.0), (2.2, 2.6, 5.0)]], 'hazard', bevel=0.12)
    g.cyl(G(0, 0.9, 5.8), G(0, 0.5, 16.2), 1.3, 10, 'steel', r2=0.8, bevel=0.05)
    g.cyl(G(0, 0.5, 16.2), G(0, 0.5, 17.1), 0.8, 8, 'lightc')
