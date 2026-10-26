"""Modelling in Blender, in ENGINE coordinates: X right, Y up, Z forward (Blender axes used as-is).

A unit spec gets a `Unit` (k). k.piece(name) returns a Builder whose shape methods take GLOBAL
coordinates (use b.at(x, y, z) for coordinates relative to the piece origin). Pieces, offsets and
hierarchy come from the original 3DO so the original COB/BOS script keeps working.

Shape options shared by every shape method:
  mat      one of common.MATS
  bevel    chamfer width (0 = none); seg = bevel segments
  mirror   True -> also make a copy mirrored across global X=0 that SHARES UV space (halves texture use).
           Only on pieces whose origin has x == 0; build the +x or -x side only, never parts crossing x=0.
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from .common import MATS
from . import threedo

SHARP = math.radians(40)


def material(name):
    """the kit material slot `name`, created if missing (blends saved before a slot was added to MATS lack it)."""
    m = bpy.data.materials.get(name)
    return m if m is not None else bpy.data.materials.new(name)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for m in MATS:
        if m not in bpy.data.materials:
            bpy.data.materials.new(m)


class Builder:
    def __init__(self, unit, name):
        self.unit, self.name = unit, name
        self.org = Vector(unit.P[name])
        self.bm = bmesh.new()
        self.mir = self.bm.faces.layers.int.new('mir')       # 0 normal, 1 mirror source, 2 mirror copy

    # -- helpers --------------------------------------------------------------------------------
    def at(self, x, y, z):
        return (self.org.x + x, self.org.y + y, self.org.z + z)

    def _finish_part(self, faces, mat, bevel, seg, mirror):
        mi = MATS.index(mat)
        if mirror and abs(self.org.x) > 1e-4:
            raise ValueError(f'mirror=True on piece {self.name} whose origin x != 0; use Unit.clone(mirror_x=True)')
        faces = [f for f in faces if f.is_valid]

        def tag(fs):
            for f in fs:
                if f.is_valid:
                    f.material_index = mi
                    if mirror:
                        f[self.mir] = 1
        # tag BEFORE bevelling: bevel replaces the original faces and only copies their data to the new ones
        tag(faces)
        if bevel > 0:
            edges = list({e for f in faces for e in f.edges})
            res = bmesh.ops.bevel(self.bm, geom=edges, offset=bevel, segments=seg, profile=0.5,
                                  affect='EDGES', clamp_overlap=True)
            tag(res['faces'])

    # -- shapes ---------------------------------------------------------------------------------
    def hull(self, pts, mat='paint', bevel=0.1, seg=1, mirror=False):
        vs = [self.bm.verts.new(Vector(p) - self.org) for p in pts]
        r = bmesh.ops.convex_hull(self.bm, input=vs, use_existing_faces=False)
        junk = list({g for g in r['geom_interior'] + r['geom_unused'] if isinstance(g, bmesh.types.BMVert)})
        if junk:
            bmesh.ops.delete(self.bm, geom=junk, context='VERTS')
        faces = [g for g in r['geom'] if isinstance(g, bmesh.types.BMFace) and g.is_valid]
        r2 = bmesh.ops.dissolve_limit(self.bm, angle_limit=math.radians(1),
                                      verts=list({v for f in faces for v in f.verts}),
                                      edges=list({e for f in faces for e in f.edges}))
        # dissolve's 'region' holds only the merged faces; hull triangles it left alone must be kept too
        keep = [f for f in faces if f.is_valid] + [f for f in r2['region'] if f.is_valid]
        self._finish_part(list(dict.fromkeys(keep)), mat, bevel, seg, mirror)

    def box(self, lo, hi, mat='paint', bevel=0.08, seg=1, mirror=False):
        self.hull([(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])],
                  mat, bevel, seg, mirror)

    def prism(self, x0, x1, prof, mat='paint', bevel=0.1, seg=1, mirror=False):
        """convex side profile [(z, y), ...] extruded along X from x0 to x1"""
        self.hull([(x, y, z) for x in (x0, x1) for (z, y) in prof], mat, bevel, seg, mirror)

    def plan(self, y0, y1, poly, mat='paint', bevel=0.1, seg=1, mirror=False, top_inset=0.0):
        """convex plan outline [(x, z), ...] extruded along Y; top_inset shrinks the top face (sloped sides)"""
        c = Vector((sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly)))
        top = []
        for x, z in poly:
            v = Vector((x, z)); d = (v - c)
            v2 = v - d.normalized() * top_inset if d.length > 1e-6 else v
            top.append((v2.x, y1, v2.y))
        self.hull([(x, y0, z) for x, z in poly] + top, mat, bevel, seg, mirror)

    def cyl(self, p0, p1, r, segs=12, mat='dark', r2=None, rot=0.0, bevel=0.0, cap=True, mirror=False):
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        M = Matrix.Translation((p0 + p1) / 2 - self.org) @ q.to_matrix().to_4x4() @ Matrix.Rotation(rot, 4, 'Z')
        res = bmesh.ops.create_cone(self.bm, cap_ends=cap, cap_tris=False, segments=segs, radius1=r,
                                    radius2=(r if r2 is None else r2), depth=d.length, matrix=M)
        faces = list({f for v in res['verts'] for f in v.link_faces})
        self._finish_part(faces, mat, bevel, 1, mirror)

    def sphere(self, c, r, mat='dark', segs=10, rings=6, scale=(1, 1, 1), mirror=False):
        M = Matrix.Translation(Vector(c) - self.org) @ Matrix.Diagonal((*scale, 1))
        res = bmesh.ops.create_uvsphere(self.bm, u_segments=segs, v_segments=rings, radius=r, matrix=M)
        faces = list({f for v in res['verts'] for f in v.link_faces})
        self._finish_part(faces, mat, 0, 1, mirror)

    def from_3do(self, piece=None, mat=None, bevel=0.0):
        """Add the original 3DO polygons of a piece (blockout / first pass). mat=None guesses from TA texture names."""
        p = self.unit.T[piece or self.name]
        vs = [self.bm.verts.new(Vector(v) + Vector(self.unit.P[piece or self.name]) - self.org) for v in p['verts']]
        for q in threedo.real_faces(p):
            try:
                # 3DO: the engine negated Z, so TA winding flips; reverse to keep faces outward. S3O refs are already right.
                order = q['idx'] if p.get('src') == 's3o' else list(reversed(q['idx']))
                f = self.bm.faces.new([vs[i] for i in order])
            except ValueError:
                continue
            f.material_index = MATS.index(mat or threedo.guess_mat(q['tex']))
        bmesh.ops.remove_doubles(self.bm, verts=self.bm.verts, dist=1e-4)


class Unit:
    """Holds the 3DO reference, the builders, and turns them into Blender objects."""
    def __init__(self, ref3do, ground=True, air=False, skeleton=None, skel_opts=None):
        self.T = threedo.load_any(ref3do)
        self.skeleton, self.skel_report = skeleton, None
        if skeleton:     # standard walker hierarchy replaces the original leg pieces (see skeleton.py)
            from . import skeleton as SK
            self.T, self.skel_report = SK.remap(self.T, skeleton, **(skel_opts or {}))
        self.P = {n: Vector(p['gpos']) for n, p in self.T.items()}
        self.builders, self.clones = {}, {}
        self.ground, self.air = ground, air
        self.objs = {}

    def piece(self, name):
        if name not in self.T:
            raise KeyError(f'{name} is not a piece of the 3DO: {list(self.T)}')
        if name not in self.builders:
            self.builders[name] = Builder(self, name)
        return self.builders[name]

    def standard_legs(self, thigh='paint', shin='paint2', foot='dark', joint='dark', width=1.4, armour=True):
        """Federation-style backwards legs on the standard skeleton. Builds the right-front leg once; every other
        leg is a clone (mirrored for the left side), so all legs share one set of UVs."""
        from .skeleton import LEGS
        ids = LEGS[self.skeleton]
        H = self.P['pelvis'].y
        w = 0.11 * H * width
        src = ids[0]                                   # 'r' or 'rf'
        t = self.piece(src + 'thigh'); A = t.at
        kn = Vector(self.T[src + 'leg']['off'])         # knee, relative to the hip
        t.cyl(A(-1.25 * w, 0, 0), A(1.25 * w, 0, 0), 0.13 * H, 10, joint, bevel=0.03 * H)
        def across(p0, p1, r0, r1):
            """4 (y, z) points: a bone from p0 to p1 with half-depth r0 at p0 and r1 at p1, measured PERPENDICULAR to
            the bone in the side view (offsets along the bone made the first walkers' shins paper-thin struts)."""
            dy, dz = p1[0] - p0[0], p1[1] - p0[1]
            n = (dy * dy + dz * dz) ** 0.5 or 1.0
            ny, nz = -dz / n, dy / n
            return [(p0[0] + ny * r0, p0[1] + nz * r0), (p0[0] - ny * r0, p0[1] - nz * r0),
                    (p1[0] + ny * r1, p1[1] + nz * r1), (p1[0] - ny * r1, p1[1] - nz * r1)]
        t.hull([A(x, y, z) for x in (-w, w) for (y, z) in across((0.0, 0.0), (kn.y, kn.z), 0.11 * H, 0.08 * H)],
               thigh, bevel=0.025 * H)
        if armour:   # outer armour plate: big readable shape from above
            t.hull([A(x, y, z) for x in (-1.15 * w, -0.85 * w) for (y, z) in
                    [(0.1 * H, 0.12 * H), (0.02 * H, -0.16 * H), (kn.y * 0.55, kn.z * 0.75), (kn.y * 0.45, kn.z * 0.2)]],
                   thigh, bevel=0.015 * H)
        l = self.piece(src + 'leg'); B = l.at
        an = Vector(self.T[src + 'foot']['off'])        # ankle, relative to the knee
        l.cyl(B(-1.1 * w, 0, 0), B(1.1 * w, 0, 0), 0.1 * H, 10, joint, bevel=0.02 * H)
        l.hull([B(x, y, z) for x in (-0.85 * w, 0.85 * w) for (y, z) in across((0.0, 0.0), (an.y, an.z), 0.085 * H, 0.06 * H)],
               shin, bevel=0.025 * H)
        f = self.piece(src + 'foot'); C = f.at
        g = -self.T[src + 'foot']['gpos'][1]            # ground, relative to the ankle
        f.cyl(C(-0.9 * w, 0, 0), C(0.9 * w, 0, 0), 0.07 * H, 8, joint)
        f.hull([C(x, y, z) for x in (-1.3 * w, 1.3 * w) for (y, z) in
                [(0.03 * H, -0.08 * H), (0.03 * H, 0.1 * H), (g + 0.02 * H, 0.38 * H), (g, 0.3 * H), (g, -0.26 * H), (g + 0.05 * H, -0.28 * H)]],
               foot, bevel=0.02 * H)
        for i in ids[1:]:
            mx = i.startswith('l')
            for part in ('thigh', 'leg', 'foot'):
                self.clone(i + part, src + part, mirror_x=mx)

    def clone(self, name, of, mirror_x=False):
        """piece `name` reuses piece `of`'s geometry AND UVs (local coords), optionally mirrored in local X."""
        self.clones[name] = (of, mirror_x)

    # ------------------------------------------------------------------------------------------
    def realize(self):
        """Create objects for all pieces (empty pieces become empties)."""
        for name in self.T:
            if name in self.builders:
                bm = self.builders[name].bm
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
                me = bpy.data.meshes.new(name)
                bm.to_mesh(me); bm.free()
                for m in MATS:
                    me.materials.append(material(m))
                ob = bpy.data.objects.new(name, me)
            else:
                ob = bpy.data.objects.new(name, None)
            ob.location = self.P[name]
            bpy.context.scene.collection.objects.link(ob)
            self.objs[name] = ob
        return self.objs


# ============================================================== visibility, UVs, mirroring
def _hemi_dirs(n, count=48):
    import random
    rnd = random.Random(1)
    t = n.orthogonal().normalized(); b = n.cross(t)
    out = []
    for i in range(count):
        u, v = (i + 0.5) / count, rnd.random()
        r = math.sqrt(u); th = 2 * math.pi * v
        out.append((t * (r * math.cos(th)) + b * (r * math.sin(th)) + n * math.sqrt(max(0, 1 - u))).normalized())
    return out


def _world_polys(objs):
    verts, polys, owner = [], [], []
    for ob in objs:
        me = ob.data; base = len(verts); M = ob.matrix_world
        verts += [M @ v.co for v in me.vertices]
        for p in me.polygons:
            polys.append([base + i for i in p.vertices]); owner.append(ob.name)
    return verts, polys, owner


def visibility_cull(objs, ground=True, air=False, rays=48, interior_thresh=0.7, protect=('ash',)):
    """Delete faces buried inside their own piece's solids (and ground-contact undersides for land units).
    Returns {obj: {face_index_after: exposure}} via a 'expo' float face attribute."""
    vtx, polys, owner = _world_polys(objs)
    whole = BVHTree.FromPolygons(vtx, polys)
    stats = {}
    for ob in objs:
        me = ob.data; M = ob.matrix_world
        self_bvh = BVHTree.FromPolygons([M @ v.co for v in me.vertices], [list(p.vertices) for p in me.polygons])
        bm = bmesh.new(); bm.from_mesh(me)
        expo = bm.faces.layers.float.get('expo') or bm.faces.layers.float.new('expo')
        kill = []
        for f in bm.faces:
            c = M @ f.calc_center_median(); n = (M.to_3x3() @ f.normal).normalized()
            if n.length < 0.5:
                continue
            o = c + n * 0.02
            dirs = _hemi_dirs(n, rays)
            esc = back = 0
            for d in dirs:
                hit = self_bvh.ray_cast(o, d, 1000)
                if hit[0] is not None and hit[1].dot(d) > 0:
                    back += 1
            for d in dirs:
                hit = whole.ray_cast(o, d, 1000)
                if hit[0] is None:
                    # rays heading below the ground plane don't count as visible for land units
                    if ground and not air and d.y < -0.05 and o.y < 40:
                        continue
                    esc += 1
            e = esc / len(dirs)
            f[expo] = e
            if back / len(dirs) > interior_thresh and MATS[f.material_index] not in protect:
                # confirm at points near every corner: a big face whose centre happens to sit inside
                # a small part must survive; only faces buried everywhere are deleted
                buried = True
                for v in f.verts:
                    p = M @ (f.calc_center_median().lerp(v.co, 0.85)) + n * 0.02
                    b2 = sum(1 for d in dirs[::3] if (h := self_bvh.ray_cast(p, d, 1000))[0] is not None and h[1].dot(d) > 0)
                    if b2 / len(dirs[::3]) <= interior_thresh:
                        buried = False; break
                if buried:
                    kill.append(f)
            elif ground and not air and n.y < -0.95 and c.y < 0.35:
                kill.append(f)          # flat underside sitting on the ground
        stats[ob.name] = (len(bm.faces), len(kill))
        if kill:
            bmesh.ops.delete(bm, geom=kill, context='FACES')
        bm.to_mesh(me); bm.free()
    return stats


def _islands(bm, uv):
    parent = {f.index: f.index for f in bm.faces}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for e in bm.edges:
        if len(e.link_faces) != 2:
            continue
        f1, f2 = e.link_faces
        def uvs(f):
            return {l.vert.index: l[uv].uv.copy() for l in f.loops if l.vert in e.verts}
        a, b = uvs(f1), uvs(f2)
        if all((a[k] - b[k]).length < 1e-6 for k in a):
            parent[find(f1.index)] = find(f2.index)
    groups = {}
    for f in bm.faces:
        groups.setdefault(find(f.index), []).append(f)
    return list(groups.values())


def _min_rect_area(pts):
    best = None
    for k in range(0, 90, 5):
        a = math.radians(k); c, s_ = math.cos(a), math.sin(a)
        xs = [p.x * c - p.y * s_ for p in pts]; ys = [p.x * s_ + p.y * c for p in pts]
        ar = (max(xs) - min(xs)) * (max(ys) - min(ys))
        best = ar if best is None or ar < best else best
    return best or 1e-12


def _uv_area(f, uv):
    p = [l[uv].uv for l in f.loops]
    return sum(abs((p[i] - p[0]).cross(p[i + 1] - p[0])) / 2 for i in range(1, len(p) - 1))


def split_poor_islands(bm, uv, fill_min=0.45):
    """Islands that waste space (rings of chamfers, slivers) are cut into per-face islands, each laid flat
    along its longest edge at the same texel density. The packer then nests them tightly."""
    n_split = 0
    for isl in _islands(bm, uv):
        if len(isl) < 2:
            continue
        a_uv = sum(_uv_area(f, uv) for f in isl)
        rect = _min_rect_area([l[uv].uv for f in isl for l in f.loops])
        if a_uv / rect >= fill_min:
            continue
        a_3d = sum(f.calc_area() for f in isl) or 1e-12
        k = math.sqrt(a_uv / a_3d)                       # uv units per world unit
        cen = sum((l[uv].uv for f in isl for l in f.loops), Vector((0, 0))) / sum(len(f.loops) for f in isl)
        for f in isl:
            e = max(f.edges, key=lambda e: e.calc_length())
            ax = (e.verts[1].co - e.verts[0].co).normalized()
            ay = f.normal.cross(ax).normalized()
            o = f.loops[0].vert.co
            for l in f.loops:
                d = l.vert.co - o
                l[uv].uv = cen + Vector((d.dot(ax), d.dot(ay))) * k
        n_split += 1
    return n_split


PACK_FILL = 0.68      # typical packed fraction, used to predict pixel sizes before packing
MIN_PX = 6            # an island's longest side must reach this many texels at the final resolution
MIN_PX_THIN = 2.5     # and its shortest side this many (thin chamfer strips)


def _scale_island(isl, uv, s):
    cen = sum((l[uv].uv for f in isl for l in f.loops), Vector((0, 0))) / sum(len(f.loops) for f in isl)
    for f in isl:
        for l in f.loops:
            l[uv].uv = cen + (l[uv].uv - cen) * s


IMPORTANCE = {'tread': 0.6, 'tread2': 0.6, 'tread3': 0.6, 'tread4': 0.6, 'black': 0.4, 'ash': 0.7, 'team': 1.0, 'lightw': 0.8, 'lightc': 0.8, 'lightr': 0.8}


def unwrap(objs, margin_px=3, res=1024, angle=55, ground=True, air=False, water=None):
    """Smart project -> uniform texel density -> shrink islands by visibility/importance -> tight pack.
    Faces tagged as mirror copies (mir==2) must not exist yet; mirrors are added after this.
    water: for ships, the model-space height of the water surface (= unitdef waterline). Islands below it and
    downward-facing islands get less texture (only seen through water, or never); None for land/air units."""
    meshes = [o for o in objs if o.type == 'MESH' and len(o.data.polygons)]
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=0.0, area_weight=0.0,
                             correct_aspect=True, scale_to_bounds=False)
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode='OBJECT')
    # split wasteful islands, then importance scaling per island
    bms = {}
    for o in meshes:
        bm = bmesh.new(); bm.from_mesh(o.data)
        uv = bm.loops.layers.uv.active
        split_poor_islands(bm, uv)
        expo = bm.faces.layers.float.get('expo')
        bm.faces.ensure_lookup_table()
        isls = []
        for isl in _islands(bm, uv):
            area = sum(f.calc_area() for f in isl) or 1e-9
            e = sum((f[expo] if expo else 1.0) * f.calc_area() for f in isl) / area
            down = sum(f.calc_area() for f in isl if f.normal.y < -0.7) / area
            mat = MATS[isl[0].material_index]
            k = (0.15 + 0.85 * min(1.0, e * 1.6) ** 0.8) * IMPORTANCE.get(mat, 1.0)
            if ground and not air:
                k *= (1 - 0.6 * down)
            elif water is not None:
                M = o.matrix_world
                sub = sum(f.calc_area() for f in isl if (M @ f.calc_center_median()).y < water - 0.5) / area
                k *= (1 - 0.5 * sub) * (1 - 0.5 * down)
            _scale_island(isl, uv, math.sqrt(max(k, 0.06)))
            isls.append(isl)
        bms[o] = (bm, uv, isls)
    # minimum island size: an island smaller than a few texels gets no baked texels of its own and
    # samples its neighbours' colours. Predict the packer's scale and grow islands below MIN_PX.
    total = sum(_uv_area(f, uv) for bm, uv, isls in bms.values() for isl in isls for f in isl) or 1e-9
    fscale = math.sqrt(PACK_FILL / total) * res
    for bm, uv, isls in bms.values():
        for isl in isls:
            pts = [l[uv].uv for f in isl for l in f.loops]
            side = min(max(p.x for p in pts) - min(p.x for p in pts), max(p.y for p in pts) - min(p.y for p in pts))
            big = max(max(p.x for p in pts) - min(p.x for p in pts), max(p.y for p in pts) - min(p.y for p in pts))
            px_small, px_big = side * fscale, big * fscale
            if px_big < MIN_PX:
                _scale_island(isl, uv, MIN_PX / max(px_big, 1e-6))
            elif px_small < MIN_PX_THIN:
                _scale_island(isl, uv, min(MIN_PX_THIN / max(px_small, 1e-6), 3.0))
    for o, (bm, uv, isls) in bms.items():
        bm.to_mesh(o.data); bm.free()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM', rotate=True, rotate_method='ANY', scale=True,
                            merge_overlap=False, margin_method='FRACTION', margin=margin_px / res,
                            shape_method='CONCAVE')
    bpy.ops.object.mode_set(mode='OBJECT')


def add_mirrors(objs):
    for o in objs:
        if o.type != 'MESH':
            continue
        bm = bmesh.new(); bm.from_mesh(o.data)
        mir = bm.faces.layers.int.get('mir')
        src = [f for f in bm.faces if mir and f[mir] == 1]
        if src:
            r = bmesh.ops.duplicate(bm, geom=src)
            nv = [g for g in r['geom'] if isinstance(g, bmesh.types.BMVert)]
            nf = [g for g in r['geom'] if isinstance(g, bmesh.types.BMFace)]
            for v in nv:
                v.co.x = -v.co.x
            bmesh.ops.reverse_faces(bm, faces=nf, flip_multires=False)
            for f in nf:
                f[mir] = 2
        bm.to_mesh(o.data); bm.free()


def apply_clones(unit):
    for name, (of, mx) in unit.clones.items():
        src = unit.objs[of]
        me = src.data.copy(); me.name = name
        if mx:
            bm = bmesh.new(); bm.from_mesh(me)
            for v in bm.verts:
                v.co.x = -v.co.x
            bmesh.ops.reverse_faces(bm, faces=bm.faces[:], flip_multires=False)
            bm.to_mesh(me); bm.free()
        old = unit.objs[name]
        ob = bpy.data.objects.new(name + '_tmp', me)
        ob.location = old.location
        bpy.context.scene.collection.objects.link(ob)
        bpy.data.objects.remove(old)
        ob.name = name
        unit.objs[name] = ob


def finalize_shading(objs):
    for o in objs:
        if o.type != 'MESH':
            continue
        bm = bmesh.new(); bm.from_mesh(o.data)
        for f in bm.faces:
            f.smooth = True
        for e in bm.edges:
            e.smooth = len(e.link_faces) == 2 and e.calc_face_angle(0) < SHARP
        bm.to_mesh(o.data); bm.free()
        if not any(m.type == 'WEIGHTED_NORMAL' for m in o.modifiers):
            wn = o.modifiers.new('wn', 'WEIGHTED_NORMAL'); wn.keep_sharp = True; wn.mode = 'FACE_AREA'


def uv_report(objs, res=512, save=None):
    """Fraction of the texture covered by UVs (overlaps counted once) and triangle count."""
    import numpy as np
    from PIL import Image, ImageDraw
    img = Image.new('L', (res, res), 0); dr = ImageDraw.Draw(img)
    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type != 'MESH':
            continue
        me = o.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
        uv = me.uv_layers.active.uv
        for t in me.loop_triangles:
            dr.polygon([(uv[l].vector.x * res, (1 - uv[l].vector.y) * res) for l in t.loops], fill=255)
        tris += len(me.loop_triangles)
    a = np.array(img)
    if save:
        img.save(save)
    return dict(uv_coverage=round(float((a > 0).mean()), 3), tris=tris)
