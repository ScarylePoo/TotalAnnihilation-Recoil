"""Scrubber (CORE_T1_HOV_Scrubber) - Core scout hovercraft. Narrow and fast: two slim diamond-plan pontoons on black
skirts (TA layout, each pontoon its own skirt), a high central keel/cockpit between them, two jet engine pods on
raised pylons at the stern (lthrustpoint/rthrustpoint are the exhaust emit points) with swept spike fins, and a tiny
laser turret on the spine. Distinct from the Arm Skimmer: no prop ring, twin jets, two spike fins, much narrower.
Pieces: base (rocks x/z), turret (turn y), gun (turn x), flare (empty), l/rthrustpoint (empty), wake01..08 (empty).
Value groups from above: black skirt rails, dark warm pontoons, darker paint2 keel, two light steel jet pods
(Core = light mechanics) with black intakes, team stripe down the keel + team fin tips, ochre nose tips.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=12, pose={'turret': (0, 60, 0)}),
    preview_pose={'turret': (0, -20, 0)},
)

DIA = [(7.6, 25.3), (12.6, 8.8), (12.6, -8.6), (7.6, -25.7), (1.2, -17.8), (1.2, 17.7)]


def dia(y, d=0.0):
    out = []
    for x, z in DIA:
        L = math.hypot(x - 7.0, z) or 1
        out.append((x + (x - 7.0) / L * d, y, z + z / L * d))
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ pontoons (+X built, mirrored)
    b.hull(dia(0.0, 0.4) + dia(2.6, 1.7) + dia(5.2, 1.4) + dia(6.6, 0.5), 'tread', bevel=0.25, mirror=True)
    b.hull(dia(6.2, -0.4) + dia(11.3, -1.6), 'paint', bevel=0.2, mirror=True)
    b.hull(dia(6.4, 0.2) + dia(7.6, 0.1), 'steel', bevel=0.08, mirror=True)
    # ochre nose tip on each pontoon
    b.hull([(6.2, 11.3, 19.0), (8.6, 11.3, 15.2), (7.1, 11.3, 22.2), (6.2, 11.45, 19.0), (8.6, 11.45, 15.2), (7.1, 11.45, 22.2),
            (5.6, 9.6, 21.0), (7.4, 9.6, 24.0)], 'hazard', bevel=0.03, mirror=True)
    # small lift fan in each pontoon
    x, z = 7.2, -2.0
    b.cyl((x, 10.8, z), (x, 11.8, z), 3.4, 14, 'dark', bevel=0.1, mirror=True)
    b.cyl((x, 11.8, z), (x, 11.85, z), 2.6, 14, 'black', mirror=True)
    for i in range(3):
        a = i * 2 * math.pi / 3
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.6, 2.4):
            for s in (-0.5, 0.5):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, 11.55, pz), (px, 11.85, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ central keel + cockpit (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 7.0, -20.0), (2.4, 7.0, 16.0), (1.0, 8.0, 21.0), (4.2, 14.2, -16.0), (4.2, 14.2, 3.6),
             (2.0, 13.4, 14.6), (2.8, 17.6, -13.0), (2.8, 17.6, -2.0)]], 'paint2', bevel=0.2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 14.6, 3.6), (1.4, 13.6, 10.6), (1.6, 16.6, 1.0), (0.8, 15.2, 7.2)]], 'glass', bevel=0.08)
    # team stripe down the keel back
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 17.62, -12.4), (2.2, 17.62, -2.6), (2.2, 17.78, -12.4), (2.2, 17.78, -2.6)]], 'team', bevel=0.02)
    # team plates on the pontoon decks, forward of the fans (the Scrubber's two team arrows from above)
    b.hull([(x, y, z) for y in (11.32, 11.48) for x, z in [(5.4, 3.0), (9.6, 3.0), (9.4, 9.8), (7.2, 13.6), (5.6, 12.0)]],
           'team', bevel=0.03, mirror=True)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 13.48, 13.8), (2.4, 14.24, 4.6), (1.4, 13.62, 13.82), (2.4, 14.38, 4.62)]], 'team', bevel=0.02)
    # cross beams to the pontoons
    b.box((1.6, 9.6, -14.0), (6.4, 11.6, -10.0), 'dark', bevel=0.1, mirror=True)
    b.box((1.6, 9.6, 6.0), (6.4, 11.6, 9.6), 'dark', bevel=0.1, mirror=True)
    # ------------------------------------------------------------------ twin jet pods on pylons (+X, mirrored)
    jx, jy = 5.5, 17.0
    b.hull([(3.4, 14.0, -18.0), (4.6, 14.0, -18.0), (3.4, 14.0, -9.0), (4.6, 14.0, -9.0),
            (4.8, 16.0, -17.0), (6.0, 16.0, -17.0), (4.8, 16.0, -10.0), (6.0, 16.0, -10.0)], 'dark', bevel=0.1, mirror=True)
    b.cyl((jx, jy, -20.6), (jx, jy, -7.0), 2.3, 12, 'steel', bevel=0.1, mirror=True)
    b.cyl((jx, jy, -7.0), (jx, jy, -5.6), 2.3, 12, 'steel', r2=1.8, mirror=True)
    b.cyl((jx, jy, -5.6), (jx, jy, -5.5), 1.5, 12, 'black', mirror=True)
    b.cyl((jx, jy, -21.6), (jx, jy, -20.6), 1.6, 12, 'dark', r2=2.1, mirror=True)
    b.cyl((jx, jy, -21.7), (jx, jy, -21.6), 1.2, 12, 'lightr', mirror=True)
    b.cyl((jx, jy, -15.0), (jx, jy, -13.8), 2.45, 12, 'dark', mirror=True)
    # swept spike fins on the pods (Core spikes), team tips
    b.hull([(jx + 1.4, 18.6, -19.6), (jx + 1.4, 18.6, -12.0), (jx + 2.0, 18.6, -19.4), (jx + 4.8, 27.4, -18.2),
            (jx + 5.2, 27.4, -17.0)], 'paint', bevel=0.08, mirror=True)
    b.hull([(jx + 3.95, 24.4, -18.7), (jx + 4.4, 24.4, -16.3), (jx + 4.5, 24.4, -18.7), (jx + 4.8, 27.45, -18.25),
            (jx + 5.25, 27.45, -17.0), (jx + 4.2, 24.4, -18.0)], 'team', bevel=0.02, mirror=True)
    # nose lights
    b.box((-1.2, 8.2, 20.6), (1.2, 9.4, 21.4), 'lightw', bevel=0.0)
    # antenna
    b.cyl((-2.2, 17.6, -6.0), (-2.2, 18.4, -6.0), 0.3, 8, 'dark')
    b.cyl((-2.2, 18.4, -6.0), (-2.2, 25.0, -6.0), 0.08, 6, 'steel', r2=0.04)
    b.cyl((-2.2, 25.0, -6.0), (-2.2, 25.2, -6.0), 0.13, 6, 'lightr')

    # ---------------------------------------------------------------- turret (origin 0, 19.62, -7.5)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -2.1, 0), A(0, 0.2, 0), 2.6, 12, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.9, 0.0, -4.2), (2.9, 0.0, 1.2), (1.6, 3.6, -3.4), (1.6, 3.6, 0.6), (1.8, 0.0, 2.6)]], 'paint', bevel=0.14)
    t.box(A(-1.2, 3.55, -2.9), A(1.2, 3.75, 0.2), 'team', bevel=0.03)
    # ---------------------------------------------------------------- gun (origin 0, 22.12, -6.63)
    g = k.piece('gun'); G = g.at
    g.box(G(-1.2, -1.1, -0.4), G(1.2, 0.9, 2.0), 'paint2', bevel=0.1)
    g.cyl(G(0, -0.4, 1.6), G(0, -0.4, 9.4), 0.5, 10, 'steel')
    g.cyl(G(0, -0.4, 2.6), G(0, -0.4, 4.6), 0.8, 10, 'steel', rot=math.pi / 10, bevel=0.03)
    g.cyl(G(0, -0.4, 9.2), G(0, -0.4, 9.9), 0.7, 8, 'steel', rot=math.pi / 8)
    g.cyl(G(0, -0.4, 9.88), G(0, -0.4, 9.94), 0.3, 8, 'lightr')
