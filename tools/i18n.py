#!/usr/bin/env python3
"""Multilingual layer for the Eastbridge site.

The English site is built first (python3 build.py). This tool then:
  extract  -> collects every translatable segment from dist/ into src/i18n/segments.json
              and lists, per language, the segments still missing a translation
              (src/i18n/todo-<lang>.json)
  apply    -> writes translated copies of every page to dist/<lang>/..., with lang/dir,
              localised links, canonical + hreflang, translated metadata and JSON-LD,
              and a localised sitemap

Translations live in src/i18n/<lang>.json as {segment_key: translated_html}.
A segment is the inner HTML of a 'leaf' block (a block with text and no block children),
or an attribute value (alt, aria-label, placeholder, meta description, title).
Keys are a hash of the English text, so unchanged text keeps its translation when the
site is rebuilt, and new or edited text shows up in the todo file.

Usage:  python3 tools/i18n.py extract
        python3 tools/i18n.py apply
"""
import hashlib, json, os, re, sys, glob
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
I18N = ROOT / "src" / "i18n"
sys.path.insert(0, str(ROOT / "src"))
import config as C

LANGS = {  # code: (native name, html lang, dir, og locale)
    "ar": ("العربية", "ar", "rtl", "ar_AE"),
    "ru": ("Русский", "ru", "ltr", "ru_RU"),
    "zh": ("中文", "zh-Hans", "ltr", "zh_CN"),
    "hi": ("हिन्दी", "hi", "ltr", "hi_IN"),
}
ALL = ["en"] + list(LANGS)
NATIVE = {"en": "English", **{k: v[0] for k, v in LANGS.items()}}

BLOCK = {"address", "article", "aside", "blockquote", "details", "dialog", "dd", "div", "dl", "dt", "fieldset",
         "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "li",
         "main", "nav", "ol", "p", "section", "table", "tbody", "thead", "tfoot", "tr", "td", "th", "ul",
         "summary", "select", "option", "svg", "picture", "iframe", "body", "html", "label", "legend", "button"}
SKIP = {"script", "style", "noscript", "head", "template"}
ATTRS = ["alt", "aria-label", "placeholder", "title", "data-title"]
LD_KEYS = {"name", "text", "description", "headline", "slogan", "about", "serviceType", "jobTitle", "genre"}

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

IMG_TAG = re.compile(r"<(img|source)\b[^>]*?>")

def strip_media(s):
    """Image URLs, sizes and dimensions don't change the words, so they don't change the key."""
    def keep_alt(m):
        alt = re.search(r'\salt="[^"]*"', m.group(0))
        return f"<{m.group(1)}{alt.group(0) if alt else ''}>"
    return IMG_TAG.sub(keep_alt, s)

def key(s):
    return hashlib.sha1(strip_media(norm(s)).encode("utf-8")).hexdigest()[:16]

def has_letters(s):
    return re.search(r"[A-Za-z]{2,}", s) is not None

def has_block_desc(el):
    return any(isinstance(d, Tag) and d.name in BLOCK for d in el.descendants)

def inner(el):
    return "".join(str(c) for c in el.contents)

def notranslate(el):
    for p in [el] + list(el.parents):
        if isinstance(p, Tag) and (p.get("translate") == "no" or "notranslate" in (p.get("class") or [])):
            return True
    return False

def walk(el, out):
    """Yield ('el', tag) for leaf segments and ('txt', node) for loose text nodes."""
    for c in list(el.children):
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            if has_letters(str(c)) and el.name not in SKIP and not notranslate(el):
                out.append(("txt", c))
            continue
        if not isinstance(c, Tag) or c.name in SKIP or notranslate(c):
            continue
        if c.name == "svg":
            for t in c.find_all(["text", "title", "tspan"]):
                if has_letters(t.get_text()) and not t.find(["tspan"]):
                    out.append(("el", t))
            continue
        text = c.get_text()
        if not has_letters(text):
            continue
        if c.name not in ("html", "body") and not has_block_desc(c) and c.name != "select":
            out.append(("el", c))
        else:
            walk(c, out)

def segments_of(soup):
    out = []
    if soup.body:
        walk(soup.body, out)
    return out

def attr_targets(soup):
    res = []
    for el in soup.find_all(True):
        if el.name in SKIP and el.name != "head":
            continue
        for a in ATTRS:
            v = el.get(a)
            if v and has_letters(v) and not notranslate(el):
                res.append((el, a))
    for m in soup.find_all("meta"):
        if m.get("name") in ("description",) or m.get("property") in ("og:title", "og:description"):
            if m.get("content") and has_letters(m["content"]):
                res.append((m, "content"))
    return res

def ld_strings(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in LD_KEYS and isinstance(v, str) and has_letters(v):
                acc.append(v)
            else:
                ld_strings(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            ld_strings(v, acc)

def english_pages():
    pages = []
    for f in sorted(DIST.rglob("*.html")):
        rel = f.relative_to(DIST).as_posix()
        if rel.split("/")[0] in LANGS:
            continue
        pages.append(f)
    return pages

def load(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default

# ---------------------------------------------------------------- extract
def extract():
    I18N.mkdir(parents=True, exist_ok=True)
    segs = {}
    for f in english_pages():
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        if soup.title and has_letters(soup.title.get_text()):
            t = soup.title.get_text(); segs[key(t)] = norm(t)
        for kind, node in segments_of(soup):
            h = norm(str(node)) if kind == "txt" else norm(inner(node))
            segs[key(h)] = h
        for el, a in attr_targets(soup):
            v = norm(el[a]); segs[key(v)] = v
        for s in soup.find_all("script", type="application/ld+json"):
            acc = []
            ld_strings(json.loads(s.string), acc)
            for v in acc:
                segs[key(v)] = norm(v)
    (I18N / "segments.json").write_text(json.dumps(segs, ensure_ascii=False, indent=0), encoding="utf-8")
    words = sum(len(re.sub(r"<[^>]+>", " ", v).split()) for v in segs.values())
    print(f"{len(segs)} segments, about {words} words")
    for lang in LANGS:
        tr = load(I18N / f"{lang}.json", {})
        todo = {k: v for k, v in segs.items() if k not in tr}
        (I18N / f"todo-{lang}.json").write_text(json.dumps(todo, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"  {lang}: {len(todo)} to translate")

# ---------------------------------------------------------------- apply
EXT = re.compile(r"\.(xml|txt|webp|png|jpg|svg|woff2|css|js|json|webmanifest|ico|pdf)$")

def local_href(h, lang):
    if not h or not h.startswith("/") or h.startswith("//") or h.startswith("/assets/") or EXT.search(h.split("#")[0]):
        return h
    if any(h.startswith(f"/{l}/") or h == f"/{l}" for l in LANGS):
        return h
    return f"/{lang}{h}"

def page_path(f):
    rel = "/" + f.relative_to(DIST).as_posix()
    return rel[: -len("index.html")] if rel.endswith("index.html") else rel

def lang_url(path, lang):
    return path if lang == "en" else f"/{lang}{path}"

# Python 3.11's html.parser drops a bare '&' near the end of a fragment ("FF&E" -> "FFE"); escape it first.
BARE_AMP = re.compile(r"&(?!#\d+;|#[xX][0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]*;)")

CUR_ATTR = ' aria-current="true"'

def switcher(path, cur):
    items = "".join(
        f'<li><a href="{lang_url(path, l)}" hreflang="{(LANGS[l][1] if l != "en" else "en")}" lang="{(LANGS[l][1] if l != "en" else "en")}" data-lang="{l}"'
        f'{CUR_ATTR if l == cur else ""}>{NATIVE[l]}</a></li>' for l in ALL)
    return f'<nav class="langs" aria-label="Language" translate="no"><ul>{items}</ul></nav>'

def add_alternates(soup, path):
    head = soup.head
    for l in soup.find_all("link", rel="alternate"):
        if l.get("hreflang"):
            l.decompose()
    for l in ALL:
        t = soup.new_tag("link", rel="alternate", href=C.SITE_URL + lang_url(path, l))
        t["hreflang"] = "en" if l == "en" else LANGS[l][1]
        head.append(t)
    t = soup.new_tag("link", rel="alternate", href=C.SITE_URL + path); t["hreflang"] = "x-default"; head.append(t)

def tag_forms(soup, lang):
    for fm in soup.find_all("form"):
        if not fm.find("input", attrs={"name": "language"}):
            fm.insert(0, soup.new_tag("input", attrs={"type": "hidden", "name": "language", "value": lang}))
        else:
            fm.find("input", attrs={"name": "language"})["value"] = lang
        # Netlify registers each form (and the field labels it shows in the dashboard and in
        # notification emails) from the HTML it finds at deploy. The same form name on five
        # language pages would let a translated copy define the labels, so only the English
        # page carries data-netlify. Translated pages post to the same form via form-name.
        if lang != "en" and fm.has_attr("data-netlify"):
            if not fm.find("input", attrs={"name": "form-name"}):
                fm.insert(0, soup.new_tag("input", attrs={"type": "hidden", "name": "form-name", "value": fm.get("name", "")}))
            del fm["data-netlify"]
            if fm.has_attr("netlify-honeypot"):
                del fm["netlify-honeypot"]

def insert_switcher(soup, path, cur):
    for old in soup.select("nav.langs"):
        old.decompose()
    u = soup.select_one(".utility .u-right")
    if u:
        u.insert(0, BeautifulSoup(switcher(path, cur), "html.parser"))
    nav = soup.select_one("#nav")
    if nav:
        nav.append(BeautifulSoup(switcher(path, cur).replace('class="langs"', 'class="langs langs--nav"'), "html.parser"))

FONTS = {
    "ar": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Noto+Naskh+Arabic:wght@500&display=swap",
    "ru": "https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=Noto+Serif+Display:wght@400&display=swap",
    "zh": "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Noto+Serif+SC:wght@500&display=swap",
    "hi": "https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600&family=Noto+Serif+Devanagari:wght@500&display=swap",
}

def translate_page(f, lang, tr, missing):
    soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    path = page_path(f)
    def T(s):
        k = key(s)
        if k in tr:
            return tr[k]
        missing.add(k)
        return None
    attrs = [(el, a, el[a]) for el, a in attr_targets(soup)]
    # text segments
    for kind, node in segments_of(soup):
        if kind == "txt":
            v = T(str(node))
            if v is not None:
                node.replace_with(NavigableString(v))
        else:
            v = T(inner(node))
            if v is not None:
                src_imgs = [dict(i.attrs) for i in node.find_all(["img", "source"])]
                node.clear()
                frag = BeautifulSoup(BARE_AMP.sub("&amp;", v), "html.parser")
                # take image files and sizes from the current English page, keep the translated alt text
                for i, img_attrs in zip(frag.find_all(["img", "source"]), src_imgs):
                    alt = i.get("alt")
                    i.attrs = dict(img_attrs)
                    if alt is not None:
                        i["alt"] = alt
                for c in list(frag.contents):
                    node.append(c)
    if soup.title:
        v = T(soup.title.get_text())
        if v: soup.title.string = v
        else: soup.title.string = soup.title.get_text() + " · " + NATIVE[lang]  # keep titles unique until translated
    for el, a, orig in attrs:
        v = T(orig)
        if v: el[a] = re.sub(r"<[^>]+>", "", v)
    for s in soup.find_all("script", type="application/ld+json"):
        data = json.loads(s.string)
        def tx(o):
            if isinstance(o, dict):
                for k2, v2 in list(o.items()):
                    if k2 in LD_KEYS and isinstance(v2, str) and has_letters(v2):
                        r = T(v2)
                        if r: o[k2] = re.sub(r"<[^>]+>", "", r)
                    elif k2 in ("url", "item", "mainEntityOfPage", "@id") and isinstance(v2, str) and v2.startswith(C.SITE_URL + "/") and "#" not in v2:
                        o[k2] = C.SITE_URL + local_href(v2[len(C.SITE_URL):], lang)
                    else:
                        tx(v2)
                if o.get("@type") in ("Article", "WebSite") or "inLanguage" in o:
                    o["inLanguage"] = LANGS[lang][1]
            elif isinstance(o, list):
                for v2 in o: tx(v2)
        tx(data)
        s.string = json.dumps(data, ensure_ascii=False)
    # links, forms
    for a in soup.find_all("a", href=True):
        if a.get("data-lang"):
            continue
        a["href"] = local_href(a["href"], lang)
    for fm in soup.find_all("form", action=True):
        fm["action"] = local_href(fm["action"], lang)
    # html attributes, canonical, og, fonts
    soup.html["lang"] = LANGS[lang][1]
    soup.html["dir"] = LANGS[lang][2]
    if LANGS[lang][2] == "rtl":
        for l in soup.find_all("link", rel="stylesheet"):
            if l.get("href", "").startswith("/assets/site.css"):
                l["href"] = l["href"].replace("/assets/site.css", "/assets/site-rtl.css")
    can = soup.find("link", rel="canonical")
    if can:
        # Usually the page itself; a page may point elsewhere (the calculator embed points to the full calculator).
        cpath = can["href"][len(C.SITE_URL):] if can["href"].startswith(C.SITE_URL + "/") else path
        can["href"] = C.SITE_URL + lang_url(cpath, lang)
    ogu = soup.find("meta", property="og:url")
    if ogu: ogu["content"] = C.SITE_URL + lang_url(path, lang)
    ogl = soup.find("meta", property="og:locale")
    if ogl: ogl["content"] = LANGS[lang][3]
    rss = soup.find("link", type="application/rss+xml")
    pre = soup.new_tag("link", rel="preconnect", href="https://fonts.gstatic.com"); pre["crossorigin"] = ""
    soup.head.append(pre)
    soup.head.append(soup.new_tag("link", rel="stylesheet", href=FONTS[lang]))
    add_alternates(soup, path)
    insert_switcher(soup, path, lang)
    tag_forms(soup, lang)
    out = DIST / lang / f.relative_to(DIST)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(soup), encoding="utf-8")
    return path

def merge():
    """Fold finished chunk files (src/i18n/parts/<lang>-NN.json) into src/i18n/<lang>.json."""
    for lang in LANGS:
        tr = load(I18N / f"{lang}.json", {})
        n = 0
        for part in sorted((I18N / "parts").glob(f"{lang}-*.json")):
            d = json.loads(part.read_text(encoding="utf-8"))
            tr.update(d); n += len(d)
        (I18N / f"{lang}.json").write_text(json.dumps(tr, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
        print(f"{lang}: {len(tr)} translations ({n} from parts)")

def apply():
    pages = english_pages()
    report = {}
    for lang in LANGS:
        tr = load(I18N / f"{lang}.json", {})
        missing = set()
        for f in pages:
            translate_page(f, lang, tr, missing)
        report[lang] = len(missing)
    # English pages: alternates + switcher
    for f in pages:
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        path = page_path(f)
        add_alternates(soup, path)
        insert_switcher(soup, path, "en")
        tag_forms(soup, "en")
        f.write_text(str(soup), encoding="utf-8")
    # sitemap with alternates
    sm = (DIST / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<url><loc>(.*?)</loc><lastmod>(.*?)</lastmod><priority>(.*?)</priority></url>", sm)
    out = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, lm, pr in locs:
        path = loc[len(C.SITE_URL):]
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{("en" if l == "en" else LANGS[l][1])}" href="{C.SITE_URL + lang_url(path, l)}"/>' for l in ALL)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>'
        for l in ALL:
            out.append(f"<url><loc>{C.SITE_URL + lang_url(path, l)}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority>{alts}</url>")
    out.append("</urlset>\n")
    (DIST / "sitemap.xml").write_text("".join(out), encoding="utf-8")
    llms = DIST / "llms.txt"
    if llms.exists():
        extra = "\n## Other languages\n" + "".join(
            f"- [{NATIVE[l]}]({C.SITE_URL}/{l}/): the full site in {NATIVE[l]}\n" for l in LANGS)
        llms.write_text(llms.read_text(encoding="utf-8").rstrip() + "\n" + extra, encoding="utf-8")
    for lang, n in report.items():
        print(f"{lang}: {n} segments untranslated (shown in English)")

if __name__ == "__main__":
    {"extract": extract, "merge": merge, "apply": apply}[sys.argv[1]]()
