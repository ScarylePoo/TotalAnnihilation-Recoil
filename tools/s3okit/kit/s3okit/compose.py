"""Turn baked maps into the S3O texture pair (numpy only, no Blender needed).

tex1 (<name>_1.png): RGB diffuse with baked AO, A = team colour amount (engine: mix(diffuse, team, a) before lighting)
tex2 (<name>_2.png): R self-illumination, G reflectivity/specular (engine: specular *= G*4), B 0, A 255 (A<0.5 = invisible)

mode: 'unit' | 'wreck' (burnt, no team colour, no lights) | 'heap' (scrap, burnt, rust)
"""
import numpy as np
from PIL import Image
from .common import MATS

PALETTES = {
    # cool, light blue-grey camouflage; reads light against most terrain from above
    'ARM': dict(camo=('#a3afbb', '#95a2af', '#8693a1'), camo_scale=0.085, paint2='#344050', wear='#d0d7de',
                dark='#2b3036', steel='#50565d', accent='#d8a82a', glass='#1d3550', team_base='#3a3a3a',
                lightw='#fff3d2', lightc='#8af3ff', lightr='#ff5a3c'),
    # warm dark gunmetal with ochre hazard accents; darker overall so the factions separate at a glance.
    # (2026-10-25: the first Core unit came out light grey: the painted-in top light lifts mid tones, so the camo is
    # pulled down to ~35 % value and steel lifted, giving light guns/mechanics against dark armour, the inverse of Arm.)
    'CORE': dict(camo=('#5e5850', '#57514a', '#4f4a44'), camo_scale=0.07, paint2='#262421', wear='#a89f93',
                 dark='#1f2022', steel='#8d8982', accent='#d9861c', glass='#3a2414', team_base='#363636',
                 lightw='#ffe2b0', lightc='#ffb347', lightr='#ff4a2a'),
    # generic scrap heaps and anything neutral
    'SCRAP': dict(camo=('#6f706e', '#5b5c5a', '#474846'), camo_scale=0.12, paint2='#3a3b3a', wear='#a9aaa6',
                  dark='#3c3d3e', steel='#6e7175', accent='#8a6a2a', glass='#1b1f24', team_base='#3a3a3a',
                  lightw='#000000', lightc='#000000', lightr='#000000'),
}
# Readability at game distance (a unit is ~30 px on screen): fine detail averages away, so value must come from
# big blocks. VALUE['top'/'side'/'down'] multiply colour by facing (painted-in top light), 'rim' lightens convex
# edges, 'seam' is panel-line strength, 'team' the team-colour alpha.
VALUE = dict(top=1.12, side=0.72, down=0.45, rim=0.18, seam=0.22, team=0.97)

REFLECT = {'paint': 0.16, 'paint2': 0.18, 'dark': 0.24, 'tread': 0.04, 'steel': 0.5, 'team': 0.22, 'black': 0.03,
           'hazard': 0.14, 'glass': 0.7, 'rust': 0.05, 'ash': 0.02}
LIGHTS = {'lightw': 1.0, 'lightc': 0.9, 'lightr': 0.9}

# ------------------------------------------------------------------------------- noise helpers
_rng = np.random.default_rng(7)
_PERM = _rng.permutation(4096); _VAL = _rng.random(4096).astype(np.float32)
def _h(ix, iy, iz): return _VAL[_PERM[(_PERM[(_PERM[ix & 4095] + iy) & 4095] + iz) & 4095]]
def vnoise(p):
    i = np.floor(p).astype(np.int64); f = (p - i).astype(np.float32); u = f * f * (3 - 2 * f)
    x, y, z = i[..., 0], i[..., 1], i[..., 2]; ux, uy, uz = u[..., 0], u[..., 1], u[..., 2]
    L = lambda a, b, t: a + (b - a) * t
    c00 = L(_h(x, y, z), _h(x + 1, y, z), ux); c10 = L(_h(x, y + 1, z), _h(x + 1, y + 1, z), ux)
    c01 = L(_h(x, y, z + 1), _h(x + 1, y, z + 1), ux); c11 = L(_h(x, y + 1, z + 1), _h(x + 1, y + 1, z + 1), ux)
    return L(L(c00, c10, uy), L(c01, c11, uy), uz)
def fbm(p, oct=4, gain=0.5, seed=0.0):
    s, a, n = 0, 1, 0
    for o in range(oct):
        s = s + a * vnoise(p * (2 ** o) + o * 17.3 + seed); n += a; a *= gain
    return s / n
def sm(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)
def hexc(h): return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32)
def srgb2lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lin2srgb(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def compose(npz, out_prefix, final=1024, side='ARM', mode='unit', seed=0, seams=True):
    M = np.load(npz)
    # dilate: every empty texel takes the maps of the nearest baked texel (replaces Cycles' bake margin)
    from scipy.ndimage import distance_transform_edt
    cover = M['cover'][..., 0] > 0
    _, (iy, ix) = distance_transform_edt(~cover, return_indices=True)
    D = lambda a: a[iy, ix]
    pos = D(M['pos'].astype(np.float32)); nrm = D(M['nrm'].astype(np.float32))
    edge = np.clip((1 - D(M['edge'][..., 0].astype(np.float32))) * 9.0, 0, 1)
    aon = np.clip(D(M['aonear'][..., 0].astype(np.float32)), 0, 1)
    aof = np.clip(D(M['aofar'][..., 0].astype(np.float32)), 0, 1)
    mid = np.rint(D(M['id'][..., 0].astype(np.float32)) * 32).astype(int) - 1
    H, W = mid.shape
    tread_phase = np.zeros((H, W), np.float32)          # tread2..4 = tread advanced by 1/4, 2/4, 3/4 of a link
    for k, n in enumerate(('tread2', 'tread3', 'tread4'), 1):
        sel = mid == MATS.index(n)
        tread_phase[sel] = 0.25 * k; mid[sel] = MATS.index('tread')
    pal = PALETTES[side]
    x, y, z = pos[..., 0], pos[..., 1], pos[..., 2]
    up = np.clip(nrm[..., 1], 0, 1)
    sd = seed * 31.7
    camo = fbm(pos * np.float32(pal['camo_scale']), 4, seed=sd)
    fine = fbm(pos * np.float32(1.3), 3, seed=sd)
    grain = fbm(pos * np.float32(5.0), 2, seed=sd)
    brush = fbm(pos * np.array([3.0, 3.0, 0.25], np.float32), 3, seed=sd)
    wearn = fbm(pos * np.float32(2.2), 3, seed=sd)
    def mask(n): return (mid == MATS.index(n))
    m3 = lambda n: mask(n)[..., None]

    wear = sm(0.35, 0.6, np.clip(edge * 1.4 - 0.25 + (wearn - 0.5) * 1.2, 0, 1))
    W3 = wear[..., None]

    # panel seams + rivets projected along the dominant normal axis
    ax = np.argmax(np.abs(nrm), axis=-1)
    pu = np.where(ax == 0, z, x); pv = np.where(ax == 1, z, y)
    row = np.floor(pu / 5.2)
    seam_u = np.abs(np.mod(pu + 2.6, 5.2) - 2.6)
    seam_v = np.abs(np.mod(pv + row * 1.7 + 1.6, 3.2) - 1.6)
    lw = 0.055
    seam = np.clip(np.maximum(1 - sm(lw * 0.5, lw, seam_u), 1 - sm(lw * 0.5, lw, seam_v)), 0, 1) if seams else np.zeros_like(x)
    rv = np.abs(np.mod(pv + row * 1.7 + 1.6, 0.8) - 0.4)
    rivet = (1 - sm(0.05, 0.09, np.hypot(seam_u - 0.22, rv))) * (seam_u < 0.4) if seams else np.zeros_like(x)

    c1, c2, c3 = (hexc(c) for c in pal['camo'])
    t1 = sm(0.475, 0.49, camo)[..., None]; t2 = sm(0.575, 0.59, camo)[..., None]
    paint = (c1 * (1 - t1) + c2 * t1) * (1 - t2) + c3 * t2
    paint = paint * (0.94 + 0.12 * fine[..., None]) * (0.97 + 0.06 * grain[..., None])
    paint = paint * (1 - VALUE['seam'] * seam[..., None]) + 0.06 * rivet[..., None]
    paint = paint * (1 - W3) + hexc(pal['wear']) * W3
    paint2 = hexc(pal['paint2']) * (0.92 + 0.16 * fine[..., None]) * (1 - 0.6 * VALUE['seam'] * seam[..., None])
    paint2 = paint2 * (1 - W3) + hexc(pal['wear']) * W3
    dark = hexc(pal['dark']) * (0.9 + 0.2 * fine[..., None]) * (0.95 + 0.1 * grain[..., None]) * (1 - 0.35 * seam[..., None])
    dark = dark * (1 - W3) + hexc('#9aa1a8') * W3
    link = np.mod(z * 1.35 + 0.15 * x + tread_phase, 1.0)
    grouser = sm(0.05, 0.12, link) - sm(0.38, 0.45, link)
    pin = np.where(np.abs(nrm[..., 0]) > 0.7, sm(0.6, 0.8, np.mod(y * 1.6, 1.0)) * 0.5, 0)
    tread = hexc('#2c2b29') * (1 - grouser[..., None]) + hexc('#4d4a45') * grouser[..., None]
    tread = tread * (1 - pin[..., None] * 0.6) * (0.9 + 0.2 * grain[..., None])
    tread = tread * (1 - edge[..., None] * 0.5) + hexc('#77736c') * (edge[..., None] * 0.5)
    steel = hexc(pal['steel']) * (0.85 + 0.3 * brush[..., None])
    steel = steel * (1 - W3) + hexc('#c9ced3') * W3
    team = hexc(pal['team_base']) * np.ones((H, W, 1), np.float32)
    haz = sm(0.48, 0.52, np.mod((np.abs(x) + z) * 0.75, 1.0))
    hazard = hexc(pal['accent']) * (1 - haz[..., None]) + hexc('#232220') * haz[..., None]
    hazard = hazard * (0.93 + 0.14 * fine[..., None]) * (1 - W3) + hexc('#b9bdc0') * W3
    glass = hexc(pal['glass']) * (0.8 + 0.4 * up[..., None]) + 0.25 * sm(0.7, 0.95, brush)[..., None]
    rust = hexc('#6b3d22') * (0.7 + 0.6 * fine[..., None]) * (0.85 + 0.3 * grain[..., None])
    ash = hexc('#3b342c') * (0.75 + 0.5 * fine[..., None]) * (0.85 + 0.3 * grain[..., None])

    col = np.zeros((H, W, 3), np.float32)
    for n, c in [('paint', paint), ('paint2', paint2), ('dark', dark), ('tread', tread), ('steel', steel),
                 ('team', team), ('hazard', hazard), ('glass', glass), ('rust', rust), ('ash', ash)]:
        col = np.where(m3(n), c, col)
    lights = np.zeros((H, W), bool)
    for n in LIGHTS:
        col = np.where(m3(n), hexc(pal[n]), col); lights |= mask(n)
    col = np.where(m3('black'), hexc('#121315'), col)

    dust = np.clip(sm(4.0, 0.3, y) * 0.55 + (1 - aof) * 0.35 + up * 0.08, 0, 1) * (0.55 + 0.6 * fine)
    dust = np.clip(dust, 0, 0.75)
    dust = np.where(mask('tread'), np.clip(dust * 1.3, 0, 0.85), dust)
    dust = np.where(lights | mask('ash'), 0, dust)
    col = col * (1 - dust[..., None]) + hexc('#6f6656') * dust[..., None]

    emi = np.zeros((H, W), np.float32)
    for n, v in LIGHTS.items():
        emi = np.where(mask(n), v, emi)
    refl = np.zeros((H, W), np.float32)
    for n, v in REFLECT.items():
        refl = np.where(mask(n), v, refl)
    refl = refl + wear * 0.25 * (~mask('tread'))
    tc = np.where(mask('team'), VALUE['team'] * (1 - 0.3 * wear) * (1 - 0.3 * dust), 0)

    if mode in ('wreck', 'heap'):
        # burnt: desaturate, darken, soot blotches, scorched edges, rust in crevices; no team colour or lights
        g = col.mean(-1, keepdims=True)
        col = (col * 0.35 + g * 0.65) * 0.62
        soot = sm(0.42, 0.62, fbm(pos * np.float32(0.35), 4, seed=sd + 5))
        scorch = np.clip(soot * 0.85 + (1 - aof) * 0.4 + sm(0.3, 0.9, edge) * 0.3, 0, 1)
        col = col * (1 - scorch[..., None] * 0.8) + hexc('#151312') * scorch[..., None] * 0.8
        rustm = np.clip(sm(0.55, 0.7, fbm(pos * np.float32(0.9), 4, seed=sd + 9)) + (1 - aon) * 0.5, 0, 1) * (1 - scorch * 0.6)
        col = col * (1 - rustm[..., None] * 0.7) + rust * rustm[..., None] * 0.7
        bare = sm(0.5, 0.8, wear + sm(0.7, 0.8, fbm(pos * np.float32(3.0), 2, seed=sd + 3)) * 0.6)
        col = col * (1 - bare[..., None] * 0.5) + hexc('#77736d') * bare[..., None] * 0.5
        emi[:] = 0; tc[:] = 0
        refl = np.clip(refl * 0.35 + bare * 0.12, 0, 1) * (1 - scorch * 0.7)
        col = np.where(m3('ash'), ash, col)

    # painted-in lighting: lit tops, darker sides, dark undersides, bright convex rims -> shape survives distance
    ny = nrm[..., 1]
    face = np.where(ny >= 0, VALUE['side'] + (VALUE['top'] - VALUE['side']) * np.clip(ny, 0, 1) ** 0.8,
                    VALUE['side'] + (VALUE['down'] - VALUE['side']) * np.clip(-ny, 0, 1))
    keep = lights | mask('black') | mask('ash')
    col = np.where(keep[..., None], col, col * face[..., None])
    rim = VALUE['rim'] * sm(0.25, 0.7, edge) * (0.4 + 0.6 * np.clip(ny, 0, 1))
    col = np.where(keep[..., None], col, col + rim[..., None] * (1 - col))
    occ = (0.3 + 0.7 * aof ** 1.4) * (0.45 + 0.55 * aon)
    occ = np.where(lights & (mode == 'unit'), 1.0, occ)
    col = lin2srgb(srgb2lin(col) * occ[..., None])
    refl = np.clip(refl * (1 - dust * 0.8) * (0.4 + 0.6 * aof), 0, 1)

    def save(arr, path, mode_):
        im = Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8), mode_)
        if final != W:   # per channel: PIL premultiplies alpha when resizing RGBA, which blackens RGB where A=0
            im = Image.merge(mode_, [c.resize((final, final), Image.LANCZOS) for c in im.split()])
        im.save(path)
    save(np.dstack([col, tc]), out_prefix + '_1.png', 'RGBA')
    save(np.dstack([emi, refl, np.zeros_like(emi), np.ones_like(emi)]), out_prefix + '_2.png', 'RGBA')
    return dict(texture=final)
