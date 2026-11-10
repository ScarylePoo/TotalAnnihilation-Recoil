#!/usr/bin/env python3
"""Faction pictures and emblems for the Slate faction chooser.

The chooser (luaui/slate/widgets/slate_factionchooser.lua) shows each
faction's picture at 392x220 dp; one dp is one pixel at 1920x1080 and scales
with the screen. The pictures are drawn at four times that, 1568x880, so they
stay sharp on anything up to 8K and are scaled down below it. They are
opaque, so they need no premultiplied alpha (see theme.rcss).

The emblems are also saved on their own, 1024x1024 with transparency, for
use elsewhere in the UI. Those are premultiplied, as RmlUi needs.

Everything is drawn with Pillow: shapes are rendered at SS times the final
size and scaled down for anti-aliasing. The original Total Annihilation
marks are not copied; these are new designs in the factions' colours.

    python3 tools/faction_logos.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "luaui", "slate", "images", "factions")
FONT_BOLD = os.path.join(ROOT, "luaui", "slate", "fonts", "Saira_SemiCondensed-Bold.ttf")
FONT_SEMI = os.path.join(ROOT, "luaui", "slate", "fonts", "Saira_SemiCondensed-SemiBold.ttf")

W, H = 1568, 880       # 4x the 392x220 dp the chooser shows
SS = 4                 # supersampling for the vector shapes
EMBLEM = 640           # emblem diameter in the picture
EMBLEM_FILE = 1024     # emblem-only file size

BG = (13, 14, 16)
TEXT = (244, 245, 247)
MUTED = (181, 186, 193)
STEEL = (214, 221, 230)   # the metal ring both emblems share

FACTIONS = [
    # file stem, name, tagline, faction colour (`color` in slate_game.lua), symbol colour
    ("arm", "ARM", "SPEED  ·  RANGE  ·  NUMBERS", (0x4a, 0x86, 0xe0), (0x8c, 0xb8, 0xff)),
    ("core", "CORE", "ARMOUR  ·  WEIGHT  ·  FIREPOWER", (0xd8, 0x4a, 0x3c), (0xf0, 0x5a, 0x48)),
]


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


# ---------------------------------------------------------------- emblems
# Each emblem is drawn into a unit circle (radius 1, centre 0) on an RGBA
# canvas of `size` pixels, at SS times that and scaled down.

def _canvas(size):
    px = size * SS
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    scale = px / 2.0

    def P(x, y):
        return (scale + x * scale * 0.98, scale + y * scale * 0.98)

    return img, P


def _ring(draw, P, r_out, r_in, colour):
    draw.ellipse([P(-r_out, -r_out), P(r_out, r_out)], fill=colour)
    draw.ellipse([P(-r_in, -r_in), P(r_in, r_in)], fill=(0, 0, 0, 0))


def _polygon(draw, P, pts, colour):
    draw.polygon([P(x, y) for x, y in pts], fill=colour)


def _rotate(pts, a):
    c, s = math.cos(a), math.sin(a)
    return [(x * c - y * s, x * s + y * c) for x, y in pts]


def emblem_arm(size, symbol):
    """A steel ring around an arrow pointing up: the Arm rising."""
    img, P = _canvas(size)
    d = ImageDraw.Draw(img)
    steel = STEEL + (255,)
    col = symbol + (255,)

    _ring(d, P, 0.98, 0.84, steel)
    # two small breaks in the ring at the sides, so it reads as made, not drawn
    for sx in (-1, 1):
        _polygon(d, P, [(sx * 0.80, -0.045), (sx * 1.02, -0.045), (sx * 1.02, 0.045), (sx * 0.80, 0.045)], (0, 0, 0, 0))

    # arrow head: a chevron with a flat inner apex
    _polygon(d, P, [(-0.66, 0.16), (0, -0.72), (0.66, 0.16), (0.50, 0.30), (0, -0.40), (-0.50, 0.30)], col)
    # shaft, with a slot of light down the middle
    _polygon(d, P, [(-0.11, -0.26), (0.11, -0.26), (0.11, 0.66), (-0.11, 0.66)], col)
    _polygon(d, P, [(-0.025, -0.10), (0.025, -0.10), (0.025, 0.50), (-0.025, 0.50)], (0, 0, 0, 0))
    # a light edge along the top of the chevron
    _polygon(d, P, [(-0.66, 0.16), (0, -0.72), (0.66, 0.16), (0.62, 0.20), (0, -0.66), (-0.62, 0.20)], TEXT + (255,))

    return img.resize((size, size), Image.LANCZOS)


def emblem_core(size, symbol):
    """A steel gear around a red hexagonal reactor: the Core."""
    img, P = _canvas(size)
    d = ImageDraw.Draw(img)
    steel = STEEL + (255,)
    col = symbol + (255,)
    dark = mix(BG, symbol, 0.25) + (255,)

    # gear: ring plus twelve teeth
    _ring(d, P, 0.84, 0.70, steel)
    tooth = [(-0.11, -0.80), (0.11, -0.80), (0.085, -0.99), (-0.085, -0.99)]
    for k in range(12):
        _polygon(d, P, _rotate(tooth, k * math.pi / 6), steel)

    # hexagon, flat top, with a dark centre
    hexa = [(math.cos(a) * 0.56, math.sin(a) * 0.56) for a in (math.radians(30 + 60 * k) for k in range(6))]
    hexb = [(math.cos(a) * 0.46, math.sin(a) * 0.46) for a in (math.radians(30 + 60 * k) for k in range(6))]
    _polygon(d, P, hexa, col)
    _polygon(d, P, hexb, dark)
    # the reactor: a disc with three vents cut from it
    d.ellipse([P(-0.27, -0.27), P(0.27, 0.27)], fill=col)
    vent = [(-0.035, -0.30), (0.035, -0.30), (0.035, -0.10), (-0.035, -0.10)]
    for k in range(3):
        _polygon(d, P, _rotate(vent, k * 2 * math.pi / 3 + math.pi), dark)
    d.ellipse([P(-0.09, -0.09), P(0.09, 0.09)], fill=TEXT + (255,))

    return img.resize((size, size), Image.LANCZOS)


EMBLEMS = {"arm": emblem_arm, "core": emblem_core}


# ---------------------------------------------------------------- pictures

def background(colour, cx, cy):
    """Dark glass with a wash of the faction colour and a glow behind the emblem."""
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    bg = np.array(BG, np.float32)
    col = np.array(colour, np.float32)

    # a soft wash from the lower left, as the rest of Slate's panels have
    dist = (xs / W) * 0.65 + (1 - ys / H) * 0.35
    t = np.clip(0.34 - dist * 0.34, 0, 1)
    img = bg + (col - bg) * t[..., None]

    # a glow behind the emblem
    r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / (EMBLEM * 0.75)
    g = np.clip(1 - r, 0, 1) ** 2 * 0.30
    img = img + (col - img) * g[..., None]

    out = Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8), "RGB")

    # faint diagonal stripes across the right end
    stripes = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stripes)
    for k in range(-H, W, 88):
        x0 = W * 0.52 + k
        sd.polygon([(x0, H), (x0 + 36, H), (x0 + 36 + H, 0), (x0 + H, 0)], fill=255)
    tint = Image.new("RGB", (W, H), mix(BG, colour, 0.5))
    out = Image.composite(Image.blend(out, tint, 0.14), out, stripes)
    return out


def spaced_text(draw, xy, text, font, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x - spacing


def spaced_width(draw, text, font, spacing):
    return sum(draw.textlength(ch, font=font) for ch in text) + spacing * (len(text) - 1)


def picture(stem, name, tagline, colour, symbol):
    cx, cy = 400, H // 2 - 8
    img = background(colour, cx, cy)

    # the emblem, with a soft shadow under it
    em = EMBLEMS[stem](EMBLEM, symbol)
    shadow = Image.new("RGBA", (EMBLEM + 80, EMBLEM + 80), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (40, 48), em)
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    img.paste(shadow, (cx - EMBLEM // 2 - 40, cy - EMBLEM // 2 - 40), shadow)
    img.paste(em, (cx - EMBLEM // 2, cy - EMBLEM // 2), em)

    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(FONT_BOLD, 330)
    small = ImageFont.truetype(FONT_SEMI, 40)

    x0 = 780
    # the name, sat on a baseline so ARM and CORE line up the same way
    asc, desc = big.getmetrics()
    bb = d.textbbox((0, 0), name, font=big)
    name_h = bb[3] - bb[1]
    top = cy - 150 - bb[1]
    d.text((x0 - bb[0], top), name, font=big, fill=TEXT)
    name_w = bb[2] - bb[0]

    # a rule in the faction colour, then the tagline
    rule_y = top + bb[1] + name_h + 44
    d.rectangle([x0, rule_y, x0 + name_w, rule_y + 6], fill=colour)
    tag_fill = mix(MUTED, colour, 0.45)
    spaced_text(d, (x0, rule_y + 34), tagline, small, tag_fill, 3)

    # a band of the faction colour along the bottom
    d.rectangle([0, H - 20, W, H], fill=colour)
    return img


def premultiplied(img):
    a = np.asarray(img.convert("RGBA")).astype(np.float32)
    alpha = a[..., 3:4] / 255.0
    a[..., :3] *= alpha
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8), "RGBA")


def main():
    os.makedirs(OUT, exist_ok=True)
    for stem, name, tagline, colour, symbol in FACTIONS:
        path = os.path.join(OUT, stem + ".png")
        picture(stem, name, tagline, colour, symbol).save(path, optimize=True)
        print(path)
        path = os.path.join(OUT, stem + "_emblem.png")
        premultiplied(EMBLEMS[stem](EMBLEM_FILE, symbol)).save(path, optimize=True)
        print(path)


if __name__ == "__main__":
    main()
