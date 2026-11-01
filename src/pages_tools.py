"""Interactive tools: the /tools/ hub and the villa build and renovation cost calculator.

Every rate used by the calculator lives in RATES below and is cited in SOURCES. The same
RATES object is embedded in the page as JSON and read by src/static/assets/calc.js, so the
server-rendered worked example and the live calculator always use identical figures.
"""
import json
import math
import re
import html as H
import build as B
import config as C
from content.areas import AREAS

esc = H.escape
CALC_PATH = "/tools/villa-build-cost-calculator/"
THANKS_PATH = CALC_PATH + "thanks/"
EMBED_PATH = CALC_PATH + "embed/"      # calculator only, for other sites' iframes (noindex, canonical to CALC_PATH)
EMBED_HEIGHT = 1600                     # default iframe height in the embed code, in CSS pixels
SQFT_PER_M2 = 10.7639

# ---------------------------------------------------------------- sources
SOURCES = [
    ("ev", "Engel & Völkers, Construction cost in Dubai (December 2025)",
     "https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai"),
    ("kf", "Knight Frank Q2 2025 construction costs, reported by Gulf Construction",
     "https://gulfconstructiononline.com/ArticleTA/436847"),
    ("tt", "Turner & Townsend, UAE market intelligence Q1 2024: construction cost performance (individual detached villas, AED per m²)",
     "https://assets.foleon.com/eu-central-1/de-uploads-7e3kk3/48604/uaemi_24_construction_cost_performance.58a8c5990842.pdf"),
    ("opt", "Optimal Engineering Consultants, Cost to build a villa in Dubai (2026 guide, March 2026)",
     "https://www.optimal.ae/blog/cost-to-build-a-villa-in-dubai"),
    ("sr", "Smart Renovation, Villa renovation in Dubai: 2026 guide to costs, timeline and permits",
     "https://smartrenovation.ae/villa-renovation-in-dubai-complete-2026-guide-to-costs-timeline-permits/"),
    ("tt25", "Turner & Townsend, UAE market intelligence 2025: construction cost performance (inflation, preliminaries)",
     "https://marketintelligence.turnerandtownsend.com/uaemi-2025/construction-cost-performance/"),
    ("pra", "PRASOON, Owner's representative vs project manager in the UAE (citing Currie & Brown)",
     "https://prasoon.design/insights/owners-representative-vs-project-manager-uae"),
    ("gn", "Gulf News, Dubai Municipality warns consultancies over inflated villa designs (August 2025)",
     "https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704"),
    ("vat", "PwC Worldwide Tax Summaries, United Arab Emirates: other taxes (VAT)",
     "https://taxsummaries.pwc.com/united-arab-emirates/corporate/other-taxes"),
    # Currency display (FX below). Titles carry no date, so the monthly rate refresh changes only FX_AS_AT.
    ("peg", "Gulf News, Creation, history and evolution of the UAE dirham (the dirham's peg of AED 3.6725 to the US dollar)",
     "https://gulfnews.com/uae/year-of-the-50th/creation-history-and-evolution-of-the-uae-dirham-1.1621767243152"),
    ("ecb", "European Central Bank, euro foreign exchange reference rates",
     "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"),
    ("cbr", "Bank of Russia, official exchange rates of foreign currencies against the rouble",
     "https://www.cbr.ru/eng/currency_base/daily/"),
    # Real Estate Club Dubai is a property information and lead-referral website, not a primary or industry source.
    # It is cited only for the figures we could not find in a primary or industry source (landscaping, smart home,
    # demolition, FF&E, the fixed approvals band and the phase durations), and its links carry rel="nofollow".
    ("reca", "Real Estate Club Dubai (property information website), Villa architects in Dubai: FF&E, approvals and timelines",
     "https://realestateclubdubai.com/dubai-villa-architects"),
    ("recc", "Real Estate Club Dubai (property information website), Villa build cost calculator methodology",
     "https://realestateclubdubai.com/tools/villa-build-cost-calculator"),
]
NOFOLLOW = {"reca", "recc"}

def rel_of(k):
    return "nofollow noopener" if k in NOFOLLOW else "noopener"
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
    # Renovation: published whole-villa bands by scope (Smart Renovation guide). null = no published ceiling: only the
    # starting figure is shown and anything above it needs a project-specific assessment. No size formula is used.
    # "months" are the guide's durations: interior upgrades two to three months, kitchens and bathrooms four to six,
    # structural changes, extensions or complete redesign six months or longer.
    "reno": {
        # "soft": False = no design fees or approvals allowance (cosmetic work rarely needs drawings or a permit).
        "standard": {"label": "Basic refresh: painting, flooring, small upgrades", "cost": [200000, 300000], "months": [2, 3], "soft": False},
        "premium": {"label": "Mid-range: kitchens, bathrooms and interiors", "cost": [400000, 800000], "months": [4, 6]},
        "luxury": {"label": "Luxury: premium materials and structural changes", "cost": [1000000, None], "months": [6, None]},
        # The guide publishes no separate ultra-luxury band, so it is treated exactly as luxury.
        "ultra": {"label": "Ultra-luxury: no separate published band, treated as luxury", "cost": [1000000, None], "months": [6, None]},
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

# Month the construction rates above were last reviewed against their sources (year, month). Shown near the
# result as "Rates last reviewed: <month year>, by Philip Chapman". The AUTOMATION.md monthly step updates it.
RATES_REVIEWED = (2026, 10)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

def month_year(ym):
    return f"{MONTHS[ym[1] - 1]} {ym[0]}"

# ---------------------------------------------------------------- currency display (AED is the only calculation currency)
# Fixed rates, never fetched live. The figures below are copied from the published sources (SOURCES "peg", "ecb", "cbr")
# and converted to AED per one unit of each currency. Display-only: every estimate is calculated in AED and converted
# figures are labelled "approximate, at rates of <FX_AS_AT>". Refresh monthly (AUTOMATION.md, Monthly).
#   - AED 3.6725 per US dollar: the dirham's fixed peg (Central Bank of the UAE, since November 1997).
#   - ECB euro reference rates of 30 October 2026: 1 EUR = 1.1172 USD = 0.83380 GBP = 7.4326 CNY = 106.0840 INR.
#     (The ECB publishes no rouble rate.)
#   - Bank of Russia official rate set on 30 October 2026 (effective 31 October): 1 AED = 21.9353 RUB.
FX_AS_AT = "2026-10-30"
FX_INPUTS = {
    "aedPerUsd": 3.6725,
    "ecbPerEur": {"USD": 1.1172, "GBP": 0.83380, "CNY": 7.4326, "INR": 106.0840},
    "rubPerAed": 21.9353,
}

def _fx_table(i):
    aed_per_eur = i["ecbPerEur"]["USD"] * i["aedPerUsd"]
    per = {"USD": i["aedPerUsd"], "EUR": aed_per_eur, "GBP": aed_per_eur / i["ecbPerEur"]["GBP"],
           "CNY": aed_per_eur / i["ecbPerEur"]["CNY"], "INR": aed_per_eur / i["ecbPerEur"]["INR"],
           "RUB": 1 / i["rubPerAed"]}
    return {k: round(v, 6) for k, v in per.items()}

FX = {"asAt": FX_AS_AT, "aedPer": _fx_table(FX_INPUTS)}

# (code, option label, language page that also offers it). AED is the default everywhere; GBP, USD and EUR are
# offered on every page, RUB only on /ru/, CNY only on /zh/ and INR only on /hi/ (calc.js removes the others).
CURRENCIES = [
    ("AED", "UAE dirham (AED)", None), ("GBP", "British pound (GBP)", None), ("USD", "US dollar (USD)", None),
    ("EUR", "Euro (EUR)", None), ("RUB", "Russian rouble (RUB)", "ru"), ("CNY", "Chinese yuan (CNY)", "zh"),
    ("INR", "Indian rupee (INR)", "hi"),
]
# How a converted amount is written: (full figure, thousands, millions). Translators may adapt them per language.
CUR_FORMAT = {
    "GBP": ("£{n}", "£{n}k", "£{n}m"), "USD": ("US${n}", "US${n}k", "US${n}m"), "EUR": ("€{n}", "€{n}k", "€{n}m"),
    "RUB": ("RUB {n}", "RUB {n}k", "RUB {n}m"), "CNY": ("CNY {n}", "CNY {n}k", "CNY {n}m"),
    "INR": ("INR {n}", "INR {n}k", "INR {n}m"),
}

def fx_date_text():
    y, m, d = (int(x) for x in FX_AS_AT.split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"

def fx_list(codes):
    return "; ".join("%s %s" % (c, format(FX["aedPer"][c], ".4g")) for c in codes)

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
        low_only = hi is None          # no published ceiling: only the starting column is meaningful
        out["build"] = [lo, lo, lo] if low_only else tri([lo, hi])
        out["basement"] = z
        out["demo"] = z
        open_hi = low_only
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
    out["low_only"] = i["mode"] != "new" and open_hi
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
    r["low_only"] = e.get("low_only", False)
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
    "reno-open": "Construction from {cons} · luxury renovations are published only as above AED 1 million, so this is a starting figure; anything above it needs a project-specific assessment",
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
        s = f"About {a}–{b} months on these phases end to end, less where they overlap. Engel &amp; Völkers puts most villas at 12–24 months from approval to completion."
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
         ("rowBuild-new", LINES[0][1]), ("rowBuild-reno", "Renovation works (whole-villa scope band)"),
         ("enterArea", "Enter the built-up area to see an estimate."),
         ("srLikely", "Likely total:"), ("srFrom", "Starting total:")]
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
    # Currency display, sharing and the WhatsApp summary.
    for c, (full, k, mm) in CUR_FORMAT.items():
        m += [(f"money-{c}", full), (f"moneyK-{c}", k), (f"moneyM-{c}", mm)]
    m += [("fxNote", "Calculated in AED: {aed}. Other currencies are approximate, at rates of {date}."),
          ("copied", "Link copied. Anyone with the link sees this estimate."),
          ("copyFail", "Copy this link:"), ("none", "None"),
          ("wa-new", "Hello, I used your villa cost calculator: new build, {area}, {tier}, {loc}, likely {total}. Could we talk it through?"),
          ("wa-reno", "Hello, I used your villa cost calculator: renovation, {tier}, {loc}, likely {total}. Could we talk it through?"),
          ("wa-from", "Hello, I used your villa cost calculator: renovation, {tier}, {loc}, from {total}. Could we talk it through?"),
          ("wa-none", "Hello, I used your villa cost calculator and would like to talk through my project."),
          ("embedCopied", "Code copied. Paste it into your page's HTML where the calculator should appear."),
          ("embedCopyFail", "Select the code above and copy it with your keyboard.")]
    items = "".join(f'<li data-m="{k}">{v}</li>' for k, v in m)
    devs = sorted({a["developer"] for a in AREAS if a.get("developer")})
    items += "".join(f'<li data-dev="{esc(d)}">{esc(d)}</li>' for d in devs)
    return f'<div class="calc-msgs" id="calc-msgs" hidden><ul>{items}</ul></div>'

# ---------------------------------------------------------------- share, save and send
SITE_HOST = C.SITE_URL.split("//", 1)[1]
WA_DEFAULT = "Hello, I used your villa cost calculator and would like to talk through my project."

def print_head():
    """Letterhead and input summary, shown only when the estimate is printed or saved as PDF.
    calc.js fills the date, the input list and the link from the form (so they are in the page's language)."""
    return f'''<div class="print-only calc-print-head">
<p class="calc-print-brand"><img src="/assets/logo.png" alt="" width="40" height="40"><span>{esc(C.NAME)}</span></p>
<p class="calc-print-title">Indicative villa cost estimate</p>
<p class="calc-print-meta">Prepared on <span data-print-date></span> with the villa build cost calculator at {SITE_HOST}</p>
<h3 class="calc-h">Your inputs</h3>
<dl class="calc-print-inputs" data-print-inputs></dl>
</div>'''

def print_foot():
    names = "Engel &amp; Völkers, Knight Frank (via Gulf Construction), Turner &amp; Townsend, Optimal Engineering and Smart Renovation, with Real Estate Club Dubai for the few lines no industry source covers"
    return f'''<div class="print-only calc-print-foot">
<p><b>Sources.</b> Rates are published 2025–26 market ranges from {names}. Other currencies are converted from AED using the dirham’s US dollar peg, the European Central Bank’s euro reference rates and the Bank of Russia’s official rate. Full sources, assumptions and method: {SITE_HOST}{CALC_PATH}#sources</p>
<p class="calc-print-link">Open this estimate online: <span data-print-url>{SITE_HOST}{CALC_PATH}</span></p>
<p class="calc-print-contact"><b>{esc(C.NAME)}</b> · Client-side project management for private villas in Dubai and Abu Dhabi · {C.EMAIL} · {C.PHONE_DISPLAY} · {SITE_HOST}</p>
</div>'''

def actions_html():
    """Copy link, Save as PDF, WhatsApp and send. Hidden until calc.js runs, because each one needs the live estimate."""
    return f'''<div class="calc-actions" data-calc-actions hidden>
<p class="calc-h">Keep or share this estimate</p>
<div class="calc-actions__row">
<button type="button" class="btn btn--ghost btn--sm" data-copy-link>Copy link</button>
<button type="button" class="btn btn--ghost btn--sm" data-print>Save as PDF</button>
<a class="btn btn--ghost btn--sm" data-wa-estimate href="{B.wa_link(WA_DEFAULT)}" rel="noopener">Discuss on WhatsApp</a>
<a class="btn btn--sm" href="#send">Send this estimate to Philip</a>
</div>
<p class="calc-status" data-copy-status role="status" aria-live="polite"></p>
<input class="calc-copy-fallback" data-copy-fallback type="text" readonly hidden aria-label="Link to this estimate">
</div>'''

def send_form_html():
    """'Send this estimate to Philip': Netlify form "estimate". calc.js keeps the hidden fields in step with the
    calculator (inputs as codes, the AED result and any converted figures, and the shareable link)."""
    first = esc(C.FOUNDER["name"].split()[0])
    return f'''<section class="section--tight paper calc-send" id="send"><div class="wrap split">
<div><h2>Send this estimate to {first}</h2>
<p class="muted">Your inputs and the line-by-line result go with the form, so there is nothing to retype. {esc(C.RESPONSE_PROMISE)}, with his view on whether the figures look realistic for your plot and specification. It is free and confidential.</p></div>
<form class="form calc-send__form" name="estimate" method="POST" action="{THANKS_PATH}" data-netlify="true" netlify-honeypot="company_site" data-estimate>
<input type="hidden" name="form-name" value="estimate">
<input type="hidden" name="estimate_inputs" value="">
<input type="hidden" name="estimate_result" value="">
<input type="hidden" name="estimate_link" value="">
<input type="hidden" name="currency" value="AED">
<p class="hp"><label>Leave this empty <input name="company_site" tabindex="-1" autocomplete="off"></label></p>
<div class="row"><div><label for="e-name">Your name</label><input id="e-name" name="name" autocomplete="name" required></div>
<div><label for="e-email">Email</label><input id="e-email" name="email" type="email" autocomplete="email" inputmode="email" required></div></div>
<div class="row"><div><label for="e-phone">Phone or WhatsApp number <span class="opt">Optional</span></label><input id="e-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" aria-describedby="e-phone-hint"><p class="hint" id="e-phone-hint">Include the country code, for example +971 or +44.</p></div>
<div><label for="e-plot">Plot location <span class="opt">Optional</span></label><input id="e-plot" name="plot" autocomplete="off" aria-describedby="e-plot-hint"><p class="hint" id="e-plot-hint">The community, and the plot number if you have one.</p></div></div>
<div><label for="e-notes">Notes <span class="opt">Optional</span></label><textarea id="e-notes" name="message" rows="4" aria-describedby="e-notes-hint"></textarea><p class="hint" id="e-notes-hint">Anything the calculator cannot see: the design stage, quotes you already have, or what worries you.</p></div>
<div><label class="consent" for="e-mkt"><input id="e-mkt" name="marketing_opt_in" type="checkbox" value="yes"> <span>Optional: also send me Eastbridge notes for villa owners by email, no more than once a month. Leaving this unticked does not affect your estimate. Unsubscribe at any time by replying to any note or writing to {C.EMAIL}.</span></label></div>
<p class="small muted calc-send__privacy"><b>We never pass your details to contractors or suppliers.</b> {first} reads every estimate personally and uses your details to reply to you. See our <a href="/privacy/">privacy notice</a>.</p>
<p class="submit-row"><button class="btn" type="submit">Send this estimate to {first}</button></p>
</form></div></section>'''

def embed_actions_html():
    """Embed page only: the estimate continues on the full calculator (save, share, send), in a new tab.
    calc.js adds the inputs to the link, so the full page opens on the same estimate."""
    return f'''<div class="calc-actions calc-actions--embed">
<p class="calc-h">Save, share or have this estimate checked</p>
<p class="calc-actions__row"><a class="btn btn--sm" data-full-link href="{CALC_PATH}" target="_blank" rel="noopener">Open this estimate in the full calculator</a></p>
<p class="calc-note">The full calculator adds the sources for every rate, a PDF copy and a free check of the figures by {esc(C.FOUNDER["name"])}.</p>
</div>'''

def results_html(e, embed=False):
    """Server-rendered result panel. calc.js updates the same nodes in place (no layout shift).
    embed=True: the version inside other sites' iframes, with no print letterhead and no share or send buttons."""
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
    sources = f'{CALC_PATH}#sources" target="_blank" rel="noopener' if embed else "#sources"
    return f'''<div class="calc-out" id="calc-out">
{"" if embed else print_head()}
<p class="calc-label">Indicative total, including soft costs</p>
<p class="calc-total" aria-live="polite" aria-atomic="true"><span class="sr" data-sr>Likely total: </span><b data-out="likely">{aed(e["total"][1])}</b>
<span class="calc-range">Range <span data-out="low">{aed(e["total"][0])}</span> to <span data-out="high">{aed(e["total"][2])}{hi_sfx}</span></span></p>
<p class="calc-fx" data-fx-note hidden></p>
<p class="calc-sub" data-out="sub">{sub}</p>
<p class="calc-reviewed">Rates last reviewed: {month_year(RATES_REVIEWED)}, by {esc(C.FOUNDER["name"])}</p>
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
<p class="calc-flag">An indicative estimate from published market ranges, not a quotation. Each line is rounded and the totals are the sum of the lines. Excludes the plot, finance, insurance, cost inflation and advisers' fees, including ours; allow for 5% VAT if your quotes exclude it. <a href="{sources}">Sources and assumptions</a></p>
{embed_actions_html() if embed else actions_html()}
{"" if embed else print_foot()}
</div>'''

def form_html():
    tiers = "".join(
        f'<label class="calc-opt"><input type="radio" name="tier" value="{k}"{" checked" if k == EXAMPLE["tier"] else ""}>'
        f'<span><b>{esc(v["label"])}</b><small data-tier-note="{k}">{tier_new_note(v, "sqft")}</small></span></label>'
        for k, v in RATES["tiers"].items())
    dubai = "".join(f'<option value="{a["slug"]}" data-city="Dubai" data-dev="{esc(a["developer"])}"{" selected" if a["slug"] == EXAMPLE["loc"] else ""}>{esc(a["name"])}</option>' for a in AREAS if a["city"] == "Dubai")
    ad = "".join(f'<option value="{a["slug"]}" data-city="Abu Dhabi" data-dev="{esc(a["developer"])}">{esc(a["name"])}</option>' for a in AREAS if a["city"] == "Abu Dhabi")
    def cur_opt(c, lbl, lang):
        extra = (' data-cur-lang="%s"' % lang if lang else "") + (" selected" if c == "AED" else "")
        return f'<option value="{c}"{extra}>{esc(lbl)}</option>'
    curs = "".join(cur_opt(*x) for x in CURRENCIES)
    return f'''<form class="calc-in" id="calc" novalidate onsubmit="return false">
<fieldset><legend>Project type</legend><div class="calc-seg">
<label><input type="radio" name="mode" value="new" checked><span>New build</span></label>
<label><input type="radio" name="mode" value="reno"><span>Renovation</span></label></div></fieldset>
<div><label for="c-loc">Where is the villa?</label><select id="c-loc" name="loc">
<optgroup label="Dubai">{dubai}<option value="dubai" data-city="Dubai" data-dev="">Elsewhere in Dubai</option></optgroup>
<optgroup label="Abu Dhabi">{ad}<option value="abu-dhabi" data-city="Abu Dhabi" data-dev="">Elsewhere in Abu Dhabi</option></optgroup></select>
<p class="hint" data-loc-hint>Location changes the approvals route shown, not the rate. No published source supports a reliable location premium.</p></div>
<fieldset><legend>Units</legend><div class="calc-seg calc-seg--sm">
<label><input type="radio" name="unit" value="sqft" checked><span>sq ft</span></label>
<label><input type="radio" name="unit" value="m2"><span>m²</span></label></div></fieldset>
<div class="calc-cur"><label for="c-cur">Show amounts in</label><select id="c-cur" name="cur" aria-describedby="c-cur-hint">{curs}</select>
<p class="hint" id="c-cur-hint">The estimate is always calculated in UAE dirhams. Other currencies are approximate conversions, at rates of {fx_date_text()}.</p></div>
<div data-area-field><label for="c-area">Built-up area (<span data-unit>sq ft</span>)</label><input id="c-area" name="area" type="number" inputmode="numeric" min="0" step="50" value="{EXAMPLE["area"]}" aria-describedby="c-area-hint">
<p class="hint" id="c-area-hint" data-area-typical>For scale, Optimal Engineering's budget examples use about 3,000 sq ft for a compact villa, 5,000 sq ft for a mid-range villa and 10,000 sq ft or more for a luxury villa.{cite("opt")}</p>
<p class="hint" id="c-area-fixed" data-area-fixed hidden>Renovation figures are whole-villa scope examples from a published guide. They do not change with floor area, so the area is not used for them.</p></div>
<fieldset><legend>Specification</legend><div class="calc-tiers">{tiers}</div>
<p class="hint is-off" data-reno-hint>For renovations, the specification selects a whole-villa scope example from a published guide, not a rate per square foot. The examples do not change with floor area, so they can read low for a large or older villa, and luxury shows only a starting figure. Pool and landscaping are added on top of the band, and a basic refresh carries no design fees or approvals allowance.</p></fieldset>
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
     "Optimal Engineering, Knight Frank via Gulf Construction). Turner &amp; Townsend's UAE figures for an individual detached villa, about AED 460–560 per sq ft "
     "at a medium standard and AED 1,000–1,230 at a prestige standard, sit within those ranges. Design fees, approvals, contingency and furniture come on top."),
    ("What does the per square foot rate leave out?",
     "The rate covers the build itself. On top you should budget design and engineering fees (typically 6–12% of construction), "
     "approvals, NOCs and utility connections (from AED 25,000–75,000 for a straightforward villa to AED 80,000–250,000 in total, depending on the authority and the source), a contingency of 10–15%, "
     "and any pool, landscaping, smart home or furniture. Plot cost, VAT and finance are also outside the rate."),
    ("How much does a villa renovation cost in Dubai?",
     "A 2026 guide from Smart Renovation puts a basic renovation (painting, flooring, small upgrades) from around AED 200,000–300,000, "
     "a mid-range renovation of kitchens, bathrooms and interiors at AED 400,000–800,000, and a luxury renovation with structural "
     "changes above AED 1 million. Works typically take two to six months, longer for structural changes or extensions."),
    ("How long does it take to build a villa in Dubai?",
     "Engel &amp; Völkers puts most villas at 12–24 months from approval to completion. Published phase estimates are design 3–4 months, approvals 2–3 months, "
     "construction 8–14 months and snagging 1–2 months, about 14–23 months end to end, less where phases overlap, and 24–36 months for a custom luxury villa "
     "(Real Estate Club Dubai). Optimal Engineering allows 4–8 weeks for approvals on a straightforward project and typically 12–18 months for construction."),
    ("How accurate is this calculator?",
     "It is an indicative estimate built from published market ranges, not a quote. The real figure depends on the design, the ground, "
     "the contract and the market when you tender. Treat the range as a starting point for a conversation with your consultant, and test it "
     "against a proper cost plan before you commit to a plot or a design. We are happy to check it against your plot."),
]

def embed_code(path=EMBED_PATH):
    return (f'<iframe src="{C.SITE_URL}{path}" title="Villa build cost calculator by {C.NAME}" '
            f'width="100%" height="{EMBED_HEIGHT}" style="border:0;max-width:1100px;display:block" loading="lazy"></iframe>')

def embed_box_html():
    """'Add this calculator to your website' on the full page. The code box is never translated (translate="no");
    calc.js points it at the embed page in the language being viewed and handles "Copy code"."""
    return f'''<section class="section--tight calc-embed" id="embed"><div class="wrap split"><div><h2>Add this calculator to your website</h2>
<p class="muted">For estate agents, architects, lawyers and other advisers whose clients ask what a villa in Dubai or Abu Dhabi costs to build.</p></div><div class="prose">
<p>The calculator is free to use on your own website. Paste the code below into your page's HTML where it should appear. It shows the calculator only, in the same five languages, with a link back to this page for the sources. We keep the rates up to date, so there is nothing for you to maintain, and no analytics or advertising cookies run inside it.</p>
<label class="calc-embed__label" for="embed-code">Embed code</label>
<textarea class="calc-embed__code" id="embed-code" readonly rows="4" spellcheck="false" translate="no" data-embed-code data-site="{C.SITE_URL}">{esc(embed_code())}</textarea>
<p class="calc-embed__row"><button type="button" class="btn btn--sm" data-embed-copy>Copy code</button> <a class="link" href="{EMBED_PATH}" target="_blank" rel="noopener" data-embed-preview>Preview the embedded calculator</a></p>
<p class="calc-status" data-embed-status role="status" aria-live="polite"></p>
<p class="small muted">The iframe is {EMBED_HEIGHT} pixels tall by default; change the height value if your layout needs it. Questions about using it: <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p>
</div></div></section>'''

def embed_page():
    """The calculator alone, for other sites' iframes: no site header, footer or analytics, noindex, canonical to
    the full calculator, and every link opens in a new tab (the rest of the site refuses to be framed)."""
    title = "Villa build and renovation cost calculator"
    data = json.dumps(js_rates(), separators=(",", ":"))
    body = f'''<div class="embed wrap">
<div class="embed__head"><h1 class="embed__title">{title}</h1>
<p class="embed__by"><a href="{CALC_PATH}" target="_blank" rel="noopener">Calculator by {esc(C.NAME)}</a></p></div>
<div class="calc calc--embed">
{form_html()}
{results_html(estimate(EXAMPLE), embed=True)}
</div>
<p class="embed__foot">An indicative estimate from published 2025–26 market ranges, not a quotation. <a href="{CALC_PATH}#sources" target="_blank" rel="noopener">Sources, method and the full calculator</a> at {SITE_HOST}.</p>
</div>
<script type="application/json" id="calc-data">{data}</script>
<script src="/assets/calc.js" defer></script>'''
    # Source numbers point to the list on the full page. Any link without a target would load the full site inside
    # the iframe, which the site's headers forbid, so every link opens in a new tab.
    body = body.replace('href="#src-', f'href="{CALC_PATH}#src-')
    body = re.sub(r'<a (?![^>]*\btarget=)', '<a target="_blank" rel="noopener" ', body)
    crumbs = [("Home", "/"), ("Tools", "/tools/"), ("Villa build cost calculator", CALC_PATH)]
    B.page(EMBED_PATH, "Villa Cost Calculator, Embeddable Version | Eastbridge",
           "The Eastbridge villa build and renovation cost calculator for Dubai and Abu Dhabi, in a compact version for other websites.",
           body, crumbs, noindex=True, canonical=CALC_PATH, bare=True)

def js_rates():
    """The script needs only the numbers; every word it shows comes from #calc-msgs."""
    return {**RATES, "tiers": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in RATES["tiers"].items()},
            "reno": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in RATES["reno"].items()},
            "fx": FX}

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
    srcs = "".join(f'<li id="src-{k}">{esc(t)}. <a href="{u}" rel="{rel_of(k)}">{esc(u.split("//", 1)[1].split("/", 1)[0])}</a></li>' for k, t, u in SOURCES)
    data = json.dumps(js_rates(), separators=(",", ":"))
    body = B.page_head(crumbs, "Villa build and renovation cost calculator",
                       "An indicative cost for building or renovating a private villa in Dubai or Abu Dhabi, from published 2025–26 market ranges. "
                       "Every rate is sourced on this page. It is an estimate, not a quote.").replace('class="page-head"', 'class="page-head page-head--tool"', 1) + f'''
<section class="section--tight calc-sec"><div class="wrap calc">
{form_html()}
{results_html(e)}
</div></section>
{send_form_html()}
<script type="application/json" id="calc-data">{data}</script>
<script src="/assets/calc.js" defer></script>

<section class="section--tight paper"><div class="wrap split"><div><h2>How the estimate works</h2></div><div class="prose">
<p>The short answer: a new villa in Dubai costs roughly AED 300–500 per sq ft to build at a standard specification and AED 850–1,400 at a luxury one, before fees, approvals, contingency and furniture. The calculator adds those layers so the total is closer to what an owner actually spends.</p>
<ol>
<li><strong>Construction.</strong> Built-up area multiplied by the published rate for your specification.{cite("ev", "kf", "opt", "tt")} The likely figure is the midpoint of the range. A basement is priced as extra built-up area at the same rate.</li>
<li><strong>Extras.</strong> Pool AED 80,000–250,000, from a basic fibreglass pool to a standard concrete one.{cite("opt")} Landscaping at AED 100–500 per sq ft of garden, smart home and AV at AED 50,000–300,000 and demolition of an existing villa at AED 50,000–200,000 are the only published figures we have found for these lines, from a property information website.{cite("recc", "reca")} For comparison, Optimal Engineering puts smart home wiring and infrastructure alone at AED 30,000–150,000.{cite("opt")}</li>
<li><strong>Design and engineering fees.</strong> 6–12% of the construction contract value; the calculator uses the 9% midpoint as the likely figure.{cite("opt")}</li>
<li><strong>Approvals, NOCs and connections.</strong> As our own assumption, the calculator uses a fixed band of AED 25,000–75,000 for a straightforward villa.{cite("recc")} Optimal Engineering itemises a Dubai Municipality building permit at AED 15,000–60,000 for a standard villa and a permanent DEWA connection at AED 10,000–40,000, and puts total authority approvals, including Trakhees routes, NOCs and temporary connections, at AED 80,000–250,000;{cite("opt")} on a large, complex or free-zone villa, allow for the higher figure. Engel &amp; Völkers puts design, engineering and permits together at AED 50,000–150,000.{cite("ev")} A basic renovation refresh carries no approvals allowance.</li>
<li><strong>Contingency.</strong> 10–15%, widely recommended.{cite("ev", "opt")} The calculator applies it to construction and uses 12% as the likely figure, our own choice just below the midpoint.</li>
<li><strong>Furniture, fixtures and equipment.</strong> 30–40% of construction at the top end of the market, with 35% as the likely figure. This is the only published percentage we have found, from a property information website.{cite("reca", "recc")} For comparison, Engel &amp; Völkers puts luxury villa interiors at AED 800,000 to over AED 1 million.{cite("ev")} On standard and premium specifications treat it as a ceiling.</li>
</ol>
<p>Renovations work differently. The calculator uses Smart Renovation's whole-villa bands by scope rather than rates per square foot: basic AED 200,000–300,000, mid-range AED 400,000–800,000, and luxury above AED 1 million.{cite("sr")} Those bands suit a typical villa; on a large or older villa needing new services and waterproofing, a per square foot budget will be higher, as our <a href="/insights/villa-renovation-cost-dubai/">renovation cost guide</a> explains. Pool and landscaping are added on top of the band.</p>
<p><strong>Currencies.</strong> Every figure is calculated in UAE dirhams. Pounds, US dollars and euros (and roubles, yuan or rupees on the Russian, Chinese and Hindi pages) are display-only conversions at fixed rates of {fx_date_text()}: the dirham’s peg of AED 3.6725 to the US dollar,{cite("peg")} the European Central Bank’s euro reference rates{cite("ecb")} and, for the rouble, the Bank of Russia’s official rate.{cite("cbr")} Each converted line is rounded the same way as the dirham figures, so a converted total can differ slightly from the dirham total divided by the rate. The page never fetches live rates; we update them monthly.</p>
</div></div></section>

<section class="section--tight"><div class="wrap split"><div><h2>Build rates by specification</h2><p class="muted">Construction only, 2025–26. The right-hand columns apply each rate to a 6,000 sq ft villa with no extras.</p></div><div class="prose">
{tier_table()}
<p class="small muted">Sources: Engel &amp; Völkers, Optimal Engineering, Knight Frank via Gulf Construction, Turner &amp; Townsend. Knight Frank's Q2 2025 figures were about AED 4,200 per m² (around AED 390 per sq ft) for standard and AED 11,000 per m² (around AED 1,020 per sq ft) for high-end construction.{cite("kf")} Turner &amp; Townsend's Q1 2024 UAE figures for an individual detached villa were AED 4,950–6,050 per m² (around AED 460–560 per sq ft) at a medium standard and AED 10,800–13,200 per m² (around AED 1,000–1,230 per sq ft) at a prestige standard.{cite("tt")}</p>
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
<li>VAT. The UAE's general VAT rate is 5%.{cite("vat")} Published rates do not consistently state whether it is included, so allow for 5% VAT on contractor invoices if your quotes exclude it.</li>
<li>Finance costs, insurance and your own advisers' fees, including ours.</li>
<li>Cost inflation. For 2026, Turner &amp; Townsend forecast construction inflation of 4% in Dubai and 5% in Abu Dhabi,{cite("tt25")} and Currie &amp; Brown about 3% for the UAE;{cite("pra")} the calculator does not apply it.</li>
<li>A location premium. We have found no published source that supports one, so the area you choose changes the approvals route shown, not the rate.</li>
</ul>
</div></div></section>

<section class="section--tight" id="sources"><div class="wrap split"><div><h2>Sources and assumptions</h2></div><div class="prose">
<ol class="calc-sources">{srcs}</ol>
<h3>Assumptions</h3>
<ul>
<li>The likely figure for each rate is the midpoint of the published range; for contingency we use 12%, just below the 12.5% midpoint.</li>
<li>Premium spans Engel &amp; Völkers' mid-range floor of AED 500 to Optimal Engineering's premium ceiling of AED 850 per sq ft. Luxury uses Optimal Engineering's AED 850–1,200 per sq ft. Ultra-luxury has no published ceiling: the calculator uses AED 1,200 (Optimal Engineering's floor) to 1,400 (the top of Engel &amp; Völkers' luxury range) per sq ft and marks the high figure with a plus sign.</li>
<li>Approvals use the fixed AED 25,000–75,000 band, our own choice for a straightforward villa. Published totals for all authority approvals run up to AED 250,000, so a large or free-zone villa needs more.</li>
<li>A basic renovation refresh (painting, flooring, small upgrades) carries no design fees or approvals allowance, because cosmetic work rarely needs drawings or an authority permit. Your master developer may still require an NOC.</li>
<li>Luxury renovations are published only as "above AED 1 million", so the calculator shows that starting figure with no likely or high figure; anything above it needs a project-specific assessment. The guide has no separate ultra-luxury band, so ultra-luxury renovation is treated as luxury.</li>
<li>Basements are priced as extra built-up area at the chosen rate. No published Dubai figure separates them.</li>
<li>Timelines: design 3–4 months, approvals 2–3 months, construction 8–14 months, snagging 1–2 months; 24–36 months plot to keys for custom luxury. These phase figures come from a property information website, the only published phase-by-phase breakdown we have found.{cite("reca")} Engel &amp; Völkers puts most villas at 12–24 months from approval to completion,{cite("ev")} and Optimal Engineering allows 4–8 weeks for approvals on a straightforward project and typically 12–18 months for construction.{cite("opt")} Renovation works two to six months or longer, with approvals taking a few weeks.{cite("sr")}</li>
<li>Each cost line is rounded to the nearest AED 1,000, or AED 10,000 above AED 1 million. Construction and the totals are the sums of the rounded lines, so the figures shown add up.</li>
<li>Renovation bands are whole-villa scope examples from a published guide. No published source gives a reliable way to scale them with floor area, so the calculator does not use the area for them; a large or older villa needs a project-specific assessment.</li>
<li>Currency rates as at {fx_date_text()}, in AED per unit: {fx_list(("GBP", "USD", "EUR"))}; on the Russian, Chinese and Hindi pages also {fx_list(("RUB", "CNY", "INR"))}. US dollar from the fixed peg;{cite("peg")} pound, euro, yuan and rupee crossed from the European Central Bank’s euro reference rates;{cite("ecb")} rouble from the Bank of Russia’s official rate.{cite("cbr")} Converted figures are approximate and for display only.</li>
</ul>
<p class="small muted">Rates last reviewed {month_year(RATES_REVIEWED)} by {esc(C.FOUNDER["name"])}; currency rates as at {fx_date_text()}. This page gives general information, not financial, legal or engineering advice.</p>
</div></div></section>

<section class="section--tight paper"><div class="wrap split"><div><h2>Questions</h2></div><div>{B.faq_html(FAQS)}</div></div></section>

{embed_box_html()}

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
    import pages_owner_tools as OT
    crumbs = [("Home", "/"), ("Tools", "/tools/")]
    body = B.page_head(crumbs, "Tools for villa owners",
                       "Free planning tools for owners building or renovating a villa in Dubai or Abu Dhabi. Each one shows its sources.") + f'''
<section class="section--tight"><div class="wrap split"><div><h2>Available tools</h2></div><div class="prose">
<h3><a href="{CALC_PATH}">Villa build and renovation cost calculator</a></h3>
<p>Low, likely and high costs for a new build or renovation, with design fees, approvals, contingency, furniture and an indicative timeline. Built from published 2025–26 market ranges, each one cited.</p>
<p><a class="btn" href="{CALC_PATH}">Open the calculator</a></p>
{OT.hub_html()}<h3>Free printable checklists</h3>
<ul><li><a href="/guides/villa-owner-checklist/">The Villa Owner’s Pre-Construction Checklist</a>: the questions to answer at each stage, from the plot to the end of the defects period.</li>
<li><a href="/guides/villa-snagging-checklist/">The Villa Snagging Checklist</a>: systems and rooms with a severity column, the handover documents to collect and the defects liability periods.</li></ul>
<h3>Further reading</h3>
<ul><li><a href="/insights/villa-construction-cost-dubai/">What it costs to build a villa in Dubai</a></li>
<li><a href="{OT.RR_ARTICLE}">Renovate or rebuild a villa in Dubai?</a></li>
<li><a href="{OT.STALLED}">What to do when a villa build stalls</a></li>
<li><a href="/insights/buying-a-villa-plot-in-dubai-checks/">Checks before buying a villa plot</a></li>
<li><a href="/fees/">How our fees work</a></li></ul>
</div></div></section>
{B.cta_band("Have a plot or a villa in mind?")}'''
    schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "url": B.url("/tools/"), "name": "Tools for villa owners",
               "hasPart": [{"@id": B.url(p) + "#app"} for p in [CALC_PATH] + [h[0] for h in OT.HUB]]}]
    B.page("/tools/", "Villa Planning Tools: Dubai & Abu Dhabi | Eastbridge",
           "Free, sourced tools for villa owners in Dubai and Abu Dhabi: build cost calculator, renovate or rebuild, stage payment planner and delay cost estimator.",
           body, crumbs, schema)

def estimate_thanks():
    """Thank-you page for the "estimate" form (noindex, like the other thank-you pages)."""
    first = esc(C.FOUNDER["name"].split()[0])
    crumbs = [("Home", "/"), ("Tools", "/tools/"), ("Villa build cost calculator", CALC_PATH), ("Thank you", THANKS_PATH)]
    steps = [
        (f"{first} reads your estimate", f"He looks at your inputs, the line-by-line result and any notes on the plot. {esc(C.RESPONSE_PROMISE)}, by email or by phone if you gave a number. Our hours are {esc(C.HOURS)}."),
        ("A plain view of the numbers", "Whether the figures look realistic for the plot and specification, which lines carry the most risk, and what would firm them up."),
        ("A free 30-minute call, if it helps", "At a time that suits you, including UK and European hours. If a closer look is worthwhile, such as a plot review, we set out the scope and a fixed fee in writing before we start."),
    ]
    body = f'''<section class="page-head"><div class="wrap">{B.crumbs_html(crumbs)}<h1>Thank you. Your estimate is with {first}.</h1>
<p class="lede">{esc(C.RESPONSE_PROMISE)}. We never pass your details to contractors or suppliers.</p></div></section>
<section class="section--tight thanks"><div class="wrap">
{B.steps_html(steps)}
<div class="split thanks-more"><div><h2 class="h-sm">If it is urgent</h2><p class="contact-actions"><a class="btn" href="{B.wa_link("Hello, I have just sent you an estimate from your villa cost calculator.")}" rel="noopener">Message us on WhatsApp</a><a class="btn btn--ghost" href="tel:{C.PHONE_E164}">Call {C.PHONE_DISPLAY}</a></p></div>
<div><h2 class="h-sm">While you wait</h2><ul class="read-list">
<li><a href="{CALC_PATH}"><b>Back to the calculator</b><span>Your browser’s back button returns you to your estimate.</span></a></li>
<li><a href="/insights/villa-construction-cost-dubai/"><b>What it costs to build a villa in Dubai</b><span>Published build costs, tier by tier.</span></a></li>
<li><a href="/services/plot-due-diligence/"><b>Plot due diligence</b><span>What we check before you commit to a plot or a design.</span></a></li>
</ul></div></div>
</div></section>'''
    B.page(THANKS_PATH, "Estimate sent | Eastbridge", "Your estimate from the villa build cost calculator has been sent to Philip at Eastbridge.", body, crumbs, noindex=True)

def build_tools():
    import pages_owner_tools as OT      # imported here: it builds on this module's rates and sources
    OT.build_owner_tools()
    tools_hub()
    calculator()
    estimate_thanks()
    embed_page()
