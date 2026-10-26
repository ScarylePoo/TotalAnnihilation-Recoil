"""Informer (CORE_T2_VEH_Informer) - Core mobile radar. Articulated two-part carrier: a `front` section on one wide
roller drum (bigwheel, spin x) and a `rear` section on a pair of short tracks (tracks1..4 frame-cycled, wheels1..4 hub
discs); both turn y about the coupling at the origin when steering, so their geometry stays clear of z = 0.
On the front sits the radar: turret (spins y when active) -> arm_1 (raises 90 deg) -> arm_2 (+30) -> arm_3 (-40) ->
dish, a folding radar of a centre plate and two hinged wing panels per side (panel_a1/b1, panel_a2/b2 turn z +-30 to
flatten when deployed). Piece layout is the third-party S3O's (the COB drives it).
The radar is the identity, so its panels are enlarged well past the S3O's (span ~16 elmo, depth 10): stowed it lies
over the front section as a wide light steel shell with a team centre; deployed it stands up as a big light panel.
Value groups from above: light steel radar panels + team centre, dark warm carrier, paint2 rear deck, black
roller/tracks, ochre hazard on the coupling.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=79, drop=['dish'], remove=['tracks2', 'tracks3', 'tracks4']),
    preview_pose={'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)
DZ = 5.2          # radar panel half depth (z)


def build(k):
    # ------------------------------------------------------------------ rear section (origin 0, 6, 0)
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        t = k.piece(f'tracks{i}')
        belt = [(-13.8, 0.0), (-2.4, 0.0), (-0.8, 1.6), (-1.6, 3.4), (-14.0, 3.4), (-15.4, 1.6)]
        t.prism(4.6, 8.2, belt, mat, bevel=0.14, mirror=True)
    for i, r in ((1, 1.6), (2, 1.3)):
        w = k.piece(f'wheels{i}'); W = w.at
        w.cyl(W(8.15, 0, 0), W(8.45, 0, 0), r, 10, 'dark', bevel=0.04, mirror=True)
        w.cyl(W(8.45, 0, 0), W(8.6, 0, 0), r * 0.42, 8, 'steel', mirror=True)
    k.clone('wheels4', 'wheels1')
    k.clone('wheels3', 'wheels2')
    r = k.piece('rear')
    r.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.0, 3.4, -15.0), (9.0, 3.4, -2.6), (8.4, 7.2, -14.2), (8.0, 7.2, -4.0), (4.2, 5.6, -1.0), (4.6, 3.4, -0.8)]],
           'paint', bevel=0.18)
    r.box((-6.4, 7.2, -13.4), (6.4, 7.5, -5.0), 'paint2', bevel=0.05)
    r.box((-5.0, 7.5, -12.6), (5.0, 8.6, -9.4), 'dark', bevel=0.08)            # generator block
    for z in (-12.2, -11.4, -10.6, -9.8):
        r.box((-4.6, 8.6, z), (4.6, 8.72, z + 0.4), 'black', bevel=0.0)
    r.box((5.6, 7.5, -8.4), (7.6, 7.72, -5.4), 'team', bevel=0.03, mirror=True)
    r.cyl((0, 3.6, -1.6), (0, 6.2, -1.6), 2.0, 12, 'hazard', bevel=0.06)       # coupling knuckle
    r.box((-6.0, 4.0, -15.5), (6.0, 6.4, -14.9), 'dark', bevel=0.05)
    r.box((4.4, 5.0, -15.6), (5.6, 5.8, -15.45), 'lightr', bevel=0.0, mirror=True)
    r.cyl((-7.2, 7.2, -13.6), (-7.2, 7.8, -13.6), 0.3, 8, 'dark')
    r.cyl((-7.2, 7.8, -13.6), (-7.2, 12.6, -13.6), 0.08, 6, 'steel', r2=0.04)
    r.cyl((-7.2, 12.6, -13.6), (-7.2, 12.8, -13.6), 0.13, 6, 'lightr')

    # ------------------------------------------------------------------ front section (origin 0, 5, 0)
    bw = k.piece('bigwheel'); BW = bw.at
    bw.cyl(BW(-7.2, 0, 0), BW(7.2, 0, 0), 3.0, 14, 'tread', rot=math.pi / 14, bevel=0.14)
    bw.cyl(BW(-7.6, 0, 0), BW(-7.2, 0, 0), 1.8, 10, 'dark', bevel=0.04)
    bw.cyl(BW(7.2, 0, 0), BW(7.6, 0, 0), 1.8, 10, 'dark', bevel=0.04)
    f = k.piece('front')
    # fork frame holding the drum + nose, low deck under the stowed radar
    f.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 3.4, 5.6), (9.6, 3.4, 15.0), (9.6, 6.6, 6.4), (9.6, 6.6, 13.6), (8.8, 7.0, 8.0), (8.8, 7.0, 12.4)]],
           'paint', bevel=0.16)
    f.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 3.0, 1.2), (4.6, 3.0, 20.0), (4.0, 6.6, 1.2), (4.0, 6.6, 16.8), (2.4, 5.0, 20.4)]], 'paint', bevel=0.16)
    f.cyl((7.6, 3.0, 10.25), (8.2, 3.0, 10.25), 2.4, 12, 'dark', bevel=0.05, mirror=True)
    # ochre hazard nose (front bumper) and lights
    f.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 5.2, 19.6), (2.0, 4.6, 20.8), (3.4, 6.5, 17.6), (2.0, 5.8, 20.0)]], 'hazard', bevel=0.04)
    f.box((5.2, 4.8, 14.6), (8.6, 6.0, 15.4), 'dark', bevel=0.05, mirror=True)
    f.box((5.4, 5.0, 15.35), (8.4, 5.8, 15.45), 'lightw', bevel=0.0, mirror=True)
    f.box((7.0, 6.95, 8.4), (9.2, 7.17, 12.0), 'team', bevel=0.03, mirror=True)
    f.cyl((0, 6.4, 0), (0, 7.1, 0), 3.0, 14, 'dark', bevel=0.05)               # turret ring over the coupling

    # ---------------------------------------------------------------- radar mast
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.1, 0), A(0, 1.8, 0), 2.6, 10, 'paint2', r2=2.0, rot=math.pi / 10, bevel=0.1)
    t.box(A(-1.6, 1.6, -1.2), A(1.6, 2.6, 1.2), 'dark', bevel=0.06)
    a1 = k.piece('arm_1'); B = a1.at
    a1.cyl(B(-1.4, 0, 0), B(1.4, 0, 0), 0.9, 10, 'steel')
    a1.box(B(-0.9, -0.6, -0.4), B(0.9, 0.6, 2.4), 'dark', bevel=0.08)
    a2 = k.piece('arm_2'); C = a2.at
    a2.cyl(C(-1.0, 0, 0), C(1.0, 0, 0), 0.7, 10, 'steel')
    a2.hull([C(x, y, z) for x in (-0.6, 0.6) for y, z in [(-0.5, -0.3), (0.5, -0.5), (2.6, 2.0), (1.9, 2.7)]], 'paint2', bevel=0.06)
    a3 = k.piece('arm_3'); D = a3.at
    a3.cyl(D(-0.9, 0, 0), D(0.9, 0, 0), 0.6, 10, 'steel')
    a3.box(D(-0.6, -0.4, -0.3), D(0.6, 0.4, 2.4), 'dark', bevel=0.06)

    # ---------------------------------------------------------------- dish: centre plate (origin 0, 11, 6.7)
    d = k.piece('dish'); E = d.at
    d.box(E(-0.9, -0.2, -1.4), E(0.9, 0.5, 1.4), 'dark', bevel=0.06)          # mount
    d.hull([E(x, y, z) for x in (-2.15, 2.15) for y in (-1.45, -0.85) for z in (-DZ, DZ)], 'steel', bevel=0.1)
    d.box(E(-1.7, -0.85, -DZ + 0.6), E(1.7, -0.68, DZ - 0.6), 'team', bevel=0.03)
    d.cyl(E(0, -1.45, 0), E(0, -2.6, 0), 0.5, 8, 'dark')                       # feed (faces the concave side)
    d.cyl(E(0, -2.6, 0), E(0, -2.75, 0), 0.4, 8, 'lightr')

    # ---------------------------------------------------------------- wing panels (build side 1, mirror for 2)
    pa = k.piece('panel_a1'); F = pa.at
    # inner wing: from its hinge (at the centre plate edge) out to panel_b1's hinge (-1.51, -1.10)
    pa.hull([F(x, y + dy, z) for x, y in ((0.0, 0.0), (-1.51, -1.10)) for dy in (-0.3, 0.3) for z in (-DZ, DZ)], 'steel', bevel=0.08)
    pa.box(F(-1.1, -0.9, -DZ + 0.8), F(-0.4, -0.2, DZ - 0.8), 'dark', bevel=0.03)
    pb = k.piece('panel_b1'); G = pb.at
    # outer wing: long, slightly drooping; team tip strip
    pb.hull([G(x, y + dy, z) for x, y in ((0.0, 0.0), (-4.6, -1.3)) for dy in (-0.25, 0.25) for z in (-DZ, DZ)], 'steel', bevel=0.08)
    pb.hull([G(x, y + dy, z) for x, y in ((-3.6, -1.02), (-4.5, -1.27)) for dy in (0.24, 0.36) for z in (-DZ + 0.4, DZ - 0.4)],
            'team', bevel=0.02)
    pb.cyl(G(0, 0, -DZ), G(0, 0, DZ), 0.35, 8, 'dark')
    k.clone('panel_a2', 'panel_a1', mirror_x=True)
    k.clone('panel_b2', 'panel_b1', mirror_x=True)
