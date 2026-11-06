#!/usr/bin/env python3
"""Placeholder faction pictures for the Slate faction chooser.

The chooser (luaui/slate/widgets/slate_factionchooser.lua) shows each
faction's picture at 392x220 dp. One dp is one pixel at 1920x1080 and scales
with the screen (two pixels at 3840x2160), so the pictures are made at twice
that, 784x440, which stays sharp up to 4K and is scaled down below it.

They are opaque, so they need no premultiplied alpha (see theme.rcss).
Replace them with real art of the same size and keep the file names, or
change `picture` in luaui/slate/configs/slate_game.lua.

    source ~/.venvs/s3o/bin/activate && python3 tools/faction_placeholders.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "luaui", "slate", "images", "factions")
FONT_BOLD = os.path.join(ROOT, "luaui", "slate", "fonts", "Saira_SemiCondensed-Bold.ttf")
FONT_SEMI = os.path.join(ROOT, "luaui", "slate", "fonts", "Saira_SemiCondensed-SemiBold.ttf")

W, H = 784, 440  # 2x the 392x220 dp the chooser shows

FACTIONS = [
    # file, name, sub, colour (the same as `color` in slate_game.lua)
    ("arm.png", "ARM", "Arm Commander", (0x4a, 0x86, 0xe0)),
    ("core.png", "CORE", "Core Commander", (0xd8, 0x4a, 0x3c)),
]

BG = (13, 14, 16)
TEXT = (244, 245, 247)
MUTED = (181, 186, 193)


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def make(name, sub, colour):
    img = Image.new("RGB", (W, H), BG)
    px = img.load()
    # a soft wash of the faction colour from the lower left
    for y in range(H):
        for x in range(W):
            d = ((x / W) * 0.65 + (1 - y / H) * 0.35)
            t = max(0.0, 0.42 - d * 0.42)
            px[x, y] = mix(BG, colour, t)
    d = ImageDraw.Draw(img)

    # diagonal stripes across the right end, very faint
    stripe = mix(BG, colour, 0.10)
    for k in range(-H, W, 44):
        d.polygon([(W * 0.58 + k, H), (W * 0.58 + k + 18, H), (W * 0.58 + k + 18 + H, 0), (W * 0.58 + k + H, 0)], fill=stripe)
    # a band of the colour along the bottom
    d.rectangle([0, H - 10, W, H], fill=colour)

    big = ImageFont.truetype(FONT_BOLD, 150)
    mid = ImageFont.truetype(FONT_SEMI, 34)
    small = ImageFont.truetype(FONT_BOLD, 22)

    d.text((48, 72), name, font=big, fill=TEXT)
    d.text((54, 268), sub.upper(), font=mid, fill=mix(MUTED, colour, 0.35))

    # the placeholder mark: an outlined tag in the top right corner
    tag = "PLACEHOLDER"
    tb = d.textbbox((0, 0), tag, font=small)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 16, 10
    x2, y1 = W - 32, 32
    x1, y2 = x2 - tw - 2 * pad_x, y1 + th + 2 * pad_y
    d.rounded_rectangle([x1, y1, x2, y2], radius=8, outline=(242, 194, 48), width=3)
    d.text((x1 + pad_x - tb[0], y1 + pad_y - tb[1]), tag, font=small, fill=(242, 194, 48))

    d.text((54, H - 62), "%d x %d  -  replace with faction art" % (W, H), font=ImageFont.truetype(FONT_SEMI, 20), fill=MUTED)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    for fname, name, sub, colour in FACTIONS:
        path = os.path.join(OUT, fname)
        make(name, sub, colour).save(path, optimize=True)
        print(path)


if __name__ == "__main__":
    main()
