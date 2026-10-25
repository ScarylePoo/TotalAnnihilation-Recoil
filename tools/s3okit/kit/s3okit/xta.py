"""Reading XTA unit/feature defs and installing results into the repo."""
import re, os, glob, shutil
from .common import REPO


def kv(t, k):
    m = re.search(r'(?im)^\s*%s\s*=\s*([^;\r\n]*);' % k, t)
    return m.group(1).strip() if m else None


def find_fbi(unitname, repo=REPO):
    for f in glob.glob(os.path.join(repo, 'units/**/*.fbi'), recursive=True):
        if os.path.splitext(os.path.basename(f))[0].lower() == unitname.lower():
            return f
    raise FileNotFoundError(unitname)


def unit_info(unitname, repo=REPO):
    f = find_fbi(unitname, repo); t = open(f, errors='replace').read()
    info = {k: kv(t, k) for k in ('unitname', 'name', 'side', 'description', 'objectname', 'corpse', 'footprintx',
                                   'footprintz', 'movementclass', 'canfly', 'floater', 'waterline', 'upright',
                                   'collisionvolumescales', 'collisionvolumeoffsets', 'collisionvolumetype')}
    info['fbi'] = os.path.relpath(f, repo)
    side = (info['side'] or '').upper()
    info['side'] = 'CORE' if side.startswith('COR') else 'ARM'
    obj = info['objectname'] or unitname
    info['model'] = model_path(obj, repo)
    for p in (f'scripts/{unitname}.bos', f'scripts/bos/{unitname}.bos', f'scripts/{unitname}.lua', f'scripts/{unitname}.cob'):
        if os.path.exists(os.path.join(repo, p)):
            info.setdefault('script', p)
            if p.endswith('.bos'):
                info['bos'] = p
    info['corpse_chain'] = corpse_chain(info['corpse'], repo)
    return info


def model_path(name, repo=REPO):
    if not name:
        return None
    base = os.path.join(repo, 'objects3d')
    for f in os.listdir(base):
        lf = f.lower()
        if lf == name.lower() or lf in (name.lower() + '.3do', name.lower() + '.s3o'):
            return os.path.join('objects3d', f)
    return None


_feat_cache = {}
def features(repo=REPO):
    if repo not in _feat_cache:
        d = {}
        for f in glob.glob(os.path.join(repo, 'features/**/*.tdf'), recursive=True):
            t = open(f, errors='replace').read()
            for m in re.finditer(r'\[([^\]]+)\]\s*\{(.*?)\n\}', t, re.S):
                b = m.group(2)
                d[m.group(1).strip().lower()] = dict(tdf=os.path.relpath(f, repo), object=kv(b, 'object'),
                                                     featuredead=kv(b, 'featuredead'),
                                                     footprint=(kv(b, 'footprintx'), kv(b, 'footprintz')))
        _feat_cache[repo] = d
    return _feat_cache[repo]


def corpse_chain(corpse, repo=REPO):
    out, f, seen, F = [], (corpse or '').lower(), set(), features(repo)
    while f and f in F and f not in seen:
        seen.add(f); out.append(dict(feature=f, **F[f])); f = (F[f]['featuredead'] or '').lower()
    return out


def bos_summary(path):
    """piece list + what the script does to each piece (turn/move/spin/hide/show/explode/emit), with axes"""
    t = open(path, errors='replace').read()
    t = re.sub(r'//.*', '', t)
    m = re.search(r'piece\s+([^;]*);', t)
    pieces = [p.strip() for p in m.group(1).split(',')] if m else []
    use = {p: set() for p in pieces}
    for op, pc, ax in re.findall(r'\b(turn|move|spin|stop-spin)\s+(\w+)\s+(?:to|around|along)\s+([xyz])-axis', t):
        use.setdefault(pc, set()).add(f'{op} {ax}')
    for op, pc in re.findall(r'\b(hide|show|explode|emit-sfx\s+\w+\s+from)\s+(\w+)', t):
        use.setdefault(pc, set()).add(op.split()[0])
    for pc in re.findall(r'piecenum\s*=\s*(\w+)\s*;', t):
        use.setdefault(pc, set()).add('query/aimfrom')
    return pieces, {k: sorted(v) for k, v in use.items()}


# ------------------------------------------------------------------ install into the repo
def _set_kv_in_section(text, section, key, value):
    """set key=value; inside [section]{...} of a TDF (case-insensitive section name)."""
    m = re.search(r'(\[%s\]\s*\{)(.*?)(\n\})' % re.escape(section), text, re.S | re.I)
    if not m:
        raise KeyError(section)
    body = m.group(2)
    if re.search(r'(?im)^\s*%s\s*=' % key, body):
        body2 = re.sub(r'(?im)^(\s*%s\s*=)[^;\r\n]*;' % key, lambda mm: mm.group(1) + value + ';', body, count=1)
    else:
        body2 = body + f'\n\t{key}={value};'
    return text[:m.start(2)] + body2 + text[m.end(2):]


def install_unit(unitname, workdir, repo=REPO):
    """copy model + textures for the unit and its corpses into the repo and point the defs at them"""
    info = unit_info(unitname, repo)
    out = os.path.join(workdir, 'out')
    done = []
    for f in os.listdir(out):
        src = os.path.join(out, f)
        if f.endswith('.s3o'):
            shutil.copy(src, os.path.join(repo, 'objects3d', f)); done.append('objects3d/' + f)
        elif f.endswith('.png') and re.search(r'_[12]\.png$', f):
            shutil.copy(src, os.path.join(repo, 'unittextures', f)); done.append('unittextures/' + f)
    fbi = os.path.join(repo, info['fbi'])
    t = open(fbi, newline='').read()
    t = re.sub(r'(?im)^(\s*objectname\s*=)[^;\r\n]*;', lambda m: m.group(1) + unitname + '.s3o;', t, count=1)
    open(fbi, 'w', newline='').write(t); done.append(info['fbi'])
    for c in info['corpse_chain']:
        name = (c['object'] or '').lower()
        if os.path.exists(os.path.join(out, name + '.s3o')):
            p = os.path.join(repo, c['tdf'])
            tt = open(p, newline='').read()
            tt = _set_kv_in_section(tt, c['feature'], 'object', name + '.s3o')   # explicit ext: engine picks 3do/s3o arbitrarily otherwise
            open(p, 'w', newline='').write(tt); done.append(c['tdf'] + f' [{c["feature"]}]')
    return done


def install_heap(name, workdir, repo=REPO):
    """copy heap model/textures; point EVERY feature using object=<name> at <name>.s3o"""
    out = os.path.join(workdir, 'out'); done = []
    for f in os.listdir(out):
        if f.endswith('.s3o'):
            shutil.copy(os.path.join(out, f), os.path.join(repo, 'objects3d', f)); done.append(f)
        elif f.endswith('.png'):
            shutil.copy(os.path.join(out, f), os.path.join(repo, 'unittextures', f)); done.append(f)
    for p in glob.glob(os.path.join(repo, 'features/**/*.tdf'), recursive=True):
        t = open(p, newline='').read()
        t2 = re.sub(r'(?im)^(\s*object\s*=\s*)%s\s*;' % re.escape(name), lambda m: m.group(1) + name + '.s3o;', t)
        if t2 != t:
            open(p, 'w', newline='').write(t2); done.append(os.path.relpath(p, repo))
    return done
