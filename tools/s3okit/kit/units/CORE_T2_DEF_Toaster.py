"""Toaster (CORE_T2_DEF_Toaster) - Core pop-up heavy cannon (TA:CC). A flush square frame round a pit closed by two
hazard-striped lids; on activation the lids swing down into the pit walls and an A-frame (pillartops) rises 26.5 elmo
carrying a boxy gun house with a long light steel cannon that runs out 31 elmo.
Identity from above (open): a dark square frame with team corners, a dark A-frame and gun house with a team roof and
a long light barrel well past the frame; closed = the frame round a yellow-black double lid (the pop-up hatch).
Pieces (COB): ground, frame, door1/2 (turn z, move y), hole, pillartops (move y, turn y), turretssides, turret (turn x),
barrel2/barrel3/barrel1/turretback (move z), flare (emit, empty). The model's default pose is OPEN; the preview
shows it with the lids turned down and sunk as activatescr leaves them.
Two wrecks: CORE_T2_DEF_Toaster_dead (level 1) and CORE_T2_DEF_Toaster_dead2 (level 2).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=51, drop=['barrel1'], pose={'turret': (14, 0, 0)}),
    preview_pose={'door1': {'move': (0, -19.25, 0), 'rot': (0, 0, 88.6)}, 'door2': {'move': (0, -19.25, 0), 'rot': (0, 0, -89.3)},
                  'pillartops': (0, -20, 0), 'turret': (-6, 0, 0)},
)

RO, RI, H = 22.8, 16.4, 3.5


def build(k):
    # ------------------------------------------------------------------ frame: square ring round the pit
    f = k.piece('frame')
    for s in (-1, 1):
        f.hull([(s * x, y, z) for x, y, zs in ((RO, 0.0, RO), (RI, 0.0, RO), (RO - 1.6, H, RO - 1.6), (RI, H, RO - 1.6))
                for z in (-zs, zs)], 'paint', bevel=0.25)
        f.hull([(x, y, s * z) for x, y, z in ((-RI, 0.0, RO), (RI, 0.0, RO), (-RI, 0.0, RI), (RI, 0.0, RI),
                                             (-RI, H, RO - 1.6), (RI, H, RO - 1.6), (-RI, H, RI), (RI, H, RI))], 'paint', bevel=0.25)
    for s in (-1, 1):
        for t in (-1, 1):   # team corner L-blocks (two non-overlapping boxes)
            f.box((min(s * (RI + 0.4), s * (RO - 2.0)), H - 0.1, min(t * 8.0, t * (RO - 2.0))),
                  (max(s * (RI + 0.4), s * (RO - 2.0)), H + 0.3, max(t * 8.0, t * (RO - 2.0))), 'team', bevel=0.04)
            f.box((min(s * 8.0, s * (RI + 0.4)), H - 0.1, min(t * (RI + 0.4), t * (RO - 2.0))),
                  (max(s * 8.0, s * (RI + 0.4)), H + 0.3, max(t * (RI + 0.4), t * (RO - 2.0))), 'team', bevel=0.04)
    f.box((-1.0, 1.0, RO - 0.6), (1.0, 2.2, RO + 0.05), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ hole: pit floor
    k.piece('hole').box((-RI, 1.6, -RI), (RI, 2.4, RI), 'black', bevel=0.0)

    # ------------------------------------------------------------------ doors: pit lids (door1 hinge x -15.34, y 2.81)
    d = k.piece('door1'); D = d.at
    d.box(D(0.0, -0.4, -14.8), D(15.2, 0.8, 14.8), 'dark', bevel=0.12)
    d.box(D(0.8, 0.75, -14.0), D(14.4, 0.98, 14.0), 'hazard', bevel=0.03)
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ pillartops: the rising A-frame (origin 0, 3.62, 0)
    p = k.piece('pillartops'); P = p.at
    for sx in (-1, 1):
        p.hull([P(sx * x, y, z) for x, y, z in
                [(10.0, -1.4, -11.0), (14.6, -1.4, -11.0), (10.0, -1.4, 11.0), (14.6, -1.4, 11.0),
                 (9.4, 13.0, -5.0), (12.6, 13.0, -5.0), (9.4, 13.0, 5.0), (12.6, 13.0, 5.0)]], 'paint', bevel=0.3)
        p.hull([P(sx * x, y, z) for x, y, z in
                [(14.62, 2.0, -6.0), (14.8, 2.0, -6.0), (14.62, 2.0, 6.0), (14.8, 2.0, 6.0),
                 (12.7, 11.0, -3.6), (12.9, 11.0, -3.6), (12.7, 11.0, 3.6), (12.9, 11.0, 3.6)]], 'dark', bevel=0.0)
    p.box(P(-10.0, 0.4, -3.0), P(10.0, 4.0, 3.0), 'dark', bevel=0.15)          # crossbeam

    # ------------------------------------------------------------------ turretssides: trunnion plates (origin 0, 0, 0)
    ts = k.piece('turretssides')
    ts.box((8.8, 13.6, -3.6), (10.0, 20.4, 3.6), 'paint2', bevel=0.15, mirror=True)
    ts.cyl((7.2, 17.0, 0.0), (10.2, 17.0, 0.0), 2.6, 10, 'steel', bevel=0.05, mirror=True)

    # ------------------------------------------------------------------ turret: gun house (origin 0, 13.77, 0)
    t = k.piece('turret'); T = t.at
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.2, -3.4, -9.6), (7.2, -3.4, 9.0), (7.2, 7.0, -9.6), (7.2, 6.0, 9.0), (5.6, 9.0, -7.6), (5.6, 8.4, 6.0)]],
           'paint', bevel=0.35)
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 8.95, -6.6), (4.6, 8.45, 5.0), (4.6, 9.2, -6.6), (4.6, 8.7, 5.0)]], 'team', bevel=0.0)
    t.box(T(-0.8, 4.0, 9.0), T(0.8, 5.2, 9.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ barrel2: mantlet (origin 0, 18.51, 11.01)
    m = k.piece('barrel2'); M = m.at
    m.hull([M(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, -1.8, 0.0), (5.0, 2.6, 0.0), (4.0, -1.4, 6.8), (4.0, 2.2, 6.8)]], 'dark', bevel=0.2)

    # ------------------------------------------------------------------ barrel3: gun tube (origin 0, 16.67, -11.55)
    g = k.piece('barrel3'); G = g.at
    g.cyl(G(0, 1.4, 0.4), G(0, 1.4, 30.0), 3.0, 12, 'steel', rot=math.pi / 12, bevel=0.06)
    g.cyl(G(0, 1.4, 24.6), G(0, 1.4, 26.4), 3.5, 12, 'dark', rot=math.pi / 12)
    # turretback: counterweight (origin 0, 16.63, -11.09)
    tb = k.piece('turretback'); B = tb.at
    tb.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(7.0, 0.0, -5.4), (7.0, 0.0, 0.0), (6.0, 6.2, -4.6), (6.0, 6.2, 0.0)]], 'paint2', bevel=0.25)
    tb.box(B(-4.0, 6.15, -3.8), B(4.0, 6.4, -0.6), 'team', bevel=0.03)

    # ------------------------------------------------------------------ barrel1: the long cannon (origin 0, 17.52, 18.22)
    br = k.piece('barrel1'); R = br.at
    br.cyl(R(0, 0.4, -1.0), R(0, 0.4, 22.0), 2.5, 10, 'steel', rot=math.pi / 10)
    br.cyl(R(0, 0.4, 21.4), R(0, 0.4, 25.6), 3.3, 8, 'steel', r2=3.0, rot=math.pi / 8, bevel=0.06)
    br.cyl(R(0, 0.4, 22.8), R(0, 0.4, 23.8), 3.42, 8, 'dark', rot=math.pi / 8)
    br.cyl(R(0, 0.4, 25.58), R(0, 0.4, 25.7), 1.4, 10, 'black')
