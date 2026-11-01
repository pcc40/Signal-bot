#!/usr/bin/env python3
"""Technical SEO audit of the built site (dist/). Exit code 1 if anything blocks publishing.
Includes the build safeguards (canonical targets, JSON-LD validity and banned types, FAQ duplicates, title/h1,
placeholder text, "test" URLs, contact facts against src/config.py, key facts in static HTML).
Usage: python3 tools/seo_audit.py            (after python3 build.py)"""
import re, glob, os, json, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "dist")
FORBIDDEN = [r"\bwe supervise\b", r"supervision consultant(?! [a-z]* ?(?:is|carries|on))", r"\bwe (?:obtain|submit) (?:your )?(?:building )?permits?\b",
             r"\bprepare tender documents\b", r"\bprequalif", r"\bwe certify\b", r"#1\b", r"\bbest villa contractor in dubai\b(?!\?)"]
errors, warns = [], []
files = glob.glob(D + "/**/*.html", recursive=True)
titles, descs = {}, {}

# ---------------------------------------------------------------- build safeguards (competitor brief, item 8)
sys.path.insert(0, os.path.join(ROOT, "src"))
import config as C
TITLE_MAX = 60  # English titles, including the " | Eastbridge" suffix
# English pages whose titles are over TITLE_MAX and are owned by another work round (fees page in src/pages.py
# fees(), claims service in src/content/services.py). They report as warnings until shortened; any other page
# over TITLE_MAX is an error. Remove an entry once its title is 60 characters or fewer.
LONG_TITLE_PENDING = {"/fees/", "/services/variations-delays-and-claims/"}
BANNED_TYPES = {"Review", "AggregateRating", "Rating", "EmployerAggregateRating", "HowTo", "HowToStep",
                "HowToSection", "HowToDirection", "GovernmentService"}
BANNED_PROPS = {"review", "reviews", "aggregateRating", "reviewRating"}
PLACEHOLDERS = [(r"lorem ipsum", re.I), (r"\[link:", 0), (r"\bTODO\b", 0)]
ORG_ID = C.SITE_URL + "/#org"
OUR_NAMES = {C.NAME, C.SHORT, C.LEGAL}
DIGITS = lambda x: re.sub(r"\D", "", str(x or ""))
LICENCE_NO = re.search(r"\d[\d.]*\d", C.LICENCE).group(0)

def ld_checks(o, rel, ours=False):
    """Walk one JSON-LD tree: banned types/properties, FAQ duplicates, and business facts against src/config.py."""
    if isinstance(o, list):
        for x in o: ld_checks(x, rel, ours)
        return
    if not isinstance(o, dict):
        return
    t = o.get("@type")
    t = set(t if isinstance(t, list) else [t]) if t else set()
    for b in sorted(t & BANNED_TYPES):
        errors.append(f"JSON-LD type {b} not allowed on {rel}")
    for b in sorted(set(o) & BANNED_PROPS):
        errors.append(f"JSON-LD property {b} not allowed on {rel}")
    if "FAQPage" in t:
        seen = set()
        qs = o.get("mainEntity") or []
        for q in (qs if isinstance(qs, list) else [qs]):
            n = " ".join(str(q.get("name", "")).lower().split()) if isinstance(q, dict) else ""
            if not n or not isinstance(q.get("acceptedAnswer"), dict) or not q["acceptedAnswer"].get("text"):
                errors.append(f"FAQPage question without name or answer on {rel}")
            elif n in seen:
                errors.append(f"duplicate FAQPage question on {rel}: {q.get('name')}")
            seen.add(n)
    # a node is ours when it is the site organisation or carries our name; its address and contact point inherit that
    if o.get("@id") == ORG_ID or o.get("name") in OUR_NAMES or o.get("legalName") == C.LEGAL:
        ours = True
    elif o.get("name") and t & {"Organization", "LocalBusiness", "ProfessionalService", "Corporation", "Person"}:
        ours = False
    if o.get("@id") == ORG_ID and "name" in o and o["name"] != C.NAME:
        errors.append(f"JSON-LD organisation name '{o['name']}' differs from config NAME on {rel}")
    if ours:
        if "telephone" in o and DIGITS(o["telephone"]) != DIGITS(C.PHONE_E164):
            errors.append(f"JSON-LD telephone {o['telephone']} differs from config on {rel}")
        if "email" in o and str(o["email"]).replace("mailto:", "") != C.EMAIL:
            errors.append(f"JSON-LD email {o['email']} differs from config on {rel}")
        if "legalName" in o and o["legalName"] != C.LEGAL:
            errors.append(f"JSON-LD legalName {o['legalName']} differs from config on {rel}")
        if "streetAddress" in o and o["streetAddress"] != C.ADDRESS["street"]:
            errors.append(f"JSON-LD streetAddress differs from config on {rel}")
    for k, v in o.items():
        if k != "@id": ld_checks(v, rel, ours)

def path_has_test(p):
    return any(re.search(r"(?:^|[-_.])test(?:s|ing)?(?:$|[-_.])", seg, re.I) for seg in p.split("/"))

for f in files:
    s = open(f, encoding="utf-8").read()
    rel = f.replace(D, "")
    page_path = rel[:-len("index.html")] if rel.endswith("index.html") else rel
    lang0 = rel.split("/")[1] if rel.split("/")[1] in ("ar", "ru", "zh", "hi") else "en"
    # canonical: exactly one, on the site domain, pointing at a page that exists in dist/
    cans = re.findall(r'<link (?=[^>]*rel="canonical")[^>]*href="([^"]+)"', s)
    if len(cans) != 1:
        errors.append(f"{len(cans)} canonical links on {rel}")
    for cu in cans:
        if not cu.startswith(C.SITE_URL + "/"):
            errors.append(f"canonical off the site domain on {rel}: {cu}")
        else:
            cp = cu[len(C.SITE_URL):].split("#")[0].split("?")[0]
            if not os.path.exists(D + cp + ("index.html" if cp.endswith("/") else "")):
                errors.append(f"canonical points to a path missing from dist/ on {rel}: {cu}")
    # "test" in a URL: the page's own path and every internal link
    if path_has_test(page_path):
        errors.append(f"'test' in the URL path {page_path}")
    for h in set(re.findall(r'href="(?:' + re.escape(C.SITE_URL) + r')?(/[^"#?]*)', s)):
        if path_has_test(h):
            errors.append(f"link to a URL with 'test' in its path on {rel}: {h}")
    # JSON-LD: valid, typed, schema.org context, no banned types, no duplicate FAQ questions, facts match config
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            o = json.loads(j)
        except Exception:
            continue  # reported below as bad JSON-LD
        for top in (o if isinstance(o, list) else [o]):
            if not isinstance(top, dict) or "schema.org" not in str(top.get("@context", "")):
                errors.append(f"JSON-LD block without a schema.org @context on {rel}")
            elif "@type" not in top and "@graph" not in top:
                errors.append(f"JSON-LD block without @type on {rel}")
        ld_checks(o, rel)
    # rendered text: scripts, styles and templates removed (what a crawler sees without running JavaScript)
    static = re.sub(r"<(script|style|template|noscript)\b.*?</\1>", " ", s, flags=re.S | re.I)
    rtext = html.unescape(re.sub(r"<[^>]+>", " ", static))
    for pat, fl in PLACEHOLDERS:
        if re.search(pat, rtext, fl):
            errors.append(f"placeholder text '{pat}' on {rel}")
    # title and h1 must be present and non-empty; English titles at most TITLE_MAX characters
    tm = re.search(r"<title>(.*?)</title>", s, re.S)
    if not tm or not tm.group(1).strip():
        errors.append(f"missing or empty title on {rel}")
    elif lang0 == "en" and len(html.unescape(tm.group(1).strip())) > TITLE_MAX:
        tl = len(html.unescape(tm.group(1).strip()))
        (warns if page_path in LONG_TITLE_PENDING else errors).append(f"title over {TITLE_MAX} characters ({tl}) on {rel}")
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", s, re.S)
    if not h1 or not re.sub(r"<[^>]+>", "", h1.group(1)).strip():
        errors.append(f"missing or empty h1 on {rel}")
    # contact details in the HTML must match src/config.py
    for tel in set(re.findall(r'href="tel:([^"]+)"', s)):
        if DIGITS(tel) != DIGITS(C.PHONE_E164):
            errors.append(f"tel: link {tel} differs from config on {rel}")
    for a_tel, a_txt in re.findall(r'<a [^>]*href="tel:([^"]+)"[^>]*>(.*?)</a>', s, re.S):
        shown = DIGITS(re.sub(r"<[^>]+>", "", a_txt))
        if len(shown) >= 7 and shown != DIGITS(a_tel):
            errors.append(f"phone shown as '{a_txt.strip()[:40]}' but dials {a_tel} on {rel}")
    for wa in set(re.findall(r"wa\.me/(\d+)", s)):
        if wa != C.WHATSAPP:
            errors.append(f"WhatsApp link {wa} differs from config on {rel}")
    for em in set(re.findall(r"[A-Za-z0-9._%+-]+@" + re.escape(C.EMAIL.split("@")[1]), s)):
        if em != C.EMAIL:
            errors.append(f"email {em} differs from config on {rel}")
    # key facts in the static HTML (footer), not only injected by JavaScript. Embed pages carry no footer by design.
    if "/embed/" not in rel:
        for label, ok in (("phone", C.PHONE_DISPLAY in rtext and "tel:" + C.PHONE_E164 in static),
                          ("email", C.EMAIL in rtext), ("licence number", LICENCE_NO in rtext)):
            if not ok:
                errors.append(f"key fact ({label}) missing from the static HTML of {rel}")
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
    # noindex is expected on 404, thank-you pages and the embeddable calculator (/embed/, canonical to the full page)
    if "noindex" in s and "404" not in rel and "thanks" not in rel and "/embed/" not in rel: warns.append(f"noindex on {rel}")
    if "/embed/" in rel:
        if 'content="noindex' not in s: errors.append(f"embed page without noindex: {rel}")
        if re.search(r'<a (?![^>]*target="_blank")[^>]*href=', s): errors.append(f"embed page link that would open inside the iframe: {rel}")
        if 'class="site-head"' in s or 'class="site-foot"' in s: errors.append(f"embed page carries the site header or footer: {rel}")
        can = re.search(r'<link [^>]*rel="canonical"[^>]*href="([^"]+)"', s) or re.search(r'<link [^>]*href="([^"]+)"[^>]*rel="canonical"', s)
        if not can or "/embed/" in can.group(1): errors.append(f"embed page must be canonical to the full calculator: {rel}")
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
    # Thank-you pages and the embed page are noindex and carry no hreflang (build.py leaves it out, so hreflang never
    # points at URLs that are not canonical); every other page needs the full set.
    exempt = "404" in rel or "thanks" in rel or "/embed/" in rel
    if exempt and "x-default" not in s and 'content="noindex' not in s: errors.append(f"page without hreflang is not noindex: {rel}")
    if exempt and 'hreflang="x-default"' in s and ("thanks" in rel or "/embed/" in rel): errors.append(f"hreflang on a noindex page: {rel}")
    if not exempt and s.count('hreflang="x-default"') < 1: errors.append(f"no hreflang on {rel}")
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
try:
    sm_text = open(os.path.join(D, "sitemap.xml"), encoding="utf-8").read()
    if "/embed/" in sm_text: errors.append("sitemap.xml lists an embed page (they are noindex)")
except OSError:
    pass

# ---------------------------------------------------------------- structure, schema, media, machine files
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
for name in ("llms.txt", "llms-full.txt"):
    try:
        lt = open(os.path.join(D, name), encoding="utf-8").read()
    except OSError:
        continue
    for pat, fl in PLACEHOLDERS:
        if re.search(pat, lt, fl):
            errors.append(f"placeholder text '{pat}' in /{name}")
    for label, val in (("phone", C.PHONE_DISPLAY), ("email", C.EMAIL), ("licence", C.LICENCE)):
        if val not in lt:
            errors.append(f"/{name} does not state the {label} from config ({val})")
for a in ("/assets/logo.png", "/favicon.svg", "/apple-touch-icon.png", "/site.webmanifest"):
    if not os.path.exists(D + a):
        errors.append(f"missing {a}")

print(f"Audited {len(files)} pages: {len(errors)} errors, {len(warns)} warnings")
for e in errors: print("ERROR", e)
for w in sorted(warns, key=lambda w: "untranslated" in w)[:40]: print("warn ", w)  # untranslated last
sys.exit(1 if errors else 0)
