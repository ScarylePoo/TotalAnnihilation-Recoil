"""PNG -> DDS (DXT1 / DXT5) with a full mip chain, for unit textures.

Orientation: the image is written as-is (top row first), NOT flipped. The engine loads unit DDS through nv_dds with a
vertical flip, which lines it up with S3O texcoords written straight from Blender (texv = blender v). Verified in game
by the user on the Flash (2026-10-25): PNG + flipped UVs needed a manual fix; DDS + unflipped UVs is correct.

Formats: tex1 = DXT5 (alpha = team colour mask), tex2 = DXT1 (R self-illum, G reflectivity; alpha must be opaque).
Mips are box-filtered per channel (never premultiplied: team alpha must not darken RGB), down to 1x1.
Pillow encodes each level; the levels are concatenated under one header with the mipmap count set.
"""
import io, struct
import numpy as np
from PIL import Image

DDSD_MIPMAPCOUNT = 0x20000
DDSCAPS_COMPLEX, DDSCAPS_MIPMAP = 0x8, 0x400000


def _mips(a):
    """a: HxWxC uint8 -> list of float32 levels, box filter, down to 1x1."""
    lv = [a.astype(np.float32)]
    while max(lv[-1].shape[:2]) > 1:
        x = lv[-1]
        h, w = x.shape[:2]
        if h > 1:
            x = (x[0::2] + x[1::2]) * 0.5 if h % 2 == 0 else x
        if w > 1:
            x = (x[:, 0::2] + x[:, 1::2]) * 0.5 if w % 2 == 0 else x
        lv.append(x)
    return lv


def _encode(level, fmt):
    a = np.clip(np.rint(level), 0, 255).astype(np.uint8)
    h, w = a.shape[:2]
    if h < 4 or w < 4:   # BC blocks are 4x4: pad tiny levels by edge replication, the block is what gets stored
        a = np.pad(a, ((0, max(0, 4 - h)), (0, max(0, 4 - w)), (0, 0)), mode='edge')
    b = io.BytesIO()
    Image.fromarray(a, 'RGBA').save(b, 'DDS', pixel_format=fmt)
    d = b.getvalue()
    assert d[:4] == b'DDS ' and struct.unpack_from('<I', d, 4)[0] == 124
    hdr, data = d[:128], d[128:]
    return hdr, data


def write(png_or_array, out_path, fmt):
    """fmt: 'DXT5' (tex1) or 'DXT1' (tex2)."""
    if isinstance(png_or_array, str):
        a = np.asarray(Image.open(png_or_array).convert('RGBA'))
    else:
        a = np.asarray(png_or_array)
    if fmt == 'DXT1':
        a = a.copy(); a[..., 3] = 255
    h, w = a.shape[:2]
    if (h & (h - 1)) or (w & (w - 1)):
        raise ValueError(f'{out_path}: texture must be a power of two ({w}x{h})')
    levels = _mips(a)
    hdr, data0 = _encode(levels[0], fmt)
    blocks = [data0] + [_encode(l, fmt)[1] for l in levels[1:]]
    hdr = bytearray(hdr)
    flags = struct.unpack_from('<I', hdr, 8)[0] | DDSD_MIPMAPCOUNT
    struct.pack_into('<I', hdr, 8, flags)
    struct.pack_into('<I', hdr, 28, len(levels))                                  # dwMipMapCount
    caps = struct.unpack_from('<I', hdr, 108)[0] | DDSCAPS_COMPLEX | DDSCAPS_MIPMAP
    struct.pack_into('<I', hdr, 108, caps)
    with open(out_path, 'wb') as f:
        f.write(bytes(hdr)); [f.write(b) for b in blocks]
    return dict(path=out_path, fmt=fmt, size=(w, h), mips=len(levels))


def convert_pair(prefix):
    """<prefix>_1.png -> <prefix>_1.dds (DXT5), <prefix>_2.png -> <prefix>_2.dds (DXT1)."""
    return [write(prefix + '_1.png', prefix + '_1.dds', 'DXT5'), write(prefix + '_2.png', prefix + '_2.dds', 'DXT1')]
