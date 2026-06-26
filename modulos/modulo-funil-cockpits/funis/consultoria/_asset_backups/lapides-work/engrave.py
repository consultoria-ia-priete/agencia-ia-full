#!/usr/bin/env python3
"""Engrave tombstone text onto the clean high-quality bases (768x1024).

- Removes near-white background -> transparent (matches originals).
- Big uppercase serif label + smaller R.I.P. epitaph (2-3 lines, centered).
- Carved effect: dark incised fill + subtle light bevel offset.
- One dedicated base per tombstone (base-afiliado / base-drop / base-info).
"""
from PIL import Image, ImageDraw, ImageFont

GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TIMES_BOLD   = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

# Text face region on the stone (tuned for the 768x1024 flux-pro bases)
FACE_CX = 397          # horizontal center of the stone face
LABEL_Y = 350          # top anchor for the big label
RIP_Y   = 470          # where the R.I.P. block starts (top)
FACE_W  = 300          # usable inner face width for wrapping

DARK   = (34, 39, 45, 255)     # incised shadow (dark slate)
LIGHT  = (216, 220, 224, 140)  # subtle bevel highlight

def remove_white_bg(im: Image.Image, thresh=236) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= thresh and g >= thresh and b >= thresh:
                px[x, y] = (r, g, b, 0)
    return im

def fit_font(path, text, max_w, start, min_size=22):
    size = start
    while size > min_size:
        f = ImageFont.truetype(path, size)
        bb = f.getbbox(text)
        if (bb[2]-bb[0]) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)

def draw_carved_centered(draw, cx, y_top, text, font):
    bb = font.getbbox(text)
    tw = bb[2]-bb[0]
    x = cx - tw/2 - bb[0]
    y = y_top - bb[1]
    draw.text((x+1.5, y+1.5), text, font=font, fill=LIGHT)  # bevel highlight
    draw.text((x, y), text, font=font, fill=DARK)            # incised fill

def engrave(base_path, out_path, label, rip_lines, label_size):
    im = remove_white_bg(Image.open(base_path))
    draw = ImageDraw.Draw(im)
    # big label (uniform size across the 3 stones)
    lf = ImageFont.truetype(GEORGIA_BOLD, label_size)
    draw_carved_centered(draw, FACE_CX, LABEL_Y, label, lf)
    # R.I.P. epitaph block
    y = RIP_Y
    for i, line in enumerate(rip_lines):
        is_rip = (i == 0)
        f = fit_font(TIMES_BOLD, line, FACE_W, start=(48 if is_rip else 40))
        bb = f.getbbox(line)
        lh = bb[3]-bb[1]
        draw_carved_centered(draw, FACE_CX, y, line, f)
        y += lh + (22 if is_rip else 14)
    im.save(out_path)
    print(f"  saved {out_path}")

if __name__ == "__main__":
    WORK   = "$PROJECTS_ROOT/ALEX_SSCIA/Funis de Vendas/Funil ConsultorIA/public/assets/_work"
    ASSETS = "$PROJECTS_ROOT/ALEX_SSCIA/Funis de Vendas/Funil ConsultorIA/public/assets"

    # uniform label size: largest that fits the longest label within FACE_W
    longest = "DROPSHIPPING"
    label_size = 80
    while label_size > 30:
        f = ImageFont.truetype(GEORGIA_BOLD, label_size)
        bb = f.getbbox(longest)
        if (bb[2]-bb[0]) <= FACE_W:
            break
        label_size -= 2
    print(f"uniform label_size = {label_size} (fits '{longest}' in {FACE_W}px)")

    jobs = [
        ("base-afiliado.png", "lapide-afiliado.png", "AFILIADO",
         ["R.I.P.", "DESISTIU ANTES DE ACHAR", "O PRODUTO CAMPEÃO"]),
        ("base-drop.png", "lapide-drop.png", "DROPSHIPPING",
         ["R.I.P.", "FORNECEDOR", "DEIXOU NA MÃO"]),
        ("base-info.png", "lapide-info.png", "INFOPRODUTO",
         ["R.I.P.", "GASTOU MUITO DINHEIRO", "E NÃO VENDEU"]),
    ]
    for base, out, label, rip in jobs:
        print(f"[{label}]")
        engrave(f"{WORK}/{base}", f"{ASSETS}/{out}", label, rip, label_size)
