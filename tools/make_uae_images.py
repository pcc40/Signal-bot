#!/usr/bin/env python3
"""Turn the UAE image library (assets-src/uae-images/<folder>/) into the site's image sizes and manifest entries.

For each original listed in a folder's manifest.json this writes, into src/static/assets/img/:
  uae-<folder>-NN-640.webp, -1280.webp, -1600.webp   (never upscaled: a size wider than the original is skipped;
                                                       hero images also get -320.webp for the /areas/ thumbnails)
  uae-<folder>-NN-og.jpg                              (1200 x 630 centre crop, for og:image, JSON-LD and the
                                                       sitemap; hero and general images at least 1200 px wide)
and records each image in src/img_manifest.json under the key "uae-<folder>" with: base, w, h, src, name, place,
photo (the credit exactly as in the folder's manifest.json, printed by credit_of()), credit, alt, role, is_render,
source_page, og, uae. The two images in general/ keep descriptive bases (uae-dubai-skyline-villas-01,
uae-abu-dhabi-skyline-01) under the key "uae-general".

Originals stay in assets-src/, which build.py never copies; only the generated files are published.
Images narrower than 1280 px (the 880 px Jumeirah Bay images, the Palm Jumeirah panorama) only get the 640 size:
they are for image strips, never for a hero (the site's hero picker only uses role "hero" images).

Usage:  python3 tools/make_uae_images.py            (skips sizes that already exist and are newer than the original)
        python3 tools/make_uae_images.py --force    (regenerate every file)
Needs Pillow (pip install pillow)."""
import json, re, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets-src/uae-images"
OUT = ROOT / "src/static/assets/img"
MANIFEST = ROOT / "src/img_manifest.json"
SIZES = (640, 1280, 1600)
OG = (1200, 630)
QUALITY = 78
# Byte budget per width: a file over it is re-encoded at lower quality (down to MIN_QUALITY) until it fits.
# 1280 px is the hero size most pages preload as the LCP image. MIN_QUALITY is a visual floor: a very detailed
# image (al-barari-05, dubai-hills-estate-01) may stay a little over budget rather than show artefacts.
BUDGET = {1280: 200_000}
MIN_QUALITY = 62

# Folder -> (community name used in captions and alt text, place)
NAMES = {
    "al-barari": ("Al Barari", "Dubai"),
    "arabian-ranches": ("Arabian Ranches", "Dubai"),
    "district-one": ("District One, MBR City", "Dubai"),
    "dubai-hills-estate": ("Dubai Hills Estate", "Dubai"),
    "dubai-islands": ("Dubai Islands", "Dubai"),
    "emirates-hills": ("Emirates Hills", "Dubai"),
    "general": ("Dubai and Abu Dhabi", "UAE"),
    "hudayriyat": ("Hudayriyat Island", "Abu Dhabi"),
    "island-e": ("Island E, Dubai Islands", "Dubai"),
    "jumeirah-bay": ("Jumeirah Bay Island", "Dubai"),
    "jumeirah-islands": ("Jumeirah Islands", "Dubai"),
    "palm-jebel-ali": ("Palm Jebel Ali", "Dubai"),
    "palm-jumeirah": ("Palm Jumeirah", "Dubai"),
    "saadiyat": ("Saadiyat Island", "Abu Dhabi"),
}
# Words that show the alt text already names the community (otherwise the name is appended).
NAME_HINTS = {
    "al-barari": ["Al Barari"], "arabian-ranches": ["Arabian Ranches"], "district-one": ["District One"],
    "dubai-hills-estate": ["Dubai Hills"], "dubai-islands": ["Dubai Islands"], "emirates-hills": ["Emirates Hills"],
    "general": ["Palm Jumeirah", "Abu Dhabi"], "hudayriyat": ["Hudayriyat", "Wadeem"], "island-e": ["Island E"],
    "jumeirah-bay": ["Jumeirah Bay"], "jumeirah-islands": ["Jumeirah Islands"], "palm-jebel-ali": ["Palm Jebel Ali"],
    "palm-jumeirah": ["Palm Jumeirah"], "saadiyat": ["Saadiyat"],
}
# Alt text written by hand where the 'shows' line is too long or does not name the community.
ALT = {
    "hudayriyat-01.png": "Aerial view of terracotta-roofed villas on Hudayriyat Island at sunset, with the sea beyond",
    "hudayriyat-02.jpg": "Render of a villa terrace in Wadeem Gardens, Hudayriyat Island, over landscaped streets",
    "hudayriyat-03.jpg": "Render of a tree-lined street and park with a fountain among villas in Wadeem, Hudayriyat Island",
    "hudayriyat-04.jpg": "Render of a shaded green walkway between villas in Wadeem, Hudayriyat Island",
    "hudayriyat-05.jpg": "Render of a landscaped boulevard past townhouses in Wadeem Gardens, Hudayriyat Island",
    "dubai-hills-estate-01.jpg": "Aerial render of villas around a landscaped lake at Address Villas Hillcrest, Dubai Hills Estate",
    "dubai-hills-estate-02.jpg": "Render of two-storey villas on a palm-lined road at Golf Place II, Dubai Hills Estate",
    "dubai-hills-estate-03.jpg": "Render of a modern white villa with terrace and garden at Address Villas Hillcrest, Dubai Hills Estate",
    "dubai-hills-estate-04.jpg": "Elevated view over the Dubai Hills Estate golf course and villa neighbourhoods",
    "dubai-hills-estate-05.jpg": "Aerial render of Palm Hills villas, park and pools in Dubai Hills Estate, Downtown skyline beyond",
    "palm-jumeirah-01.jpg": "Sunset aerial of Palm Jumeirah along the trunk and villa-lined fronds towards Atlantis",
    "palm-jumeirah-02.jpg": "Low aerial of two Palm Jumeirah fronds lined with beachfront villas, Atlantis The Royal beyond",
    "palm-jumeirah-03.jpg": "Aerial over the Palm Jumeirah frond villas and trunk towards The Palm Tower and Dubai Marina",
    "saadiyat-02.webp": "Render of a villa terrace over a communal pool and gardens at Saadiyat Reserve, The Dunes, Saadiyat Island",
    "saadiyat-03.jpg": "Render of Nobu Residences by Saadiyat Island's white-sand beach, Guggenheim Abu Dhabi in the distance",
    "arabian-ranches-01.jpg": "Mediterranean-style Arabian Ranches villas reflected in a lake, with flowers in the foreground",
    "arabian-ranches-02.jpg": "Elevated sunset view over Arabian Ranches villas, a lake and the golf course",
    "jumeirah-islands-01.jpg": "Aerial of the Jumeirah Islands villa clusters set in lakes, with the JLT and Marina skyline behind",
    "emirates-hills-02.jpg": "The Montgomerie golf course in Emirates Hills with the Dubai Marina towers behind",
}
# The two general images keep descriptive bases.
GENERAL_BASE = {"dubai-skyline-villas-01.jpg": "uae-dubai-skyline-villas-01", "abu-dhabi-skyline-01.jpg": "uae-abu-dhabi-skyline-01"}

def alt_for(folder, e):
    if e["file"] in ALT:
        a = ALT[e["file"]]
    else:
        a = re.sub(r"^Photograph of (an? |the )?", "", e["shows"].strip()).rstrip(".")
        a = a[0].upper() + a[1:]
        if not any(h in a for h in NAME_HINTS[folder]):
            a += ", " + NAMES[folder][0]
    if len(a) >= 125:
        raise SystemExit(f"alt text too long ({len(a)}) for {folder}/{e['file']}: {a}")
    return a

def base_for(folder, e):
    if folder == "general":
        return GENERAL_BASE[e["file"]]
    num = re.search(r"-(\d+)\.\w+$", e["file"]).group(1)
    return f"uae-{folder}-{num}"

def fresh(dst, src, force):
    return not force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime

def load(src):
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")

def make(folder, e, force):
    src = SRC / folder / e["file"]
    base = base_for(folder, e)
    im = None
    w, h = Image.open(src).size
    written = []
    for size in ((320,) + SIZES if e["role"] == "hero" else SIZES):  # 320: /areas/ hub thumbnails
        if size > w:
            continue  # never upscale
        dst = OUT / f"{base}-{size}.webp"
        if fresh(dst, src, force):
            continue
        im = im or load(src)
        r = im if size == w else im.resize((size, round(h * size / w)), Image.LANCZOS)
        q = QUALITY
        r.save(dst, "WEBP", quality=q, method=6)
        while size in BUDGET and dst.stat().st_size > BUDGET[size] and q > MIN_QUALITY:
            q -= 3
            r.save(dst, "WEBP", quality=q, method=6)
        written.append(dst.name)
    og = w >= OG[0] and (e["role"] == "hero" or folder == "general")
    if og:
        dst = OUT / f"{base}-og.jpg"
        if not fresh(dst, src, force):
            im = im or load(src)
            ImageOps.fit(im, OG, Image.LANCZOS, centering=(0.5, 0.5)).save(dst, "JPEG", quality=82, optimize=True, progressive=True)
            written.append(dst.name)
    name, place = NAMES[folder]
    entry = {"base": base, "w": w, "h": h, "src": f"assets-src/uae-images/{folder}/{e['file']}",
             "name": name, "place": place, "photo": e["credit"], "credit": e["credit"],
             "alt": alt_for(folder, e), "role": e["role"], "is_render": bool(e.get("is_render")),
             "source_page": e.get("source_page", ""), "og": og, "uae": True}
    if e.get("licence"):
        entry["licence"] = e["licence"]
    return entry, written

def main():
    force = "--force" in sys.argv
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest = {k: v for k, v in manifest.items() if not k.startswith("uae-")}
    total = 0
    for folder in sorted(p.name for p in SRC.iterdir() if (p / "manifest.json").exists()):
        if folder not in NAMES:
            raise SystemExit(f"add {folder} to NAMES in tools/make_uae_images.py")
        entries = json.loads((SRC / folder / "manifest.json").read_text(encoding="utf-8"))
        out = []
        for e in entries:
            entry, written = make(folder, e, force)
            out.append(entry)
            total += len(written)
        if folder == "general":
            out.sort(key=lambda m: m["base"] != "uae-dubai-skyline-villas-01")
        else:
            out.sort(key=lambda m: m["base"])
        manifest[f"uae-{folder}"] = out
    keep = {f"{m['base']}-og.jpg" for v in manifest.values() for m in v if m.get("og")}
    for f in OUT.glob("uae-*-og.jpg"):
        if f.name not in keep:
            f.unlink()
    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    n = sum(len(v) for k, v in manifest.items() if k.startswith("uae-"))
    print(f"{n} UAE images in src/img_manifest.json; {total} files written to {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
