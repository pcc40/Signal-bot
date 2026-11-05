#!/usr/bin/env python3
"""Build the lead-magnet PDF: "The Villa Owner's Pre-Construction Checklist (Dubai & Abu Dhabi)".

Usage:  python3 tools/make_checklist_pdf.py
Output: src/static/assets/guides/villa-owner-checklist.pdf   (commit the PDF; build.py copies it to dist/)

Uses the site's own fonts (Instrument Serif / Instrument Sans) when fontTools + brotli are installed,
converting the woff2 files to TTF in a temporary folder. Otherwise falls back to Times / Helvetica.
All copy follows src/content/WRITING_BRIEF.md: British English, no invented figures, compliant role wording.
"""
import sys, tempfile, datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Spacer, Table, TableStyle,
                                Flowable, NextPageTemplate, PageBreak, KeepTogether, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph as _Paragraph


def Paragraph(text, style):
    """Typographic apostrophes in every paragraph (markup attributes use double quotes)."""
    return _Paragraph(text.replace("'", "\u2019"), style)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import config as C

OUT = ROOT / "src/static/assets/guides/villa-owner-checklist.pdf"
FONTS = ROOT / "src/static/assets/fonts"

# ---------------------------------------------------------------- palette (from site.css :root)
INK = HexColor("#151C1F")
SLATE = HexColor("#1C2629")
SLATE_2 = HexColor("#26343A")
INK_SOFT = HexColor("#4A5357")
STONE = HexColor("#F2F0EB")
STONE_2 = HexColor("#E4E1D9")
BRASS = HexColor("#8B6A33")
BRASS_LIGHT = HexColor("#CFAE72")
MUTED_DARK = HexColor("#A9B1AF")

# ---------------------------------------------------------------- fonts
SERIF, SERIF_I, SANS, SANS_M, SANS_B = "Times-Roman", "Times-Italic", "Helvetica", "Helvetica", "Helvetica-Bold"

def register_fonts():
    global SERIF, SERIF_I, SANS, SANS_M, SANS_B
    try:
        from fontTools.ttLib import TTFont as FT
        import brotli  # noqa: F401  (needed by fontTools to read woff2)
    except Exception:
        print("fontTools/brotli not installed: using built-in Times and Helvetica")
        return
    tmp = Path(tempfile.mkdtemp(prefix="eb-fonts-"))
    want = {"EB-Serif": "iserif-400", "EB-Serif-Italic": "iserif-400i", "EB-Sans": "instrument-400",
            "EB-Sans-Medium": "instrument-500", "EB-Sans-Semibold": "instrument-600"}
    try:
        for name, f in want.items():
            t = FT(str(FONTS / f"{f}.woff2"))
            t.flavor = None
            dst = tmp / f"{f}.ttf"
            t.save(str(dst))
            pdfmetrics.registerFont(TTFont(name, str(dst)))
    except Exception as e:  # any conversion problem: stay on built-in fonts
        print(f"Could not register site fonts ({e}): using built-in fonts")
        return
    SERIF, SERIF_I, SANS, SANS_M, SANS_B = "EB-Serif", "EB-Serif-Italic", "EB-Sans", "EB-Sans-Medium", "EB-Sans-Semibold"
    from reportlab.lib.fonts import addMapping
    addMapping("EB-Sans", 0, 0, "EB-Sans")
    addMapping("EB-Sans", 1, 0, "EB-Sans-Semibold")
    addMapping("EB-Sans", 0, 1, "EB-Sans")
    addMapping("EB-Sans", 1, 1, "EB-Sans-Semibold")
    addMapping("EB-Serif", 0, 0, "EB-Serif")
    addMapping("EB-Serif", 0, 1, "EB-Serif-Italic")
    addMapping("EB-Serif", 1, 0, "EB-Serif")
    addMapping("EB-Serif", 1, 1, "EB-Serif-Italic")

# ---------------------------------------------------------------- content
TITLE = "The Villa Owner's Pre-Construction Checklist"
SUBTITLE = "Dubai & Abu Dhabi"

STAGES = [
    {
        "n": "01", "title": "Before you buy the plot",
        "intro": "The plot decides what you can build, what it will cost and how long it will take. Most of the "
                 "expensive surprises we saw as builders could have been spotted before the purchase was signed.",
        "groups": [
            ("Title and documents", [
                "Obtain the affection plan (or site plan) and confirm the plot number, boundaries, area and permitted use match the sale documents.",
                "Have a UAE-qualified lawyer review the title, the sale and purchase agreement and any master developer obligations before you pay a deposit.",
                "Ask whether the sale carries a build-by deadline: a date by which construction must start or finish, and what happens if it is missed.",
                "Confirm current and projected service charges, and any fees the master developer charges for NOCs, design review or construction access.",
            ]),
            ("What the rules let you build", [
                "Get the master developer's current design guidelines and read the setbacks, height limits, plot coverage, basement rules and material requirements.",
                "Confirm which authority will issue the building permit: Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits. In Abu Dhabi, permits are issued by the municipalities through TAMM.",
                "Check whether neighbouring plots are built, under construction or empty, and how their future buildings could affect views, privacy and site access.",
            ]),
            ("Ground, services and budget", [
                "Ask what is known about ground conditions, the water table and any dewatering or shoring a basement would need. Budget for a site investigation before design is fixed.",
                "Confirm where water, power, drainage and telecoms connections are, and whether infrastructure in the community is complete.",
                "Price the villa the plot actually allows, not an average per square foot. Test plot plus build plus fees against a realistic exit value.",
            ]),
        ],
        "note": "This is a practical checklist, not legal or valuation advice. Use a UAE-qualified lawyer for the transaction and an independent valuer for price.",
    },
    {
        "n": "02", "title": "Brief and budget",
        "intro": "A clear brief and an honest budget are the cheapest protection you will ever buy. Changes made on "
                 "paper cost a fraction of changes made on site.",
        "groups": [
            ("The brief", [
                "Write down how you will live in the house: who lives there, who visits, how you entertain, and what must be private.",
                "List rooms with target sizes, and separate the must-haves from the nice-to-haves before the first design meeting.",
                "Decide the finish level you expect room by room, with reference images, so every designer and bidder prices the same house.",
                "Agree who makes decisions on your side, how quickly, and who can approve changes while you are away.",
            ]),
            ("The whole-project budget", [
                "Build the budget from every cost, not just construction: design and engineering fees, authority and NOC fees, utility connections, pool, landscaping, furniture, fixtures and equipment, and your own advisers.",
                "Hold a separate contingency. Published guidance for Dubai villas suggests 10–15% (Real Estate Club Dubai); we would not start a custom build with less.",
                "Allow for cost movement over the programme. Plot to keys for a villa is commonly quoted at 12–24 months, and longer for custom luxury homes (Real Estate Club Dubai).",
                "Set a cost check at the end of each design stage, and agree in advance what will be cut if the design comes in over budget.",
            ]),
        ],
        "note": "Published ranges are a starting point, not a quotation. Price the specific villa your plot and brief produce.",
    },
    {
        "n": "03", "title": "Choosing your consultant and contractor",
        "intro": "In Dubai, the design, authority submissions and statutory supervision are carried out by a registered "
                 "consultancy you appoint. Your choice of consultant and contractor shapes the whole project.",
        "groups": [
            ("The consultant", [
                "Confirm the consultancy is registered with Dubai Municipality (or the relevant Abu Dhabi authority) for the work you need. The Dubai BPS app includes a consultant and contractor registry.",
                "Ask to see completed villas of a similar size and specification, and speak to the owners where possible.",
                "Compare fee proposals like-for-like: list what is included at each stage (design, engineering disciplines, authority submissions, site supervision, interiors, landscape) and what is extra.",
                "Ask how they control cost during design. Dubai Municipality has warned villa consultancies about over-designing structures and inflating build costs (Gulf News, August 2025).",
                "Confirm who will actually work on your project, how often they will be on site during construction, and how they report to you.",
            ]),
            ("The contractor", [
                "Check the contractor's registration and classification for the value and type of work, and look at villas they have completed and are building now.",
                "Ask about their current workload, who the site manager will be, and which trades they employ directly or subcontract.",
                "Invite bids on the same drawings, specification and contract terms, with a clear deadline and a single point of contact for questions.",
                "Compare bids like-for-like: exclusions, provisional sums, preliminaries, programme and payment terms, not just the total.",
                "Be wary of a price far below the others. Ask what it leaves out before you assume it is a saving.",
            ]),
        ],
        "note": "You appoint the consultant and the contractor. An independent client-side project manager can help you compare and choose; the decision stays with you.",
    },
    {
        "n": "04", "title": "Contract terms to look for",
        "intro": "The contract is where risk is allocated. Most disputes we saw in two decades of building came from "
                 "something the contract left vague. Dubai Municipality publishes standard contract forms for private "
                 "villa consultancy and construction contracts, which is a sensible place to start.",
        "groups": [
            ("Price and payment", [
                "Is the price fixed for the scope shown, or subject to remeasurement? Know which items can move and why.",
                "Are provisional sums and prime cost items listed with realistic values, and is it clear how they will be adjusted?",
                "Are interim payments tied to work actually completed and verified, rather than to dates or round percentages?",
                "Is an advance payment secured by a guarantee, and is there a performance guarantee for the construction period?",
                "How much retention is held, and what exactly triggers its release?",
            ]),
            ("Time, change and quality", [
                "Is there an agreed programme with a completion date, and delay damages that reflect your real loss?",
                "Does the contract set out how extensions of time are claimed, with notice periods and supporting records?",
                "Must every variation be priced and agreed in writing before the work is done? Who can instruct one on your behalf?",
                "Are materials, samples and mock-ups subject to approval before ordering?",
                "How long is the defects liability period, and how quickly must defects be put right?",
            ]),
            ("Protection", [
                "Which insurances must the contractor hold (for example contractor's all risks and third-party liability), and for how long?",
                "What are the grounds and procedure for termination by either side?",
                "How are disputes resolved, and in which forum? Ask your lawyer about statutory liability for structural defects under UAE law.",
            ]),
        ],
        "note": "This is not legal advice. Take advice from a UAE-qualified lawyer before you sign any consultancy or construction contract.",
    },
    {
        "n": "05", "title": "During construction: monthly checks",
        "intro": "Once work starts, a short, disciplined monthly review catches problems while they are still small. "
                 "This is what we would want to know every month if it were our own house.",
        "groups": [
            ("Progress and programme", [
                "Compare progress with the agreed programme and the critical path, not just the percentage complete.",
                "Ask for dated site photographs and a short written report from the consultant and the contractor.",
                "Check that staged authority inspections (for example shoring and foundations, and each slab) have been booked and passed before work is covered up.",
                "Review the look-ahead for the next two months: long-lead items, approvals and decisions needed from you.",
            ]),
            ("Money", [
                "Check each payment application against work actually completed and verified, before you pay.",
                "Keep a variations log: what was instructed, by whom, the agreed price and the effect on the programme.",
                "Track committed and forecast cost against the budget and the remaining contingency.",
                "Confirm that guarantees and insurances are still valid and will not expire before completion.",
            ]),
            ("Quality and records", [
                "Confirm that samples, materials and shop drawings were approved before installation.",
                "Look for open quality issues and check that they are being closed, not carried forward.",
                "Keep every instruction, approval and decision in writing, in one place you control.",
                "Record any delay events promptly, with dates and causes, while the facts are fresh.",
            ]),
        ],
        "note": "Statutory supervision is the role of your registered consultant. These are the owner's checks, alongside that supervision.",
    },
    {
        "n": "06", "title": "Snagging and handover",
        "intro": "Handover is your last point of real leverage. Once the final payment and retention are released, "
                 "getting a contractor back becomes much harder.",
        "groups": [
            ("Before you accept the house", [
                "Walk every room with a written snag list, with photographs and locations, and agree a date for each item to be closed.",
                "Witness the testing and commissioning of air conditioning, water, electrical, pool and smart-home systems, rather than accepting a certificate alone.",
                "Confirm the completion inspection has been passed and the completion certificate issued, and that utility connections are live.",
                "Check outstanding variations and claims are agreed in writing before the final account is settled.",
            ]),
            ("Documents and keys", [
                "Collect as-built drawings, operation and maintenance manuals, test certificates and equipment warranties.",
                "Get a schedule of all keys, codes, remotes and access cards, and change codes once you take possession.",
                "Record meter readings and confirm who pays utilities from which date.",
            ]),
            ("The defects period", [
                "Keep a dated defects diary from the first day you move in, with photographs.",
                "Notify defects in writing, as the contract requires, and well before the end of the defects period.",
                "Release retention only when the defects list is closed and the documents are complete.",
            ]),
        ],
        "note": "A professional snagging inspection is worth its fee on a new villa. Book it before handover, not after.",
    },
]

SOURCES = [
    ("Real Estate Club Dubai: villa architects and build costs (contingency, timelines)", "https://realestateclubdubai.com/dubai-villa-architects"),
    ("Dubai Municipality: single window for building permits", "https://www.dm.gov.ae/dubai-launches-single-window-for-building-permits/"),
    ("Dubai Municipality: new building permits app with consultant and contractor registry", "https://www.dm.gov.ae/new-improved-building-permits-app-launched-for-streamlined-services/"),
    ("Dubai Municipality: residential building permits procedures (staged inspections, completion)", "https://stgportalnew.dm.gov.ae/wp-content/uploads/2020/06/Residential-Buildings_Building-Permits-Procedures.pdf"),
    ("Dubai Municipality: contract forms for private villas", "https://www.dm.gov.ae/municipality-business/guidance-contracts-forms-for-engineering-consulting-services-and-construction-contracting-for-private-villas/"),
    ("Gulf News: Dubai Municipality warns consultancies over inflated villa designs", "https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704"),
    ("Abu Dhabi DMT: amendments to private villas regulations", "https://www.dmt.gov.ae/en/Media-Centre/News/Department-of-Municipalities-and-Transport-Announces-Amendments-to-Private-Villas-Regulations"),
]

# ---------------------------------------------------------------- styles
def styles():
    return {
        "h1": ParagraphStyle("h1", fontName=SERIF, fontSize=30, leading=34, textColor=INK, spaceAfter=10),
        "kicker": ParagraphStyle("kicker", fontName=SANS_B, fontSize=7.5, leading=10, textColor=BRASS, spaceAfter=6),
        "intro": ParagraphStyle("intro", fontName=SERIF, fontSize=13.5, leading=19, textColor=INK_SOFT, spaceAfter=14),
        "h3": ParagraphStyle("h3", fontName=SANS_B, fontSize=8, leading=11, textColor=INK, spaceBefore=10, spaceAfter=4),
        "item": ParagraphStyle("item", fontName=SANS, fontSize=9.6, leading=13.6, textColor=INK),
        "body": ParagraphStyle("body", fontName=SANS, fontSize=10, leading=15, textColor=INK, spaceAfter=8),
        "small": ParagraphStyle("small", fontName=SANS, fontSize=8, leading=11.5, textColor=INK_SOFT, spaceAfter=4),
        "note": ParagraphStyle("note", fontName=SERIF_I, fontSize=11, leading=15, textColor=INK_SOFT),
    }

# ---------------------------------------------------------------- flowables
class Box(Flowable):
    """An empty tick box."""
    def __init__(self, size=3.4 * mm):
        super().__init__(); self.size = size
    def wrap(self, aw, ah):
        return self.size, self.size + 1.2 * mm
    def draw(self):
        c = self.canv
        c.setStrokeColor(BRASS); c.setLineWidth(0.8)
        c.rect(0, 0, self.size, self.size, stroke=1, fill=0)

class Rule(Flowable):
    def __init__(self, width=None, color=STONE_2, thick=0.6, space=4):
        super().__init__(); self.w, self.color, self.thick, self.space = width, color, thick, space
    def wrap(self, aw, ah):
        self.aw = self.w or aw
        return self.aw, self.space * 2
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.thick)
        self.canv.line(0, self.space, self.aw, self.space)

def check_rows(items, st, width):
    rows = [[Box(), Paragraph(t, st["item"])] for t in items]
    t = Table(rows, colWidths=[7 * mm, width - 7 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (0, -1), 7.2), ("TOPPADDING", (1, 0), (1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, STONE_2),
    ]))
    return t

def note_box(text, st, width):
    t = Table([[Paragraph(text, st["note"])]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), STONE),
        ("LINEBEFORE", (0, 0), (0, -1), 2, BRASS_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t

# ---------------------------------------------------------------- page furniture
W, H = A4
M_L, M_R, M_T, M_B = 22 * mm, 22 * mm, 26 * mm, 22 * mm

def logo_mark(c, x, y, s, stroke=white):
    """The Eastbridge keystone-arch mark (owner's choice, 5 November 2026), drawn at (x, y) bottom-left, size s.
    The arch takes `stroke` as its colour; the keystone is brass."""
    k = s / 48.0
    X = lambda v: x + v * k
    Y = lambda v: y + (48 - v) * k
    c.saveState(); c.setFillColor(stroke); c.setStrokeColor(stroke)
    p = c.beginPath()
    p.moveTo(X(5), Y(44)); p.lineTo(X(5), Y(25))
    p.arcTo(X(5), Y(44), X(43), Y(6), startAng=180, extent=-180)   # outer arc, centre (24, 25), r 19
    p.lineTo(X(43), Y(44)); p.lineTo(X(35), Y(44)); p.lineTo(X(35), Y(25))
    p.arcTo(X(13), Y(36), X(35), Y(14), startAng=0, extent=180)    # inner arc, r 11
    p.lineTo(X(13), Y(44)); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(HexColor("#CFAE72") if stroke != INK else HexColor("#7A5C2C"))
    q = c.beginPath(); q.moveTo(X(21), Y(6)); q.lineTo(X(27), Y(6)); q.lineTo(X(25.75), Y(14.6)); q.lineTo(X(22.25), Y(14.6)); q.close()
    c.drawPath(q, stroke=0, fill=1)
    c.restoreState()

def draw_tracked(c, x, y, text, font, size, space, color):
    c.saveState(); c.setFillColor(color)
    t = c.beginText(x, y); t.setFont(font, size); t.setCharSpace(space); t.textLine(text); c.drawText(t)
    c.restoreState()

def cover(c, doc):
    c.saveState()
    c.setFillColor(SLATE); c.rect(0, 0, W, H, stroke=0, fill=1)
    # subtle architectural lines, kept clear of the text
    c.setStrokeColor(SLATE_2); c.setLineWidth(0.6)
    for i in range(1, 9):
        c.line(W * i / 9, H * 0.36 - 30 * mm, W * i / 9, H * 0.36 - 60 * mm)
    c.setStrokeColor(BRASS_LIGHT); c.setLineWidth(0.8)
    c.line(M_L, H * 0.36, W - M_R, H * 0.36)
    logo_mark(c, M_L, H - M_T - 12 * mm, 12 * mm)
    draw_tracked(c, M_L + 16 * mm, H - M_T - 5 * mm, "Eastbridge", SERIF, 16.0, 0, white)
    draw_tracked(c, M_L + 16 * mm, H - M_T - 10 * mm, "STRATEGIC PARTNERS", SANS, 6.3, 2.2, MUTED_DARK)
    draw_tracked(c, M_L, H * 0.68, "A FREE GUIDE FOR VILLA OWNERS", SANS_B, 8, 2.2, BRASS_LIGHT)
    c.setFillColor(white); c.setFont(SERIF, 44)
    y = H * 0.68 - 22 * mm
    for line in ["The Villa Owner\u2019s", "Pre-Construction", "Checklist"]:
        c.drawString(M_L, y, line); y -= 15.5 * mm
    c.setFont(SERIF_I, 22); c.setFillColor(BRASS_LIGHT); c.drawString(M_L, y + 1 * mm, SUBTITLE)
    c.setFillColor(MUTED_DARK); c.setFont(SANS, 10.5)
    ty = H * 0.36 - 14 * mm
    for line in ["Practical checks for every stage of a private villa build or renovation:",
                 "the plot, the brief and budget, choosing your team, the contract,",
                 "monthly checks on site, and snagging and handover."]:
        c.drawString(M_L, ty, line); ty -= 5.6 * mm
    c.setFillColor(white); c.setFont(SANS_M, 9)
    c.drawString(M_L, M_B + 8 * mm, f"Written by {C.FOUNDER['name']}, {C.FOUNDER['role']}")
    c.setFillColor(MUTED_DARK); c.setFont(SANS, 8.5)
    c.drawString(M_L, M_B + 3 * mm, f"{C.FOUNDED_TRACK_RECORD_YEARS} years running {C.FOUNDER['company_uk']}, now on the client\u2019s side of the table.")
    c.drawRightString(W - M_R, M_B + 3 * mm, C.SITE_URL.replace("https://", ""))
    c.restoreState()

def body_page(c, doc):
    c.saveState()
    logo_mark(c, M_L, H - 15 * mm, 6 * mm, stroke=INK)
    draw_tracked(c, M_L + 8.5 * mm, H - 12.4 * mm, "Eastbridge", SERIF, 11.2, 0, INK)
    draw_tracked(c, W - M_R - 72 * mm, H - 12.4 * mm, "PRE-CONSTRUCTION CHECKLIST", SANS, 6.5, 1.6, INK_SOFT)
    c.setStrokeColor(STONE_2); c.setLineWidth(0.6); c.line(M_L, H - 17.5 * mm, W - M_R, H - 17.5 * mm)
    c.line(M_L, 15 * mm, W - M_R, 15 * mm)
    c.setFont(SANS, 6.8); c.setFillColor(INK_SOFT)
    c.drawString(M_L, 10.5 * mm, "General information, not advice for your specific project. Eastbridge represents the owner alongside the owner\u2019s registered consultant.")
    c.setFont(SANS_M, 7.5); c.setFillColor(INK)
    c.drawRightString(W - M_R, 10.5 * mm, str(doc.page))
    c.restoreState()

def back_page(c, doc):
    c.saveState()
    c.setFillColor(SLATE); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(SLATE_2); c.setLineWidth(0.6)
    for i in range(1, 9):
        c.line(W * i / 9, H * 0.82, W * i / 9, H)
    c.setStrokeColor(BRASS_LIGHT); c.setLineWidth(0.8); c.line(M_L, H * 0.82, W - M_R, H * 0.82)
    logo_mark(c, M_L, M_B + 4 * mm, 10 * mm)
    draw_tracked(c, M_L + 14 * mm, M_B + 10 * mm, "Eastbridge", SERIF, 14.4, 0, white)
    draw_tracked(c, M_L + 14 * mm, M_B + 5.5 * mm, "STRATEGIC PARTNERS", SANS, 6, 2, MUTED_DARK)
    c.restoreState()

# ---------------------------------------------------------------- document
def build():
    register_fonts()
    st = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
                          title=f"{TITLE} ({SUBTITLE})".replace("'", "\u2019"), author=f"{C.NAME}",
                          subject="Practical pre-construction checklists for private villa owners in Dubai and Abu Dhabi",
                          creator=C.NAME, keywords="villa, Dubai, Abu Dhabi, checklist, owner's representative, project management")
    fw = W - M_L - M_R
    frame = Frame(M_L, M_B, fw, H - M_T - M_B, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    back_frame = Frame(M_L, M_B + 22 * mm, fw, H * 0.82 - M_B - 22 * mm - 14 * mm, id="b",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover),
        PageTemplate(id="body", frames=[frame], onPage=body_page),
        PageTemplate(id="back", frames=[back_frame], onPage=back_page),
    ])

    s = [NextPageTemplate("body"), PageBreak()]

    # --- how to use
    s += [Paragraph("BEFORE YOU START", st["kicker"]),
          Paragraph("How to use this checklist", st["h1"]),
          Paragraph("Building a villa is a long chain of decisions, and the costly ones are usually made early. "
                    "This checklist follows a private villa project from the plot to the end of the defects period, "
                    "and lists the questions we would want answered at each stage if it were our own house.", st["intro"])]
    s += [Paragraph("We spent 21 years on the builder's side of the table. Our founder, Philip Chapman, ran "
                    "P Chapman Construction, a premium residential builder in the UK, and saw at first hand where budgets leak, how "
                    "variations and delay claims are built, and what contractors hope clients will not check. "
                    "Eastbridge now sits on the owner's side.", st["body"]),
          Paragraph("Tick each item as it is answered, and keep the evidence: a document, an email or a signed "
                    "drawing. An item you cannot tick is a question to put to your consultant, your contractor or your lawyer.", st["body"]),
          Spacer(1, 6)]
    roles = [
        [Paragraph("<b>Who does what</b>", st["item"]), ""],
        [Paragraph("Registered consultant", st["item"]),
         Paragraph("Designs the villa, makes the authority submissions and carries out statutory supervision. Appointed by you; must be registered with the relevant authority.", st["item"])],
        [Paragraph("Contractor", st["item"]),
         Paragraph("Builds the villa under the construction contract. Appointed by you.", st["item"])],
        [Paragraph("Client-side project manager", st["item"]),
         Paragraph("Represents you alongside your consultant and contractor: cost and programme control, independent site visits and reporting, and commercial and contractual advice. This is the role Eastbridge plays.", st["item"])],
        [Paragraph("UAE-qualified lawyer", st["item"]),
         Paragraph("Advises on the plot purchase and on the consultancy and construction contracts.", st["item"])],
    ]
    rt = Table(roles, colWidths=[46 * mm, fw - 46 * mm])
    rt.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)), ("BACKGROUND", (0, 0), (-1, 0), STONE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, STONE_2),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    s += [rt, Spacer(1, 14)]
    contents = [[Paragraph(f'<font color="#8B6A33">{x["n"]}</font>', st["item"]), Paragraph(x["title"], st["item"])] for x in STAGES]
    ct = Table([[Paragraph("<b>Inside</b>", st["item"]), ""]] + contents, colWidths=[12 * mm, fw - 12 * mm])
    ct.setStyle(TableStyle([("SPAN", (0, 0), (1, 0)), ("LINEBELOW", (0, 0), (-1, -1), 0.4, STONE_2),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    s += [ct]

    # --- stages
    for stg in STAGES:
        s += [PageBreak(), Paragraph(f"STAGE {stg['n']}", st["kicker"]), Paragraph(stg["title"], st["h1"]),
              Paragraph(stg["intro"], st["intro"])]
        for head, items in stg["groups"]:
            s += [KeepTogether([Paragraph(head.upper(), st["h3"]), Rule(color=BRASS_LIGHT, thick=0.8, space=2),
                                check_rows(items[:2], st, fw)])]
            if len(items) > 2:
                s += [check_rows(items[2:], st, fw)]
        s += [Spacer(1, 12), KeepTogether([note_box(stg["note"], st, fw)])]

    # --- sources
    s += [CondPageBreak(70 * mm), Spacer(1, 18), Paragraph("SOURCES", st["kicker"])]
    for title, link in SOURCES:
        s += [Paragraph(f'{title}. <link href="{link}" color="#8B6A33">{link}</link>', st["small"])]
    s += [Spacer(1, 6), Paragraph(f"Published by {C.NAME}, {datetime.date.today().strftime('%B %Y')}. Regulations, fees and "
                                  "procedures change; check current requirements with the relevant authority and your registered consultant.", st["small"])]

    # --- notes
    s += [Spacer(1, 22), Paragraph("YOUR PROJECT NOTES", st["kicker"]),
          Paragraph("Questions to raise, decisions pending and who owns them.", st["small"])]
    s += [Rule(color=STONE_2, thick=0.6, space=11) for _ in range(12)]

    # --- back page
    w_ = ParagraphStyle("w", parent=st["body"], textColor=white)
    m_ = ParagraphStyle("m", parent=st["body"], textColor=MUTED_DARK, fontSize=9.5, leading=14)
    h_ = ParagraphStyle("hb", parent=st["h1"], textColor=white, fontSize=28, leading=33)
    k_ = ParagraphStyle("kb", parent=st["kicker"], textColor=BRASS_LIGHT)
    s += [NextPageTemplate("back"), PageBreak(),
          Paragraph("TALK IT THROUGH", k_),
          Paragraph("Your villa, managed from your side of the table.", h_), Spacer(1, 6),
          Paragraph("Eastbridge Strategic Partners is an independent, client-side project manager for private villa builds "
                    "and renovations in Dubai and Abu Dhabi. We represent the owner, alongside the owner's registered "
                    "consultant and the contractor: cost and programme control, independent site visits and reporting, "
                    "and commercial and contractual advice. We are paid only by the owner we represent and take no commissions from "
                    "contractors or suppliers.", w_),
          Paragraph("If you are planning a villa, the first conversation is free and confidential. "
                    f"{C.RESPONSE_PROMISE}.", w_), Spacer(1, 14)]
    lab = ParagraphStyle("lab", parent=st["kicker"], textColor=BRASS_LIGHT, spaceAfter=0)
    val = ParagraphStyle("val", parent=st["body"], textColor=white, fontSize=11, leading=15, spaceAfter=0)
    site = C.SITE_URL.replace("https://", "")
    rows = [
        ("EMAIL", f'<link href="mailto:{C.EMAIL}">{C.EMAIL}</link>'),
        ("PHONE AND WHATSAPP", f'<link href="https://wa.me/{C.WHATSAPP}">{C.PHONE_DISPLAY}</link>'),
        ("WEBSITE", f'<link href="{C.SITE_URL}/contact/">{site}</link>'),
        ("OFFICE", f'{C.ADDRESS["street"]}, {C.ADDRESS["locality"]}, {C.ADDRESS["country_name"]}'),
        ("HOURS", C.HOURS),
    ]
    tt = Table([[Paragraph(a, lab), Paragraph(b, val)] for a, b in rows], colWidths=[44 * mm, fw - 44 * mm])
    tt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                            ("LINEBELOW", (0, 0), (-1, -1), 0.4, SLATE_2)]))
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
    import shutil, subprocess
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
        dst = OUT.with_name("villa-owner-checklist-cover.webp")
        im.save(dst, "WEBP", quality=82, method=6)
        print(f"Wrote {dst.relative_to(ROOT)} ({im.width}x{im.height})")

if __name__ == "__main__":
    build()
