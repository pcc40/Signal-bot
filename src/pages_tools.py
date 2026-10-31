"""Interactive tools: the /tools/ hub and the villa build and renovation cost calculator.

Every rate used by the calculator lives in RATES below and is cited in SOURCES. The same
RATES object is embedded in the page as JSON and read by src/static/assets/calc.js, so the
server-rendered worked example and the live calculator always use identical figures.
"""
import json
import math
import html as H
import build as B
from content.areas import AREAS

esc = H.escape
CALC_PATH = "/tools/villa-build-cost-calculator/"
SQFT_PER_M2 = 10.7639

# ---------------------------------------------------------------- sources
SOURCES = [
    ("ev", "Engel & Völkers, Construction cost in Dubai (December 2025)",
     "https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai"),
    ("kf", "Knight Frank Q2 2025 construction costs, reported by Gulf Construction",
     "https://gulfconstructiononline.com/ArticleTA/436847"),
    ("reca", "Real Estate Club Dubai, Villa architects in Dubai: fees, contingency and timelines",
     "https://realestateclubdubai.com/dubai-villa-architects"),
    ("recc", "Real Estate Club Dubai, Villa build cost calculator methodology",
     "https://realestateclubdubai.com/tools/villa-build-cost-calculator"),
    ("opt", "Optimal Engineering, Cost to build a villa in Dubai",
     "https://www.optimal.ae/blog/cost-to-build-a-villa-in-dubai"),
    ("sr", "Smart Renovation, Villa renovation in Dubai: 2026 guide to costs, timeline and permits",
     "https://smartrenovation.ae/villa-renovation-in-dubai-complete-2026-guide-to-costs-timeline-permits/"),
    ("pra", "PRASOON, Owner's representative vs project manager in the UAE (citing Currie & Brown)",
     "https://prasoon.design/insights/owners-representative-vs-project-manager-uae"),
    ("gn", "Gulf News, Dubai Municipality warns consultancies over inflated villa designs (August 2025)",
     "https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704"),
]
SRC_NUM = {k: i + 1 for i, (k, _, _) in enumerate(SOURCES)}

def cite(*keys):
    return "".join(f'<sup><a href="#src-{k}" aria-label="Source {SRC_NUM[k]}">[{SRC_NUM[k]}]</a></sup>' for k in keys)

# ---------------------------------------------------------------- rates (AED)
# Construction-only rates in AED per sq ft, [low, high]. "Likely" is the midpoint.
RATES = {
    "sqftPerM2": SQFT_PER_M2,
    "tiers": {
        "standard": {"label": "Standard", "nb": [300, 500]},
        "premium": {"label": "Premium", "nb": [500, 850]},
        "luxury": {"label": "Luxury", "nb": [850, 1200]},
        "ultra": {"label": "Ultra-luxury", "nb": [1200, 1400], "open": True},
    },
    # Renovation: published whole-villa bands by scope. null = no published ceiling.
    "reno": {
        # "soft": False = no design fees or approvals allowance (cosmetic work rarely needs drawings or a permit).
        "standard": {"label": "Basic refresh: painting, flooring, small upgrades", "cost": [200000, 300000], "months": [2, 3], "soft": False},
        "premium": {"label": "Mid-range: kitchens, bathrooms and interiors", "cost": [400000, 800000], "months": [4, 6]},
        "luxury": {"label": "Luxury: premium materials and structural changes", "cost": [1000000, None], "months": [6, None]},
        "ultra": {"label": "Ultra-luxury: full strip-out and remodel", "cost": [1000000, None], "months": [6, None]},
    },
    "pool": [80000, 250000],
    "land": [100, 500],          # per sq ft of garden
    "smart": [50000, 300000],
    "demo": [50000, 200000],
    "design": [0.06, 0.09, 0.12],
    "contingency": [0.10, 0.12, 0.15],
    "ffe": [0.30, 0.35, 0.40],
    "permitsFixed": [25000, 50000, 75000],
    "time": {"design": [3, 4], "approvals": [2, 3], "build": [8, 14], "snag": [1, 2], "luxTotal": [24, 36]},
}

def tri(pair):
    lo, hi = pair
    return [lo, (lo + hi) / 2, hi]

def estimate(i):
    """Mirror of calc.js estimate(). i: mode, area (sq ft), tier, basement, pool, garden, smart, ffe, demo."""
    R = RATES
    t = R["tiers"][i["tier"]]
    nb = tri(t["nb"])
    z = [0, 0, 0]
    out = {}
    if i["mode"] == "new":
        out["build"] = [i["area"] * r for r in nb]
        out["basement"] = [i["basement"] * r for r in nb]
        out["demo"] = tri(R["demo"]) if i["demo"] else z
        open_hi = bool(t.get("open"))
    else:
        rv = R["reno"][i["tier"]]
        lo, hi = rv["cost"]
        if hi is None:
            hi = max(lo, i["area"] * t["nb"][0])
        out["build"] = tri([lo, hi])
        out["basement"] = z
        out["demo"] = z
        open_hi = rv["cost"][1] is None
    out["pool"] = tri(R["pool"]) if i["pool"] else z
    out["land"] = [i["garden"] * r for r in tri(R["land"])]
    out["smart"] = tri(R["smart"]) if i["smart"] else z
    cons = [sum(out[k][n] for k in ("build", "basement", "demo", "pool", "land", "smart")) for n in range(3)]
    soft = i["mode"] == "new" or R["reno"][i["tier"]].get("soft", True)
    out["design"] = [cons[n] * R["design"][n] for n in range(3)] if soft else z
    out["permits"] = list(R["permitsFixed"]) if soft else z
    out["contingency"] = [cons[n] * R["contingency"][n] for n in range(3)]
    out["ffe"] = [cons[n] * R["ffe"][n] for n in range(3)] if i["ffe"] else z
    out["open"] = open_hi
    return rounded(out)

# Every cost line is rounded on its own; construction and the total are the sums of the rounded lines, so the
# figures shown always add up. calc.js does exactly the same.
LINE_KEYS = ("build", "basement", "demo", "pool", "land", "smart", "design", "permits", "contingency", "ffe")
CONS_KEYS = LINE_KEYS[:6]

def rounded(e):
    r = {k: [rnd(v) for v in e[k]] for k in LINE_KEYS}
    r["construction"] = [sum(r[k][n] for k in CONS_KEYS) for n in range(3)]
    r["total"] = [sum(r[k][n] for k in LINE_KEYS) for n in range(3)]
    r["open"] = e["open"]
    return r

def rnd(x):
    """Nearest AED 1,000, or AED 10,000 from AED 1 million (half up, as Math.round in calc.js)."""
    step = 10000 if x >= 1e6 else 1000
    return int(math.floor(x / step + 0.5) * step)

def aed(x):
    return f"AED {int(x):,}"

def compact(x):
    x = rnd(x)
    if x >= 1e6:
        return f"AED {x / 1e6:.2f}m".replace(".00m", "m")
    return f"AED {round(x / 1000):,}k"

def aed_rate(x):
    return f"AED {int(round(x / 10) * 10):,}"

def per_m2(v):
    return int(round(v * SQFT_PER_M2 / 10) * 10)

# ---------------------------------------------------------------- worked example
EXAMPLE = {"mode": "new", "area": 6000, "tier": "premium", "basement": 0, "pool": True,
           "garden": 3000, "smart": False, "ffe": False, "demo": False, "loc": "dubai-hills-estate"}

LINES = [("build", "Main build (shell, MEP and finishes)"), ("basement", "Basement"), ("demo", "Demolition of an existing villa"),
         ("pool", "Swimming pool"), ("land", "Landscaping"), ("smart", "Smart home and AV"),
         ("design", "Design and engineering fees"), ("permits", "Approvals, NOCs and connections"),
         ("contingency", "Contingency"), ("ffe", "Furniture, fixtures and equipment (FF&amp;E)")]
BAR = [("build", "Build"), ("extras", "Extras"), ("design", "Design fees"), ("permits", "Approvals"),
       ("contingency", "Contingency"), ("ffe", "FF&amp;E")]

def bar_parts(e):
    extras = [e["basement"][n] + e["demo"][n] + e["pool"][n] + e["land"][n] + e["smart"][n] for n in range(3)]
    vals = {"build": e["build"][1], "extras": extras[1], "design": e["design"][1], "permits": e["permits"][1],
            "contingency": e["contingency"][1], "ffe": e["ffe"][1]}
    tot = sum(vals.values()) or 1
    return vals, tot

# ---------------------------------------------------------------- live text
# Everything calc.js writes on the page comes from the hidden #calc-msgs list below (one <li> per message),
# so the i18n pipeline translates it with the rest of the page and calc.js holds no English text.
# Placeholders in braces ({n}, {cons}, {rate}, {dev}) are filled in by the script and must be kept in translations.
SUB = {
    "new-sqft": "Construction {cons} · {rate} per sq ft of built-up area (main build only, excluding extras)",
    "new-m2": "Construction {cons} · {rate} per m² of built-up area (main build only, excluding extras)",
    "reno-fixed": "Construction {cons} · a whole-villa scope example, so the floor area is not used",
    "reno-open": "Construction {cons} · the high figure applies the lowest new-build rate for this specification to the built-up area",
}
ROUTE_DUBAI = "Approvals in Dubai go through Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits."
ROUTE_AD = "In Abu Dhabi the Department of Municipalities and Transport regulates villa building, and permits are issued by the municipality through TAMM."
ROUTE_DEV = "The master developer, {dev}, has its own approval requirements; check them before design starts."
ROUTE_NAKHEEL_RENO = "In Nakheel communities, renovation and extension approvals start with a Nakheel NOC application through its portal."
ROUTES = {
    "ad": ROUTE_AD, "ad-dev": f"{ROUTE_AD} {ROUTE_DEV}",
    "dubai": ROUTE_DUBAI, "dubai-dev": f"{ROUTE_DUBAI} {ROUTE_DEV}",
    "dubai-nakheel-reno": f"{ROUTE_DUBAI} {ROUTE_NAKHEEL_RENO}",
}
RENO_NOTE = "Smaller interior upgrades take around two to three months; structural changes and extensions six months or longer."
PHASES = [("design", "Design"), ("approvals", "Approvals and NOCs"), ("build", "Construction"), ("snag", "Snagging and handover")]

def months(p):
    return f"{p[0]}–{p[1]} months" if p[1] is not None else f"{p[0]} months or longer"

def time_note(lux, basement):
    t = RATES["time"]
    if lux:
        s = f"Custom luxury villas commonly take {t['luxTotal'][0]}–{t['luxTotal'][1]} months from plot to keys. Phases can overlap."
    else:
        a, b = sum(t[k][0] for k, _ in PHASES), sum(t[k][1] for k, _ in PHASES)
        s = f"About {a}–{b} months on these phases end to end. Real Estate Club Dubai quotes 12–24 months from plot to keys, as phases can overlap."
    return s + (" A basement adds time to the ground works stage." if basement else "")

def route_key(city, dev, mode):
    """Mirror of route() in calc.js."""
    if city == "Abu Dhabi":
        return "ad-dev" if dev else "ad"
    if dev == "Nakheel" and mode == "reno":
        return "dubai-nakheel-reno"
    return "dubai-dev" if dev else "dubai"

def tier_new_note(t, unit):
    plus = "+" if t.get("open") else ""
    lo, hi = t["nb"]
    if unit == "m2":
        return f"AED {per_m2(lo):,}–{per_m2(hi):,}{plus} per m²"
    return f"AED {lo:,}–{hi:,}{plus} per sq ft"

def reno_band(rv):
    lo, hi = rv["cost"]
    band = f"AED {lo:,}–{hi:,}" if hi is not None else f"from AED {lo / 1e6:g} million"
    return f"{rv['label']}, {band}"

def calc_messages():
    m = [("money", "AED {n}"), ("moneyK", "AED {n}k"), ("moneyM", "AED {n}m"), ("notIncluded", "Not included"),
         ("unit-sqft", "sq ft"), ("unit-m2", "m²"), ("jsNote", "Figures update as you change the inputs."),
         ("rowBuild-new", LINES[0][1]), ("rowBuild-reno", "Renovation works (whole-villa scope band)")]
    m += [(f"sub-{k}", v) for k, v in SUB.items()]
    for k, t in RATES["tiers"].items():
        rv = RATES["reno"][k]
        m += [(f"tierNew-{k}-sqft", tier_new_note(t, "sqft")), (f"tierNew-{k}-m2", tier_new_note(t, "m2")),
              (f"tierReno-{k}", reno_band(rv)), (f"timeV-works-{k}", months(rv["months"]))]
    for k, lbl in PHASES:
        m += [(f"time-{k}", lbl), (f"timeV-{k}", months(RATES["time"][k]))]
    m += [("time-noc", "Developer NOC and permit"), ("timeV-noc", "A few weeks"), ("time-works", "Works")]
    m += [("note-new", time_note(False, False)), ("note-new-base", time_note(False, True)),
          ("note-lux", time_note(True, False)), ("note-lux-base", time_note(True, True)), ("note-reno", RENO_NOTE)]
    m += [(f"route-{k}", v) for k, v in ROUTES.items()]
    items = "".join(f'<li data-m="{k}">{v}</li>' for k, v in m)
    devs = sorted({a["developer"] for a in AREAS if a.get("developer")})
    items += "".join(f'<li data-dev="{esc(d)}">{esc(d)}</li>' for d in devs)
    return f'<div class="calc-msgs" id="calc-msgs" hidden><ul>{items}</ul></div>'

def results_html(e):
    """Server-rendered result panel. calc.js updates the same nodes in place (no layout shift)."""
    hi_sfx = "+" if e["open"] else ""
    vals, tot = bar_parts(e)
    segs = "".join(f'<span class="cb-seg cb-{k}" data-seg="{k}" style="width:{vals[k] / tot * 100:.2f}%"></span>' for k, _ in BAR)
    legend = "".join(f'<li><i class="cb-{k}" aria-hidden="true"></i>{lbl} <b data-leg="{k}">{compact(vals[k])}</b></li>' for k, lbl in BAR)
    rows = "".join(f'<tr data-row="{k}"><th scope="row"{" data-row-label" if k == "build" else ""}>{lbl}</th><td data-v="{k}-0">{aed(e[k][0])}</td>'
                   f'<td data-v="{k}-1">{aed(e[k][1])}</td><td data-v="{k}-2">{aed(e[k][2])}</td></tr>' for k, lbl in LINES)
    t = RATES["time"]
    times = "".join(f'<li><span>{lbl}</span><b>{months(t[k])}</b></li>' for k, lbl in PHASES)
    loc = next(a for a in AREAS if a["slug"] == EXAMPLE["loc"])
    route = ROUTES[route_key(loc["city"], loc["developer"], EXAMPLE["mode"])].format(dev=esc(loc["developer"]))
    sub = SUB["new-sqft"].format(cons=f'<span data-out="cons">{aed(e["construction"][1])}</span>',
                                 rate=f'<span data-out="rate">{aed_rate(e["build"][1] / max(EXAMPLE["area"], 1))}</span>')
    return f'''<div class="calc-out" id="calc-out">
<p class="calc-label">Indicative total, including soft costs</p>
<p class="calc-total" aria-live="polite" aria-atomic="true"><span class="sr">Likely total: </span><b data-out="likely">{aed(e["total"][1])}</b>
<span class="calc-range">Range <span data-out="low">{aed(e["total"][0])}</span> to <span data-out="high">{aed(e["total"][2])}{hi_sfx}</span></span></p>
<p class="calc-sub" data-out="sub">{sub}</p>
<p class="calc-note calc-assess" data-reno-assess hidden>Renovation bands describe a typical villa. A large or older villa, or one that needs new services, waterproofing or structural work, needs a project-specific assessment rather than a band. <a href="/contact/">Ask us for a project-specific assessment</a>.</p>
<div class="cb" role="img" aria-label="Breakdown of the likely total" data-bar>{segs}</div>
<ul class="cb-legend">{legend}</ul>
<div class="table-wrap"><table class="table calc-table"><caption class="sr">Cost lines: low, likely and high</caption>
<thead><tr><th scope="col">Cost line</th><th scope="col" class="num">Low</th><th scope="col" class="num">Likely</th><th scope="col" class="num">High</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><th scope="row">Total</th><td data-v="total-0">{aed(e["total"][0])}</td><td data-v="total-1">{aed(e["total"][1])}</td><td data-v="total-2">{aed(e["total"][2])}{hi_sfx}</td></tr></tfoot></table></div>
<h3 class="calc-h">Indicative timeline</h3>
<ol class="calc-time" data-time>
{times}
</ol>
<p class="calc-note" data-time-note>{time_note(False, False)}</p>
<p class="calc-note" data-route>{route}</p>
<p class="calc-note calc-js" data-js-note>Showing the worked example below. Switch on JavaScript to change the inputs.</p>
<p class="calc-flag">An indicative estimate from published market ranges, not a quotation. Each line is rounded and the totals are the sum of the lines. Excludes the plot, finance, insurance, cost inflation and advisers' fees, including ours; allow for 5% VAT if your quotes exclude it. <a href="#sources">Sources and assumptions</a></p>
</div>'''

def form_html():
    tiers = "".join(
        f'<label class="calc-opt"><input type="radio" name="tier" value="{k}"{" checked" if k == EXAMPLE["tier"] else ""}>'
        f'<span><b>{esc(v["label"])}</b><small data-tier-note="{k}">{tier_new_note(v, "sqft")}</small></span></label>'
        for k, v in RATES["tiers"].items())
    dubai = "".join(f'<option value="{a["slug"]}" data-city="Dubai" data-dev="{esc(a["developer"])}"{" selected" if a["slug"] == EXAMPLE["loc"] else ""}>{esc(a["name"])}</option>' for a in AREAS if a["city"] == "Dubai")
    ad = "".join(f'<option value="{a["slug"]}" data-city="Abu Dhabi" data-dev="{esc(a["developer"])}">{esc(a["name"])}</option>' for a in AREAS if a["city"] == "Abu Dhabi")
    return f'''<form class="calc-in" id="calc" novalidate onsubmit="return false">
<fieldset><legend>Project type</legend><div class="calc-seg">
<label><input type="radio" name="mode" value="new" checked><span>New build</span></label>
<label><input type="radio" name="mode" value="reno"><span>Renovation</span></label></div></fieldset>
<div><label for="c-loc">Where is the villa?</label><select id="c-loc" name="loc">
<optgroup label="Dubai">{dubai}<option value="dubai" data-city="Dubai" data-dev="">Elsewhere in Dubai</option></optgroup>
<optgroup label="Abu Dhabi">{ad}<option value="abu-dhabi" data-city="Abu Dhabi" data-dev="">Elsewhere in Abu Dhabi</option></optgroup></select>
<p class="hint">Location changes the approvals route shown, not the rate. No published source supports a reliable location premium.</p></div>
<fieldset><legend>Units</legend><div class="calc-seg calc-seg--sm">
<label><input type="radio" name="unit" value="sqft" checked><span>sq ft</span></label>
<label><input type="radio" name="unit" value="m2"><span>m²</span></label></div></fieldset>
<div data-area-field><label for="c-area">Built-up area (<span data-unit>sq ft</span>)</label><input id="c-area" name="area" type="number" inputmode="numeric" min="0" step="50" value="{EXAMPLE["area"]}" aria-describedby="c-area-hint">
<p class="hint" id="c-area-hint" data-area-typical>Typical 4-bedroom villas are about 4,000–5,000 sq ft; 5-bedroom 6,000–8,000 sq ft.{cite("recc")}</p>
<p class="hint" id="c-area-fixed" data-area-fixed hidden>Basic and mid-range renovation figures are whole-villa scope examples from a published guide. They do not change with floor area, so the area is not used for them.</p>
<p class="hint" id="c-area-open" data-area-open hidden>For luxury and ultra-luxury renovations, the area sets only the high figure, at the lowest new-build rate for the specification.</p></div>
<fieldset><legend>Specification</legend><div class="calc-tiers">{tiers}</div>
<p class="hint is-off" data-reno-hint>For renovations, the specification selects a whole-villa scope example from a published guide, not a rate per square foot. Basic and mid-range examples do not change with floor area, so they can read low for a large or older villa. Pool and landscaping are added on top of the band, and a basic refresh carries no design fees or approvals allowance.</p></fieldset>
<fieldset><legend>Extras</legend>
<div class="calc-row"><div data-new-only><label for="c-base">Basement area (<span data-unit>sq ft</span>)</label><input id="c-base" name="basement" type="number" inputmode="numeric" min="0" step="50" value="0"></div>
<div><label for="c-garden">Landscaped garden (<span data-unit>sq ft</span>)</label><input id="c-garden" name="garden" type="number" inputmode="numeric" min="0" step="50" value="{EXAMPLE["garden"]}"></div></div>
<div class="calc-checks">
<label><input type="checkbox" name="pool" checked> Swimming pool</label>
<label><input type="checkbox" name="smart"> Smart home and AV</label>
<label><input type="checkbox" name="ffe"> Furniture, fixtures and equipment</label>
<label data-new-only><input type="checkbox" name="demo"> Demolish an existing villa first</label></div>
<p class="hint">Basement and demolition apply to new builds only. New build and renovation each keep their own pool and garden choices when you switch between them.</p></fieldset>
{calc_messages()}
</form>'''

# ---------------------------------------------------------------- copy
FAQS = [
    ("How much does it cost to build a villa in Dubai per square foot?",
     "Published 2025–26 ranges for construction only are about AED 300–500 per sq ft for a standard specification, "
     "AED 500–850 for premium, AED 850–1,200 for luxury (Engel &amp; Völkers goes up to 1,400) and AED 1,200 and upwards for ultra-luxury (Engel &amp; Völkers, "
     "Real Estate Club Dubai, Knight Frank via Gulf Construction). Design fees, approvals, contingency and furniture come on top."),
    ("What does the per square foot rate leave out?",
     "The rate covers the build itself. On top you should budget design and engineering fees (typically 6–12% of construction), "
     "approvals, NOCs and utility connections (AED 25,000–75,000, or 2–5% of the build, depending on the source), a contingency of 10–15%, "
     "and any pool, landscaping, smart home or furniture. Plot cost, VAT and finance are also outside the rate."),
    ("How much does a villa renovation cost in Dubai?",
     "A 2026 guide from Smart Renovation puts a basic renovation (painting, flooring, small upgrades) from around AED 200,000–300,000, "
     "a mid-range renovation of kitchens, bathrooms and interiors at AED 400,000–800,000, and a luxury renovation with structural "
     "changes above AED 1 million. Works typically take two to six months, longer for structural changes or extensions."),
    ("How long does it take to build a villa in Dubai?",
     "Typical phases are design 3–4 months, approvals 2–3 months, construction 8–14 months and snagging 1–2 months: about 14–23 months "
     "end to end, while Real Estate Club Dubai quotes 12–24 months from plot to keys because phases can overlap. Custom luxury villas commonly take 24–36 months (Real Estate Club Dubai)."),
    ("How accurate is this calculator?",
     "It is an indicative estimate built from published market ranges, not a quote. The real figure depends on the design, the ground, "
     "the contract and the market when you tender. Treat the range as a starting point for a conversation with your consultant, and test it "
     "against a proper cost plan before you commit to a plot or a design. We are happy to check it against your plot."),
]

def worked_table():
    e = estimate(EXAMPLE)
    rows = "".join(f'<tr><th scope="row">{lbl}</th><td class="num">{aed(e[k][0])}</td><td class="num">{aed(e[k][1])}</td><td class="num">{aed(e[k][2])}</td></tr>'
                   for k, lbl in LINES if any(e[k]))
    return f'''<div class="table-wrap"><table class="table"><caption class="sr">Worked example: 6,000 sq ft premium new-build villa</caption>
<thead><tr><th scope="col">Cost line</th><th scope="col" class="num">Low</th><th scope="col" class="num">Likely</th><th scope="col" class="num">High</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><td>Total</td><td class="num">{aed(e["total"][0])}</td><td class="num">{aed(e["total"][1])}</td><td class="num">{aed(e["total"][2])}</td></tr></tfoot></table></div>''', e

def tier_table():
    rows = ""
    for k, t in RATES["tiers"].items():
        e = estimate({**EXAMPLE, "tier": k, "pool": False, "garden": 0})
        plus = "+" if t.get("open") else ""
        rows += (f'<tr><th scope="row">{esc(t["label"])}</th><td class="num">{t["nb"][0]:,}–{t["nb"][1]:,}{plus}</td>'
                 f'<td class="num">{per_m2(t["nb"][0]):,}–{per_m2(t["nb"][1]):,}{plus}</td>'
                 f'<td class="num">{compact(e["construction"][0])}–{compact(e["construction"][2])}{plus}</td>'
                 f'<td class="num">{compact(e["total"][0])}–{compact(e["total"][2])}{plus}</td></tr>')
    return f'''<div class="table-wrap"><table class="table"><caption class="sr">Construction rates by specification, and a 6,000 sq ft villa at each</caption>
<thead><tr><th scope="col">Specification</th><th scope="col" class="num">AED per sq ft</th><th scope="col" class="num">AED per m²</th><th scope="col" class="num">6,000 sq ft build</th><th scope="col" class="num">With soft costs</th></tr></thead>
<tbody>{rows}</tbody></table></div>'''

def calculator():
    crumbs = [("Home", "/"), ("Tools", "/tools/"), ("Villa build cost calculator", CALC_PATH)]
    wt, e = worked_table()
    srcs = "".join(f'<li id="src-{k}">{esc(t)}. <a href="{u}" rel="noopener">{esc(u.split("//", 1)[1].split("/", 1)[0])}</a></li>' for k, t, u in SOURCES)
    # The script needs only the numbers; every word it shows comes from #calc-msgs.
    js_rates = {**RATES, "tiers": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in RATES["tiers"].items()},
                "reno": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in RATES["reno"].items()}}
    data = json.dumps(js_rates, separators=(",", ":"))
    body = B.page_head(crumbs, "Villa build and renovation cost calculator",
                       "An indicative cost for building or renovating a private villa in Dubai or Abu Dhabi, from published 2025–26 market ranges. "
                       "Every rate is sourced on this page. It is an estimate, not a quote.").replace('class="page-head"', 'class="page-head page-head--tool"', 1) + f'''
<section class="section--tight calc-sec"><div class="wrap calc">
{form_html()}
{results_html(e)}
</div></section>
<script type="application/json" id="calc-data">{data}</script>
<script src="/assets/calc.js" defer></script>

<section class="section--tight paper"><div class="wrap split"><div><h2>How the estimate works</h2></div><div class="prose">
<p>The short answer: a new villa in Dubai costs roughly AED 300–500 per sq ft to build at a standard specification and AED 850–1,400 at a luxury one, before fees, approvals, contingency and furniture. The calculator adds those layers so the total is closer to what an owner actually spends.</p>
<ol>
<li><strong>Construction.</strong> Built-up area multiplied by the published rate for your specification.{cite("ev", "kf", "reca", "opt")} The likely figure is the midpoint of the range. A basement is priced as extra built-up area at the same rate.</li>
<li><strong>Extras.</strong> Pool AED 80,000–250,000; landscaping AED 100–500 per sq ft of garden; smart home and AV AED 50,000–300,000; demolition of an existing villa AED 50,000–200,000.{cite("recc", "reca")}</li>
<li><strong>Design and engineering fees.</strong> 6–12% of construction, about 9% typical for a multi-discipline practice.{cite("reca", "opt")}</li>
<li><strong>Approvals, NOCs and connections.</strong> Real Estate Club Dubai gives AED 25,000–75,000 for approvals, NOCs and DEWA{cite("recc")} and, elsewhere, 2–5% of the build for approvals and permits.{cite("reca")} As our own assumption, the calculator uses the fixed AED 25,000–75,000 band; on a large or complex villa the percentage figure would be higher. For comparison, Engel &amp; Völkers puts design, engineering and permits together at AED 50,000–150,000.{cite("ev")} A basic renovation refresh carries no approvals allowance.</li>
<li><strong>Contingency.</strong> 10–15% of construction, 12% as the likely figure.{cite("reca", "recc")}</li>
<li><strong>Furniture, fixtures and equipment.</strong> 30–40% of construction at the top end of the market.{cite("reca", "recc")} On standard and premium specifications treat this as a ceiling.</li>
</ol>
<p>Renovations work differently. The calculator uses Smart Renovation's whole-villa bands by scope rather than rates per square foot: basic AED 200,000–300,000, mid-range AED 400,000–800,000, and luxury above AED 1 million.{cite("sr")} Those bands suit a typical villa; on a large or older villa needing new services and waterproofing, a per square foot budget will be higher, as our <a href="/insights/villa-renovation-cost-dubai/">renovation cost guide</a> explains. Pool and landscaping are added on top of the band.</p>
</div></div></section>

<section class="section--tight"><div class="wrap split"><div><h2>Build rates by specification</h2><p class="muted">Construction only, 2025–26. The right-hand columns apply each rate to a 6,000 sq ft villa with no extras.</p></div><div class="prose">
{tier_table()}
<p class="small muted">Sources: Engel &amp; Völkers, Real Estate Club Dubai, Knight Frank via Gulf Construction, Optimal Engineering. Knight Frank's Q2 2025 figures were about AED 4,200 per m² (around AED 390 per sq ft) for standard and AED 11,000 per m² (around AED 1,020 per sq ft) for high-end construction.{cite("kf")}</p>
</div></div></section>

<section class="section--tight paper"><div class="wrap split"><div><h2>Worked example</h2><p class="muted">A 6,000 sq ft premium new-build villa in Dubai Hills Estate, with a pool and 3,000 sq ft of landscaped garden. This is what the calculator shows when it first loads.</p></div><div class="prose">
{wt}
<p>The likely total of {aed(e["total"][1])} works out at about {aed_rate(e["total"][1] / EXAMPLE["area"])} per sq ft of built-up area once fees, approvals and contingency are added, against a construction-only rate of {aed_rate(e["build"][1] / EXAMPLE["area"])}. That gap is why a headline per-square-foot rate on its own understates the budget.</p>
</div></div></section>

<section class="section--tight"><div class="wrap split"><div><h2>What moves the number most</h2></div><div class="prose">
<p>From the contractor's side of the table, where our founder spent 21 years, specification moves a villa budget far more than size. Two houses of the same area can differ by a factor of three once glazing, stone, joinery and services are chosen. When we priced a job as the builder, the first things we looked at were the frame, the ground and the window package, because that is where the money and the risk sit.</p>
<ul>
<li><strong>Ground and basements.</strong> Shoring, dewatering and waterproofing depend on the plot. We price basements at the build rate, but on a waterfront plot the real figure can be higher.</li>
<li><strong>Glazing and façade.</strong> Large-format and structural glazing is one of the quickest ways to move from premium into luxury rates.</li>
<li><strong>Services.</strong> Cooling, automation and pool plant grow with specification and are easy to under-describe in a tender.</li>
<li><strong>The design itself.</strong> In August 2025 Dubai Municipality warned villa engineering consultancies about over-designing structures and inflating build costs.{cite("gn")} A design review before tender is usually cheaper than a variation after it.</li>
</ul>
</div></div></section>

<section class="section--tight paper"><div class="wrap split"><div><h2>What is not included</h2></div><div class="prose">
<ul>
<li>The plot, transfer fees and any service charges.</li>
<li>VAT. Published rates do not consistently state whether 5% VAT is included; allow for 5% VAT on contractor invoices if your quotes exclude it.{cite("recc")}</li>
<li>Finance costs, insurance and your own advisers' fees, including ours.</li>
<li>Cost inflation. Currie &amp; Brown forecast about 3% for UAE construction in 2026; the calculator does not apply it.{cite("pra")}</li>
<li>A location premium. We have found no published source that supports one, so the area you choose changes the approvals route shown, not the rate.</li>
</ul>
</div></div></section>

<section class="section--tight" id="sources"><div class="wrap split"><div><h2>Sources and assumptions</h2></div><div class="prose">
<ol class="calc-sources">{srcs}</ol>
<h3>Assumptions</h3>
<ul>
<li>The likely figure for each rate is the midpoint of the published range, except design fees (9%), contingency (12%) and furniture (35%), where the sources give a typical figure.</li>
<li>Luxury uses Real Estate Club Dubai's AED 850–1,200 per sq ft. Ultra-luxury has no published ceiling: the calculator uses AED 1,200 (Real Estate Club Dubai's floor) to 1,400 (the top of Engel &amp; Völkers' luxury range) per sq ft and marks the high figure with a plus sign.</li>
<li>Approvals use the fixed AED 25,000–75,000 band rather than a percentage of the build; this is our own choice between two published figures.</li>
<li>A basic renovation refresh (painting, flooring, small upgrades) carries no design fees or approvals allowance, because cosmetic work rarely needs drawings or an authority permit. Your master developer may still require an NOC.</li>
<li>Luxury renovations are published as "above AED 1 million". As our own rule of thumb, a full strip-out back to structure approaches new-build cost, so the high figure is the area multiplied by the lowest new-build rate for that specification.</li>
<li>Basements are priced as extra built-up area at the chosen rate. No published Dubai figure separates them.</li>
<li>Timelines: design 3–4 months, approvals 2–3 months, construction 8–14 months, snagging 1–2 months; 24–36 months plot to keys for custom luxury.{cite("reca")} Renovation works two to six months or longer, with approvals taking a few weeks.{cite("sr")}</li>
<li>Each cost line is rounded to the nearest AED 1,000, or AED 10,000 above AED 1 million. Construction and the totals are the sums of the rounded lines, so the figures shown add up.</li>
<li>Basic and mid-range renovation bands are whole-villa scope examples from a published guide. No published source gives a reliable way to scale them with floor area, so the calculator does not use the area for them; a large or older villa needs a project-specific assessment.</li>
</ul>
<p class="small muted">Rates last checked October 2026. This page gives general information, not financial, legal or engineering advice.</p>
</div></div></section>

<section class="section--tight paper"><div class="wrap split"><div><h2>Questions</h2></div><div>{B.faq_html(FAQS)}</div></div></section>

<section class="section dark calc-cta"><div class="wrap split"><div><h2>Get this checked against your plot</h2></div><div>
<p class="lede">A calculator cannot see your plot's ground conditions, setbacks or master developer rules. We can. We review the plot, the brief and the budget together before you commit, and tell you plainly whether the numbers hold.</p>
<p><a class="btn" href="/contact/">Get this checked against your plot</a> <a class="btn btn--ghost" href="/services/plot-due-diligence/">About plot due diligence</a></p>
</div></div></section>'''
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "@id": B.url(CALC_PATH) + "#app",
         "name": "Villa build and renovation cost calculator (Dubai and Abu Dhabi)", "url": B.url(CALC_PATH),
         "description": "Indicative low, likely and high costs for building or renovating a villa in Dubai or Abu Dhabi, including design fees, approvals, contingency and a timeline, from published 2025–26 market ranges.",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "inLanguage": "en-GB", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AED"},
         "publisher": {"@id": B.ORG_ID}, "provider": {"@id": B.ORG_ID},
         "citation": [u for _, _, u in SOURCES]},
        B.faq_schema(FAQS),
    ]
    B.page(CALC_PATH, "Villa Build Cost Calculator: Dubai & Abu Dhabi | Eastbridge",
           "Estimate the cost to build or renovate a villa in Dubai or Abu Dhabi: low, likely and high totals with fees, approvals, contingency and timeline, all sourced.",
           body, crumbs, schema)

def tools_hub():
    crumbs = [("Home", "/"), ("Tools", "/tools/")]
    body = B.page_head(crumbs, "Tools for villa owners",
                       "Free planning tools for owners building or renovating a villa in Dubai or Abu Dhabi. Each one shows its sources.") + f'''
<section class="section--tight"><div class="wrap split"><div><h2>Available tools</h2></div><div class="prose">
<h3><a href="{CALC_PATH}">Villa build and renovation cost calculator</a></h3>
<p>Low, likely and high costs for a new build or renovation, with design fees, approvals, contingency, furniture and an indicative timeline. Built from published 2025–26 market ranges, each one cited.</p>
<p><a class="btn" href="{CALC_PATH}">Open the calculator</a></p>
<h3>Further reading</h3>
<ul><li><a href="/insights/villa-construction-cost-dubai/">What it costs to build a villa in Dubai</a></li>
<li><a href="/insights/buying-a-villa-plot-in-dubai-checks/">Checks before buying a villa plot</a></li>
<li><a href="/fees/">How our fees work</a></li></ul>
</div></div></section>
{B.cta_band("Have a plot or a villa in mind?")}'''
    schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "url": B.url("/tools/"), "name": "Tools for villa owners",
               "hasPart": [{"@id": B.url(CALC_PATH) + "#app"}]}]
    B.page("/tools/", "Villa Planning Tools: Dubai & Abu Dhabi | Eastbridge",
           "Free, sourced planning tools for villa owners in Dubai and Abu Dhabi, starting with a build and renovation cost calculator covering fees, approvals and timeline.",
           body, crumbs, schema)

def build_tools():
    tools_hub()
    calculator()
