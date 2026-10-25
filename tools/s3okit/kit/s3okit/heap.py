"""Generic scrap heap: a pulverised wreck reduced to small broken bits on a scorched mound.
One model per footprint size (and per variant seed). Neutral 'SCRAP' palette, burnt texture."""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler, noise
from .common import MATS
from . import geom


def make(size, seed=1):
    rnd = random.Random(seed * 7919 + size)
    geom.reset_scene()
    R = size * 16 * 0.42                    # mound radius in elmos
    H = 1.4 + size * 0.85                   # mound height
    bm = bmesh.new()
    mi = lambda n: MATS.index(n)

    def mound(r):
        t = max(0.0, 1 - (r / R) ** 2)
        return H * t ** 1.5

    # scorched ground mound (rim dips below 0 so it blends into terrain)
    rings, segs = 6 + size, 10 + 3 * size
    grid = []
    for i in range(rings + 1):
        r = R * 1.08 * i / rings
        row = []
        for j in range(segs if i else 1):
            a = 2 * math.pi * j / segs
            p = Vector((r * math.cos(a), 0, r * math.sin(a)))
            p.y = mound(r) + noise.noise(p * 0.25 + Vector((seed, 0, 0))) * 0.35 * (1 - i / rings) - (0.6 if i == rings else 0)
            row.append(bm.verts.new(p))
        grid.append(row)
    for i in range(1, rings + 1):
        inner, outer = grid[i - 1], grid[i]
        for j in range(segs):
            a, b = outer[j], outer[(j + 1) % segs]
            if i == 1:
                f = bm.faces.new((inner[0], b, a))
            else:
                c, d = inner[(j + 1) % segs], inner[j]
                f = bm.faces.new((d, c, b, a))
            f.material_index = mi('ash')
    mound_faces = list(bm.faces)
    for f in mound_faces:           # make every mound face point up (outwards)
        f.normal_update()
        if f.normal.y < 0:
            f.normal_flip()

    def add_hull(pts, mat):
        vs = [bm.verts.new(p) for p in pts]
        r = bmesh.ops.convex_hull(bm, input=vs)
        junk = list({g for g in r['geom_interior'] + r['geom_unused'] if isinstance(g, bmesh.types.BMVert)})
        if junk:
            bmesh.ops.delete(bm, geom=junk, context='VERTS')
        for g in r['geom']:
            if isinstance(g, bmesh.types.BMFace) and g.is_valid:
                g.material_index = mi(mat)

    def place(local_pts, at, rot):
        M = Matrix.Translation(at) @ rot.to_matrix().to_4x4()
        return [M @ Vector(p) for p in local_pts]

    mats = ['paint'] * 4 + ['paint2'] * 2 + ['dark'] * 4 + ['steel'] * 2 + ['rust'] * 3 + ['hazard']
    n = int(42 * size ** 1.5) + 20
    for _ in range(n):
        r = R * 0.92 * math.sqrt(rnd.random()); a = rnd.uniform(0, 2 * math.pi)
        at = Vector((r * math.cos(a), 0, r * math.sin(a)))
        s = rnd.uniform(0.3, 1.15) * (0.8 + 0.1 * size)
        at.y = mound(r) + rnd.uniform(-0.25, 0.35) * s
        rot = Euler((rnd.uniform(-1.2, 1.2), rnd.uniform(0, 6.3), rnd.uniform(-1.2, 1.2)))
        kind = rnd.choices(['plate', 'beam', 'pipe', 'chunk', 'wheel', 'bent'], [30, 18, 12, 28, 4, 8])[0]
        mat = rnd.choice(mats)
        if kind == 'plate':
            w, d, t = s * rnd.uniform(1.0, 2.2), s * rnd.uniform(0.7, 1.6), 0.12 + 0.05 * s
            pts = [(x * w, y * t, z * d) for x in (-.5, .5) for y in (-.5, .5) for z in (-.5, .5)]
            pts[0] = (pts[0][0] * 0.6, pts[0][1], pts[0][2] * 0.5)          # torn corner
            add_hull(place(pts, at, rot), mat)
        elif kind == 'beam':
            l, w = s * rnd.uniform(2.0, 4.0), 0.22 + 0.08 * s
            add_hull(place([(x * w, y * w, z * l) for x in (-.5, .5) for y in (-.5, .5) for z in (-.5, .5)], at, rot),
                     rnd.choice(['dark', 'steel', 'rust']))
        elif kind == 'pipe':
            M = Matrix.Translation(at) @ rot.to_matrix().to_4x4()
            res = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.18 * s + 0.1, radius2=0.18 * s + 0.1,
                                        depth=s * rnd.uniform(1.5, 3.0), matrix=M)
            for f in {f for v in res['verts'] for f in v.link_faces}:
                f.material_index = mi(rnd.choice(['steel', 'dark', 'rust']))
        elif kind == 'chunk':
            pts = [(rnd.uniform(-.6, .6) * s, rnd.uniform(-.4, .4) * s, rnd.uniform(-.6, .6) * s) for _ in range(8)]
            add_hull(place(pts, at, rot), mat)
        elif kind == 'wheel':
            M = Matrix.Translation(at) @ rot.to_matrix().to_4x4() @ Matrix.Rotation(math.pi / 2, 4, 'X')
            res = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.6 * s, radius2=0.6 * s, depth=0.35 * s, matrix=M)
            for f in {f for v in res['verts'] for f in v.link_faces}:
                f.material_index = mi('dark')
        else:  # bent panel: two plates at an angle
            w, d, t = s * 1.4, s * 1.0, 0.12 + 0.04 * s
            k = rnd.uniform(0.4, 1.1)
            p1 = [(x * w, y * t, z * d) for x in (0, 1) for y in (-.5, .5) for z in (-.5, .5)]
            p2 = [(-x * w * math.cos(k), y * t + x * w * math.sin(k), z * d) for x in (0, 1) for y in (-.5, .5) for z in (-.5, .5)]
            add_hull(place(p1, at, rot), mat); add_hull(place(p2, at, rot), mat)

    me = bpy.data.meshes.new('base'); bm.to_mesh(me); bm.free()
    for m in MATS:
        me.materials.append(geom.material(m))
    ob = bpy.data.objects.new('base', me)
    bpy.context.scene.collection.objects.link(ob)
    return ob
