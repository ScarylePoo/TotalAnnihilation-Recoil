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


TILE = 2048    # largest image baked in one go; larger bakes are done tile by tile


def bake_maps(out_npz, res=2048, quality='final', ao_far=3.0, ao_near=0.6):
    """Bake the helper maps at res x res. Above TILE the bake is split into (res/TILE)^2 tiles: the UVs are scaled and
    offset so each tile fills a TILE x TILE image, baked, and stitched. The shell's memory cgroup (~5.8 GB shared by
    every agent's processes) OOM-killed 4096 bakes; tiling keeps the peak at the 2048 level for any size."""
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.render.bake.margin = 0
    n = max(1, res // TILE) if res > TILE else 1
    tile = res // n
    img = bpy.data.images.new('bake', tile, tile, alpha=True, float_buffer=True)
    img.colorspace_settings.name = 'Non-Color'
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and len(o.data.polygons)]
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    q = QUALITY[quality]
    # original UVs, restored after every tile
    uv0 = {}
    for o in meshes:
        uvl = o.data.uv_layers.active
        a = np.empty(len(uvl.data) * 2, np.float32); uvl.data.foreach_get('uv', a)
        uv0[o.name] = a
    res_maps = {}
    kinds = [('id', 1), ('pos', 1), ('nrm', 1), ('edge', q['edge']), ('aonear', q['aonear']), ('aofar', q['aofar'])]
    for kind, spp in kinds:
        res_maps[kind] = np.zeros((res, res, 1 if kind in ('id', 'edge', 'aonear', 'aofar') else 3),
                                  np.float16 if kind != 'pos' else np.float32)
    try:
        for ty in range(n):
            for tx in range(n):
                if n > 1:     # map this tile's UV square onto the whole image
                    for o in meshes:
                        a = uv0[o.name].reshape(-1, 2) * n - (tx, ty)
                        o.data.uv_layers.active.data.foreach_set('uv', a.astype(np.float32).ravel())
                # margin MUST be 0: with several objects baking into one image, Cycles applies each object's margin
                # over the other objects' texels. compose.py dilates islands itself using the coverage mask.
                for kind, spp in kinds:
                    _setup(kind, img, ao_far, ao_near)
                    sc.cycles.samples = spp
                    img.pixels.foreach_set(np.zeros(tile * tile * 4, np.float32))
                    bpy.ops.object.bake(type='EMIT', margin=0)
                    a = np.empty(tile * tile * 4, np.float32); img.pixels.foreach_get(a)
                    a = a.reshape(tile, tile, 4)[::-1, :, :3]          # rows top (v=1) first
                    r0 = (n - 1 - ty) * tile                            # tile ty counts v from the bottom
                    dst = res_maps[kind]
                    dst[r0:r0 + tile, tx * tile:(tx + 1) * tile] = a[..., :dst.shape[2]]
                    del a
                print('baked tile', tx, ty, 'of', n, 'x', n, flush=True)
    finally:
        for o in meshes:
            o.data.uv_layers.active.data.foreach_set('uv', uv0[o.name])
    res_maps['cover'] = (res_maps['id'] > 0.5 / 32).astype(np.uint8)
    np.savez_compressed(out_npz, **res_maps)
