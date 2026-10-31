#!/usr/bin/env python3
"""Technical SEO audit of the built site (dist/). Exit code 1 if anything blocks publishing.
Usage: python3 tools/seo_audit.py            (after python3 build.py)"""
import re, glob, os, json, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "dist")
FORBIDDEN = [r"\bwe supervise\b", r"supervision consultant(?! [a-z]* ?(?:is|carries|on))", r"\bwe (?:obtain|submit) (?:your )?(?:building )?permits?\b",
             r"\bprepare tender documents\b", r"\bprequalif", r"\bwe certify\b", r"#1\b", r"\bbest villa contractor in dubai\b(?!\?)"]
errors, warns = [], []
files = glob.glob(D + "/**/*.html", recursive=True)
titles, descs = {}, {}
for f in files:
    s = open(f, encoding="utf-8").read()
    rel = f.replace(D, "")
    for h in re.findall(r'href="(/[^"#?]*)', s):
        p = D + h + ("index.html" if h.endswith("/") else "")
        if not os.path.exists(p): errors.append(f"broken link {h} on {rel}")
    for ss in re.findall(r'srcset="([^"]+)"', s):
        for u in re.findall(r'(/assets/[^\s,]+)', ss):
            if not os.path.exists(D + u): errors.append(f"missing image {u} on {rel}")
    for src in re.findall(r'src="(/[^"?]+)', s):
        if not os.path.exists(D + src): errors.append(f"missing asset {src} on {rel}")
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as e: errors.append(f"bad JSON-LD on {rel}: {e}")
    if "noindex" in s and "404" not in rel and "thanks" not in rel: warns.append(f"noindex on {rel}")
    t = re.search(r"<title>(.*?)</title>", s); d = re.search(r'<meta (?=[^>]*name="description")[^>]*content="(.*?)"', s)
    if not t or not d: errors.append(f"missing title/description on {rel}"); continue
    t, d = html.unescape(t.group(1)), html.unescape(d.group(1))
    titles.setdefault(t, []).append(rel); descs.setdefault(d, []).append(rel)
    lang = rel.split("/")[1] if rel.split("/")[1] in ("ar", "ru", "zh", "hi") else "en"
    if lang != "en":
        if 'dir="rtl"' not in s and lang == "ar": errors.append(f"Arabic page not right-to-left {rel}")
        body = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)\b.*?</\1>", "", s.split("<body", 1)[-1], flags=re.S))
        latin = len(re.findall(r"\b[a-z]{4,}\b", body)); allw = len(body.split())
        if allw and latin / allw > 0.12: warns.append(f"looks partly untranslated ({latin}/{allw} English words) {rel}")
    if s.count('hreflang="x-default"') < 1 and "404" not in rel: errors.append(f"no hreflang on {rel}")
    if len(t) > 65 and lang == "en": warns.append(f"long title ({len(t)}) {rel}")
    if len(d) > 170 and lang == "en": warns.append(f"long description ({len(d)}) {rel}")
    if s.count("<h1") != 1: errors.append(f"{s.count('<h1')} h1 tags on {rel}")
    for m in re.findall(r"<img [^>]*>", s):
        if 'alt="' not in m: errors.append(f"img without alt on {rel}")
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", s, flags=re.S))
    for pat in FORBIDDEN:
        if re.search(pat, text, re.I): errors.append(f"compliance wording '{pat}' on {rel}")
for k, v in titles.items():
    if len(v) > 1:
        # Same page in several languages, awaiting translation: warn (the untranslated check also flags it).
        same_page = len({re.sub(r"^/(ar|ru|zh|hi)/", "/", r) for r in v}) == 1
        (warns if same_page else errors).append(f"duplicate title '{k}': {v}")
for k, v in descs.items():
    if len(v) > 1: warns.append(f"duplicate description on {v}")
print(f"Audited {len(files)} pages: {len(errors)} errors, {len(warns)} warnings")
for e in errors: print("ERROR", e)
for w in warns[:40]: print("warn ", w)
sys.exit(1 if errors else 0)
