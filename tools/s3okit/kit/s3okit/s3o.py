"""S3O writer (from Blender objects) and reader.

Conventions verified against the Recoil source:
- S3O and 3DO share the engine coordinate frame here; we write engine coords directly.
- triangles (primitiveType 0), winding such that cross(b-a, c-a) points along the vertex normals.
- texv = blender_v, unflipped, with DDS textures written unflipped (s3okit/dds.py). Confirmed in game by the user
  (2026-10-25): the old texv = 1 - v with PNG textures came out upside down and had to be fixed by hand.
- Emit points: S3DModelPiece::GetEmitPos/GetEmitDir use vertex 0 (and 1). 0 verts -> pos 0, dir +Z;
  1 vert -> pos 0, dir = v0; 2+ -> pos v0, dir v1-v0. Weapons fire from and emit-sfx uses these, so we
  PREPEND the original 3DO piece's first one/two vertices (unreferenced by triangles) to every piece.
"""
import struct


def mesh_data(ob, dg):
    """(verts, indices) for an object: verts = (x,y,z,nx,ny,nz,u,v) piece-local, deduplicated."""
    if ob is None or ob.type != 'MESH':
        return [], []
    me = ob.evaluated_get(dg).to_mesh()
    me.calc_loop_triangles()
    cn = me.corner_normals
    uvl = me.uv_layers.active.uv if me.uv_layers.active else None
    verts, idx, key = [], [], {}
    for tri in me.loop_triangles:
        for li in tri.loops:
            co = me.vertices[me.loops[li].vertex_index].co
            n = cn[li].vector
            u, v = (uvl[li].vector.x, uvl[li].vector.y) if uvl else (0.0, 0.0)
            k = (round(co.x, 5), round(co.y, 5), round(co.z, 5), round(n.x, 4), round(n.y, 4), round(n.z, 4),
                 round(u, 6), round(v, 6))
            if k not in key:
                key[k] = len(verts); verts.append(k)
            idx.append(key[k])
    ob.evaluated_get(dg).to_mesh_clear()
    return verts, idx


def write(path, pieces, tex1, tex2):
    """pieces: ordered list of dict(name, parent, off(x,y,z), gpos, verts, idx, emit=[(x,y,z), ...])
    The first piece with parent None is the root."""
    by = {p['name']: p for p in pieces}
    kids = {}
    for p in pieces:
        kids.setdefault(p['parent'], []).append(p['name'])
    root = kids[None][0]
    allpts = [(p['gpos'][0] + v[0], p['gpos'][1] + v[1], p['gpos'][2] + v[2]) for p in pieces for v in p['verts']]
    if not allpts:
        allpts = [(0, 0, 0)]
    mins = [min(a[i] for a in allpts) for i in range(3)]
    maxs = [max(a[i] for a in allpts) for i in range(3)]
    mid = [(mins[i] + maxs[i]) / 2 for i in range(3)]
    radius = max(sum((a[i] - mid[i]) ** 2 for i in range(3)) ** 0.5 for a in allpts)
    height = maxs[1]

    buf = bytearray(b'\0' * 52)
    def put(b):
        o = len(buf); buf.extend(b); return o
    def cstr(s): return put(s.encode() + b'\0')

    def wp(n):
        p = by[n]
        ch = [wp(c) for c in kids.get(n, [])]
        emit = [tuple(e) + (0.0, 1.0, 0.0, 0.0, 0.0) for e in p.get('emit', [])]
        verts = emit + list(p['verts'])
        idx = [i + len(emit) for i in p['idx']]
        name_o = cstr(n)
        ch_o = put(struct.pack('<%di' % len(ch), *ch)) if ch else 0
        vo = put(b''.join(struct.pack('<8f', *v) for v in verts)) if verts else 0
        io = put(struct.pack('<%di' % len(idx), *idx)) if idx else 0
        return put(struct.pack('<10i3f', name_o, len(ch), ch_o, len(verts), vo, 0, 0, len(idx), io, 0, *p['off']))

    ro = wp(root)
    t1, t2 = cstr(tex1), cstr(tex2)
    struct.pack_into('<12si5f4i', buf, 0, b'Spring unit\0', 0, radius, height, *mid, ro, 0, t1, t2)
    open(path, 'wb').write(buf)
    return dict(radius=round(radius, 2), height=round(height, 2), mid=[round(m, 2) for m in mid],
                bytes=len(buf), tris=sum(len(p['idx']) // 3 for p in pieces))


def read(path):
    d = open(path, 'rb').read()
    cs = lambda o: d[o:d.index(b'\0', o)].decode()
    mag, ver, rad, h, mx, my, mz, root, coll, t1, t2 = struct.unpack_from('<12si5f4i', d, 0)
    assert mag == b'Spring unit\0', 'not an S3O'
    out = []
    def rp(o, parent):
        nm, nch, cho, nv, vo, vt, pt, nidx, io, col, x, y, z = struct.unpack_from('<10i3f', d, o)
        name = cs(nm)
        V = [struct.unpack_from('<8f', d, vo + 32 * i) for i in range(nv)]
        I = list(struct.unpack_from('<%di' % nidx, d, io)) if nidx else []
        out.append(dict(name=name, parent=parent, off=(x, y, z), verts=V, idx=I, primtype=pt))
        for i in range(nch):
            rp(struct.unpack_from('<i', d, cho + 4 * i)[0], name)
    rp(root, None)
    return dict(radius=rad, height=h, mid=(mx, my, mz), tex1=cs(t1), tex2=cs(t2), pieces=out)


def emit_verts_from_3do(piece3do, has_geometry):
    """vertices to prepend so the S3O piece has the same emit pos/dir as the 3DO piece had"""
    v = [tuple(x) for x in piece3do['verts'][:2]]
    if len(v) >= 2:
        return v                                   # pos v0, dir v1-v0
    if len(v) == 1:
        return v if not has_geometry else [(0.0, 0.0, 0.0), v[0]]          # pos 0, dir v0
    return [] if not has_geometry else [(0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]  # pos 0, dir +Z
