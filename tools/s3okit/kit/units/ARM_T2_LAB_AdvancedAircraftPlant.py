"""Advanced Aircraft Plant (ARM_T2_LAB_AdvancedAircraftPlant) - Arm T2 air factory. The T1 plant's airfield deck
(light deck, dark lane, team shoulders, big round pad, front beacons: `lights`) with a symmetric back row: a tall light
control tower in the middle (cyan cab, team cap, spinning radar dish) whose lower shaft is wrapped by two hazard-roofed
nano boxes (nanobox1/2), each flanked by a team-roofed wedge hangar (building1/2). On activation boxes and hangars
slide ~19.4 apart (move x) and the nano heads (nano1/nano2) slide forward into niches in the boxes' fronts.
Arm lab family (T2 = taller, more parts): light chamfered blocks, team roofs, dark lane, light round pad, cyan lights.
Identity from above: a huge light deck with a disc, a tall tower dead centre at the back between two pairs of blocks
(the T1 air plant has its tower on the left beside a hangar and a silo).
Pieces (COB): base, building1/2 (move x), nanobox1/2 (move x), nano1/2 (move z), beam1/2 (empty nano emit points),
radar (spin y), lights (beacons), pad (spin y; QueryBuildInfo). Side 2 pieces are mirror clones of side 1.
Preview: OPEN (activatescr end state; COB x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['nano1', 'nano2'],
    wreck=dict(seed=77, drop=['radar']),
    preview_pose={
        'building1': {'move': (-19.5, 0, 0)}, 'building2': {'move': (19.625, 0, 0)},
        'nanobox1': {'move': (-19.25, 0, 0)}, 'nanobox2': {'move': (19.375, 0, 0)},
        'nano1': {'move': (0, 0, 8.875)}, 'nano2': {'move': (0, 0, 10.0)},
    },
)

DY = 1.0


def build(k):
    # ------------------------------------------------------------------ deck (as the T1 plant) + tower
    b = k.piece('base')
    b.plan(0.0, DY, [(-56.0, -10.0), (56.0, -10.0), (56.0, 47.0), (-56.0, 47.0)], 'paint', bevel=0.2, top_inset=0.5)
    b.box((-36.3, DY - 0.05, -9.5), (36.3, DY + 0.07, 44.0), 'paint2', bevel=0.04)
    b.box((-55.4, DY - 0.05, -8.0), (-40.6, DY + 0.12, 45.6), 'team', bevel=0.05, mirror=True)
    b.box((-40.0, DY - 0.05, -9.0), (-36.4, DY + 0.1, 46.0), 'hazard', bevel=0.04, mirror=True)
    for x in (-30.0, -18.0, -6.0, 6.0, 18.0, 30.0):
        b.box((x - 1.0, DY, 46.6), (x + 1.0, DY + 0.5, 47.1), 'lightc', bevel=0.0)
    b.box((-56.0, 0.0, -48.5), (56.0, 0.8, -10.0), 'paint2', bevel=0.1)                        # back apron
    for z in (-40.0, -16.0):                                                                   # slide rails
        b.box((-55.0, 0.7, z - 1.0), (55.0, 1.3, z + 1.0), 'steel', bevel=0.1)
    # tower: shaft (wrapped by the boxes at rest), tapered body, cab, team cap
    b.box((-6.0, 0.6, -36.0), (6.0, 27.0, -20.0), 'paint2', bevel=0.3)
    b.box((-6.2, 8.0, -20.1), (6.2, 9.2, -19.8), 'lightc', bevel=0.0)
    b.hull([(x, 26.5, z) for x in (-9.0, 9.0) for z in (-38.0, -18.0)]
           + [(x, 52.0, z) for x in (-5.0, 5.0) for z in (-31.0, -24.0)], 'paint', bevel=0.4)
    b.hull([(x, 51.0, z) for x in (-6.0, 6.0) for z in (-33.0, -22.0)]
           + [(x, 60.0, z) for x in (-8.5, 8.5) for z in (-35.0, -20.0)], 'paint2', bevel=0.3)
    b.box((-8.8, 55.0, -35.3), (8.8, 57.6, -19.7), 'lightc', bevel=0.1)
    b.hull([(x, 59.9, z) for x in (-8.5, 8.5) for z in (-35.0, -20.0)]
           + [(x, 65.0, z) for x in (-5.0, 5.0) for z in (-31.0, -24.0)], 'team', bevel=0.25)
    r = k.piece('radar'); R = r.at                                                             # spinning dish
    r.cyl(R(0, -0.6, 0), R(0, 3.0, 0), 0.9, 8, 'steel')
    r.hull([R(x, y, z) for x, y, z in [(-9.0, 2.6, 0.4), (9.0, 2.6, 0.4), (-9.0, 8.4, -0.6), (9.0, 8.4, -0.6),
                                       (-6.0, 3.0, 3.6), (6.0, 3.0, 3.6), (-6.0, 8.0, 2.8), (6.0, 8.0, 2.8)]], 'dark',
           bevel=0.15)
    r.box(R(-0.9, 4.8, 3.2), R(0.9, 6.4, 4.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ nano box (wraps the shaft; niche at the front)
    nb = k.piece('nanobox1')
    nb.box((-22.4, 0.7, -44.6), (-6.4, 25.4, -26.5), 'paint', bevel=0.4)                       # back block
    nb.box((-22.4, 0.7, -26.5), (-17.4, 25.4, -12.2), 'paint', bevel=0.35)                     # niche walls
    nb.box((-7.6, 0.7, -26.5), (-6.4, 25.4, -12.2), 'paint', bevel=0.2)
    nb.box((-17.4, 0.7, -26.5), (-7.6, 3.4, -12.2), 'paint2', bevel=0.15)                      # niche floor
    nb.box((-17.4, 12.6, -26.5), (-7.6, 25.4, -12.2), 'paint', bevel=0.3)                      # over the niche
    nb.box((-21.6, 25.3, -43.8), (-7.2, 25.8, -25.0), 'hazard', bevel=0.06)
    nb.box((-21.6, 25.3, -24.6), (-7.2, 25.8, -13.0), 'team', bevel=0.06)
    k.clone('nanobox2', 'nanobox1', mirror_x=True)
    n = k.piece('nano1')                                       # head in the niche, beam1 at (3.75, 7, -24.38)
    n.box((-16.6, 3.5, -34.0), (-8.4, 12.0, -26.6), 'steel', bevel=0.3)
    n.cyl((-12.5, 7.0, -26.8), (-12.5, 7.0, -23.0), 1.8, 10, 'dark', r2=1.3)
    n.cyl((-12.5, 7.0, -23.1), (-12.5, 7.0, -22.0), 1.3, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)
    # ------------------------------------------------------------------ hangars (outer wedges)
    h = k.piece('building1')
    h.hull([(x, 0.7, z) for x in (-29.0, -22.6) for z in (-38.0, -8.5)]
           + [(-26.5, 20.0, -36.0), (-22.6, 20.0, -36.0), (-26.5, 20.0, -11.0), (-22.6, 20.0, -11.0)], 'paint',
           bevel=0.35)
    h.hull([(-26.4, 19.9, -35.6), (-22.8, 19.9, -35.6), (-26.4, 19.9, -11.4), (-22.8, 19.9, -11.4),
            (-26.4, 20.4, -35.6), (-22.8, 20.4, -35.6), (-26.4, 20.4, -11.4), (-22.8, 20.4, -11.4)], 'team', bevel=0.05)
    h.box((-29.0, 4.0, -30.0), (-28.4, 5.2, -16.0), 'lightc', bevel=0.0)
    k.clone('building2', 'building1', mirror_x=True)

    # ------------------------------------------------------------------ beacons + pad
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 50.4, sx * 55.6))
        k.piece('lights').box((x0, DY, 37.0), (x1, 4.8, 42.0), 'lightr', bevel=0.3)
    pd = k.piece('pad'); Pd = pd.at
    pd.cyl(Pd(0, DY - 0.33, 0), Pd(0, DY + 0.1, 0), 27.0, 44, 'dark', bevel=0.12)
    pd.cyl(Pd(0, DY + 0.1, 0), Pd(0, DY + 0.22, 0), 24.8, 44, 'paint')
    pd.cyl(Pd(0, DY + 0.2, 0), Pd(0, DY + 0.3, 0), 4.2, 16, 'paint2')
    for a in range(4):                                         # T2 mark: four dark chevrons on the pad
        t = a * math.pi / 2 + math.pi / 4
        pd.hull([Pd(rr * math.cos(t + dt), yy, rr * math.sin(t + dt)) for rr, dt in ((12.0, 0.0), (18.0, -0.22),
                 (18.0, 0.22), (16.0, 0.0)) for yy in (DY + 0.2, DY + 0.32)], 'paint2', bevel=0.0)
