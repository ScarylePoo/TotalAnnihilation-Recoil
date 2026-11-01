"""Metal Extractor (CORE_T1_ECO_MetalExtractor) - Core mex. A low dark hexagonal pyramid over the metal spot; on top a
heavy three-armed claw (the 'arms') that rises 15 elmo on its shaft when switched on and spins, its three steel
claw hands raking the ore at the pyramid shoulders.
Identity from above: dark warm hexagon, three team facets between the claws, a light steel 'Y' claw with a glowing
core (the Arm mex is a light octagon with a straight two-drill bar).
Pieces (COB): base, stand (static shaft), arms (move y 15 on Go, spin y), hand1..3 (claw hands, children of arms).
Preview: working state (arms raised 15).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=12, drop=['hand2']),
    preview_pose={'arms': {'move': (0, 15.0, 0), 'rot': (0, 20, 0)}},
)


def hexagon(r, rot=0.0):
    return [(r * math.cos(rot + i * math.pi / 3), r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def build(k):
    # ------------------------------------------------------------------ base: hex pyramid
    b = k.piece('base')
    b.plan(0.0, 3.0, hexagon(27.4), 'paint2', bevel=0.25, top_inset=0.8)
    b.plan(2.9, 17.6, hexagon(25.4), 'paint', bevel=0.3, top_inset=13.4)
    b.plan(17.5, 19.6, hexagon(12.6), 'dark', bevel=0.15, top_inset=0.6)
    b.cyl((0, 19.0, 0), (0, 19.9, 0), 7.6, 12, 'black')

    # facet plates: team on the three faces between the claws, dark vent grilles on the other three
    def face_plate(ang, mat, w0, w1, y0, y1, lift=0.1):
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a); px, pz = -cz, cx
        ap = lambda y: (25.4 - (y - 2.9) / 14.7 * 13.4) * math.cos(math.pi / 6)
        pts = []
        for y, w in ((y0, w0), (y1, w1)):
            r = ap(y)
            for t in (-w, w):
                for d in (lift, lift + 0.25):
                    pts.append((cx * (r + d) + px * t, y + d * 0.7, cz * (r + d) + pz * t))
        b.hull(pts, mat, bevel=0.0)
    for ang in (90, 210, 330):
        face_plate(ang, 'team', 9.0, 4.4, 4.2, 14.6)
    for ang in (30, 150, 270):
        face_plate(ang, 'dark', 5.0, 3.0, 4.6, 11.0)
        for i in range(3):
            y = 5.6 + i * 1.9
            face_plate(ang, 'black', 4.2 - i * 0.35, 4.0 - i * 0.35, y, y + 0.8, lift=0.32)
    # ochre hazard band on the skirt front and a warm light
    b.box((-6.0, 1.0, 23.35), (6.0, 2.4, 23.75), 'hazard', bevel=0.0)
    b.box((-1.0, 0.9, -23.75), (1.0, 2.0, -23.45), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ stand: the shaft the claw rides on
    s = k.piece('stand')
    s.cyl((0, 18.0, 0), (0, 33.0, 0), 3.4, 8, 'steel', rot=math.pi / 8)
    for y in (22.0, 26.0):
        s.cyl((0, y, 0), (0, y + 0.8, 0), 3.9, 8, 'dark', rot=math.pi / 8)

    # ------------------------------------------------------------------ arms: claw hub + three arms (origin 0,0,0)
    a = k.piece('arms')
    a.cyl((0, 17.0, 0), (0, 24.6, 0), 6.4, 6, 'paint', r2=5.4, rot=math.pi / 6, bevel=0.2)
    a.cyl((0, 24.5, 0), (0, 25.4, 0), 3.6, 6, 'lightr', rot=math.pi / 6)

    def along(ang, pts):
        c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        return [(u * c - w * s_, y, u * s_ + w * c) for u, y, w in pts]

    for ang in (270, 30):          # hand1 at -z, hand3 at +x+z (hand2's arm at -x+z is the mirror twin)
        m = ang == 30
        a.hull(along(ang, [(u, y, w) for u in (4.0, 15.6) for y in (18.4, 23.0) for w in (-2.8, 2.8)]
                     ), 'paint', bevel=0.25, mirror=m)
        a.hull(along(ang, [(u, y, w) for u in (5.0, 14.0) for y in (23.0, 23.3) for w in (-2.0, 2.0)]), 'team',
               bevel=0.0, mirror=m)
        a.cyl(tuple(along(ang, [(12.6, 21.0, -3.2)])[0]), tuple(along(ang, [(12.6, 21.0, 3.2)])[0]), 2.2, 8, 'dark',
              mirror=m)

    # ------------------------------------------------------------------ hands: claw fingers hanging off the arm tips
    def hand(name, ang):
        h = k.piece(name)
        h.hull(along(ang, [(u, y, w) for (u, y) in ((11.0, 21.6), (16.6, 21.6), (16.0, 12.0), (13.0, 11.0))
                           for w in (-2.6, 2.6)]), 'steel', bevel=0.2)
        h.hull(along(ang, [(u, y, w) for (u, y) in ((13.0, 11.4), (16.0, 12.4), (14.8, 1.0), (13.6, 1.4))
                           for w in (-1.8, 1.8)]), 'dark', bevel=0.12)
    hand('hand1', 270)
    hand('hand3', 30)
    k.clone('hand2', 'hand3', mirror_x=True)
