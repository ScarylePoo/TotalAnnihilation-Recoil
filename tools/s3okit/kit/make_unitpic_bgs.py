#!/usr/bin/env python3
"""Enhance the 96x96 TA unit picture backgrounds to 256x256 PNGs in unitpic_bg/. Needs torch + spandrel and the RealESRGAN_x4plus weights
(not in the game's kit venv): python make_unitpic_bgs.py <folder of small/*.bmp> <weights.pth> <out dir>.
A light blur first clears the 8-bit dither, which the model would otherwise treat as detail; a quarter of the plain upscale is blended back so
flat ground keeps its mottling."""
import glob, os, sys
import numpy as np, torch
from PIL import Image, ImageFilter
from spandrel import ModelLoader
src, weights, out = sys.argv[1:4]
m = ModelLoader().load_from_file(weights).to('cuda').eval()
for f in sorted(glob.glob(os.path.join(src, '*.bmp'))):
    im = Image.open(f).convert('RGB')
    soft = im.filter(ImageFilter.GaussianBlur(0.7))
    a = torch.from_numpy(np.array(soft, dtype=np.float32) / 255).permute(2, 0, 1)[None].cuda()
    a = torch.nn.functional.pad(a, (16, 16, 16, 16), mode='reflect')
    with torch.no_grad():
        r = m(a).clamp(0, 1)[0, :, 64:-64, 64:-64].permute(1, 2, 0).cpu().numpy()
    big = Image.fromarray((r * 255 + .5).astype('uint8')).resize((256, 256), Image.LANCZOS)
    plain = soft.resize((256, 256), Image.BICUBIC)
    Image.blend(big, plain, 0.25).save(os.path.join(out, os.path.basename(f)[:-4].replace(' ', '_') + '.png'))
