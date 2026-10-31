"""Illustrative case study: a waterfront villa on Island E, Dubai Islands.
The owners, events and outcome figures are a modelled scenario. Plot facts are Nakheel's published figures
(price and payment plan sheet and draft development controls, 24 September 2026). Cost ranges are from the
published sources listed at the end. All arithmetic is computed below so every figure on the page agrees."""
import math

# ---------------------------------------------------------------- inputs (AED millions unless stated)
PLOT_SQFT = 8050
PLOT_PRICE = 17.61                      # ≈ Nakheel's average waterfront rate of AED 2,188 per sq ft
FAR = 0.97
GFA = 7800                              # above-ground floor area within the FAR limit (0.97 × 8,050 = 7,808)
BASEMENT = 3200
PLOT_PLAN = [("Oct 2026", .20), ("Mar 2027", .15), ("Sep 2027", .13), ("Mar 2028", .13),
             ("Sep 2028", .13), ("Mar 2029", .13), ("Sep 2029", .13)]

BUDGET = [  # line, approved budget, modelled outturn
 ("Main contract: structure, envelope, MEP and fit-out", 12.00, None),
 ("External works, pool and landscaping", 1.00, None),
 ("Design team, interior design and consultant of record", 1.04, 1.04),
 ("Nakheel, authority and utility connection fees", 0.30, 0.30),
 ("Contingency, held by the owners", 1.30, None),
]
CONTRACT_SUM = 12.88       # agreed lump sum for main contract + externals (pre-tender estimate 13.00)
OWNER_UPGRADES = 0.41      # kitchen and home automation upgrades, priced before instruction
DEWATERING = 0.085         # agreed value of the genuine change (claimed 0.64)
OTHER_VARS = 0.275          # design development and agreed site variations
EOT_COST = 0.10            # four weeks of time-related cost on the agreed extension
CONSTRUCTION_OUT = round(CONTRACT_SUM + OWNER_UPGRADES + DEWATERING + OTHER_VARS + EOT_COST, 3)   # 13.805
APPROVED = round(sum(b for _, b, _ in BUDGET), 2)                                                   # 15.64
OUTTURN = round(CONSTRUCTION_OUT + 1.04 + 0.30, 3)                                                   # 15.145
UNDER = round(APPROVED - OUTTURN, 3)                                                                 # 0.495
CONT_USED = round(CONSTRUCTION_OUT - 13.00, 3)                                                       # 0.805

VALUE_REVIEW = [
 ("Structure", "Simplified the structural grid so the cantilevered terrace no longer needed deep transfer beams. Same overhang, less steel and concrete.", 0.65),
 ("Glazing", "Kept the full-height sliding glass on the water elevation; standard high-performance frames elsewhere. The view from every main room is unchanged.", 0.90),
 ("Stone", "Imported stone where it is touched and seen: entrance, living floors and the pool surround. Porcelain in plant, staff and service areas.", 0.50),
 ("Cooling and services", "Heat-load calculation after the glazing change let the cooling plant drop a size. Smaller plant room, lower running costs.", 0.25),
]
VALUE_TOTAL = round(sum(v for *_, v in VALUE_REVIEW), 2)   # 2.30
CONCEPT_EST = round(APPROVED + VALUE_TOTAL, 2)                # 17.94 -> shown as 17.9

BIDS = [  # contractor, headline, normalised, note
 ("Contractor A", 11.85, 13.90, "Lowest headline price. Pool and landscaping excluded (AED 1.0m); provisional sums of AED 1.6m against AED 0.6m in other bids; 14-month programme no one could achieve."),
 ("Contractor B", 12.95, 13.05, "Complete scope, realistic 18-month programme, named site manager and MEP lead. Small allowance added for a missing pool plant item."),
 ("Contractor C", 13.40, 13.40, "Complete and well-presented. Simply the most expensive."),
 ("Contractor D", 12.60, 13.35, "Preliminaries priced for 12 months of site staff on an 18-month job; the shortfall would have come back as claims."),
]
AVOIDED = [
 ("Design brought back to budget before tender", VALUE_TOTAL),
 ("Lowest headline bid avoided (normalised cost difference)", round(BIDS[0][2] - BIDS[1][2], 2)),
 ("Dewatering claim reduced to the genuine change", round(0.64 - DEWATERING, 3)),
 ("Extension of time held to four weeks, not eleven", 0.16),
]
AVOIDED_TOTAL = round(sum(round(v, 2) for _, v in AVOIDED), 2)   # 3.99, the sum of the figures as shown

EVENTS_UNSORTED = [
 ("Month 18", "Dewatering", "The contractor claims AED 640,000 for extra dewatering in the basement excavation.",
  "The ground investigation was issued with the tender and the contract put ground risk with the contractor. Only the extra 1.2 m of basement depth the owners added in month 17, for a wine store, is a genuine change.",
  "Agreed at AED 85,000."),
 ("Month 20", "Owners' upgrades", "The owners want a larger kitchen and a better home automation system.",
  "Both priced by the contractor and checked before anything is instructed, with the time effect stated. The owners decide with the number in front of them.",
  "AED 410,000 approved from contingency, no delay."),
 ("Month 24", "Valuation 9", "The monthly payment application claims AED 1.42m.",
  "Measured on site against the programme: façade cladding claimed as complete is 60% fixed, and loose materials are not yet protected on site.",
  "AED 1.11m recommended. The balance is paid the following month, once the work is done."),
 ("Month 29", "Delay claim", "The contractor seeks an 11-week extension of time, citing late information and shamal winds.",
  "Records show joinery information from the interior designer was five weeks late, causing four weeks of critical delay. Wind days were within the contract allowance.",
  "Four weeks granted, with four weeks of time-related cost. The owners keep their right to delay damages beyond that."),
 ("Month 15", "Long-lead glazing", "The sliding glass for the water elevation has a 26-week lead time.",
  "Ordered as an early package straight after contract award, with drawings checked before production.",
  "Glazing arrives in time for the envelope; no knock-on delay to fit-out."),
]

STAGES = [  # name, start month, end month (inclusive)
 ("Plot review and EOI", 1, 1),
 ("Brief, budget, team", 1, 3),
 ("Concept and scheme design", 4, 8),
 ("Nakheel design review", 7, 9),
 ("Detailed design and permit", 9, 13),
 ("Tender and contract", 13, 15),
 ("Construction", 16, 34),
 ("Snagging and handover", 34, 35),
]

EVENTS = sorted(EVENTS_UNSORTED, key=lambda e: int(e[0].split()[1]))

# ---------------------------------------------------------------- derived: cash by year
def _cash_by_year():
    plot = {"2026": 0, "2027": 0, "2028": 0, "2029": 0}
    for d, p in PLOT_PLAN:
        plot[d[-4:]] += PLOT_PRICE * p
    months = [(2028, m) for m in range(1, 13)] + [(2029, m) for m in range(1, 8)]
    n = len(months)
    w = [math.sin(math.pi * (i + .5) / n) ** 1.2 for i in range(n)]
    s = sum(w)
    build = {"2026": 0, "2027": 0, "2028": 0, "2029": 0}
    for (y, _), wi in zip(months, w):
        build[str(y)] += CONSTRUCTION_OUT * wi / s
    fees = {"2026": 0.05, "2027": 0.80, "2028": 0.29, "2029": 0.20}
    return [(y, round(plot[y], 2), round(build[y] + fees[y], 2)) for y in ("2026", "2027", "2028", "2029")]

CASH = _cash_by_year()

def m(x, dp=2):
    """AED millions formatter."""
    return f"AED {x:.{dp}f}m"

# ---------------------------------------------------------------- SVG charts (inline, theme tokens via CSS vars)
C_PLOT, C_BUILD, C_ALT = "#2F6A8A", "#C0832F", "#4F8F7A"

def svg_cash():
    W, H, L, R, T, B = 720, 320, 56, 20, 30, 44
    maxv = 16.0
    bw = 90
    xs = [L + 40 + i * ((W - L - R - 80) / 3) for i in range(4)]
    def y(v): return T + (H - T - B) * (1 - v / maxv)
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Annual outgoings: plot instalments and build costs, 2026 to 2029" class="chart">']
    for t in range(0, 17, 2):
        g.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="grid"/><text x="{L-10}" y="{y(t)+4:.1f}" class="tick" text-anchor="end">{t}</text>')
    g.append(f'<text x="{L-10}" y="{T-12}" class="tick" text-anchor="end">AED m</text>')
    for (yr, p, b), x in zip(CASH, xs):
        y0 = y(0); yp = y(p); yb = y(p + b)
        g.append(f'<g><title>{yr}: plot {m(p)}, build and fees {m(b)}, total {m(p+b)}</title>'
                 f'<rect x="{x-bw/2:.1f}" y="{yp:.1f}" width="{bw}" height="{y0-yp:.1f}" fill="{C_PLOT}"/>')
        if b > 0:
            g.append(f'<rect x="{x-bw/2:.1f}" y="{yb:.1f}" width="{bw}" height="{max(0.0, yp-yb-2):.1f}" fill="{C_BUILD}"/>')
        g.append(f'<text x="{x:.1f}" y="{yb-8:.1f}" text-anchor="middle" class="val">{p+b:.1f}</text>')
        g.append(f'<text x="{x:.1f}" y="{H-B+20}" text-anchor="middle" class="tick">{yr}</text></g>')
    g.append("</svg>")
    return "".join(g)

def svg_bids():
    W, H, L, R, T = 720, 300, 120, 70, 16
    rowh = 66
    maxv = 14.5
    def x(v): return L + (W - L - R) * v / maxv
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Contractor bids: headline price against normalised like-for-like cost" class="chart">']
    for t in range(0, 15, 2):
        g.append(f'<line y1="{T}" y2="{T+rowh*4}" x1="{x(t):.1f}" x2="{x(t):.1f}" class="grid"/><text y="{T+rowh*4+18}" x="{x(t):.1f}" class="tick" text-anchor="middle">{t}</text>')
    g.append(f'<text y="{T+rowh*4+36}" x="{W-R}" class="tick" text-anchor="end">AED m</text>')
    for i, (name, head, norm, _) in enumerate(BIDS):
        y0 = T + i * rowh + 10
        g.append(f'<g><title>{name}: headline {m(head)}, normalised {m(norm)}</title>'
                 f'<text x="{L-12}" y="{y0+22}" text-anchor="end" class="lab">{name}</text>'
                 f'<rect x="{L}" y="{y0}" width="{x(head)-L:.1f}" height="16" fill="{C_ALT}"/>'
                 f'<text x="{x(head)+6:.1f}" y="{y0+12}" class="val">{head:.2f}</text>'
                 f'<rect x="{L}" y="{y0+20}" width="{x(norm)-L:.1f}" height="16" fill="{C_BUILD}"/>'
                 f'<text x="{x(norm)+6:.1f}" y="{y0+32}" class="val">{norm:.2f}</text></g>')
    g.append("</svg>")
    return "".join(g)

def svg_programme():
    W, L, R, T = 760, 190, 16, 34
    rowh = 30
    H = T + rowh * len(STAGES) + 30
    months = 35
    def x(mo): return L + (W - L - R) * (mo - 1) / months
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Programme: 35 months from plot review to handover" class="chart">']
    for mo in range(1, months + 2, 3):
        g.append(f'<line x1="{x(mo):.1f}" x2="{x(mo):.1f}" y1="{T-6}" y2="{H-30}" class="grid"/><text x="{x(mo):.1f}" y="{T-12}" class="tick" text-anchor="middle">{mo}</text>')
    g.append(f'<text x="{L-12}" y="{T-12}" class="tick" text-anchor="end">Month</text>')
    for i, (name, a, b) in enumerate(STAGES):
        yy = T + i * rowh + 6
        col = C_BUILD if name == "Construction" else C_PLOT
        g.append(f'<g><title>{name}: months {a} to {b}</title><text x="{L-12}" y="{yy+13}" text-anchor="end" class="lab">{name}</text>'
                 f'<rect x="{x(a):.1f}" y="{yy}" width="{max(6, x(b+1)-x(a)-2):.1f}" height="18" rx="2" fill="{col}"/></g>')
    # plot payment markers
    pay_months = [1, 6, 12, 18, 24, 30, 36]
    for pm in pay_months:
        if pm <= months:
            g.append(f'<circle cx="{x(pm):.1f}" cy="{H-18}" r="4" fill="{C_PLOT}"><title>Plot instalment, month {pm}</title></circle>')
    g.append(f'<text x="{L-12}" y="{H-14}" class="tick" text-anchor="end">Plot instalments</text>')
    g.append("</svg>")
    return "".join(g)

def svg_site():
    """Illustrative plot and massing, plan and section. Not to scale; setbacks are indicative only."""
    return '''<svg viewBox="0 0 760 360" role="img" aria-label="Illustrative plot plan and section: waterfront plot of 8,050 sq ft, house of basement, ground and two upper floors within a 12.5 metre height limit" class="chart site">
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
<text x="0" y="350" class="tick">Plot 8,050 sq ft · FAR 0.97 · c. 7,800 sq ft above ground</text>
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
