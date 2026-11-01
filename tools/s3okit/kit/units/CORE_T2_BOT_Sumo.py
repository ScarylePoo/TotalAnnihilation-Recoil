"""Sumo (CORE_T2_BOT_Sumo) - Core T2 heavily armoured assault unit. By the user's decision it rolls on TRACKS instead
of TA's four feet: the feet (FLFoot..RRFoot, feetparent) are dropped (skeleton=None, skeleton_opts drop), TA's two big
side blocks (rightchunk/leftchunk) become armoured track sponsons, and a tracked lower hull is added as four
animation frames (tracks1..4, cycled by the script; link pattern advanced per frame via tread..tread4). Between the
sponsons sits the body with shoulder knobs, a sloped turret with a face guard and twin short heavy cannons.
Script ported to scripts/CORE_T2_BOT_Sumo.lua (aim/fire/death from the COB, no walk).
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Sumo): the bulkiest Core T2 silhouette - two long dark-warm sponsons with team plates on
top either side of a narrow body, an ochre-faced turret and two stubby light steel barrels; distinct from The Can's
single square slab by its three-block layout."""
import math

UNIT = dict(
    skeleton_opts=dict(drop=['FLFoot', 'FRFoot', 'RLFoot', 'RRFoot', 'feetparent'],
                       add={'tracks1': ('hips', (0, 0, 0)), 'tracks2': ('hips', (0, 0, 0)),
                            'tracks3': ('hips', (0, 0, 0)), 'tracks4': ('hips', (0, 0, 0))}),
    res=1024,
    wreck=dict(seed=22, drop=['Lgun'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, -25, 0)}),
    preview_pose={'turret': (0, -20, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)


def tracks(k, name, mat):
    t = k.piece(name)                                   # origin (0, 0, 0)
    belt = [(-15.6, 0.0), (11.6, 0.0), (14.8, 3.2), (14.0, 7.4), (-15.4, 7.4), (-17.2, 3.4)]
    t.prism(9.0, 16.2, belt, mat, bevel=0.18, mirror=True)


def sponson(b, sx):
    """armoured track sponson on a chunk piece (origin (+-8.07, 18.27, -4.25)); sx = -1 right, +1 left."""
    A = lambda x, y, z: b.at(sx * x, y, z)
    b.hull([A(x, y, z) for x, y, z in
            [(0.6, -10.2, -11.4), (0.6, -10.2, 12.6), (8.6, -10.2, -11.4), (8.6, -10.2, 12.6),
             (0.6, 1.6, -10.4), (0.6, 1.6, 10.4), (7.6, 1.6, -10.4), (7.6, 1.6, 10.4),
             (4.4, -6.0, 15.4), (4.4, -2.0, 14.0)]], 'paint', bevel=0.28)
    b.hull([A(x, y, z) for x, y, z in                                                    # team plate on top
            [(1.6, 1.62, -8.6), (1.6, 1.62, 8.6), (6.6, 1.62, -8.6), (6.6, 1.62, 8.6),
             (1.6, 1.78, -8.55), (1.6, 1.78, 8.55), (6.6, 1.78, -8.55), (6.6, 1.78, 8.55)]], 'team', bevel=0.03)
    b.hull([A(x, y, z) for x, y, z in                                                    # dark side skirt band
            [(8.62, -9.6, -10.8), (8.62, -9.6, 12.0), (8.62, -6.4, -10.8), (8.62, -6.4, 12.0),
             (8.8, -9.4, -10.6), (8.8, -9.4, 11.8), (8.8, -6.6, -10.6), (8.8, -6.6, 11.8)]], 'paint2', bevel=0.04)
    b.hull([A(x, y, z) for x, y, z in                                                    # ochre nose plate
            [(1.2, -5.8, 15.2), (7.8, -5.8, 13.0), (1.2, -2.2, 13.8), (7.4, -2.2, 12.0),
             (1.2, -5.8, 15.4), (7.8, -5.8, 13.2), (1.2, -2.2, 14.0), (7.4, -2.2, 12.2)]], 'hazard', bevel=0.03)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)

    # ------------------------------------------------------------------ hull floor between the tracks (hips, origin 0)
    hp = k.piece('hips')
    hp.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(9.0, 2.4, -14.6), (9.0, 2.4, 12.0), (9.0, 8.2, -15.0), (9.0, 8.2, 13.6), (6.6, 1.4, -12.4), (6.6, 1.4, 10.6)]],
            'paint2', bevel=0.2)
    for sx in (-1, 1):
        for z in (-11.0, -5.0, 1.0, 7.0):
            hp.cyl((sx * 9.0, 3.8, z), (sx * 8.6, 3.8, z), 1.7, 12, 'dark', mirror=False)

    # ------------------------------------------------------------------ body (0, 18.27, -3.82)
    b = k.piece('body'); B = b.at
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, -8.6, -7.0), (7.6, -8.6, 10.0), (7.8, 4.2, -7.0), (7.8, 4.2, 8.6), (5.6, 5.4, -6.2), (5.6, 5.4, 6.4),
             (4.6, -4.0, 11.6)]], 'paint2', bevel=0.26)
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                             # front armour plate
            [(4.4, -6.6, 10.8), (5.0, 0.6, 9.4), (4.4, -6.6, 11.1), (5.0, 0.6, 9.7)]], 'paint', bevel=0.06)
    for y in (-4.6, -3.2, -1.8):
        b.box(B(-3.2, y, 10.0), B(3.2, y + 0.6, 10.45), 'black', bevel=0.0)
    k_ = k.piece('knobs'); KN = k_.at                                                    # shoulder knobs
    for sx in (-1, 1):
        k_.cyl(KN(sx * 7.4, -1.2, 0), KN(sx * 8.9, -1.2, 0), 2.2, 10, 'dark', bevel=0.1)   # hinge knobs in the gap
        k_.cyl(KN(sx * 8.8, -1.2, 0), KN(sx * 9.1, -1.2, 0), 1.4, 10, 'steel')

    # ------------------------------------------------------------------ sponsons (rightchunk / leftchunk)
    sponson(k.piece('rightchunk'), -1)
    sponson(k.piece('leftchunk'), 1)

    # ------------------------------------------------------------------ turret (0.21, 23.8, -4.67)
    t = k.piece('turret'); T = t.at
    t.hull([T(x, y, z) for x, y, z in
            [(-5.8, 0.0, -7.6), (5.4, 0.0, -7.6), (-5.8, 0.0, 4.6), (5.4, 0.0, 4.6), (-4.6, 5.2, -6.8), (4.2, 5.2, -6.8),
             (-4.0, 5.6, 1.0), (3.6, 5.6, 1.0), (-3.0, 2.4, 6.6), (2.6, 2.4, 6.6)]], 'paint', bevel=0.24)
    t.hull([T(x, y, z) for x, y, z in                                                     # team roof plate
            [(-3.4, 5.32, -5.6), (3.0, 5.32, -5.6), (-3.0, 5.62, 0.2), (2.6, 5.62, 0.2),
             (-3.4, 5.48, -5.55), (3.0, 5.48, -5.55), (-3.0, 5.78, 0.15), (2.6, 5.78, 0.15)]], 'team', bevel=0.03)
    t.cyl(T(-3.6, 5.2, -6.0), T(-3.6, 9.4, -6.0), 0.15, 6, 'steel', r2=0.07)            # antenna
    t.cyl(T(-3.6, 9.4, -6.0), T(-3.6, 9.65, -6.0), 0.22, 6, 'lightr')
    f = k.piece('faceguard'); F = f.at                  # (0, 25.5, -5.1)
    f.hull([F(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -1.6, 6.0), (5.0, 2.2, 5.0), (5.4, -1.6, 7.0), (5.0, 2.2, 6.0), (2.0, -1.6, 7.6), (2.0, 2.2, 6.6)]],
           'hazard', bevel=0.1)

    # ------------------------------------------------------------------ twin cannons
    g = k.piece('Lgun'); G = g.at                       # (1.27, 25.5, 2.55)
    g.hull([G(x, y, z) for x in (-0.9, 2.3) for y in (-1.0, 1.6) for z in (-0.6, 4.6)], 'dark', bevel=0.1)
    b2 = k.piece('Lbarrel'); BB = b2.at                 # (1.27, 25.5, 6.8): muzzle (lflare) at z 5.1
    b2.cyl(BB(0, 0, -0.4), BB(0, 0, 4.6), 0.9, 10, 'steel')
    b2.cyl(BB(0, 0, 4.2), BB(0, 0, 5.2), 1.15, 8, 'dark', rot=math.pi / 8, bevel=0.04)
    b2.cyl(BB(0, 0, 5.15), BB(0, 0, 5.3), 0.55, 8, 'black')
    k.clone('Rgun', 'Lgun', mirror_x=True)
    k.clone('Rbarrel', 'Lbarrel', mirror_x=True)
