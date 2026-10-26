"""Triton (ARM_T2_VEH_Triton) - Arm amphibious tank (AMPHTANK: drives along the sea floor, not a floater, so ground
culling applies). Boat-like hull with a pointed prow between two long tracked flotation pods, intake grilles on the pod
flanks, twin propeller shrouds at the stern and a tall snorkel; a low lozenge turret at the rear with one long gun
(barrel turns x and recoils 6 elmo back into the turret).
Value groups from above: light pods and prow (the boat-hull arrowhead is the read), darker paint2 deck well, dark
grilles/shrouds/snorkel, team colour on the turret roof and a stripe along each pod's inner edge, light steel gun.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=29, drop=['barrel'], pose={'turret': (0, -40, 0)}),
    preview_pose={'turret': (0, -18, 0), 'barrel': (-4, 0, 0)},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ track pods
    xi, xo = 15.0, 24.4
    belt = [(-21.6, 0.0), (18.4, 0.0), (21.6, 3.2), (20.6, 6.8), (-22.0, 6.8), (-24.0, 3.2)]
    b.prism(xi, xo, belt, 'tread', bevel=0.18, mirror=True)
    for z in (-16.8, -10.0, -3.2, 3.6, 10.4):
        b.cyl((xi, 2.6, z), (xi - 0.5, 2.6, z), 2.1, 12, 'dark', mirror=True)
        b.cyl((xi - 0.5, 2.6, z), (xi - 0.8, 2.6, z), 0.8, 8, 'steel', mirror=True)
    # flotation pod over each track: rounded-ish hull, nose raked like a float
    b.hull([(14.6, 13.4, -22.0), (24.8, 13.4, -22.0), (24.8, 13.4, 13.6), (14.6, 13.4, 13.6),
            (15.2, 14.6, -19.0), (24.0, 14.6, -19.0), (24.0, 14.6, 10.0), (15.2, 14.6, 10.0),
            (14.6, 7.6, 22.4), (24.4, 7.6, 21.4), (14.6, 9.6, 21.4), (24.4, 9.6, 20.4),
            (14.6, 6.6, -24.4), (25.2, 6.6, -24.0), (25.2, 6.6, 18.0), (14.6, 6.6, 19.0)], 'paint', bevel=0.2, mirror=True)
    # team stripe on each pod's inner top edge
    b.box((15.6, 14.6, -17.6), (17.8, 14.82, 8.6), 'team', bevel=0.04, mirror=True)
    # intake grilles on the pod flanks (TA's slatted vents), dark with black slats
    b.hull([(25.0, 8.0, -14.0), (25.0, 12.4, -14.0), (25.0, 8.0, 2.0), (25.0, 12.4, 2.0),
            (25.6, 8.4, -13.6), (25.6, 12.0, -13.6), (25.6, 8.4, 1.6), (25.6, 12.0, 1.6)], 'dark', bevel=0.06, mirror=True)
    for z in (-12.6, -9.6, -6.6, -3.6, -0.6):
        b.box((25.5, 8.6, z), (25.8, 11.8, z + 1.4), 'black', bevel=0.0, mirror=True)
    # vent block on the pod top, rear
    b.box((19.0, 14.6, -18.2), (23.2, 15.6, -10.0), 'dark', bevel=0.08, mirror=True)
    # propeller shrouds at the pod sterns
    b.cyl((19.6, 8.6, -22.6), (19.6, 8.6, -26.4), 3.0, 14, 'dark', bevel=0.08, mirror=True)
    b.cyl((19.6, 8.6, -26.4), (19.6, 8.6, -26.6), 1.8, 14, 'black', mirror=True)
    b.box((19.3, 5.6, -26.2), (19.9, 11.6, -24.8), 'steel', bevel=0.04, mirror=True)
    # lights in the pod noses
    b.box((17.0, 8.6, 21.0), (22.0, 9.6, 21.8), 'dark', bevel=0.05, mirror=True)
    b.box((17.4, 8.8, 21.75), (21.6, 9.4, 21.85), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ central hull: boat prow (crosses x = 0)
    for z in (-14.0, 4.0):
        b.box((-15.0, 3.6, z - 2.6), (15.0, 7.4, z + 2.6), 'dark', bevel=0.12)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.6, 3.0, -22.6), (10.6, 3.0, 14.0), (0.0, 3.6, 28.6),
             (11.0, 11.0, -23.4), (11.0, 11.0, 12.0), (0.0, 9.6, 29.4)]], 'paint', bevel=0.2)
    # deck well (darker) on top of the hull where the turret sits
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 11.0, -22.4), (9.6, 11.0, 10.0), (0.0, 11.0, 22.0),
             (8.0, 15.4, -20.8), (8.0, 15.4, 4.0), (0.0, 13.4, 16.0)]], 'paint2', bevel=0.18)
    # hazard prow tip (front reads as a pointed arrowhead)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.8, 10.4, 24.4), (0.0, 9.65, 29.2), (3.8, 10.55, 24.4), (0.0, 9.8, 29.2)]] + [(0.0, 10.6, 23.0)], 'hazard', bevel=0.03)
    # snorkel (tall dark tube, left rear) - the amphibious tell in side view
    b.cyl((-6.2, 15.4, -19.0), (-6.2, 24.0, -19.0), 1.1, 12, 'dark', bevel=0.05)
    b.cyl((-6.2, 24.0, -19.0), (-6.2, 24.6, -17.6), 1.3, 12, 'dark', bevel=0.05)
    b.cyl((-6.2, 24.6, -17.6), (-6.2, 24.7, -17.0), 1.0, 12, 'black')
    # bilge vents on the deck, right
    b.box((3.6, 15.4, -20.0), (7.2, 15.9, -14.6), 'dark', bevel=0.06)
    # stern plate + lights
    b.box((-10.0, 4.2, -23.8), (10.0, 10.2, -23.2), 'dark', bevel=0.06)
    b.box((8.0, 8.2, -23.9), (9.4, 9.0, -23.75), 'lightr', bevel=0.0, mirror=True)
    # cleats/tow rings on the prow (detail)
    b.cyl((3.4, 11.6, 14.0), (3.4, 12.2, 14.0), 0.6, 8, 'steel', mirror=True)

    # ---------------------------------------------------------------- turret (origin 0, 17.34, -7.03; turns y)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -2.0, 0), A(0, 0.4, 0), 5.0, 18, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.0, 0.0, -10.4), (7.4, 0.0, -2.0), (5.4, 0.0, 4.6), (2.6, 0.0, 8.6),
             (0.0, 3.2, -9.0), (6.0, 3.2, -2.0), (4.4, 3.2, 4.0), (2.0, 3.2, 7.4)]] + [A(0, 0, 9.0), A(0, 3.2, 7.8)],
           'paint', bevel=0.16)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.0, 3.18, -7.6), (4.6, 3.18, -2.0), (3.2, 3.18, 3.4), (1.4, 3.18, 6.0),
             (0.0, 3.34, -7.5), (4.5, 3.34, -2.0), (3.1, 3.34, 3.35), (1.35, 3.34, 5.9)]], 'team', bevel=0.03)
    t.box(A(-2.4, 0.4, 7.0), A(2.4, 2.6, 8.6), 'dark', bevel=0.08)           # mantlet slot
    t.cyl(A(4.6, 3.2, -4.4), A(4.6, 4.2, -4.4), 0.9, 10, 'paint2', bevel=0.05)
    t.box(A(4.2, 3.7, -3.6), A(5.0, 4.0, -3.5), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- barrel (origin at the mantlet; recoils 6)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -6.4), B(0, 0, 2.0), 1.4, 12, 'dark', bevel=0.05)
    br.cyl(B(0, 0, 1.6), B(0, 0, 16.6), 0.92, 12, 'steel')
    br.cyl(B(0, 0, 8.4), B(0, 0, 9.6), 1.25, 12, 'dark', bevel=0.05)
    br.cyl(B(0, 0, 16.4), B(0, 0, 18.4), 1.35, 8, 'dark', rot=math.pi / 8, bevel=0.06)
    br.cyl(B(0, 0, 18.38), B(0, 0, 18.46), 0.6, 8, 'black')
