#!/usr/bin/env python3
"""TA:Recoil HD cursors: TA's cursor set redrawn as anti-aliased vector art with smooth animation.

    python3 tools/cursors/cursors.py [--preview DIR]

Writes, for every size in SIZES (px of a centred cursor's canvas):
    anims/hd/<size>/<cursor>_<i>.png       frames (RGBA)
    anims/hd/<size>/<cursor>.txt           engine spec file: per-frame image + length, hotspot
and the default set (DEFAULT_SIZE) as anims/<cursor>.txt, which the engine reads before any <cursor>_<i>.bmp/png.
luaui/widgets/gui_cursor_size.lua swaps in the size that suits the screen (Spring.ReplaceMouseCursor).

Every cursor is drawn on a 64 x 64 design grid (the pointer on 32 x 48), centre (32, 32) = the hotspot, at
SS x the output size, then downsampled. Shapes get a vertical gradient fill, a dark outline and, where wanted, a
soft glow; designs follow TA's originals (same symbols and colours), animated at ~25 fps.
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIZES = [32, 48, 64, 96]
DEFAULT_SIZE = 48
SS = 4

OUT = (6, 8, 12)
SILVER = ((255, 255, 255), (150, 160, 178))
GREEN = ((170, 255, 130), (25, 125, 35))
RED = ((255, 150, 70), (175, 15, 5))
YELLOW = ((255, 252, 170), (235, 160, 0))
ORANGE = ((255, 220, 120), (230, 90, 10))
CYAN = ((200, 252, 255), (25, 130, 200))
STEEL = ((215, 232, 245), (55, 90, 130))
BLUE = ((150, 170, 255), (55, 60, 210))
GREY = ((215, 218, 222), (105, 110, 118))
PURPLE = ((205, 160, 255), (95, 40, 190))


def lerp(a, b, t):
    return a + (b - a) * t


def lerpc(c1, c2, t):
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(len(c1)))


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


class Canvas:
    def __init__(self, size, w=64, h=64):
        self.w, self.h = w, h
        self.px = size                 # output px for 64 design units
        self.k = size * SS / 64.0      # supersampled px per design unit
        self.W, self.H = int(round(w * self.k)), int(round(h * self.k))
        self.img = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))

    # --- coordinates
    def P(self, p):
        return (p[0] * self.k, p[1] * self.k)

    def mask(self, fn):
        m = Image.new("L", (self.W, self.H), 0)
        fn(ImageDraw.Draw(m), self)
        return m

    # --- compositing
    def _fill(self, m, fill, alpha=1.0):
        if isinstance(fill[0], int):
            top, bot = fill, fill
        else:
            top, bot = fill
        bb = m.getbbox()
        if not bb:
            return
        y0, y1 = bb[1], max(bb[3], bb[1] + 1)
        grad = Image.new("RGBA", (1, self.H))
        for y in range(self.H):
            t = min(1.0, max(0.0, (y - y0) / (y1 - y0)))
            grad.putpixel((0, y), lerpc(top, bot, t) + (255,))
        grad = grad.resize((self.W, self.H))
        if alpha < 1.0:
            m = m.point(lambda v: int(v * alpha))
        grad.putalpha(m)   # straight alpha (paste with a mask would darken the colour by the mask too)
        self.img.alpha_composite(grad)

    def dilate(self, m, r):
        if r <= 0:
            return m
        b = m.filter(ImageFilter.GaussianBlur(r * self.k * 0.5))
        return b.point(lambda v: 0 if v < 6 else (255 if v > 40 else int((v - 6) * 255 / 34)))

    def glow(self, m, color, radius=4.0, strength=0.8):
        g = m.filter(ImageFilter.GaussianBlur(radius * self.k))
        g = g.point(lambda v: min(255, int(v * strength * 1.6)))
        self._fill(g, color)

    def shape(self, fn, fill, outline=2.0, glow=None, alpha=1.0):
        """fn(draw, canvas) draws the shape in white on a mask."""
        m = self.mask(fn)
        if glow:
            col, rad, st = glow
            self.glow(self.dilate(m, outline), col, rad, st * alpha)
        if outline:
            self._fill(self.dilate(m, outline), OUT, alpha * 0.95)
        self._fill(m, fill, alpha)
        return m

    def out(self, size):
        im = self.img.convert("RGBa").resize((int(round(self.w * size / 64)), int(round(self.h * size / 64))),
                                             Image.LANCZOS)
        return im.convert("RGBA")


# --- shape helpers (design coords) ----------------------------------------------------------------------------
def poly(pts):
    return lambda d, c: d.polygon([c.P(p) for p in pts], fill=255)


def polys(*plist):
    def f(d, c):
        for pts in plist:
            d.polygon([c.P(p) for p in pts], fill=255)
    return f


def circle(cx, cy, r):
    return lambda d, c: d.ellipse([c.P((cx - r, cy - r)), c.P((cx + r, cy + r))], fill=255)


def circles(lst):
    def f(d, c):
        for cx, cy, r in lst:
            d.ellipse([c.P((cx - r, cy - r)), c.P((cx + r, cy + r))], fill=255)
    return f


def ring(cx, cy, r, w):
    def f(d, c):
        d.ellipse([c.P((cx - r - w / 2, cy - r - w / 2)), c.P((cx + r + w / 2, cy + r + w / 2))], fill=255)
        d.ellipse([c.P((cx - r + w / 2, cy - r + w / 2)), c.P((cx + r - w / 2, cy + r - w / 2))], fill=0)
    return f


def arc(cx, cy, r, a0, a1, w):
    """degrees, 0 = east, clockwise (screen)"""
    def f(d, c):
        if a1 - a0 <= 0.5:
            return
        d.arc([c.P((cx - r - w / 2, cy - r - w / 2)), c.P((cx + r + w / 2, cy + r + w / 2))], a0, a1, fill=255,
              width=max(1, int(round(w * c.k))))
        for a in (a0, a1):   # round caps
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            d.ellipse([c.P((x - w / 2, y - w / 2)), c.P((x + w / 2, y + w / 2))], fill=255)
    return f


def line(p1, p2, w):
    def f(d, c):
        d.line([c.P(p1), c.P(p2)], fill=255, width=max(1, int(round(w * c.k))))
        for p in (p1, p2):
            d.ellipse([c.P((p[0] - w / 2, p[1] - w / 2)), c.P((p[0] + w / 2, p[1] + w / 2))], fill=255)
    return f


def lines(segs, w):
    def f(d, c):
        for p1, p2 in segs:
            line(p1, p2, w)(d, c)
    return f


def rect(x0, y0, x1, y1, r=0):
    return lambda d, c: d.rounded_rectangle([c.P((x0, y0)), c.P((x1, y1))], radius=r * c.k, fill=255)


def union(*fns):
    def f(d, c):
        for fn in fns:
            fn(d, c)
    return f


def rot(p, a, cx=32, cy=32):
    s, co = math.sin(a), math.cos(a)
    x, y = p[0] - cx, p[1] - cy
    return (cx + x * co - y * s, cy + x * s + y * co)


def brackets(r, arm, w, cx=32, cy=32):
    """TA's corner brackets: four L corners at +-r."""
    out = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0, y0 = cx + sx * r, cy + sy * r
            out.append([(x0, y0), (x0 - sx * arm, y0), (x0 - sx * arm, y0 - sy * w), (x0 - sx * w, y0 - sy * w),
                        (x0 - sx * w, y0 - sy * arm), (x0, y0 - sy * arm)])
    return polys(*out)


def dot(c, col=(255, 255, 255)):
    c.shape(circle(32, 32, 1.6), col, outline=1.4)


def arrowhead(tip, direction, length, width):
    """triangle pointing along direction (radians)"""
    dx, dy = math.cos(direction), math.sin(direction)
    bx, by = tip[0] - dx * length, tip[1] - dy * length
    return [tip, (bx - dy * width / 2, by + dx * width / 2), (bx + dy * width / 2, by - dx * width / 2)]


def crate(cx, cy, s):
    return rect(cx - s, cy - s, cx + s, cy + s, s * 0.25)


# --- cursors: name -> (frames, frame length s, draw(canvas, t)) -------------------------------------------------
def c_normal(c, t):
    # TA's steel-blue arrow; a glint sweeps along it now and then (t < 0.35 of the loop)
    pts = [(2, 2), (2, 38), (11, 30), (17.5, 44), (23.5, 41.5), (17, 28), (28, 28)]
    m = c.shape(poly(pts), ((205, 225, 245), (60, 95, 140)), outline=2.2)
    edge = c.mask(poly([(2, 2), (2, 38), (6, 34), (6, 12), (21, 26.5), (28, 28)]))
    c._fill(ImageChops.multiply(edge, m), (235, 245, 255), 0.55)
    if t < 0.35:
        g = t / 0.35
        y = lerp(-10, 54, g)
        band = c.mask(poly([(0, y), (30, y - 14), (30, y - 7), (0, y + 7)]))
        c._fill(ImageChops.multiply(band, m), (255, 255, 255), 0.8 * math.sin(math.pi * g))


def c_move(c, t):
    p = math.sin(2 * math.pi * t)
    off = 23 + 3.5 * p
    tips = [rot((32, 32 - off), a * math.pi / 2) for a in range(4)]
    heads = [arrowhead(tp, math.atan2(tp[1] - 32, tp[0] - 32), 13, 13) for tp in tips]
    glow_s = 0.45 + 0.35 * (0.5 + 0.5 * p)
    c.shape(polys(*heads), GREEN, outline=2.0, glow=((120, 255, 90), 3.5, glow_s))
    c.shape(brackets(8.5, 6, 2.6), SILVER, outline=1.8)
    dot(c)


def blade_cursor(c, t, colors, spin=0.0, base_r=20.0, pulse=3.0, fill_override=None):
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    r = base_r + pulse * (1 - p)
    blades = []
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2 + spin
        tip = (32 + math.cos(a) * (r - 8), 32 + math.sin(a) * (r - 8))
        blades.append(arrowhead(tip, a + math.pi, 15, 12))
    col = fill_override or (lerpc(colors[0][0], colors[1][0], p), lerpc(colors[0][1], colors[1][1], p))
    c.shape(polys(*blades), col, outline=2.0, glow=(col[1], 3.5, 0.5 + 0.4 * p))
    ticks = [((32, 32 - 17), (32, 32 - 7)), ((32, 32 + 7), (32, 32 + 17)),
             ((32 - 17, 32), (32 - 7, 32)), ((32 + 7, 32), (32 + 17, 32))]
    c.shape(union(lines(ticks, 2.6), ring(32, 32, 10.5, 2.0)), SILVER, outline=1.6)
    dot(c, (255, 240, 200))


def c_attack(c, t):
    blade_cursor(c, t, (RED, YELLOW))


def c_fight(c, t):
    # attack's crosshair with orange blades spinning round it
    blade_cursor(c, 0.25, (ORANGE, ORANGE), spin=t * math.pi / 2, pulse=0)


def c_manfire(c, t):
    # D-Gun / manual fire: attack crosshair with a pulsing energy core
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    blade_cursor(c, t, ((CYAN[0], (60, 120, 255)), ((255, 255, 255), CYAN[1])))
    c.shape(circle(32, 32, 3.2 + 1.5 * p), ((255, 255, 255), (140, 220, 255)), outline=1.2,
            glow=((120, 200, 255), 3.0, 0.9))


def c_attackbad(c, t):
    blades = []
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        tip = (32 + math.cos(a) * 14, 32 + math.sin(a) * 14)
        blades.append(arrowhead(tip, a + math.pi, 15, 12))
    c.shape(polys(*blades), GREY, outline=2.0)
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    col = (lerpc((255, 120, 90), (255, 240, 120), p), lerpc((190, 10, 0), (230, 150, 0), p))
    sign = union(ring(32, 32, 11, 4.0), line(rot((32, 21.5), math.pi / 4), rot((32, 42.5), math.pi / 4), 4.0))
    c.shape(sign, col, outline=1.8, glow=(col[1], 3.0, 0.4 + 0.4 * p))


def c_select(c, t):
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    ticks = [((32, 14), (32, 24)), ((32, 40), (32, 50)), ((14, 32), (24, 32)), ((40, 32), (50, 32))]
    c.shape(union(lines(ticks, 2.6), brackets(10, 6, 2.4)), SILVER, outline=1.8)
    c.shape(circle(32, 32, 1.4 + 0.8 * p), (255, 255, 255), outline=1.2, glow=((200, 230, 255), 2.0, 0.5 * p))


def c_patrol(c, t):
    c.shape(brackets(9, 6, 2.6), SILVER, outline=1.8)
    dot(c)
    orbs = []
    for i in range(3):
        a = 2 * math.pi * (t + i / 3.0)
        for j in range(4):   # trail
            aa = a - j * 0.16
            orbs.append((32 + math.cos(aa) * 22, 32 + math.sin(aa) * 17, 3.4 - j * 0.7, j))
    for x, y, r, j in sorted(orbs, key=lambda o: -o[3]):
        c.shape(circle(x, y, r), CYAN, outline=1.4 if j == 0 else 0, glow=((90, 220, 255), 2.5, 0.6 if j == 0 else 0),
                alpha=1.0 - j * 0.22)


def c_defend(c, t):
    c.shape(brackets(9, 6, 2.6), SILVER, outline=1.8)
    dot(c)
    # an arc sweeps round (grows to a full circle), then its tail follows it away
    if t < 0.55:
        a0, a1 = -90, -90 + 360 * ease(t / 0.55)
    else:
        a0, a1 = -90 + 360 * ease((t - 0.55) / 0.45), 270
    for r, w, col in ((22, 3.0, BLUE), (17.5, 1.6, CYAN)):
        c.shape(arc(32, 32, r, a0, a1, w), col, outline=1.6, glow=((110, 150, 255), 3.0, 0.6))
    if a1 - a0 > 2:
        hx, hy = 32 + 22 * math.cos(math.radians(a1)), 32 + 22 * math.sin(math.radians(a1))
        c.shape(circle(hx, hy, 2.6), ((255, 255, 255), (170, 200, 255)), outline=1.2, glow=((140, 180, 255), 3, 1))


def c_protect(c, t):
    # TA's protect (unused by the engine): defend's sweep in green with a shield arc over the top
    c.shape(brackets(10, 7, 2.8), SILVER, outline=1.8)
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    c.shape(arc(32, 32, 22, 200, 340, 3.6), GREEN, outline=1.8, glow=((120, 255, 100), 3.5, 0.4 + 0.5 * p))
    c.shape(arc(32, 32, 17.5, 215, 325, 1.8), ((220, 255, 200), (90, 200, 80)), outline=1.4, alpha=0.5 + 0.5 * p)
    dot(c)


def c_repair(c, t):
    # TA's steel plate split by a zigzag crack: the crack closes, welds with a flash, holds, reopens
    if t < 0.45:
        gap = 6 * (1 - ease(t / 0.45))
    elif t < 0.8:
        gap = 0
    else:
        gap = 6 * ease((t - 0.8) / 0.2)
    zig = [(0, -11), (-2.5, -6), (2.5, -2), (-2.5, 2), (2.5, 6), (0, 11)]
    left = [(14, 21), (32 - gap / 2 + 0, 21)] + [(32 - gap / 2 + x, 32 + y) for x, y in zig] + [(32 - gap / 2, 43),
                                                                                                (14, 43)]
    right = [(50, 21), (32 + gap / 2, 21)] + [(32 + gap / 2 + x, 32 + y) for x, y in zig] + [(32 + gap / 2, 43),
                                                                                             (50, 43)]
    for pts in (left, right):
        c.shape(poly(pts), STEEL, outline=1.8)
    if 0.4 < t < 0.75:
        f = math.sin(math.pi * (t - 0.4) / 0.35)
        seam = lines([((32 + zig[i][0], 32 + zig[i][1]), (32 + zig[i + 1][0], 32 + zig[i + 1][1]))
                      for i in range(len(zig) - 1)], 1.6)
        c.shape(seam, ((255, 255, 230), (255, 200, 90)), outline=0, glow=((255, 190, 60), 3.0, 1.2 * f), alpha=f)
    c.shape(brackets(25, 6, 2.4), SILVER, outline=1.8)


def c_reclamate(c, t):
    # particles spiral in and compress into a glowing steel block
    c.shape(brackets(23, 6, 2.4), SILVER, outline=1.8)
    parts = []
    for i in range(12):
        ph = (t + i / 12.0) % 1.0
        a = i * 2.39996 + ph * 2.2
        r = 21 * (1 - ease(ph))
        if r > 6:
            parts.append((32 + math.cos(a) * r, 32 + math.sin(a) * r, 2.0 + 0.6 * (r / 21), min(1, (1 - ph) * 3)))
    for x, y, s, al in parts:
        c.shape(rect(x - s, y - s, x + s, y + s, 0.6), STEEL, outline=1.1, alpha=al)
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t * 2)
    s = 5.5
    c.shape(rect(32 - s, 32 - s, 32 + s, 32 + s, 1.2), ((225, 240, 250), (80, 120, 160)), outline=1.6,
            glow=((140, 210, 255), 3.0, 0.3 + 0.4 * p))


def c_revive(c, t):
    # rubble at the bottom rises into a cube that fills with life
    c.shape(brackets(14, 6, 2.6, cy=28), SILVER, outline=1.8)
    fill = ease(min(1, t / 0.7))
    for i in range(9):
        ph = (t * 1.5 + i / 9.0) % 1.0
        x = 22 + (i * 7.3) % 20
        y = lerp(52, 30, ease(ph))
        x = lerp(x, 32, ease(ph))
        c.shape(rect(x - 1.5, y - 1.5, x + 1.5, y + 1.5, 0.4), GREY, outline=1.0, alpha=min(1, (1 - ph) * 2.5))
    c.shape(polys([(18, 54), (24, 47), (30, 50), (36, 46), (44, 51), (48, 54)]), GREY, outline=1.6,
            alpha=1 - 0.6 * fill)
    s = 7
    c.shape(rect(32 - s, 28 - s, 32 + s, 28 + s, 1.5), ((200, 255, 230), (40, 160, 150)), outline=1.6,
            glow=((90, 255, 190), 3.5, 0.9 * fill), alpha=0.25 + 0.75 * fill)
    c.shape(circle(32, 32, 1.4), (255, 255, 255), outline=1.2)


def c_capture(c, t):
    # two enemy blocks slide in, meet, and turn ours
    meet = ease(min(1, t / 0.5))
    x = lerp(20, 4.5, meet)
    after = max(0, (t - 0.5) / 0.5)
    a = ease(min(1, after * 2))
    if a < 0.5:   # enemy colours -> a white flash -> ours
        col = (lerpc(YELLOW[0], (255, 255, 255), a * 2), lerpc((210, 60, 0), (230, 245, 255), a * 2))
    else:
        col = (lerpc((255, 255, 255), CYAN[0], a * 2 - 1), lerpc((230, 245, 255), CYAN[1], a * 2 - 1))
    c.shape(brackets(12, 5, 2.4), SILVER, outline=1.8)
    if after <= 0:
        for sx in (-1, 1):
            c.shape(rect(32 + sx * x - 4.5, 27.5, 32 + sx * x + 4.5, 36.5, 1), col, outline=1.6)
    else:
        f = math.sin(math.pi * min(1, after * 2))
        c.shape(rect(23, 27.5, 41, 36.5, 1.5), col, outline=1.6, glow=((120, 220, 255), 3.5, 0.3 + 0.9 * f))
    c.shape(circle(32, 32, 1.4), (255, 255, 255), outline=1.2)


def transport_base(c):
    c.shape(brackets(11, 5.5, 2.4, cy=33), SILVER, outline=1.8)
    c.shape(rect(20, 49, 44, 54, 1.5), STEEL, outline=1.6)


def c_pickup(c, t):
    transport_base(c)
    y = lerp(4, 24, ease(t))
    al = min(1, t * 5) * min(1, (1 - t) * 5)
    c.shape(poly(arrowhead((32, y + 12), math.pi / 2, 12, 14)), GREEN, outline=1.8, glow=((120, 255, 90), 3, 0.5),
            alpha=al)
    c.shape(circle(32, 32, 1.4), (255, 255, 255), outline=1.2)


def c_unload(c, t):
    transport_base(c)
    for k in range(2):
        ph = (t + k * 0.5) % 1.0
        x = lerp(32, 52, ease(ph))
        y = 33 - 26 * math.sin(math.pi * ph * 0.8) + 10 * ph * ph
        al = min(1, (1 - ph) * 4)
        c.shape(crate(x, y, 4.2 * min(1, 0.3 + ph * 5)), CYAN, outline=1.6, alpha=al)
    c.shape(circle(32, 32, 1.4), (255, 255, 255), outline=1.2)


def bad_x(c, t):
    p = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    col = (lerpc((255, 120, 90), (255, 240, 120), p), lerpc((190, 10, 0), (230, 150, 0), p))
    c.shape(lines([((25, 26), (39, 40)), ((39, 26), (25, 40))], 3.6), col, outline=1.6,
            glow=(col[1], 3, 0.3 + 0.4 * p))


def c_pickupbad(c, t):
    transport_base(c)
    c.shape(poly(arrowhead((32, 20), math.pi / 2, 12, 14)), GREY, outline=1.8)
    bad_x(c, t)


def c_unloadbad(c, t):
    transport_base(c)
    for sx in (-1, 1):
        c.shape(crate(32 + sx * 22, 33, 4.2), GREY, outline=1.6)
    bad_x(c, t)


def c_airstrike(c, t):
    ticks = [((32, 14), (32, 24)), ((32, 40), (32, 50)), ((14, 32), (24, 32)), ((40, 32), (50, 32))]
    c.shape(union(lines(ticks, 2.4), ring(32, 32, 12, 2.0)), SILVER, outline=1.6)
    for k in range(3):
        ph = (t + k / 3.0) % 1.0
        x = 32 + (k - 1) * 9 * (1 - ph)
        y = lerp(0, 30, ph * ph)
        al = min(1, ph * 6) * min(1, (1 - ph) * 5)
        body = union(rect(x - 2.6, y - 7, x + 2.6, y + 2.5, 2.6), poly([(x - 3.5, y - 9), (x + 3.5, y - 9), (x, y - 5)]))
        c.shape(body, RED if k % 2 else YELLOW, outline=1.4, alpha=al)
        if ph > 0.85:
            f = (ph - 0.85) / 0.15
            c.shape(ring(32, 32, 3 + 9 * f, 2.4 * (1 - f) + 0.6), ((255, 255, 220), (255, 170, 30)), outline=0,
                    glow=((255, 150, 20), 2.5, 1.2 * (1 - f)), alpha=1 - f * f)
    dot(c)


def water(c, t, y0):
    for j, (y, col, amp) in enumerate(((y0, (60, 90, 255), 1.6), (y0 + 9, (120, 170, 255), 1.3),
                                       (y0 + 18, (160, 210, 255), 1.0))):
        pts = [(x, y + amp * math.sin(x * 0.35 + 2 * math.pi * t * (1 if j % 2 == 0 else -1) + j))
               for x in [6 + i * 1.0 for i in range(53)]]
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        c.shape(lines(segs, 2.2), (lerpc(col, (255, 255, 255), 0.35), col), outline=1.2, alpha=1 - j * 0.15)


def c_submerged(c, t):
    water(c, t, 24)
    y = 32 + 2.5 * math.sin(2 * math.pi * t)
    c.shape(poly(arrowhead((32, y + 7), math.pi / 2, 14, 15)), PURPLE, outline=1.8, glow=((150, 90, 255), 3, 0.5))


def c_surfaced(c, t):
    water(c, t, 24)
    y = 32 - 2.5 * math.sin(2 * math.pi * t)
    c.shape(poly(arrowhead((32, y - 7), -math.pi / 2, 14, 15)), YELLOW, outline=1.8, glow=((255, 200, 40), 3, 0.5))


def c_upgrade(c, t):
    ticks = [rot((32, 13), a * math.pi / 2) for a in range(4)]
    c.shape(union(ring(32, 32, 15, 3.0), lines([(p, rot((32, 19), a * math.pi / 2)) for a, p in enumerate(ticks)],
                                                2.4)), SILVER, outline=1.6)
    y = lerp(54, 12, ease(t))
    al = min(1, t * 6) * min(1, (1 - t) * 6)
    c.shape(poly(arrowhead((32, y - 8), -math.pi / 2, 15, 15)), YELLOW, outline=1.8, glow=((255, 200, 40), 3.5, 0.7),
            alpha=al)


def c_wait(c, t):
    # an hourglass whose sand runs, then flips
    flip = ease(max(0, (t - 0.85) / 0.15)) * math.pi
    sand = min(1, t / 0.85)

    def R(p):
        return rot(p, flip)
    frame = [R(p) for p in [(21, 14), (43, 14), (34, 32), (43, 50), (21, 50), (30, 32)]]
    c.shape(union(rect(18, 11, 46, 15, 1.5), rect(18, 49, 46, 53, 1.5)) if flip == 0 else
            polys([R(p) for p in [(18, 11), (46, 11), (46, 15), (18, 15)]],
                  [R(p) for p in [(18, 49), (46, 49), (46, 53), (18, 53)]]), STEEL, outline=1.6)
    c.shape(poly(frame), ((235, 248, 255), (150, 190, 225)), outline=1.8)
    top = 1 - sand
    if top > 0.02:
        h = 15 * top
        c.shape(poly([R(p) for p in [(32 - 9 * top, 31 - h), (32 + 9 * top, 31 - h), (32, 31.5)]]), YELLOW, outline=0)
    if sand > 0.02 and flip == 0:
        h = 14 * sand
        c.shape(poly([(32 - 9.5 * min(1, sand * 1.4), 49), (32 + 9.5 * min(1, sand * 1.4), 49), (32, 49 - h)]), YELLOW,
                outline=0)
        if sand < 1:
            c.shape(line((32, 32), (32, 48), 1.0), YELLOW, outline=0)


CURSORS = {
    # name:          (frames, length, fn, topleft)
    "cursornormal":    (30, 0.04, c_normal, True),
    "cursormove":      (24, 0.04, c_move, False),
    "cursorattack":    (20, 0.04, c_attack, False),
    "cursorattackbad": (24, 0.04, c_attackbad, False),
    "cursorfight":     (24, 0.04, c_fight, False),
    "cursormanfire":   (20, 0.04, c_manfire, False),
    "cursorselect":    (24, 0.05, c_select, False),
    "cursorpatrol":    (36, 0.04, c_patrol, False),
    "cursordefend":    (32, 0.04, c_defend, False),
    "cursorprotect":   (24, 0.05, c_protect, False),
    "cursorrepair":    (32, 0.04, c_repair, False),
    "cursorreclamate": (30, 0.04, c_reclamate, False),
    "cursorrevive":    (32, 0.04, c_revive, False),
    "cursorcapture":   (32, 0.04, c_capture, False),
    "cursorpickup":    (24, 0.04, c_pickup, False),
    "cursorpickupbad": (24, 0.04, c_pickupbad, False),
    "cursorunload":    (32, 0.04, c_unload, False),
    "cursorunloadbad": (24, 0.04, c_unloadbad, False),
    "cursorairstrike": (30, 0.04, c_airstrike, False),
    "cursorsubmerged": (30, 0.05, c_submerged, False),
    "cursorsurfaced":  (30, 0.05, c_surfaced, False),
    "cursorupgrade":   (24, 0.045, c_upgrade, False),
    "cursorwait":      (40, 0.05, c_wait, False),
}


def render(name, size, frame):
    frames, length, fn, topleft = CURSORS[name]
    c = Canvas(size, 32, 48) if topleft else Canvas(size)
    t = frame / frames
    if name == "cursornormal":
        # the glint plays in the first 12 frames; the rest are the plain arrow (written once, held via the spec)
        t = frame / 12 * 0.35 if frame < 12 else 0.99
    fn(c, t)
    return c.out(size)


def write_set(size, only=None):
    d = os.path.join(ROOT, "anims", "hd", str(size))
    os.makedirs(d, exist_ok=True)
    for name, (frames, length, fn, topleft) in CURSORS.items():
        if only and name not in only:
            continue
        spec = ["hotspot %s" % ("topleft" if topleft else "center")]
        if name == "cursornormal":
            for i in range(13):
                render(name, size, i).save(os.path.join(d, "%s_%d.png" % (name, i)), optimize=True)
            spec.append("frame anims/hd/%d/%s_12.png 2.5" % (size, name))
            for i in range(12):
                spec.append("frame anims/hd/%d/%s_%d.png %.3f" % (size, name, i, length))
        else:
            for i in range(frames):
                render(name, size, i).save(os.path.join(d, "%s_%d.png" % (name, i)), optimize=True)
                spec.append("frame anims/hd/%d/%s_%d.png %.3f" % (size, name, i, length))
        body = "\n".join(spec) + "\n"
        open(os.path.join(d, name + ".txt"), "w").write(body)
        if size == DEFAULT_SIZE:
            open(os.path.join(ROOT, "anims", name + ".txt"), "w").write(body)
        print(size, name, flush=True)


def preview(outdir, size=64, scale=2):
    """an animated GIF of every cursor on a grass-coloured board, and a still sheet"""
    os.makedirs(outdir, exist_ok=True)
    names = list(CURSORS)
    cols = 6
    cell = int(size * 1.25)
    rows = (len(names) + cols - 1) // cols
    n = 60
    gif = []
    for f in range(n):
        board = Image.new("RGBA", (cols * cell, rows * cell), (74, 98, 58, 255))
        for i, name in enumerate(names):
            frames = CURSORS[name][0]
            im = render(name, size, (f * frames // n) % frames if name != "cursornormal" else min(12, f // 2))
            x, y = (i % cols) * cell + (cell - im.width) // 2, (i // cols) * cell + (cell - im.height) // 2
            board.alpha_composite(im, (x, y))
        board = board.resize((board.width * scale // 2 * 2 // 2, board.height * scale // 2 * 2 // 2), Image.NEAREST)
        gif.append(board.convert("RGB"))
    gif[0].save(os.path.join(outdir, "cursors.gif"), save_all=True, append_images=gif[1:], duration=40, loop=0)
    gif[n // 3].save(os.path.join(outdir, "cursors_still.png"))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--preview":
        preview(args[1])
    else:
        only = set(a for a in args if a.startswith("cursor")) or None
        for s in SIZES:
            write_set(s, only)
