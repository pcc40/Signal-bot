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

KPMG_2015_URL = "https://assets.kpmg.com/content/dam/kpmg/pdf/2015/04/Global-Construction-Survey.pdf"

def evidence_html():
    """Historical context only: kept small, with the year and scope beside the figures."""
    return ('<ul class="evidence-list small">'
            f'<li>In KPMG\'s <a href="{KPMG_2015_URL}" rel="noopener">Global Construction Survey 2015</a>, 31% of respondents\' projects came within 10% of budget '
            'over the previous three years, and 25% within 10% of their original deadlines. <span class="muted">A 2015 global survey of more than 100 '
            'organisations with significant capital construction programmes, not Dubai villa data.</span></li>'
            '<li>In August 2025 Dubai Municipality formally warned villa engineering consultancies about over-designing villas and inflating build costs. '
            '<span class="muted"><a href="https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704" rel="noopener">Gulf News, August 2025</a>.</span></li>'
            '</ul>')

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
{B.hero_video_html()}<div class="wrap"><span class="kicker">Client-side project management · Dubai and Abu Dhabi</span>
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
</div></section>

<section class="section band-dark" aria-labelledby="case-h"><div class="wrap case-feature">
<div><span class="kicker">Worked project example</span><h2 id="case-h">How we would manage an Island E villa</h2>
<div class="notice" style="margin:22px 0"><b>Hypothetical</b>{esc(CASE_DISCLOSURE)}</div>
<p class="muted">Worked through with Nakheel's published plot information, its draft development controls and published Dubai costs, it shows what an owner would receive from us:</p>
<div class="outputs">
<div><b>Budget structure</b><span>Every cost line, quantified or awaiting quotation, including registration fees and VAT</span></div>
<div><b>Cash-flow planning</b><span>Plot instalments and build costs, year by year</span></div>
<div><b>Tender comparison</b><span>Bids put on a like-for-like basis</span></div>
<div><b>Programme review</b><span>Plot review to keys, with the assumptions stated</span></div></div>
<p><a class="btn" href="{CASE_URL}">See the worked example</a></p></div>
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
{__import__("pages_guides").cta_block(compact=True)}
</div></section>

<section class="section--tight" aria-labelledby="hfaq-h"><div class="wrap split"><h2 id="hfaq-h">Questions</h2>{B.faq_html(faqs)}</div></section>
{B.how_it_starts()}
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
<div class="head-row"><h2>Some context</h2><p class="muted">Cost and time overruns are a long-standing risk on construction projects of every size. Two reference points, with their limits stated.</p></div>
{evidence_html()}
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
<p>Against that, a client-side project manager is a predictable cost, agreed in advance. Our <a href="/case-studies/island-e-waterfront-villa/">Island E worked example</a>, a hypothetical project rather than a completed appointment, shows what that work produces: a budget structure that separates quantified allowances from costs still awaiting quotation, a year-by-year cash-flow plan, a like-for-like tender comparison and a programme review with its assumptions stated.</p>
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
MOD = '<span class="mod">Modelled</span>'
CASE_URL = "/case-studies/island-e-waterfront-villa/"
CASE_DISCLOSURE = ("A hypothetical project that shows our method. It is not a completed Eastbridge appointment, "
                   "not a real client and not a promise of savings.")

def uk_case_card():
    """Lead the track record with a real UK project (P Chapman Construction as main contractor)."""
    p = PROJ["owers-house"]
    return f'''<section class="section"><div class="wrap feature">
<figure>{pic("owers-house-02", "Owers House, Feock: dark timber living wing cantilevered over the falling site above the Fal estuary", "(max-width:900px) 100vw, 58vw")}<figcaption>{esc(credit_of("owers-house-02"))}. Architect: {esc(p["architect"])}.</figcaption></figure>
<div><span class="kicker">UK project case study · Main contractor</span><h2>Owers House, Feock</h2>
<p class="muted">A contemporary house above the Fal estuary, designed by {esc(p["architect"])} and built by P Chapman Construction, the UK company Philip Chapman founded and led. The house won a RIBA South West Award in 2016. This was UK contracting work, not an Eastbridge appointment.</p>
<p><a class="btn" href="/work/owers-house/#case-study">Read the project case study</a></p></div></div></section>'''

def case_hub():
    path = "/case-studies/"
    crumbs = [("Home", "/"), ("Case studies", path)]
    body = B.banner(crumbs, "Case studies", "A real UK project from Philip Chapman's years as a main contractor, and a worked example of how we would manage a Dubai villa today.",
                    "owers-house-04", credit_of("owers-house-04")) + uk_case_card() + f'''
<section class="section stone"><div class="wrap feature">
<figure>{CS.svg_site()}</figure>
<div><span class="kicker">Worked project example · Hypothetical</span><h2>Island E: how we would manage a waterfront villa</h2>
<div class="notice"><b>Not a completed project</b>{esc(CASE_DISCLOSURE)}</div>
<p class="muted" style="margin-top:18px">Built on Nakheel's published Island E plot information, its draft development controls and published Dubai cost ranges. It shows what we would produce for an owner:</p>
<ul class="findings">
<li><b>Budget structure</b>Every cost line, what is quantified and what is still awaiting quotation, including registration fees and VAT.</li>
<li><b>Cash-flow planning</b>Plot instalments and build costs year by year, so funding is arranged before commitment.</li>
<li><b>Tender comparison</b>Bids put on a like-for-like basis: exclusions, provisional sums, preliminaries and programme.</li>
<li><b>Programme review</b>35 months from plot review to keys, with the assumptions behind each stage stated.</li></ul>
<p><a class="btn" href="{CASE_URL}">See the worked example</a></p></div></div></section>
<section class="section"><div class="wrap split"><div><h2>More of the houses behind it</h2></div><div><p class="muted">Private houses, estates, developments and hotel work built by P Chapman Construction in the UK.</p><p><a class="btn btn--ghost" href="/work/">See the work</a></p></div></div></section>
{B.cta_band()}'''
    B.page(path, "Case Studies: UK Project and Island E Worked Example",
           "Owers House, a RIBA award-winning UK house built by P Chapman Construction, and a hypothetical worked example of how Eastbridge would manage an Island E villa.",
           body, crumbs, og=B.og_image("owers-house-04"))

def case_page():
    path = CASE_URL
    crumbs = [("Home", "/"), ("Case studies", "/case-studies/"), ("Island E worked example", path)]
    k = CS
    r = k.r
    plot_rate = k.PLOT_PRICE * 1e6 / k.PLOT_SQFT
    vat_col = lambda vat: "5%" if vat else "To be confirmed"
    alloc_rows = "".join(f"<tr><td>{esc(line)}</td><td>{vat_col(vat)}</td><td class='num'>{v:.2f}</td></tr>" for _, line, v, vat in k.ALLOWANCES)
    budget = f'''<div class="table-wrap"><table class="table"><caption class="small muted" style="caption-side:top;text-align:left;padding-bottom:8px">Price base {k.PRICE_BASE}. AED millions. Allowances shown excluding VAT; VAT shown as its own line.</caption>
<thead><tr><th>Quantified allowance</th><th>VAT</th><th class="num">AED m</th></tr></thead><tbody>
<tr><th colspan="3">Plot and acquisition</th></tr>
<tr><td>Plot: {k.PLOT_SQFT:,} sq ft at about AED {plot_rate:,.0f} per sq ft</td><td>Exempt (bare land)</td><td class='num'>{k.PLOT_PRICE:.2f}</td></tr>
<tr><td>Dubai Land Department registration: purchaser's 2% of the plot price, plus AED {k.DLD_FIXED_AED} in fixed fees</td><td>None assumed (government fee)</td><td class='num'>{r(k.DLD_FEE):.2f}</td></tr>
<tr><th colspan="3">Design, approvals and construction</th></tr>
{alloc_rows}
<tr><th colspan="3">Tax</th></tr>
<tr><td>VAT at 5% on the allowances marked 5% (AED {k.VATABLE:.2f}m)</td><td></td><td class='num'>{r(k.VAT):.2f}</td></tr>
</tbody><tfoot><tr><td colspan="2">Subtotal of stated allowances (not an all-in budget)</td><td class="num">{r(k.STATED_SUBTOTAL):.2f}</td></tr></tfoot></table></div>'''
    awaiting = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in k.AWAITING)
    vr = "".join(f"<tr><td><b>{esc(a)}</b><br><span class='muted'>{esc(d)}</span></td><td class='num'>{v:.2f} {MOD}</td></tr>" for a, d, v in k.VALUE_REVIEW)
    bids = "".join(f"<tr><td><b>{esc(n)}</b></td><td class='num'>{h:.2f}</td><td class='num'>{nn:.2f}</td><td>{esc(note)}</td></tr>" for n, h, nn, note in k.BIDS)
    avoided = "".join(f"<tr><td>{esc(a)}<br><span class='small muted'>{esc(b)}</span></td><td class='num'>{v:.2f} {MOD}</td></tr>" for a, b, v in k.AVOIDED)
    plot_plan = "".join(f"<tr><td>{d}</td><td class='num'>{int(p*100)}%</td><td class='num'>{k.PLOT_PRICE*p:.2f}</td></tr>" for d, p in k.PLOT_PLAN)
    cash = "".join(f"<tr><td>{y}</td><td class='num'>{p:.2f}</td><td class='num'>{d:.2f}</td><td class='num'>{v:.2f}</td><td class='num'>{r(p+d+v):.2f}</td></tr>" for y, p, d, v in k.CASH)
    ct = k.CASH_TOTALS
    cash_foot = f"<tr><td>Total</td><td class='num'>{ct[0]:.2f}</td><td class='num'>{ct[1]:.2f}</td><td class='num'>{ct[2]:.2f}</td><td class='num'>{r(sum(ct)):.2f}</td></tr>"
    events = "".join(f'<li><span class="when">{esc(w)}</span><h3>{esc(t)}</h3><p>{esc(a)}</p><p>{esc(b)}</p><p class="result">{esc(res)} {MOD}</p></li>' for w, t, a, b, res in k.EVENTS)
    peak = max(k.CASH, key=lambda row: row[1] + row[2] + row[3])
    # modelled final account, reconciled against the stated allowances
    recon = [
     ("Plot", k.PLOT_PRICE, k.PLOT_PRICE),
     ("Dubai Land Department registration (purchaser's share)", k.DLD_FEE, k.DLD_FEE),
     ("Construction: house, basement, pool and external works", k.CONSTRUCTION, k.CONSTRUCTION_OUT),
     ("Design and consultant fees", k.A["design"], k.A["design"]),
     ("Approvals and connections", k.A["approvals"], k.A["approvals"]),
     ("Contingency (drawn amounts are in the construction line)", k.A["contingency"], 0.0),
     ("VAT at 5%", k.VAT, k.OUTTURN_VAT),
    ]
    recon_rows = "".join(f"<tr><td>{esc(a)}</td><td class='num'>{r(b):.2f}</td><td class='num'>{r(o):.2f}{(' ' + MOD) if r(o) != r(b) else ''}</td></tr>" for a, b, o in recon)
    outturn_rows = [
     ("Main contract and external works: agreed lump sum", k.CONTRACT_SUM),
     ("Owners' upgrades (kitchen, home automation)", k.OWNER_UPGRADES),
     ("Dewatering: the genuine change only", k.DEWATERING),
     ("Design development and agreed site variations", k.OTHER_VARS),
     ("Extension of time: four weeks of time-related cost", k.EOT_COST),
    ]
    out_html = "".join(f"<tr><td>{esc(a)}</td><td class='num'>{v:.3f} {MOD}</td></tr>" for a, v in outturn_rows)
    notice = (f'<div class="notice"><b>A hypothetical worked example</b>{esc(CASE_DISCLOSURE)} '
              'The family, the contractors, the events and every figure marked “modelled” are invented to show how we work and how the numbers move. '
              'Nothing here is a forecast for a particular plot. For that, we carry out a plot review.</div>')
    sources_kept_apart = f'''<div class="table-wrap"><table class="table"><thead><tr><th>Published</th><th>Planning assumptions</th><th>Invented for the example</th></tr></thead><tbody><tr>
<td>Island E plot price per sq ft, payment schedule, floors, 12.5 m height limit and floor area ratio (Nakheel, 24 September 2026; the development controls are a <b>draft</b>, finalised with the sale and purchase agreement). Dubai Land Department registration fees. UAE VAT rules. Published Dubai construction cost ranges.</td>
<td>Plot size and price, house size, cost allowances, price base of {k.PRICE_BASE}, a {k.CONSTRUCTION_MONTHS}-month construction period from {k.CONSTRUCTION_START} to {k.CONSTRUCTION_END}, and site access from early 2028. These are our assumptions, not Nakheel commitments.</td>
<td>The owners, the wish list, the architects and contractors, the bids, the claims, the monthly report and every outcome marked “modelled”.</td>
</tr></tbody></table></div>'''
    body = B.banner(crumbs, "How we would manage an Island E villa: a worked project example",
                    "A hypothetical waterfront villa on Island E, Dubai Islands, from plot review to keys. It shows the budget structure, cash-flow plan, tender comparison and programme review we would produce for an owner.",
                    "saqqara-01", "Photograph: Saqqara, Feock, a waterfront house built in the UK by P Chapman Construction",
                    '<span class="tag">Worked example · Hypothetical</span>') + f'''
<section class="section--tight"><div class="wrap">{notice}</div></section>
<section class="section--tight"><div class="wrap">
<h2>What is published, what is assumed, what is invented</h2>
{sources_kept_apart}
<div class="kpis kpis--text" style="margin-top:32px">
<div><b>Budget structure</b><span>AED {r(k.STATED_SUBTOTAL):.2f}m of stated allowances, plus {len(k.AWAITING)} items awaiting quotation or excluded</span></div>
<div><b>Cash-flow plan</b><span>Peak year {peak[0]}, about AED {r(peak[1]+peak[2]+peak[3]):.2f}m including plot instalments</span></div>
<div><b>Tender comparison</b><span>Four bids put on a like-for-like basis</span></div>
<div><b>Programme review</b><span>35 months from plot review to keys, assumptions stated</span></div></div>
<dl class="facts" style="margin-top:40px">
<div><dt>Location</dt><dd>Island E, Dubai Islands (Nakheel)</dd></div>
<div><dt>Example plot</dt><dd>Waterfront, {k.PLOT_SQFT:,} sq ft</dd></div>
<div><dt>Example plot price</dt><dd>AED {k.PLOT_PRICE:.2f}m (about AED {plot_rate:,.0f} per sq ft)</dd></div>
<div><dt>Permitted (draft controls)</dt><dd>Basement, ground and two floors; 12.5 m; FAR {k.FAR}</dd></div>
<div><dt>Assumed house</dt><dd>{k.GFA:,} sq ft above ground, {k.BASEMENT:,} sq ft basement</dd></div>
<div><dt>Hypothetical owners</dt><dd>A British family relocating from London</dd></div></dl>
</div></section>

<div class="wrap">
<section class="chapter" aria-labelledby="c1"><header><b>01</b><span>Before the plot</span></header><div>
<h2 id="c1">The plot review: what the brochure doesn't say</h2>
<p>Suppose the family are choosing between a beach plot at around AED 2,346 per sq ft and a waterfront plot at around AED 2,188, both on Nakheel's September 2026 price sheet. Plots on Island E are paid in seven instalments from booking to September 2029. Before they submit an expression of interest, we would review both plots and the draft development controls.</p>
<ul class="findings">
<li><b>Shoreline rules can tighten.</b> The draft controls allow the rules along the shoreline to be tightened after marine assessments. On a beach plot that is a design risk the owners would carry. In this example they choose the waterfront plot.</li>
<li><b>Draft is not final.</b> The controls are finalised with the sale and purchase agreement. We would list the points to confirm in writing before signing: how basement area is treated, setbacks, site coverage, any deadline to start or finish building, and when the plot will have roads and services.</li>
<li><b>The house the draft rules allow.</b> A floor area ratio of {k.FAR} on {k.PLOT_SQFT:,} sq ft gives about {k.GFA:,} sq ft above ground, over ground and two upper floors within 12.5 m, plus a basement.</li>
<li><b>The whole number, not just the plot price.</b> Plot, registration, design, approvals, construction, landscaping, contingency and VAT come to AED {r(k.STATED_SUBTOTAL):.2f}m of stated allowances. That is not an all-in budget: Eastbridge's fee, escalation, furniture and several charges awaiting confirmation are on top, and are listed in chapter 02.</li>
</ul>
<h3>The cash plan</h3>
<p>The plot instalments do not stop when building starts. In this programme, construction would run through 2028 and 2029 while four plot payments are still due. On the stated allowances, the year of peak outgoings is {peak[0]}, at about AED {r(peak[1]+peak[2]+peak[3]):.2f}m. The owners would arrange their funding for that before they commit.</p>
<figure class="chart-box"><ul class="legend"><li><i style="background:{k.C_PLOT}"></i>Plot instalments and registration</li><li><i style="background:{k.C_BUILD}"></i>Design, approvals, construction and contingency, including VAT</li></ul>{k.svg_cash()}<figcaption>Planning cash flow of the stated allowances, AED millions, at {k.PRICE_BASE} prices with no escalation. Plot payments follow Nakheel's published schedule; construction and contingency follow a typical spend curve over the assumed {k.CONSTRUCTION_MONTHS}-month construction period. Excludes Eastbridge's fee and the items awaiting quotation.</figcaption></figure>
<div class="table-wrap"><table class="table"><thead><tr><th>Year</th><th class="num">Plot and registration</th><th class="num">Design, approvals, construction, contingency (ex VAT)</th><th class="num">VAT</th><th class="num">Total (AED m)</th></tr></thead><tbody>{cash}</tbody><tfoot>{cash_foot}</tfoot></table></div>
<details><summary class="small">Plot payment schedule</summary><div class="table-wrap"><table class="table"><thead><tr><th>Instalment</th><th class="num">Share</th><th class="num">AED m</th></tr></thead><tbody>{plot_plan}</tbody></table></div></details>
</div></section>

<section class="chapter" aria-labelledby="c2"><header><b>02</b><span>Brief and budget</span></header><div>
<h2 id="c2">A wish list that didn't fit the plot</h2>
<p>In this example the family's first wish list comes to about 10,400 sq ft above ground: five bedroom suites, a guest suite, a gym, a cinema, staff quarters and a large kitchen and family room. The plot allows about {k.GFA:,}.</p>
<p>Rather than cut rooms, we would reorganise. The gym, cinema, staff quarters and plant move to a {k.BASEMENT:,} sq ft basement, subject to how the final controls treat basement area. The guest suite becomes a flexible ground-floor room. Every room the family cares about stays, and the house fits the rules before an architect has drawn a line.</p>
<p>Then the budget, built from the bottom up: construction above ground at about AED {k.HOUSE_RATE:,.0f} per sq ft, the basement separately at about AED {k.BASEMENT_RATE:,.0f} per sq ft with its dewatering and waterproofing, external works, design fees, approvals and connections, a 10% contingency held by the owners rather than the contractor, registration fees and VAT.</p>
<h3>Quantified allowances</h3>
{budget}
<h3>Awaiting quotation, confirmation or excluded</h3>
<p>None of these is treated as zero. Each is either quoted separately or must be confirmed before the budget can be called complete.</p>
<div class="table-wrap"><table class="table"><thead><tr><th>Cost</th><th>Status</th></tr></thead><tbody>{awaiting}</tbody></table></div>
<h3>Assumptions behind the figures</h3>
<ul class="small">
<li><b>Price base and escalation.</b> Allowances are at {k.PRICE_BASE} prices. Construction is assumed to run for {k.CONSTRUCTION_MONTHS} months, from {k.CONSTRUCTION_START} to {k.CONSTRUCTION_END}. Escalation between the price base and the construction period is not included, and no rate is assumed.</li>
<li><b>Construction rates.</b> About AED {k.HOUSE_RATE:,.0f} per sq ft above ground sits inside published 2025–26 ranges for luxury villas in Dubai (around AED 900 to 1,400 per sq ft). The basement rate is our planning assumption. Pool and landscaping sit within published ranges (pool AED 80,000 to 250,000; landscaping AED 100 to 500 per sq ft of garden).</li>
<li><b>Design fees.</b> About 8% of construction, inside the published 6–12% range for full design and engineering.</li>
<li><b>Registration.</b> The Dubai Land Department fee for registering a developer's initial sale of a plot is 2% of the sale value for the purchaser and 2% for the seller, plus AED 10 knowledge and AED 10 innovation fees. Only the purchaser's share is included.</li>
<li><b>VAT.</b> The sale of bare land is exempt. The zero rate applies to the first sale or lease of a new residential building, not to construction services bought by an owner building their own home, so 5% is applied to design, construction, external works and contingency. The Federal Tax Authority's refund scheme for building new homes is open to UAE nationals only. Take advice from a UAE tax adviser for a real project.</li>
</ul>
</div></section>

<section class="chapter" aria-labelledby="c3"><header><b>03</b><span>The team</span></header><div>
<h2 id="c3">Choosing the architect on more than the fee</h2>
<p>We would help the owners shortlist three architects with villa experience and a registered consultant able to act as consultant of record. In this example their fee proposals look far apart until they are read side by side: one excludes interior coordination, another excludes the construction-stage duties of the consultant of record. Normalised, the gap closes to a few per cent.</p>
<p>The owners appoint the practice whose villas they like best and whose scope is complete, and appoint their interior designer at the same time, so joinery, lighting and services are designed together from the start. While they live in London through the design stage, we would run a fortnightly design meeting by video and keep a decision log they can read on their phones.</p>
</div></section>

<section class="chapter" aria-labelledby="c4"><header><b>04</b><span>Design to cost</span></header><div>
<h2 id="c4">If the concept comes back over budget</h2>
<p>Suppose the concept cost plan puts the design at about AED {k.CONCEPT_EST:.2f}m {MOD} against the AED {k.APPROVED:.2f}m of development allowances. Left alone, that gap would surface at tender, when it is far more expensive to fix. Instead we would run a value review with the architect and engineers.</p>
<div class="table-wrap"><table class="table"><thead><tr><th>Change</th><th class="num">Reduction (AED m)</th></tr></thead><tbody>{vr}</tbody><tfoot><tr><td>Total designed out before tender</td><td class="num">{k.VALUE_TOTAL:.2f} {MOD}</td></tr></tfoot></table></div>
<p>None of these changes would be visible from the garden or the water. The design would then go to Nakheel's design review and to permit, both submitted by the consultant of record, with the cost plan back within the allowances.</p>
</div></section>

<section class="chapter" aria-labelledby="c5"><header><b>05</b><span>Tender</span></header><div>
<h2 id="c5">Why the cheapest bid can be the most expensive</h2>
<p>In this example four contractors price the same drawings. On the headline numbers, Contractor A is AED 0.75m cheaper than the next lowest bid. Put on a like-for-like basis, adding back what each bid leaves out and correcting what each under-prices, it is the most expensive of the four.</p>
<figure class="chart-box"><ul class="legend"><li><i style="background:{k.C_ALT}"></i>Headline price</li><li><i style="background:{k.C_BUILD}"></i>Normalised, like-for-like</li></ul>{k.svg_bids()}<figcaption>Modelled bids for the main contract and external works, AED millions excluding VAT. Pre-tender estimate: AED {k.CONSTRUCTION:.2f}m.</figcaption></figure>
<div class="table-wrap"><table class="table"><thead><tr><th>Bid {MOD}</th><th class="num">Headline</th><th class="num">Normalised</th><th>What the comparison finds</th></tr></thead><tbody>{bids}</tbody></table></div>
<p>The owners would appoint Contractor B. In this example, after clarification and negotiation, the lump sum is agreed at AED {k.CONTRACT_SUM:.2f}m {MOD}, with ground risk, programme and a named site team written into the contract, and the long-lead glazing ordered as an early package.</p>
</div></section>

<section class="chapter" aria-labelledby="c6"><header><b>06</b><span>Construction</span></header><div>
<h2 id="c6">Nineteen months on site</h2>
<p>Every week the owners would receive a photo update; every month, a written report with progress, the forecast final cost, the risks and the decisions they need to make. The moments that would decide the final account might look like this.</p>
<ol class="events">{events}</ol>
<h3>The monthly report</h3>
<p>One page the owners can read in five minutes, wherever they are. This sample is for month 27 of the example; it is not an actual client report.</p>
<div class="report" role="img" aria-label="Sample monthly report for the worked example: progress 61% against 64% planned, modelled forecast final cost AED {r(k.REPORT_FORECAST):.2f}m against allowances of AED {k.APPROVED:.2f}m, three decisions due">
<header><b>Eastbridge · Sample monthly report</b><span class="small">Month 27 · Island E worked example</span></header>
<div class="r-body">
<div><h4>Progress {MOD}</h4><span class="big">61%</span> <span class="pill watch">3% behind</span><div class="bar"><i style="width:61%"></i><em style="left:64%"></em></div><span class="small muted">Planned 64%. Recovery plan agreed for fit-out.</span></div>
<div><h4>Forecast final cost {MOD}</h4><span class="big">AED {r(k.REPORT_FORECAST):.2f}m</span> <span class="pill ok">Within allowances</span><div class="bar"><i style="width:{round(k.REPORT_FORECAST / k.APPROVED * 100)}%"></i><em style="left:100%"></em></div><span class="small muted">Development allowances AED {k.APPROVED:.2f}m excluding VAT, with AED {r(k.APPROVED - r(k.REPORT_FORECAST)):.2f}m of contingency not yet committed.</span></div>
<div class="r-full"><h4>Decisions needed from you</h4><ul><li>Pool tile and coping sample, by the 14th</li><li>Kitchen joinery shop drawings, by the 18th</li><li>Garden lighting scheme, by the 25th</li></ul></div>
<div><h4>Payment recommendation {MOD}</h4><span>Valuation 12: AED 0.98m claimed, AED 0.91m recommended</span></div>
<div><h4>Top risk</h4><span>Shamal season during glazing installation; protection plan in place</span></div>
</div></div>
<p class="small muted" style="margin-top:12px">Sample only. Reports are tailored to each client.</p>
</div></section>

<section class="chapter" aria-labelledby="c7"><header><b>07</b><span>Handover</span></header><div>
<h2 id="c7">Keys, and nothing left to chase</h2>
<p>We would plan handover from the start of construction: walk the house room by room and system by system, attend the commissioning of the cooling, water, pool, lighting and security systems with the consultant and contractor, and issue the snag list in sections as areas finish, so that every item is closed before the owners accept the house.</p>
<p>The handover file should be complete on the day: completion certificate, as-built drawings, warranties, operation and maintenance manuals, test certificates, and a schedule of keys and codes. Retention would be released only when the defects period ends with nothing outstanding.</p>
</div></section>

<section class="chapter" aria-labelledby="c8"><header><b>08</b><span>Modelled outcome</span></header><div>
<h2 id="c8">The modelled final account</h2>
<p>Every figure in this chapter is modelled from the invented events above. It shows how a final account is reconciled, not a result Eastbridge has achieved.</p>
<h3>Construction changes {MOD}</h3>
<div class="table-wrap"><table class="table"><thead><tr><th>Construction, excluding VAT</th><th class="num">AED m</th></tr></thead><tbody>{out_html}</tbody><tfoot><tr><td>Modelled construction final account</td><td class="num">{k.CONSTRUCTION_OUT:.3f} {MOD}</td></tr></tfoot></table></div>
<p>Against the pre-tender estimate of AED {k.CONSTRUCTION:.2f}m, the modelled construction account draws AED {r(k.CONT_USED):.2f}m from the AED {k.A["contingency"]:.2f}m contingency, AED {k.OWNER_UPGRADES:.2f}m of it on upgrades the owners chose. Handover is four weeks later than the original programme, the extension agreed.</p>
<h3>Stated allowances against the modelled outcome</h3>
<div class="table-wrap"><table class="table"><thead><tr><th>AED m</th><th class="num">Stated allowances</th><th class="num">Modelled outcome</th></tr></thead><tbody>{recon_rows}</tbody><tfoot><tr><td>Subtotal (excludes Eastbridge's fee and the items awaiting quotation)</td><td class="num">{r(k.STATED_SUBTOTAL):.2f}</td><td class="num">{r(k.OUTTURN_ALL):.2f} {MOD}</td></tr></tfoot></table></div>
<p>The difference between the two columns is the AED {r(k.CONT_LEFT):.2f}m of contingency the example never draws, plus the VAT on it. It is unspent contingency, not a separate saving.</p>
<h3>Modelled cost avoidance</h3>
<p>Each line compares one decision in the example with one hypothetical alternative. The alternatives use different baselines, so the lines are not added together, not added to the unspent contingency, and are not a demonstrated return on Eastbridge's fee.</p>
<div class="table-wrap"><table class="table"><thead><tr><th>Hypothetical comparison</th><th class="num">AED m</th></tr></thead><tbody>{avoided}</tbody></table></div>
<h3>The programme</h3>
<figure class="chart-box"><ul class="legend"><li><i style="background:{k.C_PLOT}"></i>Pre-construction stages</li><li><i style="background:{k.C_BUILD}"></i>Construction</li></ul>{k.svg_programme()}<figcaption>Assumed programme, in months from a plot review in October 2026. Construction assumes site access from early 2028. That is our planning assumption, not a Nakheel commitment: on a new island, the programme moves with the developer's infrastructure dates.</figcaption></figure>
</div></section>

<section class="chapter" aria-labelledby="c9"><header><b>09</b><span>Method</span></header><div>
<h2 id="c9">How this worked example was built</h2>
<p class="small">The price per square foot, payment schedule, floors, height limit and floor area ratio are Nakheel's published Island E figures (price and payment plan sheet and draft development control regulations, 24 September 2026); the plot size and price are an example within them. Construction rates sit within published Dubai ranges: Engel &amp; Völkers (December 2025) and Real Estate Club Dubai. Design fees sit within the 6–12% range published by Optimal Engineering. Registration fees are the Dubai Land Department's published fees; VAT treatment follows the Federal Tax Authority's real estate guide. The family, the contractors, the events and every modelled outcome are invented to show how we work and how the numbers move.</p>
<ul class="small"><li>Nakheel: Bay Estate, Island E price and payment plan sheet, masterplan and draft development control regulations, issued 24 September 2026</li><li><a href="{k.DLD_URL}" rel="noopener">Dubai Land Department: registering the initial sale of off-plan units and land plots</a></li><li><a href="{k.VAT_GUIDE_URL}" rel="noopener">Federal Tax Authority: VAT real estate guide</a></li><li><a href="https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai" rel="noopener">Engel &amp; Völkers: construction cost in Dubai</a></li><li><a href="https://realestateclubdubai.com/dubai-villa-architects" rel="noopener">Real Estate Club Dubai: villa architects, fees and timelines</a></li><li><a href="https://www.optimal.ae/blog/cost-to-build-a-villa-in-dubai" rel="noopener">Optimal Engineering: cost to build a villa in Dubai</a></li></ul>
</div></section>
</div>
{B.cta_band("Buying on Island E?", "Send us the plot number, or the plots you are choosing between. We will tell you what the draft rules allow and what a complete budget needs to cover.", "saqqara-04")}'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": "How we would manage an Island E villa: a worked project example (hypothetical)",
           "description": "A hypothetical worked example, not a completed project: budget structure, cash-flow plan, tender comparison and programme for a waterfront villa on Island E, Dubai Islands.",
           "author": {"@id": B.PERSON_ID}, "publisher": {"@id": B.ORG_ID}, "mainEntityOfPage": B.url(path),
           "image": B.url(B.og_image("saqqara-01")), "inLanguage": "en-GB", "about": "Villa construction project management, Dubai Islands",
           "genre": "Worked example"}
    B.page(path, "Island E Villa: Worked Project Example | Eastbridge",
           "A hypothetical worked example of how we would manage an Island E villa on Dubai Islands: budget structure, cash flow, tender comparison and programme review.",
           body, crumbs, [art], og=B.og_image("saqqara-01"))
