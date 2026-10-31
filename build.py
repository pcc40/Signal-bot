#!/usr/bin/env python3
"""Static site builder for Eastbridge Strategic Partners.

python3 build.py            -> writes the full site to dist/
Content lives in src/content/ (Python data + Markdown insights in src/content/insights/).
"""
import json, os, re, shutil, sys, html, datetime, hashlib
from pathlib import Path
from email.utils import format_datetime

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
import config as C
import markdown, yaml

DIST = ROOT / "dist"
TODAY = datetime.date.today().isoformat()
MANIFEST = json.loads((ROOT / "src/img_manifest.json").read_text())
CSS_HASH = hashlib.md5((ROOT / "src/static/assets/site.css").read_bytes()).hexdigest()[:8]

esc = html.escape

def url(path):
    return C.SITE_URL + path

# ---------------------------------------------------------------- images
def img_meta(base):
    slug = base.rsplit("-", 1)[0]
    for m in MANIFEST.get(slug, []):
        if m["base"] == base:
            return m
    raise KeyError(base)

def picture(base, alt, sizes="100vw", eager=False, cls=""):
    m = img_meta(base)
    widths = [w for w in (640, 1280, 1600, 2000) if (ROOT / f"src/static/assets/img/{base}-{w}.webp").exists()]
    srcset = ", ".join(f"/assets/img/{base}-{w}.webp {min(w, m['w'])}w" for w in widths)
    mid = widths[1] if len(widths) > 1 else widths[0]
    h = round(m["h"] * 1280 / m["w"])
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{base}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="1280" height="{h}" alt="{esc(alt)}" {load} decoding="async">')

def og_image(base):
    return f"/assets/img/{base}-1280.webp"

# ---------------------------------------------------------------- schema
ORG_ID = C.SITE_URL + "/#org"
PERSON_ID = C.SITE_URL + "/about/#founder"

def person_schema():
    return {"@context": "https://schema.org", "@type": "Person", "@id": PERSON_ID, "name": C.FOUNDER["name"],
            "jobTitle": C.FOUNDER["role"], "worksFor": {"@id": ORG_ID}, "nationality": "British",
            "image": url("/assets/img/philip-chapman-01-1280.webp"),
            "url": url("/about/#founder"),
            "alumniOf": {"@type": "Organization", "name": C.FOUNDER["company_uk"], "url": C.FOUNDER["company_uk_url"]},
            "knowsAbout": ["Residential construction", "Owner's representation", "Construction project management",
                           "JCT contracts", "Extension of time claims", "Construction cost management", "Villa construction"]}

def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["ProfessionalService", "Organization"],
        "@id": ORG_ID,
        "name": C.NAME,
        "alternateName": C.SHORT,
        "legalName": C.LEGAL,
        "url": C.SITE_URL + "/",
        "logo": url("/assets/logo.png"),
        "image": url(og_image("quay-house-01")),
        "description": ("Independent, client-side owner's representative and villa project management for private "
                        "clients building or renovating homes in Dubai and Abu Dhabi. No contractor commissions."),
        "email": C.EMAIL,
        "telephone": C.PHONE_E164,
        "address": {"@type": "PostalAddress", "streetAddress": C.ADDRESS["street"],
                    "addressLocality": C.ADDRESS["locality"], "addressCountry": C.ADDRESS["country"]},
        "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "City", "name": "Abu Dhabi"},
                       {"@type": "Country", "name": "United Arab Emirates"}],
        "knowsAbout": ["Owner's representation", "Construction project management", "Villa construction",
                       "Villa renovation", "Construction cost management", "Contractor tendering",
                       "Extension of time claims", "Construction contract administration", "Snagging and handover",
                       "Dubai Municipality building permits", "Master developer NOC approvals"],
        "openingHours": "Su-Th 09:00-18:00",
        "sameAs": C.SOCIAL,
        "slogan": "Your villa, managed from your side of the table.",
        "founder": {"@id": PERSON_ID},
    }

def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": C.SITE_URL + "/#website",
            "url": C.SITE_URL + "/", "name": C.NAME, "publisher": {"@id": ORG_ID}, "inLanguage": "en"}

def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)}
                                for i, (n, p) in enumerate(crumbs)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                           for q, a in faqs]}

def service_schema(s, path):
    return {"@context": "https://schema.org", "@type": "Service", "@id": url(path) + "#service",
            "name": s["name"], "serviceType": s["name"], "description": s["description"],
            "provider": {"@id": ORG_ID}, "url": url(path),
            "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "City", "name": "Abu Dhabi"}]}

# ---------------------------------------------------------------- components
def crumbs_html(crumbs):
    if len(crumbs) < 2:
        return ""
    parts = []
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{p}">{esc(n)}</a><span aria-hidden="true">/</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'

def faq_html(faqs):
    items = "".join(f"<details><summary>{esc(q)}</summary><div class=\"ans\">{a}</div></details>" for q, a in faqs)
    return f'<div class="faq">{items}</div>'

def wa_link(text="Hello, I'd like to talk about a villa project."):
    from urllib.parse import quote
    return f"https://wa.me/{C.WHATSAPP}?text={quote(text)}"

CTA_IMAGES = ["sea-glass-house-01", "owers-house-04", "the-lookout-01", "quay-house-03", "saqqara-01", "menwinnion-04"]

def cta_band(title="Tell us about the house you want to build.", text=None, image=None):
    text = text or (f"{C.RESPONSE_PROMISE}. The first conversation is free, and nothing you send us is shared.")
    image = image or CTA_IMAGES[len(PAGES) % len(CTA_IMAGES)]
    return f'''<section class="cta-band" aria-labelledby="cta-h">{picture(image, "", "100vw")}
<div class="wrap"><div><h2 id="cta-h">{esc(title)}</h2><p style="margin-top:1em;max-width:46ch">{esc(text)}</p></div>
<div class="actions"><a class="btn" href="/contact/">Start a private brief</a><a class="btn btn--ghost" href="{wa_link()}" rel="noopener">WhatsApp us</a></div></div></section>'''

def banner(crumbs, h1, lede=None, image="quay-house-01", credit=None, extra=""):
    l = f'<p class="lede">{lede}</p>' if lede else ""
    c = f'<span class="credit">{esc(credit)}</span>' if credit else ""
    return (f'<section class="banner">{picture(image, "", "100vw", eager=True)}'
            f'<div class="wrap">{crumbs_html(crumbs)}<h1>{h1}</h1>{l}{extra}</div>{c}</section>')

def video_html(provider, vid, poster_base, title):
    src = (f"https://player.vimeo.com/video/{vid}?autoplay=1&dnt=1" if provider == "vimeo"
           else f"https://www.youtube-nocookie.com/embed/{vid}?autoplay=1&rel=0")
    return f'''<div class="video" data-src="{src}" data-title="{esc(title)}">{picture(poster_base, title + " — film still", "(max-width:900px) 100vw, 1100px")}
<button type="button" aria-label="Play the film: {esc(title)}"><span>Play the film</span></button></div>'''

def hero_video_html():
    """Optional background film for the home hero (config.HERO_VIDEO). The poster slideshow is
    always the default; the script only fades the film in once Vimeo reports it is playing."""
    if not C.HERO_VIDEO:
        return ""
    src = (f"https://player.vimeo.com/video/{C.HERO_VIDEO_VIMEO_ID}"
           "?background=1&amp;autoplay=1&amp;loop=1&amp;muted=1&amp;dnt=1")
    return f'<div class="hero-video" data-src="{src}" data-title="Drone film of Quay House" aria-hidden="true"></div>'

def steps_html(items, cls="steps"):
    return f'<ol class="{cls}">' + "".join(f"<li><h3>{esc(t)}</h3><p>{d}</p></li>" for t, d in items) + "</ol>"

def start_steps():
    """The three steps from first contact to appointment. Fee figures appear only when PUBLISH_FEES is on."""
    fee = (f" A plot and pre-purchase review is {esc(C.FEES['plot_review'])}." if C.PUBLISH_FEES else "")
    return [
        ("A free 30-minute call", "Tell us about the plot, the villa or the project you are already in. We ask the questions a builder would ask, and tell you plainly whether you need us."),
        ("A fixed-fee first review", "A plot review, a health check on a project under way, or the brief and budget: scoped and priced in writing before we start." + fee),
        ("Your appointment", "If you want us to carry on, a written appointment for the stages you need, from design to handover, with the fee agreed up front. Nothing is assumed."),
    ]

def how_it_starts():
    return (f'<section class="section--tight starts" aria-labelledby="starts-h"><div class="wrap">'
            f'<div class="head-row"><div><span class="kicker">How it starts</span><h2 id="starts-h">Three steps from first call to appointment</h2></div>'
            f'<p class="muted">The call is free. After that, you decide at each step whether to go on. <a class="link" href="/fees/">How fees work</a></p></div>'
            f'{steps_html(start_steps())}'
            f'<p class="starts-cta"><a class="btn" href="/contact/">Book the free call</a>'
            f'<a class="btn btn--ghost" href="{wa_link()}" rel="noopener">Or message us on WhatsApp</a></p>'
            f'</div></section>')

WA_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false">'
           '<path d="M20 11.6a8.2 8.2 0 0 1-12.2 7.2L4 20l1.3-3.7A8.2 8.2 0 1 1 20 11.6Z"/></svg>')
CALL_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true" focusable="false">'
             '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>')
BRIEF_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true" focusable="false">'
              '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8ZM14 3v5h5M8.5 13h7M8.5 17h5"/></svg>')

def action_bar():
    """Floating WhatsApp button on larger screens; on phones it becomes one bar of three actions."""
    return (f'<nav class="action-bar" aria-label="Contact Eastbridge">'
            f'<a class="ab-wa" href="{wa_link()}" rel="noopener">{WA_ICON}<span>WhatsApp</span></a>'
            f'<a class="ab-call" href="tel:{C.PHONE_E164}">{CALL_ICON}<span>Call</span></a>'
            f'<a class="ab-brief" href="/contact/">{BRIEF_ICON}<span>Start a brief</span></a></nav>')

LOGO_MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
             '<rect x="0.75" y="0.75" width="38.5" height="38.5" fill="none" stroke="currentColor" stroke-width="1.5"/>'
             '<path d="M7 29 H33" stroke="currentColor" stroke-width="1.5"/>'
             '<path d="M10 29 V24 A10 10 0 0 1 30 24 V29" fill="none" stroke="currentColor" stroke-width="1.5"/>'
             '<path d="M20 14 V29" stroke="#C9A961" stroke-width="1.5"/></svg>')

def logo(cls=""):
    return (f'<a class="logo {cls}" href="/" aria-label="{C.NAME}, home">{LOGO_MARK}'
            f'<span class="wm"><b>Eastbridge</b><span>Strategic Partners</span></span></a>')

def header(path):
    from content.services import SERVICES, BY_SLUG as S
    cur = ' aria-current="page"'
    def a(n, p):
        return f'<li><a href="{p}"{cur if path.startswith(p) else ""}>{n}</a></li>'
    col1 = ["owners-representative", "villa-construction-project-management", "villa-renovation-project-management", "plot-due-diligence", "overseas-owners", "development-advisory"]
    col2 = ["design-and-approvals", "consultant-and-contractor-selection", "cost-and-programme-control", "site-visits-and-reporting", "variations-delays-and-claims", "stalled-project-rescue", "snagging-and-handover"]
    l1 = "".join(f'<li><a href="/services/{s}/">{esc(S[s]["short"])}</a></li>' for s in col1)
    l2 = "".join(f'<li><a href="/services/{s}/">{esc(S[s]["short"])}</a></li>' for s in col2)
    mega = (f'<div class="mega"><div><h4>For your project</h4><ul>{l1}</ul></div>'
            f'<div><h4>At every stage</h4><ul>{l2}</ul></div>'
            f'<a class="mega-feature" href="/case-studies/island-e-waterfront-villa/">{picture("saqqara-01", "", "240px")}'
            f'<span>Illustrative case study: an Island E waterfront villa, from plot to keys</span></a></div>')
    svc_cur = cur if path.startswith("/services/") else ""
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="utility"><div class="wrap"><span class="u-left">Client-side project management for private villas in Dubai and Abu Dhabi</span>
<span class="u-right"><a href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a><a href="{wa_link()}" rel="noopener">WhatsApp</a><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></span></div></div>
<header class="site-head"><div class="wrap">
{logo()}
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main"><button class="menu-close" type="button" aria-label="Close menu">Close</button><ul>
<li class="has-mega"><a href="/services/"{svc_cur}>Services</a>{mega}</li>
{a("Why client-side", "/why-a-client-side-project-manager/")}{a("Case study", "/case-studies/")}{a("Work", "/work/")}{a("Insights", "/insights/")}{a("About", "/about/")}
</ul><a class="btn" href="/contact/">Start a brief</a></nav>
</div></header>'''

def footer():
    from content.services import SERVICES
    from content.areas import AREAS
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["short"])}</a></li>' for s in SERVICES[:8])
    ar = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["name"])}</a></li>' for a in AREAS[:9])
    year = datetime.date.today().year
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-top"><h2>Planning a villa in Dubai or Abu Dhabi?</h2>
<div><p>Our occasional notes for villa owners: build costs, approvals and what is moving in the market. No more than once a month.</p>
<form class="newsletter" name="notes" method="POST" action="/contact/thanks/#notes" data-netlify="true" netlify-honeypot="company_site"><input type="hidden" name="form-name" value="notes"><p class="hp"><label>Leave empty <input name="company_site"></label></p><label class="sr" for="nl-email">Email address</label><input id="nl-email" name="email" type="email" placeholder="Your email address" required autocomplete="email"><button class="btn" type="submit">Subscribe</button></form></div></div>
<div class="foot-grid">
<div>{logo()}<p style="max-width:38ch">Client-side project management and owner's representation for private villas in Dubai and Abu Dhabi. Paid only by our clients.</p>
<p><a href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a><br><a href="mailto:{C.EMAIL}">{C.EMAIL}</a><br><a href="{wa_link()}" rel="noopener">WhatsApp</a></p>
<p>{esc(C.ADDRESS["street"])}<br>{esc(C.ADDRESS["locality"])}, {esc(C.ADDRESS["country_name"])}</p></div>
<div><h3>Services</h3><ul>{svc}<li><a href="/services/">All services</a></li></ul></div>
<div><h3>Where we work</h3><ul>{ar}<li><a href="/areas/">All areas</a></li></ul></div>
<div><h3>Firm</h3><ul><li><a href="/why-a-client-side-project-manager/">Why client-side</a></li><li><a href="/case-studies/">Case study</a></li><li><a href="/work/">Work</a></li><li><a href="/about/">About</a></li><li><a href="/approach/">How we work</a></li><li><a href="/independence/">Independence pledge</a></li><li><a href="/fees/">How fees work</a></li><li><a href="/insights/">Insights</a></li><li><a href="/faq/">Questions</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div>
<div class="legal"><span>© {year} {C.LEGAL}. {C.LICENCE}. Eastbridge acts as the client's project manager and representative. It is not a contractor and does not replace the registered consultant of record required by the authorities.</span>
<span><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/sitemap.xml">Sitemap</a></span></div>
</div></footer>
{action_bar()}'''

SCRIPT = """<script>
(function(){document.documentElement.classList.add('js');
var b=document.querySelector('.menu-toggle'),n=document.getElementById('nav'),x=document.querySelector('.menu-close');
function setNav(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);document.body.classList.toggle('nav-open',o)}
if(b&&n){b.addEventListener('click',function(){setNav(!n.classList.contains('open'))});if(x)x.addEventListener('click',function(){setNav(false)})}
document.querySelectorAll('.has-mega > a').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth<=1100){e.preventDefault();a.parentNode.classList.toggle('open')}})});
var h=document.querySelector('.site-head');if(document.body.classList.contains('has-hero')&&h){var f=function(){h.classList.toggle('stuck',window.scrollY>140)};f();window.addEventListener('scroll',f,{passive:true})}
document.querySelectorAll('.video button').forEach(function(btn){btn.addEventListener('click',function(){var v=btn.parentNode,fr=document.createElement('iframe');fr.src=v.dataset.src;fr.title=v.dataset.title;fr.allow='autoplay; fullscreen; picture-in-picture';fr.allowFullscreen=true;v.innerHTML='';v.appendChild(fr)})});
var hv=document.querySelector('.hero-video'),mm=function(q){return window.matchMedia&&window.matchMedia(q).matches};
if(hv&&mm('(min-width:900px)')&&!mm('(prefers-reduced-motion: reduce)')&&!(navigator.connection&&navigator.connection.saveData)){
 window.addEventListener('load',function(){setTimeout(function(){
  var fr=document.createElement('iframe'),done=false,VO='https://player.vimeo.com',t;
  function stop(){if(done)return;done=true;clearTimeout(t);window.removeEventListener('message',on);if(hv.parentNode)hv.parentNode.removeChild(hv)}
  function on(e){if(e.origin!==VO||e.source!==fr.contentWindow)return;var d=e.data;if(typeof d==='string'){try{d=JSON.parse(d)}catch(x){return}}if(!d)return;
   if(d.event==='ready'){['play','playProgress','timeupdate','error'].forEach(function(v){fr.contentWindow.postMessage(JSON.stringify({method:'addEventListener',value:v}),VO)})}
   else if(d.event==='error'){stop()}
   else if(!done&&(d.event==='play'||d.event==='playProgress'||d.event==='timeupdate')){done=true;clearTimeout(t);hv.classList.add('on')}}
  window.addEventListener('message',on);t=setTimeout(stop,9000);
  fr.src=hv.dataset.src;fr.title=hv.dataset.title||'';fr.allow='autoplay; fullscreen';fr.setAttribute('tabindex','-1');fr.setAttribute('aria-hidden','true');hv.appendChild(fr)},1200)})}
else if(hv&&hv.parentNode){hv.parentNode.removeChild(hv)}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
 document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)})}else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')})}
if(location.hash==='#notes'){document.querySelectorAll('[data-thanks]').forEach(function(el){el.hidden=el.getAttribute('data-thanks')!=='notes'})}
var fm=document.querySelector('form[data-enquiry]');
if(fm){fm.setAttribute('novalidate','');
 var ph=fm.querySelector('#f-phone'),phr=fm.querySelector('.ph-req'),pho=fm.querySelector('.ph-opt');
 var mark=function(el,ok){var w=el.closest('.field');if(!w)return;w.classList.toggle('invalid',!ok);if(ok)el.removeAttribute('aria-invalid');else el.setAttribute('aria-invalid','true');var m=w.querySelector('.err');if(m)m.hidden=ok};
 var check=function(el){var ok=el.checkValidity()&&!(el.required&&!el.value.trim());mark(el,ok);return ok};
 var need=function(){var m=fm.querySelector('input[name="contact_method"]:checked'),r=!!(m&&m.value!=='Email');if(ph){ph.required=r;if(phr)phr.hidden=!r;if(pho)pho.hidden=r;if(!r)mark(ph,true)}};
 var fields=fm.querySelectorAll('input:not([type=hidden]):not([type=radio]):not([name=company_site]),select,textarea');
 fields.forEach(function(el){el.addEventListener('blur',function(){if(el.value||el.dataset.touched)check(el);el.dataset.touched=1});el.addEventListener('input',function(){if(el.getAttribute('aria-invalid'))check(el)})});
 fm.querySelectorAll('input[name="contact_method"]').forEach(function(r){r.addEventListener('change',need)});need();
 fm.addEventListener('submit',function(e){var bad=null;fields.forEach(function(el){if(!check(el)&&!bad)bad=el});
  if(bad){e.preventDefault();bad.focus();return}
  var sb=fm.querySelector('button[type=submit]');if(sb){sb.setAttribute('aria-disabled','true');sb.classList.add('is-sending')}
  if(window.gtag)gtag('event','generate_lead',{form:'brief'})})}
document.querySelectorAll('a[href^="https://wa.me"]').forEach(function(a){a.addEventListener('click',function(){if(window.gtag)gtag('event','contact',{method:'whatsapp'})})});
})();
</script>"""

def analytics():
    if not C.GA4_ID:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={C.GA4_ID}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{C.GA4_ID}',{{anonymize_ip:true}});</script>")

def page(path, title, description, body, crumbs=None, schema=None, og=None, og_type="website",
         preload=None, noindex=False, hero=False):
    crumbs = crumbs or [("Home", "/")]
    schema = list(schema or [])
    if path == "/":
        schema = [org_schema(), website_schema()] + schema
    else:
        schema = [crumbs_schema(crumbs)] + schema
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    og_img = url(og or og_image("quay-house-01"))
    robots = "noindex,nofollow" if (noindex or not C.INDEXABLE) else "index,follow,max-image-preview:large,max-snippet:-1"
    verif = ""
    if C.GSC_VERIFICATION:
        verif += f'<meta name="google-site-verification" content="{C.GSC_VERIFICATION}">'
    if C.BING_VERIFICATION:
        verif += f'<meta name="msvalidate.01" content="{C.BING_VERIFICATION}">'
    hero = hero or body.lstrip().startswith(('<section class="banner"', '<section class="hero"', '<article><section class="banner"'))
    body_cls = ' class="has-hero"' if hero else ""
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    doc = f'''<!doctype html>
<html lang="en-GB" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url(path)}">
<link rel="alternate" hreflang="en" href="{url(path)}">
<link rel="alternate" hreflang="x-default" href="{url(path)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{C.NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F2629">
{verif}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Eastbridge Insights" href="/insights/feed.xml">
<link rel="preload" href="/assets/fonts/iserif-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/instrument-400.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<link rel="stylesheet" href="/assets/site.css?v={CSS_HASH}">
{ld}
{analytics()}
</head>
<body{body_cls}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
{SCRIPT}
</body>
</html>'''
    out = DIST / path.lstrip("/") / "index.html" if path.endswith("/") else DIST / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    if not noindex:
        PAGES.append(path)

PAGES = []

def page_head(crumbs, h1, lede=None, extra=""):
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'<section class="page-head"><div class="wrap">{crumbs_html(crumbs)}<h1>{h1}</h1>{l}{extra}</div></section>'

# ---------------------------------------------------------------- build
def copy_static():
    src = ROOT / "src/static"
    for p in src.rglob("*"):
        if p.is_file():
            d = DIST / p.relative_to(src)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, d)

def load_insights():
    posts = []
    for f in sorted((ROOT / "src/content/insights").glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm)
        if meta.get("draft"):
            continue
        meta["slug"] = meta.get("slug") or f.stem
        meta["html"] = markdown.markdown(body, extensions=["tables", "toc", "attr_list", "sane_lists"])
        meta["words"] = len(re.findall(r"\w+", body))
        posts.append(meta)
    posts.sort(key=lambda p: str(p["date"]), reverse=True)
    return posts

def write_sitemap():
    items = []
    for p in sorted(set(PAGES)):
        pri = "1.0" if p == "/" else ("0.9" if p.count("/") == 3 and p.startswith("/services/") else "0.7")
        items.append(f"<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority></url>")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(items) + "</urlset>\n", encoding="utf-8")

def write_robots():
    if not C.INDEXABLE:
        txt = "User-agent: *\nDisallow: /\n"
    else:
        txt = ("# Search engines and AI assistants are welcome to read and cite this site.\n"
               "User-agent: *\nAllow: /\n\n"
               "User-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\n"
               "User-agent: ClaudeBot\nAllow: /\n\nUser-agent: Claude-SearchBot\nAllow: /\n\nUser-agent: Claude-User\nAllow: /\n\n"
               "User-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nUser-agent: Applebot-Extended\nAllow: /\n\n"
               f"Sitemap: {url('/sitemap.xml')}\n")
    (DIST / "robots.txt").write_text(txt)

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    copy_static()
    import pages
    posts = load_insights()
    pages.build_all(posts)
    write_sitemap()
    write_robots()
    print(f"Built {len(set(PAGES))} pages, {len(posts)} insights -> {DIST}")

if __name__ == "__main__":
    import build
    build.main()
