"""Doomsday Machine (CORE_T2_DEF_DoomsdayMachine) - Core multi-turret energy weapon. Closed it is a tall armoured
double cube: a base block crowned by eight armour segments (four sides, four corners) with a hatch in the roof. On
activation the crown segments slide out and drop to the ground, standing as four double plates round the base, and a
three-tier turret stack rises out of it: turretc (twin guns, lowest), turretb (single gun with a sliding collar),
turreta (tall column with the top gun). Each tier turns on its own.
Identity from above (open): a dark square with four team-topped armour plates on its sides and a stepped round tower
in the middle with three light steel guns pointing three ways (previewed spread) - nothing else is a turret stack.
Pieces (COB): base, turreta/b/c (move y, turn y), sleevea/b/c (turn x), barrela/b/c1/c2 (move z), collarb, hatchb, hatchc,
flarea/b/c1/c2 (emit, empty), shell1a..4a / shell1b..4b (crown segments: move x/y/z), hatch (roof hatch).
The preview shows the OPEN state (activatescr end values).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=53, drop=['shell2a', 'shell4a'], remove=['turreta']),
    preview_pose={
        'turreta': {'move': (0, 28.85, 0), 'rot': (0, -20, 0)}, 'turretb': {'move': (0, 17.75, 0), 'rot': (0, 110, 0)},
        'turretc': {'move': (0, 6.625, 0), 'rot': (0, -140, 0)},
        'barrela': {'move': (0, 0, 9.1)}, 'barrelb': {'move': (0, 0, 8.75)}, 'barrelc1': {'move': (0, 0, 7.875)},
        'barrelc2': {'move': (0, 0, 7.85)}, 'collarb': {'move': (0, 0, 8.5)}, 'sleevec': {'move': (0, 0, 10.225)},
        'hatch': {'move': (-8.0, -9.125, 0), 'rot': (0, 0, 49)}, 'hatchb': {'move': (-7.375, 0, -8.375), 'rot': (0, -46, 0)},
        'hatchc': {'move': (0, 4.25, -1.725)},
        'shell1a': {'move': (-8.25, -28.625, 0)}, 'shell1b': {'move': (0, 0, 9.85)},
        'shell2a': {'move': (0, -28.625, -8.25)}, 'shell2b': {'move': (-10.0, 0, 0)},
        'shell3a': {'move': (8.25, -28.5, 0)}, 'shell3b': {'move': (0, 0, -10.125)},
        'shell4a': {'move': (0, -28.5, 8.25)}, 'shell4b': {'move': (10.375, 0, 0)}},
)

B = 28.5          # base top / crown bottom
CH = 28.5         # crown height


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def crown_piece(k, name, x0, x1, z0, z1, side):
    """one crown segment, global box x0..x1, z0..z1, y B..B+CH, with a chamfer on its outer top edge(s).
    side: list of outward directions ('-x','+x','-z','+z') that get the chamfer and the team stripe ('a' pieces)."""
    s = k.piece(name)
    top = B + CH
    pts = []
    for x in (x0, x1):
        for z in (z0, z1):
            pts.append((x, B + 0.1, z))
            # chamfer the outward corners down
            out = (('-x' in side and x == x0) or ('+x' in side and x == x1) or ('-z' in side and z == z0) or ('+z' in side and z == z1))
            pts.append((x, top - (8.0 if out else 0.0), z))
            if out:
                ix = x + (3.6 if x == x0 and '-x' in side else -3.6 if x == x1 and '+x' in side else 0.0)
                iz = z + (3.6 if z == z0 and '-z' in side else -3.6 if z == z1 and '+z' in side else 0.0)
                pts.append((ix, top, iz))
    s.hull(pts, 'paint', bevel=0.3)
    # dark seam band low on the outer faces
    return s


def build(k):
    # ------------------------------------------------------------------ base: block
    b = k.piece('base')
    b.plan(0.0, 3.0, [(-18.0, -18.0), (18.0, -18.0), (18.0, 18.0), (-18.0, 18.0)], 'paint2', bevel=0.3, top_inset=1.0)
    b.box((-14.0, 2.8, -14.0), (14.0, B, 14.0), 'paint2', bevel=0.35)
    for y in (8.0, 18.0):
        b.box((-14.3, y, -14.3), (14.3, y + 2.0, 14.3), 'dark', bevel=0.1)
    b.box((-13.6, B - 0.2, -13.6), (13.6, B + 0.2, 13.6), 'dark', bevel=0.06)
    for s in (-1, 1):
        b.box((s * 14.3 - 0.4 if s > 0 else -14.7, 4.0, -1.0), (14.7 if s > 0 else -14.3 + 0.4, 5.4, 1.0), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ crown: 4 side (a) + 4 corner (b) segments
    sides = {'shell1a': (-14.2, -6.0, -6.0, 6.0, ['-x']), 'shell3a': (6.0, 14.2, -6.0, 6.0, ['+x']),
             'shell2a': (-6.0, 6.0, -14.2, -6.0, ['-z']), 'shell4a': (-6.0, 6.0, 6.0, 14.2, ['+z'])}
    for n, (x0, x1, z0, z1, sd) in sides.items():
        s = crown_piece(k, n, x0, x1, z0, z1, sd)
        # team stripe along the chamfer of each side segment
        top = B + CH
        if sd[0] in ('-x', '+x'):
            sg = -1 if sd[0] == '-x' else 1
            xo, xi = (x0, x0 + 3.6) if sg < 0 else (x1, x1 - 3.6)
            s.hull([(xo + sg * d * 0.7, top - 8.0 + d, z) for z in (-4.6, 4.6) for d in (0.12, 0.3)] +
                   [(xi + sg * d * 0.7, top + d, z) for z in (-4.6, 4.6) for d in (0.12, 0.3)], 'team', bevel=0.0)
            s.box((min(xo, xo + sg * 0.3), B + 4.0, -5.0), (max(xo, xo + sg * 0.3), B + 6.0, 5.0), 'dark', bevel=0.0)
        else:
            sg = -1 if sd[0] == '-z' else 1
            zo, zi = (z0, z0 + 3.6) if sg < 0 else (z1, z1 - 3.6)
            s.hull([(x, top - 8.0 + d, zo + sg * d * 0.7) for x in (-4.6, 4.6) for d in (0.12, 0.3)] +
                   [(x, top + d, zi + sg * d * 0.7) for x in (-4.6, 4.6) for d in (0.12, 0.3)], 'team', bevel=0.0)
            s.box((-5.0, B + 4.0, min(zo, zo + sg * 0.3)), (5.0, B + 6.0, max(zo, zo + sg * 0.3)), 'dark', bevel=0.0)
    corners = {'shell1b': (-14.2, -6.0, -14.2, -6.0, ['-x', '-z']), 'shell2b': (6.0, 14.2, -14.2, -6.0, ['+x', '-z']),
               'shell3b': (6.0, 14.2, 6.0, 14.2, ['+x', '+z']), 'shell4b': (-14.2, -6.0, 6.0, 14.2, ['-x', '+z'])}
    for n, (x0, x1, z0, z1, sd) in corners.items():
        crown_piece(k, n, x0, x1, z0, z1, sd)

    # ------------------------------------------------------------------ hatch: roof hatch (origin -6, 57, 0.19)
    h = k.piece('hatch')
    h.box((-5.9, B + CH - 0.2, -5.8), (5.9, B + CH + 0.9, 6.0), 'dark', bevel=0.1)
    h.box((-5.2, B + CH + 0.85, -5.0), (5.2, B + CH + 1.1, 5.2), 'hazard', bevel=0.03)

    # ------------------------------------------------------------------ turretc: lowest tier, twin guns (origin 0, 28.5, 0)
    tc = k.piece('turretc'); C = tc.at
    tc.cyl(C(0, -6.6, 0), C(0, 6.4, 0), 9.8, 12, 'paint', bevel=0.3)
    tc.cyl(C(0, 6.4, 0), C(0, 8.4, 0), 8.4, 12, 'dark', bevel=0.1)
    hc = k.piece('hatchc'); HC = hc.at
    hc.box(HC(-4.8, -4.2, 0.0), HC(4.8, 0.0, 1.2), 'dark', bevel=0.08)
    sc = k.piece('sleevec'); SC = sc.at
    sc.hull([SC(x, y, z) for x in (-5.4, 5.4) for y, z in ((-2.4, 0.0), (1.6, 0.0), (-2.2, 9.6), (1.2, 9.6))], 'dark', bevel=0.2)
    bc = k.piece('barrelc1'); BC = bc.at
    bc.cyl(BC(0, 0, -0.5), BC(0, 0, 10.6), 1.25, 8, 'steel', rot=math.pi / 8)
    bc.cyl(BC(0, 0, 8.4), BC(0, 0, 10.7), 1.65, 8, 'steel', rot=math.pi / 8, bevel=0.04)
    k.clone('barrelc2', 'barrelc1', mirror_x=True)

    # ------------------------------------------------------------------ turretb: middle tier (origin 0, 28.5, 0)
    tb = k.piece('turretb'); TB = tb.at
    tb.cyl(TB(0, -2.4, 0), TB(0, 11.0, 0), 12.6, 12, 'paint', r2=11.4, bevel=0.3)
    tb.cyl(TB(0, 10.9, 0), TB(0, 11.3, 0), 9.4, 12, 'team')
    tb.box(TB(-11.0, 2.0, -6.0), TB(-10.4, 8.0, 6.0), 'dark', bevel=0.05)
    tb.box(TB(10.4, 2.0, -6.0), TB(11.0, 8.0, 6.0), 'dark', bevel=0.05)
    hb = k.piece('hatchb'); HB = hb.at
    hb.box(HB(0.0, -4.4, -0.4), HB(10.7, 4.4, 0.6), 'dark', bevel=0.08)
    cb = k.piece('collarb'); CB = cb.at
    cb.hull([CB(x, y, z) for x in (-5.2, 5.2) for y in (-3.8, 4.8) for z in (0.0, 3.0)], 'dark', bevel=0.2)
    sb = k.piece('sleeveb'); SB = sb.at
    sb.cyl(SB(0, 0, 0.0), SB(0, 0, 7.0), 3.0, 10, 'paint2', bevel=0.1)
    bb = k.piece('barrelb'); BB = bb.at
    bb.cyl(BB(0, 0, -0.5), BB(0, 0, 10.4), 1.7, 10, 'steel', rot=math.pi / 10)
    bb.cyl(BB(0, 0, 8.2), BB(0, 0, 10.5), 2.2, 8, 'steel', rot=math.pi / 8, bevel=0.05)

    # ------------------------------------------------------------------ turreta: top tier column (origin 0, 28.5, 0)
    ta = k.piece('turreta'); A = ta.at
    ta.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(8.8, 0.0, -6.8), (8.8, 0.0, 6.8), (7.2, 16.0, -6.0), (7.2, 16.0, 6.0), (5.4, 27.0, -5.0), (5.4, 27.0, 5.0)]],
            'paint', bevel=0.3)
    ta.box(A(-4.4, 26.95, -4.0), A(4.4, 27.2, 4.0), 'team', bevel=0.03)
    for sx in (-1, 1):
        ta.box(A(sx * 7.0 - 0.6 if sx > 0 else -7.6, 4.0, -5.0), A(7.6 if sx > 0 else -7.0 + 0.6, 12.0, 5.0), 'dark', bevel=0.05)
    sa = k.piece('sleevea'); SA = sa.at
    sa.hull([SA(x, y, z) for x in (-3.0, 3.0) for y, z in ((-6.8, -5.8), (6.6, -5.8), (-3.0, 13.4), (3.0, 13.4))], 'dark', bevel=0.25)
    ba = k.piece('barrela'); BA = ba.at
    ba.cyl(BA(0, 0, -0.5), BA(0, 0, 10.0), 1.9, 10, 'steel', rot=math.pi / 10)
    ba.cyl(BA(0, 0, 7.6), BA(0, 0, 10.1), 2.5, 8, 'steel', rot=math.pi / 8, bevel=0.05)
    ba.cyl(BA(0, 0, 10.08), BA(0, 0, 10.2), 1.0, 8, 'lightr')
