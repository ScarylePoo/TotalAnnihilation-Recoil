"""Bake helper maps from the current Blender scene into a .npz (row 0 = top of the image).
Maps: id (material slot), pos (engine coords), nrm, edge (bevel-normal dot), aonear, aofar, cover."""
import bpy, numpy as np
from .common import MATS

# final was edge 16 / aonear 24 / aofar 48. Measured on the Instigator (2048 bake, 1024 texture): 6/8/12 differs from it
# by < 0.4 % mean, ~2-3 % p99 after the 2x2 downsample (below DXT error) and bakes 4.7x faster (498 s vs 2348 s).
QUALITY = {'draft': dict(edge=4, aonear=6, aofar=10), 'final': dict(edge=6, aonear=8, aofar=12)}


def _setup(kind, img, ao_far, ao_near):
    for m in bpy.data.materials:
        if m.name not in MATS:
            continue
        m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        em = nt.nodes.new('ShaderNodeEmission')
        nt.links.new(em.outputs[0], out.inputs['Surface'])
        geo = nt.nodes.new('ShaderNodeNewGeometry')
        if kind == 'pos':
            nt.links.new(geo.outputs['Position'], em.inputs['Color'])
        elif kind == 'nrm':
            nt.links.new(geo.outputs['Normal'], em.inputs['Color'])
        elif kind in ('aonear', 'aofar'):
            ao = nt.nodes.new('ShaderNodeAmbientOcclusion')
            ao.only_local = True          # per piece: moving parts must not bake shadows onto each other
            ao.samples = 16
            ao.inputs['Distance'].default_value = ao_far if kind == 'aofar' else ao_near
            nt.links.new(ao.outputs['AO'], em.inputs['Color'])
        elif kind == 'edge':
            bev = nt.nodes.new('ShaderNodeBevel'); bev.samples = 8
            bev.inputs['Radius'].default_value = 0.09
            dot = nt.nodes.new('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'
            nt.links.new(bev.outputs[0], dot.inputs[0]); nt.links.new(geo.outputs['Normal'], dot.inputs[1])
            nt.links.new(dot.outputs['Value'], em.inputs['Color'])
        elif kind == 'id':
            em.inputs['Color'].default_value = ((MATS.index(m.name) + 1) / 32, 0, 0, 1)
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = img
        nt.nodes.active = tex


def bake_maps(out_npz, res=2048, quality='final', ao_far=3.0, ao_near=0.6):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.render.bake.margin = 0
    img = bpy.data.images.new('bake', res, res, alpha=True, float_buffer=True)
    img.colorspace_settings.name = 'Non-Color'
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and len(o.data.polygons)]
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    q = QUALITY[quality]
    res_maps = {}
    # margin MUST be 0: with several objects baking into one image, Cycles applies each object's margin
    # over the other objects' texels. compose.py dilates islands itself using the coverage mask.
    for kind, spp, mg in [('id', 1, 0), ('pos', 1, 0), ('nrm', 1, 0), ('edge', q['edge'], 0),
                          ('aonear', q['aonear'], 0), ('aofar', q['aofar'], 0)]:
        _setup(kind, img, ao_far, ao_near)
        sc.cycles.samples = spp
        img.pixels.foreach_set(np.zeros(res * res * 4, np.float32))
        bpy.ops.object.bake(type='EMIT', margin=mg)
        a = np.empty(res * res * 4, np.float32); img.pixels.foreach_get(a)
        a = a.reshape(res, res, 4)[::-1, :, :3]
        res_maps[kind] = (a[..., :1] if kind in ('id', 'edge', 'aonear', 'aofar') else a).astype(np.float16 if kind != 'pos' else np.float32).copy()
        print('baked', kind, flush=True)
    res_maps['cover'] = (res_maps['id'] > 0.5 / 32).astype(np.uint8)
    np.savez_compressed(out_npz, **res_maps)
