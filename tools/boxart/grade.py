#!/usr/bin/env python3
"""Box-art grade for the commander renders (tools/boxart/run_boxart.sh).

    grade.py arm|core in.png out.png [--sky 0.45] [--vignette 0.55] [--bloom 0.6] [--grain 0.025]

Contrast S-curve, a split tone per faction (Arm: cool shadows, warm highlights; Core: deep red shadows, ember
highlights), a graduated filter that darkens the sky toward the top, bloom on the bright parts (D-Gun, nano, lights),
a vignette, a light unsharp mask and fine grain. Works on 8-bit sRGB, output PNG or JPEG by extension.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter

LOOKS = {
    # shadows tint, highlights tint, saturation, contrast
    "arm":  dict(shadow=(0.80, 0.92, 1.12), high=(1.06, 1.00, 0.92), sat=1.10, contrast=0.22),
    "core": dict(shadow=(1.10, 0.78, 0.72), high=(1.08, 0.94, 0.82), sat=1.12, contrast=0.28),
}


def s_curve(x, amount):
    # blend toward a smoothstep around 0.5
    return x + amount * (x * x * (3 - 2 * x) - x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("look", choices=LOOKS)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--sky", type=float, default=0.45, help="darkening at the top edge")
    ap.add_argument("--vignette", type=float, default=0.55)
    ap.add_argument("--bloom", type=float, default=0.6)
    ap.add_argument("--grain", type=float, default=0.02)
    a = ap.parse_args()
    L = LOOKS[a.look]

    im = Image.open(a.src).convert("RGB")
    w, h = im.size
    x = np.asarray(im).astype(np.float32) / 255.0

    # bloom: what is bright, blurred wide, added back (screen)
    lum = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    bright = np.clip((lum - 0.72) / 0.28, 0, 1)[..., None] * x
    b8 = Image.fromarray((bright * 255).astype(np.uint8))
    glow = np.zeros_like(x)
    for r, wgt in ((w / 400, 0.5), (w / 120, 0.35), (w / 40, 0.25)):
        glow += wgt * np.asarray(b8.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0
    x = 1 - (1 - x) * (1 - np.clip(glow * a.bloom, 0, 1))

    # graduated filter over the sky: darkest at the top, gone by mid-frame
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    grad = 1 - a.sky * np.clip(1 - yy / 0.55, 0, 1) ** 1.6
    x = x * grad

    # contrast and split tone
    x = s_curve(np.clip(x, 0, 1), L["contrast"])
    lum = (x @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    tone = np.array(L["shadow"], np.float32) * (1 - lum) + np.array(L["high"], np.float32) * lum
    x = x * tone
    lum = (x @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    x = lum + (x - lum) * L["sat"]

    # vignette
    xx = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    yv = np.linspace(-1, 1, h, dtype=np.float32)[:, None]
    d = np.sqrt((xx * 0.85) ** 2 + yv ** 2)
    x = x * (1 - a.vignette * np.clip((d - 0.45) / 0.95, 0, 1) ** 1.8)[..., None]

    # grain
    rng = np.random.default_rng(7)
    x = x + rng.normal(0, a.grain, (h, w, 1)).astype(np.float32) * (0.4 + 0.6 * (1 - lum))

    out = Image.fromarray((np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8))
    out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if a.dst.lower().endswith((".jpg", ".jpeg")):
        out.save(a.dst, quality=94, subsampling=0)
    else:
        out.save(a.dst, optimize=True)


if __name__ == "__main__":
    main()
