#!/usr/bin/env python3
"""Turn artwork into raw pixel files the firmware embeds.

  img2bin.py a8 in.png out.a8 WIDTH HEIGHT   ink lines: alpha = darkness, drawn in ink colour
  img2bin.py l8 in.png out.l8 WIDTH HEIGHT   grey picture: four levels with ordered dithering

The firmware's assets.c lists each file with the same WIDTH and HEIGHT.
"""
import sys
from PIL import Image, ImageOps

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def load_gray(path, w, h):
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    return img.resize((w, h), Image.LANCZOS)


def to_a8(img):
    # Lines are dark on white. Push near-white to fully transparent, keep edges soft.
    px = img.load()
    out = bytearray()
    for y in range(img.height):
        for x in range(img.width):
            v = 255 - px[x, y]
            v = 0 if v < 40 else min(255, int((v - 40) * 255 / 180))
            out.append(v)
    return bytes(out)


def to_l8(img):
    px = img.load()
    out = bytearray()
    for y in range(img.height):
        for x in range(img.width):
            v = px[x, y] / 255 * 3 + (BAYER[y % 4][x % 4] / 16 - 0.5) * 0.9
            level = max(0, min(3, int(round(v))))
            out.append(level * 85)
    return bytes(out)


mode, src, dst, w, h = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
img = load_gray(src, w, h)
data = to_a8(img) if mode == "a8" else to_l8(img)
open(dst, "wb").write(data)
print(f"{dst}: {w}x{h} {mode} {len(data)} bytes")
