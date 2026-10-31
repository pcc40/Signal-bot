#!/usr/bin/env python3
"""WCAG 2.2 colour-contrast check for the colour pairs the stylesheet actually uses.
Reads the :root tokens from src/static/assets/site.css, so a palette change is checked automatically.
Usage: python3 tools/contrast_check.py      (exit 1 if any text pair fails AA)"""
import re, sys
from pathlib import Path

CSS = (Path(__file__).resolve().parent.parent / "src/static/assets/site.css").read_text()
root = re.search(r":root\{(.*?)\}", CSS, re.S).group(1)
T = dict(re.findall(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})", root))

def rgb(h):
    h = T.get(h, h).lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def blend(fg, alpha, bg):
    return tuple(f * alpha + b * (1 - alpha) for f, b in zip(rgb(fg), rgb(bg)))

def lum(c):
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

# (label, foreground, background, minimum) — 4.5 body text, 3.0 large text / UI components
PAIRS = [
    ("Body text on white", "ink", "white", 4.5),
    ("Soft text on white", "ink-soft", "white", 4.5),
    ("Soft text on stone", "ink-soft", "stone", 4.5),
    ("Brass kicker/meta on white", "brass", "white", 4.5),
    ("Brass kicker on stone", "brass", "stone", 4.5),
    ("Brass-light kicker on slate", "brass-light", "slate", 4.5),
    ("Muted text on slate", "muted-dark", "slate", 4.5),
    ("Muted text on ink", "muted-dark", "ink", 4.5),
    ("Stage text #B7BEBC on slate", "#B7BEBC", "slate", 4.5),
    ("Footer text #C2C8C5 on ink", "#C2C8C5", "ink", 4.5),
    ("Legal text #97A09C on ink", "#97A09C", "ink", 4.5),
    ("Placeholder #9EA6A3 on ink", "#9EA6A3", "ink", 4.5),
    ("WhatsApp button white on green", "white", "#25603F", 4.5),
    ("Button white on ink", "white", "ink", 4.5),
    ("Button hover white on brass", "white", "brass", 4.5),
    ("Error text on white", "#A3321F", "white", 4.5),
    ("Field border #767C7A on white (UI)", "#767C7A", "white", 3.0),
    ("Focus ring brass on white (UI)", "brass", "white", 3.0),
    ("Focus ring brass-light on slate (UI)", "brass-light", "slate", 3.0),
    ("Focus ring brass-light on ink (UI)", "brass-light", "ink", 3.0),
]

fails = 0
for label, fg, bg, need in PAIRS:
    r = ratio(rgb(fg), rgb(bg))
    ok = r >= need
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {r:5.2f}:1 (need {need}) {label}")
# translucent white text over the darkest part of hero/banner overlays (ink at 74% over a mid-grey photo)
over = blend("ink", 0.74, "#808080")
for label, a in [("Hero meta white 80% over overlay", 0.8), ("Banner credit white 78% over overlay", 0.78)]:
    fg = tuple(1 * a + o * (1 - a) for o in over)
    r = ratio(fg, over)
    fails += r < 4.5
    print(f"{'ok  ' if r >= 4.5 else 'FAIL'} {r:5.2f}:1 (need 4.5) {label}")
print(f"{fails} failing pair(s)")
sys.exit(1 if fails else 0)
