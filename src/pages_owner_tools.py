"""Three owner-side planning tools under /tools/ (competitor brief, item 7):

  /tools/renovate-or-rebuild/      renovation against knock-down-and-rebuild: cost per sq ft of finished space,
                                   time and approvals (rates shared with the cost calculator in pages_tools.RATES)
  /tools/stage-payment-planner/    a build budget spread over a typical payment schedule: advance, monthly
                                   valuations, retention and its release, with a monthly exposure table and chart
  /tools/delay-cost-estimator/     what each month of delay costs an owner: housing, finance, price escalation,
                                   the contractor's extended site costs and continuing fees

Each page embeds its numbers as JSON (#tool-data) for src/static/assets/tools.js, and every word the script writes
comes from the hidden #tool-msgs list, so the i18n pipeline translates it with the rest of the page. The server
renders the default example with the Python mirrors below (estimate_rr, plan_sp, estimate_dc); tools.js updates the
same nodes in place and must produce identical figures (tools/tools_check.js compares them).
"""
import json
import math
import html as H
import build as B
import config as C
import pages_tools as PT

esc = H.escape
RR_PATH = "/tools/renovate-or-rebuild/"
SP_PATH = "/tools/stage-payment-planner/"
DC_PATH = "/tools/delay-cost-estimator/"
RR_ARTICLE = "/insights/renovate-or-rebuild-villa-dubai/"
STALLED = "/insights/stalled-villa-project-dubai/"
SITE_HOST = PT.SITE_HOST

# ---------------------------------------------------------------- sources (in addition to pages_tools.SOURCES)
EXTRA_SOURCES = [
    ("srb", "Smart Renovation, How much does villa renovation cost in Dubai? Full price breakdown (2026): AED per sq ft by scope",
     "https://smartrenovation.ae/how-much-does-villa-renovation-cost-in-dubai-full-price-breakdown-2026/"),
    ("evr", "Engel & Völkers, Average villa rental prices in Dubai (2026), data from Property Monitor, updated 21 May 2026",
     "https://www.engelvoelkers.com/ae/en/resources/villa-rental-prices"),
    ("dla", "DLA Piper, Global Construction Bulletin: Security of payment, UAE (October 2025)",
     "https://www.dlapiper.com/en/insights/publications/global-construction-bulletin/2025/september-2025/security-of-payment-uae"),
    ("tam", "Al Tamimi & Company, Highlights of the laws of the UAE, the PRC and the common law applicable to construction contracts, part 2 (2011)",
     "https://www.tamimi.com/law-update-articles/highlights-of-the-laws-of-the-united-arab-emirates-the-peoples-republic-of-china-and-the-common-law/"),
    ("cbuae", "Central Bank of the UAE, CBUAE raises the Base Rate by 25 basis points (16 September 2026)",
     "https://centralbank.ae/media/dv3bo3ed/cbuae-raises-the-base-rate-by-25-basis-points-en.pdf"),
    ("dmp", "Dubai Municipality, Residential buildings: building permit procedures",
     "https://stgportalnew.dm.gov.ae/wp-content/uploads/2020/06/Residential-Buildings_Building-Permits-Procedures.pdf"),
    ("dbc", "Dubai Decree No. (45) of 2021 concerning the Dubai Building Code (Dubai Legislation Portal)",
     "https://dlp.dubai.gov.ae/Legislation%20Reference/2021/Decree%20No.%20(45)%20of%202021%20Concerning%20the%20Dubai%20Building%20Code.html"),
]
ALL_SOURCES = {k: (t, u) for k, t, u in PT.SOURCES + EXTRA_SOURCES}

class Cites:
    """Numbered citations for one page: numbers follow the order of first use; sources_html() lists them."""
    def __init__(self):
        self.order = []
    def __call__(self, *keys):
        out = ""
        for k in keys:
            if k not in self.order:
                self.order.append(k)
            n = self.order.index(k) + 1
            out += f'<sup><a href="#src-{k}" aria-label="Source {n}">[{n}]</a></sup>'
        return out
    def sources_html(self):
        items = "".join(f'<li id="src-{k}">{esc(ALL_SOURCES[k][0])}. <a href="{ALL_SOURCES[k][1]}" rel="{PT.rel_of(k)}">'
                        f'{esc(ALL_SOURCES[k][1].split("//", 1)[1].split("/", 1)[0])}</a></li>' for k in self.order)
        return f'<ol class="calc-sources">{items}</ol>'
    def urls(self):
        return [ALL_SOURCES[k][1] for k in self.order]

# ---------------------------------------------------------------- shared figures
R = PT.RATES
# Smart Renovation's price breakdown, AED per sq ft of existing floor area. Luxury is published only as "450 or more"
# (None = no published ceiling: only the starting column is shown, like the luxury band in the cost calculator).
RENO_RATES = {
    "basic": {"label": "Basic refresh", "rate": [120, 250], "months": R["reno"]["standard"]["months"], "soft": False},
    "mid": {"label": "Mid-range: kitchens, bathrooms and interiors", "rate": [250, 450], "months": R["reno"]["premium"]["months"], "soft": True},
    "lux": {"label": "Luxury or structural", "rate": [450, None], "months": R["reno"]["luxury"]["months"], "soft": True},
}
# Engel & Völkers (data from Property Monitor), average annual villa rent in Dubai, May 2026 year to date.
RENT_ANNUAL = {"3": 212220, "4": 343461, "5": 546924}
def jr(x):
    """Round half up, like Math.round in tools.js (Python's round() rounds half to even)."""
    return int(math.floor(x + 0.5))
def rent_month(beds):
    return int(jr(RENT_ANNUAL[beds] / 12 / 100) * 100)
RENT_DEFAULT = rent_month("4")                     # AED 28,620 a month
BASE_RATE = 3.9                                    # CBUAE Base Rate from 17 September 2026 (a floor, not a loan rate)
EXAMPLE_CONS = PT.estimate(PT.EXAMPLE)["construction"][1]   # the cost calculator's worked example, construction only
# Construction inflation forecasts for 2026 (% a year): Currie & Brown UAE about 3% (via PRASOON); Turner & Townsend
# Dubai 4%, Abu Dhabi 5%. Low = Currie & Brown, high = Turner & Townsend for the emirate, likely = the midpoint.
ESCALATION = {"dubai": [3.0, 3.5, 4.0], "ad": [3.0, 4.0, 5.0]}
# Turner & Townsend 2025: preliminaries on a 2,500 m² project, Dubai 12%, Abu Dhabi 15% of construction cost.
PRELIMS = {"dubai": 0.12, "ad": 0.15}
# Construction phase from the cost calculator's timeline (8-14 months). High monthly cost = the shortest build.
BUILD_MONTHS = [R["time"]["build"][1], sum(R["time"]["build"]) / 2, R["time"]["build"][0]]

def rnd100(x):
    return int(math.floor(x / 100 + 0.5) * 100)

def aed(x):
    return f"AED {int(x):,}"

def num(x):
    return f"{x:,.0f}"

def months_txt(x):
    return f"{x:g} months"

def common_msgs():
    return [("money", "AED {n}"), ("notIncluded", "Not included"), ("printed", "Prepared on {date}"),
            ("unit-sqft", "sq ft"), ("unit-m2", "m²"), ("monthsN", "{n} months"), ("monthsPlus", "{n}+ months"),
            ("jsNote", "Figures update as you change the inputs.")]

def msgs_html(m):
    items = "".join(f'<li data-m="{k}">{v}</li>' for k, v in m)
    return f'<div class="calc-msgs" id="tool-msgs" hidden><ul>{items}</ul></div>'

def print_head(title):
    return f'''<div class="print-only calc-print-head">
<p class="calc-print-brand"><img src="/assets/logo.png" alt="" width="40" height="40"><span>{esc(C.NAME)}</span></p>
<p class="calc-print-title">{title}</p>
<p class="calc-print-meta" data-print-date></p>
<h3 class="calc-h">Your inputs</h3>
<dl class="calc-print-inputs" data-print-inputs></dl>
</div>'''

def print_foot(path, names):
    return f'''<div class="print-only calc-print-foot">
<p><b>Sources.</b> {names} Full sources, assumptions and method: {SITE_HOST}{path}#sources</p>
<p class="calc-print-contact"><b>{esc(C.NAME)}</b> · Client-side project management for private villas in Dubai and Abu Dhabi · {C.EMAIL} · {C.PHONE_DISPLAY} · {SITE_HOST}</p>
</div>'''

def actions_html(wa_text):
    return f'''<div class="calc-actions" data-tool-actions hidden>
<p class="calc-h">Keep or discuss this result</p>
<div class="calc-actions__row">
<button type="button" class="btn btn--ghost btn--sm" data-print>Save as PDF</button>
<a class="btn btn--ghost btn--sm" href="{B.wa_link(wa_text)}" rel="noopener">Discuss on WhatsApp</a>
<a class="btn btn--sm" href="/contact/">Ask us to check it</a>
</div></div>'''

def other_tools(current):
    tools = [(PT.CALC_PATH, "Villa build and renovation cost calculator", "Low, likely and high costs with fees, approvals, contingency and a timeline."),
             (RR_PATH, "Renovate or rebuild?", "Renovation against knock-down-and-rebuild, per sq ft of finished space."),
             (SP_PATH, "Stage payment planner", "A build budget spread over a typical payment schedule, month by month."),
             (DC_PATH, "Delay cost estimator", "What each month of delay costs an owner.")]
    items = "".join(f'<li><a href="{p}"><b>{t}</b><span>{d}</span></a></li>' for p, t, d in tools if p != current)
    return f'''<section class="section--tight"><div class="wrap split"><div><h2>Other tools</h2></div><div>
<ul class="read-list">{items}<li><a href="/tools/"><b>All tools</b><span>Free planning tools for villa owners, each with its sources.</span></a></li></ul>
</div></div></section>'''

def unit_field():
    return '''<fieldset><legend>Units</legend><div class="calc-seg calc-seg--sm">
<label><input type="radio" name="unit" value="sqft" checked><span>sq ft</span></label>
<label><input type="radio" name="unit" value="m2"><span>m²</span></label></div></fieldset>'''

def money_field(name, label, value, hint, step=1000, hid=None):
    hid = hid or f"t-{name}-hint"
    return (f'<div><label for="t-{name}">{label}</label><input id="t-{name}" name="{name}" type="number" inputmode="numeric" min="0" '
            f'step="{step}" value="{value}" aria-describedby="{hid}"><p class="hint" id="{hid}">{hint}</p></div>')

def schema_app(path, name, desc, cites):
    return {"@context": "https://schema.org", "@type": "WebApplication", "@id": B.url(path) + "#app",
            "name": name, "url": B.url(path), "description": desc,
            "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
            "inLanguage": "en-GB", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"},
            "publisher": {"@id": B.ORG_ID}, "provider": {"@id": B.ORG_ID}, "citation": cites.urls()}

def tool_page(path, kind, crumb, h1, lede, form, out, data, body_after, title, desc, schema_name, schema_desc, faqs, cites):
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (crumb, path)]
    head = B.page_head(crumbs, h1, lede).replace('class="page-head"', 'class="page-head page-head--tool"', 1)
    body = head + f'''
<section class="section--tight calc-sec tool-sec"><div class="wrap calc tool" data-tool="{kind}">
{form}
{out}
</div></section>
<script type="application/json" id="tool-data">{json.dumps(data, separators=(",", ":"))}</script>
<script src="/assets/tools.js" defer></script>
{body_after}
<section class="section--tight paper"><div class="wrap split"><div><h2>Questions</h2></div><div>{B.faq_html(faqs)}</div></div></section>
<section class="section--tight" id="sources"><div class="wrap split"><div><h2>Sources</h2></div><div class="prose">
{cites.sources_html()}
<p class="small muted">Rates last reviewed {PT.month_year(PT.RATES_REVIEWED)} by {esc(C.FOUNDER["name"])}. This page gives general information, not financial, legal or engineering advice.</p>
</div></div></section>
{other_tools(path)}
{B.cta_band("Want a second pair of eyes on the numbers?")}'''
    schema = [schema_app(path, schema_name, schema_desc, cites), B.faq_schema(faqs)]
    B.page(path, title, desc, body, crumbs, schema)

# ================================================================ 1. renovate or rebuild
RR_EXAMPLE = {"area": 6000, "newArea": 6000, "scope": "mid", "tier": "premium", "living": True, "rent": RENT_DEFAULT}
RR_RENO_LINES = [("works", "Renovation works"), ("design", "Design and engineering fees"), ("permits", "Approvals, NOCs and connections"),
                 ("contingency", "Contingency"), ("living", "Living elsewhere during the works")]
RR_NEW_LINES = [("demo", "Demolition of the existing villa"), ("build", "New villa (shell, MEP and finishes)"),
                ("design", "Design and engineering fees"), ("permits", "Approvals, NOCs and connections"),
                ("contingency", "Contingency"), ("living", "Living elsewhere from demolition to keys")]

def tri(p):
    return [p[0], (p[0] + p[1]) / 2, p[1]]

def estimate_rr(i):
    """Mirror of rr() in tools.js. Areas in sq ft. Every line is rounded (pages_tools.rnd) and totals are sums."""
    rv = RENO_RATES[i["scope"]]
    lo, hi = rv["rate"]
    low_only = hi is None
    rate = [lo, lo, lo] if low_only else tri([lo, hi])
    ix = [0, 0, 0] if low_only else [0, 1, 2]     # starting figures only: every column uses the low percentages
    z = [0, 0, 0]
    rn = {"works": [i["area"] * r for r in rate]}
    rn["design"] = [rn["works"][n] * R["design"][ix[n]] for n in range(3)] if rv["soft"] else z
    rn["permits"] = [R["permitsFixed"][ix[n]] for n in range(3)] if rv["soft"] else z
    rn["contingency"] = [rn["works"][n] * R["contingency"][ix[n]] for n in range(3)]
    m0, m1 = rv["months"]
    rmonths = [m0, m0, m0] if m1 is None else tri([m0, m1])
    rn["living"] = [i["rent"] * m for m in rmonths] if i["living"] else z
    t = R["tiers"][i["tier"]]
    nb = {"demo": tri(R["demo"]), "build": [i["newArea"] * r for r in tri(t["nb"])]}
    cons = [nb["demo"][n] + nb["build"][n] for n in range(3)]
    nb["design"] = [cons[n] * R["design"][n] for n in range(3)]
    nb["permits"] = list(R["permitsFixed"])
    nb["contingency"] = [cons[n] * R["contingency"][n] for n in range(3)]
    tm = R["time"]
    away = [tm["build"][0] + tm["snag"][0], 0, tm["build"][1] + tm["snag"][1]]
    away[1] = (away[0] + away[2]) / 2
    nb["living"] = [i["rent"] * m for m in away] if i["living"] else z
    lux = i["tier"] in ("luxury", "ultra")
    if lux:
        total_m = tri(tm["luxTotal"])
    else:
        a = sum(tm[k][0] for k in ("design", "approvals", "build", "snag"))
        b = sum(tm[k][1] for k in ("design", "approvals", "build", "snag"))
        total_m = tri([a, b])
    out = {"rn": {k: [PT.rnd(v) for v in rn[k]] for k, _ in RR_RENO_LINES},
           "nb": {k: [PT.rnd(v) for v in nb[k]] for k, _ in RR_NEW_LINES}}
    for s, lines in (("rn", RR_RENO_LINES), ("nb", RR_NEW_LINES)):
        out[s]["total"] = [sum(out[s][k][n] for k, _ in lines) for n in range(3)]
    out["rn"]["months"] = rmonths
    out["rn"]["away"] = rmonths
    out["nb"]["months"] = total_m
    out["nb"]["away"] = away
    out["lowOnly"] = low_only
    out["rn"]["rate"] = [out["rn"]["total"][n] / i["area"] if i["area"] else 0 for n in range(3)]
    out["nb"]["rate"] = [out["nb"]["total"][n] / i["newArea"] if i["newArea"] else 0 for n in range(3)]
    return out

def rate_txt(x):
    return aed(int(jr(x / 10) * 10))

def cell_txt(arr, n):
    """A low/likely/high cell; a line that is zero in every column reads "Not included" (as tools.js cells())."""
    if arr[0] == 0 and arr[2] == 0:
        return "Not included" if n == 1 else "–"
    return aed(arr[n])

def rr_table(side, lines, e, caption):
    rows = "".join(f'<tr data-row="{side}-{k}"><th scope="row">{lbl}</th>' +
                   "".join(f'<td data-v="{side}-{k}-{n}">{cell_txt(e[side][k], n)}</td>' for n in range(3)) + "</tr>"
                   for k, lbl in lines)
    def mrow(key, label, attr=""):
        return (f'<tr class="tool-meta"><th scope="row"{attr}>{label}</th>' +
                "".join(f'<td data-v="{side}-{key}-{n}">{months_txt(e[side][key][n])}</td>' for n in range(3)) + "</tr>")
    rate = (f'<tr class="tool-meta"><th scope="row" data-rate-label="{side}">Total per sq ft of finished space</th>' +
            "".join(f'<td data-v="{side}-rate-{n}">{rate_txt(e[side]["rate"][n])}</td>' for n in range(3)) + "</tr>")
    when = "Start of works to completion" if side == "rn" else "Start of design to keys"
    away = "Months out of the house"
    return f'''<div class="table-wrap"><table class="table calc-table"><caption class="sr">{caption}</caption>
<thead><tr><th scope="col">{caption}</th><th scope="col" class="num">Low</th><th scope="col" class="num">Likely</th><th scope="col" class="num">High</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><th scope="row">Total</th>{"".join(f'<td data-v="{side}-total-{n}">{aed(e[side]["total"][n])}</td>' for n in range(3))}</tr>
{rate}{mrow("months", when)}{mrow("away", away)}</tfoot></table></div>'''

def rr_verdict(e):
    d = e["nb"]["total"][1] - e["rn"]["total"][1]
    pct = jr(abs(d) / e["rn"]["total"][1] * 100) if e["rn"]["total"][1] else 0
    key = "verdict-more" if d >= 0 else "verdict-less"
    txt = RR_MSG[key].format(diff=aed(abs(d)), pct=f"{pct}%")
    return txt + " " + RR_MSG["verdict-rate"].format(rb=rate_txt(e["nb"]["rate"][1]), rn=rate_txt(e["rn"]["rate"][1]), unit="sq ft")

RR_MSG = {
    "verdict-more": "In the likely case, knocking down and rebuilding costs about {diff} more than renovating ({pct} more).",
    "verdict-less": "In the likely case, knocking down and rebuilding costs about {diff} less than renovating ({pct} less).",
    "verdict-from": "Luxury and structural renovations are published only as a starting rate, so this compares starting figures: renovating from {rn}, rebuilding from {rb}.",
    "verdict-rate": "Per {unit} of finished space, the rebuild works out at {rb} against {rn} for the renovation.",
    "verdict-bigger": "The rebuild also adds {extra} of floor area, which renovating the existing villa does not.",
    "enterArea": "Enter the existing built-up area to compare the two.",
    "cardRate-sqft": "{rate} per sq ft of finished space",
    "cardRate-m2": "{rate} per m² of finished space",
}

def scope_note(v, unit):
    lo, hi = v["rate"]
    if unit == "m2":
        lo, hi, u = PT.per_m2(lo), (PT.per_m2(hi) if hi else None), "m²"
    else:
        u = "sq ft"
    return f"AED {lo:,}–{hi:,} per {u}" if hi else f"From AED {lo:,} per {u}"

def rr_msgs():
    m = common_msgs() + list(RR_MSG.items())
    m += [("rateLabel-sqft", "Total per sq ft of finished space"), ("rateLabel-m2", "Total per m² of finished space")]
    for k, v in RENO_RATES.items():
        m += [(f"scope-{k}-sqft", scope_note(v, "sqft")), (f"scope-{k}-m2", scope_note(v, "m2"))]
    for k, t in R["tiers"].items():
        m += [(f"tier-{k}-sqft", PT.tier_new_note(t, "sqft")), (f"tier-{k}-m2", PT.tier_new_note(t, "m2"))]
    return m

def rr_form():
    scopes = "".join(f'<label class="calc-opt"><input type="radio" name="scope" value="{k}"{" checked" if k == RR_EXAMPLE["scope"] else ""}>'
                     f'<span><b>{esc(v["label"])}</b><small data-scope-note="{k}">{scope_note(v, "sqft")}</small></span></label>'
                     for k, v in RENO_RATES.items())
    tiers = "".join(f'<label class="calc-opt"><input type="radio" name="tier" value="{k}"{" checked" if k == RR_EXAMPLE["tier"] else ""}>'
                    f'<span><b>{esc(v["label"])}</b><small data-tier-note="{k}">{PT.tier_new_note(v, "sqft")}</small></span></label>'
                    for k, v in R["tiers"].items())
    return f'''<form class="calc-in tool-in" id="tool-form" novalidate onsubmit="return false">
{unit_field()}
<div class="calc-row"><div><label for="t-area">Existing built-up area (<span data-unit>sq ft</span>)</label><input id="t-area" name="area" type="number" inputmode="numeric" min="0" step="50" value="{RR_EXAMPLE["area"]}" data-area></div>
<div><label for="t-newArea">Built-up area after a rebuild (<span data-unit>sq ft</span>)</label><input id="t-newArea" name="newArea" type="number" inputmode="numeric" min="0" step="50" value="{RR_EXAMPLE["newArea"]}" data-area aria-describedby="t-newArea-hint"></div></div>
<p class="hint" id="t-newArea-hint">A rebuild can sometimes add floor area, within the plot's permitted built-up area and the master developer's rules. Check them with your consultant before relying on it.</p>
<fieldset><legend>Renovation scope</legend><div class="calc-tiers">{scopes}</div>
<p class="hint">Rates per sq ft of the existing villa, from a published 2026 price breakdown. A basic refresh carries no design fees or approvals allowance.</p></fieldset>
<fieldset><legend>Rebuild specification</legend><div class="calc-tiers">{tiers}</div>
<p class="hint">The same construction rates as our cost calculator. Demolition of the existing villa is always included.</p></fieldset>
<fieldset><legend>Living elsewhere</legend>
<div class="calc-checks"><label><input type="checkbox" name="living" checked> Include the cost of living elsewhere while the house is unusable</label></div>
{money_field("rent", "Monthly rent or hotel cost (AED)", RR_EXAMPLE["rent"], f"The default is the average Dubai rent for a four-bedroom villa, AED {RENT_ANNUAL['4']:,} a year (May 2026). Three bedrooms: AED {RENT_ANNUAL['3']:,}; five bedrooms: AED {RENT_ANNUAL['5']:,}.", step=500)}
</fieldset>
{msgs_html(rr_msgs())}
</form>'''

def rr_out(e):
    d = e["nb"]["total"][1] - e["rn"]["total"][1]
    return f'''<div class="calc-out" id="tool-out">
{print_head("Renovate or rebuild: indicative comparison")}
<div class="tool-compare">
<div class="tool-card"><p class="calc-label">Renovate, likely total</p><p class="calc-total"><b data-out="rn-likely">{aed(e["rn"]["total"][1])}</b>
<span class="calc-range">Range <span data-out="rn-low">{aed(e["rn"]["total"][0])}</span> to <span data-out="rn-high">{aed(e["rn"]["total"][2])}</span></span></p>
<p class="calc-sub" data-out="rn-rate">{RR_MSG["cardRate-sqft"].format(rate=rate_txt(e["rn"]["rate"][1]))}</p></div>
<div class="tool-card"><p class="calc-label">Knock down and rebuild, likely total</p><p class="calc-total"><b data-out="nb-likely">{aed(e["nb"]["total"][1])}</b>
<span class="calc-range">Range <span data-out="nb-low">{aed(e["nb"]["total"][0])}</span> to <span data-out="nb-high">{aed(e["nb"]["total"][2])}</span></span></p>
<p class="calc-sub" data-out="nb-rate">{RR_MSG["cardRate-sqft"].format(rate=rate_txt(e["nb"]["rate"][1]))}</p></div>
</div>
<p class="tool-verdict" data-out="verdict" aria-live="polite">{rr_verdict(e)}</p>
<p class="calc-reviewed">Rates last reviewed: {PT.month_year(PT.RATES_REVIEWED)}, by {esc(C.FOUNDER["name"])}</p>
<h3 class="calc-h tool-h-side">Renovate</h3>
{rr_table("rn", RR_RENO_LINES, e, "Renovation")}
<h3 class="calc-h tool-h-side">Knock down and rebuild</h3>
{rr_table("nb", RR_NEW_LINES, e, "Knock down and rebuild")}
<h3 class="calc-h">Approvals</h3>
<ul class="tool-approvals">
<li><b>Renovate.</b> Cosmetic work often needs no permit, though your master developer may still require an NOC. Structural changes, extensions, façade changes and a new pool need the master developer's NOC and a permit from Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits.</li>
<li><b>Rebuild.</b> Approval to demolish, then the full sequence for a new villa: design to the current Dubai Building Code, authority NOCs, the building permit, staged inspections and a completion certificate before connection.</li>
</ul>
<p class="calc-note calc-js" data-js-note>Showing the example below. Switch on JavaScript to change the inputs.</p>
<p class="calc-flag">An indicative comparison from published market ranges, not a quotation. Each line is rounded and the totals are the sum of the lines. Excludes the plot, pool, landscaping, furniture, finance, VAT, inflation and advisers' fees, including ours. <a href="#sources">Sources and assumptions</a></p>
{actions_html("Hello, I used your renovate or rebuild tool and would like to talk through my villa.")}
{print_foot(RR_PATH, "Renovation rates: Smart Renovation. New-build rates, fees, contingency and approvals: the Eastbridge cost calculator (Engel &amp; Völkers, Optimal Engineering, Knight Frank, Turner &amp; Townsend). Demolition and timeline: a property information website. Rents: Engel &amp; Völkers.")}
</div>'''

def renovate_or_rebuild():
    c = Cites()
    e = estimate_rr(RR_EXAMPLE)
    srb, opt, ev, kf, tt, reca, recc, sr, evr, dmp, dbc = (c("srb"), c("opt"), c("ev"), c("kf"), c("tt"), c("reca"), c("recc"),
                                                           c("sr"), c("evr"), c("dmp"), c("dbc"))
    after = f'''<section class="section--tight paper"><div class="wrap split"><div><h2>How the comparison works</h2></div><div class="prose">
<p>The short answer: on a sound villa, renovating is usually cheaper per square foot of finished space than knocking down and rebuilding, because the structure stays. The gap narrows when the renovation is deep (new services, waterproofing, structural changes) and when a rebuild adds floor area the existing villa cannot. Our <a href="{RR_ARTICLE}">guide to renovating or rebuilding a Dubai villa</a> explains how to decide.</p>
<ol>
<li><strong>Renovation works.</strong> Existing built-up area multiplied by Smart Renovation's published rate for the scope: AED 120–250 per sq ft for a basic renovation, AED 250–450 for mid-range and AED 450 or more for luxury work with structural changes.{srb} Luxury has no published ceiling, so the tool then shows starting figures only.</li>
<li><strong>Rebuild.</strong> The new built-up area at the cost calculator's construction rates for the chosen specification,{ev}{kf}{opt}{tt} plus demolition of the existing villa at AED 50,000–200,000.{recc}</li>
<li><strong>Design fees, approvals and contingency</strong> follow the cost calculator: design and engineering 6–12% of construction,{opt} a fixed AED 25,000–75,000 approvals band (our own assumption for a straightforward villa),{recc} and a 10–15% contingency{ev}{opt} with 12% as the likely figure. A basic renovation carries no design fees or approvals allowance.</li>
<li><strong>Time.</strong> Renovation works take two to three months for a basic refresh, four to six for kitchens, bathrooms and interiors, and six months or longer for structural work.{sr} A rebuild runs through design (3–4 months), approvals (2–3), construction (8–14) and snagging (1–2), and 24–36 months from plot to keys for a custom luxury villa.{reca} Demolition is assumed to sit within the construction phase.</li>
<li><strong>Living elsewhere.</strong> The monthly cost you enter, multiplied by the months the house cannot be lived in: the renovation works, or construction and snagging for a rebuild (you can usually stay in the old villa while the new one is designed and approved). The default is Engel &amp; Völkers' average Dubai rent for a four-bedroom villa, AED {RENT_ANNUAL["4"]:,} a year as of May 2026, from Property Monitor data.{evr}</li>
</ol>
<p>On approvals, a rebuild goes through the whole residential permit sequence: drawings and fees submitted by your registered consultant, authority NOCs, the permit, staged inspections, a joint completion inspection and the completion certificate before service connection.{dmp} The new design must meet the current Dubai Building Code.{dbc} A renovation that leaves structure and façade alone avoids most of that.</p>
</div></div></section>
<section class="section--tight"><div class="wrap split"><div><h2>Worked example</h2><p class="muted">A 6,000 sq ft villa: a mid-range renovation against a premium rebuild of the same size, with the family renting a four-bedroom villa meanwhile. This is what the tool shows when it first loads.</p></div><div class="prose">
<p>Renovating is likely to cost {aed(e["rn"]["total"][1])}, about {rate_txt(e["rn"]["rate"][1])} per sq ft of finished space, with the family out of the house for around {e["rn"]["away"][1]:g} months. Rebuilding is likely to cost {aed(e["nb"]["total"][1])}, about {rate_txt(e["nb"]["rate"][1])} per sq ft, and around {e["nb"]["months"][1]:g} months from the start of design to keys.</p>
<p>The rebuild buys a new structure, new services and a layout designed for how the family lives now, which a mid-range renovation does not. Whether that is worth the difference depends on the condition of the existing villa, which no calculator can see. A condition survey and some opening-up of the existing building, before any design is fixed, is the cheapest way to find out.</p>
</div></div></section>
<section class="section--tight paper"><div class="wrap split"><div><h2>Assumptions</h2></div><div class="prose"><ul>
<li>The likely figure for each rate is the midpoint of the published range; contingency uses 12%.</li>
<li>Renovation rates apply to the existing built-up area; the rebuild rate applies to the built-up area after the rebuild.</li>
<li>Pool, landscaping, smart home and furniture are left out of both options, because they can be kept, reused or replaced either way. Use the <a href="{PT.CALC_PATH}">cost calculator</a> to add them.</li>
<li>Demolition (AED 50,000–200,000) and the phase-by-phase timeline are the only published figures we have found, from a property information website.</li>
<li>Living elsewhere uses the same monthly cost in every column; only the number of months changes. The likely number of months is the midpoint. On a luxury renovation the published duration is "six months or longer", so the starting figure is used.</li>
<li>Each cost line is rounded to the nearest AED 1,000, or AED 10,000 above AED 1 million. Totals are the sums of the rounded lines.</li>
</ul></div></div></section>'''
    data = {"kind": "rr", "sqftPerM2": PT.SQFT_PER_M2, "reno": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in RENO_RATES.items()},
            "tiers": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in R["tiers"].items()},
            "demo": R["demo"], "design": R["design"], "contingency": R["contingency"], "permitsFixed": R["permitsFixed"], "time": R["time"]}
    faqs = [
        ("Is it cheaper to renovate or rebuild a villa in Dubai?",
         "Usually cheaper to renovate, if the structure is sound. Published 2026 renovation rates run from about AED 120–250 per sq ft for basic work to AED 250–450 for mid-range and AED 450 or more for luxury or structural work (Smart Renovation), while new-build construction runs from about AED 300–500 per sq ft at a standard specification to AED 850–1,200 or more for luxury, before demolition, fees and contingency. A deep renovation of an older villa can close much of that gap."),
        ("How long does a rebuild take compared with a renovation?",
         "Renovation works typically take two to six months, longer for structural changes. A rebuild goes through design, approvals, construction and snagging, about 14–23 months end to end on published phase estimates and 24–36 months for a custom luxury villa. You can usually stay in the old villa while the new one is designed and approved, so the months out of the house are fewer than the total."),
        ("Do I need a permit to demolish and rebuild my villa?",
         "Yes. Demolition needs approval, and the new villa needs a full building permit through Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits, usually after your master developer's NOC. Your DM-registered consultant handles the submissions. A purely cosmetic renovation often needs no permit, though the master developer may still require an NOC."),
        ("Can I build a bigger villa if I knock down the old one?",
         "Sometimes. The plot's permitted built-up area, setbacks and height, and the master developer's own rules, set the limit. Check them with your consultant and the master developer before you assume extra floor area, because it is often the deciding factor in favour of rebuilding."),
        ("How accurate is this comparison?",
         "It is indicative, built from published market ranges, and it cannot see the condition of your villa. Use it to frame the decision, then test it with a condition survey, opening-up and a proper cost plan for each option before committing."),
    ]
    tool_page(RR_PATH, "rr", "Renovate or rebuild", "Renovate or rebuild your villa?",
              "Compare renovating a Dubai or Abu Dhabi villa with knocking it down and rebuilding: cost per square foot of finished space, time and approvals, low, likely and high. Every rate is sourced; it is an estimate, not a quote.",
              rr_form(), rr_out(e), data, after,
              "Renovate or Rebuild a Villa in Dubai? Costs | Eastbridge",
              "Compare renovating a Dubai villa with knocking down and rebuilding: cost per sq ft of finished space, time and approvals, low to high, all sourced.",
              "Renovate or rebuild: villa cost comparison (Dubai and Abu Dhabi)",
              "Compares renovating a villa with knocking it down and rebuilding: low, likely and high totals, cost per square foot of finished space, time and approvals, from published market ranges.",
              faqs, c)

# ================================================================ 2. stage payment planner
SP_EXAMPLE = {"contract": EXAMPLE_CONS, "months": 12, "advance": 10.0, "retention": 10.0, "dlp": 12, "profile": "s"}
PROFILES = [("even", "Even"), ("s", "S-curve"), ("peak", "Peaked")]

def weights(n, profile):
    if profile == "even":
        return [1.0] * n
    w = [math.sin(math.pi * (i + 0.5) / n) for i in range(n)]
    return [x * x for x in w] if profile == "peak" else w

def plan_sp(i):
    """Mirror of sp() in tools.js. All amounts in whole AED; every column of the schedule adds up exactly."""
    C_, n = int(i["contract"]), max(1, int(i["months"]))
    adv = int(jr(C_ * i["advance"] / 100 / 1000) * 1000)
    w = weights(n, i["profile"])
    sw = sum(w)
    vals = [int(jr(C_ * x / sw / 1000) * 1000) for x in w[:-1]]
    vals.append(C_ - sum(vals))
    rows, cum_v, ret_cum, rec_cum, paid = [], 0, 0, 0, adv
    for k, v in enumerate(vals):
        cum_v += v
        ret_to = int(jr(cum_v * i["retention"] / 100 / 10) * 10)
        rec_to = adv if k == n - 1 else int(jr(adv * cum_v / C_ / 10) * 10) if C_ else 0
        ret, rec = ret_to - ret_cum, rec_to - rec_cum
        ret_cum, rec_cum = ret_to, rec_to
        pay = v - ret - rec
        paid += pay
        rows.append({"m": k + 1, "value": v, "ret": ret, "rec": rec, "pay": pay, "paid": paid, "held": ret_cum, "unrec": adv - rec_cum})
    rel1 = int(jr(ret_cum / 2 / 10) * 10)
    rel2 = ret_cum - rel1
    peak = max(rows, key=lambda r: r["pay"])
    return {"adv": adv, "rows": rows, "rel1": rel1, "rel2": rel2, "retTotal": ret_cum, "paidAtHandover": paid + rel1,
            "total": adv + sum(r["pay"] for r in rows) + rel1 + rel2, "peak": peak["pay"], "peakMonth": peak["m"]}

SP_MSG = {
    "row-advance": "Advance payment, on signing",
    "row-month": "Month {n}",
    "row-handover": "Handover: half the retention released",
    "row-final": "End of the defects period (month {n}): balance of retention released",
    "peakText": "{amount} in month {n}",
    "chartLabel": "Monthly payments to the contractor (bars) and the cumulative total paid (line)",
    "summary": "With a {adv} advance and {ret}% retention, you pay {peak} in the busiest month and have paid {handover} by handover. {held} of retention is still held after handover until the end of the defects period.",
    "noContract": "Enter the contract sum and the build period to see the schedule.",
}

def sp_msgs():
    return common_msgs() + list(SP_MSG.items())

def sp_form():
    profs = "".join(f'<label><input type="radio" name="profile" value="{k}"{" checked" if k == SP_EXAMPLE["profile"] else ""}><span>{lbl}</span></label>' for k, lbl in PROFILES)
    return f'''<form class="calc-in tool-in" id="tool-form" novalidate onsubmit="return false">
{money_field("contract", "Construction contract sum (AED)", SP_EXAMPLE["contract"], f"The example is the construction cost of the worked example in our cost calculator: {aed(EXAMPLE_CONS)}.", step=10000)}
<div class="calc-row"><div><label for="t-months">Build period (months)</label><input id="t-months" name="months" type="number" inputmode="numeric" min="1" max="60" step="1" value="{SP_EXAMPLE["months"]}"></div>
<div><label for="t-dlp">Defects period after handover (months)</label><input id="t-dlp" name="dlp" type="number" inputmode="numeric" min="0" max="36" step="1" value="{SP_EXAMPLE["dlp"]}"></div></div>
<div class="calc-row"><div><label for="t-advance">Advance payment (% of contract)</label><input id="t-advance" name="advance" type="number" inputmode="decimal" min="0" max="30" step="0.5" value="{SP_EXAMPLE["advance"]:g}" aria-describedby="t-advance-hint"><p class="hint" id="t-advance-hint">Typically 10–20%, depending on the project.</p></div>
<div><label for="t-retention">Retention (% of each valuation)</label><input id="t-retention" name="retention" type="number" inputmode="decimal" min="0" max="20" step="0.5" value="{SP_EXAMPLE["retention"]:g}" aria-describedby="t-retention-hint"><p class="hint" id="t-retention-hint">Commonly 10%, half released at handover and half after the defects period.</p></div></div>
<fieldset><legend>How the work is spread</legend><div class="calc-seg calc-seg--sm">{profs}</div>
<p class="hint">Even: the same value every month. S-curve: a slow start and finish with the busiest months in the middle, the usual shape of a build. Peaked: more of the work squeezed into the middle months.</p></fieldset>
<p class="hint">Percentages are typical and contract-dependent. Your contract sets the real terms; this is not legal advice.</p>
{msgs_html(sp_msgs())}
</form>'''

def sp_rows_html(p, dlp):
    def tr(label, cells, cls="", attr=""):
        return f'<tr{cls}{attr}><th scope="row">{label}</th>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    rows = [tr(SP_MSG["row-advance"], ["–", "–", "–", aed(p["adv"]), aed(p["adv"]), "–", aed(p["adv"])])]
    for r in p["rows"]:
        rows.append(tr(SP_MSG["row-month"].format(n=r["m"]), [aed(r["value"]), aed(r["ret"]), aed(r["rec"]), aed(r["pay"]), aed(r["paid"]), aed(r["held"]), aed(r["unrec"])],
                       ' class="is-peak"' if r["m"] == p["peakMonth"] else ""))
    paid = p["rows"][-1]["paid"]
    rows.append(tr(SP_MSG["row-handover"], ["–", "–", "–", aed(p["rel1"]), aed(paid + p["rel1"]), aed(p["rel2"]), "AED 0"]))
    rows.append(tr(SP_MSG["row-final"].format(n=len(p["rows"]) + dlp), ["–", "–", "–", aed(p["rel2"]), aed(p["total"]), "AED 0", "AED 0"]))
    return "".join(rows)

def sp_summary(p, i):
    return SP_MSG["summary"].format(adv=aed(p["adv"]), ret=f"{i['retention']:g}", peak=aed(p["peak"]),
                                    handover=aed(p["paidAtHandover"]), held=aed(p["rel2"]))

def sp_out(p):
    peaks = [plan_sp({**SP_EXAMPLE, "profile": k}) for k, _ in PROFILES]
    return f'''<div class="calc-out" id="tool-out">
{print_head("Stage payment plan: indicative schedule")}
<p class="calc-label">Busiest month, likely (S-curve)</p>
<p class="calc-total"><b data-out="peak">{aed(p["peak"])}</b>
<span class="calc-range">Range <span data-out="peak-low">{aed(peaks[0]["peak"])}</span> (even) to <span data-out="peak-high">{aed(peaks[2]["peak"])}</span> (peaked)</span></p>
<p class="tool-verdict" data-out="summary" aria-live="polite">{sp_summary(p, SP_EXAMPLE)}</p>
<div class="table-wrap"><table class="table calc-table tool-peaks"><caption class="sr">Key figures by spending pattern</caption>
<thead><tr><th scope="col">Key figures</th><th scope="col" class="num">Low (even)</th><th scope="col" class="num">Likely (S-curve)</th><th scope="col" class="num">High (peaked)</th></tr></thead>
<tbody><tr><th scope="row">Busiest month</th>{"".join(f'<td data-v="peak-{n}">{SP_MSG["peakText"].format(amount=aed(q["peak"]), n=q["peakMonth"])}</td>' for n, q in enumerate(peaks))}</tr>
<tr><th scope="row">Advance paid on signing</th>{"".join(f'<td data-v="adv-{n}">{aed(q["adv"])}</td>' for n, q in enumerate(peaks))}</tr>
<tr><th scope="row">Paid by handover</th>{"".join(f'<td data-v="handover-{n}">{aed(q["paidAtHandover"])}</td>' for n, q in enumerate(peaks))}</tr>
<tr><th scope="row">Retention held after handover</th>{"".join(f'<td data-v="held-{n}">{aed(q["rel2"])}</td>' for n, q in enumerate(peaks))}</tr></tbody></table></div>
<h3 class="calc-h">Payments month by month</h3>
<div class="tool-chart" data-chart role="img" aria-label="{SP_MSG["chartLabel"]}"></div>
<div class="table-wrap"><table class="table calc-table tool-schedule"><caption class="sr">Payment schedule</caption>
<thead><tr><th scope="col">When</th><th scope="col" class="num">Work valued</th><th scope="col" class="num">Retention held back</th><th scope="col" class="num">Advance recovered</th><th scope="col" class="num">You pay</th><th scope="col" class="num">Paid to date</th><th scope="col" class="num">Retention held</th><th scope="col" class="num">Advance not yet recovered</th></tr></thead>
<tbody data-schedule>{sp_rows_html(p, SP_EXAMPLE["dlp"])}</tbody>
<tfoot><tr><th scope="row">Total</th><td data-v="sum-value">{aed(sum(r["value"] for r in p["rows"]))}</td><td data-v="sum-ret">{aed(p["retTotal"])}</td><td data-v="sum-rec">{aed(p["adv"])}</td><td data-v="sum-pay">{aed(p["total"])}</td><td></td><td></td><td></td></tr></tfoot></table></div>
<p class="calc-reviewed">Last reviewed: {PT.month_year(PT.RATES_REVIEWED)}, by {esc(C.FOUNDER["name"])}</p>
<p class="calc-note calc-js" data-js-note>Showing the example below. Switch on JavaScript to change the inputs.</p>
<p class="calc-flag">An illustration of a typical schedule, not your contract and not legal advice. Payment is shown in the month the work is valued; in practice certification and payment follow some weeks later. Excludes variations, VAT and fees. <a href="#sources">Sources and assumptions</a></p>
{actions_html("Hello, I used your stage payment planner and would like to talk through my build budget.")}
{print_foot(SP_PATH, "Typical advance and retention percentages from Al Tamimi &amp; Company and DLA Piper; the example contract sum from the Eastbridge cost calculator.")}
</div>'''

def stage_payment_planner():
    c = Cites()
    p = plan_sp(SP_EXAMPLE)
    tam, dla, opt, reca = c("tam"), c("dla"), c("opt"), c("reca")
    after = f'''<section class="section--tight paper"><div class="wrap split"><div><h2>How the schedule works</h2></div><div class="prose">
<p>The short answer: on a typical villa contract you pay an advance on signing, then monthly payments for the work valued, less retention and less a share of the advance, then half the retention at handover and the rest when the defects period ends. The planner shows how much leaves your account each month, and how much of your money is in the contractor's hands before it has been earned.</p>
<ol>
<li><strong>Advance.</strong> Al Tamimi &amp; Company describes an advance payment of between 10% and 20%, depending on the nature of the project, as industry practice.{tam} Under FIDIC contracts it is given in return for an advance payment guarantee. The planner recovers it from each monthly valuation in proportion to the work done, a simple and common approach; your contract may set a different recovery schedule.</li>
<li><strong>Monthly valuations.</strong> The contract sum spread over the build period on the pattern you choose. Each month's value is rounded to the nearest AED 1,000 and the last month takes the difference, so the months add up to the contract sum exactly.</li>
<li><strong>Retention.</strong> DLA Piper describes common UAE practice as 10% retention, with 5% released at handover and 5% after the defects liability period.{dla} Under the FIDIC Red Book, the taking-over certificate releases the first half.{tam} Retention is not required by UAE law; the percentage, any cap and the release dates are whatever your contract says.</li>
<li><strong>Build period.</strong> The example uses 12 months. Published estimates put villa construction at typically 12–18 months{opt} or 8–14 months for the construction phase alone.{reca}</li>
</ol>
<p>The column "Advance not yet recovered" is your exposure: money paid ahead of the work. It falls as the advance is recovered, which is why the advance payment guarantee should reduce on the same schedule and stay valid until the last of it is recovered. Retention is the opposite: the contractor's money in your hands, which is why it gives you leverage at handover.</p>
<p>From the builder's side, the first month's valuation was always the one we watched most closely, because front-loading the early payments is the easiest way for a contractor to finance a job with the owner's money. A schedule like this one, agreed before signing, gives you something to check each payment application against. Our guide to <a href="/insights/villa-construction-contracts-uae/">villa construction contracts in the UAE</a> covers retention, advance payment guarantees and bonds in more detail.</p>
</div></div></section>'''
    data = {"kind": "sp"}
    faqs = [
        ("How much advance payment is normal on a UAE villa build?",
         "An advance of 10–20% of the contract sum is described as industry practice, depending on the project (Al Tamimi &amp; Company). It should be secured by an advance payment guarantee that reduces as the advance is recovered from later payments. The figure is negotiable and set by your contract."),
        ("How much retention is held on a construction contract in the UAE?",
         "Commonly 10% of each payment, with 5% released at handover and 5% after the defects liability period (DLA Piper). Retention is not mandated by UAE law, so the percentage, any cap and the release dates are whatever your contract says."),
        ("When is retention released?",
         "Typically half at handover (the taking-over certificate under FIDIC) and the balance at the end of the defects period, often a year. Keep a dated list of defects and report them in writing well before the period ends."),
        ("Why does the busiest month matter?",
         "Because it is the month your cash has to be ready. On an S-curve the middle months carry the most work, so the peak payment is well above the average. Plan finance drawdowns and currency transfers around it."),
        ("Is this legal advice?",
         "No. It illustrates a typical schedule. Payment terms, retention, guarantees and their release are contract-specific; take advice from a UAE-qualified lawyer on your contract."),
    ]
    tool_page(SP_PATH, "sp", "Stage payment planner", "Stage payment and cash-flow planner",
              "Spread a villa build budget over a typical payment schedule: advance, monthly valuations, retention and its release. See what you pay each month and how much of your money is ahead of the work.",
              sp_form(), sp_out(p), data, after,
              "Villa Stage Payment Planner: Dubai & UAE | Eastbridge",
              "Spread a villa build budget over a typical UAE payment schedule: advance, monthly valuations, retention and release, with a monthly cash-flow table and chart.",
              "Stage payment and cash-flow planner for a villa build (UAE)",
              "Spreads a villa construction contract over a typical UAE payment schedule (advance, monthly valuations, retention and release) and shows the owner's monthly payments and exposure.",
              faqs, c)

# ================================================================ 3. delay cost estimator
DC_EXAMPLE = {"months": 3, "loc": "dubai", "rent": RENT_DEFAULT, "borrowed": rnd100(EXAMPLE_CONS / 2) // 10000 * 10000,
              "rate": BASE_RATE, "remaining": rnd100(EXAMPLE_CONS / 2) // 10000 * 10000, "contract": EXAMPLE_CONS,
              "prelims": False, "fees": 0}
DC_LINES = [("housing", "Rent or hotel while you wait"), ("finance", "Interest on money borrowed for the build"),
            ("escalation", "Price escalation on the work still to build"), ("prelims", "Contractor's extended site costs"),
            ("fees", "Professional fees that continue")]

def estimate_dc(i):
    """Mirror of dc() in tools.js. Monthly cost per line, low/likely/high, rounded to AED 100; totals are sums."""
    z = [0, 0, 0]
    esc_ = ESCALATION[i["loc"]]
    o = {"housing": [i["rent"]] * 3,
         "finance": [i["borrowed"] * i["rate"] / 100 / 12] * 3,
         "escalation": [i["remaining"] * r / 100 / 12 for r in esc_],
         "prelims": [i["contract"] * PRELIMS[i["loc"]] / m for m in BUILD_MONTHS] if i["prelims"] else z,
         "fees": [i["fees"]] * 3}
    r = {k: [rnd100(v) for v in o[k]] for k, _ in DC_LINES}
    r["total"] = [sum(r[k][n] for k, _ in DC_LINES) for n in range(3)]
    m = max(0, i["months"])
    r["over"] = [sum(r[k][n] * m for k, _ in DC_LINES) for n in range(3)]
    return r

DC_MSG = {
    "over": "Over {n} months of delay: likely {likely}, between {low} and {high}.",
    "over-one": "This is the cost of one month's delay.",
    "noMonths": "Enter how many months the delay may last to see the total.",
}

def dc_msgs():
    return common_msgs() + list(DC_MSG.items())

def dc_form():
    i = DC_EXAMPLE
    return f'''<form class="calc-in tool-in" id="tool-form" novalidate onsubmit="return false">
<div class="calc-row"><div><label for="t-months">Expected delay (months)</label><input id="t-months" name="months" type="number" inputmode="numeric" min="0" max="60" step="1" value="{i["months"]}"></div>
<div><label for="t-loc">Where is the villa?</label><select id="t-loc" name="loc"><option value="dubai" selected>Dubai</option><option value="ad">Abu Dhabi</option></select></div></div>
{money_field("rent", "Rent or hotel per month while you wait (AED)", i["rent"], f"Set to 0 if you are not paying for somewhere else to live. The default is the average Dubai rent for a four-bedroom villa, AED {RENT_ANNUAL['4']:,} a year (May 2026); three bedrooms AED {RENT_ANNUAL['3']:,}, five bedrooms AED {RENT_ANNUAL['5']:,}.", step=500)}
<div class="calc-row">{money_field("borrowed", "Money borrowed for the build so far (AED)", i["borrowed"], "Set to 0 if the build is paid from savings.", step=10000)}
<div><label for="t-rate">Interest rate (% a year)</label><input id="t-rate" name="rate" type="number" inputmode="decimal" min="0" max="25" step="0.05" value="{i["rate"]:g}" aria-describedby="t-rate-hint"><p class="hint" id="t-rate-hint">The default is the UAE Central Bank's base rate, {BASE_RATE:g}% since 17 September 2026: a floor, not a loan rate. Enter your own loan rate.</p></div></div>
{money_field("remaining", "Value of the work still to build (AED)", i["remaining"], "Escalation applies to work that is not yet built or bought. On a firm fixed price the contractor carries much of this risk until the contract changes.", step=10000)}
<fieldset><legend>Contractor's time-related costs</legend>
<div class="calc-checks"><label><input type="checkbox" name="prelims"> Include the contractor's extended site costs (only if the delay is on the owner's side)</label></div>
{money_field("contract", "Construction contract sum (AED)", i["contract"], "Used only for the contractor's extended site costs.", step=10000)}
</fieldset>
{money_field("fees", "Professional fees that continue each month (AED)", i["fees"], "Your consultant's site-stage fee, a project manager's monthly fee or similar. Check your appointments; no published benchmark exists.", step=500)}
<p class="hint">The examples for money borrowed and work still to build are each half the construction cost of our cost calculator's worked example ({aed(EXAMPLE_CONS)}).</p>
{msgs_html(dc_msgs())}
</form>'''

def dc_over(e, m):
    if m <= 0:
        return DC_MSG["noMonths"]
    if m == 1:
        return DC_MSG["over-one"]
    return DC_MSG["over"].format(n=m, likely=aed(e["over"][1]), low=aed(e["over"][0]), high=aed(e["over"][2]))

def dc_out(e):
    rows = "".join(f'<tr data-row="{k}"><th scope="row">{lbl}</th>' +
                   "".join(f'<td data-v="{k}-{n}">{aed(e[k][n]) if (e[k][0] or e[k][2]) else ("Not included" if n == 1 else "–")}</td>' for n in range(3)) +
                   "</tr>" for k, lbl in DC_LINES)
    return f'''<div class="calc-out" id="tool-out">
{print_head("Cost of delay: indicative estimate")}
<p class="calc-label">One month's delay, likely cost</p>
<p class="calc-total" aria-live="polite" aria-atomic="true"><b data-out="likely">{aed(e["total"][1])}</b>
<span class="calc-range">Range <span data-out="low">{aed(e["total"][0])}</span> to <span data-out="high">{aed(e["total"][2])}</span></span></p>
<p class="tool-verdict" data-out="over">{dc_over(e, DC_EXAMPLE["months"])}</p>
<p class="calc-reviewed">Rates last reviewed: {PT.month_year(PT.RATES_REVIEWED)}, by {esc(C.FOUNDER["name"])}</p>
<div class="table-wrap"><table class="table calc-table"><caption class="sr">Cost of one month's delay: low, likely and high</caption>
<thead><tr><th scope="col">Each month of delay</th><th scope="col" class="num">Low</th><th scope="col" class="num">Likely</th><th scope="col" class="num">High</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><th scope="row">Total per month</th>{"".join(f'<td data-v="total-{n}">{aed(e["total"][n])}</td>' for n in range(3))}</tr>
<tr class="tool-meta"><th scope="row">Total for the delay</th>{"".join(f'<td data-v="over-{n}">{aed(e["over"][n])}</td>' for n in range(3))}</tr></tfoot></table></div>
<p class="calc-note">If the delay is the contractor's responsibility, the contract may give you delay damages or other remedies, which this does not deduct. What applies depends on the contract and the records; take advice from a UAE-qualified lawyer. Our guide to <a href="{STALLED}">what to do when a villa build stalls</a> sets out the first ten days.</p>
<p class="calc-note calc-js" data-js-note>Showing the example below. Switch on JavaScript to change the inputs.</p>
<p class="calc-flag">An indicative estimate, not a claim valuation. Each line is rounded to the nearest AED 100 and the totals are the sum of the lines. Excludes storage, travel, lost rental income from the finished villa and the cost of disputes. <a href="#sources">Sources and assumptions</a></p>
{actions_html("Hello, I used your delay cost estimator and would like to talk about my project.")}
{print_foot(DC_PATH, "Rents from Engel &amp; Völkers (Property Monitor data); base rate from the Central Bank of the UAE; construction inflation from Turner &amp; Townsend and Currie &amp; Brown (via PRASOON); preliminaries from Turner &amp; Townsend.")}
</div>'''

def delay_cost_estimator():
    c = Cites()
    e = estimate_dc(DC_EXAMPLE)
    evr, cbuae, tt25, pra, reca = c("evr"), c("cbuae"), c("tt25"), c("pra"), c("reca")
    after = f'''<section class="section--tight paper"><div class="wrap split"><div><h2>How the estimate works</h2></div><div class="prose">
<p>The short answer: a month's delay on a villa build costs the owner the rent or hotel they are still paying, the interest on money already borrowed, the rise in the price of the work not yet built and, if the delay is on the owner's side, the contractor's time-related site costs. Fees that run by the month come on top. The estimator adds those up, line by line.</p>
<ol>
<li><strong>Rent or hotel.</strong> The monthly figure you enter. The default is Engel &amp; Völkers' average Dubai rent for a four-bedroom villa, AED {RENT_ANNUAL["4"]:,} a year as of May 2026 (three bedrooms AED {RENT_ANNUAL["3"]:,}; five bedrooms AED {RENT_ANNUAL["5"]:,}), from Property Monitor data.{evr} It is the same in every column.</li>
<li><strong>Finance.</strong> Money borrowed multiplied by the annual rate, divided by twelve. The default rate is the Central Bank of the UAE's base rate, raised to {BASE_RATE:g}% from 17 September 2026.{cbuae} It is the floor for overnight money-market rates, not what a bank charges for a loan, so enter your own rate.</li>
<li><strong>Escalation.</strong> The value of the work still to build, multiplied by a month's construction inflation. For 2026, Turner &amp; Townsend forecast 4% in Dubai and 5% in Abu Dhabi,{tt25} and Currie &amp; Brown about 3% for the UAE.{pra} The low column uses 3%, the high column Turner &amp; Townsend's figure for the emirate, and the likely column the midpoint.</li>
<li><strong>Contractor's extended site costs.</strong> Off by default. If the delay is on the owner's side (late decisions, late design information, late payment), the contractor may be entitled to more time and its time-related costs. The estimator spreads Turner &amp; Townsend's preliminaries, 12% of construction cost on a 2,500 m² project in Dubai and 15% in Abu Dhabi,{tt25} over a construction phase of 8–14 months:{reca} the shortest build gives the highest monthly figure. Treat it as an order of magnitude; the contract and the records decide what is actually due.</li>
<li><strong>Professional fees.</strong> Whatever monthly fees continue under your appointments. There is no published benchmark, so nothing is assumed.</li>
</ol>
<p>From the builder's side, the cost of delay was always easier to see from the contractor's chair than from the owner's: site cabins, supervision and plant hire run by the week whether work moves or not. The owner's costs are quieter but often larger, because rent and finance never stop. When a build has stalled, our guide to <a href="{STALLED}">what to do when a villa build stalls</a> covers the first ten days, and a <a href="/services/stalled-project-rescue/">stalled project review</a> puts a number on the way back.</p>
</div></div></section>'''
    data = {"kind": "dc", "escalation": ESCALATION, "prelims": PRELIMS, "buildMonths": BUILD_MONTHS}
    faqs = [
        ("How much does a month's delay cost on a villa build in Dubai?",
         "It depends on your circumstances, but the main costs are rent or a hotel while you wait, interest on money borrowed, the rise in price of the work still to build, and, if the delay is on your side, the contractor's time-related site costs. On the default example, renting a four-bedroom villa at the Dubai average and with half the build still to go, one month's delay is likely to cost about " + aed(e["total"][1]) + "."),
        ("Who pays for delay on a construction project?",
         "That depends on the cause and the contract. A contractor-caused delay may entitle the owner to delay damages; an owner-caused delay may entitle the contractor to more time and costs. The records made at the time decide most disputes. Take advice from a UAE-qualified lawyer on your contract."),
        ("How much does construction inflation add each month?",
         "For 2026 Turner &amp; Townsend forecast construction inflation of 4% in Dubai and 5% in Abu Dhabi, and Currie &amp; Brown about 3% for the UAE. A year's inflation divided by twelve, applied to the work still to build, gives a rough monthly figure. On a firm fixed price the contractor carries much of that risk, until the scope or the programme changes."),
        ("What should I do if my villa project is delayed?",
         "Establish the cause in writing, keep dated records of the site and the correspondence, check what the contract says about notices and extensions of time, and pay only what has been properly valued. If the site has stopped, read our guide to the first ten days of a stalled villa build."),
        ("Does this include delay damages from the contractor?",
         "No. Whether delay damages are payable, and how much, depends on the contract, the cause of the delay and UAE law, so the estimator shows your costs only."),
    ]
    tool_page(DC_PATH, "dc", "Delay cost estimator", "Villa delay cost estimator",
              "What a month's delay on a villa build in Dubai or Abu Dhabi costs the owner: rent or hotel, finance, price escalation, the contractor's extended site costs and continuing fees, low, likely and high.",
              dc_form(), dc_out(e), data, after,
              "Villa Delay Cost Estimator: Dubai & Abu Dhabi | Eastbridge",
              "What a month's delay on a villa build costs the owner in Dubai or Abu Dhabi: rent, finance, escalation, extended site costs and fees, low to high, sourced.",
              "Villa construction delay cost estimator (Dubai and Abu Dhabi)",
              "Estimates the monthly cost to an owner of a delay on a villa build: housing, finance, construction price escalation, the contractor's extended site costs and continuing fees, low, likely and high.",
              faqs, c)

# ---------------------------------------------------------------- hub entries and build
HUB = [(RR_PATH, "Renovate or rebuild?", "Renovating against knocking down and rebuilding: cost per square foot of finished space, time and approvals, low, likely and high. Uses the cost calculator's rates, with published renovation rates per square foot.", "Compare renovating and rebuilding"),
       (SP_PATH, "Stage payment and cash-flow planner", "A build budget spread over a typical payment schedule: advance, monthly valuations, retention and its release, with a month-by-month table and chart of what you pay and how much is ahead of the work.", "Plan your payments"),
       (DC_PATH, "Delay cost estimator", "What each month of delay costs an owner: rent or hotel, finance, price escalation, the contractor's extended site costs and continuing fees.", "Estimate the cost of delay")]

def hub_html():
    return "".join(f'<h3><a href="{p}">{t}</a></h3>\n<p>{d}</p>\n<p><a class="btn" href="{p}">{b}</a></p>\n' for p, t, d, b in HUB)

def build_owner_tools():
    renovate_or_rebuild()
    stage_payment_planner()
    delay_cost_estimator()
