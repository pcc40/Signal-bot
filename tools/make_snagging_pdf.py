#!/usr/bin/env python3
"""Build the second lead-magnet PDF: "The Villa Snagging Checklist (Dubai & Abu Dhabi)".

Usage:  python3 tools/make_snagging_pdf.py
Output: src/static/assets/guides/villa-snagging-checklist.pdf        (commit it; build.py copies it to dist/)
        src/static/assets/guides/villa-snagging-checklist-cover.webp  (landing-page cover, from page 1)

Same design system as tools/make_checklist_pdf.py: its palette, fonts, tick box, rules, note box and logo mark are
imported from that module, so the two guides stay identical in look. All copy follows src/content/WRITING_BRIEF.md
(British English, compliant role wording, no invented figures). Every legal period is cited to a primary text or to
UAE law-firm commentary; see LIABILITY and SOURCES below, and keep them in step with
src/content/insights/villa-snagging-checklist-dubai.md.
"""
import sys, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_checklist_pdf as K  # shared design system (palette, fonts, flowables, page furniture helpers)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Spacer, Table, TableStyle,
                                NextPageTemplate, PageBreak, KeepTogether, CondPageBreak)

Paragraph = K.Paragraph
C = K.C
ROOT = K.ROOT
OUT = ROOT / "src/static/assets/guides/villa-snagging-checklist.pdf"
COVER = OUT.with_name("villa-snagging-checklist-cover.webp")

TITLE = "The Villa Snagging Checklist"
SUBTITLE = "Dubai & Abu Dhabi"

# ---------------------------------------------------------------- content
# Each section: (number, title, intro, [(group heading, [check, ...]), ...], note)
SYSTEMS = [
    ("01", "Waterproofing and roofs",
     "Water damage is the most expensive defect to find late. Check every place water can get in before a single finish is accepted.",
     [("Roofs and terraces", [
         "Roof and terrace falls run to outlets; no standing water after washing down.",
         "Outlets and overflows clear, with guards fitted.",
         "Upstands and terminations at terrace door thresholds are continuous and sealed.",
         "Flood-test records for wet areas and roof terraces (or tests carried out before tiling) are provided.",
      ]),
      ("Below and around", [
         "No staining on ceilings under bathrooms, terraces, planters or the pool.",
         "Planters and green roofs drain freely and have root barriers.",
         "Basement walls and construction joints dry, with no tide marks or efflorescence.",
      ])],
     "Ask for the waterproofing warranty in your name, with its start date and the name of the specialist who installed it."),
    ("02", "Air conditioning and ventilation",
     "Run the system the way you will live with it: every unit on at once, on cooling, for several hours.",
     [("Performance", [
         "Every room reaches and holds its set temperature with all units running.",
         "Commissioning records provided: airflow, refrigerant pressures and chilled-water flow where relevant.",
         "No noise or vibration from outdoor units near bedrooms or neighbouring plots.",
      ]),
      ("Drainage and access", [
         "Condensate drains on every unit fall correctly and discharge where intended.",
         "Bathroom and kitchen extracts move air and terminate outside, not into a ceiling void.",
         "Access panels exist for every fan coil unit, damper and valve.",
      ])],
     "Blocked or badly falling condensate lines are a common cause of ceiling leaks months after handover."),
    ("03", "Electrical, lighting and low current",
     "Test everything that switches, and check that the paperwork matches what is on the wall.",
     [("Power and lighting", [
         "Every socket, switch and lighting circuit works; dimmers and scenes behave as specified.",
         "Earth leakage protection tested; the distribution board schedule matches the circuits.",
         "External lighting, timers and sensors work and are aimed correctly.",
      ]),
      ("Systems and access", [
         "Data points, Wi-Fi coverage, CCTV, intercom, gate and garage door controls tested.",
         "Home automation demonstrated scene by scene, with admin access and passwords handed over.",
         "Electrical test certificates provided.",
      ])],
     "Change every default code and password once you take possession."),
    ("04", "Plumbing, hot water and drainage",
     "Fill, run and flush everything. Slow drainage and gurgling are easier to fix before the furniture arrives.",
     [("Water supply", [
         "Every tap runs hot and cold; hot water reaches temperature in reasonable time at the furthest outlet.",
         "Pressure is acceptable on every floor; booster pump and water tank tested.",
         "No leaks under sinks and vanities, at the water heater or at visible joints.",
      ]),
      ("Drainage", [
         "Every bath and basin filled to overflow level and drained; every WC flushed repeatedly.",
         "Manholes and gullies lifted: clean, benched and free of construction debris.",
         "Pressure test records for the plumbing provided.",
      ])],
     None),
    ("05", "Pool and plant room",
     "Leave the filtration running for at least a day before you inspect, so the pool shows you how it really behaves.",
     [("The pool", [
         "Water clear and the level stable (a falling level suggests a leak).",
         "Tiles, copings and expansion joints sound, with no hollow or sharp edges.",
         "Lights, heater or chiller, cover and water features tested.",
      ]),
      ("The plant room", [
         "Valves and pipework labelled; access, ventilation and floor drainage adequate.",
         "Pool pressure test records and equipment warranties provided.",
      ])],
     None),
    ("06", "Facade, glazing and doors",
     "Open, close and lock every opening. Large sliding panels should run smoothly without force.",
     [("Glazing", [
         "Every window and sliding door opens, closes and locks; seals and gaskets continuous.",
         "No daylight around frames; no water at sills or corners after rain or a hose test.",
         "Glass free of scratches, chips and marks; motorised blinds and shading devices work.",
      ]),
      ("External envelope", [
         "Cladding, render and stone free of cracks, staining, open joints and colour variation.",
         "External doors and gates hang true, close fully and lock.",
      ])],
     None),
    ("07", "External works",
     "The garden should send water away from the house, not towards it.",
     [("Hard and soft landscaping", [
         "Paving falls away from the house and thresholds.",
         "Boundary walls, gates and movement joints sound.",
         "Irrigation zones run without leaks and with full coverage.",
         "Garden drainage does not run towards doors or the basement.",
      ])],
     None),
]

ROOMS = [
    ("Entrance, living and dining", [
        "Floors: no lippage between tiles, no hollow tiles (tap them), consistent grout, stone sealed.",
        "Walls and ceilings: no cracks, even plaster and paint under low-angle light, straight shadow gaps.",
        "Doors swing and close without binding; ironmongery fixed; door stops fitted.",
    ]),
    ("Kitchen", [
        "Appliances installed, connected and tested; manuals and warranties handed over.",
        "Worktop joints tight; sealant neat and continuous; extract ducted outside.",
        "Cabinet doors aligned; soft-close working; under-cabinet lighting working.",
    ]),
    ("Bathrooms and wet areas", [
        "Floor tiles fall to the drains; no ponding after a shower.",
        "Silicone joints continuous; shower screens sealed; no hollow tiles in wet areas.",
        "Mirrors, accessories and sanitaryware securely fixed; access to concealed cisterns and valves.",
    ]),
    ("Bedrooms and wardrobes", [
        "Joinery aligned; edge banding intact; internal finishes complete; fixings into walls secure.",
        "Air conditioning quiet at night setting; blackout blinds and curtains working.",
    ]),
    ("Staircases, balustrades and terraces", [
        "Balustrade fixings solid; glass secure; handrails continuous; finishes undamaged.",
        "Terrace finishes, thresholds and drainage as checked in section 01.",
    ]),
    ("Basement, garage and service rooms", [
        "No damp patches; sump pumps tested; ventilation working.",
        "Garage door safety stop works; service rooms labelled and accessible.",
    ]),
]

SEVERITY = [
    ("Critical", "Affects safety, structure or keeps water out of the house. For example: cracking in structural elements, "
                 "water coming through a roof or basement, an electrical safety fault, an insecure balustrade.",
     "Do not accept handover with it open. Ask for the cause to be investigated, the remedy agreed in writing and the "
     "work re-inspected before you sign."),
    ("Major", "A system that does not perform or a defect that will get worse. For example: AC not holding temperature, "
              "wrong falls to drains, hollow tiles in wet areas, failing glazing seals, a pool losing water.",
     "Fix before handover, or list it with a written completion date and keep enough money back to cover it."),
    ("Minor", "Cosmetic or finishing items. For example: paint coverage, scratches, silicone, alignment of doors and "
              "joinery, missing door stops.",
     "Number, photograph and list it; agree a close-out date; check it at the joint re-inspection."),
]

DOCS = [
    ("Building completion certificate", "The permitting authority (Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits), after the final inspection requested by your consultant and contractor"),
    ("Master developer completion letter or NOC", "The master developer, where the community requires one"),
    ("Title deed (villa bought from a developer)", "Dubai Land Department, after completion and handover"),
    ("Utility connections and accounts", "DEWA and the telecoms provider, once the completion certificate is issued"),
    ("As-built drawings: architecture, structure, MEP", "Your registered consultant and the contractor, as your contracts require"),
    ("Test and commissioning certificates", "The contractor and specialist subcontractors"),
    ("Warranties and guarantees, in your name", "Manufacturers and specialist subcontractors, through the main contractor"),
    ("Operation and maintenance manuals", "The contractor, compiled from each specialist"),
    ("Keys, cards, remotes and passwords schedule", "The contractor, signed by both sides"),
    ("Spare tiles, stone and paint from the same batch", "The contractor, as the contract or specification requires"),
]

# Rows: (what, period, runs from, who, citation). Keep in step with the insight article.
LIABILITY = [
    ("Collapse, or a defect that threatens the stability or safety of the building",
     "10 years, or longer if the contract says so", "Delivery (handover) of the work",
     "Contractor and the engineer who supervised the work, jointly. An engineer who only designed is liable for design defects only.",
     "UAE Civil Transactions Law 1985, arts 880 and 881; for contracts from 1 June 2026, arts 821 to 824 of Federal Decree-Law No. 25 of 2025"),
    ("Claim under that ten-year liability", "Must be brought within 3 years", "The collapse, or discovery of the defect",
     "The owner", "1985 law, art. 883"),
    ("Clauses excluding or limiting that liability", "Void", "–", "–", "1985 law, art. 882"),
    ("Structural parts of a unit bought from a developer (jointly owned property, Dubai)",
     "10 years", "The project's completion certificate", "The developer", "Dubai Law No. 6 of 2019, art. 40(a)"),
    ("Installations in that unit: mechanical, electrical, sanitary and sewerage",
     "1 year", "Handover of the unit (or the completion certificate, if the owner does not take possession)",
     "The developer", "Dubai Law No. 6 of 2019, art. 40(b)"),
    ("Other defects on a private build", "The defects liability period in your contract", "As the contract says",
     "The contractor", "Your construction contract"),
]

SOURCES = [
    ("Federal Law No. 5 of 1985, Civil Transactions Law, arts 880 to 883 (official Arabic text, published by Dubai Municipality)",
     "https://www.dm.gov.ae/documents/federal-law-no-5-of-1985-concerning-the-issuance-of-the-civil-transactions-law-of-the-united-arab-emirates/"),
    ("Dubai Law No. 6 of 2019 concerning Ownership of Jointly Owned Real Property, art. 40 (Dubai Legislation Portal)",
     "https://dlp.dubai.gov.ae/Legislation%20Reference/2019/Law%20No.%20%286%29%20of%202019%20Concerning%20Ownership%20of%20Jointly%20Owned%20Real%20Property%20in%20the%20Emirate%20of%20Dubai.html"),
    ("Kayrouz & Associates: decennial liability and the new UAE Civil Code (April 2026)",
     "https://www.kayrouzandassociates.com/insights/decennial-liability-uae-contractors-engineers-2026"),
    ("Charles Russell Speechlys: decennial liability under the new UAE Civil Code, arts 821 to 824 (2026)",
     "https://www.charlesrussellspeechlys.com/en/insights/expert-insights/construction-engineering-and-projects/2026/decennial-liability-and-subcontractors-under-the-new-uae-civil-code-articles-821-to-824/"),
    ("Bracewell: the UAE's new Civil Code explained (effective date and transition)",
     "https://www.bracewell.com/resources/the-uaes-new-civil-code-explained-practical-changes-for-businesses-and-investors/"),
    ("Dubai Municipality: procedure for building permit and building completion certificate, villas",
     "https://dmpmedia.dm.gov.ae/uploads/2020/06/Residential-Buildings_Building-Permits-Procedures.pdf"),
    ("Meraas: guide to the title deed and Oqood (title deed issued by Dubai Land Department)",
     "https://meraas.com/en/latest-post/journal/guide-title-deed-and-oqood"),
]

# ---------------------------------------------------------------- flowables
W, H = A4
M_L, M_R, M_T, M_B = K.M_L, K.M_R, K.M_T, K.M_B
SEV_W, REF_W, BOX_W = 25 * mm, 17 * mm, 7 * mm


def sev_style(st):
    return ParagraphStyle("sev", parent=st["item"], fontName=K.SANS, fontSize=7.2, leading=13.6,
                          textColor=K.INK_SOFT, alignment=1)


def head_row(st, width, first="Check"):
    lab = ParagraphStyle("lab", parent=st["kicker"], fontSize=6.6, spaceAfter=0, textColor=K.INK_SOFT)
    labc = ParagraphStyle("labc", parent=lab, alignment=1)
    return [Paragraph("", lab), Paragraph(first.upper(), lab), Paragraph("SEVERITY", labc), Paragraph("REF", labc)]


def snag_rows(items, st, width, header=False):
    """Tick box | check | severity to circle (C / Ma / Mi) | snag reference, written in."""
    sv = sev_style(st)
    rows = ([head_row(st, width)] if header else []) + \
           [[K.Box(), Paragraph(t, st["item"]), Paragraph("C &nbsp;·&nbsp; Ma &nbsp;·&nbsp; Mi", sv), ""] for t in items]
    t = Table(rows, colWidths=[BOX_W, width - BOX_W - SEV_W - REF_W, SEV_W, REF_W])
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (1, 0), (1, -1), 6),
        ("TOPPADDING", (0, 0), (0, -1), 7.2), ("TOPPADDING", (1, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, K.STONE_2),
        ("LINEBEFORE", (3, 0), (3, -1), 0.4, K.STONE_2),
    ]
    if header:
        style += [("TOPPADDING", (0, 0), (-1, 0), 2), ("BOTTOMPADDING", (0, 0), (-1, 0), 3),
                  ("LINEBELOW", (0, 0), (-1, 0), 0.8, K.BRASS_LIGHT)]
    t.setStyle(TableStyle(style))
    return t


def boxed_table(rows, widths, st, head=True, zebra=False):
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LINEBELOW", (0, 0), (-1, -1), 0.4, K.STONE_2),
             ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
             ("TOPPADDING", (0, 0), (-1, -1), 5.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6.5)]
    if head:
        style += [("BACKGROUND", (0, 0), (-1, 0), K.STONE), ("LINEBELOW", (0, 0), (-1, 0), 0.8, K.BRASS_LIGHT)]
    t.setStyle(TableStyle(style))
    return t

# ---------------------------------------------------------------- page furniture

def cover(c, doc):
    c.saveState()
    c.setFillColor(K.SLATE); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(K.SLATE_2); c.setLineWidth(0.6)
    for i in range(1, 9):
        c.line(W * i / 9, H * 0.36 - 30 * mm, W * i / 9, H * 0.36 - 60 * mm)
    c.setStrokeColor(K.BRASS_LIGHT); c.setLineWidth(0.8)
    c.line(M_L, H * 0.36, W - M_R, H * 0.36)
    K.logo_mark(c, M_L, H - M_T - 12 * mm, 12 * mm)
    K.draw_tracked(c, M_L + 16 * mm, H - M_T - 5 * mm, "EASTBRIDGE", K.SANS_M, 10, 3.2, white)
    K.draw_tracked(c, M_L + 16 * mm, H - M_T - 10 * mm, "STRATEGIC PARTNERS", K.SANS, 6.3, 2.2, K.MUTED_DARK)
    K.draw_tracked(c, M_L, H * 0.68, "A FREE GUIDE FOR VILLA OWNERS", K.SANS_B, 8, 2.2, K.BRASS_LIGHT)
    c.setFillColor(white); c.setFont(K.SERIF, 44)
    y = H * 0.68 - 22 * mm
    for line in ["The Villa", "Snagging Checklist"]:
        c.drawString(M_L, y, line); y -= 15.5 * mm
    c.setFont(K.SERIF_I, 22); c.setFillColor(K.BRASS_LIGHT); c.drawString(M_L, y + 1 * mm, SUBTITLE)
    c.setFillColor(K.MUTED_DARK); c.setFont(K.SANS, 10.5)
    ty = H * 0.36 - 14 * mm
    for line in ["Systems first, then room by room: what to test before you accept",
                 "a new or renovated villa, the documents to collect at handover,",
                 "and how long the builder and developer stay liable for defects."]:
        c.drawString(M_L, ty, line); ty -= 5.6 * mm
    c.setFillColor(white); c.setFont(K.SANS_M, 9)
    c.drawString(M_L, M_B + 8 * mm, f"Written by {C.FOUNDER['name']}, {C.FOUNDER['role']}")
    c.setFillColor(K.MUTED_DARK); c.setFont(K.SANS, 8.5)
    c.drawString(M_L, M_B + 3 * mm, f"{C.FOUNDED_TRACK_RECORD_YEARS} years running {C.FOUNDER['company_uk']}, now on the client’s side of the table.")
    c.drawRightString(W - M_R, M_B + 3 * mm, C.SITE_URL.replace("https://", ""))
    c.restoreState()


def body_page(c, doc):
    c.saveState()
    K.logo_mark(c, M_L, H - 15 * mm, 6 * mm, stroke=K.INK)
    K.draw_tracked(c, M_L + 8.5 * mm, H - 12.4 * mm, "EASTBRIDGE", K.SANS_M, 7, 2.2, K.INK)
    K.draw_tracked(c, W - M_R - 60 * mm, H - 12.4 * mm, "VILLA SNAGGING CHECKLIST", K.SANS, 6.5, 1.6, K.INK_SOFT)
    c.setStrokeColor(K.STONE_2); c.setLineWidth(0.6); c.line(M_L, H - 17.5 * mm, W - M_R, H - 17.5 * mm)
    c.line(M_L, 15 * mm, W - M_R, 15 * mm)
    c.setFont(K.SANS, 6.8); c.setFillColor(K.INK_SOFT)
    c.drawString(M_L, 10.5 * mm, "General information, not legal or engineering advice. Eastbridge represents the owner alongside the owner’s registered consultant.")
    c.setFont(K.SANS_M, 7.5); c.setFillColor(K.INK)
    c.drawRightString(W - M_R, 10.5 * mm, str(doc.page))
    c.restoreState()

# ---------------------------------------------------------------- document

def build():
    K.register_fonts()
    st = K.styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
                          title=f"{TITLE} ({SUBTITLE})", author=C.NAME,
                          subject="A room-by-room and systems snagging checklist for private villa owners in Dubai and Abu Dhabi",
                          creator=C.NAME, keywords="villa, snagging, handover, defects liability, Dubai, Abu Dhabi, checklist")
    fw = W - M_L - M_R
    frame = Frame(M_L, M_B, fw, H - M_T - M_B, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    back_frame = Frame(M_L, M_B + 22 * mm, fw, H * 0.82 - M_B - 22 * mm - 14 * mm, id="b",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover),
        PageTemplate(id="body", frames=[frame], onPage=body_page),
        PageTemplate(id="back", frames=[back_frame], onPage=K.back_page),
    ])
    b = st["item"]
    bold = ParagraphStyle("bold", parent=b, fontName=K.SANS_B)

    s = [NextPageTemplate("body"), PageBreak()]

    # --- how to use
    s += [Paragraph("BEFORE YOU START", st["kicker"]),
          Paragraph("How to use this checklist", st["h1"]),
          Paragraph("Snag the systems first and the finishes second. A scratched door is cheap to put right; a leaking "
                    "terrace or an air-conditioning system that cannot hold temperature in August is not.", st["intro"]),
          Paragraph("We spent 21 years on the builder's side of handovers. Our founder, Philip Chapman, ran P Chapman "
                    "Construction, a premium residential builder in the UK. The snag lists that were closed quickly were "
                    "specific, located, photographed and numbered, and arrived while money was still to be paid. The ones "
                    "that stalled were vague, long, late, or mixed with new requests.", st["body"]),
          Paragraph("Walk the house with this checklist. Tick each check that passes. Where one fails, circle a severity, "
                    "write a snag reference in the REF column, and record it in the snag log at the back with a "
                    "photograph and an exact location.", st["body"]),
          Spacer(1, 6)]
    sev_rows = [[Paragraph("<b>Severity</b>", b), Paragraph("<b>What it means</b>", b), Paragraph("<b>What to ask for</b>", b)]] + \
               [[Paragraph(f'<b>{n}</b><br/><font color="#8B6A33">{code}</font>', b),
                 Paragraph(m, b), Paragraph(a, b)] for (n, m, a), code in zip(SEVERITY, ("C", "Ma", "Mi"))]
    s += [KeepTogether([Paragraph("THE SEVERITY KEY", st["h3"]), K.Rule(color=K.BRASS_LIGHT, thick=0.8, space=2),
                        boxed_table(sev_rows, [24 * mm, (fw - 24 * mm) * 0.52, (fw - 24 * mm) * 0.48], st)])]
    s += [Spacer(1, 10), Paragraph("This is our working classification, not a legal category. Your contract decides what "
                                   "must be complete at handover.", st["small"])]
    snag_note = K.note_box("Writing a snag that gets fixed: “Paint poor in bedroom” gets a dab of paint. "
                           "“Bedroom 2, north wall: coverage patchy across the full wall; repaint the wall to match” "
                           "gets the wall repainted. Location, defect, remedy expected, photograph.", st, fw)
    contents = [[Paragraph(f'<font color="#8B6A33">{n}</font>', b), Paragraph(t, b)] for n, t, *_ in SYSTEMS] + \
               [[Paragraph('<font color="#8B6A33">08</font>', b), Paragraph("Room by room: finishes", b)],
                [Paragraph('<font color="#8B6A33">09</font>', b), Paragraph("Handover documents", b)],
                [Paragraph('<font color="#8B6A33">10</font>', b), Paragraph("Defects liability periods", b)],
                [Paragraph('<font color="#8B6A33">11</font>', b), Paragraph("Snag log", b)]]
    half = (len(contents) + 1) // 2
    pairs = [contents[k] + (contents[k + half] if k + half < len(contents) else ["", ""]) for k in range(half)]
    cw = (fw - 8 * mm) / 2
    ct = Table([[Paragraph("<b>Inside</b>", b), "", "", ""]] + pairs,
               colWidths=[9 * mm, cw - 1 * mm, 9 * mm, cw - 9 * mm])
    ct.setStyle(TableStyle([("SPAN", (0, 0), (-1, 0)), ("LINEBELOW", (0, 0), (-1, -1), 0.4, K.STONE_2),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    s += [Spacer(1, 6), ct]

    # --- systems: two sections per page where they fit
    s += [PageBreak(), Paragraph("PART ONE", st["kicker"]), Paragraph("Systems: test before you look", st["h1"]),
          Paragraph("Ask the contractor to have every system running before you arrive, and to have the commissioning "
                    "records on the table. Witness the tests rather than accepting a certificate alone.", st["intro"])]
    for i, (n, title, intro, groups, note) in enumerate(SYSTEMS):
        block = [Paragraph(f"SECTION {n}", st["kicker"]),
                 Paragraph(title, ParagraphStyle("h2", parent=st["h1"], fontSize=20, leading=24, spaceAfter=4)),
                 Paragraph(intro, st["small"])]
        first = True
        for head, items in groups:
            block += [Paragraph(head.upper(), st["h3"]), K.Rule(color=K.BRASS_LIGHT, thick=0.8, space=2),
                      snag_rows(items, st, fw, header=first)]
            first = False
        if note:
            block += [Spacer(1, 6), K.note_box(note, st, fw)]
        s += [CondPageBreak(95 * mm), Spacer(1, 10 if i else 0), KeepTogether(block)]

    # --- rooms
    s += [CondPageBreak(120 * mm), Spacer(1, 16), Paragraph("PART TWO · SECTION 08", st["kicker"]), Paragraph("Room by room: finishes", st["h1"]),
          Paragraph("Inspect in daylight, then again with a torch held low against walls and floors: raking light shows "
                    "uneven plaster, paint and tiling that overhead light hides. Repeat these checks in every room of the type.",
                    st["intro"])]
    for j, (head, items) in enumerate(ROOMS):
        s += [KeepTogether([Paragraph(head.upper(), st["h3"]), K.Rule(color=K.BRASS_LIGHT, thick=0.8, space=2),
                            snag_rows(items, st, fw, header=(j == 0))])]
    s += [Spacer(1, 12), K.note_box("Inspect and record before furniture and family move in. After that, it is hard to "
                                    "show who caused a scratch or a chip.", st, fw)]

    # --- documents
    s += [PageBreak(), Paragraph("PART THREE · SECTION 09", st["kicker"]), Paragraph("Handover documents", st["h1"]),
          Paragraph("Do not accept the keys without these, or at least a dated list of what is outstanding and when it "
                    "will arrive. The house will be maintained, insured and one day sold on the strength of this file.", st["intro"])]
    drows = [[Paragraph("", b), Paragraph("<b>Document</b>", b), Paragraph("<b>Who issues it</b>", b)]] + \
            [[K.Box(), Paragraph(d, bold), Paragraph(w, b)] for d, w in DOCS]
    dt = Table(drows, colWidths=[BOX_W, 62 * mm, fw - BOX_W - 62 * mm], repeatRows=1)
    dt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (1, 0), (1, -1), 8),
                            ("TOPPADDING", (0, 1), (0, -1), 7.2), ("TOPPADDING", (1, 0), (-1, -1), 5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                            ("LINEBELOW", (0, 0), (-1, -1), 0.4, K.STONE_2),
                            ("LINEBELOW", (0, 0), (-1, 0), 0.8, K.BRASS_LIGHT)]))
    s += [dt, Spacer(1, 12),
          K.note_box("Check whose name each warranty is in and when it starts. A warranty that began when the product "
                     "was installed may have months less to run than you expect.", st, fw),
          Spacer(1, 8),
          Paragraph("Completion certificate procedure: Dubai Municipality, villas. Title deed: Dubai Land Department, as "
                    "described by Meraas. See the sources on the last page.", st["small"])]

    # --- liability
    s += [PageBreak(), Paragraph("PART FOUR · SECTION 10", st["kicker"]),
          Paragraph("Defects liability: how long, from when, and who", st["h1"]),
          Paragraph("Two different clocks are often confused. The builder's ten-year liability under the Civil Code runs "
                    "from delivery of the work. A developer's ten-year liability for structural parts under Dubai's jointly "
                    "owned property law runs from the completion certificate.", st["intro"])]
    small_b = ParagraphStyle("sb", parent=b, fontSize=8.4, leading=11.6)
    small_bb = ParagraphStyle("sbb", parent=small_b, fontName=K.SANS_B)
    cite_st = ParagraphStyle("cite", parent=small_b, textColor=K.INK_SOFT, fontSize=7.6, leading=10.4)
    lrows = [[Paragraph("<b>Defect or matter</b>", small_b), Paragraph("<b>Period</b>", small_b),
              Paragraph("<b>Runs from</b>", small_b), Paragraph("<b>Who</b>", small_b), Paragraph("<b>Source</b>", small_b)]] + \
            [[Paragraph(a, small_bb), Paragraph(p, small_b), Paragraph(r, small_b), Paragraph(w, small_b), Paragraph(src, cite_st)]
             for a, p, r, w, src in LIABILITY]
    lw = [40 * mm, 24 * mm, 29 * mm, 33 * mm]
    s += [boxed_table(lrows, lw + [fw - sum(lw)], st)]
    s += [Spacer(1, 10),
          Paragraph("The new Civil Transactions Law (Federal Decree-Law No. 25 of 2025) came into force on 1 June 2026. "
                    "Law-firm commentary reports that it largely keeps the ten-year regime, now in articles 821 to 824, and "
                    "that contracts made before that date generally stay under the 1985 law. Dubai Law No. 6 of 2019 applies "
                    "to jointly owned property; whether it covers your villa depends on how the community is set up.", st["body"]),
          Spacer(1, 4),
          K.note_box("This is a summary, not legal advice. Notify defects in writing, as your contract requires, and take "
                     "advice from a UAE-qualified lawyer before relying on any period or withholding money.", st, fw)]

    # --- snag log
    s += [PageBreak(), Paragraph("SECTION 11", st["kicker"]), Paragraph("Snag log", st["h1"]),
          Paragraph("One list, one owner. Give each snag a number, a location and a photograph, and agree a close-out date "
                    "at the joint walk-round.", st["small"]), Spacer(1, 4), snag_note]
    hdr = ["No.", "Location", "Defect and remedy expected", "Sev.", "Photo", "Raised", "Closed"]
    log_w = [11 * mm, 27 * mm, fw - 11 * mm - 27 * mm - 12 * mm - 14 * mm - 16 * mm - 16 * mm, 12 * mm, 14 * mm, 16 * mm, 16 * mm]
    hst = ParagraphStyle("lh", parent=st["kicker"], fontSize=6.4, spaceAfter=0, textColor=K.INK_SOFT)
    log = [[Paragraph(h.upper(), hst) for h in hdr]] + [["" for _ in hdr] for _ in range(19)]
    lt = Table(log, colWidths=log_w, rowHeights=[7 * mm] + [8.6 * mm] * 19, repeatRows=1)
    lt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("BACKGROUND", (0, 0), (-1, 0), K.STONE),
                            ("LINEBELOW", (0, 0), (-1, 0), 0.8, K.BRASS_LIGHT),
                            ("LINEBELOW", (0, 1), (-1, -1), 0.4, K.STONE_2),
                            ("LINEBEFORE", (1, 0), (-1, -1), 0.4, K.STONE_2),
                            ("LEFTPADDING", (0, 0), (-1, -1), 4)]))
    s += [Spacer(1, 6), lt]

    # --- sources
    s += [PageBreak(), Paragraph("SOURCES", st["kicker"]), Paragraph("Where the periods come from", st["h1"]), Spacer(1, 4)]
    for title, link in SOURCES:
        s += [Paragraph(f'{title}. <link href="{link}" color="#8B6A33">{link}</link>', st["small"]), Spacer(1, 2)]
    s += [Spacer(1, 8), Paragraph(f"Published by {C.NAME}, {datetime.date.today().strftime('%B %Y')}. Laws, procedures and "
                                  "authority requirements change; check the current position with the relevant authority, "
                                  "your registered consultant and a UAE-qualified lawyer.", st["small"])]
    s += [Spacer(1, 22), Paragraph("YOUR NOTES", st["kicker"]),
          Paragraph("Items to raise at the joint walk-round, and who owns them.", st["small"])]
    s += [K.Rule(color=K.STONE_2, thick=0.6, space=11) for _ in range(10)]

    # --- back page
    w_ = ParagraphStyle("w", parent=st["body"], textColor=white)
    m_ = ParagraphStyle("m", parent=st["body"], textColor=K.MUTED_DARK, fontSize=9.5, leading=14)
    h_ = ParagraphStyle("hb", parent=st["h1"], textColor=white, fontSize=28, leading=33)
    k_ = ParagraphStyle("kb", parent=st["kicker"], textColor=K.BRASS_LIGHT)
    s += [NextPageTemplate("back"), PageBreak(),
          Paragraph("A SECOND PAIR OF EYES", k_),
          Paragraph("Handover is your last point of real leverage.", h_), Spacer(1, 6),
          Paragraph("Eastbridge Strategic Partners is an independent, client-side project manager for private villa builds "
                    "and renovations in Dubai and Abu Dhabi. At handover we represent the owner, alongside the owner's "
                    "registered consultant and the contractor: independent client-side inspections, a clear numbered snag "
                    "list tracked to close-out, a check of the handover documents against the contract, and commercial "
                    "advice on retention and the final payment. We are paid only by the owner we represent and take no "
                    "commissions from contractors or suppliers.", w_),
          Paragraph(f"If your villa is nearing completion, the first conversation is free and confidential. {C.RESPONSE_PROMISE}.", w_),
          Spacer(1, 14)]
    lab = ParagraphStyle("lab", parent=st["kicker"], textColor=K.BRASS_LIGHT, spaceAfter=0)
    val = ParagraphStyle("val", parent=st["body"], textColor=white, fontSize=11, leading=15, spaceAfter=0)
    site = C.SITE_URL.replace("https://", "")
    rows = [
        ("EMAIL", f'<link href="mailto:{C.EMAIL}">{C.EMAIL}</link>'),
        ("PHONE AND WHATSAPP", f'<link href="https://wa.me/{C.WHATSAPP}">{C.PHONE_DISPLAY}</link>'),
        ("WEBSITE", f'<link href="{C.SITE_URL}/services/snagging-and-handover/">{site}</link>'),
        ("OFFICE", f'{C.ADDRESS["street"]}, {C.ADDRESS["locality"]}, {C.ADDRESS["country_name"]}'),
        ("HOURS", C.HOURS),
    ]
    tt = Table([[Paragraph(a, lab), Paragraph(v, val)] for a, v in rows], colWidths=[44 * mm, fw - 44 * mm])
    tt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                            ("LINEBELOW", (0, 0), (-1, -1), 0.4, K.SLATE_2)]))
    s += [tt, Spacer(1, 16),
          Paragraph(f"{C.LEGAL}. {C.LICENCE}. Eastbridge acts as the client's project manager and representative. "
                    "It is not a contractor or an engineering consultancy and does not replace the registered consultant "
                    "required by the authorities. This guide is general information, not legal, financial or engineering "
                    "advice for your specific project.", m_)]
    doc.build(s)
    print(f"Wrote {OUT.relative_to(ROOT)}")
    make_cover_image()


def make_cover_image():
    """Render page 1 to a WebP for the landing page (needs pdftoppm from poppler-utils and Pillow)."""
    import shutil, subprocess, tempfile
    if not shutil.which("pdftoppm"):
        print("pdftoppm not found: cover image not refreshed"); return
    try:
        from PIL import Image
    except Exception:
        print("Pillow not installed: cover image not refreshed"); return
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "110", "-png", "-f", "1", "-l", "1", "-singlefile", str(OUT),
                        str(Path(tmp) / "cover")], check=True)
        im = Image.open(Path(tmp) / "cover.png").convert("RGB")
        im.thumbnail((900, 1300))
        im.save(COVER, "WEBP", quality=82, method=6)
        print(f"Wrote {COVER.relative_to(ROOT)} ({im.width}x{im.height})")


if __name__ == "__main__":
    build()
