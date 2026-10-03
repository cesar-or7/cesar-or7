# Profile banner: amber-CRT spinoff of the byterepo terminal style, with a Game of Life
# glider gun firing across the right side. Period-30 gun, so 30 frames loop seamlessly.
# Run from this folder: python3 banner.py  -> ../assets/banner.gif
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 400
BG = (18, 11, 3); AMB = (255, 176, 0); LIT = (255, 214, 130); MID = (190, 120, 10); DIM = (70, 42, 8)

from PIL import ImageFont
mono = ImageFont.truetype('JetBrainsMono%5Bwght%5D.ttf', 24); mono.set_variation_by_axes([500])
monob = ImageFont.truetype('JetBrainsMono%5Bwght%5D.ttf', 28); monob.set_variation_by_axes([700])
pix = ImageFont.truetype('Silkscreen-Bold.ttf', 140)
pixs = ImageFont.truetype('Silkscreen-Regular.ttf', 26)

# --- Game of Life: Gosper glider gun on a big grid, view a window of it ---
GUN = ["........................O...........",
       "......................O.O...........",
       "............OO......OO............OO",
       "...........O...O....OO............OO",
       "OO........O.....O...OO..............",
       "OO........O...O.OO....O.O...........",
       "..........O.....O.......O...........",
       "...........O...O....................",
       "............OO......................"]
N = 260
g = np.zeros((N, N), bool)
for y, row in enumerate(GUN):
    for x, c in enumerate(row):
        g[4 + y, 4 + x] = c == 'O'

def step(a):
    n = sum(np.roll(np.roll(a, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx)
    a = (n == 3) | (a & (n == 2))
    a[-3:, :] = a[:, -3:] = False  # absorb gliders at the far edge so nothing wraps back
    return a

for _ in range(600): g = step(g)  # warm up so the stream fills the view

CELL, VX = 9, 724  # cell size; life panel starts right of the terminal window
VW, VH = (W - VX - 16) // CELL, (H - 20) // CELL

def static_layer():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(0, H, CELL):  # faint cell grid behind the life panel
        for x in range(VX, W - 16, CELL):
            d.point((x, y), fill=DIM)
    d.rounded_rectangle((40, 34, 700, 366), 14, fill=(12, 7, 2), outline=MID, width=2)
    d.rounded_rectangle((40, 34, 700, 76), 14, fill=(40, 24, 4)); d.rectangle((40, 60, 700, 76), fill=(40, 24, 4))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((60 + i * 26, 47, 76 + i * 26, 63), fill=c)
    d.text((170, 44), '~/cesar-or7 — README.md', font=mono, fill=MID)
    d.text((66, 96), '$ whoami', font=monob, fill=AMB)
    layer = Image.new('RGB', im.size); ImageDraw.Draw(layer).text((60, 126), 'CESAR', font=pix, fill=MID)
    im = Image.fromarray(np.clip(np.asarray(im, int) + np.asarray(layer.filter(ImageFilter.GaussianBlur(14)), int) * .8, 0, 255).astype('uint8'))
    d = ImageDraw.Draw(im)
    d.text((66, 132), 'CESAR', font=pix, fill=(80, 40, 0)); d.text((60, 126), 'CESAR', font=pix, fill=LIT)
    d.text((68, 292), 'builds stuff for fun', font=pixs, fill=AMB)
    d.text((68, 326), 'hobby projects · tinkering · games', font=mono, fill=MID)
    return im

base = static_layer()
frames = []
for i in range(30):
    fr = base.copy(); d = ImageDraw.Draw(fr)
    view = g[1:1 + VH, 2:2 + VW]
    for y, x in zip(*np.nonzero(view)):
        px, py = VX + x * CELL, 10 + y * CELL
        d.rectangle((px + 1, py + 1, px + CELL - 2, py + CELL - 2), fill=AMB)
    glow = fr.filter(ImageFilter.GaussianBlur(6))
    a = np.clip(np.asarray(fr, float) + np.asarray(glow, float) * .35, 0, 255)
    a[::3] *= .84  # scanlines
    fr = Image.fromarray(a.astype('uint8'))
    if (i // 8) % 2 == 0:  # blinking cursor
        ImageDraw.Draw(fr).rectangle((210, 100, 226, 128), fill=AMB)
    frames.append(fr.convert('P', palette=Image.ADAPTIVE, colors=64))
    g = step(g)
frames[0].save('../assets/banner.gif', save_all=True, append_images=frames[1:], loop=0, duration=90, optimize=True)
frames[0].convert('RGB').save('/tmp/claude-1000/-home-alpha-Work/247086b4-1264-4da4-ac90-9e1f31dc6deb/scratchpad/gh0.png')
print('ok', VW, VH)
