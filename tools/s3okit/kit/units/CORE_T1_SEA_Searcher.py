"""Searcher (CORE_T1_SEA_Searcher) - Core scout boat. A flat, wide-shouldered dark planing hull (low, fast), the whole
superstructure is the rotating `turret`: an angular wedge bridge at the stern with a light roof, carrying two long
light missile boxes on its flanks that reach forward along the deck (sleeve1/2 pitch, barrel1/2 = the launch tubes,
recoil). From above: dark arrowhead hull, light bridge with a team roof and two light launcher rails with team tops,
an ochre hazard chevron on the bow.
Pieces (TA layout): base, turret (turn y), missile (empty aim point), sleeve1/2 (turn x), barrel1/2 (move z),
flare1/2 (empty), wake1/2 (empty). sleeve2/barrel2 are mirrored clones of sleeve1/barrel1.
Value groups from above: dark Core hull (paint) with darker paint2 deck recesses, light steel launchers, team on the
bridge roof and launcher tops, ochre bow chevron. Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=6, drop=['barrel2'], pose={'turret': (0, 30, 0)}),
    preview_pose={'turret': (0, -15, 0), 'sleeve1': (-6, 0, 0), 'sleeve2': (-6, 0, 0)},
)

OUT = [(0.0, 33.0), (3.4, 31.6), (9.8, 12.0), (11.8, -7.5), (11.8, -25.0), (6.4, -32.4)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ flat planing hull (crosses x = 0)
    b.hull(ring(OUT, -1.6, 0.7, 0.88, -1.0) + ring(OUT, 0.6, 1.0, 1.0), 'paint2', bevel=0.16)
    b.hull(ring(OUT, 0.6, 1.0, 1.0) + ring(OUT, 3.0, 0.86, 0.9, -1.0), 'paint', bevel=0.2)
    # sunken deck well amidships (darker), the launchers ride over it
    b.plan(2.6, 3.15, [(-6.6, 9.4), (6.6, 9.4), (8.0, -6.8), (8.0, -21.0), (-8.0, -21.0), (-8.0, -6.8)], 'paint2', bevel=0.1)
    # raised foredeck wedge with an ochre hazard chevron (fast-attack bow)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.4, 2.9, 9.0), (1.4, 2.9, 27.6), (5.2, 4.2, 9.6), (0.9, 3.6, 24.8)]], 'paint', bevel=0.14)
    for s in (-1, 1):
        q = [(0.0, 23.8), (1.2, 23.8), (5.0, 13.0), (3.0, 13.0)]
        b.hull([(x * s, y + h, z) for x, z in q for y in [3.62 + (24.8 - z) / 15.2 * 0.58] for h in (0.03, 0.17)],
               'hazard', bevel=0.03)
    # bow sensor dome + lights
    b.sphere((0, 3.8, 18.4), 1.3, 'dark', scale=(1, 0.7, 1.4))
    b.box((10.6, 1.4, 4.0), (10.9, 2.0, 6.0), 'lightw', bevel=0.0, mirror=True)
    # stern: twin dark water-jet housings with hot exhaust
    b.hull([(x, y, z) for x, y, z in
            [(3.0, -0.8, -26.0), (8.4, -0.8, -24.6), (3.0, -0.8, -33.4), (8.0, -0.8, -32.0),
             (3.4, 3.4, -26.6), (8.0, 3.4, -25.4), (3.6, 2.6, -32.6), (7.6, 2.6, -31.4)]], 'dark', bevel=0.16, mirror=True)
    b.cyl((5.6, 0.8, -32.4), (5.6, 0.8, -32.7), 1.3, 10, 'lightr', mirror=True)

    # ------------------------------------------------------------------ turret = the rotating bridge (origin 0, 5.25, -17.5)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -2.6, 0), A(0, -1.6, 0), 5.0, 16, 'dark', bevel=0.06)
    # lower block: wide angular base under the bridge
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.6, -1.8, 4.6), (7.4, -1.8, -1.6), (4.6, -1.8, -6.8),
             (2.6, -1.8, 8.4), (2.2, 3.4, 7.2), (6.6, 3.4, -1.4), (4.2, 3.4, -6.0)]], 'paint', bevel=0.16)
    # dark window band wrapping the front of the bridge
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.25, 3.2, 7.4), (6.85, 3.2, -1.3), (2.45, 5.1, 6.6), (7.25, 5.1, -1.6),
             (5.0, 3.2, -5.8), (5.2, 5.1, -6.0)]], 'black', bevel=0.04)
    # bridge top: light Core steel-grey roof with a team plate
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.45, 5.05, 6.6), (7.25, 5.05, -1.6), (5.2, 5.05, -6.0),
             (1.6, 7.6, 2.6), (4.2, 7.6, -1.2), (2.4, 7.6, -4.2)]], 'paint', bevel=0.14)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(1.3, 7.56, 2.0), (3.5, 7.56, -1.2), (2.0, 7.56, -3.6),
             (1.25, 7.74, 1.9), (3.4, 7.74, -1.2), (1.95, 7.74, -3.5)]], 'team', bevel=0.03)
    # sensor mast with a spinning-radar bar, offset left
    t.cyl(A(-1.6, 7.6, -2.8), A(-1.6, 12.2, -3.0), 0.32, 8, 'dark', r2=0.22)
    t.box(A(-4.0, 10.6, -3.4), A(0.8, 11.1, -2.6), 'steel', bevel=0.04)
    t.cyl(A(-1.6, 12.2, -3.0), A(-1.6, 12.5, -3.0), 0.24, 6, 'lightr')
    # aft exhaust block
    t.box(A(-2.8, 3.4, -7.0), A(2.8, 5.6, -5.2), 'dark', bevel=0.1)

    # ------------------------------------------------------------------ launcher boxes (sleeve1 origin -5, 6, -5; geometry -x)
    sv = k.piece('sleeve1'); S = sv.at
    sv.hull([S(x, y, z) for x, y, z in
             [(0.2, -1.9, -5.6), (-4.0, -1.9, -5.6), (0.2, -1.9, 10.6), (-4.0, -1.9, 10.6),
              (0.0, 2.3, -5.2), (-3.8, 2.3, -5.2), (0.0, 2.3, 10.2), (-3.8, 2.3, 10.2)]], 'steel', bevel=0.14)
    sv.box(S(-3.2, 2.25, -3.6), S(-0.6, 2.45, 8.6), 'team', bevel=0.03)
    sv.box(S(-3.6, -1.4, -6.4), S(-0.2, 1.8, -5.5), 'dark', bevel=0.06)
    sv.cyl(S(0.1, 0.0, -1.0), S(1.4, 0.0, -1.0), 1.2, 10, 'dark')   # trunnion into the bridge
    k.clone('sleeve2', 'sleeve1', mirror_x=True)
    # launch tube (barrel1 origin -6.88, 6.25, 5.88): fat light tube, dark muzzle ring, warhead tip visible
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -1.2), B(0, 0, 11.6), 1.25, 10, 'steel', rot=math.pi / 10)
    br.cyl(B(0, 0, 10.4), B(0, 0, 12.2), 1.42, 10, 'dark', rot=math.pi / 10, bevel=0.04)
    br.cyl(B(0, 0, 12.15), B(0, 0, 12.25), 0.9, 10, 'black')
    br.cyl(B(0, 0, 11.4), B(0, 0, 12.6), 0.75, 8, 'hazard', r2=0.2)
    k.clone('barrel2', 'barrel1', mirror_x=True)
