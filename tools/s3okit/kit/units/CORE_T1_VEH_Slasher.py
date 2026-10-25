"""Slasher (CORE_T1_VEH_Slasher) - Core mobile missile launcher. Tracked truck: armoured cab over a narrow front track
pair, wide flat rear bed over a wider rear track pair. On the bed a traversing cradle (turret, turn y) with two tall
uprights; the `arms` carriage slides 10 elmo up the uprights when aiming (move y) and carries the twin-tube missile
pod (`gun`, elevates on turn x; firepoint1/2 at the tube mouths, exhaust1/2 at the tube backs).
Piece layout is the third-party remodel's (the COB drives it); tracks1..4 frame-cycled with tread..tread4, wheels1..8
hub discs on the outer track faces (spin x).
Value groups from above: dark warm cab/bed armour, darker paint2 cradle/uprights, black tracks, light steel missile
tubes (Core: light weapons on dark armour) with team bands, team plates on the cab roof and bed rails, ochre hazard.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=10, drop=['gun'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, 30, 0)}),
    preview_pose={'turret': (0, -15, 0), 'gun': (-15, 0, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)

F_XI, F_XO = 7.5, 12.5      # front track pair
R_XI, R_XO = 12.0, 16.5     # rear track pair


def tracks(k, name, mat):
    t = k.piece(name)
    t.prism(F_XI, F_XO, [(7.6, 0.0), (19.6, 0.0), (21.7, 2.0), (20.8, 4.0), (7.4, 4.0), (6.6, 2.0)], mat, bevel=0.12, mirror=True)
    t.prism(R_XI, R_XO, [(-23.0, 0.0), (-6.0, 0.0), (-4.3, 2.0), (-5.0, 4.0), (-23.6, 4.0), (-24.7, 2.0)], mat, bevel=0.12, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    # wheels: 1-4 front pair (1, 4 sprockets), 5-8 rear pair
    for name, xo, r in (('wheels1', F_XO, 2.0), ('wheels2', F_XO, 1.15), ('wheels5', R_XO, 2.0)):
        w = k.piece(name); W = w.at
        w.cyl(W(xo - 0.05, 0, 0), W(xo + 0.35, 0, 0), r, 12, 'dark', bevel=0.04, mirror=True)
        w.cyl(W(xo + 0.35, 0, 0), W(xo + 0.55, 0, 0), max(0.5, r * 0.42), 8, 'steel', mirror=True)
    k.clone('wheels4', 'wheels1')
    k.clone('wheels3', 'wheels2')
    for i in (6, 7, 8):
        k.clone(f'wheels{i}', 'wheels5')

    # ------------------------------------------------------------------ body
    b = k.piece('body')
    # chassis beam (crosses x = 0)
    b.prism(-7.6, 7.6, [(-25.6, 3.4), (23.4, 3.4), (25.4, 5.4), (24.8, 7.0), (-25.8, 7.0), (-26.6, 5.2)], 'paint2', bevel=0.15)
    # rear bed: wide flat deck over the rear tracks
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(17.0, 4.6, -25.4), (17.0, 4.6, -3.4), (17.0, 7.0, -25.8), (17.0, 7.0, -3.0),
             (16.4, 7.4, -25.2), (16.4, 7.4, -3.6)]], 'paint', bevel=0.16)
    # bed rails with team tops (outer edges)
    b.box((14.0, 7.4, -24.0), (16.4, 8.4, -5.0), 'paint2', bevel=0.08, mirror=True)
    b.box((11.4, 7.4, -23.6), (14.0, 7.56, -5.4), 'team', bevel=0.03, mirror=True)      # side pods inboard of the rails
    # rear hazard bumper + lights
    b.box((-12.0, 4.6, -26.4), (12.0, 6.6, -25.6), 'dark', bevel=0.05)
    b.box((12.4, 5.2, -26.3), (14.4, 6.2, -25.8), 'lightr', bevel=0.0, mirror=True)
    # blast deflector plate behind the cradle (missile backblast)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.0, 7.4, -24.8), (9.0, 7.4, -22.4), (8.4, 9.6, -24.8)]], 'dark', bevel=0.1)
    # front mudguards over the front tracks
    b.hull([(7.0, 4.4, 6.4), (13.2, 4.4, 6.4), (7.0, 4.4, 22.4), (13.2, 4.4, 22.4),
            (7.0, 6.4, 7.4), (13.2, 6.4, 7.4), (7.0, 6.4, 20.4), (13.2, 6.4, 20.4)], 'paint', bevel=0.12, mirror=True)
    # cab: angular armoured block, sloped windscreen, spiked nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.2, 6.8, 2.4), (7.2, 6.8, 23.4), (5.6, 6.4, 25.5),
             (7.0, 16.4, 3.0), (6.4, 17.6, 8.6), (6.2, 13.6, 16.4), (5.8, 11.6, 23.0)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.2, 14.1, 15.6), (4.8, 17.0, 9.6), (5.2, 14.22, 15.72), (4.8, 17.12, 9.72)]], 'glass', bevel=0.03)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.0, 16.45, 2.8), (5.6, 17.6, 8.2), (6.0, 16.6, 2.8), (5.6, 17.75, 8.2)]], 'team', bevel=0.03)
    # headlights + grille
    b.box((-4.4, 7.4, 24.6), (4.4, 10.4, 25.3), 'dark', bevel=0.06)
    for y in (7.8, 8.7, 9.6):
        b.box((-4.0, y, 25.25), (4.0, y + 0.4, 25.45), 'black', bevel=0.0)
    b.box((5.0, 8.2, 24.4), (6.6, 9.4, 25.1), 'dark', bevel=0.05, mirror=True)
    b.box((5.15, 8.35, 25.08), (6.45, 9.25, 25.18), 'lightw', bevel=0.0, mirror=True)
    # cab exhaust + antenna
    b.cyl((7.4, 8.0, 2.8), (7.4, 18.4, 2.8), 0.6, 10, 'dark', mirror=True)
    b.cyl((7.4, 18.4, 2.8), (7.4, 18.55, 2.8), 0.42, 10, 'black', mirror=True)
    b.cyl((-5.0, 17.4, 4.0), (-5.0, 18.0, 4.0), 0.34, 8, 'dark')
    b.cyl((-5.0, 18.0, 4.0), (-5.0, 23.0, 4.0), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-5.0, 23.0, 4.0), (-5.0, 23.2, 4.0), 0.14, 6, 'lightr')

    # ---------------------------------------------------------------- turret (cradle on the bed; origin 0, 0, -10)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 7.3, 0), A(0, 8.0, 0), 8.0, 20, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.6, 8.0, -7.4), (11.1, 8.0, 6.4), (10.2, 9.4, -6.8), (10.4, 9.4, 5.8)]], 'paint2', bevel=0.14)
    # uprights (guide rails for the arms carriage), x 6.2 .. 8.6
    t.hull([A(x, y, z) for x, y, z in
            [(6.2, 9.4, -5.0), (8.6, 9.4, -5.0), (6.2, 9.4, 5.0), (8.6, 9.4, 5.0),
             (6.2, 20.0, -2.6), (8.0, 20.0, -2.6), (6.2, 20.0, 2.6), (8.0, 20.0, 2.6)]], 'paint', bevel=0.14, mirror=True)
    t.box(A(8.6, 9.4, -0.8), A(9.6, 16.0, 0.8), 'dark', bevel=0.06, mirror=True)      # hydraulic housing
    t.box(A(-6.2, 9.4, -6.6), A(6.2, 10.4, -4.6), 'dark', bevel=0.06)                  # rear tie bar

    # ---------------------------------------------------------------- arms (carriage; slides up 10)
    a = k.piece('arms'); R = a.at
    a.hull([R(x, y, z) for x, y, z in
            [(4.7, 9.6, -3.4), (6.1, 9.6, -3.4), (4.7, 9.6, 3.4), (6.1, 9.6, 3.4),
             (4.7, 17.4, -2.4), (6.1, 17.4, -2.4), (4.7, 17.4, 2.4), (6.1, 17.4, 2.4)]], 'dark', bevel=0.1, mirror=True)
    a.cyl(R(4.5, 13.5, 0), R(6.3, 13.5, 0), 1.6, 12, 'steel', bevel=0.04, mirror=True)

    # ---------------------------------------------------------------- gun (twin missile pod; origin 0, 13.5, -10)
    g = k.piece('gun'); G = g.at
    for sy in (1, -1):
        y = 3.66 * sy
        g.cyl(G(0, y, -13.6), G(0, y, 13.4), 3.0, 12, 'steel', rot=math.pi / 12, bevel=0.06)
        g.cyl(G(0, y, 13.4), G(0, y, 14.6), 3.0, 12, 'steel', r2=2.5, rot=math.pi / 12)
        g.cyl(G(0, y, 14.58), G(0, y, 14.7), 1.9, 12, 'black')
        g.cyl(G(0, y, -13.9), G(0, y, -13.6), 2.2, 12, 'black')
        for z in (-9.0, 6.0):
            g.cyl(G(0, y, z), G(0, y, z + 1.4), 3.15, 12, 'dark', rot=math.pi / 12, bevel=0.04)
    # team saddle on top of the upper tube, hazard warhead ring on the lower
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 6.55, -6.0), (1.6, 6.55, 4.0), (1.4, 6.82, -6.0), (1.4, 6.82, 4.0)]], 'team', bevel=0.03)
    g.box(G(-1.9, 6.5, -6.4), G(1.9, 6.6, 4.4), 'dark', bevel=0.0)
    g.cyl(G(0, -3.66, 11.6), G(0, -3.66, 12.8), 3.1, 12, 'hazard', rot=math.pi / 12)
    # spine between the tubes and trunnion block
    g.box(G(-1.8, -1.0, -11.0), G(1.8, 1.0, 11.0), 'paint2', bevel=0.08)
    g.box(G(-4.5, -1.4, -1.6), G(4.5, 1.4, 1.6), 'dark', bevel=0.08)
