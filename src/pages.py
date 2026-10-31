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
    from content.projects import RECOGNITION, ARCHITECTS, TESTIMONIALS
    import pages_new
    rec = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in RECOGNITION[:4])
    arch = "".join(f"<li>{esc(a)}</li>" for a in ARCHITECTS)
    body = B.banner(crumbs, "Homes we built", "Selected work of P Chapman Construction, the company Philip Chapman founded and led for 21 years: private houses, country estates, developments and hotel work.", "owers-house-02", credit_of("owers-house-02")) + f'''
<section class="section--tight"><div class="wrap"><div class="kpis kpis--text">{rec}</div></div></section>
<section class="section--tight"><div class="wrap">{work_cards(PROJECTS)}</div></section>
<section class="section band-dark"><div class="wrap"><div class="head-row"><h2>In our clients' words</h2><p class="muted">Owners and developers on P Chapman Construction.</p></div>{pages_new.quotes_html(TESTIMONIALS[3:6])}</div></section>
<section class="section"><div class="wrap split"><div><h2>Range of work</h2></div><div><p class="muted" style="margin-top:24px">P Chapman Construction worked under traditional and design-and-build contracts, for private owners, developers, hoteliers, schools and housing associations, with particular expertise in contemporary coastal houses and eco-buildings.</p></div></div></section>
{B.cta_band("Bring this standard to your villa.")}'''
    B.page("/work/", "Our Work: Award-Winning Homes by P Chapman Construction",
           "Award-winning private houses, estates, developments and hotel work built by P Chapman Construction, the company Eastbridge founder Philip Chapman led for 21 years.",
           body, crumbs, og=B.og_image("owers-house-02"))

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
    idx = [x["slug"] for x in PROJECTS].index(p["slug"])
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    body = B.banner(crumbs, esc(p["name"]), esc(p["summary"]), imgs[0]["base"], credit) + f'''
<section class="section"><div class="wrap split">
<div><dl class="facts"><div><dt>Location</dt><dd>{esc(p["place"])}</dd></div><div><dt>Project</dt><dd>{esc(p["type"])}</dd></div><div><dt>Built by</dt><dd>P Chapman Construction</dd></div>{('<div><dt>Architect</dt><dd>' + esc(p["architect"]) + '</dd></div>') if p["architect"] else ""}{('<div><dt>Recognition</dt><dd>' + esc(p["recognition"]) + '</dd></div>') if p["recognition"] else ""}</dl>{('<p class="small muted" style="margin-top:14px">Design team: ' + esc(p["team"]) + '</p>') if p["team"] else ""}</div>
<div class="prose">{p["text"]}<h2>Why it matters for a Dubai villa</h2><p>{esc(p["dubai"])}</p></div></div></section>
{video}
<section class="section--tight"><div class="wrap"><div class="gallery">{"".join(figs)}</div><p class="small muted" style="margin-top:12px">{esc(credit)}</p></div></section>
<section class="section paper"><div class="wrap split"><div><p class="muted">Next project</p><h2><a href="/work/{nxt["slug"]}/" style="text-decoration:none">{esc(nxt["name"])}</a></h2><p class="muted">{esc(nxt["type"])}, {esc(nxt["place"])}</p></div>
<a href="/work/{nxt["slug"]}/" aria-hidden="true" tabindex="-1">{pic(nxt["slug"] + "-01", "", "(max-width:880px) 100vw, 58vw")}</a></div></section>
{B.cta_band()}'''
    schema = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": f"{p['name']}, {p['place']}",
               "about": p["type"], "description": p["summary"], "image": [B.url(f"/assets/img/{m['base']}-1280.webp") for m in imgs[:4]],
               "creator": {"@id": B.ORG_ID}, "locationCreated": {"@type": "Place", "name": p["place"]}}]
    B.page(path, f"{p['name']}, {p['place'].replace(', Cornwall', '')} | Eastbridge Work",
           (f"{p['name']}, {p['place']}: {p['summary']} Built by P Chapman Construction." if len(p['summary']) < 105 else f"{p['name']}, {p['place']}: {p['summary']}"),
           body, crumbs, schema, og=B.og_image(imgs[0]["base"]), preload=f"/assets/img/{imgs[0]['base']}-1280.webp")

# ---------------------------------------------------------------- approach / independence / fees / about
def approach():
    crumbs = [("Home", "/"), ("How we work", "/approach/")]
    body = B.banner(crumbs, "How we work", "One programme, one budget, one decision log, and one firm on the project whose only job is your interest.", "polgreen-manor-07", credit_of("polgreen-manor-07")) + f'''
<section class="section dark"><div class="wrap">{stages_html()}</div></section>
<section class="section"><div class="wrap split"><div><h2>The rhythm of a project</h2></div><div class="prose">
<p>Every project runs to the same rhythm, because rhythm is what keeps a two-year build under control.</p>
<h3>Every week</h3><ul><li>A short photo update from site</li><li>Any decisions you need to make, with a recommendation and a deadline</li></ul>
<h3>Every month</h3><ul><li>A written report: progress against programme, cost to complete, risks and issues</li><li>Our recommendation on the contractor's payment application</li><li>A review of variations, approved, rejected or pending</li></ul>
<h3>At every key stage</h3><ul><li>A walk-round with you, in person or by video</li><li>A check that the next stage can start without avoidable risk</li></ul>
<h3>Always</h3><ul><li>A decision log, so nothing you agree is forgotten or reopened</li><li>An issues log with owners and dates</li></ul>
</div></div></section>
<section class="section paper"><div class="wrap split"><div><h2>Who does what</h2></div><div class="prose table-wrap">
<table><thead><tr><th>Party</th><th>Their role</th></tr></thead><tbody>
<tr><td>You, the owner</td><td>Decide, approve and pay. Appoint the consultant and contractor.</td></tr>
<tr><td>Eastbridge</td><td>Represent you: brief, budget, programme, appointments advice, cost control, reporting, variations and claims, handover.</td></tr>
<tr><td>registered consultant</td><td>Statutory design, authority submissions and the supervision duties required by law.</td></tr>
<tr><td>Main contractor</td><td>Build the villa to the contract, manage subcontractors and site safety.</td></tr>
<tr><td>Master developer</td><td>Review the design against the community guidelines and issue NOCs.</td></tr>
<tr><td>Permitting authority</td><td>Dubai Municipality, Trakhees or the Dubai Development Authority depending on your plot; the municipality via TAMM in Abu Dhabi.</td></tr>
</tbody></table>
<p>Read more in <a href="/insights/owners-representative-vs-project-manager-vs-consultant/">owner's representative vs project manager vs consultant</a>.</p></div></div></section>
<section class="section"><div class="wrap split"><div><h2>Why a builder's background matters</h2></div><div class="prose">
<p>Most owner's representatives come from consultancy. Philip came from contracting. For 21 years our founder, Philip Chapman, ran P Chapman Construction, an award-winning premium building company, pricing tenders, running sites, preparing and defending extension of time and variation claims under JCT contracts, and handing over houses to demanding owners and architects.</p>
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
    body = B.banner(crumbs, "Our independence pledge", "In a market where many project managers also design, build or take referral fees, independence has to be written down. This is ours, and it is in every appointment we sign.", "the-lookout-09", credit_of("the-lookout-09")) + f'''
<section class="section"><div class="wrap"><ul class="pledge">{lis}</ul></div></section>
<section class="section paper"><div class="wrap split"><div><h2>Why it matters</h2></div><div class="prose">
<p>When the person checking the contractor's invoices also earns a referral fee from that contractor, the check is not independent. When a design-and-build company's in-house project manager reports to the same owner as the builders, the check is not independent. When a consultant reviews the cost of a design they produced, the check is not independent.</p>
<p>None of these arrangements is necessarily dishonest. They are simply not independent. If you want an independent check, it has to come from someone whose only interest is yours.</p></div></div></section>
{B.cta_band()}'''
    B.page("/independence/", "Independence Pledge: No Contractor Commissions | Eastbridge",
           "Eastbridge is paid only by the client. No commissions, referral fees or rebates from contractors, consultants or suppliers. We don't build and we don't design.",
           body, crumbs)

def fees():
    crumbs = [("Home", "/"), ("How fees work", "/fees/")]
    f = C.FEES
    show = C.PUBLISH_FEES
    def amt(k, fallback):
        return f'<strong>{esc(f[k])}</strong>' if show else fallback
    body = B.banner(crumbs, "How our fees work", "Clear, fixed where possible, and paid only by you. We'd rather tell you the structure up front than surprise you later.", "owers-house-11", credit_of("owers-house-11")) + f'''
<section class="section"><div class="wrap prose table-wrap">
<table><thead><tr><th>Service</th><th>How it's charged</th><th>Typical fee</th></tr></thead><tbody>
<tr><td><a href="/services/plot-due-diligence/">Plot and pre-purchase review</a></td><td>Fixed fee, agreed before we start</td><td>{amt("plot_review", "Fixed, quoted on request")}</td></tr>
<tr><td><a href="/services/stalled-project-rescue/">Stalled project review</a></td><td>Fixed fee for the initial review</td><td>{amt("rescue_review", "Fixed, quoted on request")}</td></tr>
<tr><td>Brief, budget and team appointment</td><td>Fixed fee per stage</td><td>Quoted on the size of the project</td></tr>
<tr><td><a href="/services/owners-representative/">Owner's representation</a> during design and construction</td><td>Monthly fee, or a percentage of construction cost</td><td>{("From " + amt("monthly_from","") + " a month, or " + amt("percent_band","") + " of construction cost") if show else "Quoted on scope, site days and duration"}</td></tr>
<tr><td><a href="/services/snagging-and-handover/">Snagging and handover</a> only</td><td>Fixed fee</td><td>Quoted on the size of the villa</td></tr>
<tr><td><a href="/services/variations-delays-and-claims/">Variations and claims advice</a></td><td>Fixed fee per review, or hourly for negotiations</td><td>Quoted per matter</td></tr>
</tbody></table>
<h2>What's included</h2><ul><li>All our time, reporting and site visits as set out in your appointment</li><li>Travel within Dubai and to Abu Dhabi</li></ul>
<h2>What's not included</h2><ul><li>Fees of the consultant, contractor, surveyors, testing labs or lawyers you appoint; you pay them directly</li><li>Authority and master developer fees</li><li>International travel at your request</li></ul>
<h2>What we never charge</h2><p>We never take commission, referral fees, mark-ups or rebates from anyone on your project. See our <a href="/independence/">independence pledge</a>.</p>
<h2>Is it worth it?</h2><p>On a bespoke villa, one avoided variation dispute, one month of avoided delay or one design change caught before construction typically exceeds our fee. If we don't think your project needs us, we'll say so in the first conversation.</p>
</div></section>
{B.cta_band("Ask for a fee proposal for your project.")}'''
    B.page("/fees/", "Owner's Representative Fees in Dubai: How We Charge | Eastbridge",
           "How we charge for villa owner's representation in Dubai: fixed fees for reviews, monthly or percentage fees in construction, and no commissions.",
           body, crumbs)

def about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    from content.projects import RECOGNITION, ARCHITECTS, TESTIMONIALS
    import pages_new
    rec = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in RECOGNITION[:4])
    arch = "".join(f"<li>{esc(a)}</li>" for a in ARCHITECTS)
    body = B.banner(crumbs, "About Eastbridge", "A client-side practice built on 21 years running an award-winning, £17m-turnover premium building company.", "owers-house-04", credit_of("owers-house-04")) + f'''
<section class="section" id="founder"><div class="wrap feature">
<figure class="portrait">{pic("philip-chapman-01", "Philip Chapman, Founding Partner of Eastbridge Strategic Partners", "(max-width:900px) 100vw, 42vw")}</figure>
<div><span class="kicker">Founding Partner</span><h2>Philip Chapman</h2><p class="muted">British. Based in Dubai.</p><div class="prose">
<p>Philip Chapman founded <a href="{C.FOUNDER["company_uk_url"]}" rel="noopener">P Chapman Construction</a> and led it for 21 years, growing it into a premium contractor with an annual turnover of around £17 million and a reputation for exceptionally demanding private houses built for leading architects.</p>
<p>The company's homes have won a RIBA South West Award and LABC Building Excellence Awards, been reported in The Times and featured on Channel 4's Grand Designs. Alongside one-off houses it delivered country-house restorations, multi-unit developments, hotel and spa work, and schools, under both traditional and design-and-build contracts.</p>
<p>Two decades as the builder meant pricing tenders, programming complex sites, managing subcontractors, administering JCT contracts, preparing and defending extension of time and variation claims, and handing finished homes to owners and architects who expected them to be perfect. It also meant seeing, from the inside, exactly where owners lose money and time.</p>
<p>In Dubai and Abu Dhabi, Philip works on the other side of the table: for the owner, never the builder. He leads every Eastbridge appointment personally and is the person you speak to from the first conversation to handover.</p>
<p>Away from work he is a high-altitude mountaineer, which may explain a fondness for planning, contingency and getting everyone home safely.</p>
</div></div></div></section>
<section class="section--tight"><div class="wrap"><div class="kpis kpis--text">{rec}</div></div></section>
<section class="section band-dark"><div class="wrap"><div class="head-row"><h2>What clients said about the work</h2><p class="muted">Clients of P Chapman Construction.</p></div>{pages_new.quotes_html(TESTIMONIALS[:3])}</div></section>
<section class="section stone"><div class="wrap split"><div><h2>Why the client's side</h2></div><div class="prose">
<p>Dubai and Abu Dhabi are building some of the most ambitious private homes in the world. The owners commissioning them are often busy, frequently abroad and rarely builders themselves. The market around them is full of capable firms, but few that act only for the owner and take nothing from anyone else.</p>
<p>That is the gap we fill. We bring the builder's knowledge to the owner's side, and we keep it there. <a href="/why-a-client-side-project-manager/">Why it matters</a>.</p></div></div></section>
<section class="section"><div class="wrap split"><div><h2>Plainly stated</h2></div><div class="prose">
<ul>
<li>We are {esc(C.LEGAL)}, licensed in the Meydan Free Zone, Dubai ({esc(C.LICENCE.split("licence ")[-1])}).</li>
<li>We are a client-side project manager and owner's representative. We are not a contractor, an engineering consultancy, a law firm or an estate agency.</li>
<li>We are paid only by our clients. See our <a href="/independence/">independence pledge</a>.</li>
</ul></div></div></section>
{B.cta_band()}'''
    B.page("/about/", "About Eastbridge and Founder Philip Chapman | Dubai",
           "Eastbridge is led by Philip Chapman, who built P Chapman Construction into an award-winning £17m premium contractor over 21 years. Now he works only for villa owners.",
           body, crumbs, [B.person_schema()], og=B.og_image("owers-house-02"))

# ---------------------------------------------------------------- faq / contact / legal
FAQ_ALL = [
 ("What is an owner's representative?", "An owner's representative is a professional who acts only for the person paying for a building project. On a villa, we set the budget and programme, help appoint the consultant and contractor, control cost and time, report progress, handle variations and claims, and lead handover."),
 ("Do I need an owner's representative to build a villa in Dubai?", "It isn't required by law. It is most valuable on bespoke villas, major renovations, and projects where the owner is often abroad or has not built before. We will tell you honestly if you don't need us."),
 ("How is that different from the consultant I have to appoint?", "In Dubai, a registered consultant carries the statutory design, submission and supervision responsibilities. They work for the project's compliance and design. We work only for you, alongside them, on cost, time, decisions, contracts and quality."),
 ("Do you take commission from contractors?", "Never. We are paid only by you. See our <a href=\"/independence/\">independence pledge</a>."),
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
    opts = "".join(f'<label><input type="checkbox" name="stage" value="{v}"> {v}</label>' for v in
                   ["Considering a plot", "Plot bought", "In design", "Choosing a contractor", "Under construction", "Renovation", "Stalled or in dispute", "Near handover"])
    areas = "".join(f'<option>{esc(a["name"])}</option>' for a in AREAS) + "<option>Elsewhere in Dubai</option><option>Elsewhere in Abu Dhabi</option>"
    body = B.banner(crumbs, "Start a private brief", "Tell us a little about your project. Philip will reply personally within one working day. Nothing you send is shared or published.", "the-lookout-02", credit_of("the-lookout-02")) + f'''
<section class="section--tight"><div class="wrap split">
<div><h2 style="font-size:var(--step-2)">Prefer to talk?</h2>
<p><a class="btn" href="{B.wa_link()}" rel="noopener">Message us on WhatsApp</a></p>
<p>Call <a href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a><br>Email <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
<p class="muted small">{esc(C.HOURS)}. UK and European clients are welcome to book calls in their own time zone.</p>
<h2 style="font-size:var(--step-2);margin-top:2em">What happens next</h2>
<ol class="small"><li>We read your brief and reply within one working day.</li><li>A free first conversation, usually 30–45 minutes, to understand the project.</li><li>If we can help, a written proposal with a clear scope and fee. If we can't, we'll say so and, where we can, point you to someone who can.</li></ol>
</div>
<form class="form" name="brief" method="POST" action="/contact/thanks/" data-netlify="true" netlify-honeypot="company_site" data-enquiry>
<input type="hidden" name="form-name" value="brief">
<p class="hp"><label>Leave this empty <input name="company_site"></label></p>
<div class="row"><div><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div></div>
<div class="row"><div><label for="f-phone">Phone or WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
<div><label for="f-area">Where is the project?</label><select id="f-area" name="area"><option value="">Choose a location</option>{areas}</select></div></div>
<fieldset><legend>Where are you now?</legend><div class="checks">{opts}</div></fieldset>
<div class="row"><div><label for="f-budget">Approximate construction budget</label><select id="f-budget" name="budget"><option value="">Choose a range</option><option>Under AED 3m</option><option>AED 3m–8m</option><option>AED 8m–20m</option><option>AED 20m–50m</option><option>Over AED 50m</option><option>Not sure yet</option></select></div>
<div><label for="f-based">Where are you based?</label><select id="f-based" name="based"><option value="">Choose</option><option>UAE</option><option>United Kingdom</option><option>Europe</option><option>GCC</option><option>Elsewhere</option></select></div></div>
<div><label for="f-msg">Tell us about the project</label><textarea id="f-msg" name="message" required></textarea><p class="hint">The house you want, the plot or villa you have, and anything that's worrying you.</p></div>
<p class="small muted">By sending this you agree to our <a href="/privacy/">privacy notice</a>. We use your details only to reply to you.</p>
<p><button class="btn" type="submit">Send your brief</button></p>
</form></div></section>'''
    schema = [{"@context": "https://schema.org", "@type": "ContactPage", "url": B.url("/contact/"), "about": {"@id": B.ORG_ID}}]
    B.page("/contact/", "Contact Eastbridge: Start a Private Villa Project Brief | Dubai",
           "Start a confidential brief for your villa build or renovation in Dubai or Abu Dhabi. A senior reply within one working day, by email, phone or WhatsApp.",
           body, crumbs, schema)
    B.page("/contact/thanks/", "Thank you | Eastbridge", "Your brief has been received.",
           B.page_head([("Home", "/"), ("Contact", "/contact/"), ("Thank you", "/contact/thanks/")], "Thank you. Your brief is with us.",
                       "Philip will reply personally within one working day. If it's urgent, message us on WhatsApp.") +
           f'<section class="section--tight"><div class="wrap"><p><a class="btn" href="{B.wa_link()}">Message us on WhatsApp</a> <a class="btn btn--ghost" href="/insights/">Read our insights</a></p></div></section>',
           noindex=True)

def legal():
    crumbs = [("Home", "/"), ("Privacy", "/privacy/")]
    body = B.page_head(crumbs, "Privacy notice", None) + f'''<section class="section--tight"><div class="wrap prose">
<p>Last updated {datetime.date.today().strftime("%-d %B %Y")}.</p>
<p>{esc(C.LEGAL)} ("Eastbridge", "we") is licensed in the Meydan Free Zone, Dubai ({esc(C.LICENCE)}). This notice explains how we handle personal data collected through this website, consistent with the UAE Personal Data Protection Law (Federal Decree-Law No. 45 of 2021) and, for visitors in the UK and EU, the UK and EU GDPR.</p>
<h2>What we collect</h2><p>Details you send us through the enquiry form, email, phone or WhatsApp: your name, contact details, information about your project and anything else you choose to share. If analytics are enabled, we also collect anonymised usage data (pages visited, device type, approximate location) through Google Analytics with IP anonymisation.</p>
<h2>How we use it</h2><p>Only to reply to your enquiry, to prepare a proposal if you ask for one, and to deliver our services if you appoint us. We do not sell your data or use it for unrelated marketing.</p>
<h2>Who we share it with</h2><p>Our website host (Netlify) and email provider, which process data on our behalf. We share project information with third parties, such as a consultant or contractor, only with your agreement.</p>
<h2>How long we keep it</h2><p>Enquiries that don't lead to an appointment are deleted after 24 months. Client records are kept for the period required by law and our professional indemnity insurers.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your data, or object to how we use it, by emailing <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p>
<h2>Cookies</h2><p>This site uses no advertising cookies. If analytics are enabled, Google Analytics sets cookies to measure use of the site.</p>
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
<div class="author"><img class="mono" src="/assets/img/philip-chapman-thumb.webp" width="52" height="52" alt="" loading="lazy"><div><b>{esc(C.FOUNDER["name"])}, {esc(C.FOUNDER["role"])}</b><span class="small muted">Founded and ran P Chapman Construction, an award-winning £17m premium builder, for 21 years. Now represents villa owners in Dubai and Abu Dhabi. <a href="/about/#founder">About Philip</a></span></div></div>
{('<h2 id="faq">Questions</h2>' + B.faq_html(faqs)) if faqs else ""}
{('<h2 id="sources">Sources</h2><ol class="small">' + srcs + '</ol>') if srcs else ""}
<p class="small muted" style="margin-top:2em">This article is general information, not advice for your specific project. Figures are from the sources cited and change over time.</p>
</div>
<aside class="article-aside" aria-label="Talk to us"><div class="aside-card">{pic(svc_img_for(p), "", "(max-width:980px) 100vw, 30vw")}<div><h3>Planning a villa in Dubai?</h3><p>Talk it through with Philip. The first conversation is free and confidential.</p><a class="btn" href="/contact/">Start a private brief</a></div></div>
<div class="aside-links"><b>Services</b>{"".join(f'<a href="/services/{x}/">{esc(SVC[x]["short"])}</a>' for x in ("owners-representative","villa-construction-project-management","villa-renovation-project-management","plot-due-diligence"))}</div></aside>
</div></section></article>
<section class="section paper"><div class="wrap"><h2>Read next</h2>{post_cards(rel)}</div></section>
{B.cta_band()}'''
        art = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["description"],
               "datePublished": d.isoformat(), "dateModified": u.isoformat(), "author": {"@id": B.PERSON_ID},
               "publisher": {"@id": B.ORG_ID}, "mainEntityOfPage": B.url(path), "inLanguage": "en-GB",
               "image": B.url(B.og_image(hero_img)), "wordCount": p["words"],
               "about": p.get("category", ""), "citation": [s["url"] for s in p.get("sources", [])]}
        sch = [art] + ([B.faq_schema(faqs)] if faqs else [])
        B.page(path, p["title"] + (" | Eastbridge" if len(p["title"]) <= 52 else ""), p["description"], body, c, sch, og_type="article",
               og=B.og_image(hero_img))
    # RSS
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{B.url('/insights/' + p['slug'] + '/')}</link><guid>{B.url('/insights/' + p['slug'] + '/')}</guid><pubDate>{format_datetime(datetime.datetime.combine(datetime.date.fromisoformat(str(p['date'])), datetime.time(6, 0), tzinfo=datetime.timezone.utc))}</pubDate><description>{esc(p['description'])}</description></item>" for p in posts)
    (B.DIST / "insights").mkdir(parents=True, exist_ok=True)
    (B.DIST / "insights/feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Eastbridge Insights</title><link>{B.url("/insights/")}</link><description>Guides for villa owners in Dubai and Abu Dhabi.</description><language>en-gb</language>{items}</channel></rss>', encoding="utf-8")

# ---------------------------------------------------------------- 404, llms.txt, misc
def misc(posts):
    B.page("/404.html", "Page not found | Eastbridge", "This page could not be found.",
           B.page_head([("Home", "/")], "We can't find that page.", "It may have moved. Try the services, our insights, or get in touch.") +
           '<section class="section--tight"><div class="wrap"><p><a class="btn" href="/">Home</a> <a class="btn btn--ghost" href="/services/">Services</a> <a class="btn btn--ghost" href="/contact/">Contact</a></p></div></section>',
           noindex=True)
    lines = [f"# {C.NAME}", "",
             "> Independent, client-side owner's representative and villa project management for private clients building or renovating villas in Dubai and Abu Dhabi. Founded by a builder who ran a premium UK residential construction company for 21 years. Paid only by the client; no contractor commissions. Not a contractor or engineering consultancy: works alongside the client's registered consultant.", "",
             f"- Contact: {C.EMAIL}, {C.PHONE_DISPLAY} (WhatsApp available)",
             f"- Legal entity: {C.LEGAL}, {C.LICENCE}", "- Serves: Dubai and Abu Dhabi, UAE; many villa owners live in the UK and Europe",
             f"- Founder: {C.FOUNDER['name']}, who founded and led P Chapman Construction (UK premium residential contractor) for 21 years: {B.url('/about/#founder')}",
             "- Portfolio: homes built by P Chapman Construction (UK), the contractor founded and led by Philip Chapman; awards include a RIBA South West Award (2016) and LABC Building Excellence Awards (2018, 2020); a home featured on Channel 4's Grand Designs", f"- Case study: {B.url('/case-studies/island-e-waterfront-villa/')} (illustrative, modelled scenario)", "",
             "## Services"] + [f"- [{s['name']}]({B.url('/services/' + s['slug'] + '/')}): {s['description']}" for s in SERVICES] + \
            ["", "## Areas"] + [f"- [{a['name']}]({B.url('/areas/' + a['slug'] + '/')}): {a['tag']}; master developer {a['developer']}" for a in AREAS] + \
            ["", "## Guides"] + [f"- [{p['title']}]({B.url('/insights/' + p['slug'] + '/')}): {p['description']}" for p in posts] + \
            ["", "## About", f"- [About]({B.url('/about/')})", f"- [How we work]({B.url('/approach/')})", f"- [Independence pledge]({B.url('/independence/')})", f"- [Fees]({B.url('/fees/')})", f"- [FAQ]({B.url('/faq/')})"]
    import pages_glossary
    lines += pages_glossary.llms_lines()
    (B.DIST / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

def build_all(posts):
    import pages_new, pages_glossary
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
    pages_glossary.glossary_page()
    misc(posts)
