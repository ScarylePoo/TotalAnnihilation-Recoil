"""Generic scrap heap: a pulverised wreck reduced to small broken bits, piled on a scorched patch of ground.
One model per footprint size and per variant seed (a=1, b=2, ...). The variant picks the pile's layout and what it is
mostly made of, so same-size heaps differ in outline and value at game distance, not only in where the bits landed.
Neutral 'SCRAP' palette, burnt texture. Deterministic: the same (size, seed) gives the same geometry."""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler, noise
from .common import MATS
from . import geom

# The mound is flat noise under the bits, so it gets little texture: unwrap uses this instead of the units' 'ash' value.
ASH_IMPORTANCE = 0.03

KINDS = ('plate', 'beam', 'pipe', 'chunk', 'wheel', 'bent')
# per variant: bit kinds (weights in KINDS order), then metal per value cluster (dark end, light end of the cluster noise)
VARIANTS = [
    dict(kinds=(30, 16, 10, 30, 4, 10), dark=['dark', 'dark', 'rust', 'paint2'], light=['paint', 'paint', 'steel', 'hazard']),   # balanced
    dict(kinds=(10, 42, 26, 12, 2, 8), dark=['dark', 'dark', 'rust'], light=['steel', 'steel', 'paint']),                        # girders and pipes
    dict(kinds=(50, 6, 4, 14, 2, 24), dark=['paint2', 'dark'], light=['paint', 'paint', 'paint', 'steel']),                      # torn armour, light
    dict(kinds=(20, 14, 8, 48, 4, 6), dark=['rust', 'rust', 'dark'], light=['rust', 'paint2', 'paint']),                         # rusted lumps
    dict(kinds=(14, 8, 6, 64, 4, 4), dark=['dark', 'paint2'], light=['paint', 'dark', 'steel']),                                 # fine rubble
    dict(kinds=(34, 14, 10, 18, 10, 14), dark=["dark", "paint2", "dark"], light=['hazard', 'paint', 'steel', 'paint']),         # machinery, ochre flecks
]


def _layout(v, rnd):
    """lumps of the pile for variant index v: (x, z, radius x, radius z, height), in units of the footprint half-width"""
    if v == 0:      # one round pile and a small satellite
        return [(-.08, 0, .8, .8, 1.0), (.66, 0, .28, .28, .35)]
    if v == 1:      # long ridge
        return [(0, 0, .96, .4, 1.0), (.25, .22, .34, .3, .55)]
    if v == 2:      # two humps
        return [(-.42, .05, .52, .5, 1.0), (.54, -.1, .4, .36, .7)]
    if v == 3:      # crescent
        return [(.6 * math.cos(a), .6 * math.sin(a), .36, .36, h)
                for a, h in zip((-1.7, -.6, .5, 1.6), (.75, 1.0, .9, .65))]
    if v == 4:      # separate small piles, with bare ground between them
        lumps = [(0, 0, .3, .3, .75)]
        for i in range(5):
            a = i * 2 * math.pi / 5 + rnd.uniform(-.25, .25)
            lumps.append((.66 * math.cos(a), .66 * math.sin(a), .27, .27, rnd.uniform(.55, .85)))
        return lumps
    # comet: tall tight cone off centre, trailing a thin tail
    return [(.36, .28, .58, .58, 1.35), (-.3, -.22, .34, .26, .45), (-.68, -.5, .22, .18, .3)]


def make(size, seed=1):
    rnd = random.Random(seed * 7919 + size)
    geom.reset_scene()
    v = (seed - 1) % len(VARIANTS)
    var = VARIANTS[v]
    L = size * 8 * 0.95                     # half-width of the footprint the pile may use, elmos
    H = 1.6 + size * 1.15                   # height of a height-1 lump: big heaps read big
    turn = rnd.uniform(0, 2 * math.pi)
    ct, st = math.cos(turn), math.sin(turn)
    lumps = [(L * (x * ct - z * st), L * (x * st + z * ct), L * rx, L * rz, H * h) for x, z, rx, rz, h in _layout(v, rnd)]
    nseed = Vector((seed * 3.7, size * 1.3, 0))

    def field(x, z):
        """pile height at (x, z): lumps combined, 0 outside them"""
        s = 0.0
        for cx, cz, rx, rz, h in lumps:
            dx, dz = x - cx, z - cz
            lx, lz = (dx * ct + dz * st) / rx, (-dx * st + dz * ct) / rz    # the lumps' radii follow the layout's axes
            t = 1 - (lx * lx + lz * lz)
            if t > 0:
                s += (h * t ** 1.3) ** 2
        return math.sqrt(s)

    bm = bmesh.new()
    mi = lambda n: MATS.index(n)

    # scorched ground: a jittered grid kept only under the lumps, so the outline is ragged and follows the pile
    step = 1.4 + 0.5 * size
    N = int(L / step) + 2
    eps = 0.03 * H
    jit = {(i, j): (rnd.uniform(-.25, .25) * step, rnd.uniform(-.25, .25) * step)
           for i in range(-N, N + 2) for j in range(-N, N + 2)}
    gp = {k: (k[0] * step + d[0], k[1] * step + d[1]) for k, d in jit.items()}
    gh = {k: field(*p) for k, p in gp.items()}
    verts = {}

    def gv(k):
        if k not in verts:
            x, z = gp[k]
            h = gh[k]
            y = h + noise.noise(Vector((x, z, 0)) * 0.3 + nseed) * 0.1 * H * min(1.0, h / (0.3 * H)) if h > eps else -0.5
            verts[k] = bm.verts.new((x, y, z))
        return verts[k]

    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            c = [(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)]    # counter-clockwise seen from above (+Y)
            if max(gh[k] for k in c) > eps:
                for tri in ((c[0], c[1], c[2]), (c[0], c[2], c[3])):
                    bm.faces.new([gv(k) for k in tri]).material_index = mi('ash')
    for f in bm.faces:
        f.normal_update()
        if f.normal.y < 0:
            f.normal_flip()

    bit = bm.faces.layers.int.new('bit')
    for f in bm.faces:
        f[bit] = -1
    state = dict(id=-1)

    def tag(faces, mat):
        for f in faces:
            f.material_index = mi(mat)
            f[bit] = state['id']

    def add_hull(pts, mat):
        vs = [bm.verts.new(p) for p in pts]
        r = bmesh.ops.convex_hull(bm, input=vs)
        junk = list({g for g in r['geom_interior'] + r['geom_unused'] if isinstance(g, bmesh.types.BMVert)})
        if junk:
            bmesh.ops.delete(bm, geom=junk, context='VERTS')
        tag([g for g in r['geom'] if isinstance(g, bmesh.types.BMFace) and g.is_valid], mat)

    def place(local_pts, at, rot):
        M = Matrix.Translation(at) @ rot.to_matrix().to_4x4()
        return [M @ Vector(p) for p in local_pts]

    def add_cone(M, r, depth, segs, mat):
        res = bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=depth, matrix=M)
        tag({f for vt in res['verts'] for f in vt.link_faces}, mat)

    def pick_spot():
        """bits land mostly on the piles; a few are thrown clear, breaking the outline"""
        while True:
            r = L * math.sqrt(rnd.random()); a = rnd.uniform(0, 2 * math.pi)
            x, z = r * math.cos(a), r * math.sin(a)
            h = field(x, z)
            if rnd.random() < 0.05 + (h / H) ** 0.6:
                return x, z, h

    def tone(x, z):
        """value blocks at game distance: bits of one tone cluster instead of averaging into one grey"""
        return 'light' if noise.noise(Vector((x, z, 0)) * (2.6 / L) + nseed) + rnd.uniform(-.14, .14) > 0 else 'dark'

    def spot_of(want):
        for _ in range(30):
            x, z, h = pick_spot()
            if tone(x, z) == want:
                break
        return x, z, h

    def shard(at, s, mat):
        """gravel: a low open-bottomed chip, 4-5 triangles, resting on whatever is below it"""
        rot = Euler((rnd.uniform(-.4, .4), rnd.uniform(0, 6.3), rnd.uniform(-.4, .4)))
        sides = rnd.choice((4, 5))
        base = []
        for i in range(sides):
            a = 2 * math.pi * (i + rnd.uniform(-.25, .25)) / sides
            r = s * rnd.uniform(.55, 1.1)
            base.append((r * math.cos(a), rnd.uniform(-.08, .08) * s, r * rnd.uniform(.6, 1) * math.sin(a)))
        apex = (rnd.uniform(-.3, .3) * s, rnd.uniform(.22, .5) * s, rnd.uniform(-.3, .3) * s)
        vs = [bm.verts.new(p) for p in place(base + [apex], at, rot)]
        mid = sum((vt.co for vt in vs), Vector()) / len(vs)
        faces = []
        for i in range(sides):
            f = bm.faces.new((vs[i], vs[(i + 1) % sides], vs[sides]))
            f.normal_update()
            if f.normal.dot(f.calc_center_median() - mid) < 0:
                f.normal_flip()
            faces.append(f)
        tag(faces, mat)

    def piece(at, s, mat):
        """one bigger broken bit: plate, beam, pipe, chunk, wheel or bent panel"""
        tilt = 1.0 if rnd.random() < 0.2 else 0.4       # most lie flat and cover the pile, a few stick out of it
        rot = Euler((rnd.uniform(-tilt, tilt), rnd.uniform(0, 6.3), rnd.uniform(-tilt, tilt)))
        kind = rnd.choices(KINDS, var['kinds'])[0]
        if kind == 'plate':
            w, d, t = s * rnd.uniform(1.0, 2.2), s * rnd.uniform(0.7, 1.6), 0.14 + 0.06 * s
            pts = [(a * w, b * t, c * d) for a in (-.5, .5) for b in (-.5, .5) for c in (-.5, .5)]
            pts[0] = (pts[0][0] * 0.6, pts[0][1], pts[0][2] * 0.5)          # torn corner
            add_hull(place(pts, at, rot), mat)
        elif kind == 'beam':
            l, w = s * rnd.uniform(2.0, 4.0), 0.26 + 0.1 * s
            add_hull(place([(a * w, b * w, c * l) for a in (-.5, .5) for b in (-.5, .5) for c in (-.5, .5)], at, rot), mat)
        elif kind == 'pipe':
            M = Matrix.Translation(at) @ rot.to_matrix().to_4x4()
            add_cone(M, 0.2 * s + 0.1, s * rnd.uniform(1.5, 3.0), 5, mat)
        elif kind == 'chunk':
            pts = [(rnd.uniform(-.6, .6) * s, rnd.uniform(-.4, .4) * s, rnd.uniform(-.6, .6) * s) for _ in range(7)]
            add_hull(place(pts, at, rot), mat)
        elif kind == 'wheel':
            M = Matrix.Translation(at) @ rot.to_matrix().to_4x4() @ Matrix.Rotation(math.pi / 2, 4, 'X')
            add_cone(M, 0.6 * s, 0.35 * s, 8, 'dark')
        else:  # bent panel: two plates at an angle
            w, d, t = s * 1.4, s * 1.0, 0.14 + 0.05 * s
            k = rnd.uniform(0.4, 1.1)
            p1 = [(a * w, b * t, c * d) for a in (0, 1) for b in (-.5, .5) for c in (-.5, .5)]
            p2 = [(-a * w * math.cos(k), b * t + a * w * math.sin(k), c * d) for a in (0, 1) for b in (-.5, .5) for c in (-.5, .5)]
            add_hull(place(p1, at, rot), mat); add_hull(place(p2, at, rot), mat)

    placements = []     # (bit id, source anchor, new anchor, yaw, tilt x, tilt z, scale)

    def scatter(count, unique, make_bit, size_of, lift):
        """`unique` real bits, which get texture, then re-placed copies of them that share their UVs (see add_copies).
        A heap is hundreds of near-identical shards: giving each its own island spends the whole texture on margins."""
        lib = dict(dark=[], light=[])
        for i in range(min(count, unique)):
            want = 'light' if i % 2 else 'dark'
            x, z, h = spot_of(want)
            s = size_of()
            at = Vector((x, h + rnd.uniform(*lift) * s, z))
            state['id'] += 1
            make_bit(at, s, var[want][(i // 2) % len(var[want])])
            lib[want].append((state['id'], at))
        for _ in range(count - unique):
            x, z, h = pick_spot()
            sid, src = rnd.choice(lib[tone(x, z)])
            placements.append((sid, tuple(src), (x, h + rnd.uniform(*lift) * grow, z), rnd.uniform(0, 6.3),
                               rnd.uniform(-.25, .25), rnd.uniform(-.25, .25), rnd.uniform(.85, 1.15)))

    grow = 0.75 + 0.15 * size
    # unique bits per texture (run.py: 512 up to 1x1, 1024 up to 4x4, 2048 above): past these, the 3 px island margins
    # eat more texture than the extra bits add (measured on 1x1a and 2x2a: 39 % and 53 % coverage with the 2048 counts' formula)
    uniq_shards, uniq_pieces = (12, 24) if size <= 1 else (24, 52) if size <= 4 else (24 + 8 * size, 48 + 20 * size)
    scatter(int(120 * size ** 1.4), uniq_shards, shard, lambda: rnd.uniform(.55, 1.15) * (0.8 + 0.1 * size), (-.08, .02))
    scatter(int(50 * size ** 1.4), uniq_pieces, piece, lambda: (0.35 + 0.95 * rnd.random() ** 1.8) * grow, (-.2, .3))

    me = bpy.data.meshes.new('base'); bm.to_mesh(me); bm.free()
    for m in MATS:
        me.materials.append(geom.material(m))
    ob = bpy.data.objects.new('base', me)
    bpy.context.scene.collection.objects.link(ob)
    return ob, placements


def add_copies(ob, placements):
    """After baking: add the re-placed copies. They keep their source's UVs, so they cost triangles but no texture."""
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bit = bm.faces.layers.int['bit']
    by_bit = {}
    for f in bm.faces:
        if f[bit] >= 0:
            by_bit.setdefault(f[bit], []).append(f)
    for sid, src, at, yaw, tx, tz, sc in placements:
        faces = by_bit.get(sid)
        if not faces:       # every face of this bit was culled as buried
            continue
        M = Matrix.Translation(at) @ Euler((tx, yaw, tz)).to_matrix().to_4x4() @ Matrix.Scale(sc, 4) @ Matrix.Translation(-Vector(src))
        new = bmesh.ops.duplicate(bm, geom=faces)['geom']
        bmesh.ops.transform(bm, matrix=M, verts=[g for g in new if isinstance(g, bmesh.types.BMVert)])
    bm.to_mesh(ob.data); bm.free()
