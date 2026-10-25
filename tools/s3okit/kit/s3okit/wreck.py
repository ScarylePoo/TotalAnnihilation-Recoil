"""Wrecks: derive <corpse>.s3o from the built unit (same UV layout, own bake, burnt texture).
Level 1 = the normal corpse (recognisable). Level 2 = unit-specific second stage (xxx_dead2): much more broken.
Generic heaps (NxNa etc.) are made by heap.py instead."""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler, noise
from .common import MATS
from . import geom

LEVELS = {1: dict(remove=0.18, jitter=10, crumple=0.18, dents=6, dent_depth=0.5, holes=2, hole_r=1.2, sink=0.5, tilt=3),
          2: dict(remove=0.5, jitter=25, crumple=0.35, dents=14, dent_depth=0.9, holes=6, hole_r=2.0, sink=1.4, tilt=7)}


def make(unit_T, objs, level=1, seed=1, pose=None, drop=(), remove=()):
    """objs: piece name -> object in the unit scene (UV'd, built). Returns the new single 'base' object."""
    L = LEVELS[level]; rnd = random.Random(seed)
    # 1. rebuild the hierarchy so posing a parent carries children
    for n, t in unit_T.items():
        ob = objs.get(n)
        if ob is None:
            continue
        par = objs.get(t['parent']) if t['parent'] else None
        if par is not None:
            mw = ob.matrix_world.copy(); ob.parent = par; ob.matrix_world = mw
    pose = dict(pose or {})
    for n in unit_T:
        if n not in pose and any(k in n.lower() for k in ('turret', 'head', 'torso')):
            pose[n] = (0, rnd.uniform(-60, 60), 0)
        if n not in pose and any(k in n.lower() for k in ('sleeve', 'gun', 'barrel', 'arm')):
            pose[n] = (rnd.uniform(-5, 20), 0, 0)
    for n, r in pose.items():
        if n in objs:
            objs[n].rotation_euler = Euler([math.radians(a) for a in r])
    bpy.context.view_layer.update()
    # 2. bake transforms into one mesh
    meshes = []
    for n, ob in objs.items():
        if ob.type != 'MESH' or not len(ob.data.polygons) or n in remove:
            continue
        me = ob.data.copy(); me.transform(ob.matrix_world)
        if n in drop:   # lay detached pieces on the ground beside the hull
            bb = [v.co for v in me.vertices]
            c = sum(bb, Vector()) / len(bb)
            ang = rnd.uniform(0, 2 * math.pi)
            M = (Matrix.Translation(Vector((math.cos(ang) * 6, 0.3 - min(v.y for v in bb), math.sin(ang) * 6)) + Vector((c.x, 0, c.z)))
                 @ Matrix.Rotation(rnd.uniform(0, 6.28), 4, 'Y') @ Matrix.Rotation(math.radians(rnd.uniform(70, 100)), 4, 'Z')
                 @ Matrix.Translation(-c))
            me.transform(M)
        meshes.append(me)
    bm = bmesh.new()
    for me in meshes:
        bm.from_mesh(me)
    # 3. loose parts: remove some small ones, jitter the rest
    bm.faces.ensure_lookup_table()
    seen, parts = set(), []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, comp = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index); stack.append(h)
        parts.append(comp)
    big = max(sum(f.calc_area() for f in p) for p in parts)
    kill = []
    for p in parts:
        area = sum(f.calc_area() for f in p)
        verts = list({v for f in p for v in f.verts})
        if area < big * 0.04 and rnd.random() < L['remove']:
            kill += p; continue
        if area < big * 0.3:
            c = sum((v.co for v in verts), Vector()) / len(verts)
            R = Euler([math.radians(rnd.uniform(-L['jitter'], L['jitter'])) for _ in range(3)]).to_matrix()
            dy = -rnd.uniform(0, L['sink'])
            for v in verts:
                v.co = c + R @ (v.co - c) + Vector((0, dy, 0))
    if kill:
        bmesh.ops.delete(bm, geom=list(set(kill)), context='FACES')
    # 4. crumple, dents, holes
    off = Vector((rnd.random() * 100, rnd.random() * 100, rnd.random() * 100))
    for v in bm.verts:
        v.co += noise.noise_vector(v.co * 0.35 + off) * L['crumple']
    pts = [v.co.copy() for v in bm.verts]
    for _ in range(L['dents']):
        c = rnd.choice(pts); r = rnd.uniform(1.0, 2.5); depth = L['dent_depth'] * rnd.uniform(0.5, 1.0)
        for v in bm.verts:
            d = (v.co - c).length
            if d < r:
                v.co.y -= depth * (1 - d / r) ** 2
    bm.faces.ensure_lookup_table()
    for _ in range(L['holes']):
        c = rnd.choice(pts); r = L['hole_r'] * rnd.uniform(0.6, 1.0)
        dead = [f for f in bm.faces if f.is_valid and (f.calc_center_median() - c).length < r and f.calc_area() < 6]
        if dead:
            bmesh.ops.delete(bm, geom=dead, context='FACES')
    # 5. settle: tilt + sink
    T = Euler((math.radians(rnd.uniform(-L['tilt'], L['tilt'])), 0, math.radians(rnd.uniform(-L['tilt'], L['tilt'])))).to_matrix()
    for v in bm.verts:
        v.co = T @ v.co - Vector((0, L['sink'] * 0.5, 0))
    me = bpy.data.meshes.new('base'); bm.to_mesh(me); bm.free()
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    if not me.materials:
        for m in MATS:
            me.materials.append(bpy.data.materials[m])
    ob = bpy.data.objects.new('base', me)
    bpy.context.scene.collection.objects.link(ob)
    geom.finalize_shading([ob])
    return ob
