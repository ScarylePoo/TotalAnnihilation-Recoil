#!/usr/bin/env python3
"""Faction pictures and emblems for the Slate faction chooser.

The chooser (luaui/slate/widgets/slate_factionchooser.lua) shows each
faction's picture at 392x220 dp; one dp is one pixel at 1920x1080 and scales
with the screen. The pictures are drawn at four times that, 1568x880, so they
stay sharp on anything up to 8K and are scaled down below it. They are
opaque, so they need no premultiplied alpha (see theme.rcss).

The emblems are also saved on their own, 1024x1024 with transparency, for
use elsewhere in the UI. Those are premultiplied, as RmlUi needs.

Everything is drawn with Pillow: the logos are polygons (measured from the
reference picture in Claude Space, see the emblems section) rendered at SS
times the final size and scaled down for anti-aliasing.

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

FACTIONS = [
    # file stem, name, tagline, faction colour (`color` in slate_game.lua), symbol colour
    ("arm", "ARM", "SPEED  ·  RANGE  ·  NUMBERS", (0x4a, 0x86, 0xe0), (0x3d, 0x7e, 0xf0)),
    ("core", "CORE", "ARMOUR  ·  WEIGHT  ·  FIREPOWER", (0xd8, 0x4a, 0x3c), (0xe0, 0x3c, 0x30)),
]


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


# ---------------------------------------------------------------- emblems
# The two logos as polygons, in the pixel coordinates of the reference
# picture they were measured from ("Arm and core logo shapes.png" in Claude
# Space: the logos drawn as glowing outlines; the lit outline was
# thresholded and everything the outside could not reach was taken as the
# shape, then the straight edges and the circle were read off that mask).

def _mirror(pts, cx):
    return [(2 * cx - x, y) for x, y in pts]


def _arc(cx, cy, r, a0, a1, n=64):
    """Points on a circle from angle a0 to a1 (degrees, y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def shapes_arm():
    """A rhombus in a channel, framed by two bars split at the top, a V below,
    and swallowtail wings either side. Mirror axis x = 196."""
    cx = 196.0
    rhombus = [(cx, 61), (252, 141), (cx, 221), (140, 141)]

    # upper-left piece: the bar (inner edge through (184,50)-(148,100), outer
    # edge through (176,10)-(116,100), cut vertically at x=188 near the top)
    # grown into the upper wing (y 103..133, swallowtail end 10..24)
    def xi(y):
        return 184 - 0.72 * (y - 50)

    def xo(y):
        return 176 - 0.6667 * (y - 10)

    upper_left = [(xo(10), 10), (188, 10), (188, 50 - (188 - 184) / 0.72), (xi(133), 133),
                  (24, 133), (10, 103), (xo(103), 103)]

    # lower piece: the V (inner edge through (160,200) at 0.7 per y, outer edge
    # through (112,180) at 0.64 per y) with the lower wings (y 149..179)
    def vi(y):
        return 160 + 0.7 * (y - 200)

    def vo(y):
        return 112 + 0.64 * (y - 180)

    y_in = 200 + (cx - 160) / 0.7
    y_out = 180 + (cx - 112) / 0.64
    left = [(10, 179), (24, 149), (vi(149), 149), (cx, y_in)]
    right = _mirror([(vi(149), 149), (24, 149), (10, 179), (vo(179), 179)], cx)
    lower = left + right + [(cx, y_out), (vo(179), 179)]

    polys = [rhombus, upper_left, _mirror(upper_left, cx), lower]
    return polys, (10, 10, 382, y_out)


def shapes_core():
    """Two ears and a chevron body with legs, around an inner sector, all on
    one circle (centre (151,134), radius 129). Mirror axis x = 151."""
    cx, cy, r = 151.0, 134.0, 129.0

    def on_circle_y(x, upper):   # y of the circle at x
        dy = math.sqrt(max(0.0, r * r - (x - cx) ** 2))
        return cy - dy if upper else cy + dy

    # body: outer edge x + y = 176 from the apex to the shoulder, legs tapering
    # to a point (outer edge 0.28 per y, inner edge vertical at x=56), inner
    # edge x + y = 283 up to the inner apex
    apex = (cx, 176 - cx)
    shoulder = (6.0, 170.0)
    leg_in = 56.0
    tip_y = shoulder[1] + (leg_in - shoulder[0]) / 0.28
    inner_apex = (cx, 283 - cx)
    body_left = [shoulder, (leg_in, tip_y), (leg_in, 283 - leg_in), inner_apex]
    body = [apex] + body_left + _mirror(list(reversed(body_left[:-1])), cx)

    # inner sector: 45-degree edges from (151,148) down to the circle
    s_apex = (cx, 148.0)
    # x = cx - (y - 148) meets the circle at y = 232
    y_c = 232.0
    x_c = cx - (y_c - 148)
    a0 = math.degrees(math.atan2(y_c - cy, x_c - cx))
    a1 = 180 - a0
    sector = [s_apex] + _arc(cx, cy, r, a0, a1)

    # left ear: inside the circle, left of x=128, above the line x + y = 154
    x_in = 128.0
    top_y = on_circle_y(x_in, True)
    # the line meets the circle at (22,132)
    low = (22.0, 132.0)
    a_top = math.degrees(math.atan2(top_y - cy, x_in - cx))
    a_low = math.degrees(math.atan2(low[1] - cy, low[0] - cx))
    if a_low > a_top:
        a_low -= 360
    ear = _arc(cx, cy, r, a_top, a_low) + [(x_in, 154 - x_in), (x_in, top_y)]

    polys = [body, sector, ear, _mirror(ear, cx)]
    return polys, (6, apex[1], 296, tip_y)


SHAPES = {"arm": shapes_arm, "core": shapes_core}


def emblem(stem, box, symbol):
    """The logo drawn to fit a box pixels square: a solid fill in the faction's
    symbol colour with a lighter rim, anti-aliased by supersampling."""
    polys, (x0, y0, x1, y1) = SHAPES[stem]()
    w, h = x1 - x0, y1 - y0
    scale = box * SS / max(w, h)
    px = box * SS
    ox = (px - w * scale) / 2 - x0 * scale
    oy = (px - h * scale) / 2 - y0 * scale

    mask = Image.new("L", (px, px), 0)
    d = ImageDraw.Draw(mask)
    for poly in polys:
        d.polygon([(ox + x * scale, oy + y * scale) for x, y in poly], fill=255)

    # the rim: erode the shape at 1x (a big MinFilter at SS is far too slow)
    # and scale the eroded mask back up; its soft edge is a fine inner edge
    rim = max(2, int(round(box * 0.012)))
    small = mask.resize((box, box), Image.BOX)
    inner = small.filter(ImageFilter.MinFilter(rim * 2 + 1)).resize((px, px), Image.BILINEAR)
    inner = inner.point(lambda v: 255 if v >= 128 else 0)

    light = mix(symbol, TEXT, 0.55)
    img = Image.new("RGBA", (px, px), light + (0,))
    img.putalpha(mask)
    fill = Image.new("RGBA", (px, px), symbol + (255,))
    img.paste(fill, (0, 0), inner)
    img = img.resize((box, box), Image.LANCZOS)
    return img


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
    em = emblem(stem, EMBLEM, symbol)
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
        premultiplied(emblem(stem, EMBLEM_FILE, symbol)).save(path, optimize=True)
        print(path)


if __name__ == "__main__":
    main()
