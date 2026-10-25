"""Render an S3O (read back with our own reader, i.e. what the engine will get) with its textures.
Approximates the engine shader: base = mix(tex1.rgb, team, tex1.a); emission from tex2.r; gloss from tex2.g.
Also renders an RTS-height 'readability' thumbnail (small, colour + greyscale) to judge shape/contrast."""
import bpy, math, os
from mathutils import Vector, Matrix, Euler
from . import s3o as S3O

VIEWS = {'front34': ((-34, 30, 50), (0, 4.5, 0), 70), 'rear34': ((40, 32, -46), (0, 4.5, 0), 70),
         'side': ((-70, 12, 2), (0, 5, 0), 70), 'top': ((0.01, 75, 8), (0, 4, 0), 70),
         'rts': ((-20, 110, 75), (0, 3, 0), 120), 'close': ((-14, 16, 22), (-1, 7, -3), 70)}


def _srgb(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]


def render(path, texdir, prefix, team='2255dd', pose=None, views=('front34', 'rear34', 'side', 'rts'),
           samples=32, size=(900, 650), thumb=True):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    m = S3O.read(path)
    mat = bpy.data.materials.new('s3o'); mat.use_nodes = True
    nt = mat.node_tree; N = nt.nodes; L = nt.links
    bsdf = N['Principled BSDF']
    i1 = N.new('ShaderNodeTexImage'); i1.image = bpy.data.images.load(os.path.join(texdir, m['tex1']))
    i1.image.alpha_mode = 'CHANNEL_PACKED'
    i2 = N.new('ShaderNodeTexImage'); i2.image = bpy.data.images.load(os.path.join(texdir, m['tex2']))
    i2.image.colorspace_settings.name = 'Non-Color'
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    A = [s for s in mix.inputs if s.name == 'A' and s.type == 'RGBA'][0]
    B = [s for s in mix.inputs if s.name == 'B' and s.type == 'RGBA'][0]
    R = [s for s in mix.outputs if s.type == 'RGBA'][0]
    L.new(i1.outputs['Color'], A); B.default_value = _srgb(team); L.new(i1.outputs['Alpha'], mix.inputs['Factor'])
    L.new(R, bsdf.inputs['Base Color'])
    sep = N.new('ShaderNodeSeparateColor'); L.new(i2.outputs['Color'], sep.inputs[0])
    rough = N.new('ShaderNodeMath'); rough.operation = 'MULTIPLY_ADD'
    rough.inputs[1].default_value = -1.2; rough.inputs[2].default_value = 0.85
    L.new(sep.outputs[1], rough.inputs[0]); L.new(rough.outputs[0], bsdf.inputs['Roughness'])
    L.new(R, bsdf.inputs['Emission Color'])
    em = N.new('ShaderNodeMath'); em.operation = 'MULTIPLY'; em.inputs[1].default_value = 6.0
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
                v = V[used[lp.vertex_index]]; uvl.data[li].uv = (v[6], 1 - v[7])
            me.normals_split_custom_set([V[used[lp.vertex_index]][3:6] for lp in me.loops])
            me.materials.append(mat)
        ob = bpy.data.objects.new(p['name'], me if I else None)
        sc.collection.objects.link(ob)
        if p['parent']:
            ob.parent = objs[p['parent']]
        ob.location = p['off']
        objs[p['name']] = ob
    for name, rot in (pose or {}).items():   # rot in degrees, COB-like Euler XYZ
        if name in objs:
            objs[name].rotation_euler = Euler([math.radians(a) for a in rot])

    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.view_settings.view_transform = 'Standard'
    bpy.ops.mesh.primitive_plane_add(size=600, location=(0, -0.02, 0), rotation=(-math.pi / 2, 0, 0))
    gm = bpy.data.materials.new('ground'); gm.use_nodes = True
    gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.25, 0.22, 0.17, 1)
    bpy.context.object.data.materials.append(gm)
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 4.0
    sun.data.angle = math.radians(2)
    sun.matrix_world = Vector((0.45, -1.0, 0.3)).normalized().to_track_quat('-Z', 'X').to_matrix().to_4x4()
    sc.collection.objects.link(sun)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.6, 0.65, 0.72, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.6
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    s = max(1.0, m['radius'] / 18.0)        # views are tuned for ~18 elmo radius; scale for bigger models

    def look(pos, tgt, lens):
        mid = Vector(m['mid']); d = Vector(pos) - Vector(tgt)
        pos = mid + d * s; tgt = mid                 # frame the model's own centre, distance scaled by size
        cam.data.lens = lens; cam.data.clip_end = 5000
        f = (tgt - pos).normalized(); r = f.cross(Vector((0, 1, 0))).normalized(); u = r.cross(f)
        M = Matrix((r, u, -f)).transposed().to_4x4(); M.translation = pos; cam.matrix_world = M
    outs = []
    sc.render.resolution_x, sc.render.resolution_y = size
    for v in views:
        look(*VIEWS[v]); sc.render.filepath = f'{prefix}_{v}.png'; bpy.ops.render.render(write_still=True)
        outs.append(sc.render.filepath)
    if thumb:
        # what the player actually sees: fixed camera ~430 elmos away at ~65 deg pitch (a 2x2 unit is ~35 px wide
        # in a 2000 px screen), sandy ground, no scaling with model size - big units must look big.
        gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.42, 0.29, 0.14, 1)
        sc.render.resolution_x, sc.render.resolution_y = 240, 180
        az = math.radians(35); dist = 430; pitch = math.radians(65)
        pos = Vector((math.sin(az) * math.cos(pitch) * dist, math.sin(pitch) * dist, math.cos(az) * math.cos(pitch) * dist))
        cam.data.lens = 70
        f = (-pos).normalized(); r = f.cross(Vector((0, 1, 0))).normalized(); u = r.cross(f)
        M = Matrix((r, u, -f)).transposed().to_4x4(); M.translation = pos; cam.matrix_world = M
        sc.render.filepath = f'{prefix}_thumb.png'; bpy.ops.render.render(write_still=True)
        outs.append(sc.render.filepath)
    return outs


def sheet(paths, out, cols=2):
    from PIL import Image, ImageOps
    ims = [Image.open(p).convert('RGB') for p in paths if not p.endswith('_thumb.png')]
    if not ims:
        return
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (w * cols, h * rows), (40, 40, 40))
    for i, im in enumerate(ims):
        S.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    th = [p for p in paths if p.endswith('_thumb.png')]
    if th:
        # game-distance view, centre crop enlarged 3x with nearest-neighbour so the real pixel size stays visible
        t = Image.open(th[0]).convert('RGB'); cx, cy = t.width // 2, t.height // 2
        t = t.crop((cx - 50, cy - 38, cx + 50, cy + 38)).resize((300, 228), Image.NEAREST)   # 3x, real pixels
        g = ImageOps.grayscale(t).convert('RGB')
        S.paste(t, (w * cols - 2 * t.width - 10, 10)); S.paste(g, (w * cols - t.width - 5, 10))
    S.save(out)
