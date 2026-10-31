"""Home page, 'why client-side' page and case studies."""
import html as H
import build as B
import config as C
from content.services import SERVICES, BY_SLUG as SVC
from content.areas import AREAS
from content.projects import PROJECTS, BY_SLUG as PROJ, RECOGNITION, ARCHITECTS, TESTIMONIALS
import content.case_island_e as CS

esc = H.escape
pic = B.picture

def proj_of(base):
    return PROJ[base.rsplit("-", 1)[0]]

def credit_of(base):
    p = proj_of(base)
    return f'{p["name"]}, {p["place"]}' + (f' · photograph {p["photo"]}' if p["photo"] else "")

# ---------------------------------------------------------------- shared components
def creds_band():
    items = [("21 years", "building premium homes as P Chapman Construction"),
             ("£17m", "annual turnover at the company's peak, about AED 80m"),
             ("RIBA South West Award", "Owers House, 2016"),
             ("LABC Building Excellence", "award winner 2018, highly commended 2020"),
             ("Grand Designs", "a P Chapman Construction home featured on Channel 4")]
    return '<section class="creds" aria-label="Track record"><div class="wrap">' + "".join(
        f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in items) + "</div></section>"

def triad_svg():
    nodes = [  # x, y, title, line2
        (120, 70, "Architect and consultant", "Paid to design and to meet the code"),
        (520, 70, "Contractor", "Paid on price, variations and claims"),
        (120, 350, "Interior designer", "Paid to specify the finish"),
        (520, 350, "Developer and authority", "Protect the community and the rules"),
    ]
    g = ['<svg class="triad" viewBox="0 0 640 420" role="img" aria-label="Everyone on a villa project has their own interest. The owner sits at the centre; Eastbridge sits beside the owner and works only for them.">']
    for x, y, *_ in nodes:
        g.append(f'<path class="edge" d="M320 200 L{x} {y}"/>')
    g.append('<path class="edge-eb" d="M320 254 L320 300"/>')
    for x, y, t, s in nodes:
        g.append(f'<rect class="node" x="{x-105}" y="{y-30}" width="210" height="60"/>'
                 f'<text x="{x}" y="{y-4}" text-anchor="middle">{esc(t)}</text>'
                 f'<text x="{x}" y="{y+16}" text-anchor="middle" class="t-small">{esc(s)}</text>')
    g.append('<circle class="node-you" cx="320" cy="200" r="54"/><text x="320" y="196" text-anchor="middle" class="t-inv">You,</text><text x="320" y="214" text-anchor="middle" class="t-inv">the owner</text>')
    g.append('<rect class="node-eb" x="255" y="300" width="130" height="44"/><text x="320" y="327" text-anchor="middle" class="t-inv">Eastbridge</text>')
    g.append('<text x="320" y="410" text-anchor="middle" class="t-small">Eastbridge: paid only by you, working only for you.</text>')
    g.append("</svg>")
    return "".join(g)

COMPARE = [
 ("A budget that is a hope, set before anyone has priced the risk", "A budget built from cost per square foot, the plot rules and a contingency you hold"),
 ("A design that grows until the tender comes back over budget", "A cost check at every design stage, so the drawings never outrun the money"),
 ("Bids compared on the headline number", "Bids put on a like-for-like basis: exclusions, provisional sums, preliminaries, programme"),
 ("Payments approved from a photograph", "Every payment measured against the work actually on site"),
 ("Variations agreed on site, priced later", "Every change priced and its time effect stated before you instruct it"),
 ("Delay claims answered with opinion", "Records kept from day one, so claims are answered with facts"),
 ("A snag list that drags on for months", "Handover planned from the start; retention released only when earned"),
]

def compare_html(rows=COMPARE):
    a = "".join(f"<li>{esc(x)}</li>" for x, _ in rows)
    b = "".join(f"<li>{esc(y)}</li>" for _, y in rows)
    return (f'<div class="compare"><div class="without"><h3>Without someone on your side</h3><ul>{a}</ul></div>'
            f'<div class="with"><h3>With Eastbridge</h3><ul>{b}</ul></div></div>')

EVIDENCE = [
 ("31%", "of construction projects finished within 10% of budget, in KPMG's Global Construction Survey"),
 ("1 in 4", "finished within 10% of the original deadline, in the same survey"),
 ("2025", "the year Dubai Municipality formally warned villa consultancies about over-designing villas and inflating build costs"),
]

def evidence_html():
    return '<div class="stat-big">' + "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in EVIDENCE) + "</div>"

def quotes_html(items):
    return '<div class="quotes">' + "".join(
        f'<figure><blockquote>&ldquo;{esc(q)}&rdquo;</blockquote><figcaption>{esc(who)}, {esc(where)}<br><span class="muted">Client of P Chapman Construction</span></figcaption></figure>'
        for q, who, where in items) + "</div>"

def svc_cards(items, imgs):
    return '<div class="svc-grid">' + "".join(
        f'<a class="svc-card" href="/services/{s["slug"]}/"><figure>{pic(imgs[s["slug"]][0], "", "(max-width:600px) 100vw, (max-width:980px) 50vw, 33vw", cls="reveal")}</figure>'
        f'<h3>{esc(s["short"])}</h3><p>{esc(s["lede"])}</p></a>' for s in items) + "</div>"

# ---------------------------------------------------------------- home
HERO_SLIDES = ["quay-house-01", "owers-house-01", "sea-glass-house-01", "the-lookout-02"]

def home(posts, post_cards, stages_html, svc_img):
    slides = "".join(f'<figure>{pic(b, "", "100vw", eager=(i == 0))}</figure>' for i, b in enumerate(HERO_SLIDES))
    doors = [
     ("villa-construction-project-management", "Build a new villa", "From the plot and the first budget to the day you move in.", "sea-glass-house-02"),
     ("villa-renovation-project-management", "Renovate or extend", "Palm Jumeirah, Emirates Hills, Dubai Hills. Approvals, budget, contractor and handover.", "menwinnion-01"),
     ("stalled-project-rescue", "Rescue a stalled build", "Over budget, behind programme or in dispute. We find out where it stands and get it finished.", "polgreen-manor-01"),
    ]
    door_html = "".join(f'<a class="door" href="/services/{s}/">{pic(img, "", "(max-width:900px) 100vw, 33vw")}<div><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="go">How we help</span></div></a>' for s, t, d, img in doors)
    mosaic_items = [("m1", "quay-house-02"), ("m2", "owers-house-09"), ("m3", "the-lookout-03"), ("m4", "saqqara-06"),
                    ("m5", "sea-glass-house-04"), ("m6", "gooden-heane-01"), ("m7", "polgreen-manor-03"), ("m8", "st-michaels-02")]
    mosaic = "".join(f'<a class="{c}" href="/work/{proj_of(b)["slug"]}/">{pic(b, proj_of(b)["name"] + ", " + proj_of(b)["place"], "(max-width:760px) 100vw, 58vw")}<span>{esc(proj_of(b)["name"])}, {esc(proj_of(b)["place"])}</span></a>' for c, b in mosaic_items)
    arch = "".join(f"<li>{esc(a)}</li>" for a in ARCHITECTS[:6])
    areas = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["name"])}</a><span>{esc(a["tag"])}</span></li>' for a in AREAS)
    faqs = [
     ("What does a client-side project manager do?", "We run your villa build or renovation on your behalf. We set the budget and programme with you, help you choose and appoint the architect, consultant and contractor, check the design against the budget, monitor cost, time and quality on site, review every payment and variation, and lead handover. We are paid only by you."),
     ("Why not leave it to the architect or the contractor?", "Both are essential, and both have their own commercial interest. The architect is paid to design; the contractor is paid on the price, variations and claims. Neither is paid to protect your budget. <a href=\"/why-a-client-side-project-manager/\">Why client-side matters</a>."),
     ("Who is behind Eastbridge?", "Philip Chapman, who founded and ran P Chapman Construction for 21 years, building award-winning private homes, estates, developments and hotel work. <a href=\"/about/\">About Philip</a>."),
     ("Do you replace the registered consultant?", "No. Your villa needs a registered consultant for the statutory design, permits and supervision duties. We help you choose them and make sure they, and the contractor, deliver what you are paying for."),
     ("How are you paid?", "Only by you. We take no commission, referral fee or discount from any contractor, consultant or supplier. See <a href=\"/fees/\">how fees work</a>."),
    ]
    k = CS
    body = f'''
<section class="hero" aria-labelledby="hero-h"><div class="slides">{slides}</div>
<div class="hero-video" data-src="https://player.vimeo.com/video/219974514?background=1&amp;autoplay=1&amp;loop=1&amp;muted=1&amp;dnt=1"></div>
<div class="wrap"><span class="kicker">Client-side project management · Dubai and Abu Dhabi</span>
<h1 id="hero-h">Your villa, managed from your side of the table.</h1>
<p class="lede">An independent project manager, paid only by you. We set the budget, help you choose the team, check every payment and claim, and get you the keys on time. Led personally by Philip Chapman, who built award-winning homes for 21 years.</p>
<div class="actions"><a class="btn" href="/contact/">Start a private brief</a><a class="btn btn--ghost" href="/why-a-client-side-project-manager/">Why client-side matters</a></div></div>
<p class="hero-meta">Homes built by P Chapman Construction, founded by Philip Chapman.</p><span class="scroll-cue" aria-hidden="true"></span></section>
{creds_band()}

<section class="section" aria-labelledby="what-h"><div class="wrap">
<div class="head-row"><h2 id="what-h">What we do</h2>
<p class="lede">A client-side project manager, also called an owner's representative, runs your build for you. We don't design and we don't build, and we are paid only by you, so our one job is to deliver the house you want, for the budget you set, when you were promised it.</p></div>
<div class="doors">{door_html}</div>
<p style="margin-top:30px"><a class="link" href="/services/">All services</a> &nbsp; <a class="link" href="/approach/">How a project runs</a></p>
</div></section>

<section class="section stone" aria-labelledby="why-h"><div class="wrap">
<div class="split" style="align-items:center">
<div><span class="kicker">Why client-side</span><h2 id="why-h">Everyone on your project is good at their job. Only one of them is paid to protect your money.</h2>
<p class="muted">The architect is paid to design. The contractor is paid on the price, the variations and the claims. The developer and the authority protect the community and the rules. All of that is legitimate. None of it is your budget. That is the gap a client-side project manager fills.</p>
<p><a class="btn" href="/why-a-client-side-project-manager/">Why it pays for itself</a></p></div>
<div>{triad_svg()}</div></div>
<div style="margin-top:clamp(56px,7vw,96px)">{evidence_html()}</div>
<p class="small muted" style="margin-top:18px">Sources: KPMG International, Global Construction Survey 2015, reported by Building Design + Construction; Gulf News, August 2025.</p>
</div></section>

<section class="section band-dark" aria-labelledby="case-h"><div class="wrap case-feature">
<div><span class="kicker">Illustrative case study</span><h2 id="case-h">An Island E waterfront villa, from plot to keys</h2>
<p class="muted">How we would run a villa on one of Nakheel's new Island E plots, worked through with real plot rules and published Dubai costs: the plot review, the brief, the design brought back to budget, the bids, the claims and the handover.</p>
<div class="stat-big" style="margin:34px 0">
<div><b>AED {k.AVOIDED_TOTAL:.2f}m</b><span>of cost avoided against the first numbers on the table</span></div>
<div><b>AED {k.UNDER:.2f}m</b><span>under the approved budget at final account</span></div>
<div><b>4 weeks</b><span>extension of time agreed, against 11 weeks claimed</span></div></div>
<p><a class="btn" href="/case-studies/island-e-waterfront-villa/">Read the case study</a></p>
<p class="small muted" style="margin-top:14px">A modelled scenario, not a real client. Figures explained in full on the page.</p></div>
<figure class="chart-dark">{CS.svg_site()}<figcaption>Indicative plot plan and section within Nakheel's draft controls: basement, ground and two upper floors, 12.5 m maximum height.</figcaption></figure>
</div></section>

<section class="section" aria-labelledby="work-h"><div class="wrap">
<div class="head-row"><div><span class="kicker">Selected work</span><h2 id="work-h">Built by P Chapman Construction</h2></div>
<p class="muted">A selection from 21 years of private houses, country estates, developments and hotel work, built to the most exacting standards. It is the standard we hold every project to.</p></div>
<div class="mosaic">{mosaic}</div>
<p style="margin-top:clamp(36px,4vw,56px)"><a class="btn btn--ghost" href="/work/">See the work</a></p>
</div></section>

<section class="section band-dark" aria-labelledby="quotes-h"><div class="wrap">
<div class="head-row"><h2 id="quotes-h">In our clients' words</h2><p class="muted">Owners and developers on P Chapman Construction. The same standards now apply on the client's side.</p></div>
{quotes_html(TESTIMONIALS[:3])}
</div></section>

<section class="section" aria-labelledby="founder-h"><div class="wrap feature">
<figure class="portrait">{pic("philip-chapman-01", "Philip Chapman, Founding Partner of Eastbridge Strategic Partners", "(max-width:900px) 100vw, 42vw", cls="reveal")}</figure>
<div><span class="kicker">Founding Partner</span><h2 id="founder-h">Philip Chapman</h2>
<p>Philip founded P Chapman Construction and led it for 21 years, growing it into a premium contractor with an annual turnover of around £17 million. His company's homes have won RIBA and LABC awards, been reported in The Times and featured on Grand Designs.</p>
<p class="muted">He knows how a contractor prices a job, where variations come from and how delay claims are built, because for two decades that was his business. In Dubai and Abu Dhabi he works only for the owner, and leads every Eastbridge appointment personally.</p>
<p><a class="link" href="/about/">About Philip and Eastbridge</a></p></div>
</div></section>

<section class="section dark" aria-labelledby="stages-h"><div class="wrap">
<div class="head-row"><h2 id="stages-h">Plot to keys, in six stages</h2>
<p class="muted">Join us at any stage. The earlier we start, the more of the budget we protect, because most of the outcome is decided before anything is built.</p></div>
{stages_html()}
</div></section>

<section class="section" aria-labelledby="svc-h"><div class="wrap">
<div class="head-row"><h2 id="svc-h">The whole project, or the part you need</h2>
<p class="muted">Independent and paid only by you. <a class="link" href="/independence/">Our independence pledge</a></p></div>
{svc_cards([SVC[s] for s in ("owners-representative","plot-due-diligence","design-and-approvals","consultant-and-contractor-selection","site-visits-and-reporting","snagging-and-handover")], svc_img)}
</div></section>

<section class="section stone" aria-labelledby="areas-h"><div class="wrap">
<div class="head-row"><h2 id="areas-h">Where we work</h2><p class="muted">Each community has its own master developer, design rules and practical constraints.</p></div>
<ul class="area-list">{areas}</ul></div></section>

<section class="section" aria-labelledby="ins-h"><div class="wrap">
<div class="head-row"><h2 id="ins-h">Insights</h2><p class="muted">Straight answers for villa owners, written from the builder's side. <a class="link" href="/insights/">All insights</a></p></div>
{post_cards(posts[:3])}
</div></section>

<section class="section--tight" aria-labelledby="hfaq-h"><div class="wrap split"><h2 id="hfaq-h">Questions</h2>{B.faq_html(faqs)}</div></section>
{B.cta_band("Tell us about the house you want to build.", image="sea-glass-house-08")}'''
    B.page("/", "Villa Project Management Dubai | Client-Side Project Manager",
           "Client-side project management for villa builds and renovations in Dubai and Abu Dhabi, led by Philip Chapman, 21 years building award-winning homes. Paid only by you.",
           body, schema=[B.faq_schema(faqs)], preload="/assets/img/quay-house-01-1280.webp", hero=True)

# ---------------------------------------------------------------- why client-side
MOMENTS = [
 ("Before you buy the plot", "What the rules let you build, what it will really cost and what the purchase commits you to."),
 ("Writing the brief", "Turning a wish list into rooms, sizes and finishes that fit the plot and the budget."),
 ("Choosing the architect and consultant", "Fee proposals compared like-for-like, so nothing is missing from the scope you pay for."),
 ("At every design stage", "A cost check before each stage is signed off. Over-design is cheapest to fix on paper."),
 ("Comparing contractor bids", "Exclusions, provisional sums, preliminaries and programme put on an equal footing."),
 ("Every month on site", "Payments measured against the work actually done, and progress against the real critical path."),
 ("Every change and every claim", "Variations priced before they are instructed; delay claims tested against the records."),
 ("Handover", "Commissioning witnessed, snags closed and documents collected before retention is released."),
]

def why_page():
    path = "/why-a-client-side-project-manager/"
    crumbs = [("Home", "/"), ("Why client-side", path)]
    moments = "".join(f"<li><b>{esc(t)}</b><span>{esc(d)}</span></li>" for t, d in MOMENTS)
    faqs = [
     ("Isn't the architect supposed to protect my budget?", "A good architect will design to a budget if asked, but their job is the design, and design fees are often a percentage of construction cost. In August 2025 Dubai Municipality formally warned villa consultancies about over-designing villas and inflating build costs. An independent cost check at every design stage is the protection."),
     ("Doesn't the registered consultant supervise the contractor?", "The consultant of record carries statutory supervision duties: that the building is built to the approved design and the code. That is not the same as checking every payment, pricing every variation, testing delay claims or managing your programme and budget. We do that, alongside them."),
     ("Will good contractors resent an owner's project manager?", "In our experience the opposite. Good contractors prefer an informed client: decisions are made on time, information arrives when it should and payments are made promptly for work done. The contractors who dislike scrutiny are the ones you most need it with."),
     ("When is it too late to bring you in?", "It is never too late to help, but the earlier the better. Most of a project's cost is fixed by the brief, the design and the contract. We also take on projects that have stalled or are in dispute."),
     ("What does it cost?", "Fixed fees for plot reviews and early stages, then a monthly or percentage fee during construction. See <a href=\"/fees/\">how fees work</a>. On a bespoke villa, one avoided variation dispute or one month of avoided delay usually covers the fee for that stage."),
    ]
    body = B.banner(crumbs, "Why a client-side project manager pays for itself",
                    "On a private villa, everyone at the table is good at their job. Only one of them is paid to look after your money.",
                    "quay-house-02", credit_of("quay-house-02")) + f'''
<section class="section"><div class="wrap split" style="align-items:center">
<div><h2>The gap in every villa project</h2>
<p>A private villa in Dubai brings together a master developer, a permitting authority, an architect, a registered consultant, a main contractor, specialist subcontractors and an interior designer. Each is competent. Each has their own commercial interest, and that is how it should be.</p>
<p>The result is a project in which nobody's only job is the owner's budget, programme and quality. Owners fill the gap themselves, between their own work and family, often from another country. That is how good projects drift: a loose brief, a design that grows, a bid that looked cheapest, a payment made ahead of the work, a claim answered with opinion.</p>
<p>A client-side project manager closes the gap. We sit beside you, paid only by you, and make sure everyone else delivers what you are paying for.</p></div>
<figure>{triad_svg()}<figcaption>We don't replace anyone on your team. We make sure the team works for you.</figcaption></figure>
</div></section>

<section class="section stone"><div class="wrap">
<div class="head-row"><h2>The numbers behind it</h2><p class="muted">Construction overruns are the norm, not the exception. These figures come from a global survey of project owners and from Dubai's own regulator.</p></div>
{evidence_html()}
<p class="small muted" style="margin-top:18px">Sources: KPMG International, <a href="https://bdcnetwork.com/too-many-construction-projects-dont-meet-owners-expectations-kpmg-report" rel="noopener">Global Construction Survey 2015</a> (109 senior owners); <a href="https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704" rel="noopener">Gulf News, August 2025</a>.</p>
</div></section>

<section class="section"><div class="wrap">
<div class="head-row"><h2>The same project, two ways</h2><p class="muted">What owners typically experience without someone on their side, and what changes when they have one.</p></div>
{compare_html()}
</div></section>

<section class="section band-dark"><div class="wrap feature">
<figure>{pic("polgreen-manor-05", "Polgreen Manor, slate roofs and rooflights joining old and new buildings", "(max-width:900px) 100vw, 58vw")}<figcaption>Polgreen Manor, Mawgan Porth. LABC Building Excellence Awards 2020, Highly Commended.</figcaption></figure>
<div><span class="kicker">Why us</span><h2 class="statement">For 21 years Philip was the builder. He knows where the money goes.</h2>
<p class="muted">Most project managers come from consultancy. Philip came from contracting. Philip Chapman spent two decades pricing tenders, running sites, preparing and defending extension of time claims and handing over award-winning homes. On your side of the table, that knowledge is hard to replace.</p>
<p><a class="btn" href="/about/">About Philip</a></p></div></div></section>

<section class="section"><div class="wrap">
<div class="head-row"><h2>Eight moments where it pays for itself</h2><p class="muted">In the order they arrive on a villa project. Miss the early ones and the later ones get more expensive.</p></div>
<ol class="moments">{moments}</ol>
</div></section>

<section class="section stone"><div class="wrap split">
<div><h2>The arithmetic</h2></div>
<div class="prose">
<p>On a villa with a construction budget of AED 15 million, a 10% overrun costs AED 1.5 million. A three-month delay costs rent or hotel bills, financing and, often, a summer the family had planned around the move.</p>
<p>Against that, a client-side project manager is a modest, predictable cost that is set in advance. Our <a href="/case-studies/island-e-waterfront-villa/">illustrative Island E case study</a> works through a waterfront villa line by line: AED {CS.AVOIDED_TOTAL:.2f} million of cost avoided against the first numbers on the table, a final account AED {CS.UNDER:.2f} million under the approved budget, and an 11-week delay claim held to four weeks.</p>
<p>We will also tell you when you don't need us. On a simple renovation with an experienced owner living in Dubai, the numbers may not justify it, and we will say so.</p>
</div></div></section>

<section class="section"><div class="wrap split"><h2>Questions</h2>{B.faq_html(faqs)}</div></section>
{B.cta_band("See where your project stands.", "Send us your plot number, your drawings or your contractor's latest valuation. The first conversation is free.", "owers-house-04")}'''
    article = {"@context": "https://schema.org", "@type": "Article", "headline": "Why a client-side project manager pays for itself",
               "author": {"@id": B.PERSON_ID}, "publisher": {"@id": B.ORG_ID}, "mainEntityOfPage": B.url(path),
               "image": B.url(B.og_image("quay-house-02")), "inLanguage": "en-GB"}
    B.page(path, "Why Use a Client-Side Project Manager for a Dubai Villa",
           "Why a client-side project manager pays for itself on a Dubai villa: who on your project protects your budget, the evidence on overruns, and the moments that matter.",
           body, crumbs, [B.faq_schema(faqs), article], og=B.og_image("quay-house-02"))

# ---------------------------------------------------------------- case studies
def case_hub():
    path = "/case-studies/"
    crumbs = [("Home", "/"), ("Case study", path)]
    body = B.banner(crumbs, "Case study", "How a villa project runs with Eastbridge on the owner's side, worked through in full.",
                    "saqqara-01", credit_of("saqqara-01")) + f'''
<section class="section"><div class="wrap feature">
<figure>{CS.svg_site()}</figure>
<div><span class="kicker">Illustrative case study</span><h2>Island E, Dubai Islands: a waterfront villa from plot to keys</h2>
<p class="muted">A modelled scenario built on Nakheel's published Island E plot information and published Dubai construction costs. It follows a British family from the plot decision to the keys, with every figure shown and explained.</p>
<div class="kpis" style="margin:28px 0">
<div><b>AED {CS.AVOIDED_TOTAL:.2f}m</b><span>cost avoided</span></div>
<div><b>AED {CS.UNDER:.2f}m</b><span>under budget</span></div>
<div><b>35</b><span>months, plot to keys</span></div>
<div><b>8,050</b><span>sq ft waterfront plot</span></div></div>
<p><a class="btn" href="/case-studies/island-e-waterfront-villa/">Read the case study</a></p></div></div></section>
<section class="section stone"><div class="wrap split"><div><h2>And the houses behind it</h2></div><div><p class="muted">The judgement in the case study comes from 21 years of building. See the homes Philip Chapman's company delivered.</p><p><a class="btn btn--ghost" href="/work/">See the work</a></p></div></div></section>
{B.cta_band()}'''
    B.page(path, "Case Study: Island E Villa, Dubai Islands | Eastbridge",
           "An illustrative case study of an Island E waterfront villa on Dubai Islands, from plot review to handover, with the budget, bids, claims and programme shown in full.",
           body, crumbs, og=B.og_image("saqqara-01"))

def case_page():
    path = "/case-studies/island-e-waterfront-villa/"
    crumbs = [("Home", "/"), ("Case study", "/case-studies/"), ("Island E waterfront villa", path)]
    k = CS
    plot_rate = k.PLOT_PRICE * 1e6 / k.PLOT_SQFT
    budget_rows = ""
    out_vals = {0: None, 1: None}
    for line, b, o in k.BUDGET:
        budget_rows += f"<tr><td>{esc(line)}</td><td class='num'>{b:.2f}</td></tr>"
    outturn_rows = [
     ("Main contract and externals: agreed lump sum", k.CONTRACT_SUM),
     ("Owners' upgrades (kitchen, home automation)", k.OWNER_UPGRADES),
     ("Dewatering: the genuine change only", k.DEWATERING),
     ("Design development and agreed site variations", k.OTHER_VARS),
     ("Extension of time: four weeks of time-related cost", k.EOT_COST),
     ("Design team, interior design and consultant of record", 1.04),
     ("Nakheel, authority and utility connection fees", 0.30),
    ]
    out_html = "".join(f"<tr><td>{esc(a)}</td><td class='num'>{v:.3f}</td></tr>" for a, v in outturn_rows)
    vr = "".join(f"<tr><td><b>{esc(a)}</b><br><span class='muted'>{esc(d)}</span></td><td class='num'>{v:.2f}</td></tr>" for a, d, v in k.VALUE_REVIEW)
    bids = "".join(f"<tr><td><b>{esc(n)}</b></td><td class='num'>{h:.2f}</td><td class='num'>{nn:.2f}</td><td>{esc(note)}</td></tr>" for n, h, nn, note in k.BIDS)
    avoided = "".join(f"<tr><td>{esc(a)}</td><td class='num'>{v:.2f}</td></tr>" for a, v in k.AVOIDED)
    plot_plan = "".join(f"<tr><td>{d}</td><td class='num'>{int(p*100)}%</td><td class='num'>{k.PLOT_PRICE*p:.2f}</td></tr>" for d, p in k.PLOT_PLAN)
    cash = "".join(f"<tr><td>{y}</td><td class='num'>{p:.2f}</td><td class='num'>{b:.2f}</td><td class='num'>{p+b:.2f}</td></tr>" for y, p, b in k.CASH)
    events = "".join(f'<li><span class="when">{esc(w)}</span><h3>{esc(t)}</h3><p>{esc(a)}</p><p>{esc(b)}</p><p class="result">{esc(r)}</p></li>' for w, t, a, b, r in k.EVENTS)
    peak = max(k.CASH, key=lambda r: r[1] + r[2])
    notice = ('<div class="notice"><b>Illustrative case study</b>The owners, events and outcome figures on this page are a modelled scenario, '
              'not a description of a real client or project. The plot facts are Nakheel\'s published figures for Island E (price and payment plan sheet and draft development '
              'controls, September 2026). Construction costs are drawn from published Dubai cost ranges. It shows how we would run a villa on an Island E plot, '
              'and what the numbers could look like.</div>')
    body = B.banner(crumbs, "Island E, Dubai Islands: a waterfront villa from plot to keys",
                    "A British family, an 8,050 sq ft waterfront plot and a house that has to be designed, approved and built. How the project runs with Eastbridge on their side.",
                    "saqqara-01", "Photograph: Saqqara, Feock, a waterfront house built by P Chapman Construction",
                    '<span class="tag">Illustrative case study</span>') + f'''
<section class="section--tight"><div class="wrap">{notice}</div></section>
<section class="section--tight"><div class="wrap">
<div class="kpis">
<div><b>AED {k.AVOIDED_TOTAL:.2f}m</b><span>cost avoided against the first numbers on the table</span></div>
<div><b>AED {k.OUTTURN:.2f}m</b><span>final account, against an approved budget of AED {k.APPROVED:.2f}m (excluding the plot)</span></div>
<div><b>4 of 11</b><span>weeks of extension of time agreed, against the contractor's claim</span></div>
<div><b>35 months</b><span>from plot review to keys</span></div></div>
<dl class="facts" style="margin-top:40px">
<div><dt>Location</dt><dd>Island E, Dubai Islands (Nakheel)</dd></div>
<div><dt>Plot</dt><dd>Waterfront, {k.PLOT_SQFT:,} sq ft</dd></div>
<div><dt>Plot price</dt><dd>AED {k.PLOT_PRICE:.1f}m (AED {plot_rate:,.0f} per sq ft)</dd></div>
<div><dt>Permitted</dt><dd>Basement, ground and two floors; 12.5 m; FAR {k.FAR}</dd></div>
<div><dt>House</dt><dd>{k.GFA:,} sq ft above ground, {k.BASEMENT:,} sq ft basement</dd></div>
<div><dt>Owners</dt><dd>A British family relocating from London</dd></div></dl>
</div></section>

<div class="wrap">
<section class="chapter" aria-labelledby="c1"><header><b>01</b><span>Before the plot</span></header><div>
<h2 id="c1">The plot review: what the brochure doesn't say</h2>
<p>The family are choosing between a beach plot at around AED 2,346 per sq ft and a waterfront plot at around AED 2,188, both on Nakheel's September 2026 price sheet. Plots on Island E are paid in seven instalments from booking to September 2029. Before they submit an expression of interest, we review both plots and the draft development controls.</p>
<ul class="findings">
<li><b>Shoreline rules can tighten.</b> The draft controls allow the rules along the shoreline to be tightened after marine assessments. On a beach plot that is a design risk the owners would carry. They choose the waterfront plot.</li>
<li><b>Draft is not final.</b> The controls are finalised with the sale and purchase agreement. We list the points to confirm in writing before signing: how basement area is treated, setbacks, site coverage, any deadline to start or finish building, and when the plot will have roads and services.</li>
<li><b>The house the rules allow.</b> A floor area ratio of {k.FAR} on {k.PLOT_SQFT:,} sq ft gives about {k.GFA:,} sq ft above ground, over ground and two upper floors within 12.5 m, plus a basement.</li>
<li><b>The real total.</b> Plot, design, approvals, construction, landscaping and contingency come to about AED {k.PLOT_PRICE + k.APPROVED:.1f}m before furniture. The owners go ahead knowing the whole number, not just the plot price.</li>
</ul>
<h3>The cash plan nobody else draws</h3>
<p>The plot instalments do not stop when building starts. In this programme, construction runs through 2028 and 2029 while four plot payments are still due. The year of peak outgoings is {peak[0]}, at about AED {peak[1]+peak[2]:.1f}m. The owners arrange their funding for that before they commit.</p>
<figure class="chart-box"><ul class="legend"><li><i style="background:{k.C_PLOT}"></i>Plot instalments</li><li><i style="background:{k.C_BUILD}"></i>Build, design and fees</li></ul>{k.svg_cash()}<figcaption>Annual outgoings, AED millions. Plot payments follow Nakheel's published schedule; build costs follow a typical spend curve over the 19-month construction period.</figcaption></figure>
<div class="table-wrap"><table class="table"><thead><tr><th>Year</th><th class="num">Plot (AED m)</th><th class="num">Build and fees (AED m)</th><th class="num">Total (AED m)</th></tr></thead><tbody>{cash}</tbody></table></div>
<details><summary class="small">Plot payment schedule</summary><div class="table-wrap"><table class="table"><thead><tr><th>Instalment</th><th class="num">Share</th><th class="num">AED m</th></tr></thead><tbody>{plot_plan}</tbody></table></div></details>
</div></section>

<section class="chapter" aria-labelledby="c2"><header><b>02</b><span>Brief and budget</span></header><div>
<h2 id="c2">A wish list that didn't fit the plot</h2>
<p>The family's first wish list comes to about 10,400 sq ft above ground: five bedroom suites, a guest suite, a gym, a cinema, staff quarters and a large kitchen and family room. The plot allows about {k.GFA:,}.</p>
<p>Rather than cut rooms, we reorganise. The gym, cinema, staff quarters and plant move to a {k.BASEMENT:,} sq ft basement, subject to how the final controls treat basement area. The guest suite becomes a flexible ground-floor room. Every room the family cares about stays, and the house fits the rules before an architect has drawn a line.</p>
<p>Then the budget, built from the bottom up: construction at a luxury rate per square foot for the house above ground, a separate rate for the basement with its dewatering and waterproofing, external works, design fees, authority fees and a 10% contingency held by the owners, not the contractor.</p>
<div class="table-wrap"><table class="table"><thead><tr><th>Approved budget, excluding plot and furniture</th><th class="num">AED m</th></tr></thead><tbody>{budget_rows}</tbody><tfoot><tr><td>Total approved budget</td><td class="num">{k.APPROVED:.2f}</td></tr></tfoot></table></div>
<p class="small muted">Eastbridge's own fee is not included in these figures; set it against the cost avoided shown at the end. Construction rates sit inside published 2025–26 ranges for luxury villas in Dubai (around AED 900 to 1,400 per sq ft). Design fees of about 8% sit inside the published 6–12% range for full design and engineering.</p>
</div></section>

<section class="chapter" aria-labelledby="c3"><header><b>03</b><span>The team</span></header><div>
<h2 id="c3">Choosing the architect on more than the fee</h2>
<p>We shortlist three architects with villa experience and a registered consultant able to act as consultant of record. Their fee proposals look far apart until they are read side by side: one excludes interior coordination, another excludes the construction-stage duties of the consultant of record. Normalised, the gap closes to a few per cent.</p>
<p>The owners appoint the practice whose villas they like best and whose scope is complete, and appoint their interior designer at the same time, so joinery, lighting and services are designed together from the start. They live in London throughout the design stage; we run a fortnightly design meeting by video and a decision log they can read on their phones.</p>
</div></section>

<section class="chapter" aria-labelledby="c4"><header><b>04</b><span>Design to cost</span></header><div>
<h2 id="c4">The concept came back AED {k.CONCEPT_EST - k.APPROVED:.1f}m over budget</h2>
<p>The concept is beautiful. The cost plan puts it at about AED {k.CONCEPT_EST:.1f}m against an approved AED {k.APPROVED:.2f}m. Left alone, that gap would have surfaced at tender, when it is far more expensive to fix. Instead we run a value review with the architect and engineers.</p>
<div class="table-wrap"><table class="table"><thead><tr><th>Change</th><th class="num">Saving (AED m)</th></tr></thead><tbody>{vr}</tbody><tfoot><tr><td>Total designed out before tender</td><td class="num">{k.VALUE_TOTAL:.2f}</td></tr></tfoot></table></div>
<p>None of these changes is visible from the garden or the water. The design goes to Nakheel's design review and then to permit, both submitted by the consultant of record, with the cost plan back on budget.</p>
</div></section>

<section class="chapter" aria-labelledby="c5"><header><b>05</b><span>Tender</span></header><div>
<h2 id="c5">The cheapest bid was the most expensive</h2>
<p>Four contractors price the same drawings. On the headline numbers, Contractor A is AED 0.75m cheaper than the next lowest bid. Put on a like-for-like basis, adding back what each bid leaves out and correcting what each under-prices, it is the most expensive of the four.</p>
<figure class="chart-box"><ul class="legend"><li><i style="background:{k.C_ALT}"></i>Headline price</li><li><i style="background:{k.C_BUILD}"></i>Normalised, like-for-like</li></ul>{k.svg_bids()}<figcaption>Main contract and external works, AED millions. Pre-tender estimate: AED 13.00m.</figcaption></figure>
<div class="table-wrap"><table class="table"><thead><tr><th>Bid</th><th class="num">Headline</th><th class="num">Normalised</th><th>What we found</th></tr></thead><tbody>{bids}</tbody></table></div>
<p>The owners appoint Contractor B. After clarification and negotiation the lump sum is agreed at AED {k.CONTRACT_SUM:.2f}m, with ground risk, programme and a named site team written into the contract, and the long-lead glazing ordered as an early package.</p>
</div></section>

<section class="chapter" aria-labelledby="c6"><header><b>06</b><span>Construction</span></header><div>
<h2 id="c6">Nineteen months on site</h2>
<p>Every week the owners receive a photo update; every month, a written report with progress, the forecast final cost, the risks and the decisions they need to make. The moments that decide the final account look like this.</p>
<ol class="events">{events}</ol>
<h3>The monthly report</h3>
<p>One page the owners can read in five minutes, wherever they are. This is month 27.</p>
<div class="report" role="img" aria-label="Sample monthly report: progress 61% against 64% planned, forecast final cost AED 15.12m against budget AED 15.64m, three decisions due">
<header><b>Eastbridge · Monthly report</b><span class="small">Month 27 · Island E villa</span></header>
<div class="r-body">
<div><h4>Progress</h4><span class="big">61%</span> <span class="pill watch">3% behind</span><div class="bar"><i style="width:61%"></i><em style="left:64%"></em></div><span class="small muted">Planned 64%. Recovery plan agreed for fit-out.</span></div>
<div><h4>Forecast final cost</h4><span class="big">AED 15.12m</span> <span class="pill ok">Within budget</span><div class="bar"><i style="width:97%"></i><em style="left:100%"></em></div><span class="small muted">Budget AED 15.64m, including AED 0.52m of contingency not yet committed.</span></div>
<div class="r-full"><h4>Decisions needed from you</h4><ul><li>Pool tile and coping sample, by the 14th</li><li>Kitchen joinery shop drawings, by the 18th</li><li>Garden lighting scheme, by the 25th</li></ul></div>
<div><h4>Payment recommendation</h4><span>Valuation 12: AED 0.98m claimed, AED 0.91m recommended</span></div>
<div><h4>Top risk</h4><span>Shamal season during glazing installation; protection plan in place</span></div>
</div></div>
<p class="small muted" style="margin-top:12px">Illustrative. Reports are tailored to each client.</p>
</div></section>

<section class="chapter" aria-labelledby="c7"><header><b>07</b><span>Handover</span></header><div>
<h2 id="c7">Keys, and nothing left to chase</h2>
<p>Handover is planned from the start of construction. We walk the house room by room and system by system, witness the commissioning of the cooling, water, pool, lighting and security systems, and issue the snag list in sections as areas finish. Three hundred and twelve items are recorded; all are closed before the owners accept the house.</p>
<p>The handover file is complete on the day: completion certificate, as-built drawings, warranties, operation and maintenance manuals, test certificates, and a schedule of keys and codes. Retention is released only when the defects period ends with nothing outstanding.</p>
</div></section>

<section class="chapter" aria-labelledby="c8"><header><b>08</b><span>Outcome</span></header><div>
<h2 id="c8">The final account</h2>
<div class="table-wrap"><table class="table"><thead><tr><th>Final account, excluding plot and furniture</th><th class="num">AED m</th></tr></thead><tbody>{out_html}</tbody><tfoot><tr><td>Total</td><td class="num">{k.OUTTURN:.3f}</td></tr></tfoot></table></div>
<p>Against an approved budget of AED {k.APPROVED:.2f}m, the house comes in AED {k.UNDER:.2f}m under, having used AED {k.CONT_USED:.2f}m of the AED 1.30m contingency, AED {k.OWNER_UPGRADES:.2f}m of it on upgrades the owners chose. Handover is four weeks later than the original programme, exactly the extension agreed.</p>
<h3>Where the difference came from</h3>
<div class="table-wrap"><table class="table"><thead><tr><th>Cost avoided against the first numbers on the table</th><th class="num">AED m</th></tr></thead><tbody>{avoided}</tbody><tfoot><tr><td>Total</td><td class="num">{k.AVOIDED_TOTAL:.2f}</td></tr></tfoot></table></div>
<h3>The programme</h3>
<figure class="chart-box"><ul class="legend"><li><i style="background:{k.C_PLOT}"></i>Pre-construction stages</li><li><i style="background:{k.C_BUILD}"></i>Construction</li></ul>{k.svg_programme()}<figcaption>Months from the plot review in October 2026. Construction assumes site access from early 2028; on a new island, the programme moves with Nakheel's infrastructure dates.</figcaption></figure>
</div></section>

<section class="chapter" aria-labelledby="c9"><header><b>09</b><span>Method</span></header><div>
<h2 id="c9">How this case study was built</h2>
<p class="small">The plot size, price per square foot, payment schedule, floors, height limit and floor area ratio are Nakheel's published Island E figures (price and payment plan sheet and draft development control regulations, 24 September 2026). Construction rates sit within published Dubai ranges: Engel &amp; Völkers (December 2025) and Real Estate Club Dubai. Design fees sit within the 6–12% range published by Optimal Engineering. The family, the contractors, the events and the outcome are invented to show how we work and how the numbers move. Nothing here is a forecast for a particular plot; for that, we carry out a plot review.</p>
<ul class="small"><li>Nakheel: Bay Estate, Island E price and payment plan sheet, masterplan and draft development control regulations, issued 24 September 2026</li><li><a href="https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai" rel="noopener">Engel &amp; Völkers: construction cost in Dubai</a></li><li><a href="https://realestateclubdubai.com/dubai-villa-architects" rel="noopener">Real Estate Club Dubai: villa architects, fees and timelines</a></li><li><a href="https://www.optimal.ae/blog/cost-to-build-a-villa-in-dubai" rel="noopener">Optimal Engineering: cost to build a villa in Dubai</a></li></ul>
</div></section>
</div>
{B.cta_band("Buying on Island E?", "Send us the plot number, or the plots you are choosing between. We will tell you what you can build and what it will really cost.", "saqqara-04")}'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": "Island E, Dubai Islands: a waterfront villa from plot to keys (illustrative case study)",
           "author": {"@id": B.PERSON_ID}, "publisher": {"@id": B.ORG_ID}, "mainEntityOfPage": B.url(path),
           "image": B.url(B.og_image("saqqara-01")), "inLanguage": "en-GB", "about": "Villa construction project management, Dubai Islands",
           "genre": "Illustrative case study"}
    B.page(path, "Island E Villa Case Study: Plot to Keys | Eastbridge",
           "Illustrative case study of a waterfront villa on Island E, Dubai Islands: plot review, budget, design to cost, tender, claims and handover, with every figure shown.",
           body, crumbs, [art], og=B.og_image("saqqara-01"))
