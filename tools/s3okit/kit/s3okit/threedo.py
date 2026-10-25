"""TA .3do reader. Returns pieces in ENGINE coordinates (the engine negates Z when loading 3DO)."""
import struct

def load(path):
    d = open(path, 'rb').read()
    cs = lambda o: d[o:d.index(b'\0', o)].decode('latin1')
    def walk(off, parent, root=False):
        out = []
        while off or root:
            root = False
            (ver, nv, npr, sel, x, y, z, on, _0, ov, op, osib, ochild) = struct.unpack_from('<13i', d, off)
            verts = []
            for i in range(nv):
                a, b, c = struct.unpack_from('<3i', d, ov + 12 * i)
                verts.append((a / 65536, b / 65536, -c / 65536))
            prims = []
            for i in range(npr):
                col, ni, _, oi, ot, *_r = struct.unpack_from('<8i', d, op + 32 * i)
                idx = list(struct.unpack_from('<%dh' % ni, d, oi)) if ni else []
                prims.append(dict(idx=idx, tex=cs(ot) if ot else '', sel=(i == sel)))
            node = dict(name=cs(on), parent=parent, off=(x / 65536, y / 65536, -z / 65536),
                        verts=verts, prims=prims)
            node['children'] = walk(ochild, node['name'])
            out.append(node)
            off = osib
        return out
    return walk(0, None, True)

def flatten(tree):
    """name -> dict(parent, off, gpos, verts, prims, children[names]) in hierarchy order."""
    res = {}
    def rec(n, g):
        gp = (g[0] + n['off'][0], g[1] + n['off'][1], g[2] + n['off'][2])
        res[n['name']] = dict(parent=n['parent'], off=n['off'], gpos=gp, verts=n['verts'],
                              prims=n['prims'], children=[c['name'] for c in n['children']])
        for c in n['children']:
            rec(c, gp)
    for n in tree:
        rec(n, (0, 0, 0))
    return res

def real_faces(p):
    """3DO primitives that are drawn faces (>=3 verts, not the selection/ground plate)."""
    return [q for q in p['prims'] if len(q['idx']) >= 3 and not q['sel']]

def bbox(p):
    if not p['verts']:
        return None
    vs = p['verts']
    return [(min(v[i] for v in vs), max(v[i] for v in vs)) for i in range(3)]

def guess_mat(tex):
    t = tex.lower()
    if 'tred' in t or 'track' in t: return 'tread'
    if 'logo' in t or 'gouraud' in t: return 'team'
    if 'metal' in t or 'steel' in t: return 'steel'
    if 'noise' in t or 'dark' in t or 'black' in t: return 'dark'
    if 'glass' in t or 'window' in t: return 'glass'
    if 'light' in t or 'glow' in t: return 'lightw'
    return 'paint'


def load_any(path):
    """Reference model as a flat piece dict, from a .3do (TA) or an .s3o (some XTA units were already remodelled).
    Same structure as flatten(load(...)); S3O triangles become prims."""
    if not path.lower().endswith('.s3o'):
        return flatten(load(path))
    from . import s3o as S3O
    m = S3O.read(path)
    res, gpos = {}, {}
    for p in m['pieces']:
        g0 = gpos.get(p['parent'], (0.0, 0.0, 0.0))
        g = (g0[0] + p['off'][0], g0[1] + p['off'][1], g0[2] + p['off'][2])
        gpos[p['name']] = g
        I = p['idx']
        prims = [dict(idx=list(I[k:k + 3]), tex='', sel=False) for k in range(0, len(I), 3)] if p['primtype'] == 0 else []
        res[p['name']] = dict(parent=p['parent'], off=tuple(p['off']), gpos=g, verts=[tuple(v[:3]) for v in p['verts']],
                              prims=prims, children=[], src='s3o')
        if p['parent']:
            res[p['parent']]['children'].append(p['name'])
    return res
