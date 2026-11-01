"""Page builders. Every page is written through build.page()."""
import json, datetime, re, html as H
from email.utils import format_datetime
import build as B
import config as C
from content.services import SERVICES, BY_SLUG as SVC
from content.areas import AREAS, BY_SLUG as AREA
from content.projects import PROJECTS, BY_SLUG as PROJ

esc = H.escape
pic = B.picture

# ---------------------------------------------------------------- helpers
def service_rows(items):
    return '<div class="service-list">' + "".join(
        f'<a class="service-row" href="/services/{s["slug"]}/"><h3>{esc(s["short"])}</h3>'
        f'<p>{esc(s["lede"])}</p><span class="go">Read more</span></a>' for s in items) + "</div>"

def work_cards(projects, first_wide=True):
    pattern = ["wide", "", "", "wide", "half", "half"]
    out = []
    for i, p in enumerate(projects):
        cls = pattern[i % len(pattern)]
        sizes = "(max-width:880px) 100vw, 66vw" if cls == "wide" else "(max-width:880px) 100vw, 50vw" if cls == "half" else "(max-width:880px) 100vw, 33vw"
        out.append(f'<a class="work-card {cls}" href="/work/{p["slug"]}/"><figure>{pic(p["slug"] + "-01", p["name"] + ", " + p["place"] + " — " + p["summary"], sizes)}</figure>'
                   f'<h3>{esc(p["name"])}</h3><p>{esc(p["type"])}, {esc(p["place"])}</p></a>')
    return '<div class="work-grid">' + "".join(out) + "</div>"

STAGES = [
 ("Brief and budget", "What you want, what it should cost, and whether the plot allows it."),
 ("Team", "Choosing and appointing the consultant, and later the contractor, on fair terms."),
 ("Design and approvals", "Design reviewed against cost at every stage; approvals tracked."),
 ("Contract", "Bids compared like-for-like and a contract that leaves little to argue about."),
 ("Construction", "Site visits, reporting, payment review and variation control."),
 ("Handover", "Snagging, commissioning, documents and the defects period."),
]

def stages_html(light=False):
    lis = "".join(f"<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in STAGES)
    return f'<ol class="stages{" stages--light" if light else ""}">{lis}</ol>'

# ---------------------------------------------------------------- home
SVC_IMG = {
 "owners-representative": ("quay-house-01", ["quay-house-03", "quay-house-05", "quay-house-12"], "quay-house"),
 "villa-construction-project-management": ("sea-glass-house-02", ["sea-glass-house-03", "sea-glass-house-04", "sea-glass-house-06"], "sea-glass-house"),
 "villa-renovation-project-management": ("menwinnion-01", ["menwinnion-03", "menwinnion-07", "polgreen-manor-04"], "menwinnion"),
 "plot-due-diligence": ("saqqara-01", ["saqqara-02", "saqqara-04", "saqqara-09"], "saqqara"),
 "design-and-approvals": ("owers-house-01", ["owers-house-07", "owers-house-05", "the-lookout-04"], "owers-house"),
 "consultant-and-contractor-selection": ("gooden-heane-01", ["gooden-heane-02", "gooden-heane-03", "gooden-heane-05"], "gooden-heane"),
 "cost-and-programme-control": ("polgreen-manor-01", ["polgreen-manor-05", "polgreen-manor-04", "polgreen-manor-03"], "polgreen-manor"),
 "site-visits-and-reporting": ("the-lookout-02", ["the-lookout-03", "the-lookout-11", "the-lookout-07"], "the-lookout"),
 "variations-delays-and-claims": ("trelowen-01", ["trelowen-02", "trelowen-07", "trelowen-04"], "trelowen"),
 "stalled-project-rescue": ("esplanade-road-01", ["esplanade-road-06", "esplanade-road-02", "esplanade-road-04"], "esplanade-road"),
 "snagging-and-handover": ("ansells-01", ["ansells-02", "ansells-08", "ansells-03"], "ansells"),
 "overseas-owners": ("blue-seas-02", ["blue-seas-01", "blue-seas-03", "blue-seas-11"], "blue-seas"),
 "development-advisory": ("three-mile-beach-01", ["three-mile-beach-02", "three-mile-beach-03", "three-mile-beach-10"], "three-mile-beach"),
}
AREA_IMG = {"palm-jumeirah": "quay-house-09", "emirates-hills": "owers-house-02", "jumeirah-bay": "saqqara-05",
            "district-one": "sea-glass-house-05", "dubai-hills-estate": "gooden-heane-07", "al-barari": "quay-house-14",
            "dubai-islands": "saqqara-03", "palm-jebel-ali": "the-lookout-06", "saadiyat": "gooden-heane-08", "hudayriyat": "ansells-06"}
POST_IMG = {"villa-construction-cost-dubai": "sea-glass-house-05", "how-to-build-a-villa-in-dubai": "saqqara-07",
            "owners-representative-vs-project-manager-vs-consultant": "owers-house-08", "what-the-contractor-knows": "quay-house-02",
            "palm-jumeirah-villa-renovation": "menwinnion-11", "how-to-choose-a-villa-contractor-dubai": "gooden-heane-04",
            "villa-construction-contracts-uae": "polgreen-manor-02", "building-a-villa-in-dubai-from-the-uk": "blue-seas-01",
            "villa-snagging-checklist-dubai": "the-lookout-11", "buying-a-villa-plot-in-dubai-checks": "saqqara-09"}

def proj_of(base):
    return PROJ[base.rsplit("-", 1)[0]]

def credit_of(base):
    p = proj_of(base)
    return f'{p["name"]}, {p["place"]}' + (f' · photograph {p["photo"]}' if p["photo"] else "")

def svc_img_for(p):
    alts = ["sea-glass-house-01", "owers-house-02", "the-lookout-03", "saqqara-05", "gooden-heane-03", "quay-house-05"]
    return alts[sum(map(ord, p["slug"])) % len(alts)]

def post_img(p):
    if p.get("hero"):
        return p["hero"]
    if p["slug"] in POST_IMG:
        return POST_IMG[p["slug"]]
    pool = [m["base"] for v in B.MANIFEST.values() for m in v[:4]]
    return pool[sum(map(ord, p["slug"])) % len(pool)]

def svc_cards(items):
    return '<div class="svc-grid">' + "".join(
        f'<a class="svc-card" href="/services/{s["slug"]}/"><figure>{pic(SVC_IMG[s["slug"]][0], "", "(max-width:600px) 100vw, (max-width:980px) 50vw, 33vw")}</figure>'
        f'<h3>{esc(s["short"])}</h3><p>{esc(s["lede"])}</p></a>' for s in items) + "</div>"

service_rows = svc_cards

def post_cards(posts):
    return '<div class="post-cards">' + "".join(
        f'<a class="post-card" href="/insights/{p["slug"]}/"><figure>{pic(post_img(p), "", "(max-width:600px) 100vw, (max-width:980px) 50vw, 33vw")}</figure>'
        f'<div class="meta">{esc(p.get("category",""))}</div><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p></a>' for p in posts) + "</div>"

def strip_html(bases):
    figs = []
    for i, b in enumerate(bases):
        p = proj_of(b)
        sizes = "(max-width:760px) 100vw, 50vw" if i == 0 else "(max-width:760px) 50vw, 25vw"
        figs.append(f'<figure><a href="/work/{p["slug"]}/">{pic(b, p["name"] + ", " + p["place"], sizes)}</a><figcaption>{esc(p["name"])}, {esc(p["place"])}</figcaption></figure>')
    return '<div class="strip">' + "".join(figs) + "</div>"

HERO_SLIDES = ["sea-glass-house-01", "owers-house-01", "saqqara-01", "quay-house-01", "the-lookout-02"]

def home(posts):
    import pages_new
    pages_new.home(posts, post_cards, stages_html, SVC_IMG)

# ---------------------------------------------------------------- services
def services_hub():
    crumbs = [("Home", "/"), ("Services", "/services/")]
    body = B.banner(crumbs, "Services for villa owners", "Client-side project management from the first budget to the end of the defects period, or just the part you need.", "sea-glass-house-01", credit_of("sea-glass-house-01")) + f'''
<section class="section"><div class="wrap">{svc_cards(SERVICES)}</div></section>
<section class="section paper"><div class="wrap split"><div><h2>What we don't do</h2></div><div class="prose">
<p>We are not a contractor and we hold no construction contracts. We are not an engineering consultancy: the statutory design, permit submissions and supervision of your villa are carried out by the registered consultant you appoint, and we represent you alongside them. We are not lawyers; where legal advice is needed, we work with your UAE-qualified lawyer. And we are not estate agents.</p>
<p>Keeping these lines clear is what lets us act for you alone.</p></div></div></section>
{B.cta_band()}'''
    schema = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": B.url(f"/services/{s['slug']}/"), "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    B.page("/services/", "Villa Project Management Services Dubai | Eastbridge",
           "Owner's representation, villa builds, renovations, plot reviews, cost control, site reports, claims, snagging and handover in Dubai and Abu Dhabi.",
           body, crumbs, schema)

def service_page(s):
    path = f"/services/{s['slug']}/"
    crumbs = [("Home", "/"), ("Services", "/services/"), (s["short"], path)]
    does = "".join(f"<li>{esc(d)}</li>" for d in s["does"])
    gets = "".join(f"<li>{esc(g)}</li>" for g in s["gets"])
    related = service_rows([SVC[r] for r in s["related"]])
    areas = [a for a in AREAS if s["slug"] in a["services"]][:6]
    area_links = ", ".join(f'<a href="/areas/{a["slug"]}/">{esc(a["name"])}</a>' for a in areas)
    area_p = f'<p class="muted small">Often needed in {area_links}.</p>' if areas else ""
    ban, strip, pslug = SVC_IMG[s["slug"]]
    pj = PROJ[pslug]
    body = B.banner(crumbs, esc(s["h1"]), esc(s["lede"]), ban, credit_of(ban)) + f'''
<section class="section"><div class="wrap split">
<div class="side-sticky"><dl class="facts"><div><dt>Stage</dt><dd>{esc(s["stage"])}</dd></div><div><dt>Who it's for</dt><dd>Private villa owners and investors</dd></div><div><dt>Where</dt><dd>Dubai and Abu Dhabi</dd></div></dl>{area_p}
<figure>{pic(strip[0], proj_of(strip[0])["name"], "(max-width:900px) 100vw, 40vw")}<figcaption>{esc(credit_of(strip[0]))}</figcaption></figure></div>
<div class="prose">{s["intro"]}
<h2>What we do</h2><ul>{does}</ul>
<h2>What you receive</h2><ul>{gets}</ul></div>
</div></section>
<section class="section--tight"><div class="wrap">{strip_html([ban] + strip[1:])}</div></section>
<section class="section dark"><div class="wrap feature">
<figure>{pic(pj["slug"] + "-01", pj["name"] + ", " + pj["place"], "(max-width:900px) 100vw, 58vw")}<figcaption>{esc(pj["name"])}, {esc(pj["place"])}. Built by P Chapman Construction.</figcaption></figure>
<div><span class="kicker">From the builder's side</span><p class="statement" style="font-size:var(--s-2)">{esc(s["builder_view"])}</p><p><a class="btn btn--ghost" href="/work/{pj["slug"]}/">See {esc(pj["name"])}</a></p></div></div></section>
<section class="section"><div class="wrap split"><div><h2>Questions</h2></div><div>{B.faq_html(s["faqs"])}</div></div></section>
<section class="section paper"><div class="wrap"><h2>Related services</h2>{related}</div></section>
{B.cta_band()}'''
    B.page(path, s["title"], s["description"], body, crumbs,
           [B.service_schema(s, path), B.faq_schema(s["faqs"])], og=B.og_image(ban))

# ---------------------------------------------------------------- areas
def areas_hub():
    crumbs = [("Home", "/"), ("Areas", "/areas/")]
    dubai = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["name"])}</a><span>{esc(a["tag"])} · {esc(a["developer"])}</span></li>' for a in AREAS if a["city"] == "Dubai")
    ad = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["name"])}</a><span>{esc(a["tag"])} · {esc(a["developer"])}</span></li>' for a in AREAS if a["city"] == "Abu Dhabi")
    body = B.banner(crumbs, "Where we work", "Every villa community has its own master developer, design guidelines and practical constraints. Here is what to expect in each.", "menwinnion-05", credit_of("menwinnion-05")) + f'''
<section class="section--tight"><div class="wrap"><h2>Dubai</h2><ul class="area-list">{dubai}</ul></div></section>
<section class="section--tight"><div class="wrap"><h2>Abu Dhabi</h2><ul class="area-list">{ad}</ul></div></section>
<section class="section paper"><div class="wrap split"><div><h2>Not listed?</h2></div><div class="prose"><p>We represent owners across Dubai and Abu Dhabi, including Jumeirah Islands, Jumeirah Golf Estates, Tilal Al Ghaf, Al Wasl, Umm Suqeim and Jumeirah, and Abu Dhabi's island communities. The approach is the same: understand the master developer's rules, set a realistic budget and programme, and represent you from brief to handover.</p><p><a href="/contact/">Tell us where your plot or villa is</a>.</p></div></div></section>
{B.cta_band()}'''
    B.page("/areas/", "Villa Communities We Work In: Dubai & Abu Dhabi | Eastbridge",
           "Villa build and renovation representation on Palm Jumeirah, Emirates Hills, Jumeirah Bay, District One, Dubai Hills, Al Barari, Saadiyat and more.",
           body, crumbs)

def area_page(a):
    path = f"/areas/{a['slug']}/"
    crumbs = [("Home", "/"), ("Areas", "/areas/"), (a["name"], path)]
    svc = service_rows([SVC[s] for s in a["services"]])
    img = AREA_IMG.get(a["slug"], a["image"])
    pj = proj_of(img)
    others = [m["base"] for m in B.MANIFEST[pj["slug"]] if m["base"] != img][1:4]
    body = B.banner(crumbs, esc(a["h1"]), esc(a["lede"]), img, credit_of(img)) + f'''
<section class="section"><div class="wrap split">
<div><dl class="facts"><div><dt>City</dt><dd>{esc(a["city"])}</dd></div><div><dt>Master developer</dt><dd>{esc(a["developer"])}</dd></div><div><dt>Typical work</dt><dd>{esc(a["tag"])}</dd></div></dl></div>
<div class="prose">{a["body"]}</div></div></section>
<section class="section--tight"><div class="wrap">{strip_html(others)}</div></section>
<section class="section paper"><div class="wrap split"><div><h2>Questions about {esc(a["name"])}</h2></div><div>{B.faq_html(a["faqs"])}</div></div></section>
<section class="section"><div class="wrap"><h2>Services most relevant here</h2>{svc}</div></section>
{B.cta_band(f"Building or renovating in {a['name']}?")}'''
    schema = [B.faq_schema(a["faqs"]), {"@context": "https://schema.org", "@type": "Service",
              "name": f"Villa project management and owner's representation in {a['name']}",
              "provider": {"@id": B.ORG_ID}, "areaServed": {"@type": "Place", "name": f"{a['name']}, {a['city']}"},
              "url": B.url(path)}]
    B.page(path, a["title"], a["description"], body, crumbs, schema, og=B.og_image(img))

# ---------------------------------------------------------------- work
def work_hub():
    crumbs = [("Home", "/"), ("Work", "/work/")]
    from content.projects import RECOGNITION, TESTIMONIALS, recognition_html
    import pages_new
    rec = recognition_html(RECOGNITION[:4])
    body = B.banner(crumbs, "Homes built by P Chapman Construction", "Selected work of P Chapman Construction, the company Philip Chapman founded and led for 21 years: private houses, country estates, developments and hotel work.", "owers-house-02", credit_of("owers-house-02")) + f'''
<section class="section--tight"><div class="wrap"><div class="kpis kpis--text">{rec}</div><p class="small muted" style="margin-top:14px">Awards were made to the houses and the teams that designed and built them. Project teams are credited on each project page.</p></div></section>
<section class="section--tight"><div class="wrap">{work_cards(PROJECTS)}</div></section>
<section class="section band-dark"><div class="wrap"><div class="head-row"><h2>What P Chapman Construction's clients said</h2><p class="muted">Owners and developers on P Chapman Construction's work.</p></div>{pages_new.quotes_html(TESTIMONIALS[3:6])}</div></section>
<section class="section"><div class="wrap split"><div><h2>Range of work</h2></div><div><p class="muted" style="margin-top:24px">P Chapman Construction worked under traditional and design-and-build contracts, for private owners, developers, hoteliers, schools and housing associations, with particular expertise in contemporary coastal houses and eco-buildings.</p></div></div></section>
{B.cta_band("Bring this standard to your villa.")}'''
    B.page("/work/", "Work: Homes Built by P Chapman Construction",
           "Private houses, estates, developments and hotel work, some award-winning, built by P Chapman Construction, the company Philip Chapman led for 21 years.",
           body, crumbs, og=B.og_image("owers-house-02"))

def project_case_html(p):
    """A real UK project written up as a case study: brief, role, constraints, work delivered, documented outcome."""
    c = p.get("case")
    if not c:
        return ""
    li = lambda xs: "".join(f"<li>{esc(x)}</li>" for x in xs)
    src_t, src_u = c["source"]
    return f'''<section class="section stone" id="case-study" aria-labelledby="case-study-h"><div class="wrap">
<div class="head-row"><div><span class="kicker">UK project case study</span><h2 id="case-study-h">{esc(p["name"])}: the project in detail</h2></div>
<p class="muted">UK contracting work by P Chapman Construction as main contractor. It is not an Eastbridge appointment or a UAE project.</p></div>
<div class="split"><div class="prose">
<h3>The brief</h3><p>{esc(c["brief"])}</p>
<h3>P Chapman Construction's role</h3><p>{esc(c["role"])}</p>
<h3>Constraints</h3><ul>{li(c["constraints"])}</ul></div>
<div class="prose">
<h3>The work delivered</h3><ul>{li(c["delivered"])}</ul>
<h3>Documented outcome</h3><ul>{li(c["outcome"])}</ul>
<p class="small muted">These awards recognise the house and its project team. They are not personal awards to Philip Chapman or awards to Eastbridge. Photography: {esc(p["photo"])}. Source: <a href="{src_u}" rel="noopener">{esc(src_t)}</a>.</p>
</div></div></div></section>'''

def project_page(p):
    path = f"/work/{p['slug']}/"
    crumbs = [("Home", "/"), ("Work", "/work/"), (p["name"], path)]
    imgs = B.MANIFEST[p["slug"]]
    credit = f"Photography © {p['photo']}" if p["photo"] else "P Chapman Construction"
    figs = []
    pattern = ["full", "", "", "third", "third", "third", "full", "", ""]
    for i, m in enumerate(imgs[1:], 1):
        cls = pattern[(i - 1) % len(pattern)]
        sizes = "(max-width:760px) 100vw, " + ("1360px" if cls == "full" else "33vw" if cls == "third" else "50vw")
        figs.append(f'<figure class="{cls}">{pic(m["base"], p["name"] + ", " + p["place"] + " — view " + str(i + 1), sizes)}</figure>')
    video = ""
    if p["video"]:
        video = f'<section class="section--tight"><div class="wrap"><h2 class="sr">Film</h2>{B.video_html(p["video"][0], p["video"][1], imgs[min(1,len(imgs)-1)]["base"], p["name"] + " film")}</div></section>'
    rec_dd = ""
    if p["recognition"]:
        rec_dd = '<div><dt>Recognition</dt><dd>' + "<br>".join(
            esc(r) + (f' <a href="{esc(u)}" rel="noopener" class="small">Source</a>' if u else "") for r, u in p["recognition"]) + "</dd></div>"
    idx = [x["slug"] for x in PROJECTS].index(p["slug"])
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    body = B.banner(crumbs, esc(p["name"]), esc(p["summary"]), imgs[0]["base"], credit) + f'''
<section class="section"><div class="wrap split">
<div><dl class="facts"><div><dt>Location</dt><dd>{esc(p["place"])}</dd></div><div><dt>Project</dt><dd>{esc(p["type"])}</dd></div><div><dt>Built by</dt><dd>P Chapman Construction</dd></div>{('<div><dt>Project team</dt><dd>' + esc(p["team"]) + '</dd></div>') if p["team"] else ""}{('<div><dt>Photography</dt><dd>' + esc(p["photo"]) + '</dd></div>') if p["photo"] else ""}{rec_dd}</dl><p class="small muted" style="margin-top:14px">Project details: <a href="{esc(p["source"])}" rel="noopener">P Chapman Construction project page</a></p></div>
<div class="prose">{p["text"]}<h2>Why it matters for a Dubai villa</h2><p>{esc(p["dubai"])}</p></div></div></section>
{project_case_html(p)}
{video}
<section class="section--tight"><div class="wrap"><div class="gallery">{"".join(figs)}</div><p class="small muted" style="margin-top:12px">{esc(credit)}</p></div></section>
<section class="section paper"><div class="wrap split"><div><p class="muted">Next project</p><h2><a href="/work/{nxt["slug"]}/" style="text-decoration:none">{esc(nxt["name"])}</a></h2><p class="muted">{esc(nxt["type"])}, {esc(nxt["place"])}</p></div>
<a href="/work/{nxt["slug"]}/" aria-hidden="true" tabindex="-1">{pic(nxt["slug"] + "-01", "", "(max-width:880px) 100vw, 58vw")}</a></div></section>
{B.cta_band()}'''
    schema = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": f"{p['name']}, {p['place']}",
               "about": p["type"], "description": p["summary"], "image": [B.url(f"/assets/img/{m['base']}-1280.webp") for m in imgs[:4]],
               "creator": {"@type": "Organization", "name": C.FOUNDER["company_uk"], "url": C.FOUNDER["company_uk_url"], "description": "Main contractor"},
               "locationCreated": {"@type": "Place", "name": p["place"]},
               "subjectOf": [{"@type": "WebPage", "url": p["source"]}] + [{"@type": "WebPage", "url": u} for _, u in p["recognition"] if u]}]
    awards = [r for r, _ in p["recognition"] if not r.startswith(("Reported", "Featured")) and "longlist" not in r]
    if awards:
        schema[0]["award"] = awards  # awarded to the house and its project team
    B.page(path, f"{p['name']}, {p['place'].replace(', Cornwall', '')} | Eastbridge Work",
           (f"{p['name']}, {p['place']}: {p['summary']} Built by P Chapman Construction." if len(p['summary']) < 105 else f"{p['name']}, {p['place']}: {p['summary']}"),
           body, crumbs, schema, og=B.og_image(imgs[0]["base"]), preload=f"/assets/img/{imgs[0]['base']}-1280.webp")

# ---------------------------------------------------------------- approach / independence / fees / about
def approach():
    crumbs = [("Home", "/"), ("How we work", "/approach/")]
    body = B.banner(crumbs, "How we work", "One programme, one budget, one decision log, and an independent firm on your side, working alongside your consultant and contractor.", "polgreen-manor-07", credit_of("polgreen-manor-07")) + f'''
<section class="section dark"><div class="wrap">{stages_html()}</div></section>
<section class="section"><div class="wrap split"><div><h2>The rhythm of a project</h2></div><div class="prose">
<p>Every project runs to the same rhythm, because rhythm is what keeps a two-year build under control.</p>
<h3>Every week</h3><ul><li>A short photo update from site</li><li>Any decisions you need to make, with a recommendation and a deadline</li></ul>
<h3>Every month</h3><ul><li>A written report: progress against programme, cost to complete, risks and issues</li><li>Our recommendation on the contractor's payment application</li><li>A review of variations, approved, rejected or pending</li></ul>
<h3>At every key stage</h3><ul><li>A walk-round with you, in person or by video</li><li>A check that the next stage can start without avoidable risk</li></ul>
<h3>Always</h3><ul><li>A decision log, so nothing you agree is forgotten or reopened</li><li>An issues log with owners and dates</li></ul>
<p>The exact rhythm, including how often we are on site at each stage, is agreed in writing in your appointment.</p>
</div></div></section>
<section class="section paper"><div class="wrap split"><div><h2>Who does what</h2></div><div class="prose table-wrap">
<table><thead><tr><th>Party</th><th>Their role</th></tr></thead><tbody>
<tr><td>You, the owner</td><td>Decide, approve and pay. Appoint the consultant and contractor.</td></tr>
<tr><td>Eastbridge</td><td>Represent you: brief, budget, programme, appointments advice, cost control, reporting, variations and claims, handover.</td></tr>
<tr><td>Registered consultant</td><td>Statutory design, authority submissions and the supervision duties required by law.</td></tr>
<tr><td>Main contractor</td><td>Build the villa to the contract, manage subcontractors and site safety.</td></tr>
<tr><td>Other specialists</td><td>Quantity surveyors, engineers, testing labs and lawyers, appointed and paid by you when the project needs them.</td></tr>
<tr><td>Master developer</td><td>Review the design against the community guidelines and issue NOCs.</td></tr>
<tr><td>Permitting authority</td><td>Dubai Municipality, Trakhees or the Dubai Development Authority depending on your plot; the municipality via TAMM in Abu Dhabi.</td></tr>
</tbody></table>
<p>Read more in <a href="/insights/owners-representative-vs-project-manager-vs-consultant/">owner's representative vs project manager vs consultant</a>.</p></div></div></section>
<section class="section" id="uae-appointments"><div class="wrap split"><div><h2>How an appointment works in the UAE</h2><p class="muted">What you can expect from us on a villa in Dubai or Abu Dhabi, and where our role stops.</p></div><div class="prose">
<h3>Who leads your project</h3><p>Our founder, Philip Chapman, leads every Eastbridge appointment personally, supported by a team of three project managers who attend site and provide cover when he is unavailable. Philip is the person you speak to from the first conversation to handover. Capacity is confirmed before an appointment is accepted.</p>
<h3>Site attendance and reporting</h3><p>How often we attend site, which meetings we attend on your behalf and the reports you receive are agreed in writing in the scope of each appointment, before work starts. Attendance follows the stage of the project: typically weekly during active construction, and more often at key stages such as waterproofing, first fix and pre-handover. Agreeing this up front means the time committed to your project is clear from the start.</p>
<h3>Consultants, quantity surveyors, engineers and specialists</h3><p>Where the project needs a registered consultant, a quantity surveyor, an engineer or another specialist, you appoint them and pay them directly. We help you define what is needed, compare proposals like-for-like and choose. We take no commission or referral fee from any of them, and money never passes through us.</p>
<h3>What we do, and what we don't</h3>
<p>We provide commercial and project management on your side of the table: the brief, budget and programme, cost reporting, review of payments and variations, commercial and contractual advice, client-side site visits and reporting, decision and issues logs, and handover.</p>
<p>We do not carry out statutory design, authority submissions or permit applications, statutory supervision or certification of the works. Those duties sit with the registered consultant you appoint. We do not give legal advice; where it is needed, take advice from a UAE-qualified lawyer, and we will work alongside them.</p>
</div></div></section>
<section class="section"><div class="wrap split"><div><h2>Why a builder's background matters</h2></div><div class="prose">
<p>Many owner's representatives come from consultancy. Philip came from contracting. For 21 years our founder, Philip Chapman, ran P Chapman Construction, a premium building company whose houses have won RIBA and LABC recognition, pricing tenders, running sites, preparing and defending extension of time and variation claims under JCT contracts, and handing over houses to demanding owners and architects.</p>
<p>That background is unusual on the client side, and it is the point. We know where a contractor's price has room, where a programme has float, and which details get closed up before anyone looks. We use that knowledge fairly. Good contractors welcome an informed client, because informed clients make decisions on time and pay what is due.</p>
<p>See <a href="/insights/what-the-contractor-knows/">what a builder knows that most villa owners don't</a>.</p></div></div></section>
{B.cta_band()}'''
    B.page("/approach/", "How We Work: Villa Projects, Stage by Stage | Eastbridge",
           "Our six-stage approach to villa builds and renovations in Dubai, from brief and budget to handover, with weekly and monthly reporting.",
           body, crumbs)

def independence():
    crumbs = [("Home", "/"), ("Independence pledge", "/independence/")]
    items = [
     ("Paid only by you", "Our only income on your project is the fee you pay us. We accept no commission, referral fee, rebate, discount, gift or hospitality from any consultant, contractor, subcontractor or supplier."),
     ("We don't build", "We hold no construction contracts and have no ownership in any contracting business working on a project we represent."),
     ("We don't design", "We never act as designer or consultant of record on a project we represent, so we never review our own work."),
     ("We disclose everything", "If we have ever worked with, or know personally, anyone you are considering appointing, we tell you in writing before you decide."),
     ("You appoint, you pay", "Consultants and contractors are appointed by you and paid by you directly. Money never passes through us."),
     ("We will say no", "If you don't need us, or a project is outside what we do well, we will tell you."),
     ("Your information stays yours", "Your plans, budget and personal details are confidential. We never publish a client's name, address or project without written permission."),
    ]
    lis = "".join(f"<li><strong>{esc(t)}</strong>{esc(d)}</li>" for t, d in items)
    body = B.banner(crumbs, "Our independence pledge", "In a market where many project managers also design, build or take referral fees, independence has to be written down. This is ours, and it is written into every Eastbridge appointment.", "the-lookout-09", credit_of("the-lookout-09")) + f'''
<section class="section"><div class="wrap"><ul class="pledge">{lis}</ul></div></section>
<section class="section paper"><div class="wrap split"><div><h2>Why it matters</h2></div><div class="prose">
<p>When the person checking the contractor's invoices also earns a referral fee from that contractor, the check is not independent. When a design-and-build company's in-house project manager reports to the same owner as the builders, the check is not independent. When a consultant reviews the cost of a design they produced, the check is not independent.</p>
<p>None of these arrangements is necessarily dishonest. They are simply not independent. If you want an independent check, it has to come from someone with no other stake in the project.</p>
<p>Read more: <a href="/fees/">how our fees work</a>, <a href="/approach/">how we work</a> and <a href="/why-a-client-side-project-manager/">why appoint a client-side project manager</a>.</p></div></div></section>
{B.cta_band()}'''
    B.page("/independence/", "Independence Pledge: No Contractor Commissions | Eastbridge",
           "Eastbridge is paid only by the client. No commissions, referral fees or rebates from contractors, consultants or suppliers. We don't build and we don't design.",
           body, crumbs)

def fees():
    crumbs = [("Home", "/"), ("How fees work", "/fees/")]
    f = C.FEES
    show = C.PUBLISH_FEES
    def fixed(k):
        # A figure appears only when the owner has approved publishing (config.PUBLISH_FEES).
        return (f'Fixed fee: <strong>{esc(f[k])}</strong>. The final quotation is confirmed in writing after the free call, before we start.'
                if show else "Fixed fee, quoted in writing before we start.")
    def basis(factors):
        if show:
            return (f"<p>The figure above is for a typical review. If yours differs, for example in {factors}, we say so on the free call. "
                    "We confirm the fee and the scope in writing before we start.</p>")
        return f"<p>By {factors}. We confirm the fee and the scope in writing before we start.</p>"
    rep_fee = (f'Monthly fee from <strong>{esc(f["monthly_from"])}</strong>, or <strong>{esc(f["percent_band"])}</strong> of construction cost. '
               if show else "Monthly fee, or a percentage of construction cost. ")
    steps = [
        ("A free 30-minute call", "No cost and no obligation. You tell us about the plot, the villa or the project you are already in; we ask the questions a builder would ask and tell you plainly whether you need us, and which first step would help."),
        ("A fixed-fee first review", "A plot and pre-purchase review, or a health check on a project already under way. We send the scope, what you will receive and the fee in writing, and start only when you have agreed it."),
        ("An appointment, if you want one", "If you want us to carry on, we propose a written appointment for the stages you need, with the scope, site attendance, reporting and fee set out up front. The review does not commit you to it."),
    ]
    later = [
        ("Brief, budget and team appointment", "The brief, a realistic budget and programme, and help choosing and appointing your consultant and contractor.",
         "Fixed fee per stage, based on the size and complexity of the villa and the number of appointments you need to make."),
        ('<a href="/services/owners-representative/">Owner\'s representation</a> during design and construction', "Cost and programme control, payment and variation review, client-side site visits, reporting, the decision log and handover.",
         rep_fee + "Set by the scope, the site attendance and reporting agreed in your appointment, and the expected duration."),
        ('<a href="/services/snagging-and-handover/">Snagging and handover</a> only', "Snagging inspections on your behalf, tracking of defects to close-out, and the handover documents.",
         "Fixed fee, based on the size of the villa and the number of inspections needed."),
        ('<a href="/services/variations-delays-and-claims/">Variations and claims advice</a>', "A review of a variation, delay or claim position, and support in negotiation.",
         "Fixed fee per review, or hourly for negotiations. Quoted per matter once we have seen the papers."),
    ]
    later_rows = "".join(f"<tr><td>{a}</td><td>{esc(b)}</td><td>{c}</td></tr>" for a, b, c in later)
    body = B.banner(crumbs, "How our fees work", "Clear, fixed where possible, and paid only by you. We'd rather tell you the structure up front than surprise you later.", "owers-house-11", credit_of("owers-house-11")) + f'''
<section class="section starts" aria-labelledby="fees-starts-h"><div class="wrap"><div class="head-row"><div><span class="kicker">How it starts</span><h2 id="fees-starts-h">From a free call to an appointment</h2></div><p class="muted">The call is free. After that, you decide at each step whether to go on.</p></div>
{B.steps_html(steps)}</div></section>
<section class="section paper" id="first-review"><div class="wrap split"><div><span class="kicker">First paid step</span><h2>Plot and pre-purchase review</h2>
<dl class="facts"><div><dt>Who it's for</dt><dd>Buyers considering a villa plot, before they commit</dd></div><div><dt>How it's charged</dt><dd>{fixed("plot_review")}</dd></div><div><dt>Timing</dt><dd>Within five working days of receiving the plot documents</dd></div></dl>
<p class="small"><a class="link" href="/services/plot-due-diligence/">About the plot review</a></p></div><div class="prose">
<h3>Scope</h3><ul><li>The master developer's design guidelines: coverage, heights, setbacks and materials</li><li>Build-by deadlines and any penalties in the sale terms</li><li>Access, levels, neighbouring plots and practical buildability</li><li>A realistic build budget range for the house you want, and the total cost of ownership</li></ul>
<h3>You receive</h3><ul><li>A short written report you can read in fifteen minutes</li><li>A total project budget range, not just a plot price</li><li>The risks that matter, and a list of questions to put to the seller or developer</li></ul>
<h3>Not included</h3><ul><li>Legal advice on title or the sale contract: take advice from a UAE-qualified lawyer</li><li>Valuation: use a RICS or RERA-registered valuer</li><li>Design, surveys, ground investigation or authority submissions</li></ul>
<h3>How the quotation is set</h3>{basis("the number of plots you want reviewed, the documents available and the timetable you are working to")}
</div></div></section>
<section class="section"><div class="wrap split"><div><span class="kicker">First paid step</span><h2>Project health check</h2>
<dl class="facts"><div><dt>Who it's for</dt><dd>Owners whose project is under way and stalled, late, over budget or in dispute</dd></div><div><dt>How it's charged</dt><dd>{fixed("rescue_review")}</dd></div><div><dt>Timing</dt><dd>We start within a week; the full picture within two to three weeks</dd></div></dl>
<p class="small"><a class="link" href="/services/stalled-project-rescue/">About stalled project rescue</a></p></div><div class="prose">
<h3>Scope</h3><ul><li>An independent review of progress, quality, payments and the contract position</li><li>A realistic cost and time to complete</li><li>The options: continue, renegotiate or replace the contractor</li></ul>
<h3>You receive</h3><ul><li>The full picture: where the project stands on progress, quality, payments and the contract</li><li>Clear options, each with its costs and risks</li><li>A recovery plan for the option you choose</li></ul>
<h3>Not included</h3><ul><li>Legal advice on withholding payment, termination or disputes: take advice from a UAE-qualified lawyer</li><li>Statutory supervision, certification of work or engineering investigation, which remain with the registered consultant and any engineer you appoint</li><li>Running the recovery through to completion, which would be a separate appointment if you want one</li></ul>
<h3>How the quotation is set</h3>{basis("the size and stage of the villa, the volume of contract and payment records to review, and the site visits the review needs")}
</div></div></section>
<section class="section paper"><div class="wrap prose table-wrap"><h2>After the first review</h2>
<p>Later stages are quoted once we understand the project. Each quotation sets out the scope and the fee in writing before any work starts.</p>
<table><thead><tr><th>Service</th><th>What it covers</th><th>How the fee is set</th></tr></thead><tbody>
{later_rows}
</tbody></table>
<h2>What's included</h2><ul><li>All our time, reporting and site visits as set out in your appointment</li><li>Travel within Dubai and to Abu Dhabi</li></ul>
<h2>What's not included</h2><ul><li>Fees of the consultant, contractor, quantity surveyors, engineers, testing labs or lawyers you appoint; you pay them directly</li><li>Authority and master developer fees</li><li>International travel at your request</li></ul>
<h2>What we never charge</h2><p>We never take commission, referral fees, mark-ups or rebates from anyone on your project. See our <a href="/independence/">independence pledge</a>.</p>
<h2>Is it worth it?</h2><p>Our fee is an addition to your project budget, so it should earn its place. What it pays for is regular cost reporting, programme monitoring, review of every payment and variation, a record of decisions, and early warning of risks while they are still cheap to deal with. If we don't think your project needs us, we'll say so in the free call.</p>
</div></section>
{B.cta_band("Start with a free 30-minute call.", f"{C.RESPONSE_PROMISE} to arrange a time. We will tell you which first step, if any, would help.")}'''
    B.page("/fees/", "Owner's Representative Fees in Dubai: How We Charge | Eastbridge",
           "How we charge for villa owner's representation in Dubai: a free first call, a fixed-fee plot review or project health check, then a written appointment.",
           body, crumbs)

def about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    from content.projects import RECOGNITION, TESTIMONIALS, recognition_html
    import pages_new
    rec = recognition_html(RECOGNITION)
    body = B.banner(crumbs, "About Eastbridge", "A client-side practice built on 21 years running a £17m-turnover premium building company whose houses won RIBA and LABC recognition.", "owers-house-04", credit_of("owers-house-04")) + f'''
<section class="section" id="founder"><div class="wrap feature">
<figure class="portrait">{pic("philip-chapman-01", "Philip Chapman, Founding Partner of Eastbridge Strategic Partners", "(max-width:900px) 100vw, 42vw")}</figure>
<div><span class="kicker">Founding Partner</span><h2>Philip Chapman</h2><p class="muted">British. Based in Dubai.</p><div class="prose">
<p>Philip Chapman founded <a href="{C.FOUNDER["company_uk_url"]}" rel="noopener">P Chapman Construction</a> and led it for 21 years, growing it into a premium contractor with an annual turnover of around £17 million and a reputation for exceptionally demanding private houses.</p>
<p>Houses the company built have been recognised in their own right. Owers House, built by P Chapman Construction and completed in 2014, was featured on Channel 4's Grand Designs, won a RIBA South West Award in 2016 and was reported in <a href="https://www.thetimes.co.uk/article/wings-of-desire-9cgnbh3fg" rel="noopener">The Times</a>. The Old Station Master's House in Fowey won Best Small New Housing Development in the LABC Building Excellence Awards South West 2018 (<a href="https://www.acornpropertygroup.org/old-station-masters-house-wins-labc-award/" rel="noopener">source</a>), and Polgreen Manor was Highly Commended in the 2020 South West awards (<a href="https://www.labc.co.uk/news/labc-south-west-winners-amp-highly-commended-2020" rel="noopener">source</a>). These awards belong to the houses and the teams that designed and built them. Alongside one-off houses it delivered country-house restorations, multi-unit developments, hotel and spa work, and schools, under both traditional and design-and-build contracts.</p>
<p>Two decades as the builder meant pricing tenders, programming complex sites, managing subcontractors, administering JCT contracts, preparing and defending extension of time and variation claims, and handing finished homes to owners and design teams who expected them to be perfect. It also meant seeing, from the inside, exactly where owners lose money and time.</p>
<p>In Dubai and Abu Dhabi, Philip works on the other side of the table: for the owner, never the builder. He leads every Eastbridge appointment personally, supported by a team of three project managers who attend site and provide cover when he is unavailable, and he is the person you speak to from the first conversation to handover.</p>
<p>Away from work he is a high-altitude mountaineer, which may explain a fondness for planning, contingency and getting everyone home safely.</p>
</div></div></div></section>
<section class="section--tight" id="recognition"><div class="wrap"><div class="kpis kpis--text">{rec}</div></div></section>
<section class="section band-dark"><div class="wrap"><div class="head-row"><h2>What clients said about the work</h2><p class="muted">Clients of P Chapman Construction.</p></div>{pages_new.quotes_html(TESTIMONIALS[:3])}</div></section>
<section class="section stone"><div class="wrap split"><div><h2>Why the client's side</h2></div><div class="prose">
<p>Dubai and Abu Dhabi are building some of the most ambitious private homes in the world. The owners commissioning them are often busy, frequently abroad and rarely builders themselves. The market around them is full of capable firms, but few that act only for the owner and take nothing from anyone else.</p>
<p>That is the gap we fill. We bring the builder's knowledge to the owner's side, and we keep it there. <a href="/why-a-client-side-project-manager/">Why it matters</a>.</p></div></div></section>
<section class="section"><div class="wrap split"><div><h2>Plainly stated</h2></div><div class="prose">
<ul>
<li>We are {esc(C.LEGAL)}, licensed in the Meydan Free Zone, Dubai ({esc(C.LICENCE.split("licence ")[-1])}).</li>
<li>We are a client-side project manager and owner's representative. We are not a contractor, an engineering consultancy, a law firm or an estate agency.</li>
<li>We are paid only by the owner we represent. See our <a href="/independence/">independence pledge</a>.</li>
</ul></div></div></section>
<section class="section paper"><div class="wrap split"><div><h2>Working with us in the UAE</h2></div><div class="prose">
<ul>
<li>Philip leads every appointment personally, supported by a team of three project managers who attend site and provide cover when he is unavailable. Capacity is confirmed before an appointment is accepted.</li>
<li>Site attendance and reporting are agreed in writing in the scope of each appointment, before work starts.</li>
<li>Registered consultants, quantity surveyors, engineers and other specialists are appointed and paid by you directly when the project needs them. We help you compare proposals and choose.</li>
<li>Our role is commercial and project management on your side. Statutory design, authority submissions and supervision stay with your registered consultant, and legal advice with your UAE-qualified lawyer.</li>
</ul>
<p>More detail in <a href="/approach/#uae-appointments">how an appointment works in the UAE</a> and <a href="/fees/">how our fees work</a>.</p></div></div></section>
{B.cta_band()}'''
    B.page("/about/", "About Eastbridge and Founder Philip Chapman | Dubai",
           "Eastbridge is led by Philip Chapman, who ran P Chapman Construction, a £17m UK builder of award-winning homes, for 21 years. Now he acts only for villa owners.",
           body, crumbs, [B.person_schema()], og=B.og_image("owers-house-02"))

# ---------------------------------------------------------------- faq / contact / legal
FAQ_ALL = [
 ("What is an owner's representative?", "An owner's representative is a professional who acts only for the person paying for a building project. On a villa, we set the budget and programme, help appoint the consultant and contractor, control cost and time, report progress, handle variations and claims, and lead handover."),
 ("Do I need an owner's representative to build a villa in Dubai?", "It isn't required by law. It is most valuable on bespoke villas, major renovations, and projects where the owner is often abroad or has not built before. We will tell you honestly if you don't need us."),
 ("How is that different from the consultant I have to appoint?", "In Dubai, a registered consultant carries the statutory design, submission and supervision responsibilities. They owe you proper professional care in that role. We add independent coordination and commercial scrutiny alongside them, acting only for you on cost, time, decisions, contracts and quality."),
 ("Who will lead my project?", "Our founder, Philip Chapman, leads every Eastbridge appointment personally and is the person you speak to from the first conversation to handover. He is supported by a team of three project managers who attend site and provide cover when he is unavailable."),
 ("Who attends site, and who covers when Philip is away?", "Philip leads every appointment and attends site himself. He is supported by a team of three project managers who attend site and provide cover when he is unavailable, for example when he is travelling. How often we attend site is agreed in writing in your appointment."),
 ("How often will you be on site?", "It is agreed in writing in the scope of your appointment, before work starts. Attendance follows the stage of the project: typically weekly during active construction and more often at key stages. See <a href=\"/approach/#uae-appointments\">how an appointment works in the UAE</a>."),
 ("Who appoints the quantity surveyor, engineers and other specialists?", "You do, and you pay them directly. We help you work out what is needed, compare proposals like-for-like and choose. We take no commission or referral fee from anyone we help you appoint."),
 ("Do you handle permits, supervision or legal advice?", "No. Statutory design, authority submissions and supervision are the duties of the registered consultant you appoint, and legal advice should come from a UAE-qualified lawyer. Our role is commercial and project management on your side, alongside them."),
 ("Do you take commission from contractors?", "Never. We are paid only by you. See our <a href=\"/independence/\">independence pledge</a>."),
 ("How do your fees work?", "The first call is free and takes about 30 minutes. If we can help, the first paid step is usually a fixed-fee review, either a plot and pre-purchase review or a health check on a project under way, scoped and quoted in writing before we start." + (f" The plot review is {C.FEES['plot_review']} and the health check {C.FEES['rescue_review']}; representation during design and construction is from {C.FEES['monthly_from']} a month, or {C.FEES['percent_band']} of construction cost. The final quotation is confirmed in writing after the free call." if C.PUBLISH_FEES else "") + " Any later appointment is proposed separately, with its fee agreed up front. See <a href=\"/fees/\">how fees work</a>."),
 ("How do I arrange the free call?", "Send the short form on our <a href=\"/contact/\">contact page</a>, message us on WhatsApp or call. Philip replies personally to agree a time that suits you; there is no automatic booking."),
 ("What does it cost to build a villa in Dubai?", "Published 2025–26 guides put construction at roughly AED 300–500 per sq ft for a standard villa, AED 900–1,400 for luxury, and AED 1,200 and above for ultra-luxury, before land, design fees, approvals, interiors and landscaping. See our <a href=\"/insights/villa-construction-cost-dubai/\">full cost guide</a>."),
 ("How long does it take?", "Market guides put plot to keys at roughly 12 to 24 months, and 24 to 36 months for custom luxury villas. See <a href=\"/insights/how-to-build-a-villa-in-dubai/\">how to build a villa in Dubai</a>."),
 ("Do you work in Abu Dhabi?", "Yes. We represent owners in Dubai and Abu Dhabi, always alongside a locally registered consultant of record."),
 ("Can you help if my project has already started?", "Yes. We can join at any stage, including projects that have stalled or are in dispute. See <a href=\"/services/stalled-project-rescue/\">stalled project rescue</a>."),
 ("Can you work for me if I live in the UK?", "Yes. Many Dubai villa owners live overseas. We report weekly in a format you can read on your phone, and bring you every decision that matters. See <a href=\"/services/overseas-owners/\">owners living overseas</a>."),
 ("Do you speak Arabic?", "We work in English. Arabic-speaking clients are very welcome to bring an interpreter or adviser to any meeting."),
 ("Is my enquiry confidential?", "Yes. We never share or publish client names, addresses or projects without written permission."),
]

def faq_page():
    crumbs = [("Home", "/"), ("Questions", "/faq/")]
    body = B.banner(crumbs, "Questions villa owners ask us", None, "quay-house-07", credit_of("quay-house-07")) + f'''
<section class="section--tight"><div class="wrap">{B.faq_html(FAQ_ALL)}</div></section>{B.cta_band("Ask us anything else.")}'''
    B.page("/faq/", "Villa Owner's Representative FAQ: Dubai & Abu Dhabi | Eastbridge",
           "Answers to common questions about owner's representation, villa build costs, timelines, fees, independence and working with Eastbridge in Dubai and Abu Dhabi.",
           body, crumbs, [B.faq_schema(FAQ_ALL)])

def contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    stages = "".join(f"<option>{esc(v)}</option>" for v in
                     ["Considering a plot", "Plot bought", "In design", "Choosing a contractor", "Under construction",
                      "Planning a renovation", "Stalled or in dispute", "Near handover", "Something else"])
    areas = "".join(f'<option>{esc(a["name"])}</option>' for a in AREAS) + "<option>Elsewhere in Dubai</option><option>Elsewhere in Abu Dhabi</option>"
    budgets = "".join(f"<option>{esc(v)}</option>" for v in
                      ["Under AED 3m", "AED 3m–8m", "AED 8m–20m", "AED 20m–50m", "Over AED 50m", "Not sure yet"])
    based = "".join(f"<option>{esc(v)}</option>" for v in ["UAE", "United Kingdom", "Europe", "GCC", "Elsewhere"])
    methods = "".join(f'<label class="choice"><input type="radio" name="contact_method" value="{v}"{" checked" if v == "Email" else ""}> {v}</label>'
                      for v in ["Email", "Phone call", "WhatsApp"])
    opt = '<span class="opt">Optional</span>'
    req = '<span class="req">Required</span>'
    def err(i, msg):
        return f'<p class="err" id="{i}-err" hidden>{msg}</p>'
    steps = B.start_steps()
    next_steps = [("We reply within one working day", "A personal reply from Philip, by the method you choose in the form.")] + steps
    body = B.banner(crumbs, "Arrange a free 30-minute call", "Tell us a little about your project and how you would like us to reply. Philip replies personally within one working day to agree a time; the form does not book a slot automatically. Nothing you send is published, and it is shared only with the service providers named in our privacy notice.", "the-lookout-02", credit_of("the-lookout-02")) + f'''
<section class="section--tight"><div class="wrap split contact-grid">
<div class="contact-side">
<h2 class="h-sm">Prefer to talk?</h2>
<p class="contact-actions"><a class="btn" href="{B.wa_link()}" rel="noopener">Message us on WhatsApp</a><a class="btn btn--ghost" href="tel:{C.PHONE_E164}">Call {C.PHONE_DISPLAY}</a></p>
<p>Email <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
<p class="muted small">{esc(C.HOURS)}. UK and European clients are welcome to arrange calls in their own time zone.</p>
<h2 class="h-sm">What happens next</h2>
{B.steps_html(next_steps, "steps steps--compact")}
<p class="small"><a class="link" href="/fees/">How fees work</a></p>
</div>
<form class="form" id="brief" name="brief" method="POST" action="/contact/thanks/" data-netlify="true" netlify-honeypot="company_site" data-enquiry>
<input type="hidden" name="form-name" value="brief">
<p class="hp"><label>Leave this empty <input name="company_site" tabindex="-1" autocomplete="off"></label></p>
<p class="form-note small muted">Three fields are required: your name, your email and a few words about the project. Fields marked Optional help us reply usefully, but you can leave them blank.</p>
<div class="row"><div class="field"><label for="f-name">Your name {req}</label><input id="f-name" name="name" autocomplete="name" required aria-describedby="f-name-err">{err("f-name", "Please tell us your name.")}</div>
<div class="field"><label for="f-email">Email {req}</label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="f-email-err">{err("f-email", "Please enter an email address we can reply to, such as name@example.com.")}</div></div>
<fieldset class="field"><legend>How would you like us to reply? {opt}</legend><div class="checks">{methods}</div></fieldset>
<div class="row"><div class="field"><label for="f-phone">Phone or WhatsApp number <span class="opt ph-opt">Optional</span><span class="opt ph-req" hidden>Needed for a call or WhatsApp</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" minlength="7" pattern="\\+?[0-9][0-9 \\(\\)\\-]{{6,}}" aria-describedby="f-phone-hint f-phone-err"><p class="hint" id="f-phone-hint">Include the country code, for example +971 or +44.</p>{err("f-phone", "Please enter a phone number with its country code, for example +971 50 123 4567.")}</div>
<div class="field"><label for="f-based">Where are you based? {opt}</label><select id="f-based" name="based"><option value="">Choose</option>{based}</select></div></div>
<div class="row"><div class="field"><label for="f-stage">Project stage {opt}</label><select id="f-stage" name="stage"><option value="">Choose a stage</option>{stages}</select></div>
<div class="field"><label for="f-area">Where is the project? {opt}</label><select id="f-area" name="area"><option value="">Choose a location</option>{areas}</select></div></div>
<div class="field"><label for="f-budget">Approximate construction budget {opt}</label><select id="f-budget" name="budget" aria-describedby="f-budget-hint"><option value="">Choose a range</option>{budgets}</select><p class="hint" id="f-budget-hint">A rough band is enough. It helps us judge the scale, and is never published.</p></div>
<div class="field"><label for="f-msg">Tell us about the project {req}</label><textarea id="f-msg" name="message" required minlength="10" aria-describedby="f-msg-hint f-msg-err"></textarea><p class="hint" id="f-msg-hint">The house you want, the plot or villa you have, and anything that is worrying you.</p>{err("f-msg", "Please add a few words about your project.")}</div>
<div class="field"><label class="consent" for="f-mkt"><input id="f-mkt" name="marketing_opt_in" type="checkbox" value="yes"> <span>Optional: also send me Eastbridge notes for villa owners by email, no more than once a month. Leaving this unticked does not affect your enquiry. Unsubscribe at any time by replying to any note or writing to {C.EMAIL}.</span></label></div>
<div class="reassure"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><rect x="5" y="10.5" width="14" height="10" rx="1"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>
<p><b>Confidential.</b> Read personally by Philip and used to reply to you (and, if you tick the box above, to send our notes). We never share or publish client names, addresses or projects without written permission. See our <a href="/privacy/">privacy notice</a>.</p></div>
<p class="submit-row"><button class="btn" type="submit">Send your enquiry</button><span class="small muted">{esc(C.RESPONSE_PROMISE)}.</span></p>
</form></div></section>'''
    schema = [{"@context": "https://schema.org", "@type": "ContactPage", "url": B.url("/contact/"), "about": {"@id": B.ORG_ID}}]
    B.page("/contact/", "Contact Eastbridge: Arrange a Free 30-Minute Call | Dubai",
           "Arrange a free 30-minute call about your villa build or renovation in Dubai or Abu Dhabi. Philip replies personally within one working day, by email, phone or WhatsApp.",
           body, crumbs, schema)

    thanks_steps = [
        ("Philip reads your brief", f"{esc(C.RESPONSE_PROMISE)}, by the method you chose. Our hours are {esc(C.HOURS)}, so a brief sent at the weekend is normally answered on the next working day."),
        ("A free 30-minute call", "At a time that suits you, including UK and European hours. If you have drawings, plot details or contractor quotes, have them to hand; they are not essential."),
        ("A written next step", "If we can help, a scope and fixed fee for the first stage. If we can't, we will say so and, where we can, point you to someone who can."),
    ]
    reads = [("/why-a-client-side-project-manager/", "Why a client-side project manager", "What the role is, and where it adds value."),
             ("/case-studies/island-e-waterfront-villa/", "Island E: worked project example", "A hypothetical example of how we would manage an Island E villa, from plot to keys."),
             ("/insights/villa-construction-cost-dubai/", "What it costs to build a villa in Dubai", "Published 2026 build costs, tier by tier.")]
    read_html = "".join(f'<li><a href="{u}"><b>{esc(t)}</b><span>{esc(d)}</span></a></li>' for u, t, d in reads)
    tcrumbs = [("Home", "/"), ("Contact", "/contact/"), ("Thank you", "/contact/thanks/")]
    # One page serves both forms: the newsletter posts to /contact/thanks/#notes and the script
    # swaps the blocks marked data-thanks. Without JavaScript the brief version shows.
    B.page("/contact/thanks/", "Thank you | Eastbridge", "Your brief has been received.",
           f'''<section class="page-head"><div class="wrap">{B.crumbs_html(tcrumbs)}<h1>Thank you.</h1>
<p class="lede" data-thanks="brief">Your brief is with us. {esc(C.RESPONSE_PROMISE)}. Here is what happens next.</p>
<p class="lede" data-thanks="notes" hidden>You are on the list. Our notes for villa owners arrive no more than once a month: build costs, approvals and what is moving in the market. To unsubscribe at any time, reply to any note or write to <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p></div></section>
<section class="section--tight thanks"><div class="wrap">
<div data-thanks="brief">{B.steps_html(thanks_steps)}</div>
<div class="split thanks-more"><div><h2 class="h-sm" data-thanks="brief">If it is urgent</h2><h2 class="h-sm" data-thanks="notes" hidden>Planning a villa now?</h2><p class="contact-actions"><a class="btn" href="{B.wa_link()}" rel="noopener">Message us on WhatsApp</a><a class="btn btn--ghost" href="tel:{C.PHONE_E164}">Call {C.PHONE_DISPLAY}</a></p></div>
<div><h2 class="h-sm">While you wait</h2><ul class="read-list">{read_html}</ul></div></div>
</div></section>''',
           tcrumbs, noindex=True)

def legal():
    crumbs = [("Home", "/"), ("Privacy", "/privacy/")]
    # Wording follows the systems actually in place: Netlify Forms stores submissions; the optional
    # submission-created function sends acknowledgements and can log to a Google Sheet; analytics and
    # the background film appear only when switched on in config.py. Final wording: owner/legal review.
    if C.GA4_ID:
        analytics = ("<p>We use Google Analytics, with IP anonymisation, to see how the site is used: pages visited, device type "
                     "and approximate location. It sets cookies for this purpose.</p>")
        cookies = ("<p>This site uses no advertising cookies. Google Analytics sets cookies to measure use of the site. "
                   "A video provider may set its own cookies once you choose to play a film.</p>")
    else:
        analytics = "<p>This site does not currently use analytics, advertising or tracking tools. If that changes, we will update this notice first.</p>"
        cookies = "<p>This site sets no analytics or advertising cookies. A video provider may set its own cookies once you choose to play a film.</p>"
    film = (" On larger screens the home page may also load a muted background film from Vimeo automatically."
            if C.HERO_VIDEO else "")
    body = B.page_head(crumbs, "Privacy notice", None) + f'''<section class="section--tight"><div class="wrap prose">
<p>Last updated {datetime.date.today().strftime("%-d %B %Y")}.</p>
<p>{esc(C.LEGAL)} ("Eastbridge", "we") is licensed in the Meydan Free Zone, Dubai ({esc(C.LICENCE)}). This notice explains how we handle personal data collected through this website, consistent with the UAE Personal Data Protection Law (Federal Decree-Law No. 45 of 2021) and, for visitors in the UK and EU, the UK and EU GDPR.</p>
<h2>What we collect</h2>
<ul>
<li><b>Project enquiries.</b> What you enter in the enquiry form: your name, email, how you would like us to reply and, if you give them, your phone number, where you are based, your project stage, location and budget band, and your message. The same applies to anything you send us by email, phone or WhatsApp.</li>
<li><b>Checklist requests.</b> Your name, your email and, if you choose one, your project stage.</li>
<li><b>Calculator estimates.</b> If you send us an estimate from our cost calculator: your name, your email, the calculator inputs and result, a link to the estimate and, if you give them, your phone number, plot location and notes.</li>
<li><b>Our notes.</b> Your email address, if you subscribe or tick the optional box on the enquiry, checklist or estimate form, and a record of that choice.</li>
<li><b>Technical data.</b> Our website host processes technical data, such as your IP address, to deliver the site and to filter spam from form submissions.</li>
</ul>
{analytics}
<h2>How we use it</h2>
<ul>
<li><b>Enquiries:</b> to reply to you by the method you choose, to prepare a proposal if you ask for one, and to deliver our services if you appoint us.</li>
<li><b>Calculator estimates:</b> for Philip to review the estimate and reply to you. We never pass your details to contractors or suppliers.</li>
<li><b>Checklist requests:</b> to give you the download and keep a record of the request. Asking for the checklist does not add you to our notes.</li>
<li><b>Confirmation emails:</b> when you send a form, we may send an automatic email confirming that it reached us. It contains no marketing unless you have asked for our notes.</li>
<li><b>Our notes (marketing):</b> occasional emails for villa owners, no more than once a month. We send them only to people who subscribe or who tick the optional box on a form. Leaving the box unticked never affects an enquiry, an estimate or a checklist request.</li>
</ul>
<p>We do not sell your data, publish it or use it for unrelated marketing.</p>
<h2>Unsubscribing from our notes</h2>
<p>You can stop our notes at any time: reply to any note with "unsubscribe", or write to <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>. We handle these requests by hand, and keep a short record of the request so that we do not email you again.</p>
<h2>Who we share it with</h2>
<p>Service providers that process data on our behalf:</p>
<ul>
<li>Netlify, our website host, which receives and stores form submissions;</li>
<li>our email providers, for our business mailbox and for sending confirmation emails and our notes;</li>
<li>Google, when we use Google Sheets to keep our log of enquiries and requests.</li>
</ul>
<p>Some of these providers process data outside the UAE. If you contact us on WhatsApp, WhatsApp handles those messages under its own terms. Films on our project pages are hosted by Vimeo or YouTube and load only when you press play; the provider then receives technical data such as your IP address.{film}</p>
<p>We share project information with third parties, such as a consultant or contractor, only with your agreement.</p>
<h2>How long we keep it</h2><p>We review our records each month and delete enquiries, estimate requests and checklist requests that don't lead to an appointment within 24 months. Notes subscriptions are kept until you unsubscribe. Client records are kept for the period required by law.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your data, object to how we use it, or withdraw your agreement to our notes at any time, by emailing <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p>
<h2>Cookies</h2>{cookies}
</div></section>'''
    B.page("/privacy/", "Privacy Notice | Eastbridge Strategic Partners", "How Eastbridge Strategic Partners handles personal data collected through this website.", body, crumbs)
    crumbs = [("Home", "/"), ("Terms", "/terms/")]
    body = B.page_head(crumbs, "Website terms", None) + f'''<section class="section--tight"><div class="wrap prose">
<p>This website is operated by {esc(C.LEGAL)}, {esc(C.LICENCE)}, {esc(C.ADDRESS["street"])}, {esc(C.ADDRESS["locality"])}, {esc(C.ADDRESS["country_name"])}.</p>
<h2>About the information on this site</h2><p>Articles and guides on this site are general information, not advice for your specific project. Costs, timelines and regulations change; figures are drawn from the sources cited and should be checked for your circumstances. Nothing on this site is legal, financial, valuation or engineering advice.</p>
<h2>Our role</h2><p>Eastbridge acts as an owner's representative and adviser. It is not a contractor, an engineering consultancy office, a law firm or a real estate broker. Statutory design, authority submissions and supervision of construction are carried out by registered consultants appointed by the client.</p>
<h2>Projects shown</h2><p>Projects shown on this site were delivered in the United Kingdom by P Chapman Construction, the company established and led by our founder, acting as main contractor. Photographs are credited to their photographers and used with permission.</p>
<h2>Liability</h2><p>Our services are provided only under a written appointment, which sets out our scope, fees and liability. To the extent permitted by law, we accept no liability for reliance on information on this website.</p>
<h2>Law</h2><p>These terms are governed by the laws of the Emirate of Dubai and the federal laws of the UAE.</p>
</div></section>'''
    B.page("/terms/", "Website Terms | Eastbridge Strategic Partners", "Terms of use for the Eastbridge Strategic Partners website.", body, crumbs)

# ---------------------------------------------------------------- insights
def guide_cta():
    import pages_guides
    return pages_guides.cta_block()

def insights(posts):
    crumbs = [("Home", "/"), ("Insights", "/insights/")]
    items = "".join(f'<li><a href="/insights/{p["slug"]}/"><div><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p></div><div class="meta">{esc(p.get("category",""))}<br>{datetime.date.fromisoformat(str(p["date"])).strftime("%-d %b %Y")}</div></a></li>' for p in posts)
    body = B.banner(crumbs, "Insights", "Straight answers for villa owners in Dubai and Abu Dhabi: costs, approvals, contracts and choosing a team, written from the builder's side of the table. New to the jargon? Start with our <a href=\"/glossary/\">villa construction glossary</a>.", "quay-house-04", credit_of("quay-house-04")) + f'''
<section class="section"><div class="wrap">{post_cards(posts)}</div></section>{B.cta_band()}'''
    B.page("/insights/", "Villa Building Insights for Dubai & Abu Dhabi Owners | Eastbridge",
           "Guides for villa owners in Dubai and Abu Dhabi: build costs, approvals, contractors, contracts, snagging and renovation, from the builder's side.",
           body, crumbs)
    for i, p in enumerate(posts):
        path = f"/insights/{p['slug']}/"
        c = [("Home", "/"), ("Insights", "/insights/"), (p["title"], path)]
        kp = "".join(f"<li>{esc(k)}</li>" for k in p.get("keypoints", []))
        faqs = [(f["q"], f["a"]) for f in p.get("faqs", [])]
        srcs = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a></li>' for s in p.get("sources", []))
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["html"])
        toc = ("<nav class=\"toc\" aria-label=\"In this article\"><strong>In this article</strong><ol>" +
               "".join(f'<li><a href="#{h}">{t}</a></li>' for h, t in heads) + "</ol></nav>") if len(heads) > 2 else ""
        d = datetime.date.fromisoformat(str(p["date"]))
        u = datetime.date.fromisoformat(str(p.get("updated", p["date"])))
        mins = max(3, round(p["words"] / 230))
        rel = [q for q in posts if q["slug"] != p["slug"] and q.get("category") == p.get("category")][:2] or \
              [q for q in posts if q["slug"] != p["slug"]][:3]
        rel = (rel + [q for q in posts if q["slug"] != p["slug"] and q not in rel])[:3]
        rel_html = "".join(f'<li><a href="/insights/{q["slug"]}/"><div><h3>{esc(q["title"])}</h3><p>{esc(q["description"])}</p></div><div class="meta">{esc(q.get("category",""))}</div></a></li>' for q in rel)
        upd = f" · Updated {u.strftime('%-d %B %Y')}" if u != d else ""
        hero_img = post_img(p)
        body_html = p["html"]
        pj = proj_of(hero_img)
        inline = [m["base"] for m in B.MANIFEST[pj["slug"]] if m["base"] != hero_img][:2]
        parts = re.split(r'(?=<h2 id=)', body_html)
        for k, ins in zip((2, 5), inline):
            if len(parts) > k:
                parts[k] = f'<figure>{pic(ins, pj["name"] + ", " + pj["place"], "(max-width:760px) 100vw, 720px")}<figcaption>{esc(pj["name"])}, {esc(pj["place"])}. Built by P Chapman Construction.</figcaption></figure>' + parts[k]
        body_html = "".join(parts)
        meta = f'{esc(p.get("category",""))} · {d.strftime("%-d %B %Y")}{upd} · {mins} min read · By <a href="/about/#founder">{esc(C.FOUNDER["name"])}</a>'
        body = "<article>" + B.banner(c, esc(p["title"]), None, hero_img, credit_of(hero_img), f'<p class="article-meta">{meta}</p>') + f'''
<section class="section--tight"><div class="wrap article-grid"><div class="prose">
{('<div class="keypoints"><h2>Key points</h2><ul>' + kp + '</ul></div>') if kp else ""}
{toc}
{body_html}
<div class="author"><img class="mono" src="/assets/img/philip-chapman-thumb.webp" width="52" height="52" alt="" loading="lazy"><div><b>{esc(C.FOUNDER["name"])}, {esc(C.FOUNDER["role"])}</b><span class="small muted">Founded and ran P Chapman Construction, a £17m UK builder of award-winning homes, for 21 years. Now represents villa owners in Dubai and Abu Dhabi. <a href="/about/#founder">About Philip</a></span></div></div>
{('<h2 id="faq">Questions</h2>' + B.faq_html(faqs)) if faqs else ""}
{('<h2 id="sources">Sources</h2><ol class="small">' + srcs + '</ol>') if srcs else ""}
{guide_cta()}
<p class="small muted" style="margin-top:2em">This article is general information, not advice for your specific project. Figures are from the sources cited and change over time.</p>
</div>
<aside class="article-aside" aria-label="Talk to us"><div class="aside-card">{pic(svc_img_for(p), "", "(max-width:980px) 100vw, 30vw")}<div><h3>Planning a villa in Dubai?</h3><p>Talk it through with Philip. The first conversation is free and confidential.</p><a class="btn" href="/contact/">{esc(B.CTA_LABEL)}</a></div></div>
<div class="aside-links"><b>Services</b>{"".join(f'<a href="/services/{x}/">{esc(SVC[x]["short"])}</a>' for x in ("owners-representative","villa-construction-project-management","villa-renovation-project-management","plot-due-diligence"))}</div></aside>
</div></section></article>
<section class="section paper"><div class="wrap"><h2>Read next</h2>{post_cards(rel)}</div></section>
{B.cta_band()}'''
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "@id": B.url(path) + "#article",
               "headline": p["title"], "description": p["description"], "url": B.url(path),
               "datePublished": d.isoformat(), "dateModified": u.isoformat(), "author": {"@id": B.PERSON_ID},
               "publisher": {"@id": B.ORG_ID}, "mainEntityOfPage": B.url(path), "inLanguage": "en-GB",
               "image": B.url(B.og_image(hero_img)), "wordCount": p["words"],
               "about": p.get("category", ""), "citation": [s["url"] for s in p.get("sources", [])]}
        sch = [art] + ([B.faq_schema(faqs)] if faqs else [])
        B.page(path, p["title"] + (" | Eastbridge" if len(p["title"]) <= 47 else ""), p["description"], body, c, sch, og_type="article",
               og=B.og_image(hero_img))
    # insights/feed.xml is written by build.write_feed()

# ---------------------------------------------------------------- 404, misc
def misc(posts):
    B.page("/404.html", "Page not found | Eastbridge", "This page could not be found.",
           B.page_head([("Home", "/")], "We can't find that page.", "It may have moved. Try the services, our insights, or get in touch.") +
           '<section class="section--tight"><div class="wrap"><p><a class="btn" href="/">Home</a> <a class="btn btn--ghost" href="/services/">Services</a> <a class="btn btn--ghost" href="/contact/">Contact</a></p></div></section>',
           noindex=True)
    # llms.txt and llms-full.txt are written by build.write_llms()

def build_all(posts):
    import pages_new, pages_tools, pages_glossary, pages_guides
    home(posts)
    pages_new.why_page()
    pages_new.case_hub()
    pages_new.case_page()
    services_hub()
    for s in SERVICES: service_page(s)
    areas_hub()
    for a in AREAS: area_page(a)
    work_hub()
    for p in PROJECTS: project_page(p)
    approach(); independence(); fees(); about(); faq_page(); contact(); legal()
    insights(posts)
    pages_tools.build_tools()
    pages_glossary.glossary_page()
    pages_guides.build_all()
    misc(posts)
