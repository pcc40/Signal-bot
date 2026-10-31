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
    lang = rel.split("/")[1] if rel.split("/")[1] in ("ar", "ru", "zh", "hi") else "en"
    titles.setdefault(t, []).append((lang, rel)); descs.setdefault(d, []).append(rel)
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
    # Two pages in the same language sharing a title is an error. The same title on language versions of one
    # page means the translation is still pending (English fallback): a warning, like "partly untranslated".
    langs = [l for l, _ in v]
    if len(langs) != len(set(langs)): errors.append(f"duplicate title '{k}': {[r for _, r in v]}")
    elif len(v) > 1: warns.append(f"title not yet translated on {[r for l, r in v if l != 'en']}")
for k, v in descs.items():
    if len(v) > 1: warns.append(f"duplicate description on {v}")

# ---------------------------------------------------------------- structure, schema, media, machine files
sys.path.insert(0, os.path.join(ROOT, "src"))
import config as C
import xml.etree.ElementTree as ET
LANG_DIRS = ("ar", "ru", "zh", "hi")

def rel_of(f):
    return f.replace(D, "")

def path_of(rel):
    return rel[:-len("index.html")] if rel.endswith("index.html") else rel

def is_en(rel):
    return rel.split("/")[1] not in LANG_DIRS

ids_defined, ids_types, ids_refs = {}, {}, {}
inbound = {}
en_pages = {}
for f in files:
    s = open(f, encoding="utf-8").read()
    rel = rel_of(f)
    # og:image must be a real file
    m = re.search(r'<meta (?=[^>]*property="og:image")[^>]*content="([^"]+)"', s)
    if not m:
        errors.append(f"no og:image on {rel}")
    else:
        u = m.group(1)
        if not u.startswith(C.SITE_URL + "/"):
            errors.append(f"og:image not on site domain on {rel}: {u}")
        elif not os.path.exists(D + u[len(C.SITE_URL):].split("?")[0]):
            errors.append(f"og:image file missing on {rel}: {u}")
    # every <img> carries width and height (prevents layout shift)
    for tag in re.findall(r"<img\b[^>]*>", s):
        if not re.search(r'\swidth="\d+"', tag) or not re.search(r'\sheight="\d+"', tag):
            errors.append(f"img without width/height on {rel}: {tag[:90]}")
    if not is_en(rel) or "404" in rel:
        continue
    path = path_of(rel)
    noindex = 'content="noindex' in s
    en_pages[path] = noindex
    # JSON-LD @id bookkeeping (English pages; translations mirror them)
    def visit(o, top):
        if isinstance(o, list):
            for x in o: visit(x, False)
        elif isinstance(o, dict):
            i = o.get("@id")
            if i:
                if not i.startswith(C.SITE_URL + "/"):
                    errors.append(f"JSON-LD @id not an absolute site URL on {rel}: {i}")
                t = o.get("@type")
                t = set(t if isinstance(t, list) else [t]) if t else set()
                if t:
                    ids_types.setdefault(i, []).append((t, rel))
                # a node with properties beyond @id (nested or top-level) defines it; a bare {"@id": ...} refers to it
                if top or (t and len(set(o) - {"@id", "@type"}) > 0):
                    ids_defined.setdefault(i, set()).add(rel)
                else:
                    ids_refs.setdefault(i, set()).add(rel)
            for k, v in o.items():
                if k != "@id": visit(v, False)
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: visit(json.loads(j), True)
        except Exception: pass
    # internal links: within <main> for the 'thin linking' check, anywhere for the orphan check
    main = s.split("<main", 1)[-1].split("</main>", 1)[0]
    main_links = {h.split("#")[0] for h in re.findall(r'href="(/[^"?]*)', main)} - {path, ""}
    if not noindex and len(main_links) < 3 and path not in ("/privacy/", "/terms/", "/contact/"):  # utility pages
        warns.append(f"only {len(main_links)} internal links in the main content of {rel}")
    for h in {h.split("#")[0] for h in re.findall(r'href="(/[^"?]*)', s)}:
        if h != path:
            inbound.setdefault(h, set()).add(path)

for i, refs in ids_refs.items():
    if i not in ids_defined:
        errors.append(f"JSON-LD @id {i} is referenced (on {sorted(refs)[0]}) but never defined as a full node")
for i, ts in ids_types.items():
    for t, rel in ts:
        if not t & ts[0][0]:
            errors.append(f"JSON-LD @id {i} has inconsistent @type: {sorted(ts[0][0])} on {ts[0][1]} vs {sorted(t)} on {rel}")
            break
for path, noindex in en_pages.items():
    if path != "/" and not noindex and not inbound.get(path):
        errors.append(f"orphan page (no internal links point to it): {path}")

# sitemap, feed and llms files
sm_urls = []
try:
    sm = ET.parse(os.path.join(D, "sitemap.xml")).getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for u in sm.findall("s:url", ns):
        loc = u.find("s:loc", ns).text
        lm = u.find("s:lastmod", ns)
        if lm is None or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm.text or ""):
            errors.append(f"sitemap entry without a valid lastmod: {loc}")
        sm_urls.append(loc)
        p = loc[len(C.SITE_URL):]
        if not os.path.exists(D + p + ("index.html" if p.endswith("/") else "")):
            errors.append(f"sitemap URL has no page: {loc}")
    en_sm = {u[len(C.SITE_URL):] for u in sm_urls if is_en(u[len(C.SITE_URL):] + "x")}
    for path, noindex in en_pages.items():
        if not noindex and path not in en_sm:
            errors.append(f"indexable page missing from sitemap: {path}")
except Exception as e:
    errors.append(f"sitemap.xml invalid: {e}")
try:
    feed = ET.parse(os.path.join(D, "insights/feed.xml")).getroot()
    if len(feed.findall("channel/item")) == 0:
        errors.append("insights/feed.xml has no items")
    for it in feed.findall("channel/item"):
        p = it.find("link").text[len(C.SITE_URL):]
        if not os.path.exists(D + p + "index.html"):
            errors.append(f"feed item links to a missing page: {p}")
except Exception as e:
    errors.append(f"insights/feed.xml invalid: {e}")
for name in ("llms.txt", "llms-full.txt", "robots.txt", ".well-known/security.txt"):
    if not os.path.exists(os.path.join(D, name)):
        errors.append(f"missing /{name}")
if os.path.exists(os.path.join(D, "llms.txt")):
    for u in re.findall(r"\((https?://[^)\s]+)\)", open(os.path.join(D, "llms.txt"), encoding="utf-8").read()):
        if u.startswith(C.SITE_URL):
            p = u[len(C.SITE_URL):].split("#")[0]
            if not os.path.exists(D + p + ("index.html" if p.endswith("/") else "")):
                errors.append(f"llms.txt links to a missing page: {u}")
for a in ("/assets/logo.png", "/favicon.svg", "/apple-touch-icon.png", "/site.webmanifest"):
    if not os.path.exists(D + a):
        errors.append(f"missing {a}")

print(f"Audited {len(files)} pages: {len(errors)} errors, {len(warns)} warnings")
for e in errors: print("ERROR", e)
for w in warns[:40]: print("warn ", w)
sys.exit(1 if errors else 0)
