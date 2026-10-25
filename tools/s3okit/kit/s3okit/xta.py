"""Reading TA:Recoil unit/feature defs (Lua) and installing results into the repo.

Layout (BOTA base, all Lua since c565a1c / 7c805bd):
  units/<Name>.lua            return { <key> = { objectname = "<Name>", corpse = "<Name>_dead", ... } }
  Features/**/<Name>.lua      return { <key> = { object = "...", featuredead = "...", ... }, ... }
  scripts/<Name>.COB          compiled script (no BOS sources)  |  scripts/<Name>.lua  Lua unit script
The canonical unit name used by the kit (spec file, work dir, output files) is the unit file's stem, e.g.
ARM_T1_VEH_Flash. Lookups accept that stem, the def key or the display name, case-insensitively.
"""
import re, os, glob, shutil
from .common import REPO

# ------------------------------------------------------------------ Lua def loading (sandboxed, via lupa)
_lua = None
_LUA_SANDBOX = r'''
local proxy = setmetatable({}, {})
getmetatable(proxy).__index = function() return proxy end
getmetatable(proxy).__call = function() return proxy end
getmetatable(proxy).__concat = function() return "" end
_PROXY = proxy
function _loaddef(src, name)
  local env = setmetatable({string = string, math = math, table = table, pairs = pairs, ipairs = ipairs,
                            tostring = tostring, tonumber = tonumber, type = type, unpack = unpack or table.unpack},
                           {__index = function() return proxy end})
  local f, err = load(src, name, "t", env)
  if not f then error(err) end
  return f()
end
'''


def _L():
    global _lua
    if _lua is None:
        import lupa
        _lua = lupa.LuaRuntime(unpack_returned_tuples=True)
        _lua.execute(_LUA_SANDBOX)
    return _lua


def _py(v, proxy, depth=0):
    """Lua value -> python; tables become dicts (or lists for 1..n arrays); unknown globals -> None."""
    lua = _L()
    if lupa_type(v) != 'table':
        return v
    if v == proxy or depth > 12:
        return None
    items = list(v.items())
    keys = [k for k, _ in items]
    if keys and all(isinstance(k, int) for k in keys) and sorted(keys) == list(range(1, len(keys) + 1)):
        return [_py(x, proxy, depth + 1) for _, x in sorted(items)]
    return {(k.lower() if isinstance(k, str) else k): _py(x, proxy, depth + 1) for k, x in items}


def lupa_type(v):
    import lupa
    return lupa.lua_type(v)


def load_lua_defs(path):
    lua = _L()
    src = open(path, encoding='latin-1').read()
    t = lua.globals()._loaddef(src, '@' + os.path.basename(path))
    return _py(t, lua.globals()._PROXY) or {}


def _s(v):
    """def value -> string as the old FBI/TDF reader returned it (None when absent)."""
    if v is None:
        return None
    if isinstance(v, bool):
        return '1' if v else '0'
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


# ------------------------------------------------------------------ units
_units = {}
def units(repo=REPO):
    """stem -> dict(key=<def key>, file=<repo-relative path>, d=<def dict>)"""
    if repo not in _units:
        out = {}
        for f in sorted(glob.glob(os.path.join(repo, 'units', '**', '*.lua'), recursive=True)):
            try:
                defs = load_lua_defs(f)
            except Exception as e:
                print('WARN unit def', os.path.relpath(f, repo), e); continue
            for key, d in defs.items():
                if isinstance(d, dict):
                    out[os.path.splitext(os.path.basename(f))[0]] = dict(key=key, file=os.path.relpath(f, repo), d=d)
                    break
        _units[repo] = out
    return _units[repo]


def canonical(name, repo=REPO):
    """unit file stem for a stem / def key / display name (case-insensitive)."""
    U = units(repo); n = name.lower()
    for stem in U:
        if stem.lower() == n:
            return stem
    for stem, u in U.items():
        if u['key'].lower() == n or (u['d'].get('unitname') or '').lower() == n:
            return stem
    hits = [stem for stem, u in U.items() if (u['d'].get('name') or '').lower() == n]
    if len(hits) == 1:
        return hits[0]
    if hits:
        raise KeyError(f'{name!r} is ambiguous: {hits}')
    raise FileNotFoundError(name)


def unit_info(unitname, repo=REPO):
    stem = canonical(unitname, repo)
    u = units(repo)[stem]; d = u['d']
    info = {k: _s(d.get(k)) for k in ('unitname', 'name', 'side', 'description', 'objectname', 'corpse', 'footprintx',
                                       'footprintz', 'movementclass', 'canfly', 'floater', 'waterline', 'upright',
                                       'collisionvolumescales', 'collisionvolumeoffsets', 'collisionvolumetype',
                                       'script')}
    info['stem'] = stem
    info['def'] = u['file']
    info['fbi'] = u['file']          # older callers
    side = (info['side'] or stem).upper()
    info['side'] = 'CORE' if side.startswith('COR') else 'ARM'
    info['model'] = model_path(info['objectname'] or stem, repo)
    script = script_path(info.get('script') or stem, repo) or script_path(stem, repo)
    if script:
        info['script'] = script
        if script.lower().endswith('.cob'):
            info['cob'] = script
        elif script.lower().endswith('.lua'):
            info['lus'] = script
    info['corpse_chain'] = corpse_chain(info['corpse'], repo)
    return info


def _find_ci(base, names):
    """first file in dir `base` whose lowercased name is in names (case-insensitive VFS like the engine)."""
    if not os.path.isdir(base):
        return None
    lf = {f.lower(): f for f in os.listdir(base)}
    for n in names:
        if n.lower() in lf:
            return lf[n.lower()]
    return None


def model_path(name, repo=REPO, prefer=('.s3o', '.3do')):
    if not name:
        return None
    stem, ext = os.path.splitext(name)
    cands = [name] if ext.lower() in ('.s3o', '.3do') else [name + e for e in prefer]
    f = _find_ci(os.path.join(repo, 'objects3d'), cands)
    return os.path.join('objects3d', f) if f else None


def script_path(name, repo=REPO):
    stem = os.path.splitext(os.path.basename(name))[0]
    f = _find_ci(os.path.join(repo, 'scripts'), [stem + '.cob', stem + '.lua', stem + '_lus.lua', stem + '.bos'])
    return os.path.join('scripts', f) if f else None


# ------------------------------------------------------------------ features
_feat_cache = {}
def features(repo=REPO):
    if repo not in _feat_cache:
        d = {}
        for f in sorted(glob.glob(os.path.join(repo, 'Features', '**', '*.lua'), recursive=True)
                        + glob.glob(os.path.join(repo, 'features', '**', '*.lua'), recursive=True)):
            try:
                defs = load_lua_defs(f)
            except Exception as e:
                print('WARN feature def', os.path.relpath(f, repo), e); continue
            for key, b in defs.items():
                if not isinstance(b, dict):
                    continue
                d[key.lower()] = dict(file=os.path.relpath(f, repo), tdf=os.path.relpath(f, repo),
                                      object=_s(b.get('object')), featuredead=_s(b.get('featuredead')),
                                      footprint=(_s(b.get('footprintx')), _s(b.get('footprintz'))))
        _feat_cache[repo] = d
    return _feat_cache[repo]


def corpse_chain(corpse, repo=REPO):
    out, f, seen, F = [], (corpse or '').lower(), set(), features(repo)
    while f and f in F and f not in seen:
        seen.add(f); out.append(dict(feature=f, **F[f])); f = (F[f]['featuredead'] or '').lower()
    return out


# ------------------------------------------------------------------ script piece usage
def script_summary(path):
    """(pieces, {piece: sorted usage}) for a COB or a Lua unit script."""
    if path.lower().endswith('.cob'):
        from . import cob
        return cob.summary(path)
    return lus_summary(path)


def lus_summary(path):
    t = open(path, encoding='latin-1').read()
    t = re.sub(r'--\[\[.*?\]\]', '', t, flags=re.S); t = re.sub(r'--[^\n]*', '', t)
    pieces = []
    # piece('a', 'b') | piece "a" | piece("a")
    for m in re.finditer(r'\bpiece\s*\(?\s*((?:["\'][^"\']+["\']\s*,?\s*)+)\)?', t):
        pieces += re.findall(r'["\']([^"\']+)["\']', m.group(1))
    pieces = list(dict.fromkeys(p.lower() for p in pieces))
    use = {p: set() for p in pieces}
    ax = {'x_axis': 'x', 'y_axis': 'y', 'z_axis': 'z', '1': 'x', '2': 'y', '3': 'z'}
    for op, pc, a in re.findall(r'\b(Turn|Move|Spin|StopSpin)\s*\(\s*(\w+)\s*,\s*(\w+)', t):
        use.setdefault(pc.lower(), set()).add(f"{op.lower().replace('stopspin', 'stop-spin')} {ax.get(a.lower(), a)}")
    for op, pc in re.findall(r'\b(Hide|Show|Explode|EmitSfx)\s*\(\s*(\w+)', t):
        use.setdefault(pc.lower(), set()).add({'emitsfx': 'emit-sfx'}.get(op.lower(), op.lower()))
    for fn in re.finditer(r'function\s+script\.(Query\w*|AimFrom\w*)\s*\([^)]*\)(.*?)\bend\b', t, re.S):
        for pc in re.findall(r'return\s+(\w+)', fn.group(2)):
            use.setdefault(pc.lower(), set()).add('query/aimfrom')
    return pieces, {k: sorted(v) for k, v in use.items() if k in use}


# ------------------------------------------------------------------ install into the repo
def _set_lua_key(text, key, value, block=None):
    """set `key = "value",` (first occurrence, or inside the table `block = {...}`)."""
    lo, hi = 0, len(text)
    if block:
        m = re.search(r'(?im)^\s*\[?"?%s"?\]?\s*=\s*\{' % re.escape(block), text)
        if not m:
            raise KeyError(block)
        lo, depth, i = m.end(), 1, m.end()
        while depth and i < len(text):
            depth += {'{': 1, '}': -1}.get(text[i], 0); i += 1
        hi = i
    seg = text[lo:hi]
    pat = r'(?im)^(\s*%s\s*=\s*)("[^"\n]*"|\'[^\'\n]*\'|[^,\n]*)' % re.escape(key)
    if re.search(pat, seg):
        seg = re.sub(pat, lambda mm: mm.group(1) + f'"{value}"', seg, count=1)
    else:   # key absent: add it as the block's first entry
        seg = seg.replace('\n', f'\n\t\t{key} = "{value}",', 1)
    return text[:lo] + seg + text[hi:]


def install_unit(unitname, workdir, repo=REPO):
    """copy model + textures for the unit and its corpses into the repo and point the defs at them.
    Explicit .s3o extensions: without one the engine picks whichever registered format it finds first."""
    info = unit_info(unitname, repo)
    stem = info['stem']
    out = os.path.join(workdir, 'out')
    done = []
    for f in sorted(os.listdir(out)):
        src = os.path.join(out, f)
        if f.endswith('.s3o'):
            shutil.copy(src, os.path.join(repo, 'objects3d', f)); done.append('objects3d/' + f)
        elif f.endswith('.png') and re.search(r'_[12]\.png$', f):
            shutil.copy(src, os.path.join(repo, 'unittextures', f)); done.append('unittextures/' + f)
    p = os.path.join(repo, info['def'])
    t = open(p, newline='', encoding='latin-1').read()
    t = _set_lua_key(t, 'objectname', stem + '.s3o')
    open(p, 'w', newline='', encoding='latin-1').write(t); done.append(info['def'])
    for c in info['corpse_chain']:
        name = c['object'] or ''
        hit = _find_ci(out, [os.path.splitext(name)[0] + '.s3o'])
        if hit:
            p = os.path.join(repo, c['file'])
            tt = open(p, newline='', encoding='latin-1').read()
            tt = _set_lua_key(tt, 'object', hit, block=c['feature'])
            open(p, 'w', newline='', encoding='latin-1').write(tt); done.append(c['file'] + f' [{c["feature"]}]')
    return done


def install_heap(name, workdir, repo=REPO):
    """copy heap model/textures; point EVERY feature using object = "<name>" at <name>.s3o"""
    out = os.path.join(workdir, 'out'); done = []
    for f in os.listdir(out):
        if f.endswith('.s3o'):
            shutil.copy(os.path.join(out, f), os.path.join(repo, 'objects3d', f)); done.append(f)
        elif f.endswith('.png'):
            shutil.copy(os.path.join(out, f), os.path.join(repo, 'unittextures', f)); done.append(f)
    for p in sorted(glob.glob(os.path.join(repo, 'Features', '**', '*.lua'), recursive=True)):
        t = open(p, newline='', encoding='latin-1').read()
        t2 = re.sub(r'(?im)^(\s*object\s*=\s*)"%s(?:\.3do)?"' % re.escape(name), lambda m: m.group(1) + f'"{name}.s3o"', t)
        if t2 != t:
            open(p, 'w', newline='', encoding='latin-1').write(t2); done.append(os.path.relpath(p, repo))
    return done
