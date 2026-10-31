"""Worked project example: how we would manage a waterfront villa on Island E, Dubai Islands.

HYPOTHETICAL. This is not a completed Eastbridge appointment, not a real client and not a promise of savings.
Three kinds of information are kept apart:
  1. Published: Nakheel's Island E plot figures (price and payment plan sheet and DRAFT development controls,
     24 September 2026), the Dubai Land Department registration fee, UAE VAT rules and published cost ranges.
  2. Planning assumptions: the house size, the cost allowances, the price base, the programme and site access.
  3. Invented events: the family, the bids, the claims and every "modelled" outcome.
All arithmetic is computed here so every table, chart and headline on the site agrees."""
import math
from decimal import Decimal, ROUND_HALF_UP


def r(x, dp=2):
    """Round half up (avoids binary-float surprises such as round(0.555, 2) == 0.55)."""
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------- published plot figures (AED millions unless stated)
PLOT_SQFT = 8050
PLOT_PRICE = 17.61                      # example plot at about Nakheel's average waterfront rate of AED 2,188 per sq ft
FAR = 0.97                              # draft development controls
PLOT_PLAN = [("Oct 2026", .20), ("Mar 2027", .15), ("Sep 2027", .13), ("Mar 2028", .13),
             ("Sep 2028", .13), ("Mar 2029", .13), ("Sep 2029", .13)]

# ---------------------------------------------------------------- published transaction and tax rules
# Dubai Land Department, "Request to register the initial sale" (developer sale of a plot on the provisional
# register): seller 2% of sale value, purchaser 2% of sale value, plus AED 10 knowledge and AED 10 innovation fees.
DLD_URL = "https://dubailand.gov.ae/en/eservices/request-to-register-the-initial-sale/"
DLD_PURCHASER_RATE = 0.02
DLD_FIXED_AED = 20
DLD_FEE = PLOT_PRICE * DLD_PURCHASER_RATE + DLD_FIXED_AED / 1e6          # 0.35222
# Federal Tax Authority, Real Estate VAT guide (VATGRE1): bare land is exempt; the zero rate applies to the first
# sale or lease of a new residential building, not to construction services bought by an owner building a home.
# The FTA's VAT refund for building new residences is open to UAE nationals only.
VAT_RATE = 0.05
VAT_GUIDE_URL = "https://tax.gov.ae/DownloadOpenTextFile?fileUrl=en%2FVAT_VAT_Guides%2FReal_Estate_Guide%2FReal_Estate_Guide_VATGRE1_EN_19_04_2021_EN.pdf"

# ---------------------------------------------------------------- planning assumptions
PRICE_BASE = "October 2026"
GFA = 7800                              # above ground, within FAR (0.97 x 8,050 = 7,808)
BASEMENT = 3200
CONSTRUCTION_MONTHS = 19                # programme months 16 to 34
CONSTRUCTION_START, CONSTRUCTION_END = "January 2028", "July 2029"

# Development allowances, AED m excluding VAT: key, line, amount, VAT applied at 5%?
ALLOWANCES = [
 ("house", "Construction of the house above ground: structure, envelope, services and fit-out", 9.00, True),
 ("basement", "Basement: excavation, dewatering, waterproofing, structure and fit-out", 3.00, True),
 ("external", "Pool, landscaping and external works", 1.00, True),
 ("design", "Design and consultant fees: architect, engineers, interior designer and registered consultant", 1.04, True),
 ("approvals", "Approvals and connections: Nakheel, authority and utility fees", 0.30, False),
 ("contingency", "Contingency, held by the owners (10% of construction)", 1.30, True),
]
A = {k: v for k, _, v, _ in ALLOWANCES}
CONSTRUCTION = r(A["house"] + A["basement"] + A["external"])                # 13.00, the pre-tender estimate
APPROVED = r(sum(v for _, _, v, _ in ALLOWANCES))                            # 15.64 development allowances, ex VAT
VATABLE = r(sum(v for _, _, v, vat in ALLOWANCES if vat))                    # 15.34
VAT = VATABLE * VAT_RATE                                                      # 0.767
STATED_SUBTOTAL = PLOT_PRICE + DLD_FEE + APPROVED + VAT                       # 34.37
HOUSE_RATE = A["house"] * 1e6 / GFA                                           # AED per sq ft
BASEMENT_RATE = A["basement"] * 1e6 / BASEMENT

AWAITING = [  # cost, status: never treated as zero
 ("Eastbridge's fee", "Quoted separately for each appointment. Not included in any figure on this page."),
 ("Seller's 2% share of the registration fee", "The Dubai Land Department sets 2% for the seller as well as 2% for the purchaser. Whether any of it is passed to the buyer depends on the sale and purchase agreement. To be confirmed."),
 ("Developer and registration administration charges", "Nakheel's own charges, registration trustee fees and the title deed on final payment. To be confirmed with Nakheel and the Dubai Land Department."),
 ("VAT on approvals and connection charges", "The line mixes government fees and other charges. Treatment to be confirmed line by line, so no VAT is added to it here."),
 ("Escalation", f"Not included. Allowances are at {PRICE_BASE} prices; construction is assumed from {CONSTRUCTION_START} to {CONSTRUCTION_END}. No escalation rate is assumed."),
 ("Furniture, loose fittings and art", "Excluded. The owners' separate budget."),
 ("Other owner's costs", "Finance costs, the owners' own legal and tax advice, insurances not carried by the contractor, community service charges and moving costs. Excluded."),
]

# ---------------------------------------------------------------- invented events and modelled outcomes
CONCEPT_EST = 17.94                     # modelled concept cost plan, ex VAT
VALUE_REVIEW = [
 ("Structure", "Simplify the structural grid so the cantilevered terrace no longer needs deep transfer beams. Same overhang, less steel and concrete.", 0.65),
 ("Glazing", "Keep the full-height sliding glass on the water elevation; standard high-performance frames elsewhere. The view from every main room is unchanged.", 0.90),
 ("Stone", "Imported stone where it is touched and seen: entrance, living floors and the pool surround. Porcelain in plant, staff and service areas.", 0.50),
 ("Cooling and services", "A heat-load calculation after the glazing change lets the cooling plant drop a size. Smaller plant room, lower running costs.", 0.25),
]
VALUE_TOTAL = r(sum(v for *_, v in VALUE_REVIEW))                            # 2.30
assert r(CONCEPT_EST - VALUE_TOTAL) == APPROVED

BIDS = [  # contractor, headline, normalised, note (main contract and external works, AED m ex VAT)
 ("Contractor A", 11.85, 13.90, "Lowest headline price. Pool and landscaping excluded (AED 1.0m); provisional sums of AED 1.6m against AED 0.6m in other bids; a 14-month programme that looks unachievable."),
 ("Contractor B", 12.95, 13.05, "Complete scope, realistic 18-month programme, named site manager and MEP lead. Small allowance added for a missing pool plant item."),
 ("Contractor C", 13.40, 13.40, "Complete and well presented. Simply the most expensive."),
 ("Contractor D", 12.60, 13.35, "Preliminaries priced for 12 months of site staff on an 18-month job; the shortfall would be likely to return as claims."),
]
CONTRACT_SUM = 12.88       # modelled lump sum after clarification, against the pre-tender estimate of 13.00
OWNER_UPGRADES = 0.41      # kitchen and home automation upgrades, priced before instruction
DEWATERING_CLAIM = 0.64
DEWATERING = 0.085         # agreed value of the genuine change
OTHER_VARS = 0.275         # design development and agreed site variations
EOT_WEEKS_CLAIMED, EOT_WEEKS = 11, 4
EOT_COST = 0.10            # time-related cost of the four weeks agreed
EOT_WEEKLY = EOT_COST / EOT_WEEKS
CHANGES = OWNER_UPGRADES + DEWATERING + OTHER_VARS + EOT_COST                 # 0.87
CONSTRUCTION_OUT = CONTRACT_SUM + CHANGES                                     # 13.75
CONT_USED = CONSTRUCTION_OUT - CONSTRUCTION                                   # 0.75 drawn from contingency
CONT_LEFT = A["contingency"] - CONT_USED                                      # 0.55 not drawn
OUTTURN = CONSTRUCTION_OUT + A["design"] + A["approvals"]                     # 15.09 ex VAT
OUTTURN_VAT = (OUTTURN - A["approvals"]) * VAT_RATE
OUTTURN_ALL = PLOT_PRICE + DLD_FEE + OUTTURN + OUTTURN_VAT
# Month 27 sample report: everything committed except the extension of time agreed in month 29
REPORT_FORECAST = OUTTURN - EOT_COST
assert abs((APPROVED - OUTTURN) - CONT_LEFT) < 1e-9   # the "underspend" is exactly the undrawn contingency

# Modelled cost avoidance: each line compares one decision with one hypothetical alternative. Different
# baselines, so the lines are never totalled, never added to the undrawn contingency and never set against a fee.
AVOIDED = [
 ("Design brought back to the budget before tender", "against the modelled concept cost plan", VALUE_TOTAL),
 ("Contractor B chosen rather than the lowest headline bid", "normalised difference between Contractors A and B", r(BIDS[0][2] - BIDS[1][2])),
 ("Dewatering claim reduced to the genuine change", f"AED {DEWATERING_CLAIM:.2f}m claimed, AED {DEWATERING:.3f}m agreed", r(DEWATERING_CLAIM - DEWATERING)),
 ("Extension of time held to four weeks, not eleven", "seven weeks of time-related cost at the agreed weekly rate", r((EOT_WEEKS_CLAIMED - EOT_WEEKS) * EOT_WEEKLY)),
]

EVENTS_UNSORTED = [
 ("Month 18", "Dewatering", "Suppose the contractor claims AED 640,000 for extra dewatering in the basement excavation.",
  "The ground investigation would have been issued with the tender and the contract would put ground risk with the contractor. Only the extra 1.2 m of basement depth the owners added in month 17, for a wine store, would be a genuine change.",
  "Modelled outcome: agreed at AED 85,000."),
 ("Month 20", "Owners' upgrades", "Suppose the owners ask for a larger kitchen and a better home automation system.",
  "Both would be priced by the contractor and checked before anything is instructed, with the time effect stated. The owners decide with the number in front of them.",
  "Modelled outcome: AED 410,000 approved from contingency, no delay."),
 ("Month 24", "Valuation 9", "Suppose the monthly payment application claims AED 1.42m.",
  "We would measure it on site against the programme. In this example, façade cladding claimed as complete is 60% fixed, and loose materials are not yet protected on site.",
  "Modelled outcome: AED 1.11m recommended, with the balance paid the following month once the work is done."),
 ("Month 29", "Delay claim", "Suppose the contractor seeks an 11-week extension of time, citing late information and shamal winds.",
  "In this example the records show joinery information from the interior designer was five weeks late, causing four weeks of critical delay, and wind days were within the contract allowance.",
  "Modelled outcome: four weeks granted, with four weeks of time-related cost. The owners keep their right to delay damages beyond that."),
 ("Month 15", "Long-lead glazing", "Suppose the sliding glass for the water elevation has a 26-week lead time.",
  "We would recommend ordering it as an early package straight after contract award, with drawings checked before production.",
  "Modelled outcome: glazing arrives in time for the envelope, with no knock-on delay to fit-out."),
]

STAGES = [  # name, start month, end month (inclusive); month 1 = October 2026
 ("Plot review and EOI", 1, 1),
 ("Brief, budget, team", 1, 3),
 ("Concept and scheme design", 4, 8),
 ("Nakheel design review", 7, 9),
 ("Detailed design and permit", 9, 13),
 ("Tender and contract", 13, 15),
 ("Construction", 16, 34),
 ("Snagging and handover", 34, 35),
]
assert STAGES[6][2] - STAGES[6][1] + 1 == CONSTRUCTION_MONTHS

EVENTS = sorted(EVENTS_UNSORTED, key=lambda e: int(e[0].split()[1]))

# ---------------------------------------------------------------- planning cash flow of the stated allowances
YEARS = ("2026", "2027", "2028", "2029")
DESIGN_CASH = {"2026": .05, "2027": .70, "2028": .17, "2029": .12}           # sums to the design allowance
APPROVALS_CASH = {"2026": 0, "2027": .10, "2028": .10, "2029": .10}           # sums to the approvals allowance
assert r(sum(DESIGN_CASH.values())) == A["design"] and r(sum(APPROVALS_CASH.values())) == A["approvals"]

def _largest_remainder(values, total):
    """Round each value to 2 dp so the rounded values add up exactly to the rounded total."""
    cents = [v * 100 for v in values]
    base = [math.floor(c) for c in cents]
    short = int(round(r(total) * 100)) - sum(base)
    for i in sorted(range(len(cents)), key=lambda i: cents[i] - base[i], reverse=True)[:max(0, short)]:
        base[i] += 1
    return [b / 100 for b in base]

def _cash_by_year():
    """Per year: plot and registration, development (ex VAT), VAT. Construction and contingency follow a typical
    spend curve over the 19 construction months (January 2028 to July 2029)."""
    months = [(2028, m) for m in range(1, 13)] + [(2029, m) for m in range(1, 8)]
    n = len(months)
    w = [math.sin(math.pi * (i + .5) / n) ** 1.2 for i in range(n)]
    s = sum(w)
    build = dict.fromkeys(YEARS, 0.0)
    for (y, _), wi in zip(months, w):
        build[str(y)] += (CONSTRUCTION + A["contingency"]) * wi / s
    plot = dict.fromkeys(YEARS, 0.0)
    for d, p in PLOT_PLAN:
        plot[d[-4:]] += PLOT_PRICE * p
    plot["2026"] += DLD_FEE
    dev = {y: build[y] + DESIGN_CASH[y] + APPROVALS_CASH[y] for y in YEARS}
    vat = {y: (build[y] + DESIGN_CASH[y]) * VAT_RATE for y in YEARS}
    cols = [_largest_remainder([plot[y] for y in YEARS], PLOT_PRICE + DLD_FEE),
            _largest_remainder([dev[y] for y in YEARS], APPROVED),
            _largest_remainder([vat[y] for y in YEARS], VAT)]
    return [(y, cols[0][i], cols[1][i], cols[2][i]) for i, y in enumerate(YEARS)]

CASH = _cash_by_year()        # (year, plot and registration, development ex VAT, VAT)
CASH_TOTALS = tuple(r(sum(row[i] for row in CASH)) for i in (1, 2, 3))
assert r(sum(CASH_TOTALS)) == r(STATED_SUBTOTAL), (CASH_TOTALS, STATED_SUBTOTAL)

def m(x, dp=2):
    """AED millions formatter."""
    return f"AED {r(x, dp):.{dp}f}m"

# ---------------------------------------------------------------- SVG charts (inline, theme tokens via CSS vars)
C_PLOT, C_BUILD, C_ALT = "#2F6A8A", "#C0832F", "#4F8F7A"

def svg_cash():
    W, H, L, R, T, B = 720, 320, 56, 20, 30, 44
    peak = max(p + d + v for _, p, d, v in CASH)
    maxv = float(math.ceil(peak / 2) * 2)
    bw = 90
    xs = [L + 40 + i * ((W - L - R - 80) / 3) for i in range(4)]
    def y(v): return T + (H - T - B) * (1 - v / maxv)
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Planning cash flow of the stated allowances: plot and registration, and design, approvals, construction and contingency including VAT, 2026 to 2029" class="chart">']
    for t in range(0, int(maxv) + 1, 2):
        g.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="grid"/><text x="{L-10}" y="{y(t)+4:.1f}" class="tick" text-anchor="end">{t}</text>')
    # anchored to the left edge so a longer translated unit label cannot run out of the viewBox
    g.append(f'<text x="4" y="{T-12}" class="tick" text-anchor="start" direction="ltr">AED m</text>')
    for (yr, p, d, v), x in zip(CASH, xs):
        b = d + v
        y0 = y(0); yp = y(p); yb = y(p + b)
        g.append(f'<g><title>{yr}: plot and registration {m(p)}, development including VAT {m(b)}, total {m(p+b)}</title>'
                 f'<rect x="{x-bw/2:.1f}" y="{yp:.1f}" width="{bw}" height="{y0-yp:.1f}" fill="{C_PLOT}"/>')
        if b > 0:
            g.append(f'<rect x="{x-bw/2:.1f}" y="{yb:.1f}" width="{bw}" height="{max(0.0, yp-yb-2):.1f}" fill="{C_BUILD}"/>')
        g.append(f'<text x="{x:.1f}" y="{yb-8:.1f}" text-anchor="middle" class="val">{r(p+b):.2f}</text>')
        g.append(f'<text x="{x:.1f}" y="{H-B+20}" text-anchor="middle" class="tick">{yr}</text></g>')
    g.append("</svg>")
    return "".join(g)

def svg_bids():
    W, L, R, T = 720, 120, 70, 16
    rowh = 66
    H = T + rowh * 4 + 44          # tall enough for the tick numbers and the "modelled" axis label
    maxv = 14.5
    def x(v): return L + (W - L - R) * v / maxv
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Modelled contractor bids: headline price against normalised like-for-like cost" class="chart">']
    for t in range(0, 15, 2):
        g.append(f'<line y1="{T}" y2="{T+rowh*4}" x1="{x(t):.1f}" x2="{x(t):.1f}" class="grid"/><text y="{T+rowh*4+18}" x="{x(t):.1f}" class="tick" text-anchor="middle">{t}</text>')
    g.append(f'<text y="{T+rowh*4+36}" x="{W-R}" class="tick" text-anchor="end">AED m, modelled</text>')
    for i, (name, head, norm, _) in enumerate(BIDS):
        y0 = T + i * rowh + 10
        g.append(f'<g><title>{name}: headline {m(head)}, normalised {m(norm)} (modelled)</title>'
                 f'<text x="{L-12}" y="{y0+22}" text-anchor="end" class="lab">{name}</text>'
                 f'<rect x="{L}" y="{y0}" width="{x(head)-L:.1f}" height="16" fill="{C_ALT}"/>'
                 f'<text x="{x(head)+6:.1f}" y="{y0+12}" class="val">{head:.2f}</text>'
                 f'<rect x="{L}" y="{y0+20}" width="{x(norm)-L:.1f}" height="16" fill="{C_BUILD}"/>'
                 f'<text x="{x(norm)+6:.1f}" y="{y0+32}" class="val">{norm:.2f}</text></g>')
    g.append("</svg>")
    return "".join(g)

_MONTHS = {m: i for i, m in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), 1)}

def plot_month(label):
    """Programme month of a plot instalment date such as 'Sep 2029' (month 1 = October 2026)."""
    mon, yr = label.split()
    return (int(yr) - 2026) * 12 + _MONTHS[mon] - 10 + 1

assert [plot_month(d) for d, _ in PLOT_PLAN] == [1, 6, 12, 18, 24, 30, 36]

def svg_programme():
    W, L, R, T = 890, 320, 16, 34      # wide label gutter so translated stage names are not clipped
    rowh = 30
    H = T + rowh * len(STAGES) + 30
    pay_months = [plot_month(d) for d, _ in PLOT_PLAN]
    months = max(STAGES[-1][2], max(pay_months))     # 36: the axis runs to the last plot instalment
    def x(mo): return L + (W - L - R) * (mo - 1) / months
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Assumed programme: 35 months from plot review to handover" class="chart">']
    for mo in range(1, months + 2, 3):
        g.append(f'<line x1="{x(mo):.1f}" x2="{x(mo):.1f}" y1="{T-6}" y2="{H-30}" class="grid"/><text x="{x(mo):.1f}" y="{T-12}" class="tick" text-anchor="middle">{mo}</text>')
    g.append(f'<text x="{L-12}" y="{T-12}" class="tick" text-anchor="end">Month</text>')
    for i, (name, a, b) in enumerate(STAGES):
        yy = T + i * rowh + 6
        col = C_BUILD if name == "Construction" else C_PLOT
        g.append(f'<g><title>{name}: months {a} to {b}</title><text x="{L-12}" y="{yy+13}" text-anchor="end" class="lab">{name}</text>'
                 f'<rect x="{x(a):.1f}" y="{yy}" width="{max(6, x(b+1)-x(a)-2):.1f}" height="18" rx="2" fill="{col}"/></g>')
    # plot payment markers (Oct 2026 = month 1)
    for pm in pay_months:
        after = " (after the assumed handover)" if pm > STAGES[-1][2] else ""
        g.append(f'<circle cx="{x(pm):.1f}" cy="{H-18}" r="4" fill="{C_PLOT}"><title>Plot instalment, month {pm}{after}</title></circle>')
    g.append(f'<text x="{L-12}" y="{H-14}" class="tick" text-anchor="end">Plot instalments</text>')
    g.append("</svg>")
    return "".join(g)

def svg_site():
    """Illustrative plot and massing, plan and section. Not to scale; setbacks are indicative only."""
    return '''<svg viewBox="0 0 760 360" role="img" aria-label="Indicative plot plan and section for the worked example: waterfront plot of 8,050 sq ft, house of basement, ground and two upper floors within a 12.5 metre height limit under draft controls" class="chart site">
<g transform="translate(20,20)">
<text x="0" y="0" class="lab">Plan (indicative)</text>
<path d="M10 30 L330 18 L350 300 L0 300 Z" class="plot"/>
<path d="M0 300 C 90 318, 260 322, 350 300 L350 330 L0 330 Z" class="water"/>
<text x="175" y="322" text-anchor="middle" class="tick">Waterfront</text>
<text x="175" y="12" text-anchor="middle" class="tick">Access road</text>
<rect x="70" y="80" width="200" height="120" class="house"/>
<text x="170" y="138" text-anchor="middle" class="lab-inv">House</text>
<text x="170" y="154" text-anchor="middle" class="tick-inv">c. 3,000 sq ft footprint</text>
<rect x="120" y="215" width="130" height="38" class="pool"/>
<text x="185" y="238" text-anchor="middle" class="tick">Pool</text>
<text x="40" y="282" class="tick">Garden to the water</text>
<text x="0" y="350" class="tick">Plot 8,050 sq ft · FAR 0.97 (draft) · c. 7,800 sq ft above ground</text>
</g>
<g transform="translate(420,20)">
<text x="0" y="0" class="lab">Section (indicative)</text>
<line x1="0" x2="320" y1="230" y2="230" class="ground"/>
<line x1="0" x2="320" y1="52" y2="52" class="limit"/>
<text x="320" y="46" text-anchor="end" class="tick">12.5 m height limit</text>
<rect x="40" y="172" width="240" height="58" class="house"/><text x="160" y="206" text-anchor="middle" class="lab-inv">Ground</text>
<rect x="40" y="114" width="240" height="56" class="house"/><text x="160" y="147" text-anchor="middle" class="lab-inv">First</text>
<rect x="70" y="62" width="180" height="50" class="house"/><text x="160" y="92" text-anchor="middle" class="lab-inv">Second</text>
<rect x="40" y="232" width="240" height="56" class="base"/><text x="160" y="265" text-anchor="middle" class="lab">Basement</text>
<text x="0" y="310" class="tick">Basement, ground and two upper floors (draft controls)</text>
</g>
</svg>'''
