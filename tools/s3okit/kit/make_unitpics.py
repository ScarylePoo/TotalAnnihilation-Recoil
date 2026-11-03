#!/usr/bin/env python3
"""Unit pictures: render every unit's installed S3O + DDS at TA's 3/4 angle over the enhanced backgrounds in unitpic_bg/.
  python3 make_unitpics.py [--out DIR] [--jobs N] [--samples N] [stem ...]     (no stems = every unit; default out = ../../../unitpics, name <stem>.png)
Background choice: the one the unit's old TA picture used (unitpic_bg/old_match.json, found by matching pixels) unless it contradicts what the unit is;
otherwise by class, with a stable pick per unit. Aircraft on Air, submarines and underwater buildings on Underwater, ships, hovers and floating buildings on Sea."""
import argparse, glob, hashlib, json, math, os, re, subprocess, sys, tempfile
KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
BG = os.path.join(KIT, 'unitpic_bg')
REPO = os.path.abspath(os.path.join(KIT, '..', '..', '..'))
TEAM = {'ARM': '2255dd', 'CORE': 'cc2a14'}
VARIANTS = {k: sorted(os.path.basename(f)[:-4] for f in glob.glob(os.path.join(BG, k + '_*.png')))
            for k in ('Air', 'Desert', 'Green', 'Ground', 'Moon', 'Sea', 'Underwater')}


def kind_of(stem):
    """'air' | 'sub' | 'uwbuild' | 'sea' | 'land' from the file name and def"""
    t = open(os.path.join(REPO, 'units', stem + '.lua'), errors='ignore').read()
    c = stem.split('_')[2] if stem.count('_') >= 2 else ''
    if re.search(r'canfly\s*=\s*"?1', t, re.I) or c in ('AIR', 'SEAPL'):
        return 'air'
    if 'SUBMARINE' in t.upper():
        return 'sub'
    if c in ('SEA', 'HOV') or 'FloatingDragon' in stem or 'Shipyard' in stem or 'SeaplanePlatform' in stem or 'HovercraftPlatform' in stem:
        return 'sea'
    if c in ('SEADEF', 'SEAECO'):
        return 'uwbuild' if re.search(r'UW|Tidal|TorpedoLauncher', stem) else 'sea'
    return 'land'


def background(stem):
    kind = kind_of(stem)
    old = json.load(open(os.path.join(BG, 'old_match.json'))).get(stem) or [None, 0]
    m = old[0].replace(' ', '_') if old[0] and old[1] >= 0.15 else None
    fam = m.split('_')[0] if m else None
    ok = {'air': ('Air',), 'sub': ('Underwater',), 'uwbuild': ('Underwater',), 'sea': ('Sea',),
          'land': ('Green', 'Ground', 'Moon', 'Desert', 'Sea', 'Underwater')}[kind]     # amphibious land units may keep a water picture
    if fam in ok:
        return m
    pool = sum((VARIANTS[f] for f in {'air': ['Air'], 'sub': ['Underwater'], 'uwbuild': ['Underwater'], 'sea': ['Sea'],
                                       'land': ['Green', 'Ground']}[kind]), [])
    return pool[int(hashlib.md5(stem.encode()).hexdigest(), 16) % len(pool)]


def render_one(stem, out, samples):
    import bpy
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Euler, Vector
    import numpy as np
    from PIL import Image
    from s3okit import s3o as S3O
    from s3okit.preview import _srgb
    import run as RUN
    _, U, info = RUN.load_spec(stem)
    kind = kind_of(stem)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    m = S3O.read(os.path.join(REPO, 'objects3d', stem + '.s3o'))
    tmp = tempfile.mkdtemp()
    def tex(name):           # the shipped DDS, decoded top row first (same orientation as compose's PNG)
        p = os.path.join(tmp, name + '.png')
        Image.open(os.path.join(REPO, 'unittextures', name + '.dds')).convert('RGBA').save(p)
        return bpy.data.images.load(p)
    mat = bpy.data.materials.new('s3o'); mat.use_nodes = True
    nt = mat.node_tree; N = nt.nodes; L = nt.links
    bsdf = N['Principled BSDF']
    i1 = N.new('ShaderNodeTexImage'); i1.image = tex(stem + '_1'); i1.image.alpha_mode = 'CHANNEL_PACKED'
    i2 = N.new('ShaderNodeTexImage'); i2.image = tex(stem + '_2'); i2.image.colorspace_settings.name = 'Non-Color'
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    A = [s for s in mix.inputs if s.name == 'A' and s.type == 'RGBA'][0]
    B = [s for s in mix.inputs if s.name == 'B' and s.type == 'RGBA'][0]
    R = [s for s in mix.outputs if s.type == 'RGBA'][0]
    L.new(i1.outputs['Color'], A); B.default_value = _srgb(TEAM.get(stem.split('_')[0], '2255dd'))
    L.new(i1.outputs['Alpha'], mix.inputs['Factor']); L.new(R, bsdf.inputs['Base Color'])
    sep = N.new('ShaderNodeSeparateColor'); L.new(i2.outputs['Color'], sep.inputs[0])
    rough = N.new('ShaderNodeMath'); rough.operation = 'MULTIPLY_ADD'
    rough.inputs[1].default_value = -1.2; rough.inputs[2].default_value = 0.85
    L.new(sep.outputs[1], rough.inputs[0]); L.new(rough.outputs[0], bsdf.inputs['Roughness'])
    L.new(R, bsdf.inputs['Emission Color'])
    em = N.new('ShaderNodeMath'); em.operation = 'MULTIPLY'; em.inputs[1].default_value = 5.0
    L.new(sep.outputs[0], em.inputs[0]); L.new(em.outputs[0], bsdf.inputs['Emission Strength'])
    objs = {}
    for p in m['pieces']:
        V, I = p['verts'], p['idx']
        me = bpy.data.meshes.new(p['name'])
        if I:
            used = sorted(set(I)); remap = {o: n for n, o in enumerate(used)}
            me.from_pydata([V[i][:3] for i in used], [], [[remap[i] for i in I[k:k + 3]] for k in range(0, len(I), 3)])
            uvl = me.uv_layers.new()
            for li, lp in enumerate(me.loops):
                v = V[used[lp.vertex_index]]; uvl.data[li].uv = (v[6], v[7])
            me.normals_split_custom_set([V[used[lp.vertex_index]][3:6] for lp in me.loops])
            me.materials.append(mat)
        ob = bpy.data.objects.new(p['name'], me if I else None)
        sc.collection.objects.link(ob)
        if p['parent']:
            ob.parent = objs[p['parent'].lower()]
        ob.location = p['off']
        objs[p['name'].lower()] = ob
    for name, rot in (U.get('preview_pose') or {}).items():
        o = objs.get(name.lower())
        if not o:
            continue
        if rot == 'hide':
            o.hide_render = True; o['hidden'] = 1
        elif isinstance(rot, dict):
            o.location = Vector(o.location) + Vector(rot.get('move', (0, 0, 0)))
            o.rotation_euler = Euler([math.radians(a) for a in rot.get('rot', (0, 0, 0))])
        else:
            o.rotation_euler = Euler([math.radians(a) for a in rot])
    bpy.context.view_layer.update()
    # the model's posed vertices (above the waterline for surface units: that is what shows)
    water = None
    if kind == 'sea' and stem.split('_')[2] == 'SEA':
        water = float(U.get('water') or 0)     # ships only: water surface height in model space. Sea buildings and docks stay whole, most of them sit below it
    pts = []
    for o in objs.values():
        if o.type == 'MESH' and len(o.data.vertices) and not o.hide_render:
            mw = o.matrix_world
            pts += [mw @ v.co for v in o.data.vertices]
    if water is not None:
        above = [p for p in pts if p.y >= water]
        pts = above or pts
    lo = Vector((min(p[i] for p in pts) for i in range(3))); hi = Vector((max(p[i] for p in pts) for i in range(3)))
    ctr = (lo + hi) / 2; rad = (hi - lo).length / 2
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.cycles.device = 'CPU'; sc.render.threads = int(os.environ.get('PIC_THREADS', '6'))
    sc.view_settings.view_transform = 'Standard'; sc.render.film_transparent = True
    SIZE = 512
    sc.render.resolution_x = sc.render.resolution_y = SIZE
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 3.6; sun.data.angle = math.radians(4)
    sun.matrix_world = Vector((-0.45, 1.0, 0.5)).normalized().to_track_quat('Z', 'X').to_matrix().to_4x4()
    sc.collection.objects.link(sun)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.75, 0.8, 0.9, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.75
    # ground/water plane: shadow catcher for what sits on something; holdout at the waterline hides a ship's hull below water
    plane_y = None
    # (not at y = 0 under a dock or sea building: it would hide everything below the surface)
    if kind in ('land', 'uwbuild') or (kind == 'sea' and water is None and lo.y > -2):
        plane_y = 0.0 if kind != 'uwbuild' else min(0.0, lo.y)
    if plane_y is not None:
        bpy.ops.mesh.primitive_plane_add(size=rad * 40 + 400, location=(0, plane_y - 0.02, 0), rotation=(-math.pi / 2, 0, 0))
        bpy.context.object.is_shadow_catcher = True
    if water is not None:
        bpy.ops.mesh.primitive_plane_add(size=rad * 40 + 400, location=(0, water, 0), rotation=(-math.pi / 2, 0, 0))
        hold = bpy.data.materials.new('hold'); hold.use_nodes = True
        hn = hold.node_tree.nodes; hn.clear()
        ho = hn.new('ShaderNodeOutputMaterial'); hh = hn.new('ShaderNodeHoldout'); hold.node_tree.links.new(hh.outputs[0], ho.inputs[0])
        bpy.context.object.data.materials.append(hold)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.lens = 60; cam.data.clip_end = 20000; cam.data.sensor_width = 36
    def look_at(pos, tgt):      # the model's up is engine Y, not Blender's Z
        from mathutils import Matrix
        z = (pos - tgt).normalized(); x = Vector((0, 1, 0)).cross(z).normalized(); y = z.cross(x)
        return Matrix(((x.x, y.x, z.x, pos.x), (x.y, y.y, z.y, pos.y), (x.z, y.z, z.z, pos.z), (0, 0, 0, 1)))
    dirn = Vector((0.62, 0.62, 0.78)).normalized()     # nose toward the lower left, like TA's pictures
    fill = 0.84
    dist = rad * 4
    for _ in range(4):
        cam.location = ctr + dirn * dist
        cam.matrix_world = look_at(cam.location, ctr)
        bpy.context.view_layer.update()
        q = [world_to_camera_view(sc, cam, p) for p in pts]
        ex = max(max(v.x for v in q) - min(v.x for v in q), max(v.y for v in q) - min(v.y for v in q))
        dist *= ex / fill
    cam.location = ctr + dirn * dist
    cam.matrix_world = look_at(cam.location, ctr)
    bpy.context.view_layer.update()
    q = [world_to_camera_view(sc, cam, p) for p in pts]
    cx = (max(v.x for v in q) + min(v.x for v in q)) / 2; cy = (max(v.y for v in q) + min(v.y for v in q)) / 2
    aim = 0.5 if kind in ('air', 'sub') else 0.44      # a little below centre: the backgrounds' horizon sits high
    cam.data.shift_x = cx - 0.5; cam.data.shift_y = cy - aim
    f = os.path.join(tmp, 'unit.png'); sc.render.filepath = f
    bpy.ops.render.render(write_still=True)
    fg = np.array(Image.open(f).convert('RGBA'), dtype=np.float32) / 255
    fg[..., :3] *= fg[..., 3:]            # premultiply so the downscale has no halo
    if kind in ('sub', 'uwbuild'):
        fg[..., :3] *= np.array((0.86, 0.93, 1.06), dtype=np.float32)      # seen through water
    def down(c):
        return np.array(Image.fromarray(c).resize((256, 256), Image.LANCZOS))
    fg2 = np.stack([down(fg[..., i]) for i in range(4)], -1).clip(0, 1)
    name = background(stem)
    bg = np.array(Image.open(os.path.join(BG, name + '.png')).convert('RGB'), dtype=np.float32) / 255
    res = fg2[..., :3] + bg * (1 - fg2[..., 3:])
    Image.fromarray((res.clip(0, 1) * 255 + .5).astype('uint8')).save(os.path.join(out, stem + '.png'), optimize=True)
    print('PIC', stem, kind, name, flush=True)


def main():
    a = argparse.ArgumentParser(); a.add_argument('--out', default=os.path.join(REPO, 'unitpics')); a.add_argument('--jobs', type=int, default=6)
    a.add_argument('--samples', type=int, default=48); a.add_argument('--worker', action='store_true'); a.add_argument('stems', nargs='*')
    o = a.parse_args()
    if o.worker:
        for s in o.stems:
            try:
                render_one(s, o.out, o.samples)
            except Exception as e:              # one bad unit must not lose the rest of this worker's list
                print('FAILED', s, repr(e), flush=True)
        return
    stems = o.stems or sorted(os.path.basename(f)[:-4] for f in glob.glob(os.path.join(REPO, 'units', '*.lua')))
    os.makedirs(o.out, exist_ok=True)
    procs = []
    for i in range(o.jobs):
        part = stems[i::o.jobs]
        if part:
            procs.append(subprocess.Popen([sys.executable, __file__, '--worker', '--out', o.out, '--samples', str(o.samples)] + part,
                                          env=dict(os.environ, PIC_THREADS=str(max(2, 30 // o.jobs))), stdout=sys.stdout, stderr=subprocess.DEVNULL))
    sys.exit(max(p.wait() for p in procs))


if __name__ == '__main__':
    main()
