#!/usr/bin/env python3
"""Generates the original Bedrock-style pixel art. Edit colours and re-run from the project root:
   python3 tools/gen_textures.py"""
import zlib, struct, random, json, os
OUT = os.path.join(os.path.dirname(__file__), "..", "src/main/resources/assets/minecraft/textures/gui")

def png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(c for p in px[y*w:(y+1)*w] for c in p) for y in range(h))
    def ch(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                + ch(b"IDAT", zlib.compress(raw, 9)) + ch(b"IEND", b""))

def hx(s, a=255):
    s = s.lstrip("#"); return (int(s[0:2],16), int(s[2:4],16), int(s[4:6],16), a)

def bevel(w, h, fill, light, dark, outline, inset=False):
    if inset: light, dark = dark, light
    px = []
    for y in range(h):
        for x in range(w):
            if x in (0, w-1) or y in (0, h-1): c = outline
            elif x in (1, 2) and y < h-1 - (0) and x <= y or (y in (1, 2) and x < w-1): c = light
            elif x in (w-2, w-3) or y in (h-2, h-3): c = dark
            else: c = fill
            px.append(c)
    return px

def mcmeta(path, w, h, border):
    with open(path + ".mcmeta", "w") as f:
        json.dump({"gui": {"scaling": {"type": "nine_slice", "width": w, "height": h, "border": border}}}, f, indent=2)

SP = os.path.join(OUT, "sprites/widget")
def sprite(name, w, h, px, border=3):
    p = os.path.join(SP, name + ".png"); png(p, w, h, px); mcmeta(p, w, h, border)

OUTL = hx("1e1e1f")
# buttons
sprite("button", 200, 20, bevel(200, 20, hx("b1b2b5"), hx("d0d1d4"), hx("58585a"), OUTL))
sprite("button_highlighted", 200, 20, bevel(200, 20, hx("c4c5c8"), hx("ffffff"), hx("6a6a6c"), hx("ffffff")))
sprite("button_disabled", 200, 20, bevel(200, 20, hx("6b6c6f"), hx("7c7d80"), hx("48484a"), OUTL))
# sliders: dark inset track + button-style handle
sprite("slider", 200, 20, bevel(200, 20, hx("3a3a3c"), hx("5c5c5e"), hx("202021"), OUTL, inset=True))
sprite("slider_highlighted", 200, 20, bevel(200, 20, hx("48484b"), hx("6a6a6c"), hx("202021"), hx("ffffff"), inset=True))
sprite("slider_handle", 8, 20, bevel(8, 20, hx("b1b2b5"), hx("d0d1d4"), hx("58585a"), OUTL))
sprite("slider_handle_highlighted", 8, 20, bevel(8, 20, hx("c4c5c8"), hx("ffffff"), hx("6a6a6c"), hx("ffffff")))
# text fields
sprite("text_field", 200, 20, bevel(200, 20, hx("1b1b1c"), hx("3c3c3e"), hx("8b8c8f"), OUTL, inset=True))
sprite("text_field_highlighted", 200, 20, bevel(200, 20, hx("1b1b1c"), hx("3c3c3e"), hx("ffffff"), hx("ffffff"), inset=True))
# tabs
for n, fill, hl in [("tab_selected", "b1b2b5", False), ("tab_unselected", "58585a", False),
                    ("tab_selected_highlighted", "c4c5c8", True), ("tab_unselected_highlighted", "6b6c6f", True)]:
    p = os.path.join(SP, n + ".png")
    png(p, 130, 24, bevel(130, 24, hx(fill), hx("d0d1d4"), hx("58585a"), hx("ffffff") if hl else OUTL))
    mcmeta(p, 130, 24, {"left": 3, "top": 3, "right": 3, "bottom": 0})

# stone panel backgrounds (16x16 tiles)
def stone(path, base, spread, seed):
    r = random.Random(seed); px = []
    for _ in range(256):
        v = r.randint(-spread, spread)
        px.append((base + v, base + v, base + v + 2, 255))
    png(path, 16, 16, px)
stone(os.path.join(OUT, "menu_background.png"), 0x3a, 7, 1)
stone(os.path.join(OUT, "menu_list_background.png"), 0x2a, 5, 2)
stone(os.path.join(OUT, "inworld_menu_list_background.png"), 0x2a, 5, 3)
# header/footer separators (32x2 tiles)
for n in ("header_separator", "footer_separator", "inworld_header_separator", "inworld_footer_separator"):
    png(os.path.join(OUT, n + ".png"), 32, 2, [OUTL] * 32 + [hx("8b8c8f")] * 32)
print("textures written")
