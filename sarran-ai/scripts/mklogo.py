from PIL import Image, ImageDraw
import os

SRC = r"C:\Users\rober\OneDrive\Documents\Robert\Sarran AI Solutions LLC\02_Sales_Marketing\Sarran_AI_Solutions_LLC\SARRAN AI Solutions LLC_logo.png"
OUT = r"C:\Users\rober\claude-websites\sarran-ai\assets"

im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()
print("source:", W, "x", H)

def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]

# The metal plate is light; the emblem bezel is dark. Walk in from each edge
# along the centre row/column until brightness drops through the threshold.
THRESH = 110

def scan(fixed, horizontal):
    """Walk in from each edge to the first dark pixel, skipping the outer 12%
    of the plate — it carries a dark vignette that otherwise reads as the bezel."""
    n = W if horizontal else H
    m = int(n * 0.12)
    lo = hi = None
    for i in range(m, n - m):
        p = px[i, fixed] if horizontal else px[fixed, i]
        if lum(p) < THRESH:
            lo = i
            break
    for i in range(n - m - 1, m, -1):
        p = px[i, fixed] if horizontal else px[fixed, i]
        if lum(p) < THRESH:
            hi = i
            break
    return lo, hi

# Thresholding is unreliable on this artwork: the metal bezel carries specular
# highlights that read as background. The emblem is centred on a square canvas,
# so take a centred circle at a radius set by inspection instead.
cx, cy = W // 2, H // 2
r = 782
box = (cx - r, cy - r, cx + r, cy + r)
print("crop box:", box, "diameter:", r * 2)

crop = im.crop(box)

# Antialiased circular alpha: build the mask at 4x, then downsample.
S = 4
side = crop.size[0]
mask = Image.new("L", (side * S, side * S), 0)
ImageDraw.Draw(mask).ellipse((0, 0, side * S - 1, side * S - 1), fill=255)
mask = mask.resize((side, side), Image.LANCZOS)

emblem = crop.convert("RGBA")
emblem.putalpha(mask)

for size, name in ((512, "sarran_emblem.png"), (180, "sarran_emblem@180.png"), (64, "sarran_favicon.png")):
    out = emblem.resize((size, size), Image.LANCZOS)
    path = os.path.join(OUT, name)
    out.save(path, optimize=True)
    print("wrote", name, os.path.getsize(path) // 1024, "KB")
