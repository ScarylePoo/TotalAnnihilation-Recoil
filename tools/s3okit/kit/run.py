#!/usr/bin/env python3
"""s3okit command line. Run with the system python that has `bpy` installed (pip install bpy).

  python3 run.py inspect <unitname>            reference sheet, piece/script report, scaffold units/<unitname>.py
  python3 run.py all <unitname> [--draft]      build -> bake -> compose -> export -> wrecks -> preview
  python3 run.py build|bake|compose|export|wreck|preview <unitname> [--draft]
  python3 run.py heap <name> --size N [--seed S]   generic scrap heap (e.g. heap 2x2a --size 2)
  python3 run.py install <unitname> | install-heap <name>   copy into the repo and point the Lua defs at the S3Os

<unitname> is the unit file stem (ARM_T1_VEH_Flash); any case, the def key or the display name also work and are
resolved to the stem, which names the spec (units/<stem>.py), the work dir and every output file.
Env: XTA_REPO (default: the repo this kit lives in), S3OKIT_WORK (default <kit>/work)
"""
import sys, os, json, importlib.util, argparse, time, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s3okit.common import KIT, REPO, workdir
from s3okit import xta


def load_spec(unitname):
    p = os.path.join(KIT, 'units', unitname + '.py')
    if not os.path.exists(p):
        sys.exit(f'no spec {p}; run: python3 run.py inspect {unitname}')
    spec = importlib.util.spec_from_file_location('spec_' + unitname, p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    U = dict(getattr(mod, 'UNIT', {}))
    info = xta.unit_info(unitname)
    fp = max(int(info['footprintx'] or 2), int(info['footprintz'] or 2))
    U.setdefault('side', info['side'])
    U.setdefault('res', 1024 if fp <= 3 else 2048)
    U.setdefault('bake_res', min(2 * U['res'], 4096))
    air = (info.get('canfly') or '0').strip() == '1'
    U.setdefault('air', air)
    U.setdefault('ground', not air and (info.get('floater') or '0').strip() != '1')
    # ref = the model whose pieces the script drives; ref_model (repo-relative) overrides the def's current model
    U.setdefault('ref', os.path.join(REPO, U.pop('ref_model', None) or info['model']))
    U.setdefault('wreck', {})
    U.setdefault('wreck_res', U['res'] // 2)      # wrecks matter less; halves repo size
    U.setdefault('preview_pose', {})
    return mod, U, info


def st_build(unitname, draft=False):
    import bpy
    from s3okit import geom
    mod, U, info = load_spec(unitname)
    wd = workdir(unitname)
    geom.reset_scene()
    k = geom.Unit(U['ref'], ground=U['ground'], air=U['air'], skeleton=U.get('skeleton'), skel_opts=U.get('skeleton_opts'))
    mod.build(k)
    objs = k.realize()
    bpy.context.view_layer.update()
    meshes = [o for o in objs.values() if o.type == 'MESH']
    cull = geom.visibility_cull(meshes, ground=U['ground'], air=U['air'])
    geom.unwrap(meshes, res=U['res'], ground=U['ground'], air=U['air'])
    geom.add_mirrors(meshes)
    geom.apply_clones(k)
    allobjs = list(k.objs.values())
    geom.finalize_shading(allobjs)
    rep = geom.uv_report(allobjs, save=os.path.join(wd, 'prev', 'uv_layout.png'))
    rep['culled_faces'] = cull
    rep['skeleton'] = k.skel_report
    json.dump(k.T, open(os.path.join(wd, 'pieces.json'), 'w'), indent=1)   # export/wreck use THIS table
    # sanity: mirror sources (1) and copies (2) must match per material
    import bmesh, collections
    asym = {}
    for o in allobjs:
        if o.type != 'MESH':
            continue
        bm = bmesh.new(); bm.from_mesh(o.data); mir = bm.faces.layers.int.get('mir')
        c = collections.Counter((f.material_index, f[mir]) for f in bm.faces) if mir else {}
        bad = {geom.MATS[m]: (c.get((m, 1), 0), c.get((m, 2), 0)) for m in {k[0] for k in c} if c.get((m, 1), 0) != c.get((m, 2), 0)}
        if bad:
            asym[o.name] = bad
        bm.free()
    rep['mirror_asymmetry'] = asym
    rep['pieces'] = list(k.T)
    if info.get('script'):
        bp, use = xta.script_summary(os.path.join(REPO, info['script']))
        rep['script_pieces_missing'] = [p for p in bp if p.lower() not in {n.lower() for n in k.T}]
    json.dump(rep, open(os.path.join(wd, 'build_report.json'), 'w'), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(wd, 'unit.blend'))
    print('BUILD', unitname, rep['tris'], 'tris, UV coverage', rep['uv_coverage'])
    return rep


def st_bake(unitname, draft=False, blend='unit.blend', npz='maps.npz', res=None):
    import bpy
    from s3okit import bake
    mod, U, info = load_spec(unitname)
    wd = workdir(unitname)
    bpy.ops.wm.open_mainfile(filepath=os.path.join(wd, blend))
    r = res or (U['bake_res'] // 2 if draft else U['bake_res'])
    t = time.time()
    bake.bake_maps(os.path.join(wd, npz), res=r, quality='draft' if draft else 'final')
    print('BAKE', blend, r, f'{time.time() - t:.0f}s')


def st_compose(unitname, draft=False):
    from s3okit import compose
    mod, U, info = load_spec(unitname)
    wd = workdir(unitname)
    compose.compose(os.path.join(wd, 'maps.npz'), os.path.join(wd, 'out', unitname), final=U['res'], side=U['side'])
    from s3okit import dds
    dds.convert_pair(os.path.join(wd, 'out', unitname))


def st_export(unitname, draft=False):
    import bpy
    from s3okit import s3o, threedo
    mod, U, info = load_spec(unitname)
    wd = workdir(unitname)
    bpy.ops.wm.open_mainfile(filepath=os.path.join(wd, 'unit.blend'))
    T = json.load(open(os.path.join(wd, 'pieces.json')))
    dg = bpy.context.evaluated_depsgraph_get()
    pieces = []
    for name, t in T.items():
        ob = bpy.data.objects.get(name)
        v, i = s3o.mesh_data(ob, dg)
        pieces.append(dict(name=name, parent=t['parent'], off=t['off'], gpos=t['gpos'], verts=v, idx=i,
                           emit=s3o.emit_verts_from_3do(t, bool(i))))
    r = s3o.write(os.path.join(wd, 'out', unitname + '.s3o'), pieces, unitname + '_1.dds', unitname + '_2.dds')
    print('EXPORT', unitname, r)
    return r


def _is_generic_heap(obj):
    return bool(re.fullmatch(r'\d+x\d+[a-z]?', (obj or '').lower()))


def st_wreck(unitname, draft=False):
    """corpse chain: [0] -> level-1 wreck; [1] -> level-2 wreck if unit-specific (generic NxN heaps come from `heap`)"""
    import bpy
    from s3okit import wreck, threedo, s3o, bake, compose, geom
    mod, U, info = load_spec(unitname)
    wd = workdir(unitname)
    T = json.load(open(os.path.join(wd, 'pieces.json')))
    made = []
    for lvl, c in enumerate(info['corpse_chain'][:2], start=1):
        obj = os.path.splitext(c['object'] or '')[0]
        if not obj or _is_generic_heap(obj) or obj.lower() == 'rock_teeth':
            continue
        bpy.ops.wm.open_mainfile(filepath=os.path.join(wd, 'unit.blend'))
        objs = {n: bpy.data.objects[n] for n in T if n in bpy.data.objects}
        W = U['wreck']
        ob = wreck.make(T, objs, level=lvl, seed=W.get('seed', 1) + lvl, pose=W.get('pose'),
                        drop=W.get('drop', ()), remove=W.get('remove', ()))
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(wd, f'{obj}.blend'))
        r = U['wreck_res'] if draft else min(U['bake_res'], 2 * U['wreck_res'])
        bake.bake_maps(os.path.join(wd, f'{obj}.npz'), res=r, quality='draft' if draft else 'final')
        compose.compose(os.path.join(wd, f'{obj}.npz'), os.path.join(wd, 'out', obj), final=U['wreck_res'],
                        side=U['side'], mode='wreck', seed=lvl)
        from s3okit import dds
        dds.convert_pair(os.path.join(wd, 'out', obj))
        bpy.ops.wm.open_mainfile(filepath=os.path.join(wd, f'{obj}.blend'))
        dg = bpy.context.evaluated_depsgraph_get()
        v, i = s3o.mesh_data(bpy.data.objects['base'], dg)
        rr = s3o.write(os.path.join(wd, 'out', obj + '.s3o'),
                       [dict(name='base', parent=None, off=(0, 0, 0), gpos=(0, 0, 0), verts=v, idx=i)],
                       obj + '_1.dds', obj + '_2.dds')
        print('WRECK', obj, 'level', lvl, rr)
        made.append(obj)
    return made


def st_preview(unitname, draft=False):
    from s3okit import preview
    mod, U, info = load_spec(unitname)
    wd = workdir(unitname); out = os.path.join(wd, 'out')
    pose = U['preview_pose'] or {}
    paths = preview.render(os.path.join(out, unitname + '.s3o'), out, os.path.join(wd, 'prev', unitname),
                           pose=pose, samples=16 if draft else 32)
    for f in sorted(os.listdir(out)):
        if f.endswith('.s3o') and f != unitname + '.s3o':
            paths += preview.render(os.path.join(out, f), out, os.path.join(wd, 'prev', f[:-4]),
                                    views=('front34',), samples=16 if draft else 24, thumb=False)
    preview.sheet(paths, os.path.join(wd, 'prev', 'sheet.png'))
    print('PREVIEW', os.path.join(wd, 'prev', 'sheet.png'))


def st_heap(name, size, seed=1, draft=False):
    import bpy
    from s3okit import heap, geom, bake, compose, s3o, preview
    wd = workdir('heap_' + name)
    ob = heap.make(size, seed)
    bpy.context.view_layer.update()
    geom.visibility_cull([ob], ground=True, rays=24)
    res = 512 if size <= 1 else 1024 if size <= 4 else 2048
    geom.unwrap([ob], res=res)
    geom.finalize_shading([ob])
    rep = geom.uv_report([ob])
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(wd, 'heap.blend'))
    bake.bake_maps(os.path.join(wd, 'maps.npz'), res=res if draft else min(2 * res, 2048), quality='draft' if draft else 'final',
                   ao_far=2.0, ao_near=0.4)
    compose.compose(os.path.join(wd, 'maps.npz'), os.path.join(wd, 'out', name), final=res, side='SCRAP', mode='heap',
                    seed=seed, seams=False)
    from s3okit import dds
    dds.convert_pair(os.path.join(wd, 'out', name))
    bpy.ops.wm.open_mainfile(filepath=os.path.join(wd, 'heap.blend'))
    dg = bpy.context.evaluated_depsgraph_get()
    v, i = s3o.mesh_data(bpy.data.objects['base'], dg)
    r = s3o.write(os.path.join(wd, 'out', name + '.s3o'), [dict(name='base', parent=None, off=(0, 0, 0), gpos=(0, 0, 0), verts=v, idx=i)],
                  name + '_1.dds', name + '_2.dds')
    p = preview.render(os.path.join(wd, 'out', name + '.s3o'), os.path.join(wd, 'out'), os.path.join(wd, 'prev', name),
                       views=('front34', 'top'), samples=16)
    preview.sheet(p, os.path.join(wd, 'prev', 'sheet.png'))
    print('HEAP', name, size, r, rep)


def st_inspect(unitname, draft=False):
    from s3okit import threedo
    info = xta.unit_info(unitname)
    wd = workdir(unitname)
    print(json.dumps({k: v for k, v in info.items() if k != 'corpse_chain'}, indent=1))
    print('corpse chain:', [(c['feature'], c['object'], c['file']) for c in info['corpse_chain']])
    T = threedo.load_any(os.path.join(REPO, info['model']))
    print('\npieces (engine coords; off = offset from parent; bbox piece-local):')
    for n, t in T.items():
        bb = threedo.bbox(t)
        print(f"  {n:14s} parent={str(t['parent']):12s} off=({t['off'][0]:.2f},{t['off'][1]:.2f},{t['off'][2]:.2f})"
              f" global=({t['gpos'][0]:.2f},{t['gpos'][1]:.2f},{t['gpos'][2]:.2f}) verts={len(t['verts'])} faces={len(threedo.real_faces(t))}"
              + (f" bbox x[{bb[0][0]:.1f},{bb[0][1]:.1f}] y[{bb[1][0]:.1f},{bb[1][1]:.1f}] z[{bb[2][0]:.1f},{bb[2][1]:.1f}]" if bb else ''))
    if info.get('script'):
        bp, use = xta.script_summary(os.path.join(REPO, info['script']))
        print('\nscript pieces and what the script does with them:')
        for p in bp:
            print(f'  {p:14s} {", ".join(use.get(p, [])) or "-"}')
        miss = [p for p in bp if p.lower() not in {n.lower() for n in T}]
        if miss:
            print('  !! script pieces not in 3DO:', miss)
    from s3okit import skeleton as SK
    legs = [n for n in T if SK.is_leg_piece(n)]
    kind = None
    if legs and not re.search(r'(spider|roach|scarab|the_?can|sumo)', unitname, re.I):
        feet = [n for n in legs if SK._kind_of(n) == 'foot']
        kind = 'quad' if max(len(feet), len([n for n in legs if SK._kind_of(n) == 'thigh'])) >= 4 else 'biped'
        newT, rep = SK.remap(T, kind)
        print(f'\nLEGGED -> standard {kind} skeleton (HANDOFF "Walkers"). Verify the guess; legs dropped: {rep["dropped"]}')
        print('  pelvis height', rep['pelvis_height'], 'hipx', rep['hipx'], 'reparented:', rep['reparented'])
    elif re.search(r'(the_?can|sumo)', unitname, re.I):
        print('\nThe Can / Sumo: user wants TRACKS instead of legs (HANDOFF "Walkers"); script must change too.')
    fl = [n for n, t in T.items() if re.search(r'(flare|fire|flash|muzzle)', n, re.I) and threedo.real_faces(t)]
    if fl:
        print('\nFLARE pieces with muzzle-flash polygons (keep the piece, drop the polygons):', fl)
    _ref_sheet(T, os.path.join(wd, 'prev', 'ref3do.png'))
    print('\nreference render:', os.path.join(wd, 'prev', 'ref3do.png'))
    sp = os.path.join(KIT, 'units', unitname + '.py')
    if not os.path.exists(sp):
        with open(sp, 'w') as f:
            flare = re.compile(r'(flare|fire|flash|muzzle)', re.I)   # 1998 muzzle-flash stand-in polygons: never rebuilt
            blocks = [f"    k.piece('{n}').from_3do()" for n, t in T.items()
                      if threedo.real_faces(t) and not (kind and n in legs) and not flare.search(n)]
            if kind:
                blocks = ['    k.standard_legs()   # backwards Federation-style legs, all legs share UVs'] + blocks
            f.write(SCAFFOLD.format(unitname=unitname, name=info['name'], blocks='\n'.join(blocks),
                                    skel=(f"    skeleton='{kind}',          # standard walker hierarchy; skeleton_opts=dict(height=, hipx=)\n" if kind else '')))
        print('scaffold written:', sp)


SCAFFOLD = '''"""{name} ({unitname}). Coordinates are ENGINE/global: X right, Y up, Z forward. See HANDOFF.md."""
UNIT = dict(
{skel}    # side='ARM', res=1024, bake_res=2048, ground=True, air=False,
    wreck=dict(seed=1),            # pose={{'turret': (0, 30, 0)}}, drop=['barrel'], remove=[]
    preview_pose={{}},              # {{'turret': (0, 35, 0)}}
)


def build(k):
    P = k.P   # piece name -> global origin (Vector). b.at(x, y, z) = coordinates relative to a piece origin.
    # Blockout: the original TA polygons. Replace piece by piece with real shapes.
{blocks}
'''


def _ref_sheet(T, out):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from s3okit import threedo
    polys, cols = [], []
    cmap = plt.get_cmap('tab10')
    names = list(T)
    for n, t in T.items():
        g = t['gpos']
        for q in threedo.real_faces(t):
            polys.append([(t['verts'][i][0] + g[0], t['verts'][i][2] + g[2], t['verts'][i][1] + g[1]) for i in q['idx']])
            cols.append(cmap(names.index(n) % 10))
    if not polys:
        return
    import numpy as np
    A = np.array([p for poly in polys for p in poly]); lo, hi = A.min(0), A.max(0); c = (lo + hi) / 2; r = (hi - lo).max() / 2 + 1
    fig = plt.figure(figsize=(16, 11))
    for k, (e, a, ttl) in enumerate([(30, -60, 'front-left (front = +Z)'), (30, 120, 'rear-right'), (90, -90, 'top (front = down)'),
                                     (0, 0, 'side from +X'), (0, -90, 'front'), (-30, -60, 'under')]):
        ax = fig.add_subplot(2, 3, k + 1, projection='3d')
        ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors='k', linewidths=0.3))
        ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(max(lo[2] - 1, c[2] - r), c[2] + r)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(e, a); ax.set_title(ttl); ax.set_xlabel('x'); ax.set_ylabel('z'); ax.set_zlabel('y')
    fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=cmap(i % 10)) for i in range(len(names))], labels=names, loc='lower center', ncol=8)
    plt.tight_layout(); plt.savefig(out, dpi=70); plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd'); ap.add_argument('name')
    ap.add_argument('--draft', action='store_true', help='half-res, low-sample bakes for iterating')
    ap.add_argument('--size', type=int, default=2); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    if a.cmd not in ('heap', 'install-heap'):
        a.name = xta.canonical(a.name)     # ARM_T1_VEH_Flash, whatever case/key/display name was typed
    if a.cmd == 'heap':
        return st_heap(a.name, a.size, a.seed, a.draft)
    if a.cmd == 'install':
        print('\n'.join(xta.install_unit(a.name, workdir(a.name)))); return
    if a.cmd == 'install-heap':
        print('\n'.join(xta.install_heap(a.name, workdir('heap_' + a.name)))); return
    stages = {'inspect': [st_inspect], 'build': [st_build], 'bake': [st_bake], 'compose': [st_compose],
              'export': [st_export], 'wreck': [st_wreck], 'preview': [st_preview],
              'all': [st_build, st_bake, st_compose, st_export, st_wreck, st_preview]}[a.cmd]
    for s in stages:
        s(a.name, a.draft)


if __name__ == '__main__':
    main()
